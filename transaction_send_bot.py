from iota import *
import random
import time

class MessageSender:
    # this class handles the sending of transactions
    # requested by the main program. a proof of work node
    # is required.
    def __init__(self, send_address):
        self._send_address = send_address
        self._api = Iota('http://nodes.iota.fm:80')

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
        message = TryteString.from_unicode(message)
        send_confirmation = False
        while not send_confirmation:
            try:
                print("Sending message to the tangle...")
                self._api.send_transfer(
                  depth = 100,
                  transfers = [
                    ProposedTransaction(
                      address =
                        Address(
                          self._send_address,
                        ),
                      value = 0,
                      tag = Tag(random_tag),
                      message = message,
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
            
