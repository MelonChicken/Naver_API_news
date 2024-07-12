import urllib.request
import urllib.parse
import toml
import sys
import os

toml_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "res", "config.toml")
with open(toml_dir, "r") as f:
    config_toml = toml.load(f)

client_id = config_toml["CLIENT"]["ID"]
client_secret = config_toml["CLIENT"]["SECRET"]
search_keyword = urllib.parse.quote(config_toml["CLIENT"]["KEYWORD"], encoding="cp949")
base_url = config_toml["CLIENT"]["URL"]
node = config_toml["CLIENT"]["NODE"]
response_type = config_toml["CLIENT"]["RESPONSE_TYPE"]
display_count = config_toml["CLIENT"]["DISPLAY_COUNT"]
sort_criteria = config_toml["CLIENT"]["SORT_CRITERIA"]
url_query = f"{base_url}{node}.{response_type}?query={search_keyword}&display={display_count}&sort={sort_criteria}"


class Response:
    def __init__(self, raw_data, body, data_type, status_code):
        self.raw = raw_data
        self.body = body
        self.data_type = data_type
        self.status_code = status_code
        self.cooked_data = []


def get_response(url_query: str = url_query, client_id: str = client_id, client_secret: str = client_secret,
                 response_type: str = response_type) -> Response:
    request = urllib.request.Request(url_query)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    print(f"url_query: {url_query}")
    print(f"request: {request}")
    response = urllib.request.urlopen(request)
    resp_code = response.getcode()

    if resp_code != 200:
        sys.stdout.write("The response from {url_query} was not received correctly.  The Error Code is [{resp_code}].")
        resp_body = None
        result = Response(raw_data=response, body=resp_body, data_type=response_type, status_code=response.getcode())
    else:
        resp_body = response.read().decode("utf-8")
        result = Response(raw_data=response, body=resp_body, data_type=response_type, status_code=response.getcode())

    return result
