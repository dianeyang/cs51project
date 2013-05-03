import sys

f = open("lower.txt", 'r')
fout = open("pl.txt", 'wt')
counter = 0
while True:
	line = f.readline()
	if not line:
		break
	if line.find('#') == 0:
		linenew = line.replace('#', '#'+str(counter%27+26))
		fout.write(linenew)
		counter = counter+1
	else:
		fout.write(line)
f.close()
fout.close()