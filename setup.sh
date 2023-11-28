#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m' 

install_gnome_screensaver() {
    echo -e "${GREEN}[+] Installing gnome-screensaver...${NC}"
    sudo apt-get update
    sudo apt-get install gnome-screensaver -y
}

if dpkg -l | grep -q "gnome-screensaver"; then
    echo -e "${GREEN}[+] gnome-screensaver is installed on this system.${NC}"
else
    echo -e "${RED}[-] gnome-screensaver is not installed on this system.${NC}"
    install_gnome_screensaver
fi

echo -e "${YELLOW}[+] Installing required Python packages...${NC}"
sudo apt-get install python3-tk
echo -e "${GREEN}[+] Creating Executable file!${NC}"
echo -e "#!/bin/bash\n$(pwd)/main.py" > mytime
chmod +x main.py
chmod +x mytime
sudo mv mytime /bin
echo -e "${GREEN}[+] Installation Completed!!${NC}"
echo -e "${GREEN}${BOLD}[+] Execute command: mytime${NC}"
