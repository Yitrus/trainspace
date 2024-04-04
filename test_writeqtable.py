import pandas as pd

data = {'Name': ['David', 'Emma', 'Frank'],
        'Age': [28, 33, 40],
        'City': ['San Francisco', 'Seattle', 'Boston']}
df = pd.DataFrame(data)

file_path = 'data.txt'
df.to_csv(file_path, sep='\t', mode='a', index=False, header=False)  

