from customtkinter import CTkToplevel,CTkButton,CTkLabel
class Messagebox(CTkToplevel):
    def __init__(self,title,message):
        super().__init__()
        self.geometry("400x200")
        self.resizable(False,False)
        self.title(title)
        self.card= CTkLabel(self, text="🗃️",font=("Arial", 50) )
        self.card.pack(side="left",padx="10")
        self.label = CTkLabel(self, text=message,wraplength=300,justify="left")
        self.label.pack(padx=5, pady=30)
        self.ok = CTkButton(self, text="OK", command=self._on_closing)
        self.ok.pack(side="bottom",anchor="e",padx=8, pady=8)
        self.lift()  # lift window on top
        self.attributes("-topmost", True)  # stay on top
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.grab_set()  # make other windows not clickable

    def _on_closing(self):
        self.grab_release()
        self.destroy()
