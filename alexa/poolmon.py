import requests

class poolmon:
    @staticmethod
    def request(endpoint, params={}):
        if not poolmon.api_url:
            raise Exception('You must configure an API URL')
        
        headers = {'x-api-key': poolmon.api_key}
        resp = requests.get(poolmon.api_url+endpoint, params=params, headers=headers)
        
        if resp.status_code == 200:
            return resp.json()
        else:
            raise Exception(resp.json()['message'], resp.status_code)
