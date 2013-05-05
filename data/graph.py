import sys

f = open("searchable.txt", 'r')
fout = open("pl.txt", 'wt')
counter = 0
while True:
	line = f.readline().split()
	if not line:
		break
	else:
		print line[3]
		linenew = line[3]
		fout.write(linenew+ "\n")
f.close()
fout.close()