# DNScope
![DNScopeLogo](https://raw.githubusercontent.com/tamrinotte/dnscope/go/app_images/dnscope_logo.png)

DNScope is a lightweight reconnaissance utility designed for cybersecurity professionals, penetration testers, and digital investigators. The tool automates domain related metadata retrieval, DNS enumeration, and directory enumeration, providing a comprehensive snapshot of a target domain’s public-facing infrastructure and accessible directories.

It enumerates vital information including the domain's IP address, MX records, nameservers, WHOIS registration data, and performs subdomain brute-forcing and directory brute-focrcing using a customizable wordlists.

Built to be clean, efficient, and easily portable, DNScope helps analysts uncover open internet metadata and assess a domain’s external exposure surface with precision.

<br>

## Installation

1) Download the installer.

	- Kali

	      curl -L https://github.com/tamrinotte/dnscope/releases/download/go_kali_v1.1/dnscope.deb -o dnscope.deb

	- Debian

	      curl -L https://github.com/tamrinotte/dnscope/releases/download/go_debian_v1.1/dnscope.deb -o dnscope.deb

2) Start the installer.

       sudo dpkg -i dnscope.deb

<br>

## Options

__-h, --help:__ Displays the help message.

__-domain string:__ Target domain (e.g., -domain=example.com).

__-gdi:__ Gather information about the target domain.

__-dns:__ Enumerate subdomains. 

__-dir:__ Enumerate directories.

__-wordlist string:__ Subdomains wordlist file.

__-r int:__ Max recursion depth for directory enumeration. (default 3).

<br>

## Examples

1)
       dnscope -domain=example.com -gdi

2)
       dnscope -domain=example.com -dns -wordlist=subdomains.txt

3)
       dnscope -domain=example.com -dir -wordlist=dirs.txt

4)
       dnscope -domain=example.com -gdi -dns -wordlist=subdomains.txt

5)
       dnscope -domain=example.com -gdi -dir -wordlist=dirs.txt

6)
       dnscope -domain=example.com -gdi -dir -wordlist=dirs.txt -r=3

---

# DNScope
![DNScopeLogo](https://raw.githubusercontent.com/tamrinotte/dnscope/go/app_images/dnscope_logo.png)

DNScope, siber güvenlik uzmanları, sızma testi uzmanları ve dijital araştırmacılar için tasarlanmış hafif bir keşif aracıdır. Bu araç, alan adıyla ilgili meta verilerin alınması, DNS taraması ve dizin taraması işlemlerini otomatikleştirerek, hedef alan adının halka açık altyapısı ve erişilebilir dizinleri hakkında kapsamlı bir görünüm sunar.

Alan adının IP adresi, MX kayıtları, isim sunucuları, WHOIS kayıt bilgileri gibi kritik verileri toplar; ayrıca özelleştirilebilir kelime listeleri kullanarak alt alan adı ve dizin brute-force işlemleri gerçekleştirir.

Temiz, verimli ve taşınabilir olacak şekilde geliştirilen DNScope, analistlerin açık internet üzerindeki meta verileri keşfetmesini ve bir alan adının dışa açık yüzeyini hassasiyetle değerlendirmesini sağlar.

<br>

## Kurulum

1) Yükleyiciyi indirin.

	- Kali

	      curl -L https://github.com/tamrinotte/dnscope/releases/download/go_kali_v1.1/dnscope.deb -o dnscope.deb

	- Debian

	      curl -L https://github.com/tamrinotte/dnscope/releases/download/go_debian_v1.1/dnscope.deb -o dnscope.deb

2) Yükleyiciyi başlatın.

       sudo dpkg -i dnscope.deb

<br>

## Seçenekler

__-h, --help:__ Yardım mesajını görüntüle.

__-domain string:__ Hedef alanı adı (ör. -domain=example.com).

__-gdi:__ Hedef alan adı hakkında bilgi toplayın.

__-dns:__ Alt etki alanlarını numaralandırın.

__-dir:__ Dizinleri numaralandırın.

__-wordlist string:__ Alt alan adları kelime listesi dosyası.

__-r int:__ Web dizin taraması için maksimum yineleme derinliği. (varsayılan 3).

<br>

## Örnekler

1)
       dnscope -domain=example.com -gdi

2)
       dnscope -domain=example.com -dns -wordlist=subdomains.txt

3)
       dnscope -domain=example.com -dir -wordlist=dirs.txt

4)
       dnscope -domain=example.com -gdi -dns -wordlist=subdomains.txt

5)
       dnscope -domain=example.com -gdi -dir -wordlist=dirs.txt

6)
       dnscope -domain=example.com -gdi -dir -wordlist=dirs.txt -r=3