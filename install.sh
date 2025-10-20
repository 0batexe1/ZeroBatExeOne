#!/bin/bash
set -e

echo "[*] ZeroBatExeOne Kurulum Scripti Başlatılıyor..."

# 1. Sistem paketleri
echo "[*] Gerekli sistem paketleri kontrol ediliyor ve kuruluyor..."
sudo apt update
sudo apt install -y python3 python3-pip golang git curl unzip wget

# 2. Go PATH
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin
mkdir -p $GOPATH/bin

# 3. Go araçlarını kur (check)
echo "[*] Go tabanlı araçlar kuruluyor..."
declare -A GO_TOOLS
GO_TOOLS=(
    ["subfinder"]="github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
    ["findomain"]="github.com/findomain/findomain@latest"
    ["katana"]="github.com/projectdiscovery/katana/cmd/katana@latest"
    ["ffuf"]="github.com/ffuf/ffuf@latest"
    ["gau"]="github.com/lc/gau@latest"
    ["waybackurls"]="github.com/tomnomnom/waybackurls@latest"
    ["httpx"]="github.com/projectdiscovery/httpx/cmd/httpx@latest"
    ["assetfinder"]="github.com/projectdiscovery/assetfinder/cmd/assetfinder@latest"
)

for tool in "${!GO_TOOLS[@]}"; do
    if ! command -v $tool &> /dev/null; then
        echo "[*] Kuruluyor: $tool"
        go install -v "${GO_TOOLS[$tool]}"
    else
        echo "[*] $tool zaten kurulu. Atlanıyor."
    fi
done

# 4. Aquatone / gowitness
echo "[*] Aquatone kuruluyor..."
if ! command -v aquatone &> /dev/null; then
    wget https://github.com/michenriksen/aquatone/releases/download/v1.7.0/aquatone_linux_amd64.zip
    unzip aquatone_linux_amd64.zip -d /usr/local/bin
    rm aquatone_linux_amd64.zip
else
    echo "[*] Aquatone zaten kurulu. Atlanıyor."
fi

# 5. SecLists
if [ ! -d "/opt/SecLists" ]; then
    echo "[*] SecLists indiriliyor..."
    sudo git clone https://github.com/danielmiessler/SecLists.git /opt/SecLists
else
    echo "[*] SecLists zaten mevcut. Atlanıyor."
fi

# 6. Python bağımlılıkları
echo "[*] Python bağımlılıkları kuruluyor..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

echo "[*] ZeroBatExeOne kurulumu tamamlandı!"
echo "[*] Artık python3 ZeroBatExeOne.py -d example.com --screenshot ile tarama başlatabilirsiniz."
