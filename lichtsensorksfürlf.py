# Import der benötigten Module
# Bertiebssystemsanwendung und Dateizugriff
import os, pickle

# Funktion zur Abspeicherung der Messdaten
def messe(verzeichnis):
    # Messwerte in eine temporäre Datei abspeichern
    befehl = "python lichtsensor.py > Messwerte_AktuellLS.txt"
    os.system(befehl)
    # Messwerte aus der Datei lesen
    with open('Messwerte_AktuellLS.txt') as f:
        data = f.readline()[:-1]
    # Falls eine Messwerte-Datei existiert:
    if os.path.exists(verzeichnis+"Messwerte.dat"):
        # Datei zum (binären) Lesen öffnen
        h = open(verzeichnis+"Messwerte.dat","rb")
        # Inhalt lesen
        messwerte = pickle.load(h)
        # Datei schließen
        h.close()
        # Bisherigen Messwerte ergänzen
        messwerte.append(data)
        messwerteneu = messwerte[:]
        # Datei zum (binären) Schreiben öffnen
        g = open(verzeichnis+"Messwerte.dat","wb")
        # Datei mit den Messwerten überschreiben
        pickle.dump(messwerteneu,g)
        # Datei schließen
        g.close()
    # Andernfalls:
    else:
        # Neue Messwert-Liste erstellen
        messwerteneu = []
        # Durch den Messwert ergänzen
        messwerteneu.append(data)
        #  Messwerte-Datei zum (binären) Schreiben öffnen/erstellen
        g = open(verzeichnis+"Messwerte.dat","wb")
        # Messwert auf die Datei übertragen
        pickle.dump(messwerteneu,g)
        # Datei schließen
        g.close()