import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

source1 = {'amp': 1, 'frequency': 2, 'phase': 0, 'x': -5, 'y': -5}
source2 = {'amp': 1, 'frequency': 2, 'phase': 0, 'x': 5, 'y': -5}
source3 = {'amp': 1, 'frequency': 2, 'phase': 0, 'x': 0, 'y': 5}
sourceCenter = {'amp': 1, 'frequency': 2, 'phase': 0, 'x': 0, 'y': 0}

waves = [source1, source2, source3]

speed = 10

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'bo', animated=True)

minX = -10
minY = -10
maxX = 10
maxY = 10

def init():
    ax.set_xlim(minX, maxX)
    ax.set_ylim(minY, maxY)
    ax.set_autoscale_on(False)
    ax.set_xmargin(2.0);
    ax.set_ymargin(2.0);
    ax.set_frame_on(False)
    ax.set_aspect('equal')

    return ln,

def getZSin(wave, x, y):
    return np.sin(wave['frequency']*( ((wave['x']+x)*2 + (wave['y']+y)**2) * 0.5 ) + wave['phase'])

def update(frame):
    x = minX
    y = minY
    xdata = []
    ydata = []
    for wave in waves:
        wave['phase'] = -frame*speed
        
    while x <= maxX:
        y = minY
        while y <= maxY:
            z = 0 
            for wave in waves:
                if ( ((wave['x'] + x) ** 2) + ((wave['y'] + y) ** 2) ) ** 0.5 < (frame*speed):
                    z = z + getZSin(wave, x, y)
            if z > 0:
                xdata.append(x)
                ydata.append(y)
            y = y + 0.1
        x = x + 0.1
    ln.set_data(xdata, ydata)
    return ln,

ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                    init_func=init, blit=True)
plt.show()