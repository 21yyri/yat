import requests, click, os, json
from utils import *

@click.group()
def yat():
    pass


@yat.command()
@click.argument('url')
@click.argument('token')
@click.option('--prefix')
def auth(url, token, prefix = None):
    if not url_exists(url):
        click.echo("URL não existe.")
        return
    
    link, endpoint = root_link(url)

    if not prefix:
        prefix = 'Bearer'
    
    if session_exists(link):
        cursor.execute("UPDATE sessions SET token = (?), prefix = (?) WHERE url = (?)", (token, prefix, link,))
        click.echo("Sessão atualizada.")
    else:
        cursor.execute("INSERT INTO sessions (url, prefix, token) VALUES (?, ?, ?)", (link, prefix, token,))
        click.echo("Sessão criada.")

    conn.commit()


@yat.command()
@click.option('--method', multiple = True)
@click.option('--last', type = int)
@click.option('--status', type = int)
@click.option('--clean', is_flag = True)
def history(method = None, last = None, status = None, clean = False):
    if clean:
        clean_history()
        click.echo("Limpando histórico...")

        return
    
    click.echo("Lendo histórico...")
    ensure_history_exists()

    with open("../data/history.json", 'r') as file:
        history = file.read()
        json_data = json.loads(history)
    

    if method:
        method = tuple([m.upper() for m in method])
        json_data = [log for log in json_data if log.get("method") in method]
    
    if status:
        json_data = [log for log in json_data if log.get("status") == status]

    if last:
        json_data = json_data[::-1][:last]
    
    for log in json_data:
        click.echo(format_log(log))


@yat.command()
@click.argument('url')
@click.option('--auth', flag_value = True, default = False, help = 'Inclui busca de token registrado no banco de sessões.')
def get(url, auth):
    headers = {}
    if auth:
        headers = assemble_header(url)

    try:
        response = requests.get(url, headers = headers)
        click.echo(status_message(response.status_code))
        log_request(response)
        try:
            json_data = json.dumps(response.json(), indent = 4)
            click.echo(f"JSON: {json_data}")
        except requests.exceptions.JSONDecodeError:
            pass
    except requests.exceptions.ConnectionError:
        click.echo("Domínio não existe.")


@yat.command()
@click.argument('url')
@click.argument('args', nargs = -1)
@click.option('--auth', flag_value = True, default = False, help = 'Inclui busca de token registrado no banco de sessões.')
def post(url, args, auth):
    data = {}
    for arg in args:
        key, value = arg.split("=")
        data[key.strip()] = value.strip()
    
    headers = {}
    if auth:
        headers = assemble_header(url)

    try:
        response = requests.post(url, json = data, headers = headers)
        click.echo(status_message(response.status_code))
        log_request(response)
        try:
            json_data = json.dumps(response.json(), indent = 4)
            click.echo(f"JSON: {json_data}")
        except requests.exceptions.JSONDecodeError:
            pass
    except requests.exceptions.ConnectionError:
        click.echo("Domínio não existe.")


@yat.command()
@click.argument('url')
@click.option('--auth', flag_value = True, default = False, help = 'Inclui busca de token registrado no banco de sessões.')
def delete(url, auth):
    headers = {}
    if auth:
        headers = assemble_header(url)
    
    try:
        response = requests.delete(url, headers = headers)
        click.echo(status_message(response.status_code))
        log_request(response)
        try:
            json_data = json.dumps(response.json(), indent = 4)
            click.echo(f"JSON: {json_data}")
        except requests.exceptions.JSONDecodeError:
            pass
    except requests.exceptions.ConnectionError:
        click.echo("Domínio não existe.")


@yat.command()
@click.argument('url')
@click.argument('args', nargs = -1)
@click.option('--auth', flag_value = True, default = False, help = 'Inclui busca de token registrado no banco de sessões.')
def put(url, args, auth):
    data = {}
    for arg in args:
        key, value = arg.split("=")
        data[key.strip()] = value.strip()
    
    headers = {}
    if auth:
        headers = assemble_header(url)

    try:    
        response = requests.put(url, json = data, headers = headers)
        click.echo(status_message(response.status_code))
        log_request(response)
        try:
            json_data = json.dumps(response.json(), indent = 4)
            click.echo(f"JSON: {json_data}")
        except requests.exceptions.JSONDecodeError:
            pass
    except requests.exceptions.ConnectionError:
        click.echo("Domínio não existente.")


@yat.command()
@click.argument('url')
@click.argument('args', nargs = -1)
@click.option('--auth', flag_value = True, default = False, help = 'Inclui busca de token registrado no banco de sessões.')
def patch(url, args, auth):
    data = {}
    for attr in args:
        key, value = attr.split(':', 1)
        data[key.strip()] = value.strip()

    headers = {}
    if auth:
        headers = assemble_header(url)
    
    try:
        response = requests.patch(url, json = data, headers = headers)
        click.echo(status_message(response.status_code))
        log_request(response)
        try:
            json_data = json.dumps(response.json(), indent = 4)
            click.echo(f"JSON: {json_data}")
        except requests.exceptions.JSONDecodeError:
            pass
    except requests.exceptions.ConnectionError:
        click.echo("Domínio não existente.")


if __name__ == '__main__':
    yat()
