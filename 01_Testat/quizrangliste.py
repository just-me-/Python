# -*- coding: utf-8 -*-
# quizrangliste.py

import re


class QuizRangliste():
    '''Schnittstelle zur Verwaltung der HSRvote-Software-Textdaten.'''

    def __extract_file_data(self, file):
        for zeile in file:
            try:
                # Leere oder ungültige Zeilen werden ignoriert.
                if re.match(r'\w+,.*,.*$', zeile.strip()) is None:
                    continue
                elemente = zeile.strip().split(',')
                self.__file_data[elemente[0]] = {
                    'Punkte': int(elemente[1]),
                    'Zeit': float(elemente[2])
                }
            except Exception:
                continue

    def __write_data_to_file(self, file):
        try:
            with open(file, 'w+', encoding='utf-8') as file:
                for line in self.als_liste():
                    file.write(
                        line[0] + ',' +
                        str(line[1]) + ',' +
                        str(round(line[2], 1)) + '\n'
                    )
        except Exception:
            print("Fehlende Berechtigung auf dem Dateisystem!")

    def __init__(self, datei='default.txt'):
        '''
        Initialisierung der Rangliste.
        List die Daten aus der angegebenen CSV-Textdatei (encoding='utf-8')
        aus und bereitet diese zur Abfrage vor.

        Leere oder ungültige Zeilen werden ignoriert.

        Erstellt eine neue, leere Datei, falls
        die angegebene Datei noch nicht existiert.

        Argumente:
            datei: string -- Pfad zur Textdatei mit den Ranglistendaten.
        '''
        self.__file_data = {}
        self.__file_name = datei

        # "with" closes files implicitly
        try:
            # file exists - open for reading
            with open(datei, 'r', encoding='utf-8') as file:
                self.__extract_file_data(file)
        except Exception:
            # file not exists - create it
            try:
                with open(datei, 'w+', encoding='utf-8') as file:
                    self.__extract_file_data(file)
            except Exception:
                print("Fehlende Berechtigung auf dem Dateisystem!")

    def als_dictionary(self):
        '''
        Gibt die Daten als Dictionary von Dictionaries zurück:
            Key = name, Value = {’Punkte’: punkte, ’Zeit’: zeit}

        Die Datentypen der Elemente sind:
            name: string,
            punkte: int,
            zeit: float
        '''
        return self.__file_data

    def als_liste(self):
        '''
        Gibt eine Liste von Tupeln (name, punkte, zeit) zurück.
            Key = name, Value = {’Punkte’: punkte, ’Zeit’: zeit}

        Die Datentypen der Elemente sind:
            name: string,
            punkte: int,
            zeit: float

        Die Liste ist nach den folgenden Prioritäten sortiert:
            1. Punkte, absteigend
            2. Zeit, aufsteigend
            3. Name, alphabetisch aufsteigend: A=>Z
        '''
        arr = []
        for key, value in self.__file_data.items():
            arr.append((key, value['Punkte'], value['Zeit']))
        return sorted(arr, key=lambda x: (-x[1], x[2], x[0]))

    def als_string(self):
        '''
        Gibt die Daten als formatierten String zurück.

        Das Zeilen-Format ist:
            Name | Punkte | Zeit

            wobei Punkte == Ganzzahl und
            Zeit == Float (auf 1 Kommastelle gerundet)

            Die Spaltenbreite ist für alle Zeilen gleich und wird
            dynamisch anhand des längsten Elements
            in der jeweiligen Spalte ermittelt.

            Die Ausrichtungen sind:
                Name=linksbündig, Punkte=rechtsbündig, Zeit=rechtsbündig.

        Die Liste ist nach den folgenden Prioritäten sortiert:
            1. Punkte, absteigend
            2. Zeit, aufsteigend
            3. Name, alphabetisch aufsteigend: A=>Z
        '''
        string = ''
        arr = self.als_liste()

        if(len(arr) > 0):
            name_len = max([len(x) for x in self.__file_data])
            punkte_len = max(
                [len(str(self.__file_data[x]['Punkte']))
                    for x in self.__file_data]
            )
            zeit_len = max(
                [len(str(round(self.__file_data[x]['Zeit'], 1)))
                    for x in self.__file_data]
            )

            for line in arr:
                string += line[0].ljust(name_len, ' ') + ' | '
                string += str(line[1]).rjust(punkte_len, ' ') + ' | '
                string += str(round(line[2], 1)).rjust(zeit_len, ' ') + '\n'
        return string

    def resultat_addieren(self, name, punkte, zeit):
        '''
        Fügt einer Person (name) weitere Punkte und Zeit hinzu.

        Falls name bereits in den internen Daten existiert:
            punkte und zeit hinzuaddieren.
        Falls name nicht existiert: neuen Namen anlegen.

        Argumente:
            name: string, (darf keine Kommazeichen enthalten)
            punkte: int oder string,
            zeit: float oder string

        Rückgabewert:
            False: Boolean - bei ungültigen Argumenten,
            True: Boolean -  falls fehlerfrei.
        '''
        if ',' in name:
            return False
        try:
            name = str(name)
            punkte = int(punkte)
            zeit = float(zeit)
        except Exception:
            return False

        if name in self.__file_data:
            self.__file_data[name]['Punkte'] += punkte
            self.__file_data[name]['Zeit'] += zeit
        else:
            self.__file_data[name] = {'Punkte': punkte, 'Zeit': zeit}

        return True

    def name_entfernen(self, name):
        '''
        Löscht die Person (name, punkte und zeit) von der Liste.
        Falls die angegebene Person (name) nicht in der Liste ist,
        passiert nichts.

        Argumente:
            name: string
        '''
        if name in self.__file_data:
            del self.__file_data[name]

    def speichern(self, als=None):
        '''
        Schreibt die Daten als Kommagetrennte Werte (CSV)
        in die ursprüngliche Textdatei.

        Falls das Argument 'als' angegeben wird:
            schreibt die Daten in die angegebene Datei
            anstatt in die ursprüngliche Datei.

        Die Datei wird mit encoding=’utf-8’ geschrieben

        Die Liste ist nach den folgenden Prioritäten sortiert:
            1. Punkte, absteigend
            2. Zeit, aufsteigend
            3. Name, alphabetisch aufsteigend: A=>Z
        '''
        if als is None:
            als = self.__file_name
        self.__write_data_to_file(als, )


