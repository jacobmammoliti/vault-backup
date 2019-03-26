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

def recurse_through_secrets(path_prefix, candidate_key):
    candidate_values = candidate_key['data']['keys']

    for candidate_value in candidate_values:

        next_index = path_prefix + candidate_value

        if candidate_value.endswith('/') and candidate_value != 'users/':

            next_value = client.secrets.kv.v2.list_secrets(path=next_index, \
                                                           mount_point='arctiq')

            recurse_through_secrets(next_index, next_value)

        elif candidate_value != 'users/':
            final_dict = client.read('arctiq/data/' + next_index)['data']

            print ("\nvault kv put arctiq/{}".format(next_index), end='')
                        
            final_value = final_dict['data']

            try:
                final_value = final_value.encode("utf-8")
            except AttributeError:
                final_value = final_value

            for f in final_value:
                print (' "{0}={1}"'.format(f, final_value[f]), end='')

            print ()

try: 
    github_token = os.environ['GITHUB_PAT']

    login_response = client.auth.github.login(token=github_token)
except KeyError:
    github_token = input("Vault Token: ")

assert client.is_authenticated()

top_level_keys = client.secrets.kv.v2.list_secrets(path='', mount_point='arctiq')
top_vault_prefix = ''

recurse_through_secrets(top_vault_prefix, top_level_keys)