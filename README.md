# THIS REPO HAS BEEN DISCONTINUED

Please use the [new repo](https://github.com/WeirdTreeThing/chromebook-linux-audio) instead.

<details>
<summary>View the old readme</summary>

<h1 align="center">Setup audio on Chromebooks</h1>

# Instructions
1. `git clone https://github.com/eupnea-linux/audio-scripts`
2. `cd audio-scripts`
3. `./setup-audio`

# Requirements
1. `python 3.10`

# Supported distros
1. Ubuntu 22.10 
2. Ubuntu 22.04/Linux Mint: needs newer libasound2 and libasound2-data packages. Extract the 22.10 packages or use this [backport](https://github.com/eupnea-linux/apt-repo/tree/gh-pages/debian_ubuntu/pool/main/liba/libasound2-eupnea). Backports are not needed on Pop!_OS
2. Debian testing
3. Fedora 37
4. OpenSUSE
5. Void Linux
6. Arch Linux

Other distros will likely work but will require you to manually install packages.
