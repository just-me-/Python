# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 13:40:31 2019

@author: Tom-LT
"""
import re


class QuizRangliste:
    """Eine Klasse zur Verwaltung der Quiz-Resultate mit HSRVote.
    Liesst CSV Daten ein, verwaltet diese, zeigt sie an,
    und speichert sie wieder."""

    __content = ""
    __datei = ""
    __REGEX = r'(?P<name>[a-zA-z]+),(?P<score>\d+),(?P<time>\d+\.\d+)'

    @staticmethod
    def validLine(line):
        match = re.search(QuizRangliste.__REGEX, line)
        return match is not None

    def __init__(self, datei):
        """Initialisiert die Rangliste.
        Liesst die Daten aus der angegebenen Textdatei (encoding='utf-8') aus
        und bereitet diese zur Abfrage vor.
        Leere oder ungültige Zeilen werden ignoriert.
        Erstellt eine neue, leere Datei, falls
        die angegebene Datei noch nicht existiert."""
        self.__datei = datei

        try:
            with open(datei) as f:
                for line in f:
                    if QuizRangliste.validLine(line):
                        self.__content += line
            # haben immer ne newline für resultat_addieren
            self.__content += "\n"

        except FileNotFoundError:
            f = open(datei, 'w')
            f.close()

    def speichern(self, als=None):
        """Speichert das Objekt als Datei ab.
        Falls ein Argument angegeben wird,
        wird eine Datei gemäss Argument erstellt."""
        if (als is None):
            als = self.__datei
        with open(als, 'w') as f:
            f.write(self.__content)

    def als_dictionary(self):
        """Gibt ein Dictionary der Instanz zurück
        Die Form ist: Key = name, Value = {’Punkte’: punkte, ’Zeit’: zeit}"""
        dic = {}
        for line in self.__content.splitlines():
            match = re.search(self.__REGEX, line)
            if match is not None:
                name = match[1]
                score = int(match[2])
                time = float(match[3])
                dic[name] = {"Punkte": score, "Zeit": time}
        return dic

    def als_liste(self):
        """Gibt eine Liste von Tupeln (name, punkte, zeit) zurück.
            Key = name, Value = {’Punkte’: punkte, ’Zeit’: zeit}
        Die Liste ist nach den folgenden Prioritäten sortiert:
            1. Punkte, absteigend
            2. Zeit, aufsteigend
            3. Name, alphabetisch aufsteigend: A=>Z
        """
        result = []
        for name, data in self.als_dictionary().items():
            score = data["Punkte"]
            time = data["Zeit"]
            result.append((name, score, time))

        # nutze Stabilität der Sortierung aus:
        result.sort(key=lambda x: x[0], reverse=False)
        result.sort(key=lambda x: x[2], reverse=False)
        result.sort(key=lambda x: x[1], reverse=True)
        return result

    def als_string(self):
        """Gibt die Daten als formatierten String zurück.
        Das Zeilen-Format ist:
            Name | Punkte | Zeit"""
        # block für dyn länge, aber wie da unten in den
        # string format reinkriegen?
        maxlength = 0
        for name in self.als_dictionary().keys():
            if len(name) > maxlength:
                maxlength = len(name)

        result = ""
        for data in self.als_liste():
            result += '{:<8} | {:>2} | {:>5.1f}\n'.format(*data)
            # dynamische länge???
        return result

    def resultat_addieren(self, name, punkte, zeit):
        """Fügt einer Person (name) weitere Punkte und Zeit hinzu.
        Falls name bereits in den internen Daten existiert:
            punkte und zeit hinzuaddieren.
        Falls name nicht existiert: neuen Namen anlegen.

        Argumente:
            type(name) == str, (darf keine Kommazeichen enthalten)
            type(punkte) == int oder str,
            type(zeit) == float oder str

        Rückgabewert:
            False bei ungültigen Argumenten,
            True falls fehlerfrei."""
        datadict = self.als_dictionary()

        if (name in datadict.keys()):
            currentdata = datadict[name]
            old_punkte = int(currentdata["Punkte"])
            old_zeit = float(currentdata["Zeit"])
            new_punkte = old_punkte + int(punkte)
            new_zeit = old_zeit + float(zeit)

            # wir lsöchen die zeile und schreiben sie neu, ist einfacher
            self.name_entfernen(name)
            self.__content += ",".join(
                    [name, str(new_punkte), str(new_zeit)]) + '\n'

        else:
            self.__content += ",".join([name, str(punkte), str(zeit)]) + '\n'

    def name_entfernen(self, name):
        """Löscht den die Person (name ink punkte und zeit) von der Liste.
        Falls die angegebene Person (name) nicht in der Liste ist,
        passiert nichts.
        Falls name bereits in den internen Daten existiert:
            punkte und zeit hinzuaddieren.
        Falls name nicht existiert: neuen Namen anlegen."""
        if (name not in self.als_dictionary().keys()):
            return
        match = re.search(
                r'{}.+$'.format(name), self.__content, re.MULTILINE)
        von = match.start()
        bis = match.end()+1
        self.__content = self.__content[:von] + self.__content[bis:]


qr = QuizRangliste("Söhne.txt")
qr = QuizRangliste(datei='rangliste.txt')

print(qr.als_dictionary())
print()
print(qr.als_liste())
print()
print(qr.als_string())
print()
qr.resultat_addieren("Tom", 10, 5.0)
qr.resultat_addieren("Tom", 10, 15.0)
print(qr.als_string())

print()
print(qr.name_entfernen("Hans"))
print(qr.als_string())
print()
qr.resultat_addieren(name='Noemi', punkte=7, zeit=50.4)
qr.resultat_addieren(name='Noemi', punkte='7', zeit='50.4')
print(qr.als_string())
qr.speichern()
qr.speichern(als="Wiegeht")
