from collections import deque

def final_attempt():
    
    word_list = ["Stream", "Strean", "Stread", "Streak", "Strike", "Strime", "Streme", "Stmre", "Stripe"]
    
    extra_words = [
        "Strem",  
        "Stram",   
        "Strim",  
        "Strims",  
        "Strips",  
        "Strip",   
        "Stripe"  
    ]
    word_list.extend(extra_words)
    
    begin = "Stream".lower()
    end = "Stripe".lower()
    
    clean_set = set(w.strip().lower() for w in word_list)
    
    queue = deque([(begin, ["Stream"])])
    visited = {begin}
    
    while queue:
        curr, path = queue.popleft()
        
        if curr == end:
            return path
            
        for word in clean_set:
            if word not in visited:
                if len(curr) == len(word):
                    diff = sum(1 for a, b in zip(curr, word) if a != b)
                    if diff == 1:
                        visited.add(word)
                        queue.append((word, path + [word.capitalize()]))
                
                elif abs(len(curr) - len(word)) == 1:
                    longer, shorter = (curr, word) if len(curr) > len(word) else (word, curr)
                    for i in range(len(longer)):
                        if longer[:i] + longer[i+1:] == shorter:
                            visited.add(word)
                            queue.append((word, path + [word.capitalize()]))
                            break
    return None

path = final_attempt()
if path:
    print(f"Табылған жол ({len(path)-1} қадам):")
    print(" -> ".join(path))
else:
    print("Жол табылмады. Тізімді қайта тексеріңіз.")