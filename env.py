
import numpy as np
import time
import sys
import os

class Kernel():
    def __init__(self):
        self.last_stat = 50
        # self.action_space = [0, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
        self.action_space = [0, 512, 1024, 2048, 4096]
        self.n_actions = len(self.action_space)

    def read_sample(self, file_path):
        dram = int('207fffffff', 16)
        pm_star = int('2080000000', 16)
        pm_end = int('11c7fffffff', 16)
        pm_access = 0
        dram_access = 0
        qbug = 0
        allt = 0
        with open(file_path, 'r') as file:
            for line in file:
                columns = line.strip().split()

                allt += 1
                value = int(columns[-1], 16)

                if value < dram:
                    dram_access += 1
                elif (value > pm_star) and (value < pm_end):
                    pm_access += 1
                else:
                    qbug += 1
        if(dram_access==0):
            return 0
        print("ratio " + str(dram_access*100 / (pm_access+dram_access)))
        print(allt)
        print(qbug)       
        print(dram_access)
        print(pm_access)
        # make status /10, short status range
        return (dram_access*10 / (pm_access+dram_access))

    def reset(self):
        os.system('./reward.sh')
        status = self.read_sample('./main.txt')
        self.last_stat = status
        return status

    def step(self, action):
        action *= 4096
        command = 'echo "{}" > /sys/fs/cgroup/htmm/memory.action_show'.format(str(action))
        try:
            echo_code = os.system(command)
            cat_code = os.popen('cat /sys/fs/cgroup/htmm/memory.action_show').read()
            print("action "+ str(cat_code))
        except Exception as e:
            print("action failed")

        time.sleep(20)

        os.system('./reward.sh')
        status = self.read_sample('./main.txt')
        reward = status - self.last_stat
        print("reward " + str(reward))
        self.last_stat = status
        os.system('rm perf.data')
        os.system('rm main.txt')
        
        return status,reward
    
