# DATA_READER.PY
# used in neural network 
# includes functions for reading the image files and weights files
# fucntion defentition and implementation from CS181 pset, 
# with some tweaks we made 


class Image:
  def __init__(self, label):
    self.pixels = []
    self.label = label

# go from text file of image matrices to Image instances
class DataReader:
  @staticmethod
  def GetImages(filename, limit):
    images = []
    infile = open(filename, 'r')
    ct = 0
    cur_row = 0
    image = None
    while True:
      line = infile.readline().strip()
      if not line:
        break
      if line.find('#') == 0:
        if image:
          images.append(image)
          ct += 1
          if ct > limit and limit != -1:
            break
        image = Image(int(line[1:]))
      else:
        image.pixels.append([float(r) for r in line.strip().split()])
    if image:
      images.append(image)
    return images

  # put weights in text file after training
  @staticmethod
  def DumpWeights(weights, filename):
    outfile = open(filename, 'w')
    for weight in weights:
      outfile.write('%r\n' % weight.value)

  # get weights from text file to run network
  @staticmethod
  def ReadWeights(filename):
    infile = open(filename, 'r')
    weights = []
    for line in infile:
      weight = float(line.strip())
      weights.append(weight)
    return weights
