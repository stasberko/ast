import requests
from random import randint
url = 'http://localhost:8000/things'

def test(n):
    with open('values', 'w') as f:
        for i in range(n):
            row = "{},{},{},{},{}\n".format(randint(1, 10000), randint(1, 10000000), randint(1, 10000),
                                            randint(1, 10000), randint(1, 10000), )
            f.write(row)
test(100)
params = dict(test=2, res=4)
data = open("values",).read()
headers = dict(device_id="0001", corid="0002")
for i in range(3):
    resp = requests.post(url=url, data=data, headers=headers)
    print(resp)
    pass

# resp.raise_for_status()
# print(resp.json())