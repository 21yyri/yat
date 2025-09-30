import requests, sqlite3
from datetime import datetime
from urllib.parse import urlparse
import json, os

conn = sqlite3.connect("../data/yat.db")
cursor = conn.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS sessions (url TEXT, prefix TEXT, token TEXT)"
)

def root_link(url: str) -> tuple[str]:
    """Recebe uma URL e separa o link principal de seu endpoint."""
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}", parsed_url.path


def get_session(url: str) -> str | None:
    """Retorna o último token registrado para a URL recebida."""

    result = cursor.execute(
        "SELECT token, prefix FROM sessions WHERE url = (?)", (url,)
    ).fetchone()
    if not result:
        return
    
    return result


def url_exists(url: str) -> bool:
    """Verifica a existência da URL."""
    try:
        req = requests.head(url)
    except requests.exceptions.ConnectionError:
        return False
    return True


def session_exists(url: str) -> bool:
    """Verifica se a sessão já existe no banco de sessões."""
    
    link = cursor.execute("SELECT * FROM sessions WHERE url = (?)", (url,)).fetchone()
    if not link:
        return False
    return True


def assemble_header(url: str) -> dict:
    """Pega uma URL do banco e retorna um header com o token associad a URL."""

    link, endpoint = root_link(url)
    session = get_session(link)
    if session:
        token, prefix = session
        return {
            "Authorization": f"{prefix} {token}"
        }
    
    return {}


def response_code_output(status: int) -> str:
    """Colore o código no terminal."""
    match str(status)[0]:
        case '2':
            return f'\033[92m[{status}]\033[0m'
        case '3':
            return f'\033[94m[{status}]\033[0m'
        case '4':
            return f'\033[91m[{status}]\033[0m'
        case '5':
            return f'\033[33m[{status}]\033[0m'


def status_message(status: int) -> str:
    message = ''
    if status == 200:
        message = 'OK: requisição foi feita com sucesso.'
    elif status == 201:
        message = 'Created: novo recurso criado.'
    elif status == 204:
        message = 'No Content: requisição concluída, mas não trouxe conteúdo.'
    elif status == 301:
        message = 'Moved Permanently: recurso movido para nova URL.'
    elif status == 302:
        message = 'Temporary Redirect: redirecionamento temporário para nova URL.'
    elif status == 400:
        message = 'Bad Request: servidor não pôde processar a requisição.'
    elif status == 401:
        message = 'Not Authorized: cliente deve estar autênticado para concluir a requisição.'
    elif status == 403:
        message = 'Forbidden: cliente não tem autorização para acessar este recurso.'
    elif status == 404:
        message = 'Not Found: servidor não pôde encontrar o recurso.'
    elif status == 500:
        message = 'Internal Server Error: servidor encontrou uma condição não esperada.'
    elif status == 503:
        message = 'Service Unavaliable: servidor inapto a processar a requisição devido a grande fluxo de requisições ou manutenção agendada.'
    
    return f"{response_code_output(status)} {message}"


def ensure_history_exists():
    if not os.path.isfile("../data/history.json"):
        with open("../data/history.json", "w") as file:
            file.write(json.dumps([]))


def log_request(response: requests.models.Response):
    ensure_history_exists()

    request: dict = {
        "datetime": f"[{datetime.now()}]",
        "method": response.request.method,
        "url": response.request.url,
        "status": response.status_code
    }

    with open("../data/history.json", 'r') as history:
        history_json: list[dict] = json.load(history)

    history_json.append(request)

    with open('../data/history.json', 'w') as history:
        history_json = json.dumps(history_json, indent = 4)
        history.write(history_json)


def format_log(log):
    return f"{log.get('datetime')} {log.get('method')} {log.get('url')} -> {log.get('status')}"


def clean_history():
    with open("../data/history.json", "w") as file:
        file.write(json.dumps([]))
