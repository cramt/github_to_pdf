import json
import urllib.request
from bs4 import BeautifulSoup

import http_request


# class for a specific index
# an index in this context is a file or folder
class Index:
    # name decribes the name of the index
    name: str
    # the url for the index
    url: str
    # is it a file or folder
    type: str
    # the full name or the path of the index
    fullName: str
    # if it is a folder what is its children
    children = []

    # td is the td html tag that holds the info about the tag
    def __init__(self, td):
        # the name is equal to the text in the tag
        self.name = str(td.text)
        # the url is equal to the href property
        url = str(td["href"])
        self.url = "https://github.com" + url
        # all indexes' path starts after "/master/"
        a = "/master/"
        # get the fullname after the "/master/"
        self.fullName = a.join(str(x) for x in self.url.split(a)[1:])
        # create and array based on all the parts of the url
        split_url = url.split("/")
        try:
            if split_url[0] == "" and split_url[4] == "master":
                if split_url[3] == "blob":
                    # if the third element in the url is blob its a file
                    self.type = "file"
                elif split_url[3] == "tree":
                    # if the third element in the url is folder its a folder
                    self.type = "folder"
                else:
                    # if neither folder or file make error
                    self.type = "undefined"
                    raise ValueError("not blob or tree")
        except Exception as e:
            print("type error: " + str(e))


# function for http request and parse with beautiful soup
def get(url: str) -> BeautifulSoup:
    content = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(content, "html.parser")
    return soup


# function for indexes all files, it will create a structure of index objects that is either a file or folder and the folders then have children that are also indexes and so on
def indexing(url: str, ignores: [str]) -> [Index]:
    # make array for keeping the indexes
    index: [Index] = []
    # get the main stuff
    soup = get(url)

    # get the list of elements containing information for indexes
    # ignore the first cause its not useful and it crashes things
    content = list(soup.find_all("td", attrs={"class": "content"}))[1:]

    # loop thought it, and ignore it if its null
    # add stuff the array, call this function recursively if there is a folder
    for child in content:
        c = child.find("a")
        if str(type(c)) != "<class 'NoneType'>":
            i = Index(c)
            if i.name not in ignores:
                if i.type == "folder":
                    i.children = indexing(i.url, [])
                index.append(i)
    # return the array of indexes
    return index
