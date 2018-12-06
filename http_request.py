import urllib.request


async def http_request(url: str) -> urllib.request:
    return urllib.request.urlopen(url)
