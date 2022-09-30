#!/usr/bin/env python3

import os
import sys
import json
import argparse

from functions import *


# parse arguments from the cli. Only for testing/advanced use. All other parameters are handled by cli_input.py
def process_args():
    parser = argparse.ArgumentParser()
    # parser.add_argument('-l', '--local-path', dest="local_path",
    #                     help="Use local files, instead of downloading from the internet (not recommended).")
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False,
                        help="Print more output")
    return parser.parse_args()


def skl_kbl_audio():
    print_error("sklkbl audio not implemented yet")


def apl_audio():
    print_error("aplaudio not implemented yet")


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

    bash("systemctl daemon-reload")  # Reload systemd configs
    bash("systemctl enable alsa-reload")  # enable custom service

    # These commands need to be run as a regular user
    bash("su -c 'systemctl --user mask pipewire.{socket,service}' " + username)
    bash("su -c 'systemctl --user unmask pulseaudio.{socket,service}' " + username)
    bash("su -c 'systemctl --user enable pulseaudio.{socket,service}' " + username)


def str_audio():
    print_error("str audio not implemented yet")


def zen2_audio():
    print_error("zen2 audio not implemented yet")


def detect_platform():
    if Path("/usr/sbin/dmidecode").exists():
        return bash("dmidecode -s system-product-name").lower()
    else:
        # TODO: Install dmidecode automatically
        print_error("Please install dmidecode")
        exit(1)


def install_package(arch_package, deb_package, rpm_package):
    if Path("/usr/bin/pacman").exists():
        os.system(f"pacman -S --noconfirm {arch_package}")
    elif Path("/usr/bin/apt").exists():
        os.system(f"apt install -y {deb_package}")
    elif Path("/usr/bin/dnf").exists():
        os.system(f"dnf install -y {rpm_package}")
    else:
        print_error(f"Unknown package manager! Please install {deb_package} using your package manager.")
        exit(1)


if __name__ == "__main__":
    if os.geteuid() == 0 and not path_exists("/tmp/username"):
        print_error("Please start the script as non-root/without sudo")
        exit(1)

    args = process_args()  # process args before elevating to root for better ux

    # Restart script as root
    if not os.geteuid() == 0:
        # save username
        with open("/tmp/username", "w") as file:
            file.write(bash("whoami").strip())  # get non root username. os.getlogin() seems to fail in chroots
        sudo_args = ['sudo', sys.executable] + sys.argv + [os.environ]
        os.execlpe('sudo', *sudo_args)

    # read username
    with open("/tmp/username", "r") as file:
        user_id = file.read()

    device_board = detect_platform()

    with open("boards.json", "r") as file:
        boards = json.load(file)
    try:
        match boards[device_board]:
            case "skl":
                skl_kbl_audio()
            case "kbl":
                skl_kbl_audio()
            case "apl":
                apl_audio()
            case "glk":
                sof_audio("glk", user_id)
            case "whl":
                sof_audio("whl", user_id)
            case "cml":
                sof_audio("cml", user_id)
            case "jsl":
                sof_audio("jsl", user_id)
            case "tgl":
                sof_audio("tgl", user_id)
            case "str":
                str_audio()
            case "zen2":
                zen2_audio()
            case _:
                print_error(f"Unknown chromebook model: {device_board}")
                exit(1)
    except KeyError:
        print_error(f"Unknown chromebook model: {device_board}")
        exit(1)
