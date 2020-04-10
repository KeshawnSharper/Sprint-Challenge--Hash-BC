#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


class Ticket:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination


def reconstruct_trip(tickets, length):
    hashtable = HashTable(length)
    route = [None] * length
    for x in tickets:
        hash_table_insert(hashtable,x.source,x.destination)
    node = hash_table_retrieve(hashtable,"NONE")
    arr = []
    while node != "NONE":
        arr.append(node)
        node = hash_table_retrieve(hashtable,node)
    return arr
