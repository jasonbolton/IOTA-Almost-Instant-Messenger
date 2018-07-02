from iota import *
import base64
from Crypto.Cipher import AES
import random
import time

class ChatRoom:
    # this class takes in an IOTA address and begins
    # a 'chat-room' which can retrieve messages at that
    # address.
    def __init__(self, address=None, decoder_key=None):
        self._node = 'http://nodes.iota.fm:80'
        self._api = Iota(self._node)
        self._address = address
        if decoder_key != None:
            self._decoder_key = str.encode(decoder_key)
        self._finished_transactions = {}
        self._message_list = []
        # initializes block size
        #iv = Random.new().read(AES.block_size)
        self._iv = b'0000000000000000'

    def get_transactions(self):
        # this method cycles through the transactions
        # on an address in the tangle. if the transaction
        # tag is in the dictionary self._finished_transactions,
        # the message is not processed. if not, the message is
        # stripped to access the message data. the data is added
        # to a list to be returned and the tag is added to finished
        # transactions.
        print("Searching the tangle for new messages...")
        self._new_transactions = []
        transaction_dict = self._api.find_transactions(bundles=None, \
                            addresses=[self._address], tags=None, approvees=None)
        for transaction_hash in transaction_dict['hashes']:
            trytes = self._api.get_trytes([transaction_hash])['trytes'][0]
            transaction = Transaction.from_tryte_string(trytes)
            if transaction.tag not in self._finished_transactions:
                self._finished_transactions[transaction.tag] = 0
                message = transaction.signature_message_fragment
                self._new_transactions.append(message)
        print("Complete")
        print()
        return self._new_transactions

    def make_random_tag(self):
        # this method constructs a random tag to include
        # in outgoing transactions.
        construct_tag = ""
        for i in range(27):
            rand_char = chr(random.randint(80, 90))
            construct_tag += rand_char
        construct_tag = TryteString.from_unicode(construct_tag)
        if len(construct_tag) > 27:
            excess = len(construct_tag) - 27
            construct_tag = construct_tag[excess:]
        return construct_tag

    def send_message(self, message):
        # a random tag transaction with a passed-in
        # pre-encrypted message is sent using this method.
        random_tag = self.make_random_tag()
        message = str.encode(message)
        obj = AES.new(self._decoder_key, AES.MODE_CFB, self._iv)
        encoded = base64.urlsafe_b64encode(obj.encrypt(message))
        encoded = str(encoded, 'utf-8')
        encoded = TryteString.from_unicode(encoded)
        send_confirmation = False
        while not send_confirmation:
            try:
                print("Sending message to the tangle...")
                self._api.send_transfer(
                  depth = 3,
                  transfers = [
                    ProposedTransaction(
                      address =
                        Address(
                          self._address,
                        ),
                      value = 0,
                      tag = Tag(random_tag),
                      message = encoded,
                    ),
                  ],
                )
                send_confirmation = True
                print("The message was successfully attached to the tangle")
                print()
            except:
                print("Error: Retrying tangle attachment")
                print()
                time.sleep(2)
                pass
            
    def get_reload_messages(self):
        # using the chat-room class object, checks the tangle for messages
        # at the given address. decodes each message and prints to console.
        return_list = []
        new_messages = self.get_transactions()
        for message in new_messages:
            self._message_list.append(message)
        for message in self._message_list:
            message = message.decode()
            message = str.encode(message)
            obj2 = AES.new(self._decoder_key, AES.MODE_CFB, self._iv)
            decoded = obj2.decrypt(base64.urlsafe_b64decode(message))
            return_list.append(decoded.decode())
        return return_list

    def make_decoder_key(self):
        # makes a decoder key for the AES encryption.
        key = ""
        for i in range(16):
            x = random.randint(1, 5)
            if x <= 3:
                y = random.randint(1, 2)
                z = random.randint(65, 90)
                if y == 1:
                    key += chr(z)
                else:
                    key += chr(z).lower()
            else:
                z = random.randint(1, 9)
                key += str(z)
        return key

    def make_node_address(self):
        # creates an IOTA api instance in order to generate an IOTA address.
        # a proof-of-work node is required.
        gna_result = self._api.get_new_addresses()
        address = gna_result['addresses'][0]
        return address
    
