import os
import json

try:
    import hvac
except ImportError:
    print ("hvac library is needed. Run pip install hvac.")

try:
    vault_token = os.environ['VAULT_TOKEN']
except KeyError:
    print ("VAULT_TOKEN not set.. Goodbye!")
    raise SystemExit

try:
    vault_url = os.environ['VAULT_ADDR']
except KeyError:
    print ("VAULT_ADDR not set.. Goodbye!")
    raise SystemExit

hvac_client = {
    'url': vault_url,
    'token': vault_token
}

client = hvac.Client(**hvac_client)

def recurse_through_secrets(path_prefix, candidate_key, mount_point):
    """Use recursion to traverse through the secrets paths to retrieve secrets.

    Keyword arguments:
    path_prefix   -- current path we are looking at (must be a folder)
    candidate_key -- dictionary of all secrets that exist in a folder
    mount_point   -- the vault secrets engine
    """

    # dictionary of all records in current path
    candidate_values = candidate_key['data']['keys']

    # looping through each record in the above dictionary
    for candidate_value in candidate_values:

        next_index = path_prefix + candidate_value

        # if the entry ends with a '/', we know its a folder, so list out all entries
        # in this path and then use recursion to run this function against that entry
        if candidate_value.endswith('/'):

            next_value = client.secrets.kv.v2.list_secrets(path=next_index, \
                                                           mount_point=mount_point)

            recurse_through_secrets(next_index, next_value, mount_point)

        # if it doesn't end with a '/', we know its a secret so
        # we can read the data and print out the secrets safely
        else:
            final_value = client.read(mount_point + '/data/' + next_index)['data']['data']

            print ("\nvault kv put {0}/{1}".format(mount_point, next_index), end='')
            
            try:
                final_value = final_value.encode("utf-8")
            except AttributeError:
                final_value = final_value

            for secret in final_value:
               print (" '{0}={1}'".format(secret, final_value[secret]), end='')

            print ()

def main():
    assert client.is_authenticated()

    # try to set the mount point based off of env var; use `secret` as default
    mount_point = os.environ.get('VAULT_MOUNT_POINT', 'secret')

    # get initial entries of secrets of where we want to start
    top_level_keys = client.secrets.kv.v2.list_secrets(path='', mount_point=mount_point)
    top_vault_prefix = ''

    recurse_through_secrets(top_vault_prefix, top_level_keys, mount_point)

if __name__ == '__main__':
    main()