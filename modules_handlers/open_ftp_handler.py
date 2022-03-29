from modules_handlers.main_handler import MainHandler
from formatters.port_scanner import PortScanner
from concurrent.futures import ThreadPoolExecutor, as_completed

class OpenFtpHandler(MainHandler):
    def main(self):
        with ThreadPoolExecutor(max_workers=200) as executor:
            futures, results = [], []
            for asset in self.assets:
                futures.append(executor.submit(self.scan, asset))
            for future in as_completed(futures):
                results += future.result()
        result = self.export(results, file_name=f'open_ftp_{self.assets_type}')
        return result

    def scan(
        self,
        asset,
    ):
        scanner = PortScanner()
        results = []
        scan_results = scanner.get_port_protocol(
            asset=asset,
            port='21',
        )
        if not scan_results:
            return []
        for result in scan_results:
            if self.assets_type == 'ips':
                ip = result.get('ip')
                ftp_link = f'ftp://{ip}'
            else:
                ftp_link = f'ftp://{asset}'
            results.append(ftp_link)
            self.templates.print_results(ftp_link)
        return results
