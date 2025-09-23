import requests, sqlite3

conn = sqlite3.connect("../yat.db")
cursor = conn.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS sessions (url TEXT, endpoint TEXT, token TEXT)"
)


def root_link(url: str) -> tuple[str]:
    """Recebe uma URL e separa o link principal de seu endpoint."""

    link = endpoint = ''

    count = 0
    for char in url:
        if count < 3:
            link += char
            if char == '/':
                count += 1
        elif count >= 3:
            endpoint += char
    
    return link, endpoint


def get_session(url: str) -> str | None:
    """Retorna o último token registrado para a URL recebida."""

    token = cursor.execute(
        "SELECT token FROM sessions WHERE url = (?)", (url,)
    ).fetchone()
    if not token:
        return
    
    return token[0]


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
    token = get_session(link)
    if token:
        return {
            "Authorization": f"Bearer {token}"
        }
    return {}

