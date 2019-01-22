import urllib.request

from bs4 import BeautifulSoup

from indexing import Index


# represents a single file
class SampleEntry:
    # url
    url: str
    # the data inside the file
    data: str

    def __init__(self, url: str, data: str):
        self.url = url
        self.data = data


# represents many files and a head, that head html for what kind of css there is
class CompleteSample:
    # the head as a string
    head: str
    # list of SampleEntry as the files
    samples: [SampleEntry]

    def __init__(self, head: str, samples: [SampleEntry]):
        self.samples = samples
        self.head = head


# creates a bunch of samples based on indexes
def getSample(indexes: [Index]) -> [SampleEntry]:
    # list of samples
    re: [SampleEntry] = []
    # iterates over indexes
    for index in indexes:
        # if folder do this recursively to the folders children
        if index.type == "folder":
            for s in getSample(index.children):
                re.append(s)
        elif index.type == "file":
            # if file just get the raw data, create a SampleEntry and add it to the list
            i = str(urllib.request.urlopen(index.url).read())
            re.append(SampleEntry(index.url, i))
    # return the list
    return re


# creates a CompleteSample based on a bunch of indexes
def sample(indexes: [Index]) -> CompleteSample:
    # find all the samples with the get sample function
    samples = getSample(indexes)
    # find the head tag of the first sample
    head = BeautifulSoup(samples[0].data, "html.parser").find("head")
    # iterate over the samples
    for i in range(0, len(samples)):
        # parse the html
        soup = BeautifulSoup(samples[i].data, "html.parser")
        # override the data property with tag of the html where the tag is table and the class is "highlight tab-size js-file-line-container"
        samples[i].data = soup.find("table", attrs={"class": "highlight tab-size js-file-line-container"})
        # remove the part of the url contain stuff like blob and github
        samples[i].url = "/blob/master/".join(samples[i].url.split("/blob/master/")[1:])
    # return a new CompleteSample of the head and the cleaned samples
    return CompleteSample(head, samples)


# creates one long string based on the CompleteSample
def join(d: CompleteSample):
    # create variable for holding the string and add the starting tags, like doctype and html
    s = "<!DOCTYPE html><html>"
    # add the head
    s += str(d.head)
    # start the body
    s += "<body>"
    # iterate over the samples
    for sample in d.samples:
        # ignore if null
        if str(type(sample)) != "<class 'NoneType'>":
            # create a header with the url/path of the sample
            s += "<h1>" + str(sample.url) + "</h1>"
            # add the actual html formatted code of the sample
            s += str(sample.data)
    # add end tags for body and html
    s += "</body></html>"
    # return the string
    return s
