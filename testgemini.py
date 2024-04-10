import tkinter as tk
import time
import math

# Beispielfunktion zur Generierung von EKG-Daten (ersetzen Sie dies durch Ihre tatsächliche Funktion)
def get_ekg_data():
    # Hier Ihre Funktion einfügen, die EKG-Daten mit Zeitstempel liefert
    timestamp = time.time()
    value = 50 + 40 * math.sin(timestamp)  # Beispiel-Sinuswelle
    return timestamp, value

# Konstanten
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 200
SINGLE_SWEEP_DURATION = 1  # Dauer einer einzelnen Schwingung in Sekunden
MULTI_SWEEP_DURATION = 30  # Dauer des Laufbands in Sekunden

class EKGApp:
    def __init__(self, master):
        self.master = master
        master.title("EKG-Visualisierung")

        # Canvas für einzelne Schwingung
        self.single_canvas = tk.Canvas(master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
        self.single_canvas.pack(side=tk.LEFT)

        # Canvas für Laufband-Ansicht
        self.multi_canvas = tk.Canvas(master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
        self.multi_canvas.pack(side=tk.RIGHT)

        # Datenstrukturen
        self.single_data = []
        self.multi_data = []

        # Zeitstempel des Starts
        self.start_time = time.time()

        # Aktualisierungsfunktion periodisch aufrufen
        self.update_data()

    def update_data(self):
        # EKG-Daten abrufen
        timestamp, value = get_ekg_data()

        # Daten für einzelne Schwingung aktualisieren
        self.single_data.append((timestamp, value))
        if timestamp - self.single_data[0][0] > SINGLE_SWEEP_DURATION:
            self.single_data = []  # Zurücksetzen, wenn die Dauer überschritten wird

        # Daten für Laufband-Ansicht aktualisieren
        self.multi_data.append((timestamp, value))
        if timestamp - self.multi_data[0][0] > MULTI_SWEEP_DURATION:
            self.multi_data.pop(0)  # Ältesten Punkt entfernen

        # Canvas neu zeichnen
        self.draw_single_canvas()
        self.draw_multi_canvas()

        # Erneut aufrufen nach 1 ms
        self.master.after(1, self.update_data)

    def draw_single_canvas(self):
        self.single_canvas.delete("all")  # Canvas löschen

        if not self.single_data:
            return  # Nichts zu zeichnen

        # Skalierung berechnen
        x_scale = CANVAS_WIDTH / SINGLE_SWEEP_DURATION
        y_scale = CANVAS_HEIGHT / 100

        # Datenpunkte zeichnen
        last_x, last_y = None, None
        for timestamp, value in self.single_data:
            x = (timestamp - self.single_data[0][0]) * x_scale
            y = CANVAS_HEIGHT - (value * y_scale)
            if last_x is not None:
                self.single_canvas.create_line(last_x, last_y, x, y, fill="blue")
            last_x, last_y = x, y

        # Zeitachse zeichnen
        self.draw_time_axis(self.single_canvas, self.single_data[0][0], SINGLE_SWEEP_DURATION)

    def draw_multi_canvas(self):
        self.multi_canvas.delete("all")  # Canvas löschen

        if not self.multi_data:
            return  # Nichts zu zeichnen

        # Skalierung berechnen (Fehlerbehebung für Division durch Null)
        duration = max(self.multi_data[-1][0] - self.multi_data[0][0], 0.001)  # Kleine Zahl hinzufügen, um Division durch Null zu vermeiden
        x_scale = CANVAS_WIDTH / duration
        y_scale = CANVAS_HEIGHT / 100

        # Datenpunkte zeichnen
        last_x, last_y = None, None
        for timestamp, value in self.multi_data:
            x = (timestamp - self.multi_data[0][0]) * x_scale
            y = CANVAS_HEIGHT - (value * y_scale)
            if last_x is not None:
                self.multi_canvas.create_line(last_x, last_y, x, y, fill="blue")
            last_x, last_y = x, y

        # Zeitachse zeichnen
        self.draw_time_axis(self.multi_canvas, self.multi_data[0][0], duration)

    def draw_time_axis(self, canvas, start_time, duration):
        # Markierungen und Beschriftungen für jede Sekunde
        for i in range(int(duration) + 1):
            x = i * CANVAS_WIDTH / duration
            canvas.create_line(x, 0, x, CANVAS_HEIGHT, fill="gray", dash=(2, 2))
            canvas.create_text(x, CANVAS_HEIGHT - 10, text=f"{i:.1f}s", anchor=tk.N)

# Hauptanwendung starten
root = tk.Tk()
app = EKGApp(root)
root.mainloop()