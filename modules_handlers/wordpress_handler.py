from modules_handlers.main_handler import MainHandler
import requests
from requests.exceptions import RequestException
from concurrent.futures import ThreadPoolExecutor, as_completed


class WordpressHandler(MainHandler):
    def main(self):
        if self.assets_type == 'ips':
            self.assets = self.get_ips(self.assets)
        with ThreadPoolExecutor(max_workers=200) as executor:
            futures, results = [], []
            for asset in self.assets:
                futures.append(executor.submit(self.get_exploitable_urls, asset))
            for future in as_completed(futures):
                results += future.result()
        result = self.export(results, file_name=f'wordpress_vulnerabilities_{self.assets_type}')
        return result

        
    def get_exploitable_urls(
        self,
        asset,
    ):
        base_url = f'https://{asset}'
        result = []
        for exploit_url in self.templates.WORDPRESS_EXPLOITS.get('json'):
            url = base_url + exploit_url
            resp = self.get_response(url)
            if self.is_json(resp):
                result.append(url)
                self.templates.print_results(url)
        for exploit_url in self.templates.WORDPRESS_EXPLOITS.get('file_directories'):
            url = base_url + exploit_url
            resp = self.get_response(url)
            if self.response_contains_text(
                resp, 
                'parent directory',
            ):
                result.append(url)
                self.templates.print_results(url)
        for exploit_url in self.templates.WORDPRESS_EXPLOITS.get('other'):
            url = base_url + exploit_url
            resp = self.get_response(url)
            if self.response_contains_text(
                resp, 
                ['wordpress', 'index of'],
            ):
                result.append(url)
                self.templates.print_results(url)
        return result
            

    def response_contains_text(
        self,
        response,
        keywords,
    ):
        if not response:
            return
        response_text = response.text.lower()
        if not isinstance(keywords, list):
            keywords = [keywords]
        for keyword in keywords:
            if keyword in response_text:
                return True    
            
    def is_json(
        self,
        response,
    ):
        if not response:
            return
        try:
            response.json()
            return True
        except:
            return

    def get_response(
        self,
        url,
    ):
        try:
            response = requests.get(
                url, 
                headers=self.user_agent, 
                verify=False, 
                timeout=10,
            )
        except RequestException:
            return
        if response.status_code != 200:
            return
        return response


