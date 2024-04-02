
perf script record --max-size 10M -e mem-loads,mem-stores --cgroup htmm

perf script -f > main.txt