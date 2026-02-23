class Reverse:
    def __init__(self, data):
        self.data = data
        self.index = len(data) - 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < 0:
            raise StopIteration
        result = self.data[self.index]
        self.index -= 1
        return result

s = input()
r = Reverse(s)

for char in r:
    print(char, end='')