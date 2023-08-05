from requests import Session
from requests.auth import HTTPBasicAuth


class Medialoopster(object):
    def __init__(self, url, user=None, password=None):
        self.session = Session()
        self.session.verify = False

        if user and password:
            self.session.auth = HTTPBasicAuth(user, password)

        self.url = url

    def __enter__(self):
        """Enable context management."""
        return self

    def __exit__(self, *args):
        """Clean up."""
        self.close()

    def ping(self):
        r = self.session.get(self.url + "ping/")
        r.raise_for_status()

        return True

    def asset_import(self, production=None, type=None, move_asset=False, name=None, description=None, approval=0,
                     path_file=None, meta_field_store={}):
        request = {
            "production": production,
            "type": type,
            "move_asset": move_asset,
            "asset": {
                "asset_meta": {
                    "name": name,
                    "description": description,
                    "approval": approval,
                    "path_file": path_file,
                    "meta_field_store": meta_field_store
                }
            }
        }

        response = self.session.post(self.url + "asset/import/", json=request).json()

        return response.get('asset_import_id', None)

    def get_url(self, type="videoassets"):
        try:
            r = self.session.get(url=self.url)
            return r.json().get(type, None)
        except ConnectionError:
            return None

    def get_productions(self):
        return self.get_from_api(type="productions")

    def get_meta_field_store(self, type="videoassets"):
        for i in self.get_from_api(type=type):
            yield i.get("meta_field_store")

    def get_from_api(self, type="videoassets", url=None):
        if not url:
            url = self.get_url(type=type)

        while url:
            try:
                r = self.session.get(url=url)
            except ConnectionError:
                continue

            if r.links:
                url = r.links.get("next", {}).get("url", None)
            else:
                url = None

            for i in r.json():
                yield i

    def get_asset(self, asset_id, type="videoassets"):
        url = f"{self.get_url(type=type)}{asset_id}?with_sequences=true"

        r = self.session.get(url=url)
        r.raise_for_status()

        return r.json()

    # TODO
    def search_meta_field_store(self, field: str, value: str, type: str = "videoassets"):
        for field, value in self.get_meta_field_store():
            print(f"{field} - {value}")