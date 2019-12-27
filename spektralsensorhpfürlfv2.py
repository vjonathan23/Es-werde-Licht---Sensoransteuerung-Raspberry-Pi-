# Import der benötigten Module für 
# GUI, Dateizugriff und Diagrammausgabe, etc.
from spektralsensornp import messe # Spektralsensor
from tkinter import *              # GUI Ausgabe
from time import *                 # Zeitmessung
import _thread                     # Parallele Ausführung
import os, pickle                  # Dateizugriff
import matplotlib.pyplot as plt    # Diagrammausgabe

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

# Durchführung der periodischen Messungen
# (Funktion wird als Thread parallel gestartet und bleibt dauerhaft
# aktiv im "Messmodus" oder "Wartemodus")
def Messung():        
    # Schreibenden Zugriff auf globale Variable ermöglichen              
    global zeit                    
    # Lokale Variablen für Zeitmessung und Anzahl der Messungen
    letzteZeit = 0                  
    messungAnzahl = 0               
    # Hauptschleife für periodische Messungen
    while True:                     
        # Zeit als Integer in absoluten Sekunden
        zeitInt = int(zeit)    
        # Prüfung auf aktive Messung (Programm wartet dauerhaft)
        if start:   
            # Messung ist aktiv ("Messmodus")               
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
                # Prüfung Zeitschwellwert für nächste Messung
                if zeitInt - letzteZeit >= intervall:
                    # Neue Messung erstellen
                    messe(verzeichnis)
                    # letzte Zeit merken
                    letzteZeit = zeitInt
                    # Datum der aktuellsten Messung an GUI zeigen
                    labelDatum.config(text=str(asctime()))
                    # Anzahl der Messungen erhöhen
                    messungAnzahl += 1
                    # Ausgabe Anzahl Messungen an GUI
                    labelAnzahlMessungen.config(
                            text="Anzahl der Messungen: "
                            +str(messungAnzahl))
            else:
                # Fehlermeldung
                messagebox.showerror(
                        message="Das Verzeichnis existiert nicht!")
        else:
            # Messung ist inaktiv ("Wartemodus")
            # Variablen und GUI Felder zurücksetzen
            messungAnzahl = 0
            letzteZeit = 0
            labelAnzahlMessungen.config(
                    text="Anzahl der Messungen: "
                    +str(messungAnzahl))   
        # Warten
        sleep(0.01)

# Funktion für Stopuhr
# (Funktion wird als Thread parallel gestartet und bleibt dauerhaft,
# um die Zeit zu überwachen)
def Zeitanpassung():                    
    # Schreibenden Zugriff auf globale Variable ermöglichen              
    global zeit                         
    # Hauptschleife für periodische Messungen
    while True:                         
        # Prüfung auf aktive Messung (Programm wartet dauerhaft)
        if start:   
            # Messung ist aktiv ("Messmodus")    
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
            # Messung ist inaktiv ("Wartemodus")            
            zeit = 0
        # Warten
        sleep(0.01)

# Buttonreaktion: Funktion zur Erstellung eines Messwertdiagramms
def Messwerte():  
    # Aktuelle Zeiteinheit lesen                                      
    einheit = einheiten[0]      
    # Aktuelles Zeitintervall von GUI lesen                        
    intervall = int(textIntervall.get(1.0,END)[:-1])    
    # Verzeichnis aus GUI lesen
    verzeichnis = textVerzeichnis.get(1.0,END)[:-1]  
    # Existenz der Messdatei im Verzeichnis prüfen
    if os.path.exists(verzeichnis+"Messwerte.dat"):    
        # Datei zum (binären) Lesen öffnen
        h = open(verzeichnis+"Messwerte.dat","rb")      
        # Datei über "pickle" in eine Liste laden
        messwerte = pickle.load(h)   
        # Datei schließen                   
        h.close()        
        # Liste für Koordinaten des Diagramms                               
        x = []
        yred = []
        yorange = []
        yyellow = []
        ygreen = []
        yblue = []
        yviolet = []
        # Aufspaltung der Messwertrohdaten in sechs Messwerte
        for g in messwerte:
            h = g
            h = h.split(' red ')
            messwerteneu.append(float(h[0]))
            del h[0]
            h = h[0]
            h = h.split(' orange ')
            messwerteneu.append(float(h[0]))
            del h[0]
            h = h[0]
            h = h.split(' yellow ')
            messwerteneu.append(float(h[0]))
            del h[0]
            h = h[0]
            h = h.split(' green ')
            messwerteneu.append(float(h[0]))
            del h[0]
            h = h[0]
            h = h.split(' blue ')
            messwerteneu.append(float(h[0]))
            del h[0]
            h = h[0]
            h = h.split(' violet')
            messwerteneu.append(float(h[0]))
            del h[0]
            h = h[0]                               
        # Koordiatensystem aus Messwerten aufbauen           
        for i in range(1,len(messwerte)+1):       
            # Zeiteinheiten auf x-Achse
            x.append(i*intervall)       
        w = 6
        # Messwerte auf y-Achse für sechs verschiedene Wellenlängen
        for i in messwerteneu:
            if w % 6 == 0:
                yred.append(i)
            elif w % 6 == 1:
                yorange.append(i)
            elif w % 6 == 2:
                yyellow.append(i)
            elif w % 6 == 3:
                ygreen.append(i)
            elif w % 6 == 4:
                yblue.append(i)
            elif w % 6 == 5:
                yviolet.append(i)
            w += 1
        # Plot erstellen (mit Beschriftung der Messreihe)                     
        fig,p = plt.subplots(1, 1,num='Spektralmessung')
        # Plot formatieren
        # (o=kleine Punkte, -=Punkte verbinden)
        p.plot(x,yred,'ro-') # r=rot
        p.plot(x,yorange,'o-',color='tab:orange') # orange
        p.plot(x,yyellow,'yo-') # y=gelb
        p.plot(x,ygreen,'go-') # g=grün
        p.plot(x,yblue,'bo-') # b=blau
        p.plot(x,yviolet,'mo-') # m=magenta
        # Beschriftung des Diagramms (Titel und Achsen)
        p.set_title('Wellenlängen (650nm;600nm;570nm;550nm;500nm;450nm)')
        p.set_ylabel('Relative Einheit')
        p.set_xlabel('Zeit ('+einheit+')')
        # Format: Größe und Abstände zum Rand festlegen
        plt.tight_layout(pad=0.4,w_pad=0.5,h_pad=1.0)
        # Ausgabe des Diagramms
        plt.show()
    else:
        # Fehlermeldung
        messagebox.showerror(
                message="Die Messwerte.dat-Datei existiert nicht!")

