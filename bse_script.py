import os
import csv
import io
import re
import requests
import redis
from zipfile import ZipFile
from datetime import date, timedelta, datetime
from models import RedisDb

class GetEquityZip(object):

	def __init__(self,for_date=date.today().strftime('%d%m%y')):
		self.for_date = for_date
		self.csv_name = "EQ{}_CSV".format(self.for_date)
		self.red = RedisDb()
		self.zip_url = "https://www.bseindia.com/download/BhavCopy/Equity/{}.ZIP".format(self.csv_name)

	def get_zip_from_bse(self):
		try:
			#get the zip file
			response = requests.get(self.zip_url)
			if response.status_code == 200:
				#extract the zipfile
				with ZipFile(io.BytesIO(response.content)) as zip_file:
					#get the csv after extracting and read it
					with zip_file.open(zip_file.namelist().pop()) as f:
						file = io.TextIOWrapper(f, encoding="utf-8")
						data = csv.DictReader(file)
						data = [row for row in data]
			if data:
				#save data to redis DB
				if self.for_date == self.red.r_con.get('last_updated_date'):
					return {"success" : True, "message": "File already successfully loaded for date {}".format(self.for_date)}
				if not self._save_data_from_csv(data):
					return {"success" : False, "message": "Some error occured for date {}".format(self.for_date)}

				return {"success" : True, "message": "File successfully loaded for date {}".format(self.for_date)}

			if response.status_code == 404:
				#file not found
				return {"success" : False, "message": "File not found for date {}".format(self.for_date)}
		except Exception as e:
			print(e)
			return {"success" : False, "message": "Some error occured!!"}

	def _save_data_from_csv(self,data=[]):
		try:
			if not self.red.clear_db():
				return False

			for row in data:
				try:
					eq_change = round(((float(row['CLOSE']) - float(row['PREVCLOSE']))*100)/float(row['CLOSE']),2) #to get top 10 performer
				except ZeroDivisionError as e:
					eq_change = 0

				row_values = {
					'Name' : row['SC_NAME'].strip(),
					'Code' : row['SC_CODE'],
					'Open' : float(row['OPEN']),
					'Close' : float(row['CLOSE']),
					'High' :float( row['HIGH']),
					'Low' : float(row['LOW']),
					'PreClose':float(row['PREVCLOSE']),
					'Change': eq_change
				}
				self.red.insert_row(row_values['Name'], row_values)
				self.red.r_con.zadd("search",{row_values['Name']:row_values['Change']})
			self.red.r_con.set("last_updated_date", self.for_date)
			return True
		except Exception as e:
			print(e)
		return False
