import os, time, glob

t0 = time.time()

for f in glob.glob("cache/*.txt"):
	print os.stat(f).st_mtime - t0
	print os.stat(f)