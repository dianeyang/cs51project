from neuralnet import NeuralNetwork, NetworkFramework
from neuralnet import Node, Target, Input
import random

def FeedForward(network, input):

  network.CheckComplete()

  # 1) Assign input values to input nodes
  for i in input:
    network.inputs[i].raw_value = input[i]
  for i in network.inputs: 
    network.inputs[i].transformed_value = network.inputs[i].raw_value

  # 2) Propagates to hidden layer
  for i in range(len(network.hidden_nodes)):
      network.hidden_nodes[i].raw_value = network.ComputeRawValue(network.hidden_nodes[i])
      network.hidden_nodes[i].transformed_value = network.Sigmoid(network.hidden_nodes[i].raw_value)

  # 3) Propagates to the output layer   
  for i in range(len(network.outputs)):
    network.outputs[i].raw_value = network.ComputeRawValue(network.outputs[i])
  

def Backprop(network, input, target, learning_rate):

  network.CheckComplete()
  # 1) We first propagate the input through the network
  FeedForward (network,input)

  # 2) Then we compute the errors and update the weigths starting with the last layer
  for i in network.outputs:
    err = target[i] - network.outputs[i].transformed_value
    i.delta = SigmoidPrime(i.raw_value) * err
    for j in i.weights:
      j.value += learning_rate * i.transformed_value * i.delta

  # 3) We now propagate the errors to the hidden layer, and update the weights there too
  for i in network.hidden_nodes: 
    eps = 0
    for j in i.forward_neighbors:
      eps += i.forward_weights[j] * j.delta
    i.delta = SigmoidPrime(i.raw_value) * eps
    for k in i.weights:
      k.value += learning_rate * i.transformed_value * i.delta


def Train(network, inputs, targets, learning_rate, epochs):

  network.CheckComplete()
  for i in range(epochs): 
    for j in inputs:
      Backprop(network, inputs[j], targets[j], learning_rate)
  

class EncodedNetworkFramework(NetworkFramework):
  def __init__(self):
    
    super(EncodedNetworkFramework, self).__init__() #
 

  def EncodeLabel(self, label):
    
    # encode different characters with labels


  def GetNetworkLabel(self):

    # return label after feeding input through network


  def Convert(self, image):
    
    # convert image into input instance


  def InitializeWeights(self):
  
    # initialize initial weights



class SimpleNetwork(EncodedNetworkFramework):
  def __init__(self):
   
    super(SimpleNetwork, self).__init__()
    
    # 1) Adds an input node for each pixel.    
    # 2) Add an output node for each possible digit label.
    pass



class HiddenNetwork(EncodedNetworkFramework):
  def __init__(self, number_of_hidden_nodes=15):
    
    super(HiddenNetwork, self).__init__() 

    # 1) Adds an input node for each pixel
    # 2) Adds the hidden layer
    # 3) Adds an output node for each possible digit label.
    pass
    

class CustomNetwork(EncodedNetworkFramework):
  def __init__(self):
    
    super(CustomNetwork, self).__init__() 
    pass
