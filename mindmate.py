import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import font
import json

DATA_FILE = "mood_entries.json" #stores the entries for the moods   

def load():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            print("JSON corrupted. Resetting entries.")
            return []

def savedentries(entries):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(entries, file, indent=4)


def support(mood): #stash of supportive messages
    messages = { "Happy": "So happy for you! You absolutely deserve that <3",
        "Okay": "You're holding steady, and that's what's important.",
        "Tired": "It's okay to rest for a bit, take care of yourself.",
        "Stressed": "Take things one at a time, you've got this.",
        "Sad": "Your feelings matter. You're not alone.",
        "Anxious": "Breathe. You're alright. This moment will pass.",
        "Angry": "What you feel is valid, feel it in the moment." }
    return messages.get(mood)

#defining colors beforehand
BG="#230007" 
CARD="#fcc8c2" 
BUTTON="#f8D7e3" 
BUTTON2="#c75146" 
TITLE="#f4bbd3"

#main app class written here
class MindMate:
    def __init__(self, root): #constructor method
        self.root=root
        root.title("MindMate – Daily Journal")
        root.geometry("520x650")
        root.config(bg=BG)
        self.entries=load()

        self.card=tk.Frame(root, bg=CARD, bd=0, relief="flat", highlightthickness=2, highlightbackground=TITLE)
        self.card.pack(pady=20, padx=20, fill="both", expand=True)

        #Title
        tk.Label(self.card, text="| Daily Check-In 🌸 |", bg=CARD, fg="#333", font="Helvetica 20 bold underline").pack(pady=10)

        self.inputtokens()
        self.buttons()
    
    def inputtokens(self): #takes input from user over here
        tk.Label(self.card, text="How do you feel today?", bg=CARD).pack()
        moods=["Happy", "Okay", "Tired", "Stressed", "Sad", "Anxious", "Angry"]
        self.mvar=tk.StringVar()
        self.mmenu=ttk.Combobox(self.card, textvariable=self.mvar, values=moods, state="readonly")
        self.mmenu.pack(pady=5)

        tk.Label(self.card, text="Stress Slider", bg=CARD).pack()
        self.sslider=tk.Scale(self.card, from_=0, to=10, bg=CARD, orient="horizontal", troughcolor=TITLE)
        self.sslider.pack() #slider for stress level

        tk.Label(self.card, text="Energy Levels", bg=CARD).pack()
        self.eslider=tk.Scale(self.card, from_=0, to=10, bg=CARD, orient="horizontal", troughcolor=BUTTON2)
        self.eslider.pack() #slider for energy level

        tk.Label(self.card, text="Write your heart out:", bg=CARD).pack()
        self.jbox=tk.Text(self.card, height=7, width=50, relief="solid", bd=1, font=("Arial", 10))
        self.jbox.pack(pady=5) #takes entry for journal

    def buttons(self):
        btframe=tk.Frame(self.card, bg=CARD)
        btframe.pack(pady=10) #sets the framework for the buttons to be used later on

        tk.Button(btframe, text="Save Entry", compound="left", bg=BUTTON, bd=0, padx=10, pady=5, font="Arial", command=self.save).grid(row=0, column=0, padx=5)
        tk.Button(btframe, text="History", compound="left", bg=BUTTON2, bd=0, padx=10, pady=5, font="Arial", command=self.viewhistory).grid(row=0, column=1, padx=5)
        tk.Button(btframe, text="Export", compound="left", bg=BUTTON, bd=0, padx=10, pady=5, font="Arial", command=self.export).grid(row=0, column=2, padx=5)

    def save(self): # to save user input (mood)
        mood=self.mvar.get()
        stress=self.sslider.get()
        energy=self.eslider.get()
        journal=self.jbox.get("1.0", tk.END).strip()

        if not mood: 
            messagebox.showwarning("Missing Data", "Please select your mood before saving.")
            return

        entry={"date":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mood":mood,
            "stress":stress,
            "energy":energy,
            "journal":journal}

        self.entries.append(entry)
        savedentries(self.entries)

        messagebox.showinfo("Saved", support(mood))

        # Clear fields and resetting values
        self.mvar.set("")
        self.sslider.set(0)
        self.eslider.set(0)
        self.jbox.delete("1.0", tk.END)

    def viewhistory(self): # to view past entries
        hwindow=tk.Toplevel(self.root)
        hwindow.title("History")
        hwindow.geometry("450x500")

        listbox=tk.Listbox(hwindow, width=60, height=20)
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


