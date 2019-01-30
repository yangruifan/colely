from datetime import datetime, timedelta
d = datetime.now()
d2 = d - timedelta(days=365)
print(type(d2))
print(d2)
print(d)
