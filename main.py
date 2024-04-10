## cc maximilian scheinast-peter 
## bugreport mscheinastpeter@gmai.com
## last update 05.04.2024
## dieses programm funktioniert ähnlich wie ein digitales Oszi zur Darstellung von Vitalkurven


## thank me later peak to peak = mind80% of previous peak
##
#################################################################

## Autoanalyse Herz
##Analyse Einzelner Schläge canvas 1 
#    P-Welle: Ausbreitung der Erregung in den Vorhöfen (atriale Erregungsausbreitung).
#    PQ-Intervall: Überleitung der Erregung von den Vorhöfen auf die Kammern. Es spiegelt die Zeit wider, die der vom Sinusknoten gebildete elektrische Impuls benötigt, um über den Vorhof, den AV-Knoten und das His-Bündel zu den Kammern zu gelangen. Im EKG erfolgt die Messung vom Beginn der P-Welle, bis zum Beginn der Q-Zacke.
#    QRS-Komplex: Erregungsausbreitung in den Kammern (ventrikuläre Erregungsausbreitung). Er besteht normalerweise aus einer negativen Q-Zacke, einer positiven hohen R-Zacke, einer kleinen negativen S-Zacke.
#    ST-Strecke: Während der Dauer der ST-Strecke sind beide Kammern vollständig erregt. Das Ende der ST-Strecke ist der Beginn der Erregungsrückbildung.
#    T-Welle: Erregungsrückbildung in den Kammern (intraventrikuläre Erregungsrückbildung).
#    QT-Intervall: Zeitraum vom Beginn der Erregungsausbreitung in den Kammern (QRS-Komplex) bis zum Ende der Erregungsrückbildung (T-Welle).
################################################################
##Analyse Rythmus canvas 2
# durschnitt geschwindigkeit 1/10/100/1000
# auf rythmusstörung
## Autoanalyse 
import tkinter as tk
from tkinter import ttk  # Für Combobox
import time
import math

# Beispielfunktion zur Generierung von EKG-Daten (ersetzen Sie dies durch Ihre tatsächliche Funktion)
def get_ekg_data1():
    # Hier Ihre Funktion einfügen, die EKG-Daten mit Zeitstempel liefert
    timestamp = time.time()
    value = 50 + 40 * math.sin(timestamp)  # Beispiel-Sinuswelle
    return timestamp, value

def get_ekg_data():
    import serial
    import time

    # Configure serial port (adjust port name as needed)
    ser = serial.Serial('COM10', 9600)

    # Wait for the serial connection to establish
    ser.timeout = 2

    #ser.write(b'testcom.py\n')  # Send command to start the script
    while True:
        # Read data from serial port
        data = ser.readline().decode().strip()

        # Check if data is not empty
        print(data)
        if data:
            try:
                # Attempt to convert data to float
                value = float(data)
                timestamp = time.time()
                return timestamp, value
            except ValueError:
                print("Invalid data format:", data)
        else:
            print("Empty data received")
        
        # Add a small delay to prevent rapid looping
        time.sleep(0.00001)

    
# Konstanten
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 300

