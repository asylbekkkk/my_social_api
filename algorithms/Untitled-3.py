def get_middle_unique(arr):
    n = len(arr)
    # 3-ке бөлу (бүтін санмен бөлу)
    start = n // 3
    end = n - start
    
    # Ортаңғы бөлікті қиып алу
    middle_part = arr[start:end]
    
    # Сандардың қанша рет кездесетінін санау
    counts = {}
    for x in middle_part:
        counts[x] = counts.get(x, 0) + 1
        
    # Тек 1 рет кездескен сандарды қайтару
    return [x for x in middle_part if counts[x] == 1]

if __name__ == "__main__":
    # Массивті бөлу есебін тексеру
    my_array = [1, 2, 3, 4, 5, 5, 6, 7, 8, 9]
    print(f"Массив: {my_array}")
    print(f"Ортаңғы бөлік: {get_middle_unique(my_array)}")