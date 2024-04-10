import tkinter as tk
import time

class EKGSimulator:
    def __init__(self):
        self.time = 0
        self.data = []  # Hier kommen die EKG-Daten hin
        self.interval = 1  # Abstand zwischen den Datenpunkten in Millisekunden
        self.canvas_width = 400
        self.canvas_height = 200
        self.max_points = 100  # Maximale Anzahl von Datenpunkten im Laufband-Canvas
        self.max_wave_points = 1000  # Maximale Anzahl von Datenpunkten im Einzelwellen-Canvas

        self.root = tk.Tk()
        self.root.title("EKG Visualizer")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()

        self.wave_canvas = tk.Canvas(self.main_frame, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.wave_canvas.pack(side=tk.LEFT)
        self.wave_points = []

        self.scroll_canvas = tk.Canvas(self.main_frame, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.scroll_canvas.pack(side=tk.LEFT)
        self.scroll_points = []

        self.time_label = tk.Label(self.root, text="Zeit: 0 s")
        self.time_label.pack()

        self.update_visualization()

    def generate_fake_data(self):
        # Hier können Sie Ihre EKG-Daten erzeugen
        fake_value = 50  # Beispielwert
        self.data.append((self.time, fake_value))
        self.time += self.interval / 1000  # Umwandlung von Millisekunden in Sekunden

    def update_visualization(self):
        self.generate_fake_data()
        self.update_wave_canvas()
        self.update_scroll_canvas()
        self.time_label.config(text="Zeit: {:.2f} s".format(self.time))
        self.root.after(self.interval, self.update_visualization)

    def update_wave_canvas(self):
        if len(self.wave_points) >= self.max_wave_points:
            self.wave_points.pop(0)  # Löschen des ältesten Punktes, wenn der Canvas voll ist
        if len(self.data) > 0:
            time_val, value = self.data[-1]  # Nehme den neuesten Datenpunkt
            x = time_val * self.canvas_width
            y = self.canvas_height - value * (self.canvas_height / 100)
            self.wave_points.append((x, y))
            self.draw_points(self.wave_canvas, self.wave_points)

    def update_scroll_canvas(self):
        if len(self.scroll_points) >= self.max_points:
            self.scroll_points.pop(0)  # Löschen des ältesten Punktes, wenn der Canvas voll ist
        for i in range(len(self.data)):
            time_val, value = self.data[i]
            x = time_val * self.canvas_width
            y = self.canvas_height - value * (self.canvas_height / 100)
            self.scroll_points.append((x, y))
        self.draw_points(self.scroll_canvas, self.scroll_points)

    def draw_points(self, canvas, points):
        canvas.delete("all")
        if len(points) > 1:
            canvas.create_line(points, fill="blue")

if __name__ == "__main__":
    ekg_simulator = EKGSimulator()
    ekg_simulator.root.mainloop()
