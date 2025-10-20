

---

````markdown
# ZeroBatExeOne

**ZeroBatExeOne**, hedef domain için tam otomatik ve recursive bir **recon (keşif) aracı**dır.  
Alt domain keşfi, dizin/endpoint taraması, JS içindeki gizli parametrelerin analizi ve kritik URL tespitini tek komutla yapar.

> ZeroBatExeOne is a fully automated and recursive **recon tool** for a target domain. It performs subdomain discovery, directory scanning, JS hidden parameter analysis, and critical URL detection — all in a single command.

---

## ⚠️ UYARI / IMPORTANT

Bu araç güçlü keşif yetenekleri içerir. Sadece **izinli** hedeflerde kullanın: kendi altyapınız, kurumunuzun izni veya açıkça izin verilmiş bug-bounty hedefleri. İzinsiz tarama yasal sonuçlara yol açabilir.

---

## ⚙️ Özellikler / Features

Kısa açıklama: ZeroBatExeOne aşağıdaki görevleri otomatikleştirir.

- Subdomain keşfi (subfinder, assetfinder)  
- Dizin / endpoint keşfi (ffuf)  
- URL toplama (waybackurls, gau)  
- JS içindeki gizli parametre taraması (LinkFinder, Arjun)  
- HTTP canlılık kontrolü (httpx; 200, 301, 302, 401, 403)  
- Kritik URL tespiti (`/admin`, `/login`, `.git`, `.env`, `/api`, `/graphql`, `?id=`, `?file=` vb.)  
- Recursive pipeline (varsayılan derinlik: 3)  
- Opsiyonel ekran görüntüleri (Aquatone)  
- Duplicate prevention: aynı URL/subdomain tekrar işlenmez

---

## 🛠 Kurulum / Installation

Aşağıdaki adımlar repository klonlama ve kurulum içindir. `install.sh` gerekli araçları ve bağımlılıkları kurar.

