#coding:utf-8
import numpy as np
import time
import sys
import os

class Kernel():
    def __init__(self):
        self.last_pm = 0
        self.last_dram = 0
        self.action_space = [0, 1, -1]
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
            # 这里是累加的采样计数，因为每核一个线程，原子计数
            # 当两者都为0表示没有采样到或者几乎都缓存命中了（概率很小），返回特殊状态11
            if truedram == 0 and truepm == 0:
                print("hitratio 11")
                return 11
            else:
                hitratio = (truedram*100)/(truedram+truepm)
                print("hitratio "+ str(hitratio))
                return int(hitratio/10)

    def reset(self):
        status = self.read_sample()
        return status

    def step(self, action):
        if action==0:
            pass
        else:
            command = 'echo "{}" > /sys/fs/cgroup/htmm/memory.rl_threshold'.format(str(action))
            try:
                echo_code = os.system(command)
                # cat_code = os.popen('cat /sys/fs/cgroup/htmm/memory.rl_threshold').read()
                # print("rl_threshold "+ str(cat_code))
            except Exception as e:
                print("rl_threshold failed")

        time.sleep(5)

        status = self.read_sample()
        if(status == 11):
            reward = 0
        else:
            reward = status - 9 
        print("reward " + str(reward))
        
        return status,reward
    
