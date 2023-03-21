# Echtzeitsysteme Projekt

## Aufgabenstellung
-> Entwicklung eines Programmes, welches ein Ablaufdiagramm aus einer CSV Datei einlesen und visualisieren kann.

## TODO:
HIGH-Priority:
* Frontend:
    * mehrfaches Laden von Dateien in CSV-Editor hängt neuen Inhalt an den alten an - Lösung: beim Laden neuer Datei wird der alte Inhalt gelöscht
    * CSV-Editor bleibt groß - passt sich nicht an die Menge an Text an nach Löschen
    * Image-Download erst möglich, wenn überhaupt Datei vorhanden ist
    * Autoplay lässt sich auch abspielen, wenn kein Bild geladen wurde
    * Abbrechen der Animation. Zum Beispiel mit Timer, dessen Intervall zurückgesetzt wird, sobald Button geklickt (statt sleep)
    * Hover-Effekte bei Darkmode weg
    * InputChecker in Frontend integrieren (Fehlermeldungen, wenn falsche Daten eingegeben werden)
* Backend:
    * Animationsalgorithmus entwickeln und implementieren - 95% fertig (genauere Tests durchführen)
        * Problem, dass Initialwert gesetzt wird, obwohl Semaphore im gleichen Schritt Wert von Activity zuvor bekommt
        * keine genauen Probleme bekannt. Zu testen siehe TOTEST unten
    * Activity mit Duration 0 -> refresh für andere Activities (Problem derzeit: 
        * Activity nach Activity mit duration 0 nicht sofort grün geschaltet - erst in nächstem Takt wird die Activity danach ausgeführt - braucht einen Takt, obwohl 0 Takte angegeben)
        * 88e544e - dataTest2.csv - Activity 2 mit Duration 0 wird übersprungen und Semaphore dahinter erst in nächstem Takt aktiviert
    * GIF Problem mit Bildergröße. Wenn Initialisierung von Semaphore verschwindet, wird Bild kleiner. Teil des GIFs ändert sich nicht

MEDIUM-Priority:
* wow, such empty

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