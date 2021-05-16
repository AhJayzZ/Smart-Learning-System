import requests
from requests.exceptions import HTTPError

base_url = "https://api.github.com"
#base_url = "https://dictionary.cambridge.org/dictionary/english-chinese-traditional"

response = requests.get(base_url)

print(response)

for url in ['https://api.github.com', 'https://api.github.com/invalid']:
    try:
        response = requests.get(url)

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')

response.encoding = 'utf-8'  # Optional: requests infers this internally
# print(response.content)
# print(response.text)
# print(response.headers)
response.headers['Content-Type']
response.json()
