import random
import sys

sys.setrecursionlimit(2000)

def simulate_draws(n, target_digit, count_hits=0, current_step=0):
    if current_step == n:
        return count_hits
    
    ball = random.randint(1, 100)
    
    print(f"{ball}", end=", " if (current_step + 1) % 20 != 0 else "\n")

    has_digit = str(target_digit) in str(ball)
    
    return simulate_draws(n, target_digit, count_hits + int(has_digit), current_step + 1)

TRIALS = 1000
TARGET = 3

print(f"{TRIALS} рет алынған сандар тізімі:\n")
hits = simulate_draws(TRIALS, TARGET)
print(" "*30)

probability = hits / TRIALS

print(f"1000 реттен {hits} рет '3' цифры бар сан түсті.")
print(f"Нақты (эксперименттік) ықтималдық: {probability}")