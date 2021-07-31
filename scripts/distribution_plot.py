from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from src.color_tree import get_dmcs


fig = pyplot.figure()
ax = Axes3D(fig)

dmcs = get_dmcs()
data = np.zeros((len(dmcs), 3))
colors = []
for i, key_item in enumerate(dmcs.items()):
    data[i, :] = np.array(key_item[1]['rgb'])
    colors.append('#' + key_item[0])

ax.scatter(data[:, 0], data[:, 1], data[:, 2], c=colors)
ax.set_xlabel('R')
ax.set_ylabel('G')
ax.set_zlabel('B')
fig.add_axes(ax)
pyplot.show()

