# Echtzeitsysteme Projekt

## Aufgabenstellung
-> Entwicklung eines Programmes, welches ein Ablaufdiagramm aus einer CSV Datei einlesen und visualisieren kann.

## TODO:
HIGH-Priority:
* Frontend:
    * in Mitte wird jpg oder so dargestellt
    * User Interface mit Buttons (Datei laden, Animation beginnen (Animation weitergehen, Animation zurückgehen, Animation/Bild speichern))
    * Datei (CSV) muss irgendwie geladen werden können
* Animationsalgorithmus entwickeln und implementieren - 90% fertig (genauere Tests durchführen, Mutex einbauen)
* Semaphoren currentValue nicht nur auf 0 und 1, sondern auch über 1 hinaus setzen können

MEDIUM-Priority:
* Programm verschönern

LOW-Priority:
* Programm unabhängig gegenüber falschen Eingaben in CSV-Datei machen

## TOTEST:
* Mehrere Semaphoren mit unterschiedlichen Initialwert
* Activity mit Duration 0
* Mutex mehrere