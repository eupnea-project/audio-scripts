#!/usr/bin/env python3.10

from pathlib import Path
import subprocess
import os
import json

def sklkbl_audio():
    print("sklkbl audio not implemented yet")

def apl_audio():
    print("aplaudio not implemented yet")

def sof_audio():
    install_package(sof-firmware, firmware-sof-signed, alsa-sof-firmware)
    install_package(linux-firmware, linux-firmware, linux-firmware)
    src = Path("sof.conf")
    dst = Path("/etc/modprobe.d/sof.conf")
    dst.write_bytes(src.read_bytes())

def str_audio():
    print("str audio not implemented yet")

def zen2_audio():
    print("zen2 audio not implemented yet")

def detect_platform():
    if Path("/usr/bin/dmidecode").exists():
        board = subprocess.check_output("dmidecode -s system-product-name", shell=True, text=True).strip().lower()
        return board
    else:
        print("dmidecode not installed")
        exit(1)

def install_package(arch_package, deb_package, rpm_package):
    pkgmgmt = ""
    if Path("/usr/bin/pacman").exists():
        os.system(f"pacman -S --noconfirm {arch_package}")
    elif Path("/usr/bin/apt").exists():
        os.system(f"apt install -y {deb_package}")
    elif Path("/usr/bin/dnf").exists():
        os.system(f"dnf install -y {rpm_package}")
    else:
        print("\033[31m" + f"Unknown package manager! Please install {deb_package} using your package manager." + "\033[0m")
        exit(1)

if __name__ == "__main__":

    if not os.getuid() == 0:
        print(os.getuid())
        print("\033[31m" + "This script needs to be run as root!!!" + "\033[0m")
        exit(1)

    board = detect_platform()

    with open("boards.json", "r") as file:
        boards = json.load(file)
    if board in boards:
        match boards[board]:
            case "skl":
                sklkbl_audio()
            case "kbl":
                sklkbl_audio()
            case "apl":
                apl_audio()
            case "glk":
                sof_audio()
            case "whl":
                sof_audio()
            case "cml":
                sof_audio()
            case "jsl":
                sof_audio()
            case "tgl":
                sof_audio()
            case "str":
                str_audio()
            case "zen2":
                zen2_audio()
            case _:
                print("\033[31m" f"Unknown chromebook model: {board}" + "\033[0m")
                exit(1)
    else:
        print("\033[31m" f"Unknown chromebook model: {board}" + "\033[0m")
        exit(1)
