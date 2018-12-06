from types import CoroutineType

from bs4 import BeautifulSoup
import asyncio

import http_request
from indexing import Index
import urllib.request


class SampleEntry:
    url: str
    data: str

    def __init__(self, url: str, data: str):
        self.url = url
        self.data = data


class CompleteSample:
    head: str
    samples: [SampleEntry]

    def __init__(self, head: str, samples: [SampleEntry]):
        self.samples = samples
        self.head = head


def getSample(indexes: [Index]) -> [SampleEntry]:
    re: [SampleEntry] = []
    for index in indexes:
        if index.type == "folder":
            for s in getSample(index.children):
                re.append(s)
        elif index.type == "file":
            i = str(urllib.request.urlopen(index.url).read())
            re.append(SampleEntry(index.url, i))
    return re


def sample(indexes: [Index]) -> CompleteSample:
    samples = getSample(indexes)

    print(len(samples))
    head = BeautifulSoup(samples[0].data, "html.parser").find("head")
    for i in range(0, len(samples)):
        soup = BeautifulSoup(samples[i].data, "html.parser")
        samples[i].data = soup.find("table", attrs={"class": "highlight tab-size js-file-line-container"})

        samples[i].url = "/blob/master/".join(samples[i].url.split("/blob/master/")[1:])
    return CompleteSample(head, samples)


def join(d: CompleteSample):
    s = "<!DOCTYPE html><html>"
    s += str(d.head)
    s += "<body>"
    for sample in d.samples:
        if str(type(sample)) != "<class 'NoneType'>":
            s += "<h1>" + str(sample.url) + "</h1>"
            s += str(sample.data)
    s += "</body></html>"
    return s
