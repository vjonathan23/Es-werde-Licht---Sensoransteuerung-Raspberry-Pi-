# Import der benötigten Module für 
# GUI, Ansteuerung der Kamera, Zeit etc.
from Kamerasteuerung import schiesseFoto, blinken # Kamera
from tkinter import *                             # GUI Ausgabe
from time import *                                # Zeitmessung
import _thread                                    # Parallele Ausführung
import os                                         # Betriebssystemszugriff

# Deklaration von globalen Variablen. 
# Alle Funktionen haben Zugriff.
einheiten = ["s","min","h","d"] # Zeiteinheiten (Stapel)
faktoren = [1,60,3600,86400]    # Sekunden für Zeiteinheiten
start = False                   # Boolean Variable für Programm "aktiv"
startZeit = 0                   # Zeitmessung: Startzeitpunkt
zeit = 0                        # Zeitmessung: Aktuelle Zeit

# Buttonreaktion: Funktion zur Auswahl des Arbeitsverzeichnisses
def Verzeichniswaehlen():  
    # Verzeichnisdialog starten             
    v = filedialog.askdirectory()       
    # Verzeichnis ins GUI Feld übertragen
    textVerzeichnis.delete(1.0,END)
    textVerzeichnis.insert(1.0,v+"/")

# Buttonreaktion:
# Funktion zur Kontrolle, ob ein Verzeichnis existiert.
# Inkl. Option zur direkten Erstellung eines Verzeichnisses.
def check():  
    # Verzeichnis aus GUI lesen                                            
    v = textVerzeichnis.get(1.0,END)[:-1]              
    # Existenzprüfung             
    if os.path.isdir(v):                                            
        messagebox.showinfo(message="Dieses Verzeichnis existiert") 
    else:            
        # Option zur Neuanlage des Verzeichnisses                                            
        if messagebox.askyesno(
                message="Dieses Verzeichnis existiert nicht. "
                +"Wollen sie dieses Verzeichnis erzeugen?"):
            # Verzeichnis erstellen
            os.makedirs(v)
        else:
            # Fehlermeldung ausgeben
            messagebox.showinfo(
                    message="Bitte ändern sie das Verzeichnis")
   
# Buttonreaktion: Start/Stop des Programms
def Start(): 
    # Schreibenden Zugriff auf globale Variablen ermöglichen                   
    global start, startZeit    
    if start == False:
        # "Start" wurde aktiviert, Startzeit festlegen
        startZeit = time()
        start = True
    else:
        # "Stop" wurde aktiviert
        start = False

# Buttonreaktion: Anpassung der Zeiteinheiten 
def Intervall():                       
    # Schreibenden Zugriff auf globale Variablen ermöglichen
    global einheiten,faktoren  
    # Aktuelle Einheit aus "Stapel" entfernen...
    ersteEinheit = einheiten.pop(0)
    ersterFaktor = faktoren.pop(0)
    # ... und hinten im "Stapel" wieder einfügen         
    einheiten.append(ersteEinheit)
    faktoren.append(ersterFaktor)
    # aktuelle Zeiteinheit ins GUI übertragen
    buttonIntervall.config(text=einheiten[0])

