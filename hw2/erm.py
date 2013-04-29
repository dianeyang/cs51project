from data_reader import *
from neural_net import *
from neural_net_impl import *
import sys
import random


# intake file

# send it through character extraction

# create output file

# loop over output file
# if it's a space, then append ' ' else run through network




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


def zero(lst):
  for sub in lst:
    if 0 in sub:
      return True
  return False

# def validateInput(args):
#   args_map = parseArgs(args)
#   assert '-e' in args_map, "A number of epochs should be specified with the flag -e (ex: -e 10)"
#   assert '-r' in args_map, "A learning rate should be specified with the flag -r (ex: -r 0.1)"
#   assert '-t' in args_map, "A network type should be provided. Options are: simple | hidden | custom"
#   return(args_map)

def main():

  # Parsing command line arguments
  args_map = parseArgs(sys.argv)

  # filename is the name of the file being inputted
  filename = args_map['-n']

  if filename.find('.png') != -1 :

    # filething is the Processed image of filename
    filething = ProcessedImage(filename, 12, 20)

    # filetxt is the output text file of filething
    filetxt = filething.output_txt("derp.txt", "w")
    imagelist = DataReader.GetImages(filetxt, -1)
    file = open('searchableshit.txt', "w")
    for image in images:
      if zero(image.pixels):
        #neural net
      else:
        # print out space

      



  else
    print "Why are you not giving me a png file. Are you fucking stupid?"

  # # Load in the training data.
  # images = DataReader.GetImages('training.txt', -1)
  # for image in images:
  #   assert len(image.pixels) == 20
  #   assert len(image.pixels[0]) == 20

  # Initializing network

  network = CustomNetwork()

  # Hooks user-implemented functions to network
  network.FeedForwardFn = FeedForward
  network.network.weights = DataReader.ReadWeights("weight_writeout.txt")


  # Initialize network weights
  # network.InitializeWeights()
  

  # Displays information
  # print '* * * * * * * * *'
  # print 'Parameters => Epochs: %d, Learning Rate: %f' % (epochs, rate)
  # print 'Type of network used: %s' % network.__class__.__name__
  # print ('Input Nodes: %d, Hidden Nodes: %d, Output Nodes: %d' %
  #        (len(network.network.inputs), len(network.network.hidden_nodes),
  #         len(network.network.outputs)))
  # print '* * * * * * * * *'
  # Train the network.
  # network.Train(images, validation, rate, epochs)

  # Outputing trained weights to files
  # DataReader.DumpWeights(network.network.weights, "weight_writeout.txt")

if __name__ == "__main__":
  main()