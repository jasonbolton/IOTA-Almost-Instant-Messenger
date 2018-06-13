# need iota, pycryptodome

from iota import *
from chat_room import ChatRoom
from transaction_send_bot import MessageSender
import base64
from Crypto import Random
from Crypto.Cipher import AES
import os
import sys
import random

class ControlProgram():

    def __init__(self):
        self._node = 'http://node03.iotatoken.nl:15265'
        self._api = Iota(self._node)

    def make_node_address(self):
        # creates an IOTA api instance in order to generate an IOTA address.
        # a proof-of-work node is required. 
        gna_result = self._api.get_new_addresses()
        address = gna_result['addresses'][0]
        #return address
        return "CG9VFDL9OEUCQJJHTLZLEYN9GIE9XQQBYOVO9LQJQYQHPEEOFVRKABPSRGNZFMMH9BSFTVXWEVGIGTJVW"

    def make_decoder_key(self):
        key = "catsssssssssssss"
##        for i in range(16):
##            pass
        return key
            


##        decoder_key = str.encode(decoder_key)
##
    
##    # instantiates chat-room at IOTA address and message-sender
##        chat_room = ChatRoom(address)


    # checks for initial messages, then loops for message-input and reloads
    # after each message sent. messages are encoded using AES-128 before
    # attaching to the tangle.
##    message_list = []
##    get_reload_messages(chat_room, message_list, decoder_key, iv)
##
##    while True:
##        user_message = input(">: ")
##        if user_message.lower() == 'exit' or user_message.lower() == 'quit':
##            sys.exit(1)
##        if user_message.lower() == 'new':
##            get_reload_messages(chat_room, message_list, decoder_key, iv)
##        else:
##            user_message = str.encode(user_message)
##            obj = AES.new(decoder_key, AES.MODE_CFB, iv)
##            encoded = base64.urlsafe_b64encode(obj.encrypt(user_message))
##            encoded = str(encoded, 'utf-8')
##            message_sender.send_message(encoded)
##            get_reload_messages(chat_room, message_list, decoder_key, iv)

##
##
##    def get_reload_messages(chat_room, message_list, decoder_key, iv):
##        # using the chat-room class object, checks the tangle for messages
##        # at the given address. decodes each message and prints to console.
##        new_messages = chat_room.get_transactions()
##        for message in new_messages:
##            message_list.append(message)
##        
##        for message in message_list:
##            message = message.decode()
##            message = str.encode(message)
##            obj2 = AES.new(decoder_key, AES.MODE_CFB, iv)
##            decoded = obj2.decrypt(base64.urlsafe_b64decode(message))
##            print(decoded.decode())
