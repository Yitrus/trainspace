"""
这个用于和内核交互，以及获得reward的信息所需函数

"""
import numpy as np
import time
import sys
import os

dram = hex(int('207fffffff', 16))
pm_star = hex(int('2100000000', 16))
pm_end = hex(int('9e7fffffff', 16))

class Kernel():
    def __init__(self):
        self.stat = 0
        self.action_space = [0, 16, 64, 128, 256, 512, 1024, 2048, 4096]
        self.n_actions = len(self.action_space)

    def count_value_changes(file_path):
        pm_access = 0
        dram_access = 0
        qbug = 0
        allt = 0
        with open(file_path, 'r') as file:
            for line in file:
                columns = line.strip().split()

                allt += 1
                key = columns[0]
                value = hex(int(columns[1], 16))

                if value < dram:
                    pm_access += 1
                elif (value > pm_star) and (value < pm_end):
                    dram_access += 1
                else:
                    qbug += 1
        print(dram_access / (pm_access+dram_access))      
        return (dram_access / (pm_access+dram_access))

    def reset():
        os.system('./run.sh')
        time.sleep(10)
        # 1.程序启动；2. DRAM占用可能还不满，先等待，判断一下；3.返回第一个状态
        cat_code = os.popen('cat /sys/fs/cgroup/htmm/stat_show').read()
        print("cat_code "+cat_code)
        return cat_code

    def step(self, action):
        echo_code = os.system('echo'+ action*4096 +' > /sys/fs/cgroup/htmm/action_show')
        print("echo_code "+echo_code)
        if echo_code != 0:
            done = True
            return 0,0,done

        time.sleep(10)
        os.system('./reward.sh')
        
        # 调用函数并传入文件路径
        reward = self.count_value_changes('.main.txt') - 100
        # 1.echo action*4096; 2.操作完成后算reward；3.返回操作完成后状态
        # 4.done指程序运行完没有
        
        cat_code = os.popen('cat /sys/fs/cgroup/htmm/stat_show').read()
        print("cat_code "+cat_code)
        return reward,cat_code,done
    
