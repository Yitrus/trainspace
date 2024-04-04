import os

def round_integer_except_highest_two_digits(num):
    length_of_remainder = len(str(num)) - 2
    if(length_of_remainder > 0):
        highest_two_digits = int(str(num)[:2])
        rounded_num = highest_two_digits * (10 ** length_of_remainder)
        return rounded_num
    else:
        return num

def ipc_statu():
    cat_code = os.popen('cat /sys/fs/cgroup/htmm/memory.stat_show').read()
    # print(cat_code)
    columns = cat_code.strip().split()
    ipc = round(long(columns[5]) / long(columns[3]))
    print(ipc)
    status = round_integer_except_highest_two_digits(int(ipc))
    print(status)
    return status

if __name__ == "__main__":
    ipc_statu()
