import requests
from requests.auth import HTTPBasicAuth
import pdb

username = 'pezz'
password = 'giulia'

base_url = 'http://127.0.0.1:8000/api/'

patient_data = {
    "name": "Joahnna",
    "surname": "Doe",
    "age": 99,
    "gender": 2,
    "race": 0
}

#path_ct = "/HDD/UBUNTU/database/COVID/ieee_CT/coronacases_005.nii.gz"
#case_data = {
#    "patient_slug": "CrrTwM",
#    "title": "example api case",
#    "annotations": "example annotation for John Doe"
#}
#files = {'ct': open(path_ct, 'rb')}

#pdb.set_trace()
#r = requests.get(base_url)
#print(r)
#patients = r.json()
#print(patients)

pr = requests.post(base_url + 'patients/post/', patient_data,
                   auth=HTTPBasicAuth('pezz', 'giulia'))

#cr = requests.post(base_url + 'cases/post/', case_data,
#                   auth=HTTPBasicAuth('pezz', 'giulia'), files=files)

#print(pr)
#new_patients = pr.json()
#print(patients)

