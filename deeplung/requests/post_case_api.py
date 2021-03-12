import requests
from requests.auth import HTTPBasicAuth
import pdb

username = 'pezz'
password = 'giulia'

base_url = 'http://127.0.0.1:8000/api/'

path_ct = "/HDD/UBUNTU/database/COVID/ieee_CT/coronacases_005.nii.gz"
case_data = {
    "patient_slug": "CrrTwM",
    "title": "example api case",
    "annotations": "example annotation for John Doe"
}
files = {'ct': open(path_ct, 'rb')}

cr = requests.post(base_url + 'cases/post/', case_data,
                   auth=HTTPBasicAuth('pezz', 'giulia'), files=files)
