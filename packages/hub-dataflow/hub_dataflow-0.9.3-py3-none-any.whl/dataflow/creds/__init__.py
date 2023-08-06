from .creds import Creds
from .aws import AWSSecretsManager

if __name__ == "__main__":
    Creds("snarkai")
    AWSSecretsManager()
