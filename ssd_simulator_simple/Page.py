class Page:
    def __init__(self):
        self.valid = False
        self.data = None

    def write(self, data):
        self.valid = True
        self.data = data

    def invalidate(self):
        self.valid = False

    def is_free(self):
        return self.data is None
    
    def __repr__(self):
        v = 'V' if self.valid else 'I'
        return f"{v} | {self.data}"
    

