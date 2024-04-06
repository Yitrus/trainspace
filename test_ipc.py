import os

def round_float_except_highest_two_digits(num):
        # num < 1
        highest_two_digits = int(str(num)[2])
        rounded_num = highest_two_digits * 0.1 
        return rounded_num

def round_integer_except_highest_two_digits(num):
    length_of_remainder = len(str(num)) - 2
    if(length_of_remainder > 0):
        highest_two_digits = int(str(num)[:2])
        rounded_num = highest_two_digits * (10 ** length_of_remainder)
        return rounded_num
    else:
        return num

def read_statu(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                if "instructions" in line:
                    columns = line.strip().split()
                    print(columns[3])
                    return float(columns[3])

def ipc_statu():
    # cat_code = os.popen('cat /sys/fs/cgroup/htmm/memory.stat_show').read()
    # print(cat_code)
    # columns = cat_code.strip().split()
    #os.system('./statu.sh')
    ipc = read_statu('./sample.txt')
    print(ipc)
    if(ipc > 1):
        status = round_integer_except_highest_two_digits(int(ipc))
    if(ipc < 1):
        status = round_float_except_highest_two_digits(ipc)
    print(status)
    return status

if __name__ == "__main__":
    ipc_statu()
