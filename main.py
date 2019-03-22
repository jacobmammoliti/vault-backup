import os
import json

try:
	import hvac
except ImportError:
	print ("hvac library is needed. Run pip install hvac.")

hvac_client = {
	'url': vault_url,
}

client = hvac.Client()

try: 
	github_token = os.environ['GITHUB_PAT']

	login_response = client.auth.github.login(token=github_token)
except KeyError:
	github_token = input("Vault Token: ")

list_response = client.secrets.kv.v2.list_secrets(
    path='arctiq',
)

print (json.dumps(list_response, indent=4))