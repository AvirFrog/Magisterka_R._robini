import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

print("Reading csv")
df = pd.read_csv("sample30m.csv")
print("Drop col name POS")
df = df.drop(['POS'], axis = 1)

#df = df.iloc[::100, :]
#df = df.sample(n = 3_000_000)

print("START PLOTING")

x_start = 16
x_end = 60
x_step = 2

y_start = 0
y_end = 650000
y_step = 50000

sns.set(rc={"figure.figsize":(20, 10)})

for i in range(8):
    a = i + 1
    fig, ax = plt.subplots()
    
    plot = sns.histplot(df[df.columns[a]], ax=ax, kde = True, bins= list(range(x_start, x_end)),)
    #plot = sns.histplot(df[df.columns[a]], ax=ax, bins= list(range(start, end)))
    ax.set_xlim(x_start, x_end)
    plt.ylim(y_start, y_end)
    plt.xticks(list(range(x_start, x_end, x_step)))
    plt.yticks(list(range(y_start, y_end, y_step)))
    name = df.columns[a]
    name = name.split("/")
    name = name[1]
    name = name.replace('.', '_')
    save = name + '.png'
    ax.set_xlabel("Depth")
    ax.set_ylabel("Count")
    ax.set_title(name) 
    plt.savefig(save)
    plt.clf()
    print(f'Plot number {a} END')
print("END PLOTING")
    