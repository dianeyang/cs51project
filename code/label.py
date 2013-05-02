import sys

f = open("char-extract-output.txt", 'r')
fout = open("p.txt", 'wt')
counter = 0
while True:
	line = f.readline()
	if not line:
		break
	if line.find('#') == 0:
		linenew = line.replace('#', '#'+str(counter%26))
		fout.write(linenew)
		counter = counter+1
	else:
		fout.write(line)
f.close()
fout.close()