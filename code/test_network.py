# TEST_NETWORK.PY
# runs the trained neural netowrk over our testing set
# inherits functions from CS181 pset

from data_reader import *
from neural_net import *
from neural_net_impl import *
from character_extraction import ProcessedImage
from erm import *
import sys
import random

def main():
  
  # initialize network
  network = CustomNetwork()
  wgts = DataReader.ReadWeights("weight_writeout_backup.txt")
  for i in range(len(wgts)):
    network.network.weights[i].value = wgts[i]

  # initialize performance calculator
  correct = 0.0
  total = 0.0

  # get testing images
  images = DataReader.GetImages('../data/testing.txt', -1)
  for image in images:
    assert len(image.pixels) == 20
    assert len(image.pixels[0]) == 20
    if ClassifyMod(network, image) == image.label:
    	correct += 1.0

    total += 1.0


  print correct/total


if __name__ == "__main__":
  main()