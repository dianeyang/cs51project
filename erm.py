from data_reader import *
from neural_net import *
from neural_net_impl import *
from character_extraction import * 
import sys
import random

class ImageMod:
  def __init__(self):
    self.pixels = []

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
        image = ImageMod()
      else:
        image.pixels.append([float(r) for r in line.strip().split()])
    if image:
      images.append(image)
    return images

def FeedForwardMod(network, input):
  vect = []
  for i in range(len(input.values)):
    network.inputs[i].raw_value = input.values[i] 
    network.inputs[i].transformed_value = input.values[i]
  for hidden in network.hidden_nodes:
    hidden.raw_value = network.ComputeRawValue(hidden)
    hidden.transformed_value = network.Sigmoid(hidden.raw_value)
  for out in network.outputs:
    out.raw_value = network.ComputeRawValue(out)
    out.transformed_value = network.Sigmoid(out.raw_value)
    vect.append(out.transformed_value)
  return vect 

# detect if there's any black in the character
def has_zero(lst):
  for sub in lst:
    if 0 in sub:
      return True
  return False


# return what letter image is according to neural net
def neur_net(network, pixs):

  # run through feedforward so returns vector of values
  output_vec = FeedForwardMod(network, pixs)
  
  # find max value in list and letter that corresponds to
  letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
  return letters[output_vec.index(max(output_vec))]


def main():

  # have 1 argument which is a png file
  if len(sys.argv) == 2 and sys.argv[1].find('.png') != -1:

    # Initializing network... somehow... below is probs wrong !!!!!!!!!!!!
    # do we need to do .value somewhere for weights?
    network = CustomNetwork()
    network.network.weights = DataReader.ReadWeights("weight_writeout_backup.txt")

    # list of characters from preprocessing
    fileimg = ProcessedImage(sys.argv[1], 20)
    fileimg.output_txt("input_images.txt", "w")

    # get list of image data types
    imagelist = GetImagesMod("input_images.txt")

    # make file contents one long string
    contents = ""
    for image in imagelist:
      # check image is proper size; should never fail b/c preprocessed to be 20x20
      assert len(image.pixels) == 20
      assert len(image.pixels[0]) == 20
      # send to neural net if it's a letter, otherwise it's a space
      if has_zero(image.pixels):
        contents += neur_net(network, image.pixels)
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