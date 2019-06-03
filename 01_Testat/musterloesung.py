# -*- coding: utf-8 -*-
# Python Testat 1 - MusterlÃ¶sung

import copy
import operator
import os


class QuizRangliste:
    '''Verwaltet die Rangliste eines Quizzes.'''

    def __init__(self, datei, **kwargs):
        '''Ã–ffnet die angegebene Datei und extrahiert deren Daten.

        Argumente:
            datei -- Pfad der Datei
        '''
        # kooperative superclass calls
        super().__init__(**kwargs)

        # Dateipfad merken
        self.__datei = datei

        # Datei einlesen
        self.__datei_einlesen()

    def __datei_einlesen(self):
        # neues Dictionary
        self.__daten = dict()

        # falls die Datei nicht existiert
        if not os.path.isfile(self.__datei):
            # leere Datei erstellen
            with open(self.__datei, 'w'):
                pass

        # Datei zum Lesen Ã¶ffnen
        with open(self.__datei, encoding='utf-8') as f:
            # zeilenweise abarbeiten
            for line in f:
                # Zeile in einzelne Elemente aufteilen
                items = [x.strip() for x in line.split(',')]

                # falls die Zeile nicht genau drei Elemente hat
                if len(items) != 3:
                    # Zeile Ã¼berspringen
                    continue

                try:
                    # neuer Dictionary-Eintrag hinzufÃ¼gen
                    self.__daten[items[0]] = {
                        'Punkte': int(float(items[1])),
                        'Zeit': float(items[2]),
                    }
                except ValueError:
                    # Zeile Ã¼berspringen, falls ungÃ¼ltige Zahlen
                    continue

    def als_dictionary(self):
        '''Liefert die internen Daten als Dictionary.
        '''
        # tiefe Kopie des internen Dictionary zurÃ¼ckgeben
        return copy.deepcopy(self.__daten)

    def als_liste(self):
        '''Liefert die internen Daten als sortierte Liste.
        '''
        # leere Liste
        liste = []

        # Daten in neue Liste abfÃ¼llen
        for key, value in self.__daten.items():
            # als Tupel (Name, Punkte, Zeit)
            liste.append((key, value['Punkte'], value['Zeit']))

        # Daten nach aufsteigender PrioritÃ¤t sortieren
        # tiefste PrioritÃ¤t: nach dem Namen (0) aufsteigend sortieren
        # mittlere PrioritÃ¤t: nach der Zeit (2) aufsteigend sortieren
        liste.sort(key=operator.itemgetter(2, 0))
        # hÃ¶chste PrioritÃ¤t: nach der Punktezahl (1) absteigend sortieren
        liste.sort(key=operator.itemgetter(1), reverse=True)

        # sortierte Liste zurÃ¼ckgeben
        return liste

    def als_string(self):
        '''Liefert die internen Daten als formatierten String.
        '''
        # Daten als sortierte Liste
        liste = self.als_liste()

        # Listenelemente in formatierte Strings umwandeln
        liste_str = [(name, '{:d}'.format(punkte), '{:.1f}'.format(zeit))
                     for name, punkte, zeit in liste]

        # maximale Spaltenbreiten bestimmen
        maxlen = [max([len(x) for x in spalte])
                  for spalte in zip(*liste_str)]

        # String zusammenbauen, MaximallÃ¤ngen berÃ¼cksichtigen
        s = '\n'.join(
                ['{:<{}} | {:>{}} | {:>{}}'.format(
                        *[x
                          for zm in zip(zeile, maxlen)
                          for x in zm])
                 for zeile in liste_str]
        )

        # formatierten String zurÃ¼ckgeben
        return s

    def resultat_addieren(self, name, punkte, zeit):
        '''FÃ¼gt ein neues Teilresultat zu den bestehenden Daten hinzu.

        Argumente:
            name -- Name des Teilnehmers
            punkte -- Anzahl der erreichten Punkten
            zeit --  BenÃ¶tigte Zeit in Sekunden
        '''
        # falls der Name kein String ist
        if not isinstance(name, str):
            # Fehler zurÃ¼ckgeben
            return False

        # falls Kommazeichen im Namen enthalten sind
        if ',' in name:
            # Fehler zurÃ¼ckgeben
            return False

        # falls Punkte und Zeit sich nicht umwandeln lassen
        try:
            punkte = int(float(punkte))
            zeit = float(zeit)
        except ValueError:
            # Fehler zurÃ¼ckgeben
            return False

        # falls der Name schon existiert
        if name in self.__daten:
            # Zeit und Punkte addieren
            self.__daten[name]['Punkte'] += punkte
            self.__daten[name]['Zeit'] += zeit
        else:
            # neuer Eintrag erstellen
            self.__daten[name] = {
                    'Punkte': punkte,
                    'Zeit': zeit
            }

        # alles OK
        return True

    def name_entfernen(self, name):
        '''Entfernt den Eintrag mit dem angegebenen Namen.

        Argumente:
            name -- Name des Teilnehmers
        '''
        # Name aus dem Dictionary entfernen
        self.__daten.pop(name, None)

    def speichern(self, als=None):
        '''Speichert die internen Daten in die Datei ab.

        Argumente:
            als -- Alternativer Dateipfad, falls angegeben
        '''
        # falls kein alternativer Dateipfad angegeben
        if als is None:
            # ursprÃ¼nglichen Dateipfad Ã¼bernehmen
            als = self.__datei

        # Datei zum Schreiben Ã¶ffnen
        with open(als, 'w', encoding='utf-8') as f:
            # Daten zeilenweise und Komma-separiert abspeichern
            f.write(
                '\n'.join(
                        [','.join([str(x) for x in zeile])  # alles als String
                         for zeile in self.als_liste()]
                )
            )


# === Test ====================================================================
if __name__ == '__main__':
    qr = QuizRangliste(datei='rangliste.txt')
#    qr = QuizRangliste(datei='rangliste_neu.txt')
    qr.resultat_addieren('Noemi', 7, 50.4)
    print(qr.resultat_addieren('Noemi', '7', '50.4'))
    print(qr.resultat_addieren('Test,Komma', '7', '50.4'))
    print(qr.als_dictionary())
    print(qr.als_liste())
    print(qr.als_string())
    qr.name_entfernen('Fritz')
    qr.name_entfernen('Hugo')
    qr.name_entfernen('Unbekannter')
    print('---')
    print(qr.als_string())
#    qr.speichern()
#    qr.speichern('rangliste_temp.txt')
#    print('\n'.join(dir(qr)))
#    print(qr.__doc__)
#    print(qr.__init__.__doc__)
#    help(qr)
#    print(qr.__dict__)