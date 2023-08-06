import os
import click


@click.command()
@click.option("--username", prompt="Your Hub username: ", help="Provide your username")
@click.option("--password", prompt="Your Hub password: ", help="Provide your password")
def login(username, password):
    home = os.path.expanduser("~")
    if not os.path.exists(f"{home}/.snark"):
        os.mkdir(f"{home}/.snark")
    with open(f'{home}/.snark/account', "w") as f:
        f.write(f"username = {username}\n")
        f.write(f"password = {password}\n")