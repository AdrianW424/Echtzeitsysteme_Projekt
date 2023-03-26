# Echtzeitsysteme Projekt

## Aufgabenstellung
-> Entwicklung eines Programmes, welches ein Ablaufdiagramm aus einer CSV Datei einlesen und visualisieren kann.

## TODO:
HIGH-Priority:
* Frontend:
    * Angabe von der Dauer der GIF einbauen
    * InputChecker in Frontend integrieren (Fehlermeldungen, wenn falsche Daten eingegeben werden)
    * wenn mit CSV-Editor Falsches eingegeben wurde, dann lässt sich das Bild (obwohl nicht vorhanden) trotzdem downloaden und auch die Animationstasten funktionieren
* Backend:
    * Animationsalgorithmus entwickeln und implementieren - 95% fertig (genauere Tests durchführen)
        * keine genauen Probleme bekannt. Zu testen siehe TOTEST unten

MEDIUM-Priority:
* wow, such empty

LOW-Priority:
* wow, such empty

## TOTEST:
* Mehrere Semaphoren mit unterschiedlichen Initialwert                                      - passed
* Activity mit Duration 0                                                                   - passed
* Mutex mehrere                                                                             - passed
* Mutexs unterschiedlichen Tasks zugeordnet, nicht immer den beiden gleichen Activities     - passed