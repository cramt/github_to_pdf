import pdfkit

from indexing import indexing
from sampleData import sample, join

url = "https://github.com/" + input("the url for the github repo -> ")
ignores = input("list of ignores, separated by kommas -> ").split(",")
output_file_name = input("output file name -> ")


def sanitize_input_for_pdfkit(indexes):
    return join(sample(indexes)).replace("\\n", "")


indexes = indexing(url, ignores)
pdfkit.from_string(sanitize_input_for_pdfkit(indexes), output_file_name)
