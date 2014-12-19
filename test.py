import tempfile

for i in range(10):
	temp = tempfile.NamedTemporaryFile(mode="w+b", prefix="result_", dir="cache/", delete=False)
	print temp.name