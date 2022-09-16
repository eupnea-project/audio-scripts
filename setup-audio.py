#!/usr/bin/env python3.10

from pathlib import Path
import subprocess
import os
import boards
import json

def sklkbl_audio():
    print("sklkbl")

def apl_audio():
    print("apl")

def glkplus_audio():
    print("glk+")

def str_audio():
    print("str")

def zen2_audio():
    print("zen2")

def detect_platform():
    if Path("/usr/bin/dmidecode").exists():
        board = subprocess.check_output("dmidecode -s system-product-name | tr '[:upper:]' '[:lower:]' | sed 's/ /_/g' | awk 'NR==1{print $1}'", shell=True, text=True).strip()
        return board
    else:
        print("dmidecode not installed")
        exit(1)

def install_package(arch_package, deb_package, rpm_package):
    pkgmgmt = ""
    if Path("/usr/bin/pacman").exists():
        pkgmgmt = "pacman"
    elif Path("/usr/bin/apt").exists():
        pkgmgmt = "apt"
    elif Path("/usr/bin/dnf").exists():
        pkgmgmt = "dnf"
    else:
        print("\033[31m" + "Unknown package manager!" + "\033[0m")
        exit(1)
    
    match pkgmgmt:
        case "pacman":
            os.system(f"pacman -S --noconfirm {arch_package}")
        case "apt":
            os.system(f"apt install -y {deb_package}")
        case "dnf":
            os.system(f"dnf install -y {rpm_package}")

if __name__ == "__main__":

    if not os.getuid() == 0:
        print(os.getuid())
        print("\033[31m" + "This script needs to be run as root!!!" + "\033[0m")
        exit(1)

    board = detect_platform()

    with open("boards.json", "r") as file:
        boards = json.load(file)
    
    match boards[board]:
        case "skl":
            sklkbl_audio()
        case "kbl":
            sklkbl_audio()
        case "apl":
            apl_audio()
        case "glk":
            glkplus_audio()
        case "whl":
            glkplus_audio()
        case "cml":
            glkplus_audio()
        case "jsl":
            glkplus_audio()
        case "tgl":
            glkplus_audio()
        case "str":
            str_audio()
        case "zen2":
            zen2_audio()
