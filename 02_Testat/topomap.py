# -*- coding: utf-8 -*-
# topomap.py


class TopoMap():
    '''Liest Höhendaten aus einer Textdatei ein. Bereitet Informationen für Sportler auf.'''

    def __init__(self, fname='map_data.txt'):
        '''
        Initialisierung der Map-Daten.
        List die Daten aus der angegebenen CSV-Textdatei (encoding='utf-8')
        aus und bereitet diese zur Abfrage vor.

        Leere oder ungültige Zeilen werden ignoriert.

        Erstellt eine neue, leere Datei, falls
        die angegebene Datei noch nicht existiert.

        Argumente:
            datei: string -- Pfad zur Textdatei mit den Ranglistendaten.
        '''
        self.X = self.Y = self.Z = 0

        # Text einlesen
        # numpy.loadtxt()

    def highest_point(self):
        '''
        Liefert Tupel von 3D-Koordinaten (x, y,z) des höchsten Punkts.
        '''
        pass

    def lowest_point(self):
        '''
        Liefert Tupel von 3D-Koordinaten (x, y,z) des tiefsten Punkts.
        '''
        pass

    def elevation(self, position):
        '''
        Liefert die interpolierte Höhe z an der angegebenen Position [x, y]
        Das Argument kann  ein zweidimensionales NumPy-Array oder Liste sein,
        welche mehrere Positionen beinhaltet.
        '''
        pass

    def elevation_profile(self, path):
        '''
        Gibt das Höhenprofil in Abhängigkeit zur Diestanz an.
        Dar Argument definiert einen Pfad auf der Karte, bestehend aus einem
        2D NumPy Array oder einer Liste von Punkten (x,y).
        Rückgabe zwei NumPy Arrays:
            - Distanzen
            - Interpolierten Höhen
        '''
        pass

    def distance_tavelled(self, path):
        '''
        Liefert zurückgelegten Weg und überwundene Höhenmeter.
        Dar Argument definiert einen Pfad auf der Karte, bestehend aus einem
        2D NumPy Array oder einer Liste von Punkten (x,y).
        Rückgabe zwei Zahlen:
            - Totale Länge des Wegs
            - Überwundenen Höhenmeter
        '''
        pass

    def fall_line(self, start, descent=True, gamma=50, max_iter=10000, precision=0.1):
        '''
        Liefert die Fallinie eines Hanges.
        Mit descent=False kann die Richtung gekehrt werden (bergauf statt bergab steigen)
        Rückgabe des Pfads als 2D NumPy Array.
        '''
        pass

    def aligned_map(self, p, q):
        '''
        Richtet Karte neu aus.
        Parameter: zwei Referenzpunkte P=[x, y] und Q=[x, y]
            - P ist der Ursprung des koordinatensystems.
            - Q soll anschliessend genau im Norden des Ursprungs liegen.

        4 NumPy-Arrays als Rückgabewerte:
            - X_new: Array der neuen x-Werte (rotierte Kartenpunkte)
            - Y_new: Array der neuen y-Werte (rotierte Kartenpunkte)
            - Z_new: die kopierten z-Werte der Kartenpunkte
            - A: die Rotationsmatrix (gemäss eine 2 x 2-Matrix)
        '''
        pass


# --- Test --------------------------------------------------------------------
if __name__ == '__main__':
    print('Hellöw')
    tmap = TopoMap()
    print(tmap.X)
    tmap.X = 3
    # AttributeError: can’t set attribute
