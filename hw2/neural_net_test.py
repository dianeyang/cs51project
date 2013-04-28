from neural_net import *
from neural_net_impl import *
from data_reader import *
import unittest

class TrainingTest(unittest.TestCase):

    def test_feed_forward_one(self):
        network = NeuralNetwork()
        ninputs = 10
        output = Node()
        network.AddNode(output, NeuralNetwork.OUTPUT)
        for i in range(ninputs):
            n = Node()
            w = network.GetNewWeight()
            w.value = 1.0
            output.AddInput(n, w, network)
            network.AddNode(n, NeuralNetwork.INPUT)
        input = Input()
        input.values = [i * 1.0 for i in range(ninputs)]
        FeedForward(network, input)
        self.assertEquals(output.raw_value, 45.0)
        self.assertEquals(output.transformed_value, network.Sigmoid(45.0))

    def test_feed_forward_ten(self):
        network = NeuralNetwork()
        ninputs = 10
        noutputs = 10
        inputs = [Node() for i in range(ninputs)]
        outputs = [Node() for i in range(noutputs)]
        for input in inputs:
            network.AddNode(input, NeuralNetwork.INPUT)
        for output in outputs:
            network.AddNode(output, NeuralNetwork.OUTPUT)

        for input in inputs:
            for i, output in enumerate(outputs):
                w = network.GetNewWeight()
                w.value = i * 1.0
                output.AddInput(input, w, network)

        x = Input()
        x.values = [1.0 for i in range(ninputs)]
        FeedForward(network, x)
        for i, output in enumerate(outputs):
            self.assertEquals(output.raw_value, ninputs * i)
            self.assertEquals(output.transformed_value, network.Sigmoid(output.raw_value))

        nf = EncodedNetworkFramework()
        nf.network = network

        labelmax = max([n.transformed_value for n in nf.network.outputs])
        self.assertEquals(nf.network.outputs[nf.GetNetworkLabel()].transformed_value, labelmax)

    def test_backprop(self):
        network = NeuralNetwork()
        ninputs = 10
        output = Node()
        network.AddNode(output, NeuralNetwork.OUTPUT)
        for i in range(ninputs):
            n = Node()
            w = network.GetNewWeight()
            w.value = 1.0
            output.AddInput(n, w, network)
            network.AddNode(n, NeuralNetwork.INPUT)
        input = Input()
        input.values = [i * 1.0 for i in range(ninputs)]
        learning_rate = 1.
        target = Target()
        target.values = [0.]

        Backprop(network, input, target, learning_rate)
        self.assertEquals(output.error, -1.0)
        self.assertEquals(output.delta, network.SigmoidPrime(output.raw_value) * output.error)

        for i, node in enumerate(network.inputs):
            self.assertEquals(node.error, 1.0 * output.delta) 
            self.assertEquals(node.delta, network.SigmoidPrime(node.raw_value) * node.error)
            self.assertEquals(node.forward_weights[0].value, 1.0 + learning_rate * output.transformed_value * output.delta)
            self.assertEquals(output.weights[i].value, node.forward_weights[0].value)

    def test_train(self):
        network = NeuralNetwork()
        ninputs = 10
        output = Node()
        network.AddNode(output, NeuralNetwork.OUTPUT)
        for i in range(ninputs):
            n = Node()
            w = network.GetNewWeight()
            w.value = 1.0
            output.AddInput(n, w, network)
            network.AddNode(n, NeuralNetwork.INPUT)
        input = Input()
        input.values = [i * 1.0 for i in range(ninputs)]
        learning_rate = 1.
        target = Target()
        target.values = [0.]
        epochs = 1

        Train(network, [input], [target], learning_rate, epochs)
        self.assertEquals(output.error, -1.0)
        self.assertEquals(output.delta, network.SigmoidPrime(output.raw_value) * output.error)

        for i, node in enumerate(network.inputs):
            self.assertEquals(node.error, 1.0 * output.delta) 
            self.assertEquals(node.delta, network.SigmoidPrime(node.raw_value) * node.error)
            self.assertEquals(node.forward_weights[0].value, 1.0 + learning_rate * output.transformed_value * output.delta)
            self.assertEquals(output.weights[i].value, node.forward_weights[0].value)

class EncodedNetworkFrameworkTest(unittest.TestCase):

    def test_encode_label(self):
        nf = EncodedNetworkFramework()
        nlabels = 10
        for label in range(nlabels):
            encoding = nf.EncodeLabel(label)
            self.assertEquals(len(encoding.values), 10)
            self.assertEquals(encoding.values[label], 1.0)
            self.assertEquals(sum(encoding.values), 1.0)

    def test_get_network_label(self):
        nf = EncodedNetworkFramework()
        for i in range(10):
            n = Node()
            n.transformed_value = i
            nf.network.outputs.append(n)
        self.assertEquals(nf.GetNetworkLabel(), 9)

    def test_get_network_label_tie(self):
        nf = EncodedNetworkFramework()
        for i in range(10):
            n = Node()
            n.transformed_value = i
            nf.network.outputs.append(n)
        # return the first instance on tie
        nf.network.outputs[5].transformed_value = 100
        nf.network.outputs[8].transformed_value = 100
        self.assertEquals(nf.GetNetworkLabel(), 5)

    def test_convert(self):
        nf = EncodedNetworkFramework()
        pixels = []
        for i in range(14):
            pixels.append([float(i) for j in range(14)])
        image = Image(0)
        image.pixels = pixels
        encoded = nf.Convert(image)
        self.assertEquals(len(encoded.values), 196)
        for i in range(14):
            for j in range(14):
                self.assertEquals(encoded.values[i * 14 + j], i / 256.0)

    def test_init_weights(self):
        nweights = 100
        weights = [Weight(0.) for i in range(100)]
        nf = EncodedNetworkFramework()
        nf.network.weights = weights
        nf.InitializeWeights()
        new_weights = nf.network.weights
        # with very high probability, sum would be different
        self.assertTrue(sum([w.value for w in weights]) != 0.)

if __name__ == "__main__":
    unittest.main()