import json

class json_context(dict):
	def __init__(self, filename):
		self.filename = filename
		with open(filename, 'r') as f:
			dict.__init__(self, json.load(f))
	
	def __enter__(self):
		return self

	def write(self):
		data = json.dumps(self, sort_keys=True, indent=4)

		with open(self.filename, 'w') as f:
			f.write(data)
			# 不要直接json.dump(self, f)
			# 万一JSON过程中出错，cache文件就被损坏了

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.write()
		
		if exc_type:
			raise exc_type(exc_val)