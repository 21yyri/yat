import pytest
from src.utils import *

"""
    Comentar as linhas relacionadas a criação e gerenciamento de
    banco de dados no arquivo src/utils.py ao rodar os testes.
"""

def test_root_link():
    assert ("https://suap.ifrn.edu.br", "/api/token/pair") == root_link("https://suap.ifrn.edu.br/api/token/pair")
    assert ("https://google.com", '') == root_link("https://google.com")


def test_url_exists():
    assert url_exists("https://google.com") == True
    assert url_exists("http://testedefuncao.br") == False
    assert url_exists("https://amazon.com") == True
    assert url_exists("https://umaenormeperdadetempo.com") == False
