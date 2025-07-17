package modules

import (
	"fmt"
	"log"
	"net"
	"os"
	"regexp"
	"strings"
	"time"

	"github.com/likexian/whois"
	"github.com/likexian/whois-parser"
)

// ##############################
//
// # HELPER FUNCTIONS
//
// ##############################

func cleanDate(dateStr string) string {
	if dateStr == "" {
		return "N/A"
	}
	parsedTime, err := time.Parse(time.RFC3339, dateStr)
	if err != nil {
		return dateStr
	}
	return parsedTime.Format("2006-01-02 15:04:05")
}

func fileExists(filename string) bool {
	info, err := os.Stat(filename)
	if os.IsNotExist(err) {
		return false
	}
	return !info.IsDir()
}

func extractEmails(raw string) []string {
	emailRegex := regexp.MustCompile(`[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}`)
	matches := emailRegex.FindAllString(raw, -1)
	unique := make(map[string]bool)
	for _, email := range matches {
		unique[email] = true
	}
	var emails []string
	for email := range unique {
		emails = append(emails, email)
	}
	return emails
}

func extractField(raw, fieldName string) string {
	lines := strings.Split(raw, "\n")
	fieldName = strings.ToLower(fieldName)
	for _, line := range lines {
		lowerLine := strings.ToLower(line)
		if strings.Contains(lowerLine, fieldName) {
			parts := strings.SplitN(line, ":", 2)
			if len(parts) == 2 {
				return strings.TrimSpace(parts[1])
			}
		}
	}
	return ""
}

// ##############################
//
// # IP ADDRESS
//
// ##############################

func GetIPAddresses(targetDomainName string) {
	fmt.Println("=== IP Addresses ===")
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

func GetNameservers(targetDomainName string) {
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

func GetMXRecords(targetDomainName string) {
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

func GetWHOIS(targetDomainName string) {
	fmt.Println("=== WHOIS ===")
	rawResult, err := whois.Whois(targetDomainName)
	if err != nil {
		log.Println("WHOIS error:", err)
		return
	}

	parsed, err := whoisparser.Parse(rawResult)
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

	// Nameservers (extract manually from raw WHOIS)
	nsRaw := extractField(rawResult, "Name Server")
	if nsRaw == "" {
		nsRaw = extractField(rawResult, "Name Servers")
	}
	if nsRaw != "" {
		fmt.Println("Nameservers:", nsRaw)
	} else {
		fmt.Println("Nameservers: N/A")
	}

	// Emails
	emails := extractEmails(rawResult)
	if len(emails) > 0 {
		fmt.Printf("Contact Emails: %s\n", strings.Join(emails, ", "))
	} else {
		fmt.Println("Contact Emails: N/A")
	}

	// Registrant organization
	org := parsed.Registrant.Organization
	if org == "" {
		org = extractField(rawResult, "Registrant Organization")
	}
	if org == "" {
		org = "N/A"
	}
	fmt.Println("Registrant Organization:", org)

	// Abuse contact
	abuseContact := extractField(rawResult, "Abuse Contact Email")
	if abuseContact == "" {
		abuseContact = "N/A"
	}
	fmt.Println("Abuse Contact:", abuseContact)

	// DNSSEC
	dnssec := extractField(rawResult, "DNSSEC")
	if dnssec == "" {
		dnssec = "Not implemented"
	}
	fmt.Println("DNSSEC:", dnssec)

	// Domain status
	status := extractField(rawResult, "Status")
	if status == "" {
		status = "N/A"
	}
	fmt.Println("Domain Status:", status)
}

// ##############################
//
// # FULL DOMAIN INFO
//
// ##############################

func GetDomainInfo(targetDomainName string) {
	startTime := time.Now()

	GetIPAddresses(targetDomainName)
	GetNameservers(targetDomainName)
	GetMXRecords(targetDomainName)
	GetWHOIS(targetDomainName)

	duration := time.Since(startTime).Seconds()
	fmt.Printf("\nDuration: %.2f seconds.\n", duration)
}