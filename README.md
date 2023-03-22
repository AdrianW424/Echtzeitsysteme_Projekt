# Echtzeitsysteme Projekt

## Aufgabenstellung
-> Entwicklung eines Programmes, welches ein Ablaufdiagramm aus einer CSV Datei einlesen und visualisieren kann.

## TODO:
HIGH-Priority:
* Frontend:
    * Abbrechen der Animation. Zum Beispiel mit Timer, dessen Intervall zurückgesetzt wird, sobald Button geklickt (statt sleep)
    * Angabe von der Dauer der GIF einbauen
    * InputChecker in Frontend integrieren (Fehlermeldungen, wenn falsche Daten eingegeben werden)
    * wenn mit CSV-Editor Falsches eingegeben wurde, dann lässt sich das Bild (obwohl nicht vorhanden) trotzdem downloaden und auch die Animationstasten funktionieren
* Backend:
    * Animationsalgorithmus entwickeln und implementieren - 95% fertig (genauere Tests durchführen)
        * Problem, dass Initialwert gesetzt wird, obwohl Semaphore im gleichen Schritt Wert von Activity zuvor bekommt - Semaphore müsste Wert schon zeitiger und nicht erst nach einem Takt der Leere bekommen
        * keine genauen Probleme bekannt. Zu testen siehe TOTEST unten
    * Activity mit Duration 0 -> refresh für andere Activities (Problem derzeit: 
        * Activity nach Activity mit duration 0 nicht sofort grün geschaltet - erst in nächstem Takt wird die Activity danach ausgeführt - braucht einen Takt, obwohl 0 Takte angegeben)
        * 88e544e - dataTest2.csv - Activity 2 mit Duration 0 wird übersprungen und Semaphore dahinter erst in nächstem Takt aktiviert
    ==> gemeinsamer fix: neuen Animationsalgorithmus entwickeln mit Animationshandler (Noch überlegen. Wichtig ist, dass auf die Priorität der Activities geachtet wird. Weiterhin auf die korrekte Ausführung der Activities mit Duration 0 sowie das Setzen von Initialwerten für Semaphoren)

MEDIUM-Priority:
* wow, such empty

LOW-Priority:
* Backend:
    * Programm verschönern - bessere Verteilung der Objekte

## TOTEST:
* Mehrere Semaphoren mit unterschiedlichen Initialwert
* Activity mit Duration 0
* Mutex mehrere
* Mutexs unterschiedlichen Tasks zugeordnet, nicht immer den beiden gleichen Activities