```bash
git clone https://github.com/0batexe1/ZeroBatExeOne.git
cd ZeroBatExeOne
bash install.sh
````

`install.sh` ile kurulanlar (örnek): Python modülleri, Go araçları, SecLists, httpx, LinkFinder, Arjun, ffuf, Aquatone vb.

---

## 🧭 Kullanım / Usage

Aşağıdaki örnekler en yaygın kullanım senaryolarını gösterir. Her komutun altında kısa açıklama bulunur.

**Temel tarama + screenshot**

```bash
python3 ZeroBatExeOne.py -d example.com --screenshot
```

Açıklama: Alt domain keşfi, endpoint taraması, JS taraması ve Aquatone ile görsel alma işlemlerini çalıştırır.

**Özel wordlist + yüksek paralellik**

```bash
python3 ZeroBatExeOne.py -d example.com -w ~/mywordlist.txt -t 50
```

Açıklama: Kendi wordlist’inizi kullanır ve 50 paralel thread ile tarar.

**Sadece HTTP canlılık kontrolü**

```bash
python3 ZeroBatExeOne.py -d example.com --httpx-only
```

Açıklama: Sadece httpx ile canlı endpoint kontrolü yapar.

**Sadece JS hidden parametre taraması**

```bash
python3 ZeroBatExeOne.py -d example.com --js-scan-only
```

Açıklama: Toplanan JS dosyalarında LinkFinder/Arjun ile parametre arar.

**Critical URL kontrolü ve çıktı klasörü değiştirme**

```bash
python3 ZeroBatExeOne.py -d example.com --critical-only -o ~/recon_output
```

Açıklama: Sadece kritik URL kontrolü yapar ve sonuçları belirtilen klasöre yazar.

---

## 📥 CLI Argümanları / Flags

Kısa belli başlı flag açıklamaları:

```
-d, --domain          : Hedef domain (zorunlu)
-w, --wordlist        : Özel wordlist yolu
-t, --threads         : Paralel tarama sayısı
-p, --depth           : Recursive pipeline derinliği (default: 3)
-T, --timeout         : Request timeout (saniye)
--screenshot          : Subdomain ve endpoint screenshot al
--stealth             : WAF / IP block riskini azaltma modu
--update-wordlists    : SecLists / default wordlistleri güncelle
-o, --output          : Çıktı klasörü
--httpx-only          : Sadece httpx ile canlılık kontrolü
--js-scan-only        : Sadece JS hidden parametre taraması
--critical-only       : Sadece critical URL tespiti
```

---

## 📂 Çıktı Dosya Yapısı / Output files

Tarama tamamlandığında oluşturulan tipik dosyalar:

* `subdomains.txt`
  Tüm keşfedilen subdomainler / All discovered subdomains

* `<subdomain>_dirs.txt`
  Her subdomain için bulunan dizinler / Directories found per subdomain

* `<subdomain>_urls.txt`
  Toplanan tüm URL’ler / All collected URLs

* `<subdomain>_js_endpoints.txt`
  JS içinden çıkarılan gizli parametre ve endpointler / JS hidden parameters and endpoints

* `critical_urls.txt`
  Tespit edilen kritik URL’ler ve kısa açıklamaları / Critical URLs with short descriptions

---

## ⚡ Önemli Notlar / Important Notes

* Recursive pipeline derinliği varsayılan olarak **3**’tür; `-p` / `--depth` ile değiştirilebilir.
* HTTPX ile yalnızca `200`, `301`, `302`, `401`, `403` statü kodları işlemeye alınır.
* Duplicate kontrolü sayesinde aynı URL veya subdomain tekrar taranmaz.
* Tüm taramalar mümkün olduğunca otomatik ve minimum manuel müdahale ile çalışır.

---

## 🛡 Güvenlik, Etik ve Yasal Uyarı

* **Yalnızca izin verilen hedeflerde** kullanın.
* İzinsiz kullanım yasal sonuçlar doğurabilir.
* Bulduğunuz güvenlik açıklarını sorumlu açıklama (responsible disclosure) ile rapor edin.
* Hassas bulguları güvende tutun; üçüncü taraflarla paylaşmayın.

---

## 🧩 Gelişmiş İpuçları / Tips

* Wordlist optimizasyonu: hedefe özel wordlist’ler false-positive’i azaltır ve verimi artırır.
* Stealth modu: WAF veya rate-limit ile karşılaşıyorsanız `--stealth` deneyin; tarama hızını ve parallelismi azaltır.
* Ekran görüntüleri: Aquatone büyük sonuç setlerinde yavaş olabilir; gerektiğinde seçerek kullanın.
* CI/Automation: Tekrarlı taramalar için job’lar oluşturup sonuçları zaman damgası ile saklayın.

---

## 🛠 Sık Karşılaşılan Sorunlar / Troubleshooting

* **Bağımlılık hataları**: `install.sh` her aracı yüklemeyebilir; eksik araçları manuel kurun (ffuf, httpx, linkfinder, arjun vb.).
* **Rate limit / IP block**: IP’niz engellenirse tarama hızını azaltın, proxy/tor kullanımı dikkatli ve izinli olmalı.
* **Çok büyük sonuç**: Çıktıyı filtrelemek için `grep`, `jq` vb. kullanın ve yalnızca `critical_urls.txt` üzerinde çalışın.

---

## 🧾 Lisans & Katkı / License & Contributing

* Katkılar: PR’lar ve issue’lar memnuniyetle karşılanır. Test verileri anonim olmalıdır — gerçek secret'lar veya hassas veriler repoya eklenmemelidir.

---

## 📬 İletişim / Contact

Her türlü sorun, öneri veya güvenlik bildirimi için GitHub Issues kullanın. Hassas güvenlik raporları için repo sahibinin sağladığı resmi iletişim kanallarını tercih edin.

---








