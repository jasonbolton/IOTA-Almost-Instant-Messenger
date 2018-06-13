# IOTA Almost-Instant Messenger - A simple chat program based on IOTA technology.

Instructions

This program creates a one-time-use chat room based on the IOTA Tangle protocol. The user is prompted to either create a new chat-room, or to enter a chat-room with an address they already possess. The chat-room address is an IOTA address and is automatically generated. The messages will be encrypted with AES-128 encryption so a key is needed to send and decrypt messages. The creator of the channel will input a 16 character key. The address and key will need be given to the other chat-room participants. To run the main program, use tk_gui_file.py.

Dependencies

This program was made with Python 3.6.4. To run this program, pyota needs to be installed. You will also need to install PyCryptodome.

You can find pyota at: https://github.com/iotaledger/iota.lib.py

You can find python at https://www.python.org/downloads/

You can find PyCryptodome at: https://github.com/Legrandin/pycryptodome
