import tkinter as tk
from pyfirmata2 import Arduino, util

# --- CONFIGURATION ---
# Replace 'COM3' with the port your Arduino is connected to (e.g., '/dev/ttyACM0' on Mac/Linux)
PORT = 'COM3'

print(f"Connecting to Arduino on {PORT}...")
try:
    board = Arduino(PORT)
    print("Successfully connected!")
except Exception as e:
    print(f"Error connecting: {e}")
    exit()

# --- PIN DEFINITIONS ---
# Set up the pins based on your wiring (Note: ENB is changed to 10 for PWM)
in1 = board.get_pin('d:6:o')  # Output
in2 = board.get_pin('d:5:o')  # Output
in3 = board.get_pin('d:4:o')  # Output
in4 = board.get_pin('d:3:o')  # Output
ena = board.get_pin('d:9:p')  # PWM for speed control
enb = board.get_pin('d:10:p') # PWM for speed control (Moved from 8 to 10)

# --- MOVEMENT FUNCTIONS ---
def stop_car(event=None):
    in1.write(0)
    in2.write(0)
    in3.write(0)
    in4.write(0)

def move_backward(event=None):
    in1.write(1)
    in2.write(0)
    in3.write(1)
    in4.write(0)
def move_forward(event=None):
    in1.write(0)
    in2.write(1)
    in3.write(0)
    in4.write(1)

def turn_left(event=None):
    # Left wheels reverse, right wheels go forward
    in1.write(0)
    in2.write(1)
    in3.write(1)
    in4.write(0)

def turn_right(event=None):
    # Left wheels go forward, right wheels reverse
    in1.write(1)
    in2.write(0)
    in3.write(0)
    in4.write(1)

def update_speed(val):
    # Pyfirmata takes PWM values between 0.0 and 1.0
    speed_float = float(val) / 100.0
    ena.write(speed_float)
    enb.write(speed_float)

def on_closing():
    stop_car()
    board.exit()
    root.destroy()

# --- GUI SETUP ---
root = tk.Tk()
root.title("4WD RC Car Controller")
root.geometry("300x250")
root.protocol("WM_DELETE_WINDOW", on_closing)

# Label
lbl = tk.Label(root, text="Drive Controls", font=("Arial", 14, "bold"))
lbl.pack(pady=10)

# Control Frame for Buttons (Grid Layout)
btn_frame = tk.Frame(root)
btn_frame.pack()

# Buttons
btn_f = tk.Button(btn_frame, text="W (Forward)", width=10, height=2, bg="lightblue")
btn_b = tk.Button(btn_frame, text="S (Backward)", width=10, height=2, bg="lightblue")
btn_l = tk.Button(btn_frame, text="A (Left)", width=10, height=2, bg="lightgreen")
btn_r = tk.Button(btn_frame, text="D (Right)", width=10, height=2, bg="lightgreen")

# Grid Placement
btn_f.grid(row=0, column=1, padx=5, pady=5)
btn_l.grid(row=1, column=0, padx=5, pady=5)
btn_b.grid(row=1, column=1, padx=5, pady=5)
btn_r.grid(row=1, column=2, padx=5, pady=5)

# Bindings (Press to move, Release to stop)
btn_f.bind("<ButtonPress-1>", move_forward)
btn_f.bind("<ButtonRelease-1>", stop_car)

btn_b.bind("<ButtonPress-1>", move_backward)
btn_b.bind("<ButtonRelease-1>", stop_car)

btn_l.bind("<ButtonPress-1>", turn_left)
btn_l.bind("<ButtonRelease-1>", stop_car)

btn_r.bind("<ButtonPress-1>", turn_right)
btn_r.bind("<ButtonRelease-1>", stop_car)

# Speed Slider
slider_frame = tk.Frame(root)
slider_frame.pack(pady=20)

speed_lbl = tk.Label(slider_frame, text="Speed:")
speed_lbl.pack(side=tk.LEFT)

speed_slider = tk.Scale(slider_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=update_speed, length=150)
speed_slider.set(70) # Set default speed to 70%
speed_slider.pack(side=tk.LEFT, padx=10)

# Stop the car initially
stop_car()

root.mainloop()