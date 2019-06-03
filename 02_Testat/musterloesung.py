# -*- coding: utf-8 -*-
# testat2_muloe.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RectBivariateSpline
import matplotlib.colors as colors


class TopoMap:
    '''Hilfsfunktionen für die Benutzung von Kartendaten.
    '''

    def __init__(self, fname, **kwargs):
        '''Kartendaten einlesen.

        Argumente:
            fname -- Pfad der Datei
        '''
        # cooperative superclass calls
        super().__init__(**kwargs)

        # Kartendaten aus der Datei einlesen
        data = np.loadtxt(fname, delimiter=',')

        # Hilfsvariablen
        self._x = data[0, 1:]
        self._y = data[1:, 0]
        self._x_lim = (np.min(self._x), np.max(self._x))
        self._x_step = np.mean(np.abs(np.diff(self._x)))
        self._y_lim = (np.min(self._y), np.max(self._y))
        self._y_step = np.mean(np.abs(np.diff(self._y)))

        # Kartendaten in nicht-öffentliche Variablen speichern
        self._X, self._Y = np.meshgrid(self._x, self._y)
        self._Z = data[1:, 1:]

        # Interpolationsfunktion für die z-Achse
        self._Z_interp = RectBivariateSpline(self._x, self._y, self._Z.T).ev

        # Gradient in x- und y-Richtung berechnen
        # https://docs.scipy.org/doc/numpy/reference/generated/numpy.gradient.html
        dZ_dy, dZ_dx = np.gradient(
                self._Z,        # z-Werte
                self._y_step,   # Abstand zwischen den y-Werten
                self._x_step,   # Abstand zwischen den x-Werten
        )

        # Interpolationsfunktionen für den Gradienten
        self._gradient_dx = RectBivariateSpline(self._x, self._y, dZ_dx.T).ev
        self._gradient_dy = RectBivariateSpline(self._x, self._y, dZ_dy.T).ev

    @property
    def X(self):
        return self._X.copy()

    @property
    def Y(self):
        return self._Y.copy()

    @property
    def Z(self):
        return self._Z.copy()

    def highest_point(self):
        '''Find the highest point in the map.
        '''
        y_idx, x_idx = np.unravel_index(np.argmax(self._Z), self._Z.shape)

        # 3D-Position des Maximums zurückgeben
        return (self._x[x_idx], self._y[y_idx], self._Z[y_idx, x_idx])

    def lowest_point(self):
        '''Find the lowest point in the map.
        '''
        y_idx, x_idx = np.unravel_index(np.argmin(self._Z), self._Z.shape)

        # 3D-Position des Minimums zurückgeben
        return (self._x[x_idx], self._y[y_idx], self._Z[y_idx, x_idx])

    def elevation(self, position):
        '''Return the elevation at the given position.

        Arguments:
            position -- list [x, y] or 2D array [[x1, y1], ...] of positions
        '''
        position = np.atleast_2d(position)
        return self._Z_interp(position[:, 0], position[:, 1])
        # oder:
        # position = np.asarray(position)
        # return self._Z_interp(position[..., 0], position[..., 1])

    def elevation_profile(self, path):
        '''Returns the elevation profile along the given path.

        Arguments:
            path -- 2D array of positions [[x1, y1], ...]

        Returns:
            distance -- relative distance from the starting point
            z -- elevation along the path
        '''

        path = np.atleast_2d(path)
        # oder: path = np.asarray(path)  falls path sowieso 2D ist
        # oder: path = np.array(path)    falls path sowieso 2D ist
        x = path[:, 0]
        y = path[:, 1]

        # interpolierte Höhe
        z = self.elevation(path)

        # 2D-Weglänge
        distance = np.zeros_like(z)
        distance[1:] = np.cumsum(np.sqrt(np.diff(x)**2 + np.diff(y)**2))

        # 2D-Weglänge und Höhe zurückgeben
        return distance, z

    def distance_travelled(self, path):
        ''''Returns the distance and the cumulative elevation gain.

        Arguments:
            path -- 2D array of positions [[x1, y1], ...]

        Returns:
            distance -- total walk distance
            cumulative_elevation_gain -- sum of the elevation gains
        '''
        x = path[:, 0]
        y = path[:, 1]
        z = self.elevation(path)

        # Summe der euklidischen Abstände zwischen den 3D-Punkten
        distance = np.sum(
                np.sqrt(np.diff(x)**2 + np.diff(y)**2 + np.diff(z)**2)
        )

        # überwundene Höhenmeter (Summe aller positiven Höhendifferenzen)
        # https://en.wikipedia.org/wiki/Cumulative_elevation_gain
        dz = np.diff(z)
        cumulative_elevation_gain = np.sum(dz[dz > 0])

        # 3D-Weglänge und Höhenmeter zurückgeben
        return distance, cumulative_elevation_gain

    def fall_line(self, start, descent=True, gamma=50,
                  max_iter=10000, precision=0.1):
        '''Find the line of greatest slope.

        Arguments:
            start -- [x, y], list or 1D array
            descent -- downhill if True, uphill if False
            gamma -- step size multiplier
            max_iter -- maximum number of iterations
            precision -- desired precision of result

        Returns:
            path -- 2D array of the path
        '''
        # https://en.wikipedia.org/wiki/Line_of_greatest_slope

        # Startposition
        x, y = start

        # bergab oder bergauf
        if descent:
            gamma = -np.abs(gamma)
        else:
            gamma = np.abs(gamma)

        # Pfad in Richtung des Gradienten folgen
        path = [[x, y]]
        for n in range(max_iter):
            dx = self._gradient_dx(x, y)*gamma
            dy = self._gradient_dy(x, y)*gamma

            # Position in Richtung des Gradienten bewegen
            x += dx
            y += dy

            # falls den Kartenrand erreicht wurde
            if x < self._x_lim[0] or x > self._x_lim[1] \
                    or y < self._y_lim[0] or y > self._y_lim[1]:
                # stehen bleiben
                break

            # falls das Ufer (z<=0) erreicht wurde
            if self._Z_interp(x, y) <= 0:
                # stehen bleiben
                break

            # falls die Änderung genug klein geworden ist
            if (np.abs(dx) + np.abs(dy)) < precision:
                # stehen bleiben
                break

            # neue Position zur Liste hinzufügen
            path.append([x, y])

        # Pfad zurückgeben (als NumPy-Array)
        return np.array(path)

    def aligned_map(self, p, q):
        '''Returns a copy of the map data aligned to the points p and q.

        Arguments:
            p -- [x, y], list or 1D array, p is the new origin
            q -- [x, y], list or 1D array, q lies north of p
        '''

        # Ursprung zum Punkt p verschieben
        X_new = self.X - p[0]
        Y_new = self.Y - p[1]

        # Drehwinkel berechnen
        phi = np.pi/2 - np.arctan2(q[1] - p[1], q[0] - p[0])

        # Drehmatrix definieren
        A = np.array([[np.cos(phi), -np.sin(phi)],
                      [np.sin(phi),  np.cos(phi)]])

        # Kartenkoordinaten drehen
        X_rot = A[0, 0]*X_new + A[0, 1]*Y_new
        Y_rot = A[1, 0]*X_new + A[1, 1]*Y_new

        return X_rot, Y_rot, self.Z, A