# --- Test --------------------------------------------------------------------
if __name__ == '__main__':
    qr = QuizRangliste(datei='rangliste.txt')

    d = qr.als_dictionary()
    print(d)
    # {’Noemi’: {’Punkte’: 7, ’Zeit’: 40.0},
    # ’Max’: {’Punkte’: 6, ’Zeit’: 100.02},
    # ’Hans’: {’Punkte’: 2, ’Zeit’: 45.24},
    # ’Anna’: {’Punkte’: 5, ’Zeit’: 20.55},
    # ’Fritz’: {’Punkte’: 5, ’Zeit’: 39.3},
    # ’Laura’: {’Punkte’: 5, ’Zeit’: 20.55}}

    lst = qr.als_liste()
    print(lst)
    # [(’Noemi’, 7, 40.0), (’Max’, 6, 100.02), (’Anna’, 5, 20.55),
    # (’Laura’, 5, 20.55), (’Fritz’, 5, 39.3), (’Hans’, 2, 45.24)]

    s = qr.als_string()
    print(s)
    # Noemi | 7 | 40.0
    # Max   | 6 | 100.0
    # Anna  | 5 | 20.6
    # Laura | 5 | 20.6
    # Fritz | 5 | 39.3
    # Hans  | 2 | 45.2

    qr.resultat_addieren(name='Noemi', punkte=7, zeit=50.4)
    qr.resultat_addieren(name='Noemi', punkte='7', zeit='50.4')
    print(qr.als_string())
    # Noemi | 21 | 140.8
    # Max   |  6 | 100.0
    # Anna  |  5 | 20.6
    # Laura |  5 | 20.6
    # Fritz |  5 | 39.3
    # Hans  |  2 | 45.2

    qr.name_entfernen(name='Fritz')
    print(qr.als_string())
    # Noemi | 21 | 140.8
    # Max   |  6 | 100.0
    # Anna  |  5 | 20.6
    # Laura |  5 | 20.6
    # Hans  |  2 | 45.2

    qr.speichern()
    qr.speichern(als='neue rangliste.txt')

    # help(QuizRangliste)
