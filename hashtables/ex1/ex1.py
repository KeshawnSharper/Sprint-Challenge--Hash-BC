#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(16)
    if length <= 1:
        return None
    else:
        f = 0
        for x in weights:
            hash_table_insert(ht,x,f)
            f +=1 
        y = 0 
        match = None
        while match is None:
            match = hash_table_retrieve(ht,limit - weights[y])
            y += 1
        if match > y - 1:
            return [match,y-1]
        else:
            return [y-1,match]
    


def print_answer(answer):
    if answer is not None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")
