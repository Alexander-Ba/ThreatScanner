import csv
from datetime import date
from templates import PrintTemplates
import os
import pandas as pd
from tld import get_fld
from formatters.ips_formatter import IPsFormatter
import urllib3
from formatters.url_formatter import UrlFormatter

urllib3.disable_warnings()


class MainHandler:
    def __init__(
        self,
        assets,
        file_path,
        module=None,
    ):
        self.assets = assets
        self.module = module
        self.file_path = file_path
        self.templates = PrintTemplates()
        self.user_agent = UrlFormatter.user_agent
        self.assets_type = self.get_asset_type()

    def main(self):
        raise TypeError(
            f'Unknown Module {self.module}'
        )

    def export(
        self,
        result_list,
        file_name,
    ):
        if not result_list:
            print(self.templates.NO_FINDINGS)
            return []
        if not isinstance(result_list, list):
            result_list = [result_list]
        file_path = f'{self.file_path}{file_name}.csv'
        if os.path.isfile(file_path):
            file = pd.read_csv(file_path, usecols=[0,1])
            old_results = file['results'].to_list()
            if isinstance(result_list[0], list):
                result_list = [
                    result for result in result_list if 
                    result[0] not in old_results
                ]
            else:
                result_list = [
                    result for result in result_list if 
                    result not in old_results
                ]
            self.templates.print_results_amount(len(result_list))
            if not result_list:
                return []
        else:
            with open(file_path, 'w') as f:
                writer = csv.writer(f)
                first_row = ['detection_date', 'results']
                writer.writerow(first_row)
        with open(file_path, 'a') as f:
            writer = csv.writer(f)
            for result in result_list:
                today = date.today().strftime("%d/%m/%Y")
                if isinstance(result,list):
                    log = [today] + result
                else:
                    log = [today,result]
                writer.writerow(log)
        self.templates.print_success_file_save(file_path)

    def get_asset_type(
        self,
    ):
        try:
            asset_example = self.assets[0]
            if get_fld('http://'+asset_example):
                assets_type = 'domains'
        except:
            assets_type = "ips"
        return assets_type
   
    def get_ips(
        self,
        segments,
    ):
        formatter = IPsFormatter()
        ips_list = []
        for segment in segments:
            ips_list += formatter.segment_to_ips(segment)
        return ips_list

    def is_alive(
        self,
        url,
    ):
        formatter = UrlFormatter()
        return formatter.is_alive(url)
    
    def get_domain(
        self,
        asset,
    ):
        formatter = UrlFormatter()
        return formatter.get_domain(asset)
