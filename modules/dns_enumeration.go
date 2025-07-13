package modules

import (
	"bufio"
	"context"
	"fmt"
	"log"
	"net"
	"os"
	"sync"
	"time"
)

// ##############################
//
// # CONSTANTS
//
// ##############################

// max concurrent DNS lookups
const maxConcurrentLookups = 50

// ##############################
//
// # SUBDOMAINS
//
// ##############################

func GetSubdomains(targetDomain string, wordlistPath string) {
	start := time.Now()
	fmt.Println("=== Subdomains ===")

	// Open wordlist file
	file, err := os.Open(wordlistPath)
	if err != nil {
		log.Println("Error opening wordlist:", err)
		return
	}
	defer file.Close()

	// Channel to limit concurrency
	sem := make(chan struct{}, maxConcurrentLookups)

	// WaitGroup for goroutines
	var wg sync.WaitGroup

	// Channel for results
	results := make(chan string)

	// Custom resolver with timeout
	resolver := &net.Resolver{}

	// Read wordlist line by line
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		subdomain := scanner.Text()
		if subdomain == "" {
			continue
		}

		wg.Add(1)
		sem <- struct{}{} // acquire token

		go func(sub string) {
			defer wg.Done()
			defer func() { <-sem }() // release token

			fullDomain := fmt.Sprintf("%s.%s", sub, targetDomain)

			// Context with timeout for lookup
			ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
			defer cancel()

			ips, err := resolver.LookupIP(ctx, "ip", fullDomain)
			if err != nil {
				// Optionally log DNS errors if needed, e.g.:
				// log.Printf("Lookup failed for %s: %v", fullDomain, err)
				return
			}
			if len(ips) > 0 {
				results <- fullDomain
			}
		}(subdomain)
	}

	// Close results channel once all lookups complete
	go func() {
		wg.Wait()
		close(results)
	}()

	// Print results as they come in
	for result := range results {
		fmt.Println(result)
	}

	if err := scanner.Err(); err != nil {
		log.Println("Error reading wordlist:", err)
	}

	duration := time.Since(start).Seconds()
	fmt.Printf("DNS enumeration completed in %.2f seconds.\n", duration)
}