if __name__ == '__main__':

    # make a colormap that has land and ocean clearly delineated and of the
    # same length (256 + 256)
    colors_undersea = plt.cm.terrain(np.linspace(0, 0.17, 256))
    colors_land = plt.cm.terrain(np.linspace(0.25, 1, 256))
    all_colors = np.vstack([colors_undersea, colors_land])
    terrain_map = colors.LinearSegmentedColormap.from_list(
            'terrain_map', all_colors)

    class MidpointNormalize(colors.Normalize):
        def __init__(self, vmin=None, vmax=None, vcenter=None, clip=True):
            self.vcenter = vcenter
            colors.Normalize.__init__(self, vmin, vmax, clip)

        def __call__(self, value, clip=None):
            x, y = [self.vmin, self.vcenter, self.vmax], [0, 0.5, 1]
            return np.ma.masked_array(np.interp(value, x, y))

    # Karten-Objekt erstellen
    tmap = TopoMap('map_data.txt')

    # Contour-Parameter definieren
    c_min = np.floor(tmap.lowest_point()[2]/100)*100
    c_max = np.ceil(tmap.highest_point()[2]/100)*100
    c_levels = np.linspace(c_min, c_max, int((c_max - c_min)/100 + 1))
    midnorm = MidpointNormalize(vmin=c_min, vcenter=0, vmax=c_max)

    # --- Karte darstellen ----------------------------------------------------
    fig1, ax1 = plt.subplots()
    CS1 = ax1.contourf(
            tmap.X,
            tmap.Y,
            tmap.Z,
            c_levels,
            norm=midnorm,
            cmap=terrain_map
    )
    cbar1 = fig1.colorbar(CS1)
    cbar1.ax.set_ylabel('Meter über Meer')

    # Höchster und tiefster Punkt einzeichnen
    x_max, y_max, z_max = tmap.highest_point()
    ax1.plot(x_max, y_max, 'k^', label='höchster Punkt')
    ax1.text(x_max, y_max, r'$P_{H}$', va='bottom', ha='right')
    x_min, y_min, z_min = tmap.lowest_point()
    ax1.plot(x_min, y_min, 'yv', label='tiefster Punkt')
    ax1.text(x_min, y_min, r' $P_{L}$', va='center', ha='left', color='w')

    # Gradient folgen
    P1 = [6200, -5100]
    P2 = [-2500, -3000]
    pfad_abstieg = tmap.fall_line(P1)
    print('iter =', len(pfad_abstieg))
    pfad_aufstieg = tmap.fall_line(P2, descent=False)
    print('iter =', len(pfad_aufstieg))
    ax1.plot(pfad_abstieg[:, 0], pfad_abstieg[:, 1], 'b-', label='Abstieg')
    ax1.plot(pfad_aufstieg[:, 0], pfad_aufstieg[:, 1], 'r-', label='Aufstieg')
    ax1.text(*P1, r'$P_{1}$', va='top', ha='right')
    ax1.text(*pfad_abstieg[-1], r'$P_{3}$', va='bottom', ha='right')
    ax1.text(*P2, r'$P_{2}$', va='center', ha='left')
    ax1.text(*pfad_aufstieg[-1], r'$P_{4}$', va='top', ha='right', color='w')

    # Pfad A-B
    PA = [-9e3, -6e3]
    PB = [-8e3, -1.5e3]
    PC = [6e3, -2.5e3]
    pfad_ABC = np.c_[np.r_[np.linspace(PA[0], PB[0], 500),
                           np.linspace(PB[0], PC[0], 500)],
                     np.r_[np.linspace(PA[1], PB[1], 500),
                           np.linspace(PB[1], PC[1], 500)]]
    ax1.plot(*pfad_ABC.T, 'k-', label=r'$A\rightarrow B\rightarrow C$')
    ax1.text(*PA, 'A', va='top', ha='right')
    ax1.text(*PB, 'B', va='bottom', ha='center')
    ax1.text(*PC, 'C', va='bottom', ha='left')

    ax1.axis('image')
    ax1.set_xlabel('x (m)')
    ax1.set_ylabel('y (m)')
    ax1.grid(True)
    ax1.legend(loc='upper left')

    fig1.tight_layout()
