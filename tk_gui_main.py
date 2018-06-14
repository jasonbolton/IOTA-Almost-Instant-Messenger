import tkinter as tk
from tkinter import scrolledtext, PhotoImage, Image
from chat_room import ChatRoom

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.iconbitmap("images\j_icon.ico")
        self.switch_frame(StartPage)
        self.title("IOTA Almost-Instant Messenger")
        self.geometry("600x350")
        self._chat_room = ChatRoom()

    def switch_frame(self, frame_class):
        # destroys current frame and replaces it.
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def make_chat_room(self, address, decoder_key):
        # create a ChatRoom object with an address and key.
        self._chat_room = ChatRoom(address, decoder_key)

class StartPage(tk.Frame):
    # chat-room initialization page, contains address and key field
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self._address = ""
        self._key = ""

        self._address_label = tk.Label(self, text="Enter/Generate chat-room address")
        self._address_entry = tk.Entry(self, width=81)
        self._address_button = tk.Button(self, text="Generate Address",
                                  command=lambda: self.make_address(master))
        self._address_entry_reset = tk.Button(self, text="Reset",
                                  command=lambda: self.reset_address())
        
        self._key_label = tk.Label(self, text="Enter 16 character decoder key")
        self._key_entry = tk.Entry(self, width=81)
        self._key_button = tk.Button(self, text="Generate Key",
                                  command=lambda: self.make_key(master))
        self._key_entry_reset = tk.Button(self, text="Reset",
                                  command=lambda: self.reset_key())

        
        self._start_label = tk.Label(self, text="Start chat-room")
        self._page_1_button = tk.Button(self, text="Begin",
                                  command=lambda: self.switch_screen(master))
                
        self._address_label.pack(side="top", fill="x", pady=10)
        self._address_entry.pack()
        self._address_button.pack()
        self._address_entry_reset.pack()
        
        self._key_label.pack(side="top", fill="x", pady=10)
        self._key_entry.pack()
        self._key_button.pack()
        self._key_entry_reset.pack()
        
        self._start_label.pack(side="top", fill="x", pady=10)
        self._page_1_button.pack()

    def switch_screen(self, master):
        # begins the chat-room if the address and decoder key
        # are valid.
        self._address = self._address_entry.get()
        self._key = self._key_entry.get()
        if self._address != "" and len(self._address) == 81 and \
           self._key != "" and len(self._key) == 16:
            master.make_chat_room(self._address, self._key)
            master.switch_frame(PageOne)

    def make_address(self, master):
        # uses chat-room object to generate an address and
        # inserts it into the address entry field.
        self._address = master._chat_room.make_node_address()
        self._address_entry.delete(0, tk.END)
        self._address_entry.insert(0, self._address)
        print(self._address)

    def reset_address(self):
        # resets the address entry field and variable.
        self._address = ""
        self._address_entry.delete(0, tk.END)
        self._address_entry.insert(0, self._address)
        print(self._address)

    def make_key(self, master):
        # uses chat-room object to generate a key and
        # inserts it into the address entry field.
        self._key = master._chat_room.make_decoder_key()
        self._key_entry.delete(0, tk.END)
        self._key_entry.insert(0, self._key)
        print(self._key)

    def reset_key(self):
        # resets the decoder key entry field and variable.
        self._key = ""
        self._key_entry.delete(0, tk.END)
        self._key_entry.insert(0, self._key)
        print(self._key)

class PageOne(tk.Frame):
    # chat-room page with message entry field and chat-log.
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self._chat_messages = []

        def enter(event):
            # makes the enter key press an event.
            self.add_message(master)

        self._chat_box = scrolledtext.ScrolledText(self, state="disabled", width=81, height=15)
        self._input_box = tk.Entry(self, width=81)
        self._input_box.bind("<Return>", enter)
        self._send_button = tk.Button(self, text="Send",
                                      command=lambda: self.add_message(master))
        self._refresh_button = tk.Button(self, text="Refresh Messages",
                                      command=lambda: self.refresh(master))
        self._end_button = tk.Button(self, text="End Chat",
                                 command=lambda: app.destroy())

        self._chat_box.pack()
        self._input_box.pack()
        self._send_button.pack()
        self._refresh_button.pack()
        self._end_button.pack()

    def add_message(self, master):
        # sends the user-inputted message to the tangle,
        # refreshes the chat-log
        inp_message = self._input_box.get()
        if inp_message != "":
            master._chat_room.send_message(inp_message)
            self._chat_box.config(state="normal")
            self._input_box.delete(0, tk.END)
            self._chat_box.delete(0.0, tk.END)
            self.refresh(master)
            for message in self._chat_messages:
                self._chat_box.insert(0.0, message)
            self._chat_box.config(state="disabled")
        

    def refresh(self, master):
        # refreshes messages on the address and
        # reinserts them to the chat-box
        self._chat_box.config(state="normal")
        self._input_box.delete(0, tk.END)
        self._chat_box.delete(0.0, tk.END)
        self._chat_messages = master._chat_room.get_reload_messages()[::-1]
        for message in self._chat_messages:
            self._chat_box.insert(0.0, "\n")
            self._chat_box.insert(0.0, message)
        self._chat_box.config(state="disabled")        
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
