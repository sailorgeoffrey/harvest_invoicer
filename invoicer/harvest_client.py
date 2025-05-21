import json

import requests


class HarvestClient:

    def __init__(self, account_id, api_key):
        self.account_id = account_id
        self.api_key = api_key

    def fetch_report(self, start, end):
        resp = requests.get(
            url="https://api.harvestapp.com/v2/reports/time/clients",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Harvest-Account-Id": self.account_id,
                "User-Agent": "Invoicer (geoffc@gmail.com)",
                "Authorization": "Bearer " + self.api_key,
            },
            params={
                "from": start.strftime("%Y%m%d"),
                "to": end.strftime("%Y%m%d"),
            }
        )
        if resp.status_code != 200:
            print(resp.text)
            exit(1)
        return json.loads(resp.text)["results"]
