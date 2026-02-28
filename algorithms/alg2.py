data = [
    [1, 3, 4, 7, 8],
    [2, 4, 5, 6, 8, 9],
    [2, 6, 4],
    [9, 7, 5, 8, 5, 6, 7]
]
prefix_table = []
for row in data:
    p = [0]
    current_sum = 0
    for x in row:
        current_sum += x
        p.append(current_sum)
    prefix_table.append(p)

try:
    l = int(input("l мәнін енгізіңіз: "))
    r = int(input("r мәнін енгізіңіз: "))
except ValueError:
    print("Тек сандарды енгізіңіз!")
    exit()

print(f"\nНәтижелер ({l} мен {r} аралығы):")

total_sum = 0
for i, p_row in enumerate(prefix_table):
    n = len(p_row) - 1 
    
    actual_r = min(r, n)
    actual_l = min(l - 1, n)
    
    if actual_l < actual_r:
        row_sum = p_row[actual_r] - p_row[actual_l]
    else:
        row_sum = 0
        
    print(f"{i+1}-ші жол қосындысы: {row_sum}")
    total_sum += row_sum

#print("-" * 25)
#print(f"Барлық жолдардың жалпы қосындысы: {total_sum}")