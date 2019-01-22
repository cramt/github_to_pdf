import pdfkit

from indexing import indexing
from sampleData import sample, join

# get input from user
url = "https://github.com/" + input("the url for the github repo -> ")
ignores = input("list of ignores, separated by kommas -> ").split(",")
output_file_name = input("output file name -> ")


# this function takes all the indexes and joins them together
# \n is replaced since where is some weird but where there will be a bunch of "\n" in the final result otherwise
def sanitize_input_for_pdfkit(indexes):
    return join(sample(indexes)).replace("\\n", "")


# get the indexes
indexes = indexing(url, ignores)
# make pdfkit create a pdf
pdfkit.from_string(sanitize_input_for_pdfkit(indexes), output_file_name)
