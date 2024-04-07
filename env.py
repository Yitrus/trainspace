
import numpy as np
import time
import sys
import os

class Kernel():
    def __init__(self):
        self.last_stat = 50
        self.action_space = [0, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
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
        if(dram_access==0):
            return 0
        print(dram_access*100 / (pm_access+dram_access))
        print(allt)
        print(qbug)       
        return (dram_access*100 / (pm_access+dram_access))

    # def read_statu(self, file_path):
    #     with open(file_path, 'r') as file:
    #         for line in file:
    #             if "instructions" in line:
    #                 columns = line.strip().split()
    #                 return float(columns[3])

    # def round_integer_except_highest_two_digits(self, num):
    #     # num > 1
    #     length_of_remainder = len(str(num)) 
    #     if(length_of_remainder == 2):
    #         highest_two_digits = int(str(num)[:1])
    #         rounded_num = highest_two_digits * 10 
    #         return rounded_num
    #     if(length_of_remainder > 2):
    #         return 100
    #     else:
    #         return num

    # def round_float_except_highest_two_digits(self, num):
    #     # num < 1
    #     highest_two_digits = int(str(num)[2])
    #     rounded_num = highest_two_digits * 0.1 
    #     return rounded_num

    # def ipc_statu(self):
        #cat_code = os.popen('cat /sys/fs/cgroup/htmm/memory.stat_show').read()
        # print("reset_code "+cat_code)
        #columns = cat_code.strip().split()
        # print(columns)
        #if(long(columns[3]) == 0):
        #    return 0
        #ipc = float(columns[5]) / float(columns[3])
        # os.system('./statu.sh')
        # ipc = self.read_statu('./sample.txt')
        # print("ipc "+str(ipc))
        # if(ipc >= 1):
        #     status = self.round_integer_except_highest_two_digits(int(ipc))
        # if(ipc < 1):
        #     status = self.round_float_except_highest_two_digits(ipc)
        # return status

    def reset(self):
        # os.system('./run.sh') 
        # time.sleep(10)
        os.system('./reward.sh')
        status = self.read_sample('./main.txt')
        self.last_stat = status
        # status = self.ipc_statu()
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

        time.sleep(20)

        os.system('./reward.sh')
        status = self.read_sample('./main.txt')
        reward = status - self.last_stat
        self.last_stat = status
        # print("reward "+reward)
        os.system('rm perf.data')
        os.system('rm main.txt')
        
        # status = self.ipc_statu()
        # os.system('rm sample.txt')
        return status,reward
    
