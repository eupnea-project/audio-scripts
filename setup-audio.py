#!/usr/bin/env python3.10

from pathlib import Path
import subprocess
import os
import json

def cpfile(srcf, dstf):
    src = Path(srcf)
    dst = Path(dstf)
    dst.write_bytes(src.read_bytes())

def sklkbl_audio():
    print("sklkbl audio not implemented yet")

def apl_audio():
    print("aplaudio not implemented yet")

def sof_audio(cpu, username):
    # Install required packages
    install_package("sof-firmware", "firmware-sof-signed", "alsa-sof-firmware")
    install_package("linux-firmware", "linux-firmware", "linux-firmware")
    install_package("pulseaudio", "pulseaudio", "pulseaudio")


    # Copy config files
    cpfile("configs/sof/audio-reload.service", "/etc/systemd/system/alsa-reload.service")
    cpfile("configs/sof/alsa-sof.conf", "/etc/modprobe.d/alsa-sof.conf")
    cpfile("configs/sof/asound.conf", "/etc/asound.conf")
    cpfile("configs/sof/default.pa", "/etc/pulse/default.pa")
    cpfile("configs/sof/pulseaudio.service", "/usr/lib/systemd/user/pulseaudio.service")

    # Extra commands
    subprocess.run("systemctl daemon-reload")
    subprocess.run("systemctl enable alsa-reload")

    # These commands need to be ran as a regular user
    subprocess.run("su -c 'systemctl --user mask pipewire.{socket,service}' " + username)
    subprocess.run("su -c 'systemctl --user unmask pulseaudio.{socket,service}' " + username)
    subprocess.run("su -c 'systemctl --user enable pulseaudio.{socket,service}' " + username)

def str_audio():
    print("str audio not implemented yet")

def zen2_audio():
    print("zen2 audio not implemented yet")

def detect_platform():
    if Path("/usr/sbin/dmidecode").exists():
        board = subprocess.check_output("dmidecode -s system-product-name", shell=True, text=True).strip().lower()
        return board
    else:
        print("dmidecode not installed")
        exit(1)

def install_package(arch_package, deb_package, rpm_package):
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
    # Get the username of the user running the script before elevating to root
    username = os.getlogin()

    # Elevate script to root
    if not os.geteuid() == 0:
        sudo_args = ['sudo', sys.executable] + sys.argv + [os.environ]
        os.execlpe('sudo', *sudo_args)

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
                sof_audio("glk", username)
            case "whl":
                sof_audio("whl", username)
            case "cml":
                sof_audio("cml", username)
            case "jsl":
                sof_audio("jsl", username)
            case "tgl":
                sof_audio("tgl", username)
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
