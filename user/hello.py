def factoriel(num: int):
    if num == 1:
        return 1
    return num * factoriel(num-1)
print('Hello world!')
print(factoriel(6))