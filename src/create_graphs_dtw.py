import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

save_path = './calculation_results/graphs/dtw/'
path = './calculation_results/dtw/'
correlation_results = os.listdir(path)
dfs = []
reference_recordings = []
new_recordings = []
for result in correlation_results:
    file_path = path + result
    df = pd.read_csv(file_path,
    sep=" ",
    header=None)
    dfs.append(df)
    reference_recordings.append(df.iloc[0])
    new_recordings.append(df.iloc[1])

reference_values = [x[0] for x in reference_recordings]
new_values = [x[0] for x in new_recordings]
headers = list(zip(reference_values, new_values))
index = pd.MultiIndex.from_tuples(headers)
max_length = max([x.size for x in dfs])
data = pd.DataFrame(index = np.arange(max_length), columns=index)

for df in dfs:
    tmp1 = df.iloc[0,0]
    tmp2 = df.iloc[1,0]
    tmp3 = df[2:][0]
    data[tmp1, tmp2] = tmp3

for index, column in enumerate(data.columns):
    x_axis = (data.iloc[:,index].index.values - 2) * 30
    y_axis = [float(x) for x in data.iloc[:,index].values]
    plt.clf()
    plt.xlabel('time [ms]')
    plt.ylabel('distance')
    plt.plot(x_axis, y_axis)
    save_path = './calculation_results/graphs/dtw/'
    plt.savefig(f'{save_path}-{data.columns[index][0]}-{data.columns[index][1]}.png')

data.to_csv(save_path + 'table.csv', sep=';')