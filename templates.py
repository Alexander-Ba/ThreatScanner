from contextlib import redirect_stderr
from simple_colors import *


class PrintTemplates:
    WELCOME = """
        _____  _______________________ ____________
       /  _/ |/ /_  __/ __/  _/ ___/ // /_  __/ __/
     _/ //    / / / _\ \_/ // (_ / _  / / / _\ \  
    /___/_/|_/ /_/ /___/___/\___/_//_/ /_/ /___/  

                AUTOMATED THREAT DETECTOR 
                By SB @ Lima Team
"""+yellow("Usage Manual",'bold')+""" can be found here: """+blue("https://bit.ly/3hxxwga","bold")+"""



v2.2 (17/03/2022) - 
"""+green("IP's:",'bold')+"""
hetrixtools.com, abuseipdb.com, virustracker.net, servers open to FTP requests, exploits for wordpress. 
"""+green("Domains:",'bold')+"""
abuseipdb.com, genesis.market, domains open for FTP requests, exploits for wordpress, bulk alexa.com ranks checker, check if domain is alive..
"""+yellow('Works perfect with AMASS results.','bold')+""" 
"""+green("Phishing:",'bold')+""" Scan for keywords in top phishing websites databases.  
Detect """+green("active HTTP pages",'bold')+""" on multiple ports in-between the assets (Including filters for kewords such as admin, login and control panel).

"""+yellow("**TIP:",'bold')+""" The code works really hard for you and frequently needs some time to finish. It is not crashing, just leave it to work and come back later for results.
"""+yellow("**TIP:",'bold')+""" The code is extremely friendly for Intsights Analysts. (Copy from IMP and paste straight to the code, Grab files to the code rather than write files path)
"""+yellow("**TIP:",'bold')+""" Open the terminal in a known folder, besides of the output in the Terminal, The code is generating CSV files with the results in the Terminal location, pay attention to the code comments.
"""+yellow("**TIP:",'bold')+""" For domains scan, prepare a file with subdomains from AMASS tool for maximum effectivity.
(Syntax: amass enum -d example1.com,example2.com,example3.com -brute > DesiredFileToSaveIn.txt)


    """

    ASSETS_INSERTION_TIP = 'Assets can be provided as:'\
        ' '+yellow('Raw Data','bold')+' e.g: <'+yellow('185.146.8.1,192.146.8.0/24','bold')+'>'\
        ', <'+yellow('isracard.co.il,google.com','bold')+'>\n'\
        'OR '+yellow('File Path','bold')+' e.g:'\
        ' '+yellow('/home/user/Desktop/client/File.txt','bold')

    ASSETS_EXAMPLES = {
        'IPs': '185.146.8.1,192.146.8.0/24',
        'Domains': 'isracard.co.il,google.com',
    }
    MAIN_MENU = {
        '1': 'IPs',
        '2': 'Domains',
        '3': 'Phishing',
        '4': 'HTTPScan',
        '0': 'ChangeLogsPath',
    }

    FILE_EXPORT_REQUEST = 'Please choose a file export path'
    SUB_MENU = {
        'IPs': {
            '1': 'AbuseIPDB',
            '2': 'OpenFTP',
            '3': 'Wordpress',
            '4': 'Blacklists',
            '5': 'VirusTracker',
        },
        'Domains': {
            '1': 'AbuseIPDB',
            '2': 'OpenFTP',
            '3': 'Wordpress',
            '4': 'Genesis',
            '5': 'AlexaRanks',
        },
        'Phishing': {},
        'HTTPScan': {},
    }
    ABUSEIPDB_DETECTORS = [
        "not found",
        "No IP addresses",
        "We can't resolve the domain",
    ]

    WORDPRESS_EXPLOITS = {
        'json': [
            '/wp-json/wp/v2/users',
        ],
        'file_directories': [
            '/wp-admin/images',
            '/wp-includes',
            '/wp-content/uploads',
            '/wp-content/plugins',
        ],
        'other': [
            '/wp-login.php',
            '/wp-register.php',
            '/wp-admin/',
            "/author-sitemap.xml",
            "/wp-admin/setup-config.php?step=1",
        ]
    }

    NO_FINDINGS = red('No New Detections','bold')+' found, finishing module task..'

    def print_service_start(
        self,
        service,
    ):
        print('Starting service: '+blue(service,'bold'))

    def build_options_menu(
        self,
        options_dict,
        higher_level_module,
    ):
        result = f'Please choose the '+red(higher_level_module,'bold')+' modules:\n'
        for key, value in options_dict.items():
            result += f'    {key}. For {value} use '+blue(key,'bold')+'\n'

        return result

    def build_assets_menu(
        self,
        module,
    ):

        result = f'Please '+green('INSERT','bold')+' desired '+red(module,'bold')+' assets for the search..\n'
        return result

    def print_results(
        self,
        results,
        service=None,
    ):
        if not results:
            return 
        if not isinstance(results,list):
            print(green(results,'bold'))
            return 
        print(f'Results for '+blue(service,'bold'))
        for result in results:
            print(green(result,'bold'))

    def print_results_amount(self, results_amount):
        if results_amount == 0:
            color = red
        else:
            color = green
        print('Detected '+color(results_amount,'bold')+f' new results')

    def print_success_file_save(self, file):
        print('Successfully '+green('updated','bold')+f' file <{file}>')

    def print_error(
        self,
        service,
        asset,
    ):
        print(green('Error','bold')+f' on module {service} with {asset}')