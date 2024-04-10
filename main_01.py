import customtkinter as ctk
import time
import math
import random
import csv

# Function to generate realistic ECG data
def get_ekg_data():
    timestamp = time.time()
    t = (timestamp % 1) * 2 * math.pi
    p_wave = 5 * math.sin(t)
    qrs_complex = 40 * math.sin(1.5 * t) * math.exp(-0.25 * t**2)
    t_wave = 10 * math.sin(2 * t) * math.exp(-0.5 * t**2)
    value = 50 + p_wave + qrs_complex + t_wave
    value = max(0, min(value, 100))
    return timestamp, value

class EKGApp:
    def __init__(self, master):
        self.master = master
        master.title("EKG Visualization")

        # Main Frame
        main_frame = ctk.CTkFrame(master)
        main_frame.pack(fill=ctk.BOTH, expand=True)

        # Single Sweep Canvas
        self.single_canvas = ctk.CTkCanvas(main_frame, width=600, height=300)
        self.single_canvas.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

        # Multi Sweep Canvas
        self.multi_canvas = ctk.CTkCanvas(main_frame, width=600, height=300)
        self.multi_canvas.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

        # Input Frame
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.pack(side=ctk.RIGHT, fill=ctk.Y)

        # Data Structures
        self.single_data = []
        self.multi_data = []
        self.logged_data = []

        # Time Variables
        self.start_time = time.time()
        self.multi_sweep_duration = 30  # Initial Laufbanddauer

        # Trigger Variables
        self.trigger_level = 50
        self.trigger_armed = False
        self.trigger_paused = False
        self.trigger_timestamp = None
        self.last_trigger_timestamp = None
        self.last_value = 0
        self.trigger_count = 0

        # Cooldown Variables
        self.cooldown_time = 0
        self.cooldown_active = False

        # Logging Variables
        self.logging_active = False

        # Input Fields and Buttons (with consistent size)
        self.create_input_fields(input_frame)

        # Logging Frame
        logging_frame = ctk.CTkFrame(master)
        logging_frame.pack(fill=ctk.X)
        self.create_logging_buttons(logging_frame)

        # Update Data Periodically
        self.update_data()

        # Resize Handling
        self.single_canvas.bind("<Configure>", self.on_resize)
        self.multi_canvas.bind("<Configure>", self.on_resize)

    def create_input_fields(self, frame):
        # Consistent width for all input elements
        input_width = 150

        # Trigger Level
        ctk.CTkLabel(frame, text="Trigger Level:").pack()
        self.trigger_entry = ctk.CTkEntry(frame, width=input_width)
        self.trigger_entry.insert(0, str(self.trigger_level))
        self.trigger_entry.pack()

        # Flank Selection
        ctk.CTkLabel(frame, text="Flanke:").pack()
        self.flank_var = ctk.StringVar(value="Steigende Flanke")
        self.flank_combobox = ctk.CTkComboBox(frame, variable=self.flank_var, values=["Steigende Flanke", "Fallende Flanke"], width=input_width)
        self.flank_combobox.pack()

        # Cooldown
        ctk.CTkLabel(frame, text="Cooldown (Sekunden):").pack()
        self.cooldown_entry = ctk.CTkEntry(frame, width=input_width)
        self.cooldown_entry.insert(0, "0")
        self.cooldown_entry.pack()
        self.cooldown_button = ctk.CTkButton(frame, text="Cooldown setzen", command=self.set_cooldown, width=input_width)
        self.cooldown_button.pack()


        # Ax Time (X-Achsen-Zeit)
        ctk.CTkLabel(frame, text="Ax-Zeit (Sekunden):").pack()
        self.ax_time_entry = ctk.CTkEntry(frame, width=input_width)
        self.ax_time_entry.insert(0, str(self.multi_sweep_duration))  # Initial value
        self.ax_time_entry.pack()
        self.ax_time_button = ctk.CTkButton(frame, text="Ax-Zeit setzen", command=self.set_ax_time, width=input_width)
        self.ax_time_button.pack()


        # Trigger Buttons
        self.trigger_button = ctk.CTkButton(frame, text="Trigger starten", command=self.toggle_trigger, width=input_width)
        self.trigger_button.pack()
        self.pause_button = ctk.CTkButton(frame, text="Trigger pausieren", command=self.pause_trigger, state=ctk.DISABLED, width=input_width)
        self.pause_button.pack()

        # Multi Sweep Duration (Laufbanddauer)
        ctk.CTkLabel(frame, text="Laufbanddauer (Sekunden):").pack()
        self.duration_entry = ctk.CTkEntry(frame, width=input_width)
        self.duration_entry.insert(0, "30")
        self.duration_entry.pack()
        self.duration_button = ctk.CTkButton(frame, text="Dauer setzen", command=self.set_duration, width=input_width) 
        self.duration_button.pack()


    def set_ax_time(self):
        try:
            self.multi_sweep_duration = float(self.ax_time_entry.get())
        except ValueError:
            pass
        
    def create_logging_buttons(self, frame):
        # Consistent width for logging buttons
        button_width = 120

        self.start_logging_button = ctk.CTkButton(frame, text="Start Logging", command=self.start_logging, width=button_width)
        self.start_logging_button.pack(side=ctk.LEFT)
        self.end_logging_button = ctk.CTkButton(frame, text="End Logging", command=self.end_logging, state=ctk.DISABLED, width=button_width)
        self.end_logging_button.pack(side=ctk.LEFT)
        self.save_data_button = ctk.CTkButton(frame, text="Save Data", command=self.save_data, state=ctk.DISABLED, width=button_width)
        self.save_data_button.pack(side=ctk.LEFT)

    def set_cooldown(self):
        try:
            self.cooldown_time = float(self.cooldown_entry.get())
        except ValueError:
            pass

    def set_duration(self):
        try:
            self.multi_sweep_duration = float(self.duration_entry.get())
        except ValueError:
            pass

    def toggle_trigger(self):
        if self.trigger_armed:
            self.trigger_armed = False
            self.trigger_button.configure(text="Trigger starten")
            self.pause_button.configure(state=ctk.DISABLED)
            self.single_data = []
            self.draw_single_canvas()
        else:
            try:
                self.trigger_level = float(self.trigger_entry.get())
            except ValueError:
                pass
            self.trigger_armed = True
            self.trigger_button.configure(text="Trigger stoppen")
            self.pause_button.configure(state=ctk.NORMAL)
            self.trigger_count = 0

    def pause_trigger(self):
        self.trigger_paused = not self.trigger_paused
        if self.trigger_paused:
            self.pause_button.configure(text="Trigger fortsetzen")
        else:
            self.pause_button.configure(text="Trigger pausieren")

    def start_logging(self):
        self.logging_active = True
        self.logged_data = []
        self.start_logging_button.configure(state=ctk.DISABLED)
        self.end_logging_button.configure(state=ctk.NORMAL)

    def end_logging(self):
        self.logging_active = False
        self.start_logging_button.configure(state=ctk.NORMAL)
        self.end_logging_button.configure(state=ctk.DISABLED)
        self.save_data_button.configure(state=ctk.NORMAL)

    def save_data(self):
        # Popup for file name
        file_name = ctk.CTkInputDialog(text="Enter file name:", title="Save Data").get_input()
        if file_name:
            with open(f"{file_name}.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Timestamp", "Value"])
                writer.writerows(self.logged_data)
            self.save_data_button.configure(state=ctk.DISABLED)

    def update_data(self):
        # Get EKG Data
        timestamp, value = get_ekg_data()

        # Update Multi Sweep Data
        self.multi_data.append((timestamp, value))
        if timestamp - self.multi_data[0][0] > self.multi_sweep_duration:
            self.multi_data.pop(0)

        # Trigger Logic
        if self.trigger_armed and not self.trigger_paused and not self.cooldown_active:
            condition = (value >= self.trigger_level and self.last_value < self.trigger_level) if self.flank_var.get() == "Steigende Flanke" else (value <= self.trigger_level and self.last_value > self.trigger_level)
            if condition:
                self.last_trigger_timestamp = timestamp
                self.single_data = []
                self.trigger_count = 0
                if self.cooldown_time > 0:
                    self.cooldown_active = True
                    self.master.after(int(self.cooldown_time * 1000), self.end_cooldown)

        # Update Single Sweep Data
        if self.last_trigger_timestamp is not None and self.trigger_armed and not self.trigger_paused:
            self.single_data.append((timestamp, value))

        # Update Logged Data
        if self.logging_active:
            self.logged_data.append((timestamp, value))

        # Draw Canvases
        self.draw_single_canvas()
        self.draw_multi_canvas()

        # Store last value and update trigger count
        self.last_value = value
        if self.trigger_armed and not self.trigger_paused:
            self.trigger_count += 1

        # Call again after 1ms
        self.master.after(1, self.update_data)

    def end_cooldown(self):
        self.cooldown_active = False

    def draw_single_canvas(self):
        self.single_canvas.delete("all")
        if not self.single_data or self.last_trigger_timestamp is None:
            return 
        last_x, last_y = None, None
        for timestamp, value in self.single_data:
            x = (timestamp - self.last_trigger_timestamp) * self.single_canvas.winfo_width() / self.multi_sweep_duration
            y = self.single_canvas.winfo_height() - (value * self.single_canvas.winfo_height() / 100)
            if last_x is not None:
                self.single_canvas.create_line(last_x, last_y, x, y, fill="blue")
            last_x, last_y = x, y

    def draw_multi_canvas(self):
        self.multi_canvas.delete("all")
        if not self.multi_data:
            return 
        duration = max(self.multi_data[-1][0] - self.multi_data[0][0], 0.001)
        x_scale = self.multi_canvas.winfo_width() / duration
        y_scale = self.multi_canvas.winfo_height() / 100
        last_x, last_y = None, None
        for timestamp, value in self.multi_data:
            x = (timestamp - self.multi_data[0][0]) * x_scale
            y = self.multi_canvas.winfo_height() - (value * y_scale)
            if last_x is not None:
                self.multi_canvas.create_line(last_x, last_y, x, y, fill="blue")
            last_x, last_y = x, y
        self.draw_time_axis(self.multi_canvas, self.multi_data[0][0], duration)
        trigger_y = self.multi_canvas.winfo_height() - (self.trigger_level * y_scale)
        self.multi_canvas.create_line(self.multi_canvas.winfo_width() - 10, trigger_y, self.multi_canvas.winfo_width(), trigger_y + 5, fill="red")
        self.multi_canvas.create_line(self.multi_canvas.winfo_width() - 10, trigger_y, self.multi_canvas.winfo_width(), trigger_y - 5, fill="red")

    def draw_time_axis(self, canvas, start_time, duration):
        for i in range(int(duration) + 1):
            x = i * canvas.winfo_width() / duration
            canvas.create_line(x, 0, x, canvas.winfo_height(), fill="gray", dash=(2, 2))
            canvas.create_text(x, canvas.winfo_height() - 10, text=f"{i:.1f}s", anchor=ctk.N)

    def on_resize(self, event):
        self.draw_single_canvas()
        self.draw_multi_canvas()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
    root = ctk.CTk()
    app = EKGApp(root)
    root.mainloop()