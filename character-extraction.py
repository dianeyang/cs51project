from PIL import Image 

# from http://stackoverflow.com/questions/9506841/using-python-pil-to-turn-a-rgb-image-into-a-pure-black-and-white-image
# CONVERT TO BLACK AND WHITE
im = Image.open("convert.png") # open colour image
im = im.convert('1') # convert image to black and white
im.save('result.png')

# by Amna
# from http://stackoverflow.com/questions/1109422/getting-list-of-pixel-values-from-pil
'''im = Image.open("testimage3.png")
pixels = im.load() # this is not a list, nor is it list()'able
width, height = im.size
all_pixels = []
    for x in range(width):
        for y in range(height):
            cpixel = pixels[x, y]
            all_pixels.append(cpixel)
print all_pixels'''

# remove entire rows of black pixels
# from http://stackoverflow.com/questions/12770218/using-pil-or-a-numpy-array-how-can-i-remove-entire-rows-from-an-image
'''
from PIL import Image

def find_rows_with_color(pixels, width, height, color):
    rows_found=[]
    for y in xrange(height):
        for x in xrange(width):
            if pixels[x, y] != color:
                break
        else:
            rows_found.append(y)
    return rows_found

old_im = Image.open("path/to/old/image.png")
if old_im.mode != 'RGB':
    old_im = old_im.convert('RGB')
pixels = old_im.load()
width, height = old_im.size[0], old_im.size[1]

rows_to_remove = find_rows_with_color(pixels, width, height, (0, 0, 0)) #Remove black rows
new_im = Image.new('RGB', (width, height - len(rows_to_remove)))
pixels_new = new_im.load()

rows_removed = 0
for y in xrange(old_im.size[1]):
    if y not in rows_to_remove:
        for x in xrange(new_im.size[0]):
            pixels_new[x, y - rows_removed] = pixels[x, y]
    else:
        rows_removed += 1
        
new_im.save("path/to/new/image.png")
'''

class ProcessedImage(object):
    def __init__(self, file):
        self.image = Image.open(file)
        self.pixels = self.image.load()
        self.width, self.height = self.image.size
        self.lines = []
        self.characters = []
    
    def black_and_white(self):
        self.image = self.image.convert('1') # convert image to black and white
        self.pixels = self.image.load()
        
    '''def crop_margins(self):
        def col_blank(x):
            for y in range (self.height):
                #print "y: " + str(y)
                if self.pixels[x,y] != 255:
                    return False
            return True
        
        left, right = None, None
        
        #print "L E F T ! ! ! ! !"
        for x in range(self.width):
            #print "x: " + str(x)
            if not col_blank(x):
                left = x
                break
                
                
        #print "R I G H T ! ! ! ! !"
        for x in range(self.width):
            #print "x: " + str(self.width - x - 1)
            if not col_blank(self.width - x - 1):
                right = x
                break
        
        #print "CROPPING: (" + str(left) + ", 0, " + str(self.width - right) + ", " + str(self.height) + ")"
        self.image = im.crop((left, 0, self.width - right, self.height))
        self.pixels = self.image.load()
        self.width = self.width - left - right'''
    
    def get_lines(self):
        def row_blank(y):
            for x in range(self.width):
                #print "(x,y): (" + str(x) + ", " + str(y) + ")"
                if self.pixels[x,y] != 255:
                    print "pixel (" + str(x) + ", " + str(y) + ") isn't white"
                    return False
            print "BLANK"
            return True
    
        lower, upper = None, None
        prev_blank = True
        
        for y in range(self.height):
            #print "y: " + str(y)
            if row_blank(y):
                if not prev_blank:
                    lower = y
                    #print "lower: " + str(lower)
                prev_blank = True
            else:
                if prev_blank:
                    upper = y
                    #print "upper: " + str(upper)
                prev_blank = False
            if lower > upper:
                #print "checking"
                box = (0, upper, self.width, lower)
                self.lines.append(box)
                print "ADDED A LINE"
        print len(self.lines)
        return
                
    def save(name):
        self.image.save(name)
        
test = ProcessedImage('scanned.png')
print "height: " + str(test.height)
print "width : " + str(test.width)
test.black_and_white()
#test.crop_margins()
test.get_lines()
