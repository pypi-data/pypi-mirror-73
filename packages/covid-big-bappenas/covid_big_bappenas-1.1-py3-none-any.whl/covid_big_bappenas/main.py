import click
import csv
import requests
import json

from datetime import datetime

#host
host = "https://data.covid19.go.id"
#api-endpoint 
url_list_kab_kota = host + "/grafik/psbb-epidemic/epidemic-peta"
url_epidemic = host + "/grafik/psbb-epidemic/epidemic"
#list of prov_kab_kota data with their code
data_kab_kot = []
tasks = ['indikator1', 'indikator2', 'indikator3']

def welcome():
    """A helper pip package for Covid BIG BAPPENAS Project."""
    click.echo('Welcome to Covid-Big-Bappenas Package!')
    click.echo('===============================================')
    click.echo('Author: Muhammad Hasannudin Yusa')
    click.echo('Office: Pusat PPIG - Badan Informasi Geospasial')
    click.echo('Email: muhammad.hasannudin@big.go.id')
    click.echo('===============================================')
    init_tasks()
  	
@click.command()
@click.argument('task')
@click.option('--key', prompt='Your key', help='The key to login.')
#@click.option('--task', type=click.Choice(tasks, case_sensitive=False), help='The indikator to be processed.')
def init_tasks(task, key):
    if task in tasks:
    	click.echo('Task: %s ' % task)
    	insert_key(key, task)
    else:
    	click.echo('Please choose task: %s' % tasks)

def insert_key(key, task):
    init_harvester(key, task)
	
def init_harvester(key, task):
    click.echo('Harvester is initiated!')
    run_harvester(key, task)

def run_harvester(key, task):
	click.echo('Try to connect to BLC: %s' % host)
	#click.echo('task: %s' % task)
	if task == "indikator1":
		click.echo('Harvest data for indikator1')
		listing_kab_kota(key)
	elif task == "indikator2":
		click.echo('Still on progress')
	elif task == "indikator3":
		click.echo('Harvest data for indikator3')
		listing_prov(key)

def listing_kab_kota(key):
	HEADERS = {'Cookie': 'PHPSESSID='+key}
	r = requests.get(url = url_list_kab_kota,
		headers=HEADERS
    )
	if r.status_code != 200:
		# This means something went wrong.
		raise ApiError('GET /epidemic-peta/ {}'.format(r.status_code))
	
	if r.headers['Content-Type'] == 'application/json; charset=UTF-8':
		json_response = r.json()
		click.echo('Connected!')
		hits = json_response["hits"]["hits"]
		click.echo('Get list all regencies and municipalities')
		for i in hits: 
			item = {'prov':i["_source"]["prov"], 'kota':i["_source"]["kota"], 'kode_prov':i["_source"]["kode_prov"], 'kode_kota':i["_source"]["kode_kota"]}
			#print(item)
			data_kab_kot.append(item)
		data_kab_kot.sort(key = lambda x: (x["prov"], x["kota"]))
		click.echo('Done!')
		harvest_and_write_data(key)
	else:
		click.echo('Failed to connect to BLC. Please check your key.')

