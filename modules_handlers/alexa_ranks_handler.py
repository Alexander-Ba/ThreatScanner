from modules_handlers.main_handler import MainHandler
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup as BS
import re

class AlexaRanksHandler(MainHandler):
    def main(self):
        final_result = {}
        domains = set()
        for asset in self.assets:
            asset_domain = self.get_domain(asset)
            domains.add(asset_domain)
            final_result[asset] = {
                'asset': asset,
                'domain': asset_domain,
            }
        ranks_dict = self.multithread(domains, self.get_rank)
        pages_status = self.multithread(
            self.assets, 
            self.is_asset_website_alive
        )
        for asset, data in final_result.items():
            data['rank'] = ranks_dict.get(data['domain'])
            data['is_alive'] = pages_status.get(asset)

        result_list_for_export = [
            [d for d in data.values()] for 
            data in final_result.values()
        ]
        result_list_for_export = self.export(result_list_for_export, file_name=f'alexa_ranks_{self.assets_type}')
        return final_result

    def multithread(
        self,
        assets_list,
        function,
    ):
        with ThreadPoolExecutor(max_workers=200) as executor:
            futures, result = [], {}
            for asset in assets_list:
                futures.append(executor.submit(function, asset))
            for future in as_completed(futures):
                result.update(future.result())
        return result

    def get_rank(
        self,
        domain,
    ):
        url = f'https://www.alexa.com/siteinfo/{domain}'
        resp = requests.get(
            url,
            headers=self.user_agent,
        )
        soup = BS(resp.text, 'html.parser')
        rank_global = soup.select_one(".rank-global")
        if not rank_global:
            return {domain: None} 
        p = rank_global.select_one("p.data")
        data = str(p.text)
        rank = re.sub('[^0-9]', '', data)
        return {domain: rank}

    def is_asset_website_alive(
        self,
        asset,
    ):
        urls = [
            f'https://{asset}',
            f'http://{asset}',
        ]
        for url in urls:
            if self.is_alive(url):
                return {asset: 'Alive'}
        return {asset: 'Dead'}
