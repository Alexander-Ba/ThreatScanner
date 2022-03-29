
from menu_selection import MenuSelection
from modules_handlers.blacklists_handler import BlacklistsHandler
from modules_handlers.abuseipdb_handler import AbuseipdbHandler
from modules_handlers.open_ftp_handler import OpenFtpHandler
from modules_handlers.wordpress_handler import WordpressHandler
from modules_handlers.alexa_ranks_handler import AlexaRanksHandler
from templates import PrintTemplates


class Main:
    def __init__(
        self,
    ):
        self.templates = PrintTemplates()
        self.menu = MenuSelection()
        self.modules_indexer = {
            # 'Phishing': PhishingHandler, 
            # 'HTTPScan': HTTPScanHandler,
            'AbuseIPDB': AbuseipdbHandler,
            'OpenFTP': OpenFtpHandler,
            'Blacklists': BlacklistsHandler,
            'Wordpress': WordpressHandler,
            # 'VirusTracker': VirustrackerHandler,
            # 'Genesis': GenesisHandler,
            'AlexaRanks': AlexaRanksHandler,
        }
        print(self.templates.WELCOME)
        self.logs_path = self.menu.get_logs_path()

    def get_modules(self):
        active_modules_dict = self.menu.main()

        if 'ChangeLogsPath' in active_modules_dict.keys():
            self.logs_path = self.menu.get_logs_path()
            del active_modules_dict['ChangeLogsPath']
        if not active_modules_dict:
            return {}
        print(self.templates.ASSETS_INSERTION_TIP)
        for module_type in active_modules_dict.keys():
            active_modules_dict[module_type]['assets'] = self.menu.get_assets_by_module(
                module_type,
            )
        return active_modules_dict

    def handle_main_module(
        self,
        main_module,
        sub_modules,
        assets,
    ):
        final_result = {}
        for module in sub_modules:
            self.templates.print_service_start(module)
            handler = self.modules_indexer.get(module)
            handler = handler(            
                assets,
                file_path=self.logs_path,
                module=main_module,
            )
            result = handler.main()
            final_result[module] = result

        if main_module in self.modules_indexer.keys():
            self.templates.print_service_start(main_module)
            handler = self.modules_indexer.get(main_module)
            handler = handler(assets,file_path=self.logs_path)
            result = handler.main()
            final_result[main_module] = result
        return final_result

    def main(self):
        modules_dict = self.get_modules()
        for main_module, data in modules_dict.items():
            sub_modules = data.get('modules')
            assets = data.get('assets')
            assets = assets.replace(' ', '').split(',')
            self.handle_main_module(
                main_module,
                sub_modules,
                assets,
            )


ts = Main()
while True:
    ts.main()