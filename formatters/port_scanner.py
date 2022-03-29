import nmap


class PortScanner:
    def get_port_protocol(
        self,
        asset,
        port,
    ):
        scanner = nmap.PortScanner()
        scan_result = scanner.scan(asset, port, '--open')['scan']
        if not scan_result:
            return
        result = []
        for ip, data in scan_result.items():
            port_result = data['tcp'].get(int(port))
            protocol = port_result.get('name')
            result.append({
               'ip': ip,
               'protocol': protocol, 
            })
        return result

