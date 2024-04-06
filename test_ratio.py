
import os
    
def read_sample(file_path):
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
            print(columns[-1])
            value = int(columns[-1], 16)

            if value < dram:
                dram_access += 1
            elif (value > pm_star) and (value < pm_end):
                pm_access += 1
            else:
                qbug += 1
    # print(dram_access)
    # print(pm_access)    
    print(dram_access*100 / (pm_access+dram_access))  
    # print(allt)
    # print(qbug)   
    return (dram_access*100 / (pm_access+dram_access))  

if __name__ == "__main__":
    os.system('./reward.sh')
    reward = read_sample('./main.txt') - 50
    # print(reward)