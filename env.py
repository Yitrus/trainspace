
import numpy as np
import time
import sys
import os

class Kernel():
    def __init__(self):
        self.last_stat = 10
        # self.action_space = [0, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
        # basic page also should try migrate more
        # self.action_space = [8192, 16384, 32768, 65536, 131072, 262144]
        
        # below are huge page
        # self.action_space = [0, 4096, 8192, 16384, 32768, 65536, 131072]
        self.action_space = [0, 16384, 32768, 65536, 131072, 262144]
        self.n_actions = len(self.action_space)

    def read_sample(self):
        while True:
            cat_code = os.popen('cat /sys/fs/cgroup/htmm/memory.hit_ratio_show').read()
            numbers = cat_code.split()
            # print("ratio " + numbers[0])
            # print("others " + numbers[1])
            # print("dram " + numbers[2])
            # print("pm " + numbers[3])
            with open("change23hugeV30.txt", "a") as file:
                file.write("ratio " + str(numbers[0]) + "\n")
                file.write("others " + str(numbers[1]) + "\n")
                file.write("dram " + str(numbers[2]) + "\n")
                file.write("pm " + str(numbers[3]) + "\n")
            if int(numbers[2]) == 0 and int(numbers[3]) == 0:
                time.sleep(10)
            else:
                return int(numbers[0])/10

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

        time.sleep(20)

        status = self.read_sample()
        reward = status - self.last_stat
        print("reward " + str(reward))
        self.last_stat = status
        
        return status,reward
    
