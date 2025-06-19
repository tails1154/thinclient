from mitmproxy import http
from tinydb import TinyDB, Query
from urllib.parse import urlparse, parse_qs

# Load TinyDB
db = TinyDB("db.json")
ssid_table = db.table("ssid")

def is_ssid_in_db(ssid):
    SSID = Query()
    return ssid_table.contains(SSID.ssid == ssid)

class SSIDAuth:
    def request(self, flow: http.HTTPFlow) -> None:
        # Parse query parameters
        parsed_url = urlparse(flow.request.pretty_url)
        query = parse_qs(parsed_url.query)
        ssid_list = query.get("ssid")

        if not ssid_list or not is_ssid_in_db(ssid_list[0]):
            flow.response = http.Response.make(
                403,  # Forbidden
                b"SSID not authorized or missing.",
                {"Content-Type": "text/plain"}
            )

addons = [
    SSIDAuth()
]
