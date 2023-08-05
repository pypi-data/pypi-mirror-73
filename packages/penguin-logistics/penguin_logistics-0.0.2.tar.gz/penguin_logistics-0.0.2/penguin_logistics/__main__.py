import argparse

from .batch import batch
from .fake_cache import fake_cache

parser = argparse.ArgumentParser()
parser.add_argument("initial", type=int)
args = parser.parse_args()

class fake_cache_wrapped(fake_cache):
	def __init__(self):
		super().__init__(args.initial)

batch(fake_cache_wrapped)