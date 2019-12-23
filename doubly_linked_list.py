"""
          -----------      -----------               -----------      -----------
None <--- |sentinel | ---> |first    | ---> ... ---> |last     | ---> |sentinel |
          |head node| <--- |data node| <--- ... <--- |data node| <--- |tail node| ---> None
          -----------      -----------               -----------      -----------
"""

class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None
        self.prev = None
        

class DoublyLinkedList:
    def __init__(self, iterable=None):
        self.head = Node()  # sentinel head Node
        self.tail = Node()  # sentinel tail Node
        self.head.next = self.tail
        self.tail.prev = self.head

        self.length = 0

        if iterable:
            self.extend(iterable)

    def __len__(self):
        return self.length

    def __str__(self):
        values = []
        pointer = self.head.next
        while pointer is not self.tail:
            values.append(str(pointer.value))
            pointer = pointer.next

        return ' => '.join(values)

    def is_empty(self):
        return self.length == 0

    def append(self, value):
        old_last_data_node = self.tail.prev
        new_last_data_node = Node(value)

        old_last_data_node.next = new_last_data_node
        new_last_data_node.prev = old_last_data_node

        new_last_data_node.next = self.tail
        self.tail.prev = new_last_data_node

        self.length += 1

    def appendleft(self, value):
        new_first_data_node = Node(value)
        old_first_data_node = self.head.next

        self.head.next = new_first_data_node
        new_first_data_node.prev = self.head

        new_first_data_node.next = old_first_data_node
        old_first_data_node.prev = new_first_data_node

        self.length += 1

    def clear(self):
        self.head.next = self.tail
        self.tail.prev = self.head
        self.length = 0

    def count(self, value):
        """Count the number of deque elements equal to x."""

        cnt = 0
        pointer = self.head.next
        while pointer is not self.tail:
            if pointer.value == value:
                cnt += 1
            pointer = pointer.next
        return cnt

    def extend(self, iterable):
        for el in iterable:
            self.append(el)

    def index(self, value, start=0, stop=None):
        stop = self.length if stop is None else stop

        i = 0
        pointer = self.head.next
        while pointer is not self.tail:
            if pointer.value == value and (start <= i < stop):
                return i
            i += 1
            pointer = pointer.next

        raise ValueError("target value is not in linked list")

    def remove(self, value):
        """
        Remove the first occurrence of value.
        If not found, raises a ValueError.
        """
        pointer = self.head.next
        while pointer is not self.tail:

            if pointer.value == value:
                pointer.prev.next = pointer.next
                pointer.next.prev = pointer.prev
                self.length -= 1
                return

            pointer = pointer.next

        raise ValueError('value not in doubly_linked_list')

    def insert(self, index, value):
        if index <= 0:
            self.appendleft(value)
            return
        elif index >= self.length:
            self.append(value)
            return

        i = 1  # case when index is 0 is dealt above
        pointer = self.head.next
        while pointer is not self.tail:
            if i == index:
                node = Node(value)  # node to be inserted
                node_before_insertion = pointer  # insert new node after pointer node
                node_after_insertion = pointer.next

                # link the inserted node and the node before it
                node_before_insertion.next = node
                node.prev = node_before_insertion
                # link the inserted node and the node after it
                node.next = node_after_insertion
                node_after_insertion.prev = node

                self.length += 1

            i += 1
            pointer = pointer.next

    def pop(self):

        old_last_data_node = self.tail.prev
        new_last_data_node = old_last_data_node.prev

        new_last_data_node.next = self.tail
        self.tail.prev = new_last_data_node

        return old_last_data_node


    def popleft(self):

        old_first_data_node = self.head.next
        new_first_data_node = old_first_data_node.next

        self.head.next = new_first_data_node
        new_first_data_node.prev = self.head

        return old_first_data_node

    def __reversed__(self):
        if self.length <= 1:
            return

        # pointers for head & tail node can also be adjusted like a normal node
        pointer = self.head
        while pointer:
            prev = pointer.prev
            nex_ = pointer.next

            pointer.next = prev
            pointer.prev = nex_

            pointer = nex_

        # swap head and tail pointer
        self.head, self.tail = self.tail, self.head

    def reverse(self):
        self.__reversed__()

    def rotate(self, steps=1):
        # use modulus to convert steps into range [0, self.length)
        steps %= self.length

        # linear linked list => circular linked list
        first_data_node = self.head.next
        last_data_node = self.tail.prev

        first_data_node.prev = last_data_node
        last_data_node.next = first_data_node

        while steps > 0:
            first_data_node = first_data_node.next
            last_data_node = last_data_node.next
            steps -= 1

        # circular linked list => linear linked list
        self.head.next = first_data_node
        first_data_node.prev = self.head
        self.tail.prev = last_data_node
        last_data_node.next = self.tail
