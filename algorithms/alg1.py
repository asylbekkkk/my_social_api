def get_middle_unique(arr):
    n = len(arr)
    start = n // 3
    end = n - start
    
    left_part = arr[:start]
    middle_part = arr[start:end]
    right_part = arr[end:]
    
    print(f"1-ші бөлік: {left_part}")
    print(f"2-ші бөлік: {middle_part}")
    print(f"3-ші бөлік: {right_part}")
    
    counts = {}
    for x in middle_part:
        counts[x] = counts.get(x, 0) + 1
        
    return [x for x in middle_part if counts[x] == 1]

if __name__ == "__main__":
    my_array = [1, 2, 3, 4, 5, 5, 6, 7, 8,9]
    print(f"Массив: {my_array}")
    print(f"Нәтиже (уникалды ортасы): {get_middle_unique(my_array)}")