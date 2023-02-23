#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Error: Invalid number of arguments. Usage: ./run.sh <bin_file>"
    exit 1
fi

bin_file=$1
# sudo_pass=$2

echo -e "\n\n"
echo "[SCRIPT] start}"
pwd
# ls
echo "picotool load -x $bin_file -f"
picotool load -x $bin_file -F
echo "sleep 1"
sleep 3
echo -e "\n\n\n\n"
echo "run_tests.py"
python3 -u host/run_tests.py
echo -e "\n\n"
echo "[SCRIPT] end}"
