
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation

# timesteps
dt = 0.005

# visualized aread
xlim = (-1.5, 4.0)
ylim = (-2.0, 2.0)


# wave 
c = 3.5

# Slit width (only put even numbers here)
d = 2

fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1, 1, 1)
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_aspect('equal')
sources = []


# Generate sources
for i in range(16):
    source = mpl.patches.Circle((0, 0), radius=0.03,
                            color='black', fill=True, zorder=4)
    source.center= np.array([-1, 1.5-i*0.2])
    sources.append(source)
    ax.add_patch(source)
grid = []
for i in range(-8,40,2):
    for j in range(-15,16,2):
        point = mpl.patches.Circle((0, 0), radius=0.01,
                                    color='blue', fill=True, zorder=4)    
        point.center = np.array([i * 0.1, j * 0.1])
        point.set_gid((i*10)+j)
        if not ((i == -2 or i == 0) and not (j < d and j > -d)):
            grid.append(point)
            ax.add_patch(point)

waves = []

for source in sources:
    wave = mpl.patches.Circle(source.center, radius=0,
                            color='blue', linewidth=1.5,
                            fill=False, zorder=3)
    wave.startzeit = 0
    wave.set_gid(-999)
    waves.append(wave)
    ax.add_patch(wave)

def update(n):
    # Calculate current time
    t = dt * n

    # Update waves
    for wave in waves:
        wave.radius = (t - wave.startzeit) * c
        if wave.radius > 0.29 and len(waves) > 0:
            waves.pop(waves.index(wave))
    # When a wave hits a point, the point should send out a new wave (only once)
    for wave in waves:
        for point in grid:
            d = np.linalg.norm(wave.center - point.center)
            if abs(d - wave.radius) < point.radius and wave._gid != point._gid:
                if(point.get_facecolor()[2] == 1):
                    wave = mpl.patches.Circle(point.center, radius=0,
                        color='blue', linewidth=1.5,
                        fill=False, zorder=3)
                    wave.startzeit = t
                    wave.set_gid(point._gid)
                    waves.append(wave)
                    if(len(waves) > 500):
                        waves.pop(0)
                    ax.add_patch(wave)     
                point.set_color('red')                        
    return waves


ani = mpl.animation.FuncAnimation(fig, update,
                                  interval=30, blit=True)
plt.show()
