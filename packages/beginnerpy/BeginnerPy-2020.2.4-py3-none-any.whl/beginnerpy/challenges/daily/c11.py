def collatz(n):
    return 1 if n == 1 else collatz(n / 2) + 1 if n % 2 == 0 else collatz(n * 3 + 1) + 1



assert collatz(3) == 8
assert collatz(7) == 17
assert collatz(17) == 13
assert collatz(42) == 9
assert collatz(33) == 27
print("Challenge 11, all tests passed!")
