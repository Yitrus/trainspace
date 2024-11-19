#coding:utf-8
import numpy as np
import time
import sys
import os

class Kernel():
    def __init__(self):
        self.last_pm = 0
        self.last_dram = 0
        self.last_add = 0
        self.last_cyc = 0
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
           
            if truedram == 0 and truepm == 0:
                print("hitratio 11")
                return 11
            else:
                hitratio = (truedram*100)/(truedram+truepm)
                # print("hitratio "+ str(hitratio))
                # with open("/home/ssd/yi/rebuttal_1015_d1.txt", "a") as file:
                #     file.write(str(hitratio) + "\n")
                return int(hitratio/10)  # magic number k

    # def get_pending(self):
    #     try:
    #         with open('/home/ssd/yi/test_perf/count.txt', 'r') as file:
    #             lines = file.readlines()
    #             if lines:
    #                 # 获取最后一行并提取数字部分
    #                 last_line = lines[-1].strip()
    #                 # 假设每行格式为 "instructions=数字"
    #                 count_str = last_line.split('=')[-1]
    #                 return int(count_str)
    #             else:
    #                 print("文件为空。")
    #                 return None
    #     except FileNotFoundError:
    #         print("文件 'count.txt' 不存在。")
    #         return None
    #     except ValueError:
    #         print("文件格式错误，无法提取数字。")
    #         return None

    # def lat(self):
    #     while True:
    #         this_add = self.get_pending()# this_add这次读取到的累加值
    #         this_cyc = this_add - self.last_add # last_pm上次的累加值；
    #         self.last_add = this_add
    #         reward = self.last_cyc - this_cyc # last_dram指上一次延迟的周期数
    #         self.last_cyc = this_cyc

    #         return int(reward/1000) 

    # def lat0(self):
    #     while True:
    #         cat_code = os.popen('cat /sys/fs/cgroup/htmm/memory.hit_ratio_show').read()
    #         numbers = cat_code.split()
    #         thisdram = int(numbers[0])
    #         thispm = int(numbers[1])
    #         truedram = thisdram - self.last_dram
    #         truepm = thispm - self.last_pm
    #         self.last_dram = thisdram
    #         self.last_pm = thispm
           
    #         if truedram == 0 and truepm == 0:
    #             print("hitratio 11")
    #             return 125
    #         else:
    #             hitratio = (truedram*94+truepm*154)/(truedram+truepm)
    #             print("hitratio "+ str(hitratio))
    #             # with open("/home/ssd/yi/hit_ratio/rebuttal_cc1-16_0.txt", "a") as file:
    #             #     file.write(str(hitratio) + "\n")
    #             return int(hitratio)  # magic number k
            
    def reset(self):
        status = self.read_sample()
        return status

    def step(self, action):
        if action==0:
            pass
        else:
            action *= 4096
            command = 'echo "{}" > /sys/fs/cgroup/htmm/memory.action_show'.format(str(action))
            try:
                echo_code = os.system(command)
                cat_code = os.popen('cat /sys/fs/cgroup/htmm/memory.action_show').read()
                print("action "+ str(cat_code))
            except Exception as e:
                print("action failed")

        time.sleep(10) # magic number time

        status = self.read_sample()
        if(status == 11):
            reward = 0
        else:
            reward = status - 9  # magic number beta
            # reward = self.lat()  # magic number beta
        print("reward " + str(reward))
        
        return status,reward
    
