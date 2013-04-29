from data_reader import *
from neural_net import *
from neural_net_impl import *
import sys
import random

# get args from command line CAN WE JUST IMPORT THIS FROM MAIN?????
def parseArgs(args):
  """Parses arguments vector, looking for switches of the form -key {optional value}.
  For example:
    parseArgs([ 'erm.py', '-n', 'filename']) = { '-n':'filename' }"""
  args_map = {}
  curkey = None
  for i in xrange(1, len(args)):
    if args[i][0] == '-':
      args_map[args[i]] = True
      curkey = args[i]
    else:
      assert curkey
      args_map[curkey] = args[i]
      curkey = None
  return args_map

# detect if there's any black in the character
def has_zero(lst):
  for sub in lst:
    if 0 in sub:
      return True
  return False

# return what letter image is according to neural net
def neur_net(pixs):
  #tons of shit


def main():

  # Parsing command line arguments
  args_map = parseArgs(sys.argv)

  # filename is the name of the file being inputted
  filename = args_map['-n']

  # if we have the png file type
  if filename.find('.png') != -1 :

    # list of characters from preprocessing
    filething = ProcessedImage(filename, 12, 20)
    filething.output_txt("input_images.txt", "w")

    # get list of image data types
    imagelist = DataReader.GetImages("input_images.txt", -1)

    # make file contents one long string
    contents = ""
    for image in imagelist:
      assert len(image.pixels) == 20
      assert len(image.pixels[0]) == 20
      if has_zero(image.pixels):
        contents += neur_net(image.pixels)
      else:
        contents += " "
              
    # write contents out to file
    output_file = open('searchable.txt', "w")
    output_file.write(contents)
    output_file.close()

  # improper file type
  else
    print "Error: must be formatted as .png file"

  # Initializing network

  network = CustomNetwork()

  # Hooks user-implemented functions to network
  network.FeedForwardFn = FeedForward
  network.network.weights = DataReader.ReadWeights("weight_writeout.txt")


  # Initialize network weights
  # network.InitializeWeights()
  

if __name__ == "__main__":
  main()