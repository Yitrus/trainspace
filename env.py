#coding:utf-8
import numpy as np
import time
import sys
import os

class Kernel():
    def __init__(self):
        self.last_pm = 0
        self.last_dram = 0
        # 从8个2M页面算起到迁移1024个2MB页面
        self.action_space = [0, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288]
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
        action *= 4096
        command = 'echo "{}" > /sys/fs/cgroup/htmm/memory.action_show'.format(str(action))
        try:
            echo_code = os.system(command)
            cat_code = os.popen('cat /sys/fs/cgroup/htmm/memory.action_show').read()
            print("action "+ str(cat_code))
        except Exception as e:
            print("action failed")

        time.sleep(10)

        status = self.read_sample()
        if(status == 11):
            reward = 0
        else:
            reward = status - 9 
        print("reward " + str(reward))
        
        return status,reward
    
