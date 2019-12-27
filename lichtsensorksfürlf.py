# Import der ben�tigten Module
# Bertiebssystemsanwendung und Dateizugriff
import os, pickle

# Funktion zur Abspeicherung der Messdaten
def messe(verzeichnis):
    # Messwerte in eine tempor�re Datei abspeichern
    befehl = "python lichtsensor.py > Messwerte_AktuellLS.txt"
    os.system(befehl)
    # Messwerte aus der Datei lesen
    with open('Messwerte_AktuellLS.txt') as f:
        data = f.readline()[:-1]
    # Falls eine Messwerte-Datei existiert:
    if os.path.exists(verzeichnis+"Messwerte.dat"):
        # Datei zum (bin�ren) Lesen �ffnen
        h = open(verzeichnis+"Messwerte.dat","rb")
        # Inhalt lesen
        messwerte = pickle.load(h)
        # Datei schlie�en
        h.close()
        # Bisherigen Messwerte erg�nzen
        messwerte.append(data)
        messwerteneu = messwerte[:]
        # Datei zum (bin�ren) Schreiben �ffnen
        g = open(verzeichnis+"Messwerte.dat","wb")
        # Datei mit den Messwerten �berschreiben
        pickle.dump(messwerteneu,g)
        # Datei schlie�en
        g.close()
    # Andernfalls:
    else:
        # Neue Messwert-Liste erstellen
        messwerteneu = []
        # Durch den Messwert erg�nzen
        messwerteneu.append(data)
        #  Messwerte-Datei zum (bin�ren) Schreiben �ffnen/erstellen
        g = open(verzeichnis+"Messwerte.dat","wb")
        # Messwert auf die Datei �bertragen
        pickle.dump(messwerteneu,g)
        # Datei schlie�en
        g.close()