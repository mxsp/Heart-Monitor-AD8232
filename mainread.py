import tkinter as tk
import random
import time

class MovingGraph:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(self.master, width=500, height=500)
        self.canvas.pack()
        self.data = []
        self.start_time = time.time()  # Startzeit für die Zeitmessung
        self.x_axis = self.canvas.create_line(0, 490, 500, 490, fill='black')  # X-Achse hinzufügen
        self.x_labels = []

    def update_graph(self):
        self.canvas.delete('data')  # Lösche nur vorhandene Datenlinien
        self.canvas.delete('x_labels')  # Lösche nur vorhandene x-Achsenbeschriftungen
        if len(self.data) > 500:
            self.data.pop(0)
        self.data.append(random.randint(1, 500))
        for i in range(1, len(self.data)):
            self.canvas.create_line(i-1, 500-self.data[i-1], i, 500-self.data[i], fill='blue', tags='data')
        
        # Berechnen der Anzahl der x-Achsenbeschriftungen basierend auf der Anzahl der Datenpunkte
        num_labels = min(len(self.data), 10)  # Maximal 10 Beschriftungen
        label_step = max(1, len(self.data) // num_labels)
        for i in range(0, len(self.data), label_step):
            # Berechnen der vergangenen Zeit in Sekunden seit dem Start für jeden Datenpunkt
            elapsed_time = time.time() - self.start_time
            time_for_point = elapsed_time - (len(self.data) - i) * 0.1  # Annahme: 0.1 Sekunden pro Datenpunkt
            # Nur Beschriftungen anzeigen, die in 5-Sekunden-Schritten liegen
            #if int(time_for_point) % 5 == 0:
            x_label = self.canvas.create_text(i * (500 / len(self.data)), 495, text="{:.0f}s".format(time_for_point), tags='x_labels')
            self.x_labels.append(x_label)
        
        self.master.after(100, self.update_graph)

root = tk.Tk()
graph = MovingGraph(root)
root.after(10, graph.update_graph)
root.mainloop()