# Durchführung des periodischen Bilderschießens
# (Funktion wird als Thread parallel gestartet und bleibt dauerhaft
# aktiv im "Bildermodus" oder "Wartemodus")
def Bilder():
    # Schreibenden Zugriff auf globale Variable ermöglichen              
    global zeit                    
    # Lokale Variablen für Zeitmessung und Anzahl der Bilder
    letzteZeit = 0                  
    bildAnzahl = 0               
    # Hauptschleife für periodisches Bilderschießen
    while True:                     
        # Zeit als Integer in absoluten Sekunden
        zeitInt = int(zeit)    
        # Prüfung auf aktives Bilderschießen (Programm wartet dauerhaft)
        if start:   
            # Bildrschießen ist aktiv ("Bildermodus")               
            # Zeitfaktor (in Sekunden) zum aktuellen Zeitintervall
            faktor = faktoren[0]
            # Wert für Zeitintervall aus GUI lesen (z.B. 30 Sekunden)
            intervall = textIntervall.get(1.0,END)[:-1]
            # mit Sekundenfaktor multiplizieren (z.B. *60 für "min")
            intervall = float(intervall) * faktor
            # Verzeichnis aus GUI lesen
            verzeichnis = textVerzeichnis.get(1.0,END)[:-1]
            # Existenzprüfung zum Verzeichnis
            if os.path.isdir(verzeichnis):
                # Verzeichnis existiert
                # Prüfung Zeitschwellwert für nächstes Bild
                if zeitInt - letzteZeit >= intervall:
                    # LED-Ring an Kamera beginnt mit Warnblicken
                    blinken(int(intervall/10))
                    # Aktuelle Zeit wird gelesen für den Bildnamen
                    timedata = [str(localtime().tm_year),str(localtime().tm_mon),str(localtime().tm_mday),str(localtime().tm_hour),str(localtime().tm_min),str(localtime().tm_sec)]
                    # Zeitdaten werden in einen String gepackt
                    for c in range(len(timedata)):
                        if len(timedata[0]) < 2:
                            g = "0"+timedata[0]
                        else:
                            g = timedata[0]
                        del timedata[0]
                        timedata.append(g)
                    BildZeit = "".join(timedata)
                    # Neues Bild schießen
                    schiesseFoto(400,300,verzeichnis+"img_"+BildZeit+".png",verzeichnis)
                    # Letzte Zeit merken
                    letzteZeit = zeitInt + int(intervall/10)
                    # Datum der aktuellsten Messung an GUI zeigen
                    labelDatum.config(text=asctime())
                    # Letztes Bild lesen
                    letztesBild = PhotoImage(master=window,file=verzeichnis+"img_"+BildZeit+".png")
                    # Bild verkleinern
                    letztesBild = letztesBild.subsample(2)
                    # Bild auf GUI anzeigen
                    labelLetztesBild.config(image=letztesBild)
                    # Anzahl der Bilder erhöhen
                    bildAnzahl += 1
                    # Ausgabe Anzahl Bilder an GUI
                    labelAnzahlBilder.config(text="Anzahl der Bilder: "+str(bildAnzahl))
            else:
                # Fehlermeldung
                messagebox.showerror(message="Das Verzeichnis existiert nicht!")
        else:
            # Bilderschießen ist inaktiv ("Wartemodus")
            # Variablen und GUI Felder zurücksetzen
            bildAnzahl = 0
            letzteZeit = 0
            labelAnzahlBilder.config(text="Anzahl der Bilder: "+str(bildAnzahl))
        # Warten
        sleep(0.01)

