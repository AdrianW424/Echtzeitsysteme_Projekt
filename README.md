# Echtzeitsysteme Projekt

## Aufgabenstellung
-> Entwicklung eines Programmes, welches ein Ablaufdiagramm aus einer CSV Datei einlesen und visualisieren kann.

## TODO:
HIGH-Priority:
* Frontend:
    * in Mitte wird jpg oder so dargestellt
    * User Interface mit Buttons (Animation/Bild speichern, Animation automatisch abspielen)
    * Button zum automatischen Abspielen der Animation (vielleicht mit Auswahl wie viel Zeit zwischen den Bildern sein soll)
* Animationsalgorithmus entwickeln und implementieren - 95% fertig (genauere Tests durchführen)
* Semaphoren currentValue nicht nur auf 0 und 1, sondern auch über 1 hinaus setzen können
* Activity mit Duration 0 -> refresh für andere Activities

MEDIUM-Priority:
* Programm verschönern

LOW-Priority:
* Programm unabhängig gegenüber falschen Eingaben in CSV-Datei machen

## TOTEST:
* Mehrere Semaphoren mit unterschiedlichen Initialwert
* Activity mit Duration 0
* Mutex mehrere