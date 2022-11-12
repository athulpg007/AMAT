from __future__ import absolute_import, division, print_function
from mayavi import mlab
import numpy as np
import math

alpha = np.linspace(0, 2*math.pi, 100)

xs = np.cos(alpha)
ys = np.sin(alpha)
zs = np.zeros_like(xs)

mlab.points3d(0,0,0)
plt = mlab.points3d(xs[:1], ys[:1], zs[:1])

@mlab.animate(delay=100)
def anim():
    f = mlab.gcf()
    while True:
        for (x, y, z) in zip(xs, ys, zs):
            print('Updating scene...')
            plt.mlab_source.set(x=x, y=y, z=z)
            f.scene.render()
            yield


anim()
mlab.show()