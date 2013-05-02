import sys

def main():

  # get query from command line args
  query = ""
  for i in range(len(sys.argv)):
    if i > 0:
      query += sys.argv[i]
      query += " "

  # get contents of searchable file
  search_file = open('searchable.txt', "r")
  contents = search_file.read()
  search_file.close()

  # make search case insensitive
  contents = contents.lower()
  query = query.lower()

  # print out the location of the query
  index = contents.find(query)
  if index >= 0:
  	print "Query found at position %d" % index
  else:
    print "Query not found"


if __name__ == "__main__":
  main()