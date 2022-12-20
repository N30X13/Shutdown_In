import tkinter as tk
import os
import tkinter.messagebox
import uuid
import time
import tkinter.ttk as ttk
import sys

# Verstecke das Consolenfenster
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

# Erstelle das Hauptfenster
root = tk.Tk()
root.title("Timer")
root.iconbitmap(".\\icons\\clock.ico")
root.resizable(False, False)
root.attributes()
root.configure(bg="#272c36")

# Lade die CSS-Datei
root.style = tk.ttk.Style()
root.style.theme_use("default")
root.style.configure(".", background="#272c36")
root.style.configure("TButton", weight=1, font=("helvetia", 20), background="#465061", foreground="#272c36", relief=("flat"))

# Erstelle Globale Variablen
timer_window = None
timer_label = None
start_time = None
timer_duration = None
timer_stopped = True

# Erstelle Funktionen für die Buttons
def start():
    global timer_window
    global start_time
    global timer_duration
    global timer_label
    global timer_stopped

    if timer_window is not None:
        timer_window.destroy()

    # Setze die Flagge "timer_stopped" auf "False"
    timer_stopped = False

    # Hole den Wert aus dem Eingabefeld und wandle ihn in eine Zahl um
    try:
        hours, minutes = map(int, input_field.get().split(":"))
        timer_duration = hours * 3600 + minutes * 60
    except ValueError:
        # Zeige eine Fehlermeldung, falls der Wert nicht in eine Zahl umgewandelt werden kann
        tkinter.messagebox.showerror("Ungültiger Wert", "Bitte geben Sie eine gültige Zeit im Format HH:MM ein.")
        return

    # Erstelle ein neues Fenster für den Timer
    timer_window = tk.Toplevel(root)
    timer_window.title("Timer läuft")
    timer_window.resizable(False, False)
    timer_window.attributes("-topmost", True, "-toolwindow", 1)
    timer_window.config(bg="#272c36")
    timer_window.overrideredirect(True)
    screen_width = timer_window.winfo_screenwidth()
    screen_height = timer_window.winfo_screenheight()
    window_width = timer_window.winfo_width()
    window_height = timer_window.winfo_height()
    timer_window.geometry("+{}+{}".format(screen_width - 280, screen_height - 230))

    # Erstelle einen Rahmen, der das Fenster bewegen kann
    move_frame = tk.Frame(timer_window, bg='#465061', cursor=("arrow"))
    move_frame.place(relx=0, rely=0, relwidth=0.1, relheight=0.1, anchor="n")

    # Erstelle eine Funktion zum Bewegen des Fensters
    def move_window(event):
        # Bewege das Fenster an die aktuelle Mausposition
        timer_window.geometry(f"+{event.x_root}+{event.y_root}")

    # Binde die Bewegungsfunktion an den Rahmen
    move_frame.bind("<B1-Motion>", move_window)

    # Erstelle Label für den Timer und Buttons für Stop
    timer_label = tk.Label(timer_window, text=timer_duration, name=str(uuid.uuid4()), font=("helvetia", 48), bg="#272c36", foreground="#465061")
    timer_label.pack(pady=10)

    stop_button = tk.ttk.Button(timer_window, text="Stop", command=stop, style="TButton")
    stop_button.pack(pady=10)

    # Blendet das Hauptfenster aus
    root.withdraw()

    # Starte den Timer
    start_time = time.time()
    count_down()

def count_down():
    global timer_duration
    global timer_label
    global timer_stopped

    if timer_stopped == False:
        elapsed_time = time.time() - start_time
        remaining_time = timer_duration - elapsed_time
        if remaining_time <= 0:
            # Timer abgelaufen, PC herunterfahren
            shutdown_command = "shutdown /s /t 0"
            os.system(shutdown_command)
        else:
            hours, minutes = divmod(int(remaining_time), 3600)
            minutes, seconds = divmod(minutes, 60)
            timer_label["text"] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            timer_window.update()
            timer_window.after(1000, count_down)

def stop():
    # Setze die Flagge auf "True", um anzuzeigen, dass der Timer gestoppt wurde
    global timer_stopped
    timer_stopped = True

    # Schließe das Timer-Fenster
    timer_window.destroy()

    # Blendet das Hauptfenster wieder ein
    root.deiconify()

def exit():
    # Beende das Programm
    root.destroy()

# Erstelle ein neues Label-Widget mit dem Text "Shutdown in:"
label = tk.Label(root, text="Shutdown in:", font=("helvetia", 30), bg="#272c36", foreground="#465061")

# Packen Sie das Label in das Hauptfenster
label.pack()

# Erstelle das Eingabefeld
input_field = tk.Entry(root, width=8, font=("helvetia", 40), bg="#465061", foreground="#272c36", justify="center")

# Packen Sie das Eingabefeld in das Hauptfenster und füge einen Text ein
input_field.pack(pady=10)
input_field.insert(0, "1:30")

start_button = tk.ttk.Button(root, text="Start", command=start, style="TButton")
start_button.pack(side="left", padx=0, pady=0)

exit_button = tk.ttk.Button(root, text="Exit", command=exit, style="TButton")
exit_button.pack(side="right", padx=0, pady=0)

# Zeige das Hauptfenster
root.mainloop()
