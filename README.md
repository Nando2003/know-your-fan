# Fúria - Know Your Fan

Este projeto é uma aplicação que combina Django e FastAPI para criar dashboards personalizados para fãs de e-sports. Ele utiliza OCR para validação de identidade, scraping de notícias e integração com o Twitter para calcular scores de engajamento.

## Funcionalidades

- **Validação de Identidade**: Processamento de RGs usando OCR.
- **Scraping de Notícias**: Coleta de notícias de e-sports de fontes como Dust2, ValorantZone e MaisEsports.
- **Integração com Twitter**: Coleta de interações do usuário com organizações de e-sports.
- **Dashboard Personalizado**: Exibição de score, notícias recomendadas e engajamento do fã.

## Pré-requisitos

- **Docker** e **Docker Compose** instalados.
- **Conta de administrador** para configurar times.

---

## Como Usar

### 1. Configuração Inicial

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   cd furia-know-your-fan
   ```

2. Certifique-se de que o Docker está instalado e em execução.

3. Crie o arquivo `.env` na pasta `dotenv_files` com base no exemplo `.env-example`:
   ```bash
   cp dotenv_files/.env-example dotenv_files/.env
   ```

4. Configure as variáveis de ambiente no arquivo `.env`.

---

### 2. Inicializando os Contêineres

1. **Inicie os serviços principais** (Django, Redis, PostgreSQL e FastAPI):
   ```bash
   docker-compose up django_app django_psql redis fastapi_app
   ```

2. **Aguarde os serviços principais estarem prontos**. Verifique os logs para garantir que não há erros.

3. **Inicie o serviço de scraping**:
   ```bash
   docker-compose up scheduler_scraper_app
   ```

---

### 3. Configuração no Django Admin

1. Acesse o painel de administração do Django:
   - URL: [http://localhost:3000/admin](http://localhost:3000/admin)
   - Usuário: `admin`
   - Senha: `admin` (ou a senha configurada).

2. Configure os seguintes itens:
   - **Times**: Adicione times de e-sports com seus respectivos logotipos e contas do Twitter.

---

### 4. Fluxo do Usuário

1. **Registro e Login**:
   - O usuário se registra e faz login na aplicação.

2. **Validação de Identidade**:
   - O usuário envia imagens do RG (frente e verso) para validação automática via OCR.

3. **Criação do Perfil de Fã**:
   - Após a validação, o usuário seleciona seu time favorito, jogos de interesse, eventos e compras.

4. **Dashboard**:
   - O sistema calcula o score do fã e exibe um dashboard com notícias recomendadas e engajamento.

---

## Comandos Úteis

- **Parar todos os contêineres**:
  ```bash
  docker-compose down
  ```

- **Recriar contêineres**:
  ```bash
  docker-compose up --build
  ```

- **Acessar logs de um serviço específico**:
  ```bash
  docker-compose logs <nome-do-serviço>
  ```

---

## Estrutura do Projeto

- **`django_app`**: Backend principal com Django.
- **`fastapi_app`**: Serviço de OCR com FastAPI.
- **`scheduler_scraper_app`**: Serviço de scraping de notícias.
- **`dotenv_files`**: Arquivos de configuração `.env`.

---

## Observações

- Certifique-se de que as variáveis de ambiente no `.env` estão corretas.
- O serviço de scraping deve ser iniciado por último para evitar erros de dependência.
- Para mais informações, consulte os arquivos de código e a documentação inline.

---
