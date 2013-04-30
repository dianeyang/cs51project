from neural_net import NeuralNetwork, NetworkFramework
from neural_net import Node, Target, Input, Weight
import random


# <--- Problem 3, Question 1 --->

def FeedForward(network, input):
  """
  Arguments:
  ---------
  network : a NeuralNetwork instance
  input   : an Input instance

  Returns:
  --------
  Nothing

  Description:
  -----------
  This function propagates the inputs through the network. That is,
  it modifies the *raw_value* and *transformed_value* attributes of the
  nodes in the network, starting from the input nodes.

  Notes:
  -----
  The *input* arguments is an instance of Input, and contains just one
  attribute, *values*, which is a list of pixel values. The list is the
  same length as the number of input nodes in the network.

  i.e: len(input.values) == len(network.inputs)

  This is a distributed input encoding (see lecture notes 7 for more
  informations on encoding)

  In particular, you should initialize the input nodes using these input
  values:

  network.inputs[i].raw_value = input[i]
  """

  network.CheckComplete()
  for i in range(len(input.values)):
    network.inputs[i].raw_value = input.values[i] 
    network.inputs[i].transformed_value = input.values[i]
  for hidden in network.hidden_nodes:
    hidden.raw_value = network.ComputeRawValue(hidden)
    hidden.transformed_value = network.Sigmoid(hidden.raw_value)
  for out in network.outputs:
    out.raw_value = network.ComputeRawValue(out)
    out.transformed_value = network.Sigmoid(out.raw_value)
  
  # 1) Assign input values to input nodes
  # 2) Propagates to hidden layer
  # 3) Propagates to the output layer
  

#< --- Problem 3, Question 2

def Backprop(network, input, target, learning_rate):
  """
  Arguments:
  ---------
  network       : a NeuralNetwork instance
  input         : an Input instance
  target        : a target instance
  learning_rate : the learning rate (a float)

  Returns:
  -------
  Nothing

  Description:
  -----------
  The function first propagates the inputs through the network
  using the Feedforward function, then backtracks and update the
  weights.

  Notes:
  ------
  The remarks made for *FeedForward* hold here too.

  The *target* argument is an instance of the class *Target* and
  has one attribute, *values*, which has the same length as the
  number of output nodes in the network.

  i.e: len(target.values) == len(network.outputs)

  In the distributed output encoding scenario, the target.values
  list has 10 elements.

  When computing the error of the output node, you should consider
  that for each output node, the target (that is, the true output)
  is target[i], and the predicted output is network.outputs[i].transformed_value.
  In particular, the error should be a function of:

  target[i] - network.outputs[i].transformed_value
  
  """
  network.CheckComplete()
  # 1) We first propagate the input through the network
  FeedForward (network,input)

  # calculate epsilon and delta for each node
  for i in range(len(network.outputs)):
    err = target[i] - network.outputs[i].transformed_value
    network.outputs[i].delta = network.SigmoidPrime(network.outputs[i].raw_value) * err
  for node in network.hidden_nodes: 
    eps = 0
    for j in range(len(node.forward_neighbors)):
      eps += node.forward_weights[j].value * node.forward_neighbors[j].delta
    node.delta = network.SigmoidPrime(node.raw_value) * eps

# 2) Then we compute the errors and update the weigths starting with the last layer
  for hid in network.hidden_nodes:
    change = learning_rate * hid.transformed_value 
    for j in range(len(hid.forward_weights)):
      hid.forward_weights[j].value += change * hid.forward_neighbors[j].delta

  # 3) We now propagate the errors to the hidden layer, and update the weights there too
  for inp in network.inputs:
    change = learning_rate * inp.transformed_value 
    for j in range(len(inp.forward_weights)):
      inp.forward_weights[j].value += change * inp.forward_neighbors[j].delta

# <--- Problem 3, Question 3 --->

def Train(network, inputs, targets, learning_rate, epochs):
  """
  Arguments:
  ---------
  network       : a NeuralNetwork instance
  inputs        : a list of Input instances
  targets       : a list of Target instances
  learning_rate : a learning_rate (a float)
  epochs        : a number of epochs (an integer)

  Returns:
  -------
  Nothing

  Description:
  -----------
  This function should train the network for a given number of epochs. That is,
  run the *Backprop* over the training set *epochs*-times
  """
  
  network.CheckComplete()
  for i in range(epochs): 
    for j in range(len(inputs)):
      Backprop(network, inputs[j], targets[j], learning_rate)
  


# <--- Problem 3, Question 4 --->

