import requests
from tld import get_fld




class UrlFormatter:
    user_agent = {
            'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        }

    def __init__(self):
        pass

    def is_alive(
        self,
        url,
    ):
        try:
            resp = requests.get(url, headers = self.user_agent, verify=False, timeout=10)
            if resp.status_code == 200:
                return True
        except:
            return

    def get_domain(
        self,
        asset,
    ):
        asset = asset.lower()
        if not asset.startswith('http'):
            asset = f'http://{asset}'
        return get_fld(asset, fail_silently=True)
