import redis
import operator
import json
import os
from decouple import config


class RedisDb(object):
	"""redis database model functions to set and get key,values"""

	def __init__(self, host='localhost'):
		self.host = host
		self.r_con = self._connect_redis()

	#get redis connsection
	def _connect_redis(self):
		con = redis.from_url(config("REDIS_URL"), charset="utf-8", decode_responses=True)
		return con

	def insert_row(self,key,values):
		return self.r_con.hmset(key,values)

	def get_row(self,key):
		return self.r_con.hgetall(key)

	def get_top_entries(self,limit = 10):
		# top 10 entries of stock
		keys = self.r_con.zrange("search", 0, limit-1,desc=True)
		result = []
		for key in keys:
			row = self.get_row(key)
			row['Change'] = float(row['Change'])
			result.append(row)
		return result

	def seach_for_name(self,name):
		#fetch matched entries
		# matches = self.r_con.zrangebylex("search", "[" + name, "[" + name + "\xff")

		#searching on keys
		matches = self.r_con.execute_command('KEYS {}*'.format(name))
		result = []
		for match in matches:
			result.append(self.get_row(match))

		return result

	def clear_db(self):
		return self.r_con.flushall()
