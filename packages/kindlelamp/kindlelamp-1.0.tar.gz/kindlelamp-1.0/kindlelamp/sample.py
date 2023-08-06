from kindlelamp import kindlelamp
import json
from datetime import date

kindle_collction = kindlelamp.read()

dt = date.fromisoformat('2020-01-01')
dt2 = date.fromisoformat('2020-02-01')
result = kindle_collction.search(
    purchase_since=dt, purchase_until=dt2, title='プログラム')

print(result)

with open('sample.json', "w") as f:
    json.dump(result, f, default=lambda o: o.__dict__, ensure_ascii=False,
              indent=4, sort_keys=True, separators=(',', ': '))
