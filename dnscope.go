package main

import (
	"flag"
	"fmt"
	"os"
	"dnscope/modules"
)

func main() {
	// Define flags
	domain := flag.String("domain", "", "Target domain name.")
	gatherDomainInfo := flag.Bool("gdi", false, "Gather information about the target domain.")
	dnsEnum := flag.Bool("dns", false, "Enumerate subdomains.")
	dirEnum := flag.Bool("dir", false, "Enumerate directories.")
	wordlist := flag.String("wordlist", "wordlist.txt", "Path to your wordlist file.")
	recursiveDepth := flag.Int("r", 3, "Max recursion depth for directory enumeration.")

	flag.Usage = func() {
		fmt.Println("Usage: dnscope [flags]")
		flag.PrintDefaults()
		fmt.Println("\nExamples:")
		fmt.Println("  dnscope -domain=example.com -gdi")
		fmt.Println("  dnscope -domain=example.com -dns -wordlist=subdomains.txt")
		fmt.Println("  dnscope -domain=example.com -dir -wordlist=dirs.txt")
		fmt.Println("  dnscope -domain=example.com -gdi -dns -wordlist=subdomains.txt")
		fmt.Println("  dnscope -domain=example.com -gdi -dir -wordlist=dirs.txt")
		fmt.Println("  dnscope -domain=example.com -gdi -dir -wordlist=dirs.txt -r=3")
	}

	flag.Parse()

	// Validate required domain
	if *domain == "" {
		fmt.Println("Error: -domain is required.")
		flag.Usage()
		os.Exit(1)
	}

	// Enforce mutual exclusivity manually
	selectedCount := 0
	if *dnsEnum {
		selectedCount++
	}
	if *dirEnum {
		selectedCount++
	}
	if selectedCount > 1 {
		fmt.Println("Error: Only one of -dns or -dir can be specified at a time.")
		flag.Usage()
		os.Exit(1)
	}

	// Run requested modules
	if *gatherDomainInfo {
		fmt.Println("Gathering domain information for", *domain)
		modules.GetDomainInfo(*domain)
	}

	if *dnsEnum {
		fmt.Println("Enumerating subdomains for", *domain, "using", *wordlist)
		modules.GetSubdomains(*domain, *wordlist)
	}

	if *dirEnum {
		isRecursive := false
		if *recursiveDepth > 0 {
			isRecursive = true
		}
		fmt.Printf("Enumerating directories for %s using %s (recursive: %v, depth: %d)\n",
			*domain, *wordlist, isRecursive, *recursiveDepth)
		modules.GetDirs(*domain, isRecursive, *recursiveDepth, *wordlist, 30)
	}
}