class EKGApp:
    def __init__(self, master):
        self.master = master
        master.title("EKG-Visualisierung")

        # Hauptframe für obere Elemente
        main_frame = tk.Frame(master)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas für einzelne Schwingung (Triggerperiode)
        self.single_canvas = tk.Canvas(main_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
        self.single_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Canvas für Laufband-Ansicht
        self.multi_canvas = tk.Canvas(main_frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
        self.multi_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Frame für Eingabeelemente
        input_frame = tk.Frame(main_frame)
        input_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Datenstrukturen
        self.single_data = []
        self.multi_data = []

        # Zeitstempel des Starts
        self.start_time = time.time()

        # Trigger-Variablen
        self.trigger_level = 50  # Standardmäßig 50%
        self.trigger_armed = False
        self.trigger_paused = False
        self.trigger_timestamp = None
        self.last_trigger_timestamp = None
        self.last_value = 0
        self.trigger_count = 0
        self.trigger_skip = 0
        self.cooldown_time = 0  # Variable für Cooldown-Zeit
        self.cooldown_active = False  # Flag für aktiven Cooldown

        # Eingabefeld für Trigger-Level
        self.trigger_label = tk.Label(input_frame, text="Trigger-Level:")
        self.trigger_label.pack()
        self.trigger_entry = tk.Entry(input_frame, width=10)
        self.trigger_entry.pack()
        self.trigger_entry.insert(0, str(self.trigger_level))

        # Combobox für Flankenauswahl
        self.flank_label = tk.Label(input_frame, text="Flanke:")
        self.flank_label.pack()
        self.flank_options = ["Steigende Flanke", "Fallende Flanke"]
        self.flank_var = tk.StringVar(value=self.flank_options[0])
        self.flank_combobox = ttk.Combobox(input_frame, textvariable=self.flank_var, values=self.flank_options, width=15)
        self.flank_combobox.pack()

        # Eingabefeld und Button für Cooldown
        self.cooldown_label = tk.Label(input_frame, text="Cooldown (Sekunden):")
        self.cooldown_label.pack()
        self.cooldown_entry = tk.Entry(input_frame, width=10)
        self.cooldown_entry.pack()
        self.cooldown_entry.insert(0, "0")  # Standardmäßig kein Cooldown
        self.set_cooldown_button = tk.Button(input_frame, text="Cooldown setzen", command=self.set_cooldown)
        self.set_cooldown_button.pack()

        # Button zum Starten/Stoppen des Triggers
        self.trigger_button = tk.Button(input_frame, text="Trigger starten", command=self.toggle_trigger)
        self.trigger_button.pack()

        # Button zum Pausieren/Fortsetzen des Triggers
        self.pause_button = tk.Button(input_frame, text="Trigger pausieren", command=self.pause_trigger, state=tk.DISABLED)
        self.pause_button.pack()

        # Eingabefeld und Button für Laufbanddauer
        self.duration_label = tk.Label(input_frame, text="Laufbanddauer (Sekunden):")
        self.duration_label.pack()
        self.duration_entry = tk.Entry(input_frame, width=10)
        self.duration_entry.pack()
        self.duration_entry.insert(0, "30")  # Standardmäßig 30 Sekunden
        self.set_duration_button = tk.Button(input_frame, text="Dauer setzen", command=self.set_duration)
        self.set_duration_button.pack()

        # Laufbanddauer initialisieren
        self.multi_sweep_duration = 30  # Initialwert

        # Sekundärer Frame für zusätzliche Inhalte
        secondary_frame = tk.Frame(master)
        secondary_frame.pack(fill=tk.BOTH, expand=True)

        # Beispiel-Label im sekundären Frame (ersetzen Sie dies durch Ihre Inhalte)
        secondary_label = tk.Label(secondary_frame, text="Restewidget später")
        secondary_label.pack()

        # Aktualisierungsfunktion periodisch aufrufen
        self.update_data()

        # Größenänderung per Maus
        self.single_canvas.bind("<Configure>", self.on_resize)
        self.multi_canvas.bind("<Configure>", self.on_resize)

    def set_cooldown(self):
        try:
            self.cooldown_time = float(self.cooldown_entry.get())
        except ValueError:
            pass  # Ungültige Eingabe ignorieren

    def set_duration(self):
        try:
            self.multi_sweep_duration = float(self.duration_entry.get())
        except ValueError:
            pass  # Ungültige Eingabe ignorieren

    def toggle_trigger(self):
        if self.trigger_armed:
            self.trigger_armed = False
            self.trigger_button.config(text="Trigger starten")
            self.pause_button.config(state=tk.DISABLED)
            self.single_data = []
            self.draw_single_canvas()
        else:
            try:
                self.trigger_level = float(self.trigger_entry.get())
            except ValueError:
                pass
            self.trigger_armed = True
            self.trigger_button.config(text="Trigger stoppen")
            self.pause_button.config(state=tk.NORMAL)
            self.trigger_count = 0

    def pause_trigger(self):
        self.trigger_paused = not self.trigger_paused
        if self.trigger_paused:
            self.pause_button.config(text="Trigger fortsetzen")
        else:
            self.pause_button.config(text="Trigger pausieren")

    def update_data(self):
        # EKG-Daten abrufen
        timestamp, value = get_ekg_data()

        # Daten für Laufband-Ansicht aktualisieren
        self.multi_data.append((timestamp, value))
        if timestamp - self.multi_data[0][0] > self.multi_sweep_duration:
            self.multi_data.pop(0)  # Ältesten Punkt entfernen

        # Trigger-Logik (nur wenn nicht pausiert und kein Cooldown aktiv)
        if self.trigger_armed and not self.trigger_paused and not self.cooldown_active:
            if self.flank_var.get() == "Steigende Flanke":
                condition = value >= self.trigger_level and self.last_value < self.trigger_level
            else:  # Fallende Flanke
                condition = value <= self.trigger_level and self.last_value > self.trigger_level
            if condition:
                self.last_trigger_timestamp = timestamp
                self.single_data = []  # Daten für einzelne Schwingung zurücksetzen
                self.trigger_count = 0  # Zähler zurücksetzen
                if self.cooldown_time > 0:
                    self.cooldown_active = True
                    self.master.after(int(self.cooldown_time * 1000), self.end_cooldown)  # Cooldown starten

        # Daten für einzelne Schwingung aktualisieren (von letztem Trigger bis jetzt)
        if self.last_trigger_timestamp is not None and self.trigger_armed and not self.trigger_paused:
            self.single_data.append((timestamp, value))

        # Canvas neu zeichnen
        self.draw_single_canvas()
        self.draw_multi_canvas()

        # Letzten Wert speichern
        self.last_value = value

        # Trigger-Zähler erhöhen, wenn Trigger aktiv und nicht pausiert ist
        if self.trigger_armed and not self.trigger_paused:
            self.trigger_count += 1

        # Erneut aufrufen nach 1 ms
        self.master.after(1, self.update_data)

    def end_cooldown(self):
        self.cooldown_active = False

    def draw_single_canvas(self):
        self.single_canvas.delete("all")  # Canvas löschen

        if not self.single_data or self.last_trigger_timestamp is None:
            return  # Nichts zu zeichnen

        # Datenpunkte zeichnen (von letztem Trigger bis jetzt)
        last_x, last_y = None, None
        for timestamp, value in self.single_data:
            x = (timestamp - self.last_trigger_timestamp) * self.single_canvas.winfo_width() / self.multi_sweep_duration 
            y = self.single_canvas.winfo_height() - (value * self.single_canvas.winfo_height() / 100)
            if last_x is not None:
                self.single_canvas.create_line(last_x, last_y, x, y, fill="blue")
            last_x, last_y = x, y

    def draw_multi_canvas(self):
        self.multi_canvas.delete("all")  # Canvas löschen

        if not self.multi_data:
            return  # Nichts zu zeichnen

        # Skalierung berechnen (Fehlerbehebung für Division durch Null)
        duration = max(self.multi_data[-1][0] - self.multi_data[0][0], 0.001)  # Kleine Zahl hinzufügen, um Division durch Null zu vermeiden
        x_scale = self.multi_canvas.winfo_width() / duration
        y_scale = self.multi_canvas.winfo_height() / 100

        # Datenpunkte zeichnen
        last_x, last_y = None, None
        for timestamp, value in self.multi_data:
            x = (timestamp - self.multi_data[0][0]) * x_scale
            y = self.multi_canvas.winfo_height() - (value * y_scale)
            if last_x is not None:
                self.multi_canvas.create_line(last_x, last_y, x, y, fill="blue")
            last_x, last_y = x, y

        # Zeitachse zeichnen
        self.draw_time_axis(self.multi_canvas, self.multi_data[0][0], duration)

        # Trigger zeichnen
        trigger_y = self.multi_canvas.winfo_height() - (self.trigger_level * y_scale)
        self.multi_canvas.create_line(self.multi_canvas.winfo_width() - 10, trigger_y, self.multi_canvas.winfo_width(), trigger_y + 5, fill="red")
        self.multi_canvas.create_line(self.multi_canvas.winfo_width() - 10, trigger_y, self.multi_canvas.winfo_width(), trigger_y - 5, fill="red")

    def draw_time_axis(self, canvas, start_time, duration):
        # Markierungen und Beschriftungen für jede Sekunde
        for i in range(int(duration) + 1):
            x = i * canvas.winfo_width() / duration
            canvas.create_line(x, 0, x, canvas.winfo_height(), fill="gray", dash=(2, 2))
            canvas.create_text(x, canvas.winfo_height() - 10, text=f"{i:.1f}s", anchor=tk.N)

    def on_resize(self, event):
        # Canvas neu zeichnen, wenn die Größe geändert wird
        self.draw_single_canvas()
        self.draw_multi_canvas()

# Hauptanwendung starten
root = tk.Tk()
app = EKGApp(root)
root.mainloop()