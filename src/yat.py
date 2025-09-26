import requests, click
from utils import *

@click.group()
def yat():
    pass


@yat.command()
@click.argument('url')
@click.argument('token')
def session(url, token):
    if not url_exists(url):
        click.echo("URL não exsite.")
        return
    
    link, endpoint = root_link(url)
    if session_exists(link):
        cursor.execute("UPDATE sessions SET token = (?), endpoint = (?) WHERE url = (?)", (token, endpoint, link))
        click.echo("SESSÃO ATUALIZADA.")
    else:
        cursor.execute("INSERT INTO sessions (url, endpoint, token) VALUES (?, ?, ?)", (link, endpoint, token,))
        click.echo("SESSÃO CRIADA.")

    conn.commit()


@yat.command()
@click.argument('url')
@click.option('-h', flag_value = True, default = False, help = 'Inclui busca de token registrado no banco de sessões.')
def get(url, h):
    headers = {}
    if h:
        headers = assemble_header(url)

    response = requests.get(url, headers = headers)

    click.echo(response.status_code)
    click.echo(response.json())


@yat.command()
@click.argument('url')
@click.argument('json', nargs = -1)
@click.option('-h', flag_value = True, default = False, help = 'Inclui busca de token registrado no banco de sessões.')
def post(url, json, h):
    data = {}
    for attr in json:
        key, value = attr.split(':', 1)
        data[key.strip()] = value.strip()
    
    headers = {}
    if h:
        headers = assemble_header(url)

    response = requests.post(
        url, json = data, headers = headers, 
    )

    click.echo(response.status_code)
    click.echo(response.json())


@yat.command()
@click.argument('url')
@click.option('-h', flag_value = True, default = False, help = 'Inclui busca de token registrado no banco de sessões.')
def delete(url, h):
    headers = {}
    if h:
        headers = assemble_header(url)
    
    response = requests.delete(
        url, headers = headers
    )

    click.echo(response.status_code)
    click.echo(response.json())


@yat.command()
@click.argument('url')
@click.argument('json', nargs = -1)
@click.option('-h', flag_value = True, default = False, help = 'Inclui busca de token registrado no banco de sessões.')
def update(url, json, h):
    data = {}
    for attr in json:
        key, value = attr.split(':', 1)
        data[key.strip()] = value.strip()

    headers = {}
    if h:
        headers = assemble_header(url)
    
    response = requests.put(url, json = data, headers = headers)

    click.echo(response.status_code)
    click.echo(response.json())


if __name__ == '__main__':
    yat()
