from modules_handlers.main_handler import MainHandler
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException


class BlacklistsHandler(MainHandler):
    def main(self):
        result = self.get_blacklisted_ips(self.assets)
        result = self.export(result, file_name='blacklisted_ips')
        return result

    def get_blacklisted_ips(
        self,
        assets,
    ):
        ip_list = self.get_ips(assets)
        request_url = "https://www.bulkblacklist.com/"
        try:
            resp = requests.post(request_url, files={
                'ips': (None, '\n'.join(ip_list)),
            })
        except RequestException as e:
            print(
                'Error in Blacklists Source\n'
                'Service Stopped'
                f'{e}',
                )
            return []
        soup = BeautifulSoup(resp.text, 'html.parser')
        rows_with_ips = soup.find_all('tr')
        rows_with_ips.pop(0)
        blacklisted_ips = []
        for row in rows_with_ips:
            ip = row.find_all('td')[1].text
            if 'r.png' in str(row):
                blacklisted_ips.append(ip)
        self.templates.print_results(
            blacklisted_ips,
            'Blacklisted IPs',
        )
        return blacklisted_ips

