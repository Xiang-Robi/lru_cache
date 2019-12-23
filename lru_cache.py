from doubly_linked_list import Node, DoublyLinkedList

class NodeForLRUCache(Node):
    def __init__(self, key=None, value=None):
        if key is None:
            raise ValueError("key must be provided")
        super(NodeForLRUCache, self).__init__(value)
        self.key = key


class DoublyLinkedListForLRUCache(DoublyLinkedList):
    def __init__(self):
        super(DoublyLinkedListForLRUCache, self).__init__()

    def __str__(self):
        pointer = self.head.next

        items = []
        while pointer is not self.tail:
            item = "{}: {}".format(pointer.key, pointer.value)
            items.append(item)
            pointer = pointer.next
        return " => ".join(items)

    def remove_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
        self.length -= 1

    def append_node_left(self, node):
        old_first_data_node = self.head.next

        self.head.next = node
        node.prev = self.head

        node.next = old_first_data_node
        old_first_data_node.prev = node
        self.length += 1

    def move_node_to_start(self, node):
        self.remove_node(node)
        self.append_node_left(node)


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.cache = {}
        self.usage_tracking_list = DoublyLinkedListForLRUCache()

    def __str__(self):
        return str(self.usage_tracking_list)

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self.usage_tracking_list.move_node_to_start(node)
            return node.value

        return None

    def put(self, key, value):

        if key in self.cache:   # Case 1: key already in cache
            node = self.cache[key]
            node.value = value  # update node value
            self.usage_tracking_list.move_node_to_start(node)

        else:                   # Case 2: key not in cache
            if self.size == self.capacity:  # cache is full
                evicted_node = self.usage_tracking_list.pop()
                del self.cache[evicted_node.key]
                self.size -= 1

            node = NodeForLRUCache(key, value)
            self.usage_tracking_list.append_node_left(node)
            self.cache[key] = node
            self.size += 1


if __name__ == '__main__':

    lru_chache = LRUCache(2)
    lru_chache.put('a', 'A')
    lru_chache.put('b', 'B')
    print(lru_chache.get('b'))  # return 'B'
    print(lru_chache.get('a'))  # return 'A'
    print(lru_chache.get('c'))  # return None
    lru_chache.put('d', 'D')  # replace the least recently used item ('b', 'B')
    print(lru_chache.get('b'))  # return None
    
