# -*- coding: utf-8 -*-
# quizrangliste.py

# -----------------------------------------------------------------------------
class QuizRangliste():

    def __extract_file_data(self, file):
        for zeile in file:
            elemente = zeile.strip().split(',')
            # array of array... or would be an array of object better? 2Do
            self.__file_data.append(elemente)
            # 2Do:
            # Leere oder ungültige Zeilen werden ignoriert.

    def __init__(self, datei='default.txt'):
        '''Initialisiert der Rangliste.
        List die Daten aus der angegebenen Textdatei (encoding='utf-8') aus
        und bereitet diese zur Abfrage vor.

        Leere oder ungültige Zeilen werden ignoriert.

        Erstellt eine neue, leere Datei, falls
        die angegebene Datei noch nicht existiert.

        Argumente:
            type(datei) == str -- Pfad zur Textdatei mit den Ranglistendaten.
        '''
        self.__file_data = []

        # "with" closes files implicitly
        try:
            # file exists - open for reading
            with open(datei, 'r', encoding='utf-8') as file:
                self.__extract_file_data(file)
        except FileNotFoundError:
            # file not exists - create it (w+ wipes file so I need 2 exceptions...)
            try:
                with open(datei, 'w+', encoding='utf-8') as file:
                    self.__extract_file_data(file)
            except:
                print("Fehlende Berechtigung auf dem Dateisystem!")

        print(self.__file_data);

    def als_dictionary(self):
        '''
        Gibt die iDaten als Dictionary von Dictionaries zurück:
            Key = name, Value = {’Punkte’: punkte, ’Zeit’: zeit}

        Die Datentypen der Elemente sind:
            type(name) == str,
            type(punkte) == int,
            type(zeit) == float
        '''
        # ...
        pass

    def als_liste(self):
        '''
        Gibt eine Liste von Tupeln (name, punkte, zeit) zurück.
            Key = name, Value = {’Punkte’: punkte, ’Zeit’: zeit}

        Die Datentypen der Elemente sind:
            type(name) == str,
            type(punkte) == int,
            type(zeit) == float

        Die Liste ist nach den folgenden Prioritäten sortiert:
            1. Punkte, absteigend
            2. Zeit, aufsteigend
            3. Name, alphabetisch aufsteigend: A=>Z
        '''
        # ...
        pass

    def als_string(self):
        '''
        Gibt die Daten als formatierten String zurück.

        Das Zeilen-Format ist:
            Name | Punkte | Zeit

            wobei Punkte == Ganzzahl und Zeit == Float (auf 1 Kommastelle gerundet)

            Die Spaltenbreite ist für alle Zeilen gleich und wird
            dynamisch anhand des längsten Elements in der jeweiligen Spalte ermittelt.

            Die Ausrichtungen sind:
                Name=linksbündig, Punkte=rechtsbündig, Zeit=rechtsbündig.

        Die Liste ist nach den folgenden Prioritäten sortiert:
            1. Punkte, absteigend
            2. Zeit, aufsteigend
            3. Name, alphabetisch aufsteigend: A=>Z
        '''
        # ...
        pass

    def resultat_addieren(self, name, punkte, zeit):
        '''
        Fügt einer Person (name) weitere Punkte und Zeit hinzu.

        Falls name bereits in den internen Daten existiert:
            punkte und zeit hinzuaddieren.
        Falls name nicht existiert: neuen Namen anlegen.

        Argumente:
            type(name) == str, (darf keine Kommazeichen enthalten)
            type(punkte) == int oder str,
            type(zeit) == float oder str

        Rückgabewert:
            False bei ungültigen Argumenten,
            True falls fehlerfrei.
        '''
        # ...
        pass

    def name_entfernen(self, name):
        '''
        Löscht den die Person (name ink punkte und zeit) von der Liste.
        Falls die angegebene Person (name) nicht in der Liste ist, passiert nichts.

        Falls name bereits in den internen Daten existiert:
            punkte und zeit hinzuaddieren.
        Falls name nicht existiert: neuen Namen anlegen.

        Argumente:
            type(name) == str
        '''
        # ...
        pass

    def speichern(self, als=None):
        '''
        Schreibt die Daten als Kommagetrennte Werte in die ursprüngliche Textdatei.
        Falls das Argument als angegeben wird:
            schreibt die Daten in die angegebene Datei anstatt in die ursprüngliche Datei.
        Die Datei wird mit encoding=’utf-8’ geschrieben

        Die Liste ist nach den folgenden Prioritäten sortiert:
            1. Punkte, absteigend
            2. Zeit, aufsteigend
            3. Name, alphabetisch aufsteigend: A=>Z
        '''
        # ...
        pass

# --- Test --------------------------------------------------------------------
if __name__ == '__main__':
    qr = QuizRangliste(datei='rangliste.txt')

    d = qr.als_dictionary()
    print(d)
    #{’Noemi’: {’Punkte’: 7, ’Zeit’: 40.0}, ’Max’: {’Punkte’: 6, ’Zeit’: 100.02},
    #’Hans’: {’Punkte’: 2, ’Zeit’: 45.24}, ’Anna’: {’Punkte’: 5, ’Zeit’: 20.55},
    #’Fritz’: {’Punkte’: 5, ’Zeit’: 39.3}, ’Laura’: {’Punkte’: 5, ’Zeit’: 20.55}}

    lst = qr.als_liste()
    print(lst)
    #[(’Noemi’, 7, 40.0), (’Max’, 6, 100.02), (’Anna’, 5, 20.55),
    #(’Laura’, 5, 20.55), (’Fritz’, 5, 39.3), (’Hans’, 2, 45.24)]

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
