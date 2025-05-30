# **Documentação do Projeto**
## **Construir as Imagens do Docker**

Para construir as imagens do Docker a partir do `Dockerfile` e das configurações do `docker-compose.yml`, execute o seguinte comando no terminal:

```bash
  docker-compose build
  docker-compose up
```
## **Estrutura de Diretórios**

### 1. **Raiz do Projeto**
- **`docker-compose.yml`**: Arquivo de configuração para o Docker Compose.
- **`Dockerfile`**: Arquivo para construir a imagem do Docker.
- **`htmlcov/`**: Diretório gerado após a execução de testes, contendo relatórios de cobertura de código.
- **`infra/`**: Infraestrutura necessária para o funcionamento do sistema (ex: configuração do Loki, Prometheus).
- **`log_config.yaml`**: Arquivo de configuração para logs uvicorn.
- **`logs/`**: Diretório onde os logs da aplicação são armazenados.
- **`pyproject.toml`**: Arquivo de configuração do projeto Python.
- **`README.md`**: Arquivo com a documentação principal do projeto.
- **`tests/`**: Diretório contendo os testes da aplicação.

---

### 2. **Diretório `app/`**
Contém o código da aplicação principal.

- **`auth.py`**: Lógica de autenticação.
- **`clients.py`**: Manipulação dos dados dos clientes.
- **`middleware.py`**: Middleware para manipulação de requisições.
- **`products_mock.py`**: Dados de produtos mockados (fallback).
- **`schemas.py`**: Definições dos esquemas de dados (Pydantic).
- **`wishlist.py`**: Lógica da wishlist dos clientes.
- **`circuit_breaker.py`**: Lógica de Circuit Breaker para chamadas externas.
- **`database.py`**: Conexão e manipulação do banco de dados.
- **`main.py`**: Arquivo principal que inicializa a aplicação.
- **`models.py`**: Definições dos modelos de dados.
- **`token.py`**: Lógica de criação e verificação de tokens JWT.

---

### 3. **Diretório `htmlcov/`**
Relatórios gerados após a execução de testes com cobertura de código.

- **`index.html`**: Página inicial do relatório de cobertura.

---

### 4. **Diretório `infra/`**
Infraestrutura do sistema, incluindo configurações para Loki e Prometheus.

- **`loki/`**: Diretório com arquivos de configuração e cache do Loki.
- **`prometheus/`**: Contém a configuração para o Prometheus.
- **`loki-chunks/`**: Dados em chunks para o Loki.
- **`loki-config.yaml`**: Configuração para o Loki.
- **`promtail-config.yaml`**: Configuração para o Promtail.

---

### 5. **Diretório `logs/`**
Onde os logs da aplicação são armazenados.

- **`app.log`**: Log principal da aplicação.

---

### 6. **Diretório `tests/`**
Contém os testes automatizados.

- **`test_api.py`**: Testes para a API da aplicação.
- **`test_wishlist.py`**: Testes para a funcionalidade de wishlist.

---

## **Dependências e Links Úteis**

### Bibliotecas Usadas
- **FastAPI**: [Documentação FastAPI](https://github.com/fastapi/fastapi)
- **AIoBreaker** (Circuit Breaker): [GitHub AIoBreaker](https://github.com/arlyon/aiobreaker)
- **Beanie ODM** (para MongoDB): [Documentação Beanie](https://beanie-odm.dev/)
- **PyJWT** (para JWT): [Documentação PyJWT](https://pyjwt.readthedocs.io/en/stable/)
- **Prometheus FastAPI Instrumentator**: [GitHub Instrumentator](https://github.com/trallnag/prometheus-fastapi-instrumentator)
- **PassLib** (para criptografia de senhas): [Documentação PassLib](https://passlib.readthedocs.io/en/stable/narr/index.html)

### Links da aplicação
- **Uvicorn**: [Documentação do Uvicorn](https://www.uvicorn.org/)
- **Documentação Swagger da API**: [http://0.0.0.0:8001/docs](http://0.0.0.0:8001/docs)
- **Documentação Redoc da API**: [http://0.0.0.0:8001/redoc](http://0.0.0.0:8001/redoc)

### Para gerar token só usar a senha
- mysecretpassword

### Dashboard Prometheus
- **Prometheus Web Interface**: [http://localhost:3000/](http://localhost:3000/)
  - **Login**: admin / admin

---
