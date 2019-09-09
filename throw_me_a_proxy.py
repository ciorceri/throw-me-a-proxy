import re
import urllib.request


def proxy_list_from_free_proxy_list_net():
    """
    will connect to https://free-proxy-list.net/
    and will get the proxy list from that page
    proxy format : ip address, port
    """

    link = 'https://free-proxy-list.net/'
    regex = '<td>(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})<\/td><td>(?P<port>\d{1,5})<\/td>'

    req = urllib.request.Request(link)
    req.add_header('User-Agent', 'Mozilla/5.0')
    content = urllib.request.urlopen(req).read().decode('ascii')

    res = re.findall(regex, content)
    return res


def validate_proxy(ip, port):
    """
    use a google page to validate that proxy works
    we check only it it's a http proxy
    return: True/False if the proxy is working
    """
    link = 'http://www.google.com/humans.txt'
    response = b"Google is built by a large team of engineers, designers, researchers, robots, and others in many different sites across the globe. It is updated continuously, and built with more tools and technologies than we can shake a stick at. If you'd like to help us out, see careers.google.com.\n"

    proxy_handler = urllib.request.ProxyHandler({'http': 'http://{}:{}/'.format(ip, port)})
    opener = urllib.request.build_opener(proxy_handler)
    try:
        res = opener.open(link, timeout=2)
        if res.read() == response:
            return True
    except Exception as e:
        pass
    return False


proxy_list = proxy_list_from_free_proxy_list_net()
for ip, port in proxy_list:
    res = validate_proxy(ip, port)
    if res:
        print(' + {}:{}'.format(ip, port))
    else:
        print(' - {}:{}'.format(ip, port))
