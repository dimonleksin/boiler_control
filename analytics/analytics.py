import analytics_settings as settings
import matplotlib.pyplot as plt

with open(, "r") as data:
    d = data.read()
new_d = d.split(sep='\n')

x = []
y = []

for i in new_d:
    i_without_space = i.strip()
    # new[i_without_space[:-6]] = i_without_space[-5:]
    x.append(i_without_space[11:-13])
    y.append(i_without_space[-5:])
    # print(x,y)

plt.plot(x,y)
plt.savefig('test.png')

