# SEARCH.PY
# given query, finds first instance of that query in searchable.txt

import sys

def main():

  # check if a query was entered
  if len(sys.argv) >= 2:

      # get query from command line args
	  query = ""
	  for i in range(len(sys.argv)):
	    if i == 1:
	      query += sys.argv[1]
	    if i > 1:
	      query += " "
	      query += sys.argv[i]

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
  
  else:
  	print "You must submit a search query"

if __name__ == "__main__":
  main()