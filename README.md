# 🚀 Backend API — ItMax

### Desenvolvido por developer Italo Rodri.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green?style=for-the-badge&logo=fastapi)
![Firebase](https://img.shields.io/badge/Firebase-Firestore%20%26%20Storage-orange?style=for-the-badge&logo=firebase)
![Poetry](https://img.shields.io/badge/Poetry-Dependency%20Manager-purple?style=for-the-badge)

---

# ✨ Sobre o Projeto

Backend desenvolvido com **FastAPI** para gerenciamento de filmes, upload de imagens e integração com serviços Firebase.

A API foi construída com foco em:

- ⚡ Alta performance
- 🧱 Arquitetura organizada
- 🔥 Integração com Firebase
- 🧪 Testes automatizados
- 📦 Gerenciamento moderno de dependências
- 🚀 Escalabilidade

---

# 📋 Pré-requisitos

Antes de iniciar o projeto, certifique-se de possuir:

- Python 3.11+
- Poetry
- Arquivo `serviceAccountKey.json` na raiz do projeto

---

# ⚙️ Como Rodar o Projeto

## 1️⃣ Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
```

---

## 2️⃣ Instalar dependências

```bash
poetry install
```

---

## 3️⃣ Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
FIREBASE_BUCKET_NAME=""

ONESIGNAL_APP_ID=""

ONESIGNAL_REST_KEY=""
```

---

## 4️⃣ Iniciar servidor de desenvolvimento

Rodar localmente:

```bash
python -m poetry run uvicorn main:app --app-dir src --reload
```

Rodar na rede privada:

```bash
python -m poetry run uvicorn main:app --app-dir src --reload --host 0.0.0.0 --port 8000
```

---

# 📚 Documentação da API

## Swagger Docs

```txt
http://127.0.0.1:8000/docs
```

---

# 🌐 Endpoints Principais

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/api/v1/movies` | Cria filme com upload de imagem |
| GET | `/api/v1/movies` | Lista todos os filmes cadastrados |
| GET | `/` | Healthcheck da API |

---

# 🧱 Estrutura do Projeto

```plaintext
backend-python/
├── src/
│   ├── core/
│   ├── modules/
│   ├── routes/
│   ├── services/
│   └── main.py
│
├── tests/
│
├── .env
├── serviceAccountKey.json
├── pyproject.toml
└── README.md
```

---

# 🛠️ Tecnologias Utilizadas

- FastAPI
- Firebase Firestore
- Firebase Storage
- Python
- Poetry
- Loguru
- Pytest

---

# 🧪 Testes Unitários

## Instalar dependências de testes

```bash
poetry add pytest pytest-asyncio --group dev
```

---

## Executar testes

```bash
python -m poetry run pytest
```

---

# 📄 Logs da Aplicação

## Instalar Loguru

```bash
poetry add loguru
```

---

## Estrutura sugerida

```plaintext
src/core/logging.py
```

---

# ⚙️ Configuração do Python no Poetry

Atualizar versão no `pyproject.toml`:

```toml
requires-python = ">=3.11,<4.0"
```

---

# 🔄 CI/CD — GitHub Actions

Estrutura recomendada:

```plaintext
.github/workflows/main.yml
```

---

# 👨‍💻 Autor

## DEV Italo Rodri.

Desenvolvedor Full Stack especializado em:

- Flutter
- FastAPI
- Firebase
- Riverpod
- Arquitetura Escalável
- APIs REST
- Clean Architecture

---

# 📄 Licença

Projeto desenvolvido para fins de estudo e portfólio.
```