import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports

def get_available_ports():
    return [port.device for port in serial.tools.list_ports.comports()]

def on_ok():
    selected_port = port_var.get()
    ai_flag = ai_var.get()
    # Do something with selected port and AI flag
    print(f"Selected Port: {selected_port}, AI Flag: {ai_flag}")

def on_abort():
    window.destroy()

window = tk.Tk()
window.title("Simple Tkinter Window")

# Port selection
port_var = tk.StringVar(value="Select Port")
port_label = tk.Label(window, text="Port:")
port_label.pack()
port_dropdown = ttk.Combobox(window, textvariable=port_var, values=get_available_ports())
port_dropdown.pack()

# AI checkbox
ai_var = tk.BooleanVar()
ai_checkbox = tk.Checkbutton(window, text="AI Flag", variable=ai_var)
ai_checkbox.pack()

# Buttons
button_frame = tk.Frame(window)
button_frame.pack()
ok_button = tk.Button(button_frame, text="OK", command=on_ok)
ok_button.pack(side=tk.LEFT)
abort_button = tk.Button(button_frame, text="Abort", command=on_abort)
abort_button.pack(side=tk.LEFT)

window.mainloop()
