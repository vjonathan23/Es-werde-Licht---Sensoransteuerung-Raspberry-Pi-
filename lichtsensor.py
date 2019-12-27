# Import der benötigten Module
# Ansteurung über i2c
import smbus

# Nummer des Geräts wird festgelegt
DEVICE = 0x23

# Nummer eines gewissen Modus wird für den Sensor
# festgelegt, um auch mit geringen Lichtmengen zu messen
CONTINOUS_HIGH_RES_MODE_2 = 0x11

# Nummer des verwendeten i2c-Bus wird angegeben
bus = smbus.SMBus(1)

# Funktion zur Konvertierungen der Rohdaten in Dezimalwerte in Lux
def convertToNumber(data):
    return ((data[1] + (256 * data[0])) / 1.2)

# Funktion zum Lesen des Sensors per Langzeitmessung
def readLight(addr=DEVICE):
    data = bus.read_i2c_block_data(addr, CONTINOUS_HIGH_RES_MODE_2)
    return convertToNumber(data)

# Ausgabe des aktuellen Messwerts
print(str(readLight()))