class EncodedNetworkFramework(NetworkFramework):
  def __init__(self):
    """
    Initializatio.
    YOU DO NOT NEED TO MODIFY THIS __init__ method
    """
    super(EncodedNetworkFramework, self).__init__() # < Don't remove this line >
    
  # <--- Fill in the methods below --->

  def EncodeLabel(self, label):
    """
    Arguments:
    ---------
    label: a number between 0 and 25

    Returns:
    ---------
    a list of length 26 representing the distributed
    encoding of the output.

    Description:
    -----------
    Computes the distributed encoding of a given label.

    Example:
    -------
    0 => [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    3 => [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    Notes:
    ----
    Make sure that the elements of the encoding are floats.
    
    """
    # Replace line below by content of function
    l = [0.0] * 52
    l[label] = 1.0
   # new_target = Target()
   # new_target.values = l
    return l


  def GetNetworkLabel(self):
    """
    Arguments:
    ---------
    Nothing

    Returns:
    -------
    the 'best matching' label corresponding to the current output encoding

    Description:
    -----------
    The function looks for the transformed_value of each output, then decides 
    which label to attribute to this list of outputs. The idea is to 'line up'
    the outputs, and consider that the label is the index of the output with the
    highest *transformed_value* attribute

    Example:
    -------

    # Imagine that we have:
    map(lambda node: node.transformed_value, self.network.outputs) => [0.2, 0.1, 0.01, 0.7, 0.23, 0.31, 0, 0, 0, 0.1, 0]

    # Then the returned value (i.e, the label) should be the index of the item 0.7,
    # which is 3
    
    """
    # Replace line below by content of function
    outputs = []
    for out in self.network.outputs:
      outputs.append(out.transformed_value)
    return outputs.index(max(outputs))


  def Convert(self, image):
    """
    Arguments:
    ---------
    image: an Image instance

    Returns:
    -------
    an instance of Input

    Description:
    -----------
    The *image* arguments has 2 attributes: *label* which indicates
    the digit represented by the image, and *pixels* a matrix 14 x 14
    represented by a list (first list is the first row, second list the
    second row, ... ), containing numbers whose values are comprised
    between 0 and 256.0. The function transforms this into a unique list
    of 14 x 14 items, with normalized values (that is, the maximum possible
    value should be 1).
    
    """
    # Replace line below by content of function
    outer = []
    for i in image.pixels:
      for j in i: 
        outer.append(j/256.0)
    inp = Input()
    inp.values = outer
    return inp


  def InitializeWeights(self):
    """
    Arguments:
    ---------
    Nothing

    Returns:
    -------
    Nothing

    Description:
    -----------
    Initializes the weights with random values between [-0.01, 0.01].

    Hint:
    -----
    Consider the *random* module. You may use the the *weights* attribute
    of self.network.
    
    """
    # replace line below by content of function

    for wgt in self.network.weights:
      wgt.value = random.uniform(-0.01, 0.01)





#<--- Problem 3, Question 6 --->

class SimpleNetwork(EncodedNetworkFramework):
  def __init__(self):
    """
    Arguments:
    ---------
    Nothing

    Returns:
    -------
    Nothing

    Description:
    -----------
    Initializes a simple network, with 196 input nodes,
    10 output nodes, and NO hidden nodes. Each input node
    should be connected to every output node.
    """
    super(SimpleNetwork, self).__init__() # < Don't remove this line >
    
    # 1) Adds an input node for each pixel.    
    # 2) Add an output node for each possible digit label.

    for i in range(400):
      self.network.AddNode((Node()), NeuralNetwork.INPUT)
    for j in range(52):
      self.network.AddNode((Node()), NeuralNetwork.OUTPUT)
    for output in self.network.outputs:
      for input in self.network.inputs:
        output.AddInput(input, None, self.network)
   

#<---- Problem 3, Question 7 --->

class HiddenNetwork(EncodedNetworkFramework):
  def __init__(self, number_of_hidden_nodes=15):
    """
    Arguments:
    ---------
    number_of_hidden_nodes : the number of hidden nodes to create (an integer)

    Returns:
    -------
    Nothing

    Description:
    -----------
    Initializes a network with a hidden layer. The network
    should have 196 input nodes, the specified number of
    hidden nodes, and 10 output nodes. The network should be,
    again, fully connected. That is, each input node is connected
    to every hidden node, and each hidden_node is connected to
    every output node.
    """
    super(HiddenNetwork, self).__init__() # < Don't remove this line >

    # 1) Adds an input node for each pixel
    # 2) Adds the hidden layer
    # 3) Adds an output node for each possible digit label.
    for i in range(400):
      self.network.AddNode((Node()), NeuralNetwork.INPUT)
    for j in range(30):
      self.network.AddNode((Node()), NeuralNetwork.HIDDEN)
    for k in range(52):
      self.network.AddNode((Node()), NeuralNetwork.OUTPUT)
    for output in self.network.outputs:
      for hid in self.network.hidden_nodes:
        output.AddInput(hid, None, self.network)
    for hid in self.network.hidden_nodes:
      for inp in self.network.inputs:
        hid.AddInput(inp, None, self.network)
    

#<--- Problem 3, Question 8 ---> 

class CustomNetwork(EncodedNetworkFramework):
  def __init__(self):
    """
    Arguments:
    ---------
    Your pick.

    Returns:
    --------
    Your pick

    Description:
    -----------
    Surprise me!
    """
    super(CustomNetwork, self).__init__() # <Don't remove this line>
        
    for i in range(400):
      self.network.AddNode((Node()), NeuralNetwork.INPUT)
    for j in range(60):
      self.network.AddNode((Node()), NeuralNetwork.HIDDEN)
    for k in range(52):
      self.network.AddNode((Node()), NeuralNetwork.OUTPUT)
    for output in self.network.outputs:
      for hid in self.network.hidden_nodes:
        output.AddInput(hid, None, self.network)
    for hid in self.network.hidden_nodes:
      for inp in self.network.inputs:
        hid.AddInput(inp, None, self.network)
