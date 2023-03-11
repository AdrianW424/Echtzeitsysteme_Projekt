# Echtzeitsysteme Projekt

## Aufgabenstellung
-> Entwicklung eines Programmes, welches ein Ablaufdiagramm aus einer CSV Datei einlesen und visualisieren kann.

## TODO:
HIGH-Priority:
* Frontend: 
    * in Mitte wird jpg oder so dargestellt
    * User Interface mit Buttons (Datei laden, Animation beginnen (Animation weitergehen, Animation zurückgehen, Animation/Bild speichern))
    * Datei (CSV) muss irgendwie geladen werden können
* Animationsalgorithmus entwickeln und implementieren - 50% fertig (genauere Tests durchführen, Mutex einbauen)
* Aktivitätsdauer noch ungleichmäßig (Aktivität mit Semaphore mit Initialwert um einen Takt schneller fertig, als bei anderen Aktivitäten)

MEDIUM-Priority:
* Programm zur Erstellung von jpg-Bildern (oder so) aus den Arrays sowie verketteten Objekten verschönern
* aktive Semaphoren werden rot dargestellt, wie bei ODER?
* Semaphoren mit ODER haben immer ausgefüllten Pfeilkopf (auch wenn zwischen zwei Tasks) - ihn nochmal fragen

LOW-Priority:
* Programm unabhängig gegenüber falschen Eingaben in CSV-Datei machen