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

func GetDir(url string, fakeUserAgents []string, timeout time.Duration, retries int) (*DirResult, error) {
    client := &http.Client{
        Timeout: timeout,
        // Default Redirect behavior is enabled, no change needed unless overridden
    }

    for attempt := 0; attempt <= retries; attempt++ {
        userAgent := "Mozilla/5.0"
        if len(fakeUserAgents) > 0 {
            userAgent = fakeUserAgents[rand.Intn(len(fakeUserAgents))]
        }

        req, err := http.NewRequest("GET", url, nil)
        if err != nil {
            return nil, fmt.Errorf("creating request failed: %w", err)
        }

        req.Header.Set("User-Agent", userAgent)
        req.Header.Set("Referer", url)
        req.Header.Set("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
        req.Header.Set("Accept-Language", "en-US,en;q=0.9")

        resp, err := client.Do(req)
        if err != nil {
            log.Printf("Request to %s failed (attempt %d/%d): %v", url, attempt+1, retries+1, err)
            time.Sleep(500 * time.Millisecond) // Slightly longer backoff
            continue
        }

        io.Copy(io.Discard, resp.Body)
        resp.Body.Close()

        // Accept common success and redirect codes
        if resp.StatusCode == 200 || resp.StatusCode == 301 || resp.StatusCode == 302 || resp.StatusCode == 403 {
            return &DirResult{URL: url, StatusCode: resp.StatusCode}, nil
        }

        // Continue on other codes without error to keep scanning
        return nil, nil
    }

    return nil, fmt.Errorf("all retries failed for %s", url)
}

// ##############################
//
// # ENUMERATE DIRECTORIES
//
// ##############################

func GetDirs(targetDomain string, isRecursive bool, maxDepth int, wordlistPath string, maxWorkers int) {
	startTime := time.Now()

	fakeUserAgents, err := LoadUserAgents()
	if err != nil {
		log.Println("Failed to load embedded fake user agents:", err)
		fakeUserAgents = []string{}
	}

	file, err := os.Open(wordlistPath)
	if err != nil {
		log.Printf("Failed to open wordlist file %s: %v\n", wordlistPath, err)
		return
	}
	defer file.Close()

	var directories []string
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

	type Job struct {
		URL   string
		Depth int
	}

	jobs := make(chan Job)
	results := make(chan *DirResult)

	var wg sync.WaitGroup
	var jobsWg sync.WaitGroup // tracks outstanding jobs

	if maxWorkers <= 0 {
		maxWorkers = runtime.NumCPU() * 2
	}

	worker := func() {
		defer wg.Done()
		for job := range jobs {
			for _, dir := range directories {
				fullURL := job.URL + dir
				result, err := GetDir(fullURL, fakeUserAgents, 2500*time.Millisecond, 1)
				if err == nil && result != nil {
					result.Depth = job.Depth
					results <- result
					if isRecursive && job.Depth < maxDepth {
						// Add new job before sending to channel
						jobsWg.Add(1)
						jobs <- Job{URL: fullURL + "/", Depth: job.Depth + 1}
					}
				}
			}
			jobsWg.Done()
		}
	}

	wg.Add(maxWorkers)
	for i := 0; i < maxWorkers; i++ {
		go worker()
	}

	// Start initial job
	jobsWg.Add(1)
	go func() {
		jobs <- Job{URL: "http://" + targetDomain + "/", Depth: 0}
	}()

	// Close jobs channel when all jobs are processed
	go func() {
		jobsWg.Wait()
		close(jobs)
	}()

	foundDirs := make([]*DirResult, 0)
	done := make(chan struct{})

	go func() {
		for res := range results {
			foundDirs = append(foundDirs, res)
		}
		done <- struct{}{}
	}()

	wg.Wait()
	close(results)
	<-done

	// Print results
	fmt.Println("\n=== Discovered Directories ===")
	for i, dir := range foundDirs {
		fmt.Printf("%d) %s [Status: %d]\n", i+1, dir.URL, dir.StatusCode)
	}

	fmt.Printf("\nDuration: %.2f seconds.\n", time.Since(startTime).Seconds())
	log.Printf("Directory enumeration completed. Duration: %.2f seconds.", time.Since(startTime).Seconds())
}