# ERM.PY
# The overarching file to run our program
# takes in a .png file of a text document and outputs
# the text into searchable.txt
# inherits functions from CS181 pset

from data_reader import *
from neural_net import *
from neural_net_impl import *
from character_extraction import ProcessedImage
import sys
import random

# modification on datareader.getimages
def GetImagesMod(filename):
  images = []
  infile = open(filename, 'r')
  cur_row = 0
  image = None
  while True:
    line = infile.readline().strip()
    if not line:
      break
    if line.find('#') == 0:
      if image:
        images.append(image)
      image = Image(1)
    else:
      image.pixels.append([float(r) for r in line.strip().split()])
  if image:
    images.append(image)
  return images

# modification of neural_net_impl.FeedForward
def ClassifyMod(network, image):
  input = network.Convert(image)
  FeedForward(network.network, input)
  return network.GetNetworkLabel()

# detect if there's any black in the character
def has_zero(lst):
  for sub in lst:
    if 0 in sub:
      return True
  return False

def main():

  # have 1 argument which is a png file
  if len(sys.argv) == 2 and sys.argv[1].find('.png') != -1:

    # Initializing network
    network = CustomNetwork()
    wgts = DataReader.ReadWeights("weight_writeout_backup.txt")
    for i in range(len(wgts)):
      network.network.weights[i].value = wgts[i]

    # list of characters from preprocessing
    fileimg = ProcessedImage(sys.argv[1])
    resized = fileimg.resize_chars(20)
    fileimg.output_txt(resized, "input_images.txt", "w")

    # get list of image data types
    imagelist = GetImagesMod("input_images.txt")

    # array of letters; indeces corresponding to labels
    letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P',
               'Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f',
               'g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v',
               'w','x','y','z','.']
 
    # make file contents one long string
    contents = ""
    for image in imagelist:
      # check image is proper size; should never fail b/c preprocessed to 
      # be 20x20
      assert len(image.pixels) == 20
      assert len(image.pixels[0]) == 20
      # send to neural net if it's a letter, otherwise it's a space
      if has_zero(image.pixels):
        contents += letters[ClassifyMod(network, image)]
      else:
        contents += " "
              
    # write contents out to file
    output_file = open('searchable.txt', "w")
    output_file.write(contents)
    output_file.close()

  # improper file type or argument number
  else:
    print "Error: must pass one .png file"

  

if __name__ == "__main__":
  main()