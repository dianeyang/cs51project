from PIL import Image 

###################################################################
#
# References used:
#
# * Useful PIL handbook
#   http://www.pythonware.com/media/data/pil-handbook.pdf
#
# * How to convert to black & white using PIL
#   http://stackoverflow.com/questions/9506841/using-python-pil-to-turn-a-rgb-image-into-a-pure-black-and-white-image
#
# * How to expand the canvas without resizing
#   http://stackoverflow.com/questions/1572691/in-python-python-image-library-1-1-6-how-can-i-expand-the-canvas-without-resiz
#
####################################################################

class ProcessedImage(object):
    def __init__(self, file, new_size):
        self.new_size = new_size
        self.image = Image.open(file).convert('1')
        self.pixels = self.image.load()
        self.width, self.height = self.image.size
        self.space = Image.new('1', size = (new_size,new_size), color = 255)
    
    ####################################################################
    # Returns an array of the lines of text in a scanned document
    ####################################################################
    def get_lines(self):
        # determines whether a row has only white pixels
        def row_blank(y):
            for x in range(self.width):
                if self.pixels[x,y] != 255:
                    return False
            return True
    
        lower, upper = None, None
        prev_blank = True
        lines = []
        
        for y in range(self.height):
            # if the row is blank but the previous row was not blank,
            # then we've found the end of a line
            if row_blank(y):
                if not prev_blank:
                    lower = y
                prev_blank = True
            # if the row is not blank but the previous row was blank,
            # then we've found the start of a line
            else:
                if prev_blank:
                    upper = y
                    saved = False
                prev_blank = False
            # if the lower bound is lower than the upper bound,
            # then we've finished identifying a new line, so we copy it
            if lower > upper and not saved:
                box = (0, upper, self.width, lower)
                copy = self.image.crop(box)
                lines.append(copy)
                saved = True
        return lines
        
    ####################################################################
    # Returns an array of the characters in a scanned document
    ####################################################################
    def get_chars(self):
        # determines whether a column has only white pixels
        def col_blank(x, height, pixels):
            for y in range(height):
                if (pixels[x,y] != 255) and (pixels[x-1,y] != 255):
                    return False
            return True
        
        # returns a copy of the box with the given boundaries
        def copy(left, top, right, bottom):
            box = (left, top, right, bottom)
            return line.crop(box)
        
        # splits a line of text into separate characters
        def split_line(line):
            left, right = None, None
            width, height = line.size
            blanks = 0
            prev_blank = True
            new_line = True
            chars = []
            for x in range(width):
                if col_blank(x, height, line.load()):
                    if not prev_blank:
                        right = x
                    prev_blank = True
                    blanks += 1
                else:
                    if prev_blank:
                        left = x
                        copied = False
                    prev_blank = False
                    if blanks >= height/5 and not new_line and not space_added:
                        chars.append(self.space)
                        space_added = True
                    blanks = 0
                if right > left and not copied:
                    chars.append(copy(left, 0, right, height))
                    copied = True
                    new_line = False
                    space_added = False
                
            return chars
    
        lines = self.get_lines()
        chars = []
        
        # iterates through every line, splits into chars, builds flat list of chars
        for line in lines:
            line_chars = split_line(line)
            for char in line_chars:
                chars.append(char)
            chars.append(self.space)
    	return chars

    ####################################################################
    # Returns array of character images resized to the desired invariant
    ####################################################################
    def resize_chars(self):
    	resizedchars = []
        # iterates through flat list of chars
        chars = self.get_chars()
        for x in chars:
        	newsize = float(self.new_size)
        	old_w, old_h = x.size
        	if old_w > old_h:
        		newwidth = self.new_size
        		newheight = int(old_h * (newsize / old_w))
        		new = x.resize((newwidth, newheight), Image.ANTIALIAS)
        	else:
        		newwidth = int(old_w * (newsize / old_h))
        		newheight = self.new_size
        		new = x.resize((newwidth, newheight), Image.ANTIALIAS)
        	newImage = Image.new('1', size = (self.new_size, self.new_size), color=255)
        	if old_w > old_h:
        		newImage.paste(new, (0, int((newsize-newheight) / 2)))
        	else:
        		newImage.paste(new, (int((newsize - newwidth) / 2), 0))
        	resizedchars.append(newImage)
        return resizedchars
        
    ####################################################################
    # Generates a text representation of the pixel matrix
    # See data.txt for sample output
    ####################################################################
    def output_txt(self, file_name, mode):
        # Given a single letter, generates a text version of the pixels
        def output_matrix(letter):
            pixels = letter.load()
            width, height = letter.size
            matrix = "#\n"
            # Go across, then down
            for y in range(height):
                for x in range(width):
                    p = str(pixels[x,y])
                    # Format the text pixel to be 4 characters wide
                    formatted = " " * (3 - len(p)) + p + " "
                    matrix += formatted
                matrix += "\n"
            return matrix
            
        file = open(file_name, mode)
        chars = self.resize_chars()
        matrices = ""
        
        # iterate over every resized char & output text representation
        for char in chars:
            matrices += output_matrix(char) 
            
        file.write(matrices)
        file.close()

###################################################################
# Output desired files
###################################################################

<<<<<<< HEAD:character-extraction.py
training_set0 = ProcessedImage('training_images/training_set2-0.png', 24, 20)
training_set1 = ProcessedImage('training_images/training_set2-1.png', 24, 20)
=======
training_set0 = ProcessedImage('test_paragraph.png', 20)
'''training_set1 = ProcessedImage('training_images/training_set2-1.png', 24, 20)
>>>>>>> 21e7406589d48a2374c637fae99095500f8c46fc:hw2/character-extraction.py
training_set2 = ProcessedImage('training_images/training_set2-2.png', 24, 20)
training_set3 = ProcessedImage('training_images/training_set2-3.png', 24, 20)
training_set4 = ProcessedImage('training_images/training_set2-4.png', 24, 20)
training_set5 = ProcessedImage('training_images/training_set2-5.png', 24, 20)
training_set6 = ProcessedImage('training_images/training_set2-6.png', 24, 20)
training_set7 = ProcessedImage('training_images/training_set2-7.png', 24, 20)
training_set8 = ProcessedImage('training_images/training_set2-8.png', 24, 20)
training_set9 = ProcessedImage('training_images/training_set2-9.png', 24, 20)
<<<<<<< HEAD:character-extraction.py
validation_set = ProcessedImage('training_images/validation_set2.png', 24, 20)

training_set0.output_txt("training2.txt", "w")
training_set1.output_txt("training2.txt", "a")
=======
validation_set = ProcessedImage('training_images/validation_set2.png', 24, 20)'''

training_set0.output_txt("test_paragraph.txt", "w")
'''training_set1.output_txt("training2.txt", "a")
>>>>>>> 21e7406589d48a2374c637fae99095500f8c46fc:hw2/character-extraction.py
training_set2.output_txt("training2.txt", "a")
training_set3.output_txt("training2.txt", "a")
training_set4.output_txt("training2.txt", "a")
training_set5.output_txt("training2.txt", "a")
training_set6.output_txt("training2.txt", "a")
training_set7.output_txt("training2.txt", "a")
training_set8.output_txt("training2.txt", "a")
training_set9.output_txt("training2.txt", "a")
<<<<<<< HEAD:character-extraction.py
validation_set.output_txt("validation2.txt", "w")
=======
validation_set.output_txt("validation2.txt", "w")'''
>>>>>>> 21e7406589d48a2374c637fae99095500f8c46fc:hw2/character-extraction.py