# Funktion für Stopuhr
# (Funktion wird als Thread parallel gestartet und bleibt dauerhaft,
# um die Zeit zu überwachen)
def Zeitanpassung():                    
    # Schreibenden Zugriff auf globale Variable ermöglichen              
    global zeit                         
    # Hauptschleife für periodisches Bilderschießen
    while True:                         
        # Prüfung auf aktives Bilderschießen (Programm wartet dauerhaft)
        if start:   
            # Bilderschießen ist aktiv ("Bildermodus")    
            # Vergangene Zeit in Sekunden seit "Start" ermitteln
            zeit = time() - startZeit   
            # Korrekte Ausgabe der Zeit (Formatierung) an GUI:
            # Zeit auf ganze Zahl übertragen...
            zeitInt = int(zeit)      
            # ... und in korrekter Darstellung an GUI ausgeben
            if zeitInt < 60:            
                # Ausgabe im Sekundenbereich (kleiner als 1 Minuten)
                if zeitInt < 10:        
                    labelZeit.config(text="Zeit: 0:00:0"+str(zeitInt))
                else:
                    labelZeit.config(text="Zeit: 0:00:"+str(zeitInt))
            elif zeitInt < 3600:
                # Ausgabe im Minutenbereich (kleiner als 1 Stunde)
                zeitMinRest = zeitInt % 60
                zeitMin = (zeitInt - zeitMinRest) / 60
                zeitS = zeitMinRest
                zeitMin = int(zeitMin)
                zeitS = int(zeitS)
                if zeitS < 10 and zeitMin < 10:
                    labelZeit.config(
                        text="Zeit: 0:0"+str(zeitMin)+":0"+str(zeitS))
                elif zeitS < 10:
                    labelZeit.config(
                        text="Zeit: 0:"+str(zeitMin)+":0"+str(zeitS))
                elif zeitMin < 10:
                    labelZeit.config(
                        text="Zeit: 0:0"+str(zeitMin)+":"+str(zeitS))
                else:
                    labelZeit.config(
                        text="Zeit: 0:"+str(zeitMin)+":"+str(zeitS))
            else:
                # Ausgabe im Stundenbereich (größer gleich 1 Stunde)
                zeitHRest = zeitInt % 3600
                zeitH = (zeitInt - zeitHRest) / 3600
                zeitMinRest = zeitHRest % 60
                zeitMin = (zeitHRest - zeitMinRest) / 60
                zeitS =  zeitMinRest
                zeitH = int(zeitH)
                zeitMin = int(zeitMin)
                zeitS = int(zeitS)
                if zeitS < 10 and zeitMin < 10:
                    labelZeit.config(
                        text="Zeit: "
                        +str(zeitH)+":0"+str(zeitMin)+":0"+str(zeitS))
                elif zeitS < 10:
                    labelZeit.config(
                        text="Zeit: "
                        +str(zeitH)+":"+str(zeitMin)+":0"+str(zeitS))
                elif zeitMin < 10:
                    labelZeit.config(
                        text="Zeit: "
                        +str(zeitH)+":0"+str(zeitMin)+":"+str(zeitS))
                else:
                    labelZeit.config(
                        text="Zeit: "
                        +str(zeitH)+":"+str(zeitMin)+":"+str(zeitS))
        else:
            # Bilderschießen ist inaktiv ("Wartemodus")            
            zeit = 0
        # Warten
        sleep(0.01)

def Video():
    # FPS für Zeitraffer-Wiedergabe lesen
    fps = float(textFps.get(1.0,END)[:-1])
    # Verzeichnis der Bilder lesen
    verzeichnis = textVerzeichnis.get(1.0,END)[:-1]
    # Existenzprüfung
    if os.path.isdir(verzeichnis):
        # Ausgabe über "feh" mit Konsolenbefehl
        command = "feh -Y -x -q -D "+str(1/fps)+" -B black -F -Z -d "+verzeichnis+"*"
        os.system(command)
    else:
        # Fehlermeldung
        messagebox.showerror(message="Das Verzeichnis existiert nicht!")

