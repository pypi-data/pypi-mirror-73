from bs4 import BeautifulSoup
import pandas as pd
import time
import sys
import requests

class WorldCovidData:

	def init():
		return 0

	def getCovidData(country):
		columns = []
		values = []
		country = country.lower().strip()

		parent = "https://www.worldometers.info/coronavirus/?#countries"
		page = requests.get(str(parent))
		soup = BeautifulSoup(page.content, 'html.parser')
		table = soup.find("table",id="main_table_countries_today")
		header = table.find('thead')
		header_row = header.find('tr').find_all('th')
		for row in header_row:
			columns.append(row.get_text().strip())
		country_body = table.find('tbody')
		country_rows = country_body.find_all('tr')[8:]
		for row in country_rows:
			country_data = row.find_all('td')[1:]
			try:
				specific_country = country_data[0].find('a').get_text().lower().strip()
				if specific_country == country:
					for x in country_data[1:]:
						if x.find('a') == None:
							values.append(x.text)
						else:
							values.append(x.find('a').text)
			except:
				pass
		covid_data_map = dict(zip(columns[2:],values))
		return covid_data_map
