class Counter:
    def __init__(self):
        self.count = 0
    
    def count_one(self):
        self.count += 1

    def get_count(self):
        return self.count
    
    def clear(self):
        self.count = 0