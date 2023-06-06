#!/bin/bash 

# 445765
for i in $(seq 0 99) # 100核并行，建议改为笔记本核数
do
    python process.py --start $[$i * 4457] --end $[($i + 1) * 4457] &
done

# 使用&用于后台运行
python multi-process.py --start 445700 --end 445765 &