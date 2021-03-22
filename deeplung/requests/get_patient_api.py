import requests
from requests.auth import HTTPBasicAuth
import pdb

username = 'pezz'
password = 'giulia'

base_url = 'http://127.0.0.1:8000/api/patients/'

slug = 'FThVfK'

#pdb.set_trace()
r = requests.get(base_url + slug + '/')
print(r)
patients = r.json()
print(patients)

