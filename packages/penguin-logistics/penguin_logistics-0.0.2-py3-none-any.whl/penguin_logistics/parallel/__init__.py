from concurrent.futures import ThreadPoolExecutor

from ..core import test

class parallel(ThreadPoolExecutor):
	def __init__(self):
		ThreadPoolExecutor.__init__(self, max_workers=100)

	def run(self, queue):
		return self.map(test, queue)