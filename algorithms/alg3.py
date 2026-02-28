from datetime import datetime, timedelta
from collections import defaultdict
transactions = [
    {"user_id": 7, "amount": 640, "timestamp": "2026-01-08 12:23"},
    {"user_id": 2, "amount": 55, "timestamp": "2026-01-01 09:47"},
    {"user_id": 11, "amount": 520, "timestamp": "2026-01-03 16:19"},
    {"user_id": 4, "amount": 95, "timestamp": "2026-01-04 08:56"},
    {"user_id": 1, "amount": 120, "timestamp": "2026-01-02 09:41"},
    {"user_id": 9, "amount": 950, "timestamp": "2026-01-10 14:03"},
    {"user_id": 6, "amount": 70, "timestamp": "2026-01-01 10:37"},
    {"user_id": 12, "amount": 210, "timestamp": "2026-01-04 13:48"},
    {"user_id": 5, "amount": 400, "timestamp": "2026-01-02 11:52"},
    {"user_id": 3, "amount": 300, "timestamp": "2026-01-02 15:19"},
    {"user_id": 8, "amount": 160, "timestamp": "2026-01-05 09:33"},
    {"user_id": 10, "amount": 65, "timestamp": "2026-01-04 08:17"},
    {"user_id": 1, "amount": 150, "timestamp": "2026-01-03 10:29"},
    {"user_id": 7, "amount": 660, "timestamp": "2026-01-10 12:47"},
    {"user_id": 2, "amount": 60, "timestamp": "2026-01-01 09:53"},
    {"user_id": 11, "amount": 540, "timestamp": "2026-01-05 16:41"},
    {"user_id": 9, "amount": 980, "timestamp": "2026-01-15 14:56"},
    {"user_id": 6, "amount": 75, "timestamp": "2026-01-03 10:11"},
    {"user_id": 12, "amount": 220, "timestamp": "2026-01-06 13:07"},
    {"user_id": 4, "amount": 100, "timestamp": "2026-01-05 08:14"},
    {"user_id": 3, "amount": 320, "timestamp": "2026-01-05 16:52"},
    {"user_id": 5, "amount": 420, "timestamp": "2026-01-05 11:03"},
    {"user_id": 8, "amount": 165, "timestamp": "2026-01-06 09:58"},
    {"user_id": 10, "amount": 70, "timestamp": "2026-01-06 08:44"},
    {"user_id": 1, "amount": 180, "timestamp": "2026-01-05 11:47"},
    {"user_id": 7, "amount": 680, "timestamp": "2026-01-12 12:19"},
    {"user_id": 2, "amount": 70, "timestamp": "2026-01-04 13:31"},
    {"user_id": 11, "amount": 560, "timestamp": "2026-01-07 16:08"},
    {"user_id": 9, "amount": 1100, "timestamp": "2026-01-20 14:37"},
    {"user_id": 6, "amount": 80, "timestamp": "2026-01-05 10:59"},
    {"user_id": 12, "amount": 230, "timestamp": "2026-01-08 13:26"},
    {"user_id": 4, "amount": 105, "timestamp": "2026-01-06 08:39"},
    {"user_id": 3, "amount": 2000, "timestamp": "2026-01-08 09:03"},
    {"user_id": 5, "amount": 2500, "timestamp": "2026-01-10 11:18"},
    {"user_id": 8, "amount": 170, "timestamp": "2026-01-07 09:11"},
    {"user_id": 10, "amount": 75, "timestamp": "2026-01-08 08:53"},
    {"user_id": 1, "amount": 1100, "timestamp": "2026-01-10 14:02"},
    {"user_id": 7, "amount": 700, "timestamp": "2026-01-14 12:05"},
    {"user_id": 2, "amount": 500, "timestamp": "2026-01-12 18:44"},
    {"user_id": 11, "amount": 580, "timestamp": "2026-01-09 16:27"},
    {"user_id": 6, "amount": 85, "timestamp": "2026-01-07 10:06"},
    {"user_id": 12, "amount": 240, "timestamp": "2026-01-10 13:59"},
    {"user_id": 4, "amount": 110, "timestamp": "2026-01-07 08:21"},
    {"user_id": 3, "amount": 350, "timestamp": "2026-01-15 10:42"},
    {"user_id": 5, "amount": 460, "timestamp": "2026-01-15 11:39"},
    {"user_id": 8, "amount": 175, "timestamp": "2026-01-08 09:02"},
    {"user_id": 10, "amount": 80, "timestamp": "2026-01-10 08:36"},
    {"user_id": 9, "amount": 1200, "timestamp": "2026-01-20 14:41"},
    {"user_id": 1, "amount": 1300, "timestamp": "2026-01-10 14:07"},
    {"user_id": 11, "amount": 600, "timestamp": "2026-01-11 16:55"},
    {"user_id": 6, "amount": 90, "timestamp": "2026-01-09 10:48"},
    {"user_id": 12, "amount": 250, "timestamp": "2026-01-12 13:34"},
    {"user_id": 4, "amount": 115, "timestamp": "2026-01-08 08:02"},
    {"user_id": 3, "amount": 360, "timestamp": "2026-01-22 11:17"},
    {"user_id": 5, "amount": 470, "timestamp": "2026-02-02 11:09"},
    {"user_id": 8, "amount": 180, "timestamp": "2026-01-09 09:46"},
    {"user_id": 10, "amount": 85, "timestamp": "2026-01-12 08:12"},
    {"user_id": 9, "amount": 1050, "timestamp": "2026-02-03 14:58"},
    {"user_id": 7, "amount": 3000, "timestamp": "2026-02-05 13:49"},
    {"user_id": 11, "amount": 2000, "timestamp": "2026-02-06 17:03"},
    {"user_id": 6, "amount": 95, "timestamp": "2026-01-11 10:27"},
    {"user_id": 12, "amount": 260, "timestamp": "2026-02-07 14:11"},
    {"user_id": 4, "amount": 120, "timestamp": "2026-01-09 09:57"},
    {"user_id": 3, "amount": 380, "timestamp": "2026-02-01 12:08"},
    {"user_id": 6, "amount": 100, "timestamp": "2026-01-13 11:43"},
    {"user_id": 10, "amount": 90, "timestamp": "2026-01-14 08:29"}
]

