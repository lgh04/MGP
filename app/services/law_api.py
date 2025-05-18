import requests

API_KEY = "4fbf8cf2552c4074ac220162a6f1731c"
HEADERS = {"Content-Type": "application/json"}

def fetch_law_proposals(p_index=1, p_size=100):
    url = "https://open.assembly.go.kr/portal/openapi/nzmimeepazxkubdpn"
    params = {
        "KEY": API_KEY,
        "Type": "json",
        "pIndex": p_index,
        "pSize": p_size,
    }
    response = requests.get(url, params=params, headers=HEADERS)
    return response.json()

def fetch_law_details(p_index=1, p_size=100):
    url = "https://open.assembly.go.kr/portal/openapi/TVBPMBILL11"
    params = {
        "KEY": API_KEY,
        "Type": "json",
        "pIndex": p_index,
        "pSize": p_size,
    }
    response = requests.get(url, params=params, headers=HEADERS)
    return response.json()