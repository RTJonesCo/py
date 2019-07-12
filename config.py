import json
CONFIG_FILE = "config.json"

def new_config():
	config = {
		'code':'empty',
		'alert':'empty',
		'last':'empty'	
		}

	with open(CONFIG_FILE,'w') as json_file:
		json.dump(config,json_file)
		print("created new file") 
def update_config(code,alert,last):

	config = {
		'code': code,
		'alert' : alert,
		'last': last
		}
	with open(CONFIG_FILE,'w') as json_file:
		json.dump(config,json_file)
		print("updated file")

def read_config():
	
	with open(CONFIG_FILE) as json_file:
		data = json.load(json_file)
		print("config loaded")
		config = {
			'code' : data['code'],
			'alert' : data['alert'],
			'last' : data['last']
			}
	return config



##test it###
#update_config("testcode","dshkdashjkdas.wav","big ass string for last run")
cfg = read_config()
print(cfg)
#new_config()
