#!/usr/bin/python3
import os
import click

@click.command()
@click.option("--username", prompt="Your Snark Ai username: ", help="Provide your username")
@click.option("--password", prompt="Your Snark Ai password: ", help="Provide your password")
def hello(username, password):
    home = os.path.expanduser("~")
    if not os.path.exists(f"{home}/.snark"):
        os.mkdir(f"{home}/.snark")
    with open(f'{home}/.snark/account', "w") as f:
        f.write(f"username = {username}\n")
        f.write(f"password = {password}\n")


    

# if __name__ == '__main__':
#     hello()