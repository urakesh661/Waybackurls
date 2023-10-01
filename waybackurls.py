import json
import argparse

import requests

parser = argparse.ArgumentParser()
parser.add_argument("--domain", "-d", help="Provide domain name here")
parser.add_argument("--limit", "-l", help="Number of records to be returned")
parser.add_argument("--extignore", "-i", nargs='+', default=[], help="File extensions to be removed from result")

args = parser.parse_args()

limit = args.limit
domain = args.domain
extIgnore = args.extignore


def wayback_data(domain):
    waybackUrl = (f"https://web.archive.org/web/timemap/json?url={domain}&matchType=prefix&collapse=urlkey&output=json"
                  f"&fl=original%2Cmimetype%2Ctimestamp%2Cendtimestamp%2Cgroupcount%2Cuniqcount&filter=!statuscode"
                  f"%3A%5B45%5D..&limit={limit}&_=1696139889950")

    response = requests.get(waybackUrl)
    data = response.json()
    dataDumps = json.dumps(data)
    getUrl = json.loads(dataDumps)
    waybackUrls = [waybackUrl[0] for waybackUrl in getUrl]
    waybackUrls.pop(0)
    waybackUrls = [ext for ext in waybackUrls if all(ignore not in ext for ignore in extIgnore)]

    for url in waybackUrls:
        try:
            urlResponse = requests.get(url)
            print(url, urlResponse.status_code)
        except requests.exceptions.ConnectionError as connErr:
            print("Connection Error", connErr)
        except requests.exceptions.Timeout as timeOut:
            print("Connection Error", timeOut)
        except requests.exceptions.InvalidURL as invalidUrl:
            print("Connection Error", invalidUrl)


wayback_data(domain)
