import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

print("Reading csv")
df = pd.read_csv("output.csv")
print("Drop col name POS")
df = df.drop(['POS'], axis = 1)
print("10k lines")
df = df.iloc[::10000, :]

print("START PLOTING")


sns.set(rc={"figure.figsize":(20, 10)})

for i in range(8):
    a = i + 1
    fig, ax = plt.subplots()
    sns.distplot(df[df.columns[a]], ax=ax)
    ax.set_xlim(0, 100)
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
    