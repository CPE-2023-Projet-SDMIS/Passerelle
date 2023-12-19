#!/bin/bash
# Check if user is root
if [ "$(id -u)" -eq 0 ]; then
    echo "User is root. Continuing..."
else
    echo "User is not root. Please run this script as root."
    exit 1
fi

cp passerelle-simulateur.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable passerelle-simulateur.service
systemctl start passerelle-simulateur.service
systemctl status passerelle-simulateur.service

