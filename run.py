from env import Kernel
from qtable import QLearningTable
import time

def update():
    # for episode in range(100):
        observation = env.reset()
        while True:
            action = RL.choose_action(str(observation))
            observation_, reward = env.step(action)

            RL.learn(str(observation), action, reward, str(observation_))

            observation = observation_

            # break while loop when end of this episode
            # if done:
            #     break

if __name__ == "__main__":
    time.sleep(30)
    env = Kernel()
    RL = QLearningTable(actions=list(env.action_space))
    update()