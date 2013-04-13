#training file for character recognition
import Image
import math

#creates list of +/- 1 based on color of pixel
#1 = black; -1 = white
#do we need anything else to form input nodes?
#list gives values of first column, then 2nd column, etc
def getColors (image): 
	im = image.load()
	print "hello"
	colors = []
	if im.size  == (40, 40): 
		for x in range(0, 39):
			for y in range (0, 39):
				if im[x, y] == (0, 0, 0): 
					colors.append(1) 
				elif im[x, y] == (255, 255, 255):
					colors.append(-1)
				else:
					raise Exception("Image improperly formatted")
		for item in colors:
			print item
	else: 
		raise Exception("Image improperly formatted")


getColors(Image.open('Resized-DRW7A.jpg'))



