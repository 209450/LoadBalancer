class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __eq__(self, other):
        return self.name == other.name and self.size == other.size

    def __str__(self):
        return f"{self.name}: {self.size}"