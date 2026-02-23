import math

def prime_generator(n):
    for num in range(2, n + 1):
        if num < 2:
            continue
        is_prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            yield num

n = int(input())
p = prime_generator(n)
print(*(p))