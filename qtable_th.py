#coding:utf-8
import numpy as np
import pandas as pd
import os

class QLearningTable:
    def __init__(self, actions, learning_rate=0.01, reward_decay=0.9, e_greedy=0.7):
        self.actions = actions  # a list
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        if os.path.exists('./th.txt'):
            self.q_table = pd.read_csv('./th.txt', sep='\s+', header=None, dtype=np.float64)
            self.q_table.columns = [str(a) for a in actions]
            self.q_table.index = pd.Index(range(12))
        else:
            self.q_table = pd.DataFrame(columns=[str(a) for a in actions], dtype=np.float64, index=range(12))
            self.q_table = self.q_table.fillna(0)


    def choose_action(self, observation):
        # action selection
        # 要不要加上如果状态是11，action就是0，或者直接跳过去下一轮?
        if np.random.uniform() < self.epsilon:
            # choose best action
            state_action = self.q_table.loc[observation, :]
            # some actions may have the same value, randomly choose on in these actions
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        else:
            # choose random action
            action = np.random.choice(self.actions)
        with open("/home/ssd/yi/thaction_rebuttal_1015_d1.txt", "a") as file:
                    file.write(str(action) + "\n")
        return action

    #
    def learn(self, s, a, r, s_):
        q_predict = self.q_table.loc[s, str(a)]
        if s_ != 'terminal':
            q_target = r + self.gamma * self.q_table.loc[s_, :].max()  # next state is not terminal
        else:
            q_target = r  # next state is terminal
        self.q_table.loc[s, str(a)] += self.lr * (q_target - q_predict)  # update
        file_path = 'th.txt'
        self.q_table.to_csv(file_path, sep='\t', index=False, header=False) # , mode='a'