def analyze_transactions(data):
    for t in data:
        if isinstance(t['timestamp'], str):
            t['timestamp'] = datetime.strptime(t['timestamp'], "%Y-%m-%d %H:%M")
    
    data.sort(key=lambda x: x['timestamp'])

    user_data = defaultdict(list)
    for t in data:
        user_data[t['user_id']].append(t['amount'])
    
    averages = {uid: sum(amts)/len(amts) for uid, amts in user_data.items()}

    suspicious = []

    for i, curr in enumerate(data):
        reasons = []
        uid = curr['user_id']
        amt = curr['amount']
        time = curr['timestamp']

        if amt > 1000:
            reasons.append(f"Үлкен сома: {amt}")

        count_in_10m = 0
        for j in range(i - 1, -1, -1):
            prev = data[j]
            if prev['user_id'] == uid:
                if time - prev['timestamp'] <= timedelta(minutes=10):
                    count_in_10m += 1
                else:
                    break
        
        if count_in_10m >= 1:
            reasons.append(f"Жиі транзакция (10 минутта {count_in_10m + 1} рет)")
        if amt > (averages[uid] * 2):
            reasons.append(f"Орташадан 2 есе көп (Орташа: {averages[uid]:.1f})")

        if reasons:
            suspicious.append({"info": curr, "reasons": reasons})

    return suspicious

findings = analyze_transactions(transactions)

print(f"Табылған күдікті жағдайлар: {len(findings)}\n")
for f in findings:
    t = f['info']
    print(f"UserID: {t['user_id']} | Сома: {t['amount']} | Уақыт: {t['timestamp']}")
    for r in f['reasons']:
        print(f"  -> {r}")
    print("-" * 40)