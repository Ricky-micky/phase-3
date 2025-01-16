class Author:
    def __init__(self, id, name):
        self._id = id  
        self._name = name  

    # Returning the stored id
    @property
    def id(self):
        return self._id  

    # Returning the stored name
    @property
    def name(self):
        return self._name  

    def __repr__(self):
        return f'<Author {self.name}>'


# Testing the class and printing
author1 = Author(1, "Alice Smith")
print(author1)


