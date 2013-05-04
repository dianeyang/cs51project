from neural_net import NeuralNetwork, NetworkFramework
from neural_net import Node, Target, Input, Weight
from data_reader import *
import random

# run input through network
def FeedForward(network, input):

  network.CheckComplete()

  # set input values
  for i in range(len(input.values)):
    network.inputs[i].raw_value = input.values[i] 
    network.inputs[i].transformed_value = input.values[i]
  # push to hidden layer
  for hidden in network.hidden_nodes:
    hidden.raw_value = network.ComputeRawValue(hidden)
    hidden.transformed_value = network.Sigmoid(hidden.raw_value)
  # push to output
  for out in network.outputs:
    out.raw_value = network.ComputeRawValue(out)
    out.transformed_value = network.Sigmoid(out.raw_value)


# run input through network and adjust weights accordingly
def Backprop(network, input, target, learning_rate):
  network.CheckComplete()
  
  # run input through network
  FeedForward (network,input)

  # calculate error, delta, and epsilon values for each node
  for i in range(len(network.outputs)):
    err = target[i] - network.outputs[i].transformed_value
    network.outputs[i].delta = network.SigmoidPrime(network.outputs[i].raw_value) * err
  for node in network.hidden_nodes: 
    eps = 0
    for j in range(len(node.forward_neighbors)):
      eps += node.forward_weights[j].value * node.forward_neighbors[j].delta
    node.delta = network.SigmoidPrime(node.raw_value) * eps

  # update hidden layer weights 
  for hid in network.hidden_nodes:
    change = learning_rate * hid.transformed_value 
    for j in range(len(hid.forward_weights)):
      hid.forward_weights[j].value += change * hid.forward_neighbors[j].delta

  # update input layer weights
  for inp in network.inputs:
    change = learning_rate * inp.transformed_value 
    for j in range(len(inp.forward_weights)):
      inp.forward_weights[j].value += change * inp.forward_neighbors[j].delta

# trains neural network
def Train(network, inputs, targets, learning_rate, epochs):  
  network.CheckComplete()
  for i in range(epochs): 
    for j in range(len(inputs)):
      Backprop(network, inputs[j], targets[j], learning_rate)
  

class EncodedNetworkFramework(NetworkFramework):
  def __init__(self):
    super(EncodedNetworkFramework, self).__init__() # < Don't remove this line >
    
  # gives correct label to training/validation sets
  def EncodeLabel(self, label):
    l = [0.0] * 53
    l[label] = 1.0
    return l

  # returns label best fitting output
  def GetNetworkLabel(self):
    outputs = []
    for out in self.network.outputs:
      outputs.append(out.transformed_value)
    return outputs.index(max(outputs))

  # turns an image into an input vector of normalized pixel values
  def Convert(self, image):
    outer = []
    for i in image.pixels:
      for j in i: 
        outer.append(j/256.0)
    inp = Input()
    inp.values = outer
    return inp

  # randomize weights to begin training
  def InitializeWeights(self):
    #for wgt in self.network.weights:
    #  wgt.value = random.uniform(-0.01, 0.01)
    wgts = DataReader.ReadWeights("weight_writeout_backup.txt")
    for i in range(len(wgts)):
      self.network.weights[i].value = wgts[i]


#network setup: 400 inputs, 60 hidden, 53 ouput nodes
class CustomNetwork(EncodedNetworkFramework):
  def __init__(self):
    super(CustomNetwork, self).__init__() # <Don't remove this line>
        
    for i in range(400):
      self.network.AddNode((Node()), NeuralNetwork.INPUT)
    for j in range(60):
      self.network.AddNode((Node()), NeuralNetwork.HIDDEN)
    for k in range(53):
      self.network.AddNode((Node()), NeuralNetwork.OUTPUT)
    for output in self.network.outputs:
      for hid in self.network.hidden_nodes:
        output.AddInput(hid, None, self.network)
    for hid in self.network.hidden_nodes:
      for inp in self.network.inputs:
        hid.AddInput(inp, None, self.network)
