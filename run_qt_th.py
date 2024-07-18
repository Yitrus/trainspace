from env_th import Kernel
from qtable_th import QLearningTable
import time

def update():
    observation = env.reset()
    while True:
        action = RL.choose_action(observation)
        observation_, reward = env.step(action)
        RL.learn(observation, action, reward, observation_)
        observation = observation_

if __name__ == "__main__":
    time.sleep(10)
    env = Kernel()
    RL = QLearningTable(actions=list(env.action_space))
    update()