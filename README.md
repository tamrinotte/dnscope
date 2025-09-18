# DNScope
![DNScopeLogo](https://raw.githubusercontent.com/tamrinotte/dnscope/python/app_images/dnscope_logo.png)

DNScope is a lightweight reconnaissance utility designed for cybersecurity professionals, penetration testers, and digital investigators. The tool automates domain related metadata retrieval, DNS enumeration, and directory enumeration, providing a comprehensive snapshot of a target domain’s public-facing infrastructure and accessible directories.

Built to be clean, efficient, and easily portable, DNScope helps analysts uncover open internet metadata and assess a domain’s external exposure surface with precision.

<br>

## Installation

1) Download the installer.

	- Kali

	      curl -L https://github.com/tamrinotte/dnscope/releases/download/python_kali_v0.1.3/dnscope.deb -o dnscope.deb

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

__-r int:__ Max recursion depth for directory enumeration. (default 3).

__-mw MAX_WORKER, --max_worker MAX_WORKER:__ Maximum amount of workers.

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

6)
       dnscope example.com -gdi -dir -w dirs.txt -r 3

---

# DNScope
![DNScopeLogo](https://raw.githubusercontent.com/tamrinotte/dnscope/python/app_images/dnscope_logo.png)

DNScope, siber güvenlik uzmanları, sızma testi uzmanları ve dijital araştırmacılar için tasarlanmış hafif bir keşif aracıdır. Bu araç, alan adıyla ilgili meta verilerin alınması, DNS taraması ve dizin taraması işlemlerini otomatikleştirerek, hedef alan adının halka açık altyapısı ve erişilebilir dizinleri hakkında kapsamlı bir görünüm sunar.

Temiz, verimli ve taşınabilir olacak şekilde geliştirilen DNScope, analistlerin açık internet üzerindeki meta verileri keşfetmesini ve bir alan adının dışa açık yüzeyini hassasiyetle değerlendirmesini sağlar.
<br>

## Kurulum

1) Yükleyiciyi indirin.

	- Kali

	      curl -L https://github.com/tamrinotte/dnscope/releases/download/python_kali_v0.1.3/dnscope.deb -o dnscope.deb

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

__-r int:__ Web dizin taraması için maksimum yineleme derinliği. (varsayılan 3).

__-mw MAX_WORKER, --max_worker MAX_WORKER:__ Maksimum işçi sayısı.

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

6)
       dnscope example.com -gdi -dir -w dirs.txt -r 3