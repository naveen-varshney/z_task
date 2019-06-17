import redis
import operator
import json


class RedisDb(object):
	"""redis database model functions to set and get key,values"""

	def __init__(self, host='localhost'):
		self.host = host
		self.r_con = self._connect_redis()

	#get redis connsection
	def _connect_redis(self):
		con = redis.Redis(host=self.host, charset="utf-8", decode_responses=True)
		return con

	def insert_row(self,key,values):
		return self.r_con.hmset(key,values)

	def get_row(self,key):
		return self.r_con.hgetall(key)

	def get_top_entries(self,limit = 10):
		keys = self.r_con.zrange("search", 0, limit-1)
		result = []
		for key in keys:
			row = self.get_row(key)
			row['Change'] = float(row['Change'])
			result.append(row)
		return json.dumps(result)

	def seach_for_name(self,name):
		#fetch and store the matched entries
		matches = self.r_con.zrangebylex("search", "[" + name, "[" + name + "\xff")
		result = []
		for match in matches:
			result.append(self.r_con.get_row(match))

		return json.dumps(result)

	def clear_db(self):
		return self.r_con.flushall()
