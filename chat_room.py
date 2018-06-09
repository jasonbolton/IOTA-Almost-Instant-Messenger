from iota import *

class ChatRoom:
    # this class takes in an IOTA address and begins
    # a 'chat-room' which can retrieve messages at that
    # address
    def __init__(self, address):
        self._node = 'http://node03.iotatoken.nl:15265'
        self._api = Iota(self._node)
        self._address = address

        self._finished_transactions = {}

    def get_address(self):
        return self._address

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
