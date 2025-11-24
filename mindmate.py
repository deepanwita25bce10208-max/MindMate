import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import font
import json
import os
from datetime import datetime

DATA_FILE = "mood_entries.json" #stores the entries for the moods

#defining colors beforehand
BG = "#230007"       
CARD = "#fcc8c2"    
BUTTON = "#f8D7e3"   
BUTTON2 = "#c75146"  
TITLE = "#f4bbd3"    

def load():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            print("[Warning] JSON corrupted. Resetting entries.")
            return []

def savedentries(entries):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(entries, file, indent=4)


def support(mood):
    messages = {
        "Happy": "Love that for you- keep riding that wave!",
        "Okay": "You're holding steady, and that's completely valid.",
        "Tired": "Rest isn't weakness. Your body is asking for care.",
        "Stressed": "It's okay to slow down. One thing at a time.",
        "Sad": "Your feelings matter. You're not alone.",
        "Anxious": "Breathe. You're alright. This moment will pass.",
        "Angry": "Your emotions are valid. Let them flow safely."
    }
    return messages.get(mood)


#main app class written here
class MindMate:
    def __init__(self, root):
        self.root = root
        root.title("MindMate – Daily Journal")
        root.geometry("520x650")
        root.config(bg=BG)
        self.entries=load()

        # Main card frame
        card = tk.Frame(root, bg=CARD, bd=0, relief="flat", highlightthickness=2, highlightbackground=TITLE)
        card.pack(pady=20, padx=20, fill="both", expand=True)

        # Title
        tk.Label(
            card,
            text="| Daily Check-In 🌸 |",
            bg=CARD,
            fg="#333", 
            font="Helvetica 20 bold underline"
        ).pack(pady=10)

        # Mood Selector
        tk.Label(card, text="Your mood today:", bg=CARD).pack()
        moods=["Happy", "Okay", "Tired", "Stressed", "Sad", "Anxious", "Angry"]
        self.mood_var=tk.StringVar()
        self.mood_menu=ttk.Combobox(card, textvariable=self.mood_var, values=moods, state="readonly")
        self.mood_menu.pack(pady=5)

        tk.Label(card, text="Stress Level (0-10):", bg=CARD).pack()
        self.stress_slider=tk.Scale(card, from_=0, to=10, bg=CARD, orient="horizontal", troughcolor=TITLE)
        self.stress_slider.pack() #stress slider

        tk.Label(card, text="Energy Level (0-10):", bg=CARD).pack()
        self.energy_slider=tk.Scale(card, from_=0, to=10, bg=CARD, orient="horizontal", troughcolor=BUTTON2)
        self.energy_slider.pack() #energy slider

        tk.Label(card, text="Journal Entry:", bg=CARD).pack()
        self.journal_box = tk.Text(card, height=7, width=50, relief="solid", bd=1, font=("Arial", 10))
        self.journal_box.pack(pady=5) #accepts energy for journal

        btn_frame=tk.Frame(card, bg=CARD)
        btn_frame.pack(pady=10) #sets the framework for the buttons to be used later on

        tk.Button(btn_frame, text="Save Entry",
                  compound="left", bg=BUTTON, bd=0, padx=10, pady=5,
                  font="Arial", command=self.save).grid(row=0, column=0, padx=5)

        tk.Button(btn_frame, text=" History",
                  compound="left", bg=BUTTON2, bd=0, padx=10, pady=5,
                font="Arial", command=self.viewhistory).grid(row=0, column=1, padx=5)

        tk.Button(btn_frame, text=" Export",
                  compound="left", bg=BUTTON, bd=0, padx=10, pady=5,
                  font="Arial", command=self.export).grid(row=0, column=2, padx=5)

    def save(self): # to save user input (mood)
        mood=self.mood_var.get()
        stress=self.stress_slider.get()
        energy=self.energy_slider.get()
        journal=self.journal_box.get("1.0", tk.END).strip()

        if not mood: 
            messagebox.showwarning("Missing Data", "Please select your mood before saving.")
            return

        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mood": mood,
            "stress": stress,
            "energy": energy,
            "journal": journal
        }

        self.entries.append(entry)
        savedentries(self.entries)

        messagebox.showinfo("Saved", support(mood))

        # Clear fields and resetting values
        self.mood_var.set("")
        self.stress_slider.set(0)
        self.energy_slider.set(0)
        self.journal_box.delete("1.0", tk.END)

    # to view past entries
    def viewhistory(self):
        history_win=tk.Toplevel(self.root)
        history_win.title("History")
        history_win.geometry("450x500")

        listbox=tk.Listbox(history_win, width=60, height=20)
        listbox.pack(pady=10)

        for entry in self.entries:
            listbox.insert(tk.END, f"{entry['date']} - {entry['mood']}")

    #exports all entries to .txt file
    def export(self):
        file=filedialog.asksaveasfilename(defaultextension=".txt")

        if not file:
            return

        with open(file, "w", encoding="utf-8") as f:
            for entry in self.entries:
                f.write(f"Date: {entry['date']}\n")
                f.write(f"Mood: {entry['mood']}\n")
                f.write(f"Stress: {entry['stress']}\n")
                f.write(f"Energy: {entry['energy']}\n")
                f.write(f"Journal: {entry['journal']}\n")
                f.write("-"*40+"\n")

        messagebox.showinfo("Exported", "Entries exported successfully!")
    
root=tk.Tk()
app=MindMate(root)
root.mainloop()

