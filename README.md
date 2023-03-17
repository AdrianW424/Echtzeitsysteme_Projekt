# Echtzeitsysteme Projekt

## Aufgabenstellung
-> Entwicklung eines Programmes, welches ein Ablaufdiagramm aus einer CSV Datei einlesen und visualisieren kann.

## TODO:
HIGH-Priority:
* Frontend:
    * in Mitte wird jpg oder so dargestellt
    * User Interface mit Buttons (Animation/Bild speichern, Animation automatisch abspielen)
    * Button zum automatischen Abspielen der Animation (vielleicht mit Auswahl wie viel Zeit zwischen den Bildern sein soll)
    * vielleicht kleines Fenster mit CSV-Inhalt. Sowas wie Editor, in dem man live code ändern kann
* Animationsalgorithmus entwickeln und implementieren - 95% fertig (genauere Tests durchführen)
    * keine genauen Probleme bekannt. Zu testen siehe TOTEST unten
* Semaphoren currentValue nicht nur auf 0 und 1, sondern auch über 1 hinaus setzen können
* Activity mit Duration 0 -> refresh für andere Activities (Problem derzeit: 
    * Activity nach Activity mit duration 0 nicht sofort grün geschaltet - erst in nächstem Takt wird die Activity danach ausgeführt - braucht einen Takt, obwohl 0 Takte angegeben)
* Initialisierungswert erst nach einem Takt eingesetzt, davor bleibt Semaphore leer - Nur am Anfang sollte das so sein, danach sollte der Wert sofort gesetzt werden
    * weiteres Problem: manchmal wird Initialisierungswert geschluckt, wenn eine Activity abgearbeitet ist, obwohl die Activity die Semaphore schon aktivieren sollte (vielleicht nur Anzeigefehler, aufgrund von dem oberen Problem)

MEDIUM-Priority:
* Programm verschönern - bessere Verteilung der Objekte

LOW-Priority:
* Programm unabhängig gegenüber falschen Eingaben in CSV-Datei machen

## TOTEST:
* Mehrere Semaphoren mit unterschiedlichen Initialwert
* Activity mit Duration 0
* Mutex mehrere
* Mutexs unterschiedflichen Tasks zugeordnet, nicht immer den beiden gleichen Activities