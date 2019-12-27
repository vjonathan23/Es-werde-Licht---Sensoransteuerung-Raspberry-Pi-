# Import der benötigten Module
# Bertiebssystemsanwendung, Zeit und GPIO-Verknüpfung
import os
from RPi import GPIO
from time import sleep
# GPIO-Einstellungen
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
# Festlegung des verwendeten Ausgangs-Pin für LED-Ring
GPIO.setup(12, GPIO.OUT)
# Zurücksetztung des Pins
GPIO.output(12, False)

# Funktion fürs Warnblinken
def blinken(zeit):
    # Dauer des Blinkens wird übertragen
    t = zeit
    # Schleife endet, wenn t vergangen ist
    while not t <= 0:
        # LED-Ring wird eingeschaltet
        GPIO.output(12, True)
        # Warten
        sleep(0.5)
        # LED-Ring wird ausgeschaltet
        GPIO.output(12, False)
        # Warten
        sleep(0.5)
        # t verkleinern um 1 s
        t -= 1

# Funktion für das Schießen eines Bildes
def schiesseFoto(breite,hoehe,bildname,verzeichnis):
    # LED-Ring wird eingeschaltet
    GPIO.output(12, True)
    # Bild wird erstellt mit Konsolenbefehl
    befehl = "raspistill -w %i -h %i -e png -t 300 -o %s -n" % (breite,hoehe,bildname)
    os.system(befehl)
    # Warten
    sleep(0.5)
    # LED-Ring wird ausgeschaltet
    GPIO.output(12, False)