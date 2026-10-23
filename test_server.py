import requests
BASE='http://127.0.0.1:8080/demo'
r=requests.post(BASE,json={'value':'hello'},timeout=10); assert r.status_code==200,r.text
r=requests.get(BASE,timeout=10); assert r.status_code==200 and r.json()['value']=='hello',r.text
r=requests.delete(BASE,timeout=10); assert r.status_code==200,r.text
r=requests.get(BASE,timeout=10); assert r.status_code==404,r.text
print('PUT, GET, DELETE, and missing-key checks passed')
