#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'


install_gnome_screensaver() {
    echo -e "${GREEN}[+] Installing gnome-screensaver...${NC}"
    if sudo apt-get update && sudo apt-get install gnome-screensaver -y; then
        echo -e "${GREEN}[+] gnome-screensaver installed successfully.${NC}"
    else
        echo -e "${RED}[-] Installation of gnome-screensaver failed.${NC}"
        echo -e "${YELLOW}[+] Try running 'sudo apt-get update' and then 'sudo apt-get install gnome-screensaver' manually.${NC}"
        echo -e "${YELLOW}[+] Once installed, re-run this script.${NC}"
        exit 1
    fi
}


check_python_package() {
    if dpkg -l | grep -q "python-tk"; then
        echo -e "${GREEN}[+] 'python-tk' package is already installed.${NC}"
    else
        echo -e "${RED}[-] 'python-tk' package is not installed.${NC}"
        echo -e "${YELLOW}[+] Installing required 'python-tk' package...${NC}"
        if sudo apt-get install python-tk -y; then
            echo -e "${GREEN}[+] 'python-tk' package installed successfully.${NC}"
        else
            echo -e "${RED}[-] Installation of 'python-tk' package failed.${NC}"
            echo -e "${YELLOW}[+] Try running 'sudo apt-get install python-tk' manually.${NC}"
            echo -e "${YELLOW}[+] Once installed, re-run this script.${NC}"
            exit 1
        fi
    fi
}


if ! dpkg -l | grep -q "gnome-screensaver"; then
    echo -e "${RED}[-] gnome-screensaver is not installed on this system.${NC}"
    install_gnome_screensaver
else
    echo -e "${GREEN}[+] gnome-screensaver is installed on this system.${NC}"
fi

check_python_package "tk"

echo -e "${GREEN}[+] Creating Executable file!${NC}"
echo -e "#!/bin/bash\npython3 $(pwd)/main.py" > test-mytime
chmod +x test-mytime

sudo mv test-mytime /usr/local/bin

echo -e "${GREEN}[+] Installation Completed!!${NC}"
echo -e "${GREEN}${BOLD}[+] Execute command: test-mytime${NC}"
