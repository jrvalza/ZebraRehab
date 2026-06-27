
import requests

class Api_osm:
    def __init__(self, region):
        self.region = region
        self.response = []

    def get_crosswalks(self):

        if self.region:
            lat_min, lon_min, lat_max, lon_max = self.region

            query = f"""
            [out:json];
            node["highway"="crossing"]({lat_min},{lon_min},{lat_max},{lon_max});
            out body;
            """

            headers = {
                "User-Agent": "ZebraRehab/1.0",
                "Accept": "application/json"
            }

            url = "https://overpass-api.de/api/interpreter"

            response = requests.get(
                url,
                params={"data": query},
                headers=headers,
                timeout=30
            )

            response.raise_for_status()
            self.response = response.json()

        else:
            self.response = {"elements": []}

        return self.response