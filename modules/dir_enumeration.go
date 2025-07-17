package modules

import (
	"bufio"
	_ "embed"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"math/rand"
	"net/http"
	"os"
	"runtime"
	"strings"
	"sync"
	"time"
)

// ##############################
//
// # EMBEDDED DATA
//
// ##############################

//go:embed data/fake_user_agents.json
var fakeUserAgentsData []byte

// ##############################
//
// # TYPES
//
// ##############################

// UserAgents struct to parse fake_user_agents.json
type UserAgents struct {
	UserAgents []string `json:"user_agents"`
}

// DirResult holds discovered directory URL and status code
type DirResult struct {
	URL        string
	StatusCode int
	Depth      int
}

// ##############################
//
// # LOAD USER AGENTS FROM EMBEDDED JSON
//
// ##############################

func LoadUserAgents() ([]string, error) {
	var ua UserAgents
	if err := json.Unmarshal(fakeUserAgentsData, &ua); err != nil {
		return nil, fmt.Errorf("failed to parse embedded user agents JSON: %w", err)
	}
	return ua.UserAgents, nil
}

// ##############################
//
// # GET SINGLE DIR
//
// ##############################

func GetDir(url string, fakeUserAgent string, timeout time.Duration, retries int) (*DirResult, error) {
	// Initialize a new http client
	client := &http.Client{
		Timeout: timeout,
	}

	for attempt := 0; attempt <= retries; attempt++ {
		// Set the user agent
		userAgent := "Mozilla/5.0"
		if fakeUserAgent != "" {
			userAgent = fakeUserAgent
		}

		// Declare a new request
		req, err := http.NewRequest("GET", url, nil)
		if err != nil {
			return nil, fmt.Errorf("creating request failed: %w", err)
		}

		// Set request headers
		req.Header.Set("User-Agent", userAgent)
		req.Header.Set("Referer", url)
		req.Header.Set("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
		req.Header.Set("Accept-Language", "en-US,en;q=0.9")

		// Send a http request 
		resp, err := client.Do(req)
		if err != nil {
			log.Printf("Request to %s failed (attempt %d/%d): %v", url, attempt+1, retries+1, err)
			time.Sleep(500 * time.Millisecond)
			continue
		}

		// Ensure that the entire HTTP response body is read and then closed properly
		io.Copy(io.Discard, resp.Body)
		resp.Body.Close()

		// Check the HTTP response code
		if resp.StatusCode == 200 || resp.StatusCode == 301 || resp.StatusCode == 302 || resp.StatusCode == 403 {
			// Return the directory if request gives an acceptable response status code
			return &DirResult{URL: url, StatusCode: resp.StatusCode}, nil
		}

		// If the status code does not match any of those interesting codes, the function returns errors
		return nil, nil
	}

	// Return error 
	return nil, fmt.Errorf("all retries failed for %s", url)
}

// ##############################
//
// # ENUMERATE DIRECTORIES
//
// ##############################

func GetDirs(targetDomain string, isRecursive bool, maxDepth int, wordlistPath string, maxWorkers int) {
	// Get the start time
	startTime := time.Now()

	// Load user agents
	fakeUserAgents, err := LoadUserAgents()
	if err != nil {
		log.Println("Failed to load embedded fake user agents:", err)
		fakeUserAgents = []string{}
	}

	// Pick one random user agent to use for all requests
	rand.Seed(time.Now().UnixNano())
	var selectedUserAgent string = fakeUserAgents[rand.Intn(len(fakeUserAgents))]

	// Open the wordlist file
	file, err := os.Open(wordlistPath)
	if err != nil {
		log.Printf("Failed to open wordlist file %s: %v\n", wordlistPath, err)
		return
	}
	// Schedule to close the file
	defer file.Close()

	// Create an empty slice to store directories that you will scan
	var directories []string

	// Create a sanner to read a the file line by line
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line != "" {
			directories = append(directories, line)
		}
	}
	if err := scanner.Err(); err != nil {
		log.Println("Error reading wordlist:", err)
		return
	}

	// Custom data type called Job
	type Job struct {
		URL   string
		Depth int
	}

	// Declare and initialize channels
	jobs := make(chan Job)
	results := make(chan *DirResult)

	// Declare wait groups to track and wait goroutines to finish
	var waitGroup sync.WaitGroup
	var jobsWaitGroup sync.WaitGroup

	// Set maxWorkers to twice of number of cpus available in your system if it's equal or less than 0
	if maxWorkers <= 0 {
		maxWorkers = runtime.NumCPU() * 2
	}

	// Create a worker that will scan a directory
	worker := func() {
		defer waitGroup.Done()
		for job := range jobs {
			for _, dir := range directories {
				fullURL := job.URL + dir
				result, err := GetDir(fullURL, selectedUserAgent, 2500*time.Millisecond, 1)
				if err == nil && result != nil {
					result.Depth = job.Depth
					results <- result
					if isRecursive && job.Depth < maxDepth {
						// Add new job before sending to channel
						jobsWaitGroup.Add(1)
						jobs <- Job{URL: fullURL + "/", Depth: job.Depth + 1}
					}
				}
			}
			jobsWaitGroup.Done()
		}
	}

	// Register maxWorkers number of goroutines with the waitGroup.
	waitGroup.Add(maxWorkers)
	// Launch a new worker for each iteration 
	for i := 0; i < maxWorkers; i++ {
		go worker()
	}

	// Start initial job
	jobsWaitGroup.Add(1)
	go func() {
		jobs <- Job{URL: "http://" + targetDomain + "/", Depth: 0}
	}()

	// Close the jobs channel when all jobs are processed
	go func() {
		jobsWaitGroup.Wait()
		close(jobs)
	}()
	
	// Collect results
	foundDirs := make([]*DirResult, 0)
	done := make(chan struct{})

	go func() {
		for res := range results {
			foundDirs = append(foundDirs, res)
		}
		done <- struct{}{}
	}()
	
	// Wait for all workers and finish
	waitGroup.Wait()
	close(results)
	<-done

	// Print results
	fmt.Println("\n=== Discovered Directories ===")
	for i, dir := range foundDirs {
		fmt.Printf("%d) %s [Status: %d]\n", i+1, dir.URL, dir.StatusCode)
	}

	// Calculate and print the duration of scan
	duration := time.Since(startTime).Seconds()
	fmt.Printf("\nDuration: %.2f seconds.\n", duration)
}