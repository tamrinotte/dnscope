package main

import (
	"fmt"
	"log"
	"flag"
	"net"
	"github.com/likexian/whois"
	"github.com/likexian/whois-parser"
	"time"
    "os"
    "bufio"
    "sync"
)

// ##############################
//
// # MAIN
//
// ##############################

func main() {
	domainPointer := flag.String("domain", "example.com", "Target domain name.")
	wordlistPointer := flag.String("wordlist", "subdomains.txt", "Path to your wordlist file.")
	flag.Usage = func() {
		fmt.Println("Usage: dnscope [flags]")
		flag.PrintDefaults()
		fmt.Println("\nExamples:")
		fmt.Println("  dnscope -domain=example.com")
		fmt.Println("  dnscope -domain=example.com -wordlist=subdomains.txt")
	}
	flag.Parse()
	if *domainPointer != "" {
		getIPAddresses(*domainPointer)
		getNameservers(*domainPointer)
		getMXRecords(*domainPointer)
		getWHOIS(*domainPointer)
		if *wordlistPointer != "" && !fileExists(*wordlistPointer) {
			message := fmt.Sprintf("\nWordlist file '%s' does not exist. Skipping subdomain scan.\n", *wordlistPointer)
			fmt.Println(message)
		} else if *wordlistPointer == "" {
			fmt.Println("\nSkipping subdomain scan. Use -wordlist flag to specify a wordlist file.")
		} else {
			getSubdomains(*wordlistPointer, *domainPointer)
		}
	} else {
		flag.Usage()
		os.Exit(1)
	}
}

// ##############################
//
// # HELPER FUNCTIONS
//
// ##############################

func fileExists(filename string) bool {
	info, err := os.Stat(filename)
	if os.IsNotExist(err) {
		return false
	}
	return !info.IsDir()
}

func cleanDate(dateStr string) string {
    if dateStr == "" {
        return "N/A"
    }
    parsedTime, err := time.Parse(time.RFC3339, dateStr)
    if err != nil {
        return dateStr // fallback to raw string if can't parse
    }
    return parsedTime.Format("2006-01-02 15:04:05")
}

// ##############################
//
// # IP ADDRESS
//
// ##############################

func getIPAddresses(targetDomainName string) {
	fmt.Println("=== IP Address ===")
	addresses, err := net.LookupIP(targetDomainName)
	if err != nil {
		log.Println(err)
		return
	}
	for index, address := range addresses {
		fmt.Printf("%d) %s\n", index+1, address)
	}
}

// ##############################
//
// # NAMESERVERS
//
// ##############################

func getNameservers(targetDomainName string) {
    fmt.Println("=== Nameservers ===")
    nsRecords, err := net.LookupNS(targetDomainName)
    if err != nil {
        log.Println(err)
        return
    }

    for index, nsRecord := range nsRecords {
        fmt.Printf("%d) %s\n", index+1, nsRecord.Host)
    }
}

// ##############################
//
// # MX RECORDS
//
// ##############################

func getMXRecords(targetDomainName string) {
    fmt.Println("=== MX Records ===")
    mxRecords, err := net.LookupMX(targetDomainName)
    if err != nil {
        log.Println(err)
        return
    }
    for index, mxRecord := range mxRecords {
        fmt.Printf("%d) %s priority: %d\n", index+1, mxRecord.Host, mxRecord.Pref)
    }
}

// ##############################
//
// # WHOIS
//
// ##############################

func getWHOIS(targetDomainName string) {
    fmt.Println("=== WHOIS ===")
    result, err := whois.Whois(targetDomainName)
    if err != nil {
        log.Println("WHOIS error:", err)
        return
    }
    parsed, err := whoisparser.Parse(result)
    if err != nil {
        log.Println("Parse error:", err)
        return
    }
    fmt.Println("Registrar:", parsed.Registrar.Name)
    registrant := parsed.Registrant.Name
    if registrant == "" {
        registrant = "None"
    }
    fmt.Println("Registrant:", registrant)
    creationDate := cleanDate(parsed.Domain.CreatedDate)
    expirationDate := cleanDate(parsed.Domain.ExpirationDate)
    fmt.Println("Creation Date:", creationDate)
    fmt.Println("Expiration Date:", expirationDate)
}

// ##############################
//
// # SUBDOMAINS
//
// ##############################

func getSubdomains(wordlistPath string, targetDomain string) {
	fmt.Println("=== Subdomains ===")

	// Open wordlist file
	file, err := os.Open(wordlistPath)
	if err != nil {
		log.Println(err)
		return
	}
	defer file.Close()

	// Create a wait group for goroutines
	var wg sync.WaitGroup

	// Create a channel for results
	results := make(chan string)

	// Read wordlist file line by line
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		subdomain := scanner.Text()

		// Start a new goroutine for each subdomain
		wg.Add(1)
		go func(subdomain string) {
			defer wg.Done()

			// Construct full domain
			fullDomain := fmt.Sprintf("%s.%s", subdomain, targetDomain)

			// Check if subdomain exists
			if exists, _ := net.LookupIP(fullDomain); exists != nil {
				results <- fullDomain
			}
		}(subdomain)
	}

	// Close results channel when all goroutines finish
	go func() {
		wg.Wait()
		close(results)
	}()

	// Print results
	for result := range results {
		fmt.Println(result)
	}

	if err := scanner.Err(); err != nil {
		log.Println(err)
	}
}