def harvest_and_write_data(key):
	HEADERS = {'Cookie': 'PHPSESSID='+key}
	click.echo('Harvesting is started')
	name_file = datetime.today().strftime('%Y%m%d-%H%M%S')+'_indikator1_kabkot'
	with open(name_file+'.csv', 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(["No", "Nama_Provinsi", "Kode_Provinsi", "Nama_Kab_Kota", "Kode_Kab_Kota", "Tanggal", "Positif", "Kasus_Kumulatif"])
		no = 1
		k = 1
		for o in data_kab_kot:
			filter_prov = o["kode_prov"]
			filter_kota = o["kode_kota"]
			tipe = 'day'
			akumulatif = 0
			nama_prov = o["prov"]
			kode_prov = o["kode_prov"]
			nama_kabkot = o["kota"]
			kode_kabkot = o["kode_kota"]
			click.echo('%s, %s - %s ' % (k, o["prov"], o["kota"]))
			PARAMS = {'filter_prov':filter_prov,'filter_kota':filter_kota,'tipe':tipe}
			harvest = requests.get(url = url_epidemic,
				params=PARAMS,
				headers=HEADERS
			)
			if harvest.status_code != 200:
				# This means something went wrong.
				raise ApiError('GET /epidemic/ {}'.format(harvest.status_code))
			
			if harvest.headers['Content-Type'] == 'application/json; charset=UTF-8':
				harvest_response = harvest.json()
				for l in harvest_response:
					akumulatif += l["kasus_positif"]
					writer.writerow([no, nama_prov, kode_prov, nama_kabkot, kode_kabkot, l["key_as_string"], l["kasus_positif"], akumulatif])
					no += 1
			else:
				click.echo('Failed to obtain data.')
			k += 1
		click.echo('Harvesting is finished') 
		click.echo('Data is saved successfully. The file name is %s.csv' % name_file)

	
def listing_prov(key):
	HEADERS = {'Cookie': 'PHPSESSID='+key}
	r = requests.get(url = url_list_kab_kota,
		headers=HEADERS
    )
	if r.status_code != 200:
		# This means something went wrong.
		raise ApiError('GET /epidemic-peta/ {}'.format(r.status_code))
	
	if r.headers['Content-Type'] == 'application/json; charset=UTF-8':
		json_response = r.json()
		click.echo('Connected!')
		hits = json_response["hits"]["hits"]
		click.echo('Get list all provinces')
		for i in hits: 
			item = {'prov':i["_source"]["prov"], 'kode_prov':i["_source"]["kode_prov"]}
			#print(item)
			data_kab_kot.append(item)
		data_kab_kot.sort(key = lambda x: (x["prov"]))
		unique_data_kab_kot = list(map(json.loads,set(map(json.dumps, data_kab_kot))))
		click.echo('Done!')
		harvest_and_write_data_indikator3(key, unique_data_kab_kot)
	else:
		click.echo('Failed to connect to BLC. Please check your key.')

def harvest_and_write_data_indikator3(key, unique_data_kab_kot):
	HEADERS = {'Cookie': 'PHPSESSID='+key}
	click.echo('Harvesting is started')
	name_file = datetime.today().strftime('%Y%m%d-%H%M%S')+'_indikator3_prov'
	with open(name_file+'.csv', 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(["No", "Tanggal", "Nama Provinsi", "Kode Provinsi", "Kasus Diperiksa", "Akumulasi kasus diperiksa", "Kasus Positif",  "Akumulasi Kasus Positif", "Akumulasi Sembuh dari Terkonfirmasi (+)", "Meninggal dari Terkonfiirmasi (+)"])
		no = 1
		k = 1
		#print(unique_data_kab_kot)
		for o in unique_data_kab_kot:
			#print(o)
			filter_prov = o["kode_prov"]
			tipe = 'day'
			akumulatif = 0
			akumulatif_diperiksa = 0
			akumulatif_meninggal = 0
			akumulatif_sembuh = 0
			nama_prov = o["prov"]
			kode_prov = o["kode_prov"]
			click.echo('%s, %s ' % (k, o["prov"]))
			PARAMS = {'filter_prov':filter_prov,'tipe':tipe}
			harvest = requests.get(url = url_epidemic,
				params=PARAMS,
				headers=HEADERS
			)
			if harvest.status_code != 200:
				# This means something went wrong.
				raise ApiError('GET /epidemic/ {}'.format(harvest.status_code))
			
			if harvest.headers['Content-Type'] == 'application/json; charset=UTF-8':
				harvest_response = harvest.json()
				for l in harvest_response:
					#akumulatif += l["kasus_positif"]
					akumulatif_diperiksa += l["kasus_diperiksa"]
					#akumulatif_meninggal += l["positif_meninggal"]
					#akumulatif_sembuh += l["positif_sembuh"]
					writer.writerow([no, l["key_as_string"], nama_prov, kode_prov, l["kasus_diperiksa"], akumulatif_diperiksa, l["kasus_positif"], l["kasus_positif_kumulatif"],l["positif_sembuh_kumulatif"], l["positif_meninggal"]])
					no += 1
			else:
				click.echo('Failed to obtain data.')
			k += 1
		click.echo('Harvesting is finished') 
		click.echo('Data is saved successfully. The file name is %s.csv' % name_file)
		
if __name__ == '__main__':
    welcome()