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
        link, endpoint = root_link(url)
        token = get_session(link)

        headers = {
            "Authorization": f"Bearer {token}"
        }

    response = requests.get(url, headers = headers)

    click.echo(response.status_code)
    click.echo(response.json())


@yat.command()
@click.argument('url')
@click.argument('json', nargs = -1)
def post(url, json):
    data = {}
    for attr in json:
        key, value = attr.split(':', 1)
        data[key.strip()] = value.strip()
    
    sess = cursor.execute("SELECT * FROM sessions").fetchall()
    header = {}
    if sess:
        for key in sess:
            if not url.startswith(sess[0]):
                continue
            link, token = key
        header = {'Authorization': f'Bearer {token}'}
    
    response = requests.post(
        url, json = data, headers = header or None
    )

    click.echo(response.status_code)
    click.echo(response.json())


if __name__ == '__main__':
    yat()
