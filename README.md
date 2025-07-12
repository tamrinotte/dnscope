# DNScope
![DNScopeLogo](https://raw.githubusercontent.com/tamrinotte/dnscope/python/app_images/dnscope_logo.png)

DNScope is a lightweight, reconnaissance utility designed for cybersecurity professionals, penetration testers, and digital investigators. The tool automates DNS and WHOIS metadata gathering for any target domain, providing a comprehensive snapshot of its public-facing infrastructure.

It enumerates vital information including the domain's IP address, MX records, nameservers, WHOIS registration data, and performs subdomain brute-forcing using a customizable wordlist. With both human-readable and JSON output options, DNScope is ideal for integrating into automated recon pipelines or performing quick situational awareness checks during engagements.

Built to be clean, efficient, and easily portable, DNScope helps analysts uncover open internet metadata and assess a domain’s external exposure surface with precision.

<br>

## Installation

1) Download the installer.

	- Kali

	      curl -L https://github.com/tamrinotte/dnscope/releases/download/python_kali_v0.1.1/dnscope.deb -o dnscope.deb

	- Debian

	      curl -L https://github.com/tamrinotte/dnscope/releases/download/python_debian_v0.1.1/dnscope.deb -o dnscope.deb

2) Start the installer.

       sudo dpkg -i dnscope.deb

<br>

## Options

__-h, --help:__ Displays the help message.

__domain:__ Target domain (e.g., example.com).

__-dir:__ Enumerate directories.

__-dns:__ Enumerate subdomains.

__-gdi:__ Gather information about the target domain.

__-w WORDLIST, --wordlist WORDLIST:__ Subdomains wordlist file.

<br>

## Examples

1)
       dnscope example.com -gdi

2)
       dnscope example.com -dns -w subdomains.txt

3)
       dnscope example.com -dir -w dirs.txt

4)
       dnscope example.com -gdi -dns -w subdomains.txt

5)
       dnscope example.com -gdi -dir -w dirs.txt

---

# DNScope
![DNScopeLogo](https://raw.githubusercontent.com/tamrinotte/dnscope/python/app_images/dnscope_logo.png)

DNScope, siber güvenlik uzmanları, penetrasyon test uzmanları ve dijital araştırmacılar için tasarlanmış, hafif bir keşif aracıdır. Bu araç, hedef alan adının DNS ve WHOIS meta verilerini otomatik olarak toplayarak, kamuya açık altyapısının kapsamlı bir özetini sunar.

DNScope; alan adının IP adresi, MX kayıtları, isim sunucuları, WHOIS kayıt bilgileri gibi kritik verileri listeler ve özelleştirilebilir bir kelime listesi kullanarak alt alan adı (subdomain) brute-force taraması gerçekleştirir. Hem okunabilir metin hem de JSON formatında çıktı verebilme seçeneği ile DNScope, otomatik keşif süreçlerine entegre etmek veya hızlı durum farkındalığı sağlamak için idealdir.

Temiz, verimli ve kolay taşınabilir şekilde tasarlanan DNScope, analistlerin açık internet meta verilerini ortaya çıkarmasına ve bir alan adının dışa açık yüzeyini hassasiyetle değerlendirmesine yardımcı olur.

<br>

## Kurulum

1) Yükleyiciyi indirin.

	- Kali

	      curl -L https://github.com/tamrinotte/dnscope/releases/download/python_kali_v0.1.1/dnscope.deb -o dnscope.deb

	- Debian

	      curl -L https://github.com/tamrinotte/dnscope/releases/download/python_debian_v0.1.1/dnscope.deb -o dnscope.deb

2) Yükleyiciyi başlatın.

       sudo dpkg -i dnscope.deb

<br>

## Seçenekler

__-h, --help:__ Yardım mesajını görüntüler.

__domain:__ Hedef alan adı (ör. example.com).

__-dir:__ Dizinleri numaralandırın.

__-dns:__ Alt etki alanlarını numaralandırın.

__-gdi:__ Hedef etki alanı hakkında bilgi toplayın.

__--wordlist WORDLIST:__ Alt alan adları kelime listesi dosyası.

<br>

## Örnekler

1)
       dnscope example.com -gdi

2)
       dnscope example.com -dns -w subdomains.txt

3)
       dnscope example.com -dir -w dirs.txt

4)
       dnscope example.com -gdi -dns -w subdomains.txt

5)
       dnscope example.com -gdi -dir -w dirs.txt
