# YAT - Yet Another Terminal Http Client

Yat é uma ferramenta de linha de comando que permite o envio de requisições HTTP com acesso a persistência de tokens de autenticação e histórico de requisições.

Pensado para testar APIs REST de forma prática, rápida e limpa diretamente do terminal.

## Requisitos

- Python 3.10+
- pip (package manager)

## Instalando dependências
``
  bash
  pip install -r requirements.txt
``

Dependências usadas no projeto: click, pytest e requests.

## Comando principal

Adentre ao diretório ``src`` usando ``cd src`` no diretório do projeto.

``py yat.py method url data --auth``

O argumento ``method`` pode ser substituído por qualquer um dos verbos HTTP (GET, POST, PATCH, PUT, DELETE). O argumento ``url`` deve carregar a URL que deseja enviar a requisição. A partir desses dois, qualquer argumento no formato ``chave=valor`` será visto como um par de chave e valor a ser inseridos no corpo da requisição.

## Autenticação

O projeto inclui a possibilidade de incluir chaves ou tokens de autenticação dentro das headers sem a necessidade da escrita repetitiva para cada requisição.

``py yat.py auth url token --prefix``

O comando auth receberá a url, a qual deve ser constituída apenas por schema e domínio, seguida do token que o usuário deseja registrar e, por fim, o prefixo, a palavra que precede o token no cabeçalho da autenticação. Esse último tem valor padrão, que é "Bearer".

Ao registrar o token, cada requisição feita com a flag ``--auth`` incluirá o token automaticamente no cabeçalho.

## Exemplos de comandos

``py yat.py get https://suap.ifrn.edu.br/api/rh/eu --auth``

Essa requisição GET, considerando que o token ainda preserva sua validade, retornaria um código de status com mensagem e um corpo de requisição com os dados requisitados.

``py yat.py post https://suap.ifrn.edu.br/api/token/pair username=20241174010007 password=password``

Essa requisição POST, sem o argumento de autorização, retornaria o código e o corpo de requisição. O usuário poderia coletar o token recebido e registrar ele nas informações de autenticação.

## Histórico

O yat contém um registro de histórico para suas requisições.

``py yat.py history``

O comando levantaria todas as requisições registradas e formatadas no terminal. Alguns argumentos como ``--status``, ``--last`` e ``--method`` filtram suas requisições, respectivamente, pelo código, as últimas registradas e o método presente na requisição.

O argumento ``--clean`` pode limpar o histórico de requisições com o comando ``py yat.py history --clean``.

## Melhorias futuras

- Implementação de recuperação automática de token.
- Suporte a form data.
