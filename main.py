import os
import json

try:
	import hvac
except ImportError:
	print ("hvac library is needed. Run pip install hvac.")

hvac_client = {
	'url': os.environ['VAULT_ADDR'],
}

client = hvac.Client(**hvac_client)

try: 
	github_token = os.environ['GITHUB_PAT']

	login_response = client.auth.github.login(token=github_token)
except KeyError:
	github_token = input("Vault Token: ")

assert client.is_authenticated()

# path = "arctiq/data/users/arctiqjacob/testing"

# secret_version_response = client.read(path)

# for key, value in secret_version_response['data']['data'].items():
# 	print ("vault kv put {} {}={}".format(path, key, value))

list_response = client.secrets.kv.v2.list_secrets(
	path='arctiq/users/arctiqjacob/testing'
)