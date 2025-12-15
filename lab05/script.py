from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os
import json

spark = SparkSession.builder.master("local[*]").getOrCreate()

log_dir = "/content/sample_data/accounts/"

all_events = []
for root, dirs, files in os.walk(log_dir):
    for file in files:
        if file.endswith('.json'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                try:
                    data = json.loads(content)
                    if isinstance(data, list):
                        all_events.extend(data)
                    else:
                        all_events.append(data)
                except json.JSONDecodeError:
                    continue

all_events.sort(key=lambda x: x['ts'])

history_by_account = {}

for event in all_events:
    op = event['op']
    ts = event['ts']
    
    if op == 'c':
        new_record = event['data'].copy()
        new_record['ts'] = ts
        key = new_record.get('account_id')
        if key:
            if key not in history_by_account:
                history_by_account[key] = []
            history_by_account[key].append(new_record)
            
    elif op == 'u':
        updates = event['set']
        update_key = None
        if 'account_id' in updates:
            update_key = updates['account_id']
        else:
            continue 

        if update_key:
            if update_key not in history_by_account:
                history_by_account[update_key] = []

            if history_by_account[update_key]:
                last_state = history_by_account[update_key][-1].copy()
                last_state.update(updates)
                last_state['ts'] = ts
                history_by_account[update_key].append(last_state)
            else:
                continue

historical_rows = []
for key, states in history_by_account.items():
    historical_rows.extend(states)

historical_rows.sort(key=lambda x: x['ts'])

if historical_rows:
    from pyspark.sql import Row
    spark_rows = [Row(**item) for item in historical_rows]

    all_keys = set()
    for row in historical_rows:
        all_keys.update(row.keys())
    
    all_keys = sorted(list(all_keys))
    
    df = spark.createDataFrame(spark_rows)

    preferred_cols = ["ts", "account_id", "address", "email", "name", "phone_number", "card_id", "savings_account_id"]
    existing_preferred = [c for c in preferred_cols if c in df.columns]
    other_cols = [c for c in df.columns if c not in set(preferred_cols)]
    ordered_cols = existing_preferred + other_cols
    
    df = df.select(*ordered_cols)
    df.show(truncate=False)
else:
    print("No events found.")