# Hauptprgramm mit GUI Main-Loop
def Hauptprogramm():
    # Schreib-Zugriff auf globale GUI Variablen setzen
    global window
    global labelAnzahlBilder,buttonIntervall,labelZeit
    global letztesBild,labelLetztesBild,labelDatum
    
    # Hauptfenster erstellen
    window = Tk()
    # Fenstertitel festlegen
    window.title("Schüler experimentieren - Kameraansteuerung")    
    
    # GUI Felder erstellen und im Gitter anordnen:
    
    # Letztes Bild auf GUI
    letztesBild = None
    labelLetztesBild = Label(master=window,font=("Arial",14),
                             text="Keine Bilder")
    labelLetztesBild.grid(column=2,row=0,columnspan=10,rowspan=10)
    # Datum des letzten erstellten Bildes
    labelDatum = Label(master=window,font=("Arial",14))
    labelDatum.grid(column=2,row=10,columnspan=10)
    # Bezeichner für Verzeichnis
    labelVerzeichnis = Label(master=window,font=("Arial",14),
                             text="Verzeichnis")
    labelVerzeichnis.grid(column=0,row=1,sticky=W)
    # Bezeichner für Intervall
    labelIntervall = Label(master=window,font=("Arial",14),
                          text="Intervall")
    labelIntervall.grid(column=0,row=4,sticky=W)
    # Zeitausgabe mit Initialwert
    labelZeit = Label(master=window,font=("Arial",14),
                      text="Zeit: 0:00:00")
    labelZeit.grid(column=0,row=6,sticky=W)
    # Ausgabe der Anzahl der geschossenen Bilder mit Initialwert
    labelAnzahlBilder = Label(master=window,font=("Arial",14),
                              text="Anzahl der Bilder: 0")
    labelAnzahlBilder.grid(column=0,row=7,sticky=W)
    # Bezeichner für die FPS der Zeitraffer-Wiedergabe
    labelFps = Label(master=window,font=("Arial",14),
                     text="FPS")
    labelFps.grid(column=1,row=9,sticky=W)
    # Bezeichner für die Einstellungen für die Zeitraffer-Wiedergabe
    labelVideo = Label(master=window,font=("Arial",14),
                       text="Video-Optionen")
    labelVideo.grid(column=0,row=8,columnspan=2,sticky=W)
    # Button für Start/Stop mit Kommando
    buttonStartStop = Button(master=window,text="Start/Stop",width=22,
                             font=("Arial",14),command=Start)
    buttonStartStop.grid(column=0,row=0,columnspan=2,sticky=W)
    # Button für Zeitintervall-Zyklus mit Kommando
    buttonIntervall = Button(master=window,text="s",width=5,
                            font=("Arial",14),command=Intervall)
    buttonIntervall.grid(column=1,row=5,sticky=W)
    # Button für Ausgabe des Zeitraffer-Videos mit Kommando
    buttonVideo = Button(master=window,text="Video ansehen",width=22,
                         font=("Arial",14),command=Video)
    buttonVideo.grid(column=0,row=10,columnspan=2,sticky=W)
    # Button für Verzeichnisauswahl mit Kommando
    buttonVerzeichnis = Button(master=window,text="Wähle Verzeichnis",width=14,
                         font=("Arial",14),command=Verzeichniswaehlen)
    buttonVerzeichnis.grid(column=0,row=2,sticky=W)
    # Button für Existenzprüfung des Verzeichnisses mit Kommando
    buttonPruefeExistenz = Button(master=window,text="Prüfe",width=5,
                         font=("Arial",14),command=check)
    buttonPruefeExistenz.grid(column=1,row=2,sticky=W)
    # Eingabefeld für Verzeichniseingabe mit Startverzeichnis
    textVerzeichnis = Text(master=window,font=("Arial",14),
                           width=24,height=1)
    textVerzeichnis.grid(column=0,row=3,sticky=W,columnspan=2)
    textVerzeichnis.insert(END,"/home/pi/Jufo2020/")
    # Eingabefeld für Zeitintervall
    textIntervall = Text(master=window,font=("Arial",14),width=12,
                        height=1)
    textIntervall.grid(column=0,row=5,sticky=W)
    # Eingabefeld für FPS des Zeitraffer-Videos
    textFps = Text(master=window,font=("Arial",14),width=12,
                           height=1)
    textFps.grid(column=0,row=9,sticky=W)
    
    # Die beiden parallelen Abläufe starten:
    # ...Zeitüberwachung
    _thread.start_new_thread(Zeitanpassung,())
    # ...Bildererstellung
    _thread.start_new_thread(Bilder,())
    
    # Hauptschleife für GUI Fenster starten
    window.mainloop()
    
# Hauptprogramm starten    
Hauptprogramm()
