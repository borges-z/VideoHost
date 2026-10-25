# VideoHost

Plataforma web para upload, processamento e reprodução de vídeos usando **HTTP Live Streaming (HLS)**.

O VideoHost está em desenvolvimento e utiliza Flask para a aplicação web, SQLite para armazenar os dados e um worker escrito em C para processar os vídeos com auxílio do FFmpeg.

## Funcionalidades

- Cadastro e autenticação de usuários.
- Upload de vídeos.
- Listagem dos vídeos associados ao usuário.
- Processamento e segmentação de vídeos para HLS.
- Worker em C que consulta o banco de dados e identifica vídeos ainda não processados.
- Processamento individual dos vídeos para evitar executar vários trabalhos pesados simultaneamente.

## Tecnologias

- **Python / Flask** — aplicação web.
- **SQLite** — banco de dados local.
- **C** — worker de processamento.
- **FFmpeg** — processamento de mídia.
- **HLS** — entrega de vídeo segmentado.
- **Flask-Migrate / Alembic** — infraestrutura de migrações presente no projeto.

## Como funciona

1. O usuário cria uma conta e acessa a aplicação.
2. O usuário envia um vídeo pela interface web.
3. A aplicação registra as informações necessárias no banco de dados.
4. O worker em C consulta o banco e verifica quais vídeos ainda precisam ser processados.
5. O worker processa os vídeos pendentes **um por vez**, utilizando o FFmpeg para gerar os arquivos necessários à reprodução via HLS.
6. A aplicação pode listar os vídeos associados ao usuário.

O worker foi pensado para evitar o processamento simultâneo de vários vídeos, ajudando a limitar o consumo de recursos da máquina. O comportamento exato depende da implementação e da configuração do ambiente.

## Estrutura do projeto

```text
VideoHost/
├── app/
│   ├── forms/          # Formulários
│   ├── services/       # Serviços e regras da aplicação
│   ├── templates/      # Templates HTML
│   ├── uploads/        # Vídeos enviados e arquivos HLS gerados
│   ├── __init__.py     # Inicialização da aplicação
│   ├── modelos.py      # Modelos de dados
│   └── rotas.py        # Rotas Flask
├── instance/           # Dados locais, incluindo o banco SQLite
├── migrations/         # Migrações do banco de dados
├── worker/
│   ├── include/        # Cabeçalhos C
│   ├── src/            # Código-fonte do worker
│   └── Makefile        # Instruções de compilação
└── .gitignore
```

> Arquivos enviados, segmentos HLS, banco de dados local, ambiente virtual e artefatos compilados não devem ser versionados. A pasta `app/uploads/` é usada em tempo de execução.

## Requisitos

Antes de executar o projeto, prepare um ambiente com:

- Python 3.
- `pip` e suporte a ambientes virtuais do Python.
- Compilador C compatível com o código do worker.
- `make`, para utilizar o `Makefile` do worker.
- FFmpeg instalado e disponível no `PATH`.
- As dependências Python utilizadas pela aplicação.

As versões mínimas e exatas das ferramentas ainda precisam ser definidas pelo projeto.

## Configuração e execução

### 1. Obtenha o código

Clone o repositório ou baixe o código-fonte e entre na pasta do projeto.

### 2. Crie e ative um ambiente virtual Python

No Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências Python

Instale as dependências exigidas pela aplicação.

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

A aplicação utiliza SQLite por padrão, mas pode ser modificado para outros bancos de dados graças ao SQLAlchemy. nO projeto conterá uma pasta de migrações em `migrations/`; aplique as migrações conforme a configuração Flask-Migrate do projeto.

```bash
flask db init && flask db migrate && flask db upgrade
```

### 5. Inicie a aplicação Flask

Com o ambiente virtual ativado e as dependências instaladas, inicie a aplicação usando o comando Flask configurado para o projeto:

```bash
flask run
```

Se o Flask não localizar automaticamente a aplicação, configure a variável `FLASK_APP` de acordo com o ponto de entrada definido no código. O valor correto precisa ser confirmado na configuração do projeto.

### 6. Compile o worker em C

O worker possui um `Makefile` dentro da pasta `worker/`. Confira as instruções e os alvos definidos nesse arquivo e compile o programa a partir dessa pasta.

```bash
cd worker
make
```

O comando pressupõe que o `Makefile` define um alvo padrão. Caso contrário, utilize o alvo indicado no próprio arquivo.

### 7. Execute o worker

Depois de compilado, execute o worker conforme o nome e o modo de inicialização definidos no `Makefile` e no código-fonte. Ele consulta o banco de dados e processa individualmente os vídeos pendentes.

**Importante:** a aplicação Flask e o worker são componentes distintos. Iniciar o servidor Flask, por si só, não garante que o worker esteja em execução.

## Armazenamento e arquivos gerados

Os vídeos enviados e os arquivos produzidos pelo processamento HLS são armazenados em `app/uploads/`. O banco de dados local fica em `instance/`.

Esses diretórios contêm dados de execução e não devem ser usados como substitutos do código-fonte ou de backups. Em produção, defina uma política adequada de armazenamento, backup, limpeza de arquivos e controle de acesso.

## Estado do projeto

**Em desenvolvimento.**

Este repositório documenta o estado atual conhecido do VideoHost. Instruções de instalação, versões suportadas, configuração do banco e comandos exatos de inicialização ainda devem ser ajustados para corresponder à configuração final do projeto