#    fig1.savefig('topomap_all.pdf')

    # --- Höhenprofile darstellen ---------------------------------------------
    fig2, ax2 = plt.subplots(figsize=(4, 2.5))

    weg_abstieg, hoehe_abstieg = tmap.elevation_profile(pfad_abstieg)
    ax2.plot(weg_abstieg, hoehe_abstieg, label='Abstieg')

    weg_aufstieg, hoehe_aufstieg = tmap.elevation_profile(pfad_aufstieg)
    ax2.plot(weg_aufstieg, hoehe_aufstieg, label='Aufstieg')

    weg_ABC, hoehe_ABC = tmap.elevation_profile(pfad_ABC)
    ax2.plot(weg_ABC, hoehe_ABC, label=r'$A\rightarrow B\rightarrow C$')

    ax2.set_xlabel('2D-Distanz (m)')
    ax2.set_ylabel('Höhe (m ü. M.)')
    ax2.grid(True)
    ax2.legend(loc='upper right')
    fig2.tight_layout()
#    fig2.savefig('elevation_profile.pdf')

    # --- 3D-Weglänge bestimmen ----------------------------------------------
    weglaenge, hoehenmeter = tmap.distance_travelled(pfad_ABC)
    print('3D-Weglänge = {:.0f}m'.format(weglaenge))
    print('Höhenmeter = {:.0f}m'.format(hoehenmeter))

    fig4, ax4 = plt.subplots(figsize=(4, 2))
    path4 = np.array([[0, -2e3], [1e3, -2e3], [1e3, -3e3], [0, -3e3]])
    d, z = tmap.elevation_profile(path4)
    ax4.plot(d[:3], z[:3], 'ro-', label='positive Steigung')
    ax4.plot(d[2:], z[2:], 'bo-', label='negative Steigung')
    ax4.grid(True)
    ax4.set_xlabel('2D-Distanz')
    ax4.set_ylabel('Höhe')
    ax4.legend(loc='lower right')
    fig4.tight_layout()
#    fig4.savefig('distance_travelled.pdf')

    # --- Karte ausrichten ----------------------------------------------------
    fig3, ax3 = plt.subplots()
    ursprung = [5165, -6601]
    referenz = [-7052, -4115]
    X_copy, Y_copy, Z_copy, A = tmap.aligned_map(ursprung, referenz)
    neue_referenz = A @ (np.array(referenz) - np.array(ursprung))
    ax3.contourf(
            X_copy,
            Y_copy,
            tmap.Z,
            c_levels,
            norm=midnorm,
            cmap=terrain_map,
    )
    ax3.axis('image')
    ax3.grid(True)
    ax3.plot(0, 0, 'b^', label='P')
    ax3.plot(neue_referenz[0], neue_referenz[1], 'ro', label='Q')
    ax3.set_xlabel(r'$\tilde{x}$ (m)')
    ax3.set_ylabel(r'$\tilde{y}$ (m)')
    ax3.legend()
    fig3.tight_layout()
#    fig3.savefig('oriented_map.pdf')

    plt.show()
