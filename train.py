"""
这个函数代表训练时
"""

from env import Kernel
from qtable import QLearningTable


def update():
    for episode in range(100):
        # 先训练XSBench 100次看看
        observation = env.reset()
        while True:
            # fresh env
            # env.render()

            # RL choose action based on observation，写成str好当索引
            action = RL.choose_action(str(observation))

            # RL take action and get next observation and reward
            observation_, reward, done = env.step(action)

            # RL learn from this transition
            RL.learn(str(observation), action, reward, str(observation_))

            # swap observation
            observation = observation_

            # break while loop when end of this episode
            if done:
                break

    # end of game
    print('game over')

if __name__ == "__main__":
    env = Kernel()
    RL = QLearningTable(actions=list(range(env.n_actions)))

    update()