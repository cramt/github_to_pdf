import json
import urllib.request
from bs4 import BeautifulSoup

import http_request


class Index:
    name: str
    url: str
    type: str
    fullName: str
    children = []

    def __init__(self, td):
        self.name = str(td.text)
        url = str(td["href"])
        self.url = "https://github.com" + url
        a = "/master/"
        self.fullName = a.join(str(x) for x in self.url.split(a)[1:])
        split_url = url.split("/")
        try:
            if split_url[0] == "" and split_url[4] == "master":
                if split_url[3] == "blob":
                    self.type = "file"
                elif split_url[3] == "tree":
                    self.type = "folder"
                else:
                    self.type = "undefined"
                    raise ValueError("not blob or tree")
        except Exception as e:
            print("type error: " + str(e))


def get(url: str) -> BeautifulSoup:
    content = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(content, "html.parser")
    return soup


def indexing(url: str, ignores: [str]) -> [Index]:
    index: [Index] = []
    soup = get(url)
    print(url)

    content = list(soup.find_all("td", attrs={"class": "content"}))[1:]

    for child in content:
        c = child.find("a")
        if str(type(c)) != "<class 'NoneType'>":
            i = Index(c)
            if i.name not in ignores:
                if i.type == "folder":
                    i.children = indexing(i.url, [])
                index.append(i)
    return index
