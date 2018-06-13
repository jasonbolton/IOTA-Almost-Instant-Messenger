import tkinter as tk
from tkinter import scrolledtext
from main import ControlProgram
from chat_room import ChatRoom, ControlProgram

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)
        self.title("IOTA Almost-Instant Messenger")
        self.geometry("600x350")
        self._control_program = ControlProgram()
        self._chat_room = None

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def make_chat_room(self, address, decoder_key):
        self._chat_room = ChatRoom(address, decoder_key)

class StartPage(tk.Frame):
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
        if self._address != "" and len(self._address) == 81 and \
           self._key != "" and len(self._key) == 16:
            master.make_chat_room(self._address, self._key)
            master.switch_frame(PageOne)

    def make_address(self, master):
        self._address = master._control_program.make_node_address()
        self._address_entry.delete(0, 81)
        self._address_entry.insert(0, self._address)
        print(self._address)

    def reset_address(self):
        self._address = ""
        self._address_entry.delete(0, 81)
        self._address_entry.insert(0, self._address)
        print(self._address)

    def make_key(self, master):
        self._key = master._control_program.make_decoder_key()
        self._key_entry.delete(0, 81)
        self._key_entry.insert(0, self._key)
        print(self._key)

    def reset_key(self):
        self._key = ""
        self._key_entry.delete(0, 81)
        self._key_entry.insert(0, self._key)
        print(self._key)

    def get_address(self):
        return self._address

    def get_key(self):
        return self._key


class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self._chat_messages = []

        def enter(event):
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
        inp_message = self._input_box.get()
        if inp_message != "":
            master._chat_room.send_message(inp_message)
            self._chat_box.config(state="normal")
            self._input_box.delete(0, 81)
            self._chat_box.delete(0.0, 81.0)
            self.refresh(master)
            for message in self._chat_messages:
                self._chat_box.insert(0.0, message)
            print(self._chat_messages)
            #self._chat_messages = self._chat_messages[::-1]
            self._chat_box.config(state="disabled")

    def refresh(self, master):
        self._chat_box.config(state="normal")
        self._input_box.delete(0, 81)
        self._chat_box.delete(0.0, 81.0)
        self._chat_messages = master._chat_room.get_reload_messages()[::-1]
        for message in self._chat_messages:
            self._chat_box.insert(0.0, "\n")
            self._chat_box.insert(0.0, message)
        print(self._chat_messages)
        self._chat_messages = self._chat_messages[::-1]
        self._chat_box.config(state="disabled")
        
        
if __name__ == "__main__":
    app = App()
    app.mainloop()