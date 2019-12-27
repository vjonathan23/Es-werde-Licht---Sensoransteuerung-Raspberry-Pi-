# Import der benötigten Module
# Kommunikation mit dem Spektralsensor
from as7262 import AS7262

# Klasse wird zu "as7262" umbennant
as7262 = AS7262()

# Einstellungen des Sensors werden vorgenommen
as7262.set_gain(64)
as7262.set_integration_time(17.857)
as7262.set_measurement_mode(2)

# Versucht:
try:
    # Liest die Werte des Sensors
    values = as7262.get_calibrated_values()
    # Gibt für die einzelnen Wellenlängen Messwerte aus
    print("{} red {} orange {} yellow {} green {} blue {} violet".format(*values))
    # Zurücksetzung des Sensors
    as7262.set_measurement_mode(3)

# Falls die Messung abgebrochen wird:
except KeyboardInterrupt:
    # Zurücksetzung des Sensors
    as7262.set_measurement_mode(3)