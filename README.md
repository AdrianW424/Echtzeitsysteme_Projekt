# Echtzeitsysteme Projekt

## Aufgabenstellung
-> Entwicklung eines Programmes, welches ein Ablaufdiagramm aus einer CSV Datei einlesen und visualisieren kann.

## TODO:
HIGH-Priority:
* Frontend:
    * vielleicht kleines Fenster mit CSV-Inhalt. Sowas wie Editor, in dem man live code ändern kann
    * Frontend CSV-Editor - Button zum neu laden des Bildes fertig machen
    * Abbrechen der Animation. Zum Beispiel mit Timer, dessen Intervall zurückgesetzt wird, sobald Button geklickt (statt sleep)
* Backend:
    * Animationsalgorithmus entwickeln und implementieren - 95% fertig (genauere Tests durchführen)
        * keine genauen Probleme bekannt. Zu testen siehe TOTEST unten
    * Semaphoren currentValue nicht nur auf 0 und 1, sondern auch über 1 hinaus setzen können
    * Activity mit Duration 0 -> refresh für andere Activities (Problem derzeit: 
        * Activity nach Activity mit duration 0 nicht sofort grün geschaltet - erst in nächstem Takt wird die Activity danach ausgeführt - braucht einen Takt, obwohl 0 Takte angegeben)
        * 88e544e - dataTest2.csv - Activity 2 mit Duration 0 wird übersprungen und Semaphore dahinter erst in nächstem Takt aktivier
    * GIF Problem mit Bildergröße. Wenn Initialisierung von Semaphore verschwindet, wird Bild kleiner. Teil des GIFs ändert sich nicht

MEDIUM-Priority:
* Backend:
    * Programm unabhängig gegenüber falschen Eingaben in CSV-Datei machen - Input-Prüfer schreiben (überprüft die Datei, bevor sie eingelesen wird)

LOW-Priority:
* Backend:
    * Programm verschönern - bessere Verteilung der Objekte

## TOTEST:
* Mehrere Semaphoren mit unterschiedlichen Initialwert
* Activity mit Duration 0
* Mutex mehrere
* Mutexs unterschiedflichen Tasks zugeordnet, nicht immer den beiden gleichen Activities

## Input-Prüfer:
* Überprüfung der Spaltennamen sowie der einzelnen Zellen der Spalte (jeweils prüfen, ob eingegebene Daten korrekt sind)
* Überprüfung der Spaltenanzahl, damit nicht zu viele und nicht zu wenige vorhanden sind

* Alternativ einfach try-ecxept verwenden, ohne genaue Prüfung der einzelnen Zellen