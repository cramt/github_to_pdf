import urllib.request
from bs4 import BeautifulSoup
import pdfkit

from indexing import indexing
import json

from sampleData import sample, join

url = "https://github.com/cramt/angler"
ignores = ["gradle/wrapper", ".idea"]

indexes = indexing(url, ignores)
# s = urllib.request.urlopen("https://github.com/cramt/angler/blob/master/app/build.gradle").read()
pdfkit.from_string(join(sample(indexes)).replace("\\n", ""), "out.pdf")

