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

  for i in range(len(input)):
    network.inputs[i].raw_value = input[i]
  for i in range(len(network.inputs)): 
    network.inputs[i].transformed_value = network.inputs[i].raw_value
  for i in range(len(network.hidden_nodes)):
      network.hidden_nodes[i].raw_value = network.ComputeRawValue(network.hidden_nodes[i])
      network.hidden_nodes[i].transformed_value = network.Sigmoid(network.hidden_nodes[i].raw_value)
  for i in range(len(network.outputs)):
    network.outputs[i].raw_value = network.ComputeRawValue(network.outputs[i])
  
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

  # 2) Then we compute the errors and update the weigths starting with the last layer
  for i in (range(len(network.outputs))):
    err = target[i] - network.outputs[i].transformed_value
    network.outputs[i].delta = network.SigmoidPrime(network.outputs[i].raw_value) * err
    for j in range(len(network.outputs[i].weights)):
      network.outputs[i].weights[j].value += learning_rate * network.outputs[i].transformed_value * network.outputs[i].delta

  # 3) We now propagate the errors to the hidden layer, and update the weights there too
  for i in range(len(network.hidden_nodes)): 
    node = network.hidden_nodes[i]
    eps = 0
    for j in node.forward_neighbors:
      eps += node.forward_weights[j] * node.forward_neighbors[j].delta
    node.delta = network.SigmoidPrime(i.raw_value) * eps
    for k in node.weights:
      node.weights[k].value += learning_rate * node.transformed_value * node.delta

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
    label: a number between 0 and 9

    Returns:
    ---------
    a list of length 10 representing the distributed
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
  
    for i in range(10):
      label = [0]*10
      for j in range(10):
        if i == j:
          label[j] = 1.0 
        else:
          label[j] = 0.0
      return label


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
    for i in range(len(self.network.outputs)):
      outputs.append(self.network.outputs[i].transformed_value)
    return max(outputs)


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
      inner = []
      for j in i: 
        inner.append(j/256.0)
      outer.append(inner)
    return outer


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
    for i in self.network.weights:
      self.network.weights[i] = Weight(random.uniform(-0.01, 0.01))
    for j in range(len(self.network.inputs)):
        self.network.inputs[j].fixed_weight = Weight(random.uniform(-0.01, 0.01))
    for k in range(len(self.network.hidden_nodes)): 
        self.network.hidden_nodes[k].fixed_weight = Weight(random.uniform(-0.01, 0.01))
    for l in range(len(self.network.outputs)):
        self.network.outputs[l].fixed_weight = Weight(random.uniform(-0.01, 0.01))





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
    #inputNodes=[]
    #outputNodes=[]
    for i in range(196):
      #inputNodes.append = Node()
      self.network.AddNode((Node()), 1)
    for j in range(10):
      #outputNodes.append = Node()
      self.network.AddNode((Node()), 3)
   

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
    for i in range(196):
      self.network.AddNode((Node()), 1)
    for j in range(30):
      self.network.AddNode((Node()), 2)
    for k in range(10):
      self.network.AddNode((Node()), 3)
    

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
        
    for i in range(900):
      self.network.AddNode((Node()), 1)
    for j in range(30):
      self.network.AddNode((Node()), 2)
    for k in range(26):
      self.network.AddNode((Node()), 3)
