#!/bin/bash

# Systemctl needs these variables to be set
export XDG_RUNTIME_DIR="/run/user/$UID"
export DBUS_SESSION_BUS_ADDRESS="unix:path=${XDG_RUNTIME_DIR}/bus"

systemctl --user mask pipewire.{socket,service}
systemctl --user unmask pulseaudio.{socket,service}
systemctl --user enable pulseaudio.{socket,service}
