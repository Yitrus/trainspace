#!/bin/bash

# perf script record --phys-data --max-size 1M -e mem-loads,mem-stores  --all-user # --cgroup htmm

perf mem -D --phys-data record  --all-user --max-size 1M  --pid $(pgrep -o -f train) # -k CLOCK_MONOTONIC  --exclude-perf

perf script -f > main.txt