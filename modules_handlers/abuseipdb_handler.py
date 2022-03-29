from modules_handlers.main_handler import MainHandler
import requests
from requests.exceptions import RequestException
import time

class AbuseipdbHandler(MainHandler):
    def main(self):
        self.request_url = "https://www.abuseipdb.com/check/?query="
        result = []
        for asset in self.assets:
            if self.is_abused(asset):
                result.append(asset)
                self.templates.print_results(asset)
        result = self.export(result, file_name=f'abuseipdb_{self.assets_type}')
        return result

    def get_response(
        self,
        asset,
    ):
        sleep_time = 5
        for _ in range(5):
            try:
                resp = requests.get(
                    self.request_url+asset,
                    headers=self.user_agent,
                    timeout=10,
                )
            except RequestException as e:
                self.templates.print_error(
                    service='AbuseIPDB',
                    asset=asset,
                )
                return 
            if resp.status_code != 200:
                time.sleep(sleep_time)
                sleep_time += sleep_time
                continue
            return resp

    def is_abused(
        self,
        asset,
    ):
        response = self.get_response(asset)
        if not response:
            return False
        if any(
            string in response.text for 
            string in self.templates.ABUSEIPDB_DETECTORS   
        ):
            return False
        return True
