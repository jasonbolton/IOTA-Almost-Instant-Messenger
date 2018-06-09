# need iota, pycryptodome

from iota import *
from chat_room import ChatRoom
from transaction_send_bot import MessageSender
import base64
from Crypto import Random
from Crypto.Cipher import AES
import os
import sys

def main():

    # initializes block size
    #iv = Random.new().read(AES.block_size)
    iv = b'0000000000000000'

    # introduction messages
    print("IOTA Almost-Instant Messenger has begun!")
    print("These conversations are encrypted with AES-128.")
    print("When the program is closed, the conversation will be lost")
    response = input("Do you need to create a new channel? (yes/no): ")
    # creates a new channel (IOTA address) and AES key or prompts for entry of both values (currently hard-coded)
    if response.lower() == 'yes' or response.lower() == 'y':
        #address = make_node_address()
        address = "LHCNQLKHAUFNPIKQGEHBPFUWSARZPQHOKDWBSNDQMZQBDFUBAVFQXUJOEOQIZRVQRCHZWJVQAUBHUDOYC"
        print("Please provide this channel address to the intended chat partner:")
        print("address:", address)
        decoder_key = ""
        while len(decoder_key) != 16:
            decoder_key = "aaaaaaaaaaaaaaaa"
            #decoder_key = input("Please create/enter the 16 character key of the channel: ")
    else:
        address = input("Please input the address of the channel you'd like to join: ")
        decoder_key = "aaaaaaaaaaaaaaaa"
    
    print("decoder key:", decoder_key)

    decoder_key = str.encode(decoder_key)

    # instantiates chat-room at IOTA address and message-sender
    chat_room = ChatRoom(address)
    message_sender = MessageSender(address)

    # checks for initial messages, then loops for message-input and reloads
    # after each message sent. messages are encoded using AES-128 before
    # attaching to the tangle.
    message_list = []
    get_reload_messages(chat_room, message_list, decoder_key, iv)

    while True:
        user_message = input(">: ")
        if user_message.lower() == 'exit' or user_message.lower() == 'quit':
            sys.exit(1)
        if user_message.lower() == 'new':
            get_reload_messages(chat_room, message_list, decoder_key, iv)
        else:
            user_message = str.encode(user_message)
            obj = AES.new(decoder_key, AES.MODE_CFB, iv)
            encoded = base64.urlsafe_b64encode(obj.encrypt(user_message))
            encoded = str(encoded, 'utf-8')
            message_sender.send_message(encoded)
            get_reload_messages(chat_room, message_list, decoder_key, iv)

def make_node_address():
    # creates an IOTA api instance in order to generate an IOTA address.
    # a proof-of-work node is required. 
    node = 'http://node03.iotatoken.nl:15265'
    api = Iota(node)
    gna_result = api.get_new_addresses()
    address = gna_result['addresses'][0]
    return address

def get_reload_messages(chat_room, message_list, decoder_key, iv):
    # using the chat-room class object, checks the tangle for messages
    # at the given address. decodes each message and prints to console.
    new_messages = chat_room.get_transactions()
    for message in new_messages:
        message_list.append(message)

    print("|To reload messages, type 'new'. To quit, type 'exit'.|")
    
    for message in message_list:
        message = message.decode()
        message = str.encode(message)
        obj2 = AES.new(decoder_key, AES.MODE_CFB, iv)
        decoded = obj2.decrypt(base64.urlsafe_b64decode(message))
        print(decoded.decode())



main()
