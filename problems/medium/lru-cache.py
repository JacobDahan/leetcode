from collections import OrderedDict

class LRUCache:
    """
    Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.

    Implement the LRUCache class:

        LRUCache(int capacity) Initialize the LRU cache with positive size capacity.
        int get(int key) Return the value of the key if the key exists, otherwise return -1.
        void put(int key, int value) Update the value of the key if the key exists. 
            Otherwise, add the key-value pair to the cache. 
            If the number of keys exceeds the capacity from this operation, evict the least recently used key.

    The functions get and put must each run in O(1) average time complexity.
    """

    class Element():
        """
        A doubly-linked list element that also stores a value.
        Maintains references to the next and previous nodes in the list.
        """

        def __init__(self, key: int, value: int):
            self.key = key
            self.value = value
            self.prev: None | 'Element' = None
            self.next: None | 'Element' = None

    def __init__(self, capacity: int):
        """
        Task:
        - We are asked to implement an LRU cache in which up to `capacity` K, V pairs can be stored
        - When reading from the cache, we must return -1 if the element does not exist, else mark it as recently used
        - When writing to the cache, the element should be placed as "most recently used" and, if the cache is full,
          the oldest element can be removed
        
        Observations:
        - We need a list where we can store [least_recent_key, ..., most_recent_key] and update the order in O(1) runtime
        - The OrderedDict is the perfect data structure for this
          - It provides a doubly-linked-list implementation where we can easily track the order that elements have
            been added to or read from the cache
          - It provides an API for moving elements to the end of the ordered list, implying that they are the most recently
            used
          - It provides an API for removing elements from the front of the ordered list (the least recently used)
        - ... However, we may not be allowed to use an OrderedDict in an interview! So let's implement our own...
        - Logically, we need two components:
          - A hashmap to store K, V pairs (for O(1) lookup and update)
          - A linked list to keep ordering and enable easy O(1) "movement", popping, and pushing
        - How can we use the two together? 
          - Rather than storing just the value in the hashmap, we can store the linked list node, including its associated val
          - When we look up an item (get), we return just the value
          - When we insert an item (put), we create a new linked list node (if the key doesn't exist) with the value
        """
        self.capacity = capacity
        self.cache = dict()
        self.list = self.Element(0, 0) # a dummy root element to make traversing the list easier

    def get(self, key: int) -> int:
        if (element := self.cache.get(key)) is not None: # if the key exists, fetch the associated value
            self._move_to_end(element) # now we've "used" the key, so move it to the back of the list
            return element.value
        
        return -1 # the key doesn't exist, return -1
        

    def put(self, key: int, value: int) -> None:
        if not key in self.cache: # if key already exists in the cache, we should NOT evict as we do not need to create space
            while len(self.cache) >= self.capacity:
                _ = self._pop() # pop elements from the front of the list until we have 1 spot to insert
            
            element = self.Element(key, value)
            self.cache[key] = element
        else:
            element = self.cache[key]
            element.value = value

        self._move_to_end(element)

    def _pop(self) -> None:
        """
        Utility method to remove the least recently used element from the cache.
        """
        root = self.list

        # the store orders entries [LRU, ..., MRU]
        # so the element AFTER the root is the the least recently used, and the one BEFORE is the most
        popped_element = root.next

        # if the cache is empty (should never hit this code...), just exit safely
        if not popped_element:
            return
        
        # since we are removing the element after the root, we need to re-link the root
        after_popped = popped_element.next
        root.next = after_popped
        after_popped.prev = root

        # make sure we delete the key associated with this node from our cache
        self.cache.pop(popped_element.key)


    def _move_to_end(self, element: Element) -> None:
        """
        Utility method to move a node to the end of the linked list.
        """
        root = self.list

        # the element may or may not already be in the list
        # first, retrieve its previous and next elements, and connect them
        if previous := element.prev:
            previous.next = element.next
        if next := element.next:
            next.prev = element.prev
        
        # now, we have to place this node at the END of the list (just before the root!)
        mru_node = root.prev
        root.prev = element
        element.next = root

        if mru_node:
            # update the (now second) MRU node to point to the new element
            mru_node.next = element
            element.prev = mru_node
        else:
            # if the cache is empty, the new element is both the first and last element
            root.next = element
            element.prev = root
        


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)