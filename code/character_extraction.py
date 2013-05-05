# CHARACTER_EXTRACTION.PY
# takes in a .png file and divides it into character pixel matrices

from PIL import Image
import sys

###################################################################
#
# References used:
#
# * Useful PIL handbook
#   http://www.pythonware.com/media/data/pil-handbook.pdf
#
# * How to convert to black & white using PIL
#   http://stackoverflow.com/questions/9506841/using-python-pil-to-turn-a-rgb-
#    image-into-a-pure-black-and-white-image
#
# * How to expand the canvas without resizing
#   http://stackoverflow.com/questions/1572691/in-python-python-image-library-
#   1-1-6-how-can-i-expand-the-canvas-without-resiz
#
####################################################################

resize_to = 20

class ProcessedImage(object):
    def __init__(self, file):
        self.image = Image.open(file).convert('1')
        self.pixels = self.image.load()
        self.width, self.height = self.image.size
        self.space = Image.new('1', size = (resize_to, resize_to), color = 255)
    
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
    
        # store lower & upper bounds for each line of text
        lower, upper = None, None
        # keep track of whether previous row was blank
        prev_blank = True
        # list of images lines of text
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
            # stores left & right bounds of each char
            left, right = None, None
            width, height = line.size
            # counter for number of blank columns - help identify spaces
            blanks = 0
            # remember whether previous column was blank
            prev_blank = True
            # remember whether at start of new line
            # (so we don't add an unnecessary space)
            new_line = True
            # collect list of images of chars
            chars = []

            for x in range(width):
                # if we go from having non-blank columns to blank columns,
                # then we have found the right side of a char
                if col_blank(x, height, line.load()):
                    if not prev_blank:
                        right = x
                    prev_blank = True
                    blanks += 1
                else:
                    # if we go from having blank columns to non-blank columns,
                    # then we have found the left side of a char
                    if prev_blank:
                        left = x
                        copied = False
                    prev_blank = False
                    # if we've seen height/2 consecutive blank columns,
                    # then this must be a space
                    if blanks >= height/2 and not new_line and not space_added:
                        chars.append(self.space)
                        space_added = True
                    blanks = 0
                # if we've found the left & right boundaries of a new char,
                # copy it and add that to our list
                if right > left and not copied:
                    chars.append(copy(left, 0, right, height))
                    copied = True
                    new_line = False
                    space_added = False
                
            return chars
    
        lines = self.get_lines()
        chars = []
        
        # iterates through every line, splits into chars, builds flat list of 
        # chars
        for line in lines:
            line_chars = split_line(line)
            for char in line_chars:
                chars.append(char)
            chars.append(self.space)
    	return chars

    ####################################################################
    # Returns array of character images resized to the desired invariant
    ####################################################################
    def resize_chars(self, new_size):
    	resizedchars = []
        # iterates through flat list of chars
        chars = self.get_chars()
        for x in chars:
        	newsize = float(new_size)
        	old_w, old_h = x.size

            # if landscape, set width to newsize
        	if old_w > old_h:
        		newwidth = new_size
        		newheight = int(old_h * (newsize / old_w))
        		new = x.resize((newwidth, newheight), Image.ANTIALIAS)
            # if portrait (or square) set height to newsize
        	else:
        		newwidth = int(old_w * (newsize / old_h))
        		newheight = new_size
        		new = x.resize((newwidth, newheight), Image.ANTIALIAS)
            # create square white canvas
        	newImage = Image.new('1', size = (new_size, new_size), color=255)
            # paste resized char into middle of canvas
        	if old_w > old_h:
        		newImage.paste(new, (0, int((newsize-newheight) / 2)))
        	else:
        		newImage.paste(new, (int((newsize - newwidth) / 2), 0))
            # add to list of resized chars
        	resizedchars.append(newImage)
        return resizedchars
        
    ####################################################################
    # Generates a text representation of the pixel matrix
    # See data.txt for sample output
    ####################################################################
    def output_txt(self, imgs, file_name, mode):
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
        matrices = ""
        
        # iterate over every resized char & output text representation
        for img in imgs:
            matrices += output_matrix(img) 
            
        file.write(matrices)
        file.close()
        return

####################################################################
# Running from the command line
####################################################################
def from_command_line(input,output="char-extract-output.txt"):
    image = ProcessedImage(input)
    chars = image.resize_chars(20)
    counter = 1
    for char in chars:
        #char.save("extracted/char" + str(counter) + ".png")
        counter += 1
    resize = image.resize_chars(resize_to)
    image.output_txt(resize, output, "w")
    return

# can output txt from command line prompt
if __name__ == "__main__":
    if len(sys.argv) == 2:
        from_command_line(sys.argv[1])
    elif len(sys.argv) == 3:
        from_command_line(sys.argv[1], sys.argv[2])
    else:
        print "Usage: python character_extraction.py input_name [output_name]"

