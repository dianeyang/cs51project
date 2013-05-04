# NEURAL_NET_MAIN.PY
# The main function for training the neural network
# includes functions for getting command line arguments and calling 
# training function properly
# largely taken from CS181 pset, with some alterations by us

from data_reader import *
from neural_net import *
from neural_net_impl import *
import sys
import random

# get epochs, learning rate from command line arguments
def parseArgs(args):
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

# make sure arguments are given properly
def validateInput(args):
  args_map = parseArgs(args)
  assert '-e' in args_map, \
    "A number of epochs should be specified with the flag -e (ex: -e 10)"
  assert '-r' in args_map, \
    "A learning rate should be specified with the flag -r (ex: -r 0.1)"
  return(args_map)

def main():

  # Parsing command line arguments
  args_map = validateInput(sys.argv)
  epochs = int(args_map['-e'])
  rate = float(args_map['-r'])

  # Load in the training set
  images = DataReader.GetImages('../data/training.txt', -1)
  for image in images:
    assert len(image.pixels) == 20
    assert len(image.pixels[0]) == 20

  # Load the validation set.
  validation = DataReader.GetImages('../data/validation.txt', -1)
  for image in validation:
    assert len(image.pixels) == 20
    assert len(image.pixels[0]) == 20

  # Initializing network
  network = CustomNetwork()
  network.InitializeWeights()

  # Hooks user-implemented functions to network
  network.FeedForwardFn = FeedForward
  network.TrainFn = Train
  
  # Displays training information
  print '* * * * * * * * *'
  print 'Parameters => Epochs: %d, Learning Rate: %f' % (epochs, rate)
  print 'Type of network used: %s' % network.__class__.__name__
  print ('Input Nodes: %d, Hidden Nodes: %d, Output Nodes: %d' %
         (len(network.network.inputs), len(network.network.hidden_nodes),
          len(network.network.outputs)))
  print '* * * * * * * * *'
  # Train the network.
  network.Train(images, validation, rate, epochs)

  # Outputing trained weights to files
  DataReader.DumpWeights(network.network.weights, "weight_writeout.txt")

if __name__ == "__main__":
  main()
