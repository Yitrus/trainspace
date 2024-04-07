perf stat -e cpu-cycles,instructions -a --pid=$(pgrep train) -o ./sample.txt -- sleep 5