# Hauptprgramm mit GUI Main-Loop
def Hauptprogramm():
    # Schreib-Zugriff auf globale GUI Variablen setzen
    global window
    global labelAnzahlMessungen,labelZeit,labelDatum
    global textIntervall
    global buttonIntervall
    
    # Hauptfenster erstellen
    window = Tk()
    # Fenstertitel festlegen
    window.title("Schüler experimentieren - Spektralsensormessung")    
    
    # GUI Felder erstellen und im Gitter anordnen:
    
    # Datum der letzten Messung:
    labelDatum = Label(master=window,font=("Arial",14))             
    labelDatum.grid(column=0,row=9,columnspan=2,sticky=W)          
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
    # Ausgabe der Anzahl der durchgeführten Messungen mit Initialwert
    labelAnzahlMessungen = Label(master=window,font=("Arial",14),   
                              text="Anzahl der Messungen: 0")       
    labelAnzahlMessungen.grid(column=0,row=7,sticky=W)              
    # Button für Start/Stop mit Kommando
    buttonStartStop = Button(master=window,
                             text="Start / Stop",width=22,
                             font=("Arial",14),command=Start)
    buttonStartStop.grid(column=0,row=0,columnspan=2,sticky=W)
    # Button für Zeitintervall-Zyklus mit Kommando
    buttonIntervall = Button(master=window,text="s",width=5,
                            font=("Arial",14),command=Intervall)
    buttonIntervall.grid(column=1,row=5,sticky=W)
    # Button für Verzeichnisauswahl mit Kommando
    buttonVerzeichnis = Button(master=window,
                               text="Wähle Verzeichnis",width=14,
                         font=("Arial",14),
                         command=Verzeichniswaehlen)
    buttonVerzeichnis.grid(column=0,row=2,sticky=W)
    # Button für Existenzprüfung des Verzeichnisses mit Kommando
    buttonPruefeExistenz = Button(master=window,text="Prüfe",
                                  width=5,font=("Arial",14),
                                  command=check)
    buttonPruefeExistenz.grid(column=1,row=2,sticky=W)
    # Button für Diagrammausgabe mit Kommando
    buttonMesstabelle = Button(master=window,
                               text="Erstelle Messwertdiagramm",
                               width=22,font=("arial",14),
                               command=Messwerte)
    buttonMesstabelle.grid(column=0,row=8,columnspan=2,sticky=W)
    # Eingabefeld für Verzeichniseingabe mit Startverzeichnis
    textVerzeichnis = Text(master=window,font=("Arial",14),
                           width=24,height=1)
    textVerzeichnis.grid(column=0,row=3,sticky=W,columnspan=2)
    textVerzeichnis.insert(END,"/home/pi/Jufo2020/")
    # Eingabefeld für Zeitintervall
    textIntervall = Text(master=window,font=("Arial",14),width=12,
                        height=1)
    textIntervall.grid(column=0,row=5,sticky=W)
    
    # Die beiden parallelen Abläufe starten:
    # ...Zeitüberwachung
    _thread.start_new_thread(Zeitanpassung,())
    # ...Messwerterstellung
    _thread.start_new_thread(Messung,())
    
    # Hauptschleife für GUI Fenster starten
    window.mainloop()
    
# Hauptprogramm starten    
Hauptprogramm()