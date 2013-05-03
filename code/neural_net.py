import math

class Weight:
  def __init__(self, value):
    self.value = value

class Node:
  """
  Attributes:
  ----------
  inputs            : a list of node who are inputs for this node
  weights           : a list of weight objects, for links with input nodes
  fixed_weight      : w0 in the lecture notes and slides
  forward_neighbors : a list of nodes who are output for this node
  raw_value         : the linear combination of weights and input signals, that is w'x
  transformed_value : the signal emitted by this node, that is g(w'x)

  """
  def __init__(self):
    self.inputs = []
    self.weights = []
    self.fixed_weight = None
    self.forward_neighbors = []
    self.forward_weights = []
    self.raw_value = 0
    self.transformed_value = 0

  # connect a node as another node's input
  def AddInput(self, node, weight, network):
    self.inputs.append(node)
    if not weight:
      weight = network.GetNewWeight()
    self.weights.append(weight)
    node.forward_neighbors.append(self)
    node.forward_weights.append(weight)
    if not self.fixed_weight:
      self.fixed_weight = network.GetNewWeight()

# Input = set of pixels put into neural network
class Input:
  def __init__(self):
    self.values = []

# the desired output of the neural network
class Target:
  def __init__(self):
    self.values = []


class NeuralNetwork:
  INPUT = 1
  HIDDEN = 2
  OUTPUT = 3

  def __init__(self):
    self.complete = False
    self.inputs = []
    self.hidden_nodes = []
    self.outputs = []
    self.node_set = {}
    self.weights = []

  # puts a weight between 2 nodes in the network
  def GetNewWeight(self):
    weight = Weight(0.0)
    self.weights.append(weight)
    return weight

  # puts another node into the network
  def AddNode(self, node, node_type):
    self.CheckIncomplete()
    if node_type == self.INPUT:
      assert len(node.inputs) == 0, 'Input node cannot have inputs'
    # Check that we only reference inputs already in the network
    for input in node.inputs:
      assert input in self.node_set, 'Cannot reference input that is not already in the network'
    self.node_set[node] = True
    if node_type == self.INPUT:
      self.inputs.append(node)
    elif node_type == self.HIDDEN:
      self.hidden_nodes.append(node)
    else:
      assert node_type == self.OUTPUT, 'Unexpected node_type: ' % node_type
      self.outputs.append(node)
    
  # checks network formatted correctly and denotes it complete
  def MarkAsComplete(self):
    seen_nodes = {}
    for input in self.inputs:
      seen_nodes[input] = True
      assert len(input.inputs) == 0, 'Inputs should not have inputs of their own.'
    for node in self.hidden_nodes:
      seen_nodes[node] = True
      for input in node.inputs:
        assert input in seen_nodes, ('Node refers to input that was added to the network later than'
          'it.')
    for node in self.outputs:
      assert len(node.forward_neighbors) == 0, 'Output node cannot have forward neighbors.'
      for input in node.inputs:
        assert input in seen_nodes, ('Node refers to input that was added to the network later than'
          'it.')
    self.complete = True

  # checks if network is complete per above
  def CheckComplete(self):
    if self.complete:
      return
    self.MarkAsComplete()

  def CheckIncomplete(self):
    assert not self.complete, ('Tried to modify the network when it has already been marked as'
      'complete')

  # gets raw value for node: sum of input * weights
  @staticmethod
  def ComputeRawValue(node):
    total_weight = 0

    for i in range(len(node.inputs)):
      total_weight += node.weights[i].value * node.inputs[i].transformed_value
    total_weight += node.fixed_weight.value
    return total_weight
  
  # transforms raw value by applying sigmoid function to it
  @staticmethod
  def Sigmoid(value):
    try:
      return 1.0 / (1 + math.exp(-value))
    except:
      if value < 0:
        return 0.0
      else:
        return 1.0

  # derivative of sigmoid function, used for amount to adjust weights by
  @staticmethod
  def SigmoidPrime(value):
    try:
      return math.exp(-value) / math.pow(1 + math.exp(-value), 2)
    except:
      return 0

  # sets network weight values from list of weights
  def InitFromWeights(self, weights):
    assert len(self.weights) == len(weights), (
      'Trying to initialize from a different sized weight vector.')
    for i in range(len(weights)):
      self.weights[i].value = weights[i]


class NetworkFramework(object):
  def __init__(self):
    self.network = NeuralNetwork()

    # implemented in neural_net_impl
    self.FeedForwardFn = None
    self.TrainFn = None

  # set network weights initially
  def InitializeWeights(self):
    for weight in self.network.weights:
      weight.value = 0

  # returns label (ie: which index -corresponding to a letter- the image is)
  def Classify(self, image):
    input = self.Convert(image)
    self.FeedForwardFn(self.network, input)
    return self.GetNetworkLabel()

  # recods how often each epoch of training gets right answer
  def Performance(self, images):
    # Loop over the set of images and count the number correct.
    correct = 0
    for image in images:
      if self.Classify(image) == image.label:
        correct += 1
    return correct * 1.0 / len(images)

  # framework for training neural network
  def Train(self, images, validation_images, learning_rate, epochs):

    # Convert the images and labels into a format the network can understand.
    inputs = []
    targets = []
    for image in images:
      inputs.append(self.Convert(image))
      targets.append(self.EncodeLabel(image.label))
    

    # Initializes performance log
    performance_log = []
    performance_log.append((self.Performance(images), self.Performance(validation_images)))
    
    # Loop through the specified number of training epochs.
    for i in range(epochs):

      # This calls your function in neural_net_impl.py.
      self.TrainFn(self.network, inputs, targets, learning_rate, 1)

      # Print out the current training and validation performance.
      perf_train = self.Performance(images)
      perf_validate = self.Performance(validation_images)
      print '%d Performance: %.8f %.3f' % (
        i + 1, perf_train, perf_validate)

      # updates log
      performance_log.append((perf_train, perf_validate))

    
    return(performance_log)

  def RegisterFeedForwardFunction(self, fn):
    self.FeedForwardFn = fn

  def RegisterTrainFunction(self, fn):
    self.TrainFn = fn
