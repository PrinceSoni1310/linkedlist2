# Linked List Classes
# Extracted linked list implementations for better code organization

class Node:
    """Basic node class for linked lists"""
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None  # For doubly linked list

class SinglyLinkedList:
    """Singly linked list implementation"""
    def __init__(self):
        self.head = None
        self.size = 0

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1

    def insert_at_index(self, data, index):
        if index < 0 or index > self.size:
            return False
        if index == 0:
            self.insert_at_beginning(data)
            return True
        new_node = Node(data)
        current = self.head
        for i in range(index - 1):
            if current is None:
                return False
            current = current.next
        new_node.next = current.next
        current.next = new_node
        self.size += 1
        return True

    def delete_from_beginning(self):
        if self.head is None:
            return None
        deleted_data = self.head.data
        self.head = self.head.next
        self.size -= 1
        return deleted_data

    def delete_from_end(self):
        if self.head is None:
            return None
        if self.head.next is None:
            deleted_data = self.head.data
            self.head = None
            self.size -= 1
            return deleted_data
        current = self.head
        while current.next.next:
            current = current.next
        deleted_data = current.next.data
        current.next = None
        self.size -= 1
        return deleted_data

    def delete_by_value(self, value):
        if self.head is None:
            return False
        if self.head.data == value:
            self.head = self.head.next
            self.size -= 1
            return True
        current = self.head
        while current.next and current.next.data != value:
            current = current.next
        if current.next:
            current.next = current.next.next
            self.size -= 1
            return True
        return False

    def search(self, value):
        current = self.head
        position = 0
        while current:
            if current.data == value:
                return position
            current = current.next
            position += 1
        return -1

    def traverse(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements

class DoublyLinkedList:
    """Doubly linked list implementation"""
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def insert_at_beginning(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def insert_at_index(self, data, index):
        if index < 0 or index > self.size:
            return False
        if index == 0:
            self.insert_at_beginning(data)
            return True
        if index == self.size:
            self.insert_at_end(data)
            return True
        new_node = Node(data)
        current = self.head
        for i in range(index):
            current = current.next
        new_node.prev = current.prev
        new_node.next = current
        current.prev.next = new_node
        current.prev = new_node
        self.size += 1
        return True

    def delete_from_beginning(self):
        if self.head is None:
            return None
        deleted_data = self.head.data
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        self.size -= 1
        return deleted_data

    def delete_from_end(self):
        if self.tail is None:
            return None
        deleted_data = self.tail.data
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
        self.size -= 1
        return deleted_data

    def delete_by_value(self, value):
        current = self.head
        while current:
            if current.data == value:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                self.size -= 1
                return True
            current = current.next
        return False

    def search(self, value):
        current = self.head
        position = 0
        while current:
            if current.data == value:
                return position
            current = current.next
            position += 1
        return -1

    def traverse_forward(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements

    def traverse_backward(self):
        elements = []
        current = self.tail
        while current:
            elements.append(current.data)
            current = current.prev
        return elements

class CircularLinkedList:
    """Circular linked list implementation"""
    def __init__(self):
        self.head = None
        self.size = 0

    def insert_at_beginning(self, data):
        new_node = Node(data)
        if self.head is None:
            new_node.next = new_node
            self.head = new_node
        else:
            new_node.next = self.head
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = new_node
            self.head = new_node
        self.size += 1

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            new_node.next = new_node
            self.head = new_node
        else:
            new_node.next = self.head
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = new_node
        self.size += 1

    def insert_at_index(self, data, index):
        if index < 0 or index > self.size:
            return False
        if index == 0:
            self.insert_at_beginning(data)
            return True
        new_node = Node(data)
        current = self.head
        for i in range(index - 1):
            current = current.next
            if current == self.head:
                return False
        new_node.next = current.next
        current.next = new_node
        self.size += 1
        return True

    def delete_from_beginning(self):
        if self.head is None:
            return None
        deleted_data = self.head.data
        if self.head.next == self.head:
            self.head = None
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = self.head.next
            self.head = self.head.next
        self.size -= 1
        return deleted_data

    def delete_from_end(self):
        if self.head is None:
            return None
        deleted_data = self.head.data
        if self.head.next == self.head:
            self.head = None
        else:
            current = self.head
            while current.next.next != self.head:
                current = current.next
            deleted_data = current.next.data
            current.next = self.head
        self.size -= 1
        return deleted_data

    def delete_by_value(self, value):
        if self.head is None:
            return False
        if self.head.data == value:
            if self.head.next == self.head:
                self.head = None
            else:
                current = self.head
                while current.next != self.head:
                    current = current.next
                current.next = self.head.next
                self.head = self.head.next
            self.size -= 1
            return True
        current = self.head
        while current.next != self.head and current.next.data != value:
            current = current.next
        if current.next != self.head:
            current.next = current.next.next
            self.size -= 1
            return True
        return False

    def search(self, value):
        if self.head is None:
            return -1
        current = self.head
        position = 0
        while True:
            if current.data == value:
                return position
            current = current.next
            position += 1
            if current == self.head or position >= self.size:
                break
        return -1

    def traverse(self, max_elements=None):
        if self.head is None:
            return []
        elements = []
        current = self.head
        count = 0
        while current and (max_elements is None or count < max_elements):
            elements.append(current.data)
            current = current.next
            count += 1
            if current == self.head:
                break
        return elements
