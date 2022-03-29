from netaddr import IPNetwork

class IPsFormatter:
    def segment_to_ips(
        self,
        segment,
    ):
        result = []
        for ip in IPNetwork(segment):
            result.append(str(ip))
        return result