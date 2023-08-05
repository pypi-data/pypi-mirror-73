class fake_cache(dict):
	def __init__(self, initial):
		super().__init__()
		self['next'] = initial

	def __enter__(self):
		return self
		
	def __exit__(self, exc_type, exc_val, exc_tb):
		self.write()
		
		if exc_type:
			raise exc_type(exc_val)

	def write(self):
		pass