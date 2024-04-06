perf stat -e cpu-cycles,instructions -a --pid=$(pgrep -o -f train) -o ./sample.txt -- sleep 5

