
import numpy as np
import time
import sys
import os

class Kernel():
    def __init__(self):
        self.stat = 0
        self.action_space = [0, 16, 64, 128, 256, 512, 1024, 2048, 4096]
        self.n_actions = len(self.action_space)

    def read_sample(self, file_path):
        dram = int('207fffffff', 16)
        pm_star = int('2100000000', 16)
        pm_end = int('9e7fffffff', 16)
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
        print(dram_access*100 / (pm_access+dram_access))
        print(allt)
        print(qbug)       
        return (dram_access*100 / (pm_access+dram_access))

    def round_integer_except_highest_two_digits(self, num):
        length_of_remainder = len(str(num)) - 2
        if(length_of_remainder > 0):
            highest_two_digits = int(str(num)[:2])
            rounded_num = highest_two_digits * (10 ** length_of_remainder)
            return rounded_num
        else:
            return num

    def ipc_statu(self):
        cat_code = os.popen('cat /sys/fs/cgroup/htmm/memory.stat_show').read()
        # print("reset_code "+cat_code)
        columns = cat_code.strip().split()
        # print(columns)
        if(long(columns[3]) == 0):
            return 0
        ipc = int(long(columns[5]) / long(columns[3]))
        print("ipc "+str(ipc))
        status = self.round_integer_except_highest_two_digits(ipc)
        return status


    def reset(self):
        # os.system('./run.sh') 
        time.sleep(10)
        status = self.ipc_statu()
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
        # if echo_code != 0:
        #     done = True
        #     return 0,0,done

        time.sleep(30)

        os.system('./reward.sh')
        reward = self.read_sample('./main.txt') - 50
        # print("reward "+reward)
        os.system('rm perf.data')
        os.system('rm main.txt')
        
        status = self.ipc_statu()
        return status,reward
    
