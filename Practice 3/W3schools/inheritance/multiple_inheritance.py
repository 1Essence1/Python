class Flyer:
    def fly(self):
        print("Flying")

class Swimmer:
    def swim(self):
        print("Swimming")

class Duck(Flyer, Swimmer):
    # Duck inherits from both Flyer and Swimmer
    pass

donald = Duck()
donald.fly()   # Output: Flying
donald.swim()  # Output: Swimming
