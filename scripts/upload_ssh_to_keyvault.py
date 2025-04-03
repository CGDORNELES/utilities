"""
DISCLAIMER:
This script is provided "as-is" without any warranties. Use at your own risk.

It is intended for educational and operational use in Azure environments that support Managed Identity or Azure CLI authentication.
Make sure your Key Vault permissions are properly configured before execution.

The generated private key is handled in memory only. If you intend to persist it locally, implement secure storage mechanisms.
Never expose or log private keys in plain text in production environments.
"""

import argparse
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def generate_ssh_key_pair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key = private_key.public_key()
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH
    )
    return private_bytes.decode("utf-8"), public_bytes.decode("utf-8")

def upload_to_keyvault(vault_name, public_secret_name, private_secret_name, private_key, public_key):
    vault_url = f"https://{vault_name}.vault.azure.net/"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)

    print(f"Storing private key as '{private_secret_name}'...")
    client.set_secret(private_secret_name, private_key)

    print(f"Storing public key as '{public_secret_name}'...")
    client.set_secret(public_secret_name, public_key)

    print("SSH key pair successfully uploaded to Key Vault.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an SSH key pair and upload it to Azure Key Vault using DefaultAzureCredential.")
    parser.add_argument("--vault-name", required=True, help="Name of the Azure Key Vault (e.g., my-keyvault)")
    parser.add_argument("--key-name", required=True, help="Base prefix for key names (used if secret names are not specified)")
    parser.add_argument("--public-secret-name", help="Custom secret name for the public key")
    parser.add_argument("--private-secret-name", help="Custom secret name for the private key")

    args = parser.parse_args()

    public_secret = args.public_secret_name or f"{args.key_name}-public"
    private_secret = args.private_secret_name or f"{args.key_name}-private"

    print("Generating SSH key pair...")
    private_key, public_key = generate_ssh_key_pair()

    print("Uploading to Azure Key Vault...")
    upload_to_keyvault(args.vault_name, public_secret, private_secret, private_key, public_key)
