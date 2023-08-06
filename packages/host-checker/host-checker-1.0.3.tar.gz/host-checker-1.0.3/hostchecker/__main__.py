import datetime
import chrome_bookmarks
import argparse
from hostingInfo import HostInfo
from hostStorage import HostStorage

def printInfoUrl(domain, hostStorage, useCache, storeOnCache):
    """
    Print the info for the given url

    :param domain: String of the damain to get the hosting info from
    :param hostStorage: HostStorage where to store the info
    :param useCache: True enable the loading of cached results
    :param storeOnCache: True enable the caching of the result
    """

    # Load info from cache
    hostInfo = None
    if useCache:
        hostInfo = hostStorage.getHostInfo(domain)
        time = "Loaded from cache"
    
    # Get info from the web
    if hostInfo is None:
        start = datetime.datetime.now()
        hostInfo = HostInfo.hostingInfo(domain)
        end = datetime.datetime.now()

        delta = end - start
        time = delta.total_seconds()

        # Store the result
        if storeOnCache:
            hostStorage.cache([hostInfo])

    print(f"{hostInfo.domain:40} {str(hostInfo.datacenter):40} {time:.02F}s")


def urls(args):
    if args.url is None:
        urls = set()
        for url in chrome_bookmarks.urls:
            domain = HostInfo.getDomain(url.url)
            urls.add(domain)
        return list(urls)
    else:
        return [args.url]




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check who is hosting websites")
    parser.add_argument('url', type=str, nargs='?',
        help="The URL to check (esample: 'www.google.com')")
    parser.add_argument('--bookmarks', action='store_true', default=True,
        help='Check the host of all bookmarks [default true]')
    parser.add_argument('--stats', action='store_true', default=False,
        help='Print the stats of the used website [default false]')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--no-cache', action='store_true', default=False,
        help='The cache will not be used to get and store the results [default false]')
    group.add_argument('--force-cache', action='store_true', default=False,
        help='The cached result will not be used [default false]')
    
    args = parser.parse_args()
    
    hostStorage = HostStorage("host_info.sqlite3")

    if args.stats:
        stats = hostStorage.stats()
        for s in stats:
            datacenter = "<Unknown>" if s.datacenter is None else s.datacenter
            print(f"{datacenter:40} {s.count:02} {s.percentage:05.1%}")
    else:
        useCache = not (args.force_cache or args.no_cache)
        storeOnCache = not args.no_cache

        domains = urls(args)
        for d in domains:
            printInfoUrl(d, hostStorage, useCache, storeOnCache)