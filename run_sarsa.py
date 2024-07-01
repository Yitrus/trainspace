from env import Kernel
from sarsa import SarsaTable
import time

def update():
    observation = env.reset()
    action = RL.choose_action(observation)
    while True:
        observation_, reward = env.step(action)
        action_ = RL.choose_action(observation_)
        RL.learn(observation, action, reward, observation_, action_)
        observation = observation_
        action = action_

if __name__ == "__main__":
    time.sleep(10)
    env = Kernel()
    RL = SarsaTable(actions=list(env.action_space))
    update()