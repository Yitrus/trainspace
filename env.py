
import numpy as np
import time
import sys
import os

class Kernel():
    def __init__(self):
        self.last_stat = 10
        self.last_pm = 0
        self.last_dram = 0
        self.action_space = [0, 16384, 32768, 65536, 131072, 262144]
        self.n_actions = len(self.action_space)

    def read_sample(self):
        while True:
            cat_code = os.popen('cat /sys/fs/cgroup/htmm/memory.hit_ratio_show').read()
            numbers = cat_code.split()
            thisdram = int(numbers[0])
            thispm = int(numbers[1])
            truedram = thisdram - self.last_dram
            truepm = thispm - self.last_pm
            self.last_dram = thisdram
            self.last_pm = thispm
            # print("dram " + str(truedram))
            # print("pm " + str(truepm))
            #with open("change23hugeV36.txt", "a") as file:
                # file.write("ratio " + str(numbers[0]) + "\n")
                # file.write("others " + str(numbers[1]) + "\n")
                # file.write("dram " + str(numbers[2]) + "\n")
                # file.write("pm " + str(numbers[3]) + "\n")
                # file.write("dram " + str(truedram) + "\n")
                # file.write("pm " + str(truepm) + "\n")
            if truedram == 0 and truepm == 0:
                return 11
            else:
                hitratio = (truedram*100)/(truedram+truepm)
                print("hitratio "+ str(hitratio))
                return int(hitratio/10)

    def reset(self):
        status = self.read_sample()
        self.last_stat = status
        return status

    def step(self, action):
        if action==0:
            pass
        action *= 4096
        command = 'echo "{}" > /sys/fs/cgroup/htmm/memory.action_show'.format(str(action))
        try:
            echo_code = os.system(command)
            cat_code = os.popen('cat /sys/fs/cgroup/htmm/memory.action_show').read()
            print("action "+ str(cat_code))
        except Exception as e:
            print("action failed")

        time.sleep(15)

        status = self.read_sample()
        if(status == 11):
            reward = 0
        else:
            reward = status - self.last_stat
        # print("reward " + str(reward))
        self.last_stat = status
        
        return status,reward
    
