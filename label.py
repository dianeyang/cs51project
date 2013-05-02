import sys

f = open("punctuationyo", 'r')
fout = open("p", 'wt')
counter = 26
while True:
	line = f.readline()
	if not line:
		break
	if line.find('#') == 0:
		linenew = line.replace('#', '#'+str(counter%26+26))
		fout.write(linenew)
		counter = counter+1
	else:
		fout.write(line)
f.close()
fout.close()