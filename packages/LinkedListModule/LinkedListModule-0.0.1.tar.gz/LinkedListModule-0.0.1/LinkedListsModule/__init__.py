#* The node class
class Node(object):

    #* Constructor
    def __init__(self, data):
        self.data = data
        self.nextNode = None


#* The LL class
class LinkedList(object):

    #* Constructor
    def __init__(self):
        self.head = None
        self.size = 0

    #* Insert data at start
    def insertStart(self, data):
        self.size += 1
        newNode = Node(data)    
        #? Is the list empty
        if not self.head:
            self.head = newNode #* New node is the first if LL is empty
        else:
            #* Making the new node the first and the head
            newNode.nextNode = self.head #* Old head = next node of current head
            self.head = newNode
    
    #* Returning the size easily O(1)
    def sizeGet(self):
        return self.size
    
    #* Function to insert a node at the end O(N)
    def insertEnd(self, data):
        self.size += 1
        newNode = Node(data)
        currentNode = self.head
        #* Traversing
        while currentNode.nextNode is not None:
            currentNode = currentNode.nextNode #* Changing the node
        #* Setting the last node
        currentNode.nextNode = newNode
    
    #* Function ot traverse the list
    def traverseList(self):
        currentNode = self.head
        while currentNode is not None:
            print(f"{currentNode.data}")
            currentNode = currentNode.nextNode #* Changing the node
    
    #* Function to remove
    def remove(self, data):
        #? Is LL empty
        if self.head is None:
            return
        #* Decrementing the size
        self.size -= 1
        #* The head and previous node
        currentNode = self.head
        prevNode = None
        #? Is this the data we are looking for
        while currentNode.data != data:
            prevNode = currentNode #* Changing the previous node
            currentNode = currentNode.nextNode #* Changing the node
        #* Updating the references
        if prevNode is None: #* Dealing with the head
            self.head = currentNode.nextNode
        else:
            prevNode.nextNode = currentNode.nextNode #* Changing the reference to point at the node after the one we want to delete