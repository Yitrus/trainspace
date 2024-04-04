import os
def step():
    action = 10
    # echo_code = os.system('echo'+ action*4096 +' > /sys/fs/cgroup/htmm/action_show')
    # 'echo 40960 > /sys/fs/cgroup/htmm/memory.action_show'
    cat_code = os.popen('cat /sys/fs/cgroup/htmm/memory.action_show').read()
    print("before "+cat_code)

    action *= 4096
    command = 'echo "{}" > /sys/fs/cgroup/htmm/memory.action_show'.format(str(action))
    print(command)
    try:
        echo_code = os.system(command)
    except Exception as e:
        print("failed")

    # print(""+echo_code)

    # cat2_code = os.system('cat /sys/fs/cgroup/htmm/memory.action_show').read()
    # print("after "+cat2_code)
    # if echo_code != 0:
    #     done = True
    #     return 0,0,done

if __name__ == "__main__":
    step()