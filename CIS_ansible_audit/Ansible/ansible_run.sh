#!/bin/bash

read -p "Enter 'linux' or 'window': " user_input

if [[ "$user_input" == "linux" ]]; then
    ansible-playbook -i inventory.conf playbook_linux_check.yml --limit linux --ask-pass --ask-become-pass
elif [[ "$user_input" == "window" ]]; then
    read -s PASS
    ansible-playbook -i inventory.conf playbook_windows_check.yml --limit windows -e "ansible_password=$PASS"
else
    echo "Invalid input. Please enter 'linux' or 'window'."
    exit 1
fi

python3 test.py
