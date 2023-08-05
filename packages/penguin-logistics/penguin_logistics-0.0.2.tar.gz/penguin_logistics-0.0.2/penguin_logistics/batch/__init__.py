import itertools
from tqdm import tqdm
from ..parallel import parallel

class batch_class:
	def __init__(self, cache):
		self.cache = cache
		self.pool = parallel()

	def batch_work(self):
		queue = self.queue
		
		for n, txtres in zip(queue, self.pool.run(queue)):
			if txtres:
				print(str(n) + '> ' + txtres)
				self.cache[str(n)] = txtres

	def run_naked(self):
		self.queue = []
		initial = self.cache['next']
		
		for i in tqdm(itertools.count(initial), initial=initial):
			if len(self.queue) < 200:
				self.queue.append(i)
			else:
				self.batch_work()
				self.cache['next'] = i+1
				self.cache.write()
				self.queue = []
				
	def run(self):
		try:
			self.run_naked()
		except KeyboardInterrupt:
			return
			# 按Ctrl+C键停止
			# 捕获一下，不让系统输出长得要命的异常提示
			
def batch(cache_type):
	with cache_type() as cache:
		instance = batch_class(cache)
		instance.run()