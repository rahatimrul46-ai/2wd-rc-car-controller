import tkinter as tk
from pyfirmata import Arduino

# --- CONFIGURATION ---
PORT = 'COM5'

print(f"Connecting to Arduino on {PORT}...")
try:
    board = Arduino(PORT)
    print("Successfully connected!")
except Exception as e:
    print(f"Error connecting: {e}")
    exit()

# --- PIN DEFINITIONS (2WD) ---
# Left Motor
in1 = board.get_pin('d:6:o')
in2 = board.get_pin('d:5:o')

# Right Motor
in3 = board.get_pin('d:4:o')
in4 = board.get_pin('d:3:o')

# Speed control (PWM)
ena = board.get_pin('d:9:p')   # Left motor speed
enb = board.get_pin('d:10:p')  # Right motor speed


# --- MOVEMENT FUNCTIONS ---
def stop_car(event=None):
    in1.write(0)
    in2.write(0)
    in3.write(0)
    in4.write(0)


def move_forward(event=None):
    # Both motors forward
    in1.write(1)
    in2.write(0)
    in3.write(1)
    in4.write(0)


def move_backward(event=None):
    # Both motors backward
    in1.write(0)
    in2.write(1)
    in3.write(0)
    in4.write(1)


def turn_left(event=None):
    # Left motor stop, Right motor forward
    in1.write(0)
    in2.write(0)
    in3.write(1)
    in4.write(0)


def turn_right(event=None):
    # Right motor stop, Left motor forward
    in1.write(1)
    in2.write(0)
    in3.write(0)
    in4.write(0)


def update_speed(val):
    speed = float(val) / 100.0
    ena.write(speed)
    enb.write(speed)


def on_closing():
    stop_car()
    board.exit()
    root.destroy()


# --- GUI SETUP ---
root = tk.Tk()
root.title("2WD RC Car Controller")
root.geometry("300x250")
root.protocol("WM_DELETE_WINDOW", on_closing)

# Title
lbl = tk.Label(root, text="2WD Drive Controls", font=("Arial", 14, "bold"))
lbl.pack(pady=10)

# Buttons Frame
btn_frame = tk.Frame(root)
btn_frame.pack()

# Buttons
btn_f = tk.Button(btn_frame, text="W (Forward)", width=10, height=2, bg="lightblue")
btn_b = tk.Button(btn_frame, text="S (Backward)", width=10, height=2, bg="lightblue")
btn_l = tk.Button(btn_frame, text="A (Left)", width=10, height=2, bg="lightgreen")
btn_r = tk.Button(btn_frame, text="D (Right)", width=10, height=2, bg="lightgreen")

# Layout
btn_f.grid(row=0, column=1, padx=5, pady=5)
btn_l.grid(row=1, column=0, padx=5, pady=5)
btn_b.grid(row=1, column=1, padx=5, pady=5)
btn_r.grid(row=1, column=2, padx=5, pady=5)

# Bind events
btn_f.bind("<ButtonPress-1>", move_forward)
btn_f.bind("<ButtonRelease-1>", stop_car)

btn_b.bind("<ButtonPress-1>", move_backward)
btn_b.bind("<ButtonRelease-1>", stop_car)

btn_l.bind("<ButtonPress-1>", turn_left)
btn_l.bind("<ButtonRelease-1>", stop_car)

btn_r.bind("<ButtonPress-1>", turn_right)
btn_r.bind("<ButtonRelease-1>", stop_car)

# Speed control
slider_frame = tk.Frame(root)
slider_frame.pack(pady=20)

speed_lbl = tk.Label(slider_frame, text="Speed:")
speed_lbl.pack(side=tk.LEFT)

speed_slider = tk.Scale(
    slider_frame,
    from_=0,
    to=100,
    orient=tk.HORIZONTAL,
    command=update_speed,
    length=150
)
speed_slider.set(70)
speed_slider.pack(side=tk.LEFT, padx=10)

# Initialize
update_speed(70)
stop_car()

root.mainloop()