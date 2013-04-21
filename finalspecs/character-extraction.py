# useful PIL handbook
# http://www.pythonware.com/media/data/pil-handbook.pdf

from PIL import Image

class ProcessedImage(object):
    def __init__(self, file):
        self.image = Image.open(file).convert('1')
        self.pixels = self.image.load()
        self.width, self.height = self.image.size
    
    # returns an array of the lines of text in a scanned document
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
            if row_blank(y):
                if not prev_blank:
                    lower = y
                prev_blank = True
            else:
                if prev_blank:
                    upper = y
                    saved = False
                prev_blank = False
            if lower > upper and not saved:
                box = (0, upper, self.width, lower)
                copy = self.image.crop(box)
                lines.append(copy)
                saved = True
        return lines
    
    # T0D0: get_chars

    # T0D0: resize