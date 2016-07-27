import requests, re, datetime

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
            print resp.text
            raise Exception(resp.json()['message'], resp.status_code)
    
    @staticmethod
    def parse_date(date):
        min_date = max_date = date_type = None
        
        try:
            if re.match('^[0-9]{4}$', date):
                min_date = datetime.datetime(int(date), 1, 1)
                max_date = datetime.datetime(int(date), 12, 31, 23, 59)
                date_type = 'year'
            
            match = re.match('^([0-9]{4})(-)?W([0-9]{2})$', date)
            if match and not min_date:
                formatted = match.group(1)+'-W'+match.group(3)
                min_date = datetime.datetime.combine(datetime.datetime.strptime(formatted+'-1', "%Y-W%W-%w"), datetime.time(0, 0))
                max_date = datetime.datetime.combine(datetime.datetime.strptime(formatted+'-0', "%Y-W%W-%w"), datetime.time(23, 59, 59))
                date_type = 'week'
            
            match = re.match('^([0-9]{4})(-)?W([0-9]{2})(-)?([0-9]{1})$', date)
            if match and not min_date:
                formatted = match.group(1)+'-W'+match.group(3)+'-'+match.group(5)
                min_date = datetime.datetime.combine(datetime.datetime.strptime(formatted, "%Y-W%W-%w"), datetime.time(0, 0, 0))
                max_date = datetime.datetime.combine(datetime.datetime.strptime(formatted, "%Y-W%W-%w"), datetime.time(23, 59, 59))
                date_type = 'day'
            
            match = re.match('^([0-9]{4})(-)?([0-9]{2})(-)?([0-9]{2})$', date)
            if match and not min_date:
                formatted = match.group(1)+'-'+match.group(3)+'-'+match.group(5)
                min_date = datetime.datetime.combine(datetime.datetime.strptime(formatted, "%Y-%m-%d"), datetime.time(0, 0, 0))
                max_date = datetime.datetime.combine(datetime.datetime.strptime(formatted, "%Y-%m-%d"), datetime.time(23, 59, 59))
                date_type = 'day'
        except ValueError:
            min_date = max_date = date_type = None
        
        return min_date, max_date, date_type
