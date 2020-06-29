
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation

# Zeitschrittweite [s].
dt = 0.005

# Dargestellter Ortsbereich 0..+xmax, 0..+ymax [m].
xlim = (-1.5, 4.0)
ylim = (-2.0, 2.0)


# Ausbreitungsgeschwindigkeit der Welle [m/s].
c = 3.5

# Slit width
d = 2

# Erzeuge eine Figure und eine Axes.
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1, 1, 1)
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_aspect('equal')
quellen = []

#wall1 = mpl.patches.Rectangle((0.5, 0.5 ),0.2, 0.2, color='black', fill=True, zorder=10)
#ax.add_patch(wall1)
# Erzeuge zwei Kreise für Quelle und Beobachter.
for i in range(16):
    quelle = mpl.patches.Circle((0, 0), radius=0.03,
                            color='black', fill=True, zorder=4)
    quelle.center= np.array([-1, 1.5-i*0.2])
    quellen.append(quelle)
    ax.add_patch(quelle)
grid = []
for i in range(-8,40,2):
    for j in range(-15,16,2):
        beobach = mpl.patches.Circle((0, 0), radius=0.01,
                                    color='blue', fill=True, zorder=4)    
        beobach.center = np.array([i * 0.1, j * 0.1])
        beobach.set_gid((i*10)+j)
        if not ((i == -2 or i == 0) and not (j < d and j > -d)):
            grid.append(beobach)
            ax.add_patch(beobach)



# Lege eine Liste an, die die kreisförmigen Wellenzüge speichert.
kreise = []

for quelle in quellen:
    kreis = mpl.patches.Circle(quelle.center, radius=0,
                            color='blue', linewidth=1.5,
                            fill=False, zorder=3)
    kreis.startzeit = 0
    kreis.set_gid(-999)
    kreise.append(kreis)
    ax.add_patch(kreis)

def update(n):
    # Berechne den aktuellen Zeitpunkt.
    t = dt * n

    # Berechne die aktuelle Position von Quelle und Beobachter.

    # Erzeuge zum Startzeitpunkt einen neuen Kreis oder wenn
    # seit dem Aussenden des letzten Wellenzuges mehr als eine
    # Periodendauer vergangen ist.

    #for point in grid:        
        #point.set_color('blue')

    # Aktualisiere die Radien aller dargestellen Kreise.
    for kreis in kreise:
        kreis.radius = (t - kreis.startzeit) * c
        if kreis.radius > 0.29 and len(kreise) > 0:
            kreise.pop(kreise.index(kreis))
    # Färbe den Beobachter rot, wenn ein Wellenzug auftrifft.
    for kreis in kreise:
        for beobach in grid:
            d = np.linalg.norm(kreis.center - beobach.center)
            if abs(d - kreis.radius) < beobach.radius and kreis._gid != beobach._gid:
                if(beobach.get_facecolor()[2] == 1):
                    kreis = mpl.patches.Circle(beobach.center, radius=0,
                        color='blue', linewidth=1.5,
                        fill=False, zorder=3)
                    kreis.startzeit = t
                    kreis.set_gid(beobach._gid)
                    kreise.append(kreis)
                    if(len(kreise) > 500):
                        kreise.pop(0)
                    ax.add_patch(kreis)     
                beobach.set_color('red')                        



    # Färbe den Quelle rot, wenn ein Wellezug augesendet wird.

    
    #d = np.linalg.norm(kreise[-1].center - quelle.center)
    #if abs(d - kreise[-1].radius) < quelle.radius:
        #quelle.set_color('red')
    #else:
        #quelle.set_color('black')

    return kreise 

# Erstelle die Animation und zeige die Grafik an.
ani = mpl.animation.FuncAnimation(fig, update,
                                  interval=30, blit=True)
plt.show()
