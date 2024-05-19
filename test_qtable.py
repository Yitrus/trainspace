import numpy as np
import pandas as pd
import os

def learn(s, a, r, s_):
        print("a "+ str(a))
        print("s "+ str(s))  
        print("r "+ str(r))  
        q_predict = q_table.loc[s, str(a)]
        print(q_predict)

if __name__ == "__main__":
    actions = [0, 16384, 32768, 65536, 131072, 262144]

    if os.path.exists('./data0.txt'):
        q_table = pd.read_csv('./data0.txt', sep='\s+', header=None, dtype=np.float64)
        q_table.columns = [str(a) for a in actions]
        q_table.index = pd.Index(range(12))
    else:
        q_table = pd.DataFrame(columns=actions, dtype=np.float64, index=range(12))
        q_table = q_table.fillna(0)
        
    
    learn(0, 0, 0.234, 9)