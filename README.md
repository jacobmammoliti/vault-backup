# vault-backup

Export secrets from HashiCorp Vault to a file. This script will output the appropriate `vault kv put` commands to restore secrets on a different Vault instance.

## Environment Variables

The script using the following environment variables:

| Variable           | Required              | Usage  |
| ------------------ |:---------------------:| :-----|
| VAULT_TOKEN        | yes                   | your Vault token, can be retrived by authenticating against vault |
| VAULT_ADDR         | yes                   | address of Vault |
| VAULT_MOUNT_POINT  | no (default: secrets) | name of kv secrets engine |


## Preping Python Environment

```bash
~] virutalenv -p python3 venv
~] . venv/bin/activate
~] pip install -r requirements.txt
```

## Example Usuage

### Export out of Vault
```bash
~] export VAULT_ADDR='https://vault.arctiq.ca'
~] export GITHUB_PAT=[redacted]
~] vault login -method=github token=${GITHUB_PAT}
~] export VAULT_TOKEN="$(cat ~/.vault-token)"
~] export VAULT_MOUNT_POINT = 'arctiq'
~] python main.py >> output.txt
```

### Import into new Vault
> **Note:** The Secrets Engine you exported must be created prior to running the Vault import. 
```bash
~] export VAULT_ADDR='https://new-vault.arctiq.ca'
~] vault login
~] . output.txt
```