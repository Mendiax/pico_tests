#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Error: Invalid number of arguments. Usage: ./run.sh <bin_file> <password>"
    exit 1
fi

bin_file=$1
sudo_pass=$2

echo -e "\n\n"
echo "[SCRIPT] start}"
groups
pwd
# ls
export HISTIGNORE='*sudo -S*'
echo "picotool load -x $bin_file -f"
echo $sudo_pass | sudo -S -k picotool load -x $bin_file -F
echo "sleep 1"
sleep 3
echo -e "\n\n\n\n"
echo "run_tests.py"
echo $sudo_pass | sudo -S -k python3 -u host/run_tests.py
echo -e "\n\n"
echo "[SCRIPT] end}"
