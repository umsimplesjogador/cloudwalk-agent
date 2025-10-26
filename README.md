# Cloud Agent

## Descrição
Multi-agent system em FastAPI com Router Agent, Knowledge Agent (RAG) e Support Agent.
Integrado com Google Gemini API (via variável de ambiente).
Agente conversacional que responde perguntas sobre a Cloudwalk e seus produtos.

## Deploy
- CI/CD via GitHub Actions
- Hospedado no Render
- Docker multi-stage

## Segurança
- A chave GEMINI_API_KEY é armazenada como Secret (GitHub Actions e Render).

## Passos principais
1. Secrets configurados no GitHub (`GEMINI_API_KEY`, `DOCKER_USERNAME`, `DOCKER_PASSWORD`, `RENDER_API_KEY`, `RENDER_SERVICE_ID`).
2. Configurada `GEMINI_API_KEY` no Render em Environment Variables.
3. Rode o workflow para buildar e deployar.

## Endpoints
- `POST /api/message` -> processa mensagens pelo Agent Swarm.



## 🚀 Rodando localmente com Docker

### 1️⃣ Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) instalado
- Chave da API Gemini (`GEMINI_API_KEY`)
- Clonar este repositório:


git clone https://github.com/umsimplesjogador/cloudwalk-agent.git
cd cloudwalk-agent



---

## 🛠 Instruções para rodar o projeto localmente sem Docker

### Instal as dependências

pip install -r requirements.txt


### Criar arquivo `.env`

Na raiz do projeto, crie o arquivo `.env` com sua chave da Gemini API:

GEMINI_API_KEY=sua_chave_aqui


### Execute a aplicação

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


### Acesse a aplicação:

Frontend chat: http://localhost:8000/chat

Swagger UI: http://localhost:8000/docs


## Rodar com Docker

1- Construir a imagem
2- Na raiz do projeto, execute: docker build -t cloudwalk-agent .
3- Execute o container: docker run -p 10000:8000 --env GEMINI_API_KEY="sua_chave_aqui" cloudwalk-agent
4- Acessar a aplicação em: Frontend chat: http://localhost:8000/chat e Swagger UI: http://localhost:8000/docs


### Encerrar o container

docker ps          # lista containers em execução
docker stop <ID>   # encerra container


## CI/CD (GitHub Actions + DockerHub + Render)


O projeto possui workflow deploy.yml configurado:

Executa testes com pytest

Constrói a imagem Docker

Faz push para DockerHub

Realiza deploy no Render

Secrets necessários:

DOCKER_USERNAME → usuário DockerHub

DOCKER_PASSWORD → senha DockerHub

RENDER_SERVICE_ID → ID do serviço no Render

RENDER_API_KEY → API key do Render


## Dicas

Sempre use variáveis de ambiente para proteger sua chave da Gemini API.

Para atualizar o agente, reconstrua a imagem Docker.

Para acompanhar logs em tempo real: docker logs -f <CONTAINER_ID>

O chat HTML consome o endpoint /process.

Teste endpoints rapidamente pelo Swagger UI /docs.





## Sample Conversations:

1) Você: quais são os produtos da cloudwalk?

Agente:
Os produtos da Cloudwalk são:

* JIM
* InfinitePay
* STRATUS



2) Você: qual é a missão da cloudwalk?

Agente:
Nossa missão é criar a melhor rede de pagamentos na Terra. E então, em outros planetas. Estamos democratizando a indústria financeira, capacitando empreendedores por meio de soluções tecnológicas, inclusivas e que transformam vidas.

A indústria de pagamentos no planeta Terra e por que o preço importa:

A indústria de pagamentos está evoluindo. Mas os vendedores não estão colhendo os benefícios das guerras de preços entre os grandes bancos e adquirentes. No final, as "novas" medidas e soluções raramente beneficiam os vendedores, que muitas vezes são os que mais sofrem, prejudicando a economia.

É hora de mudar. Nossa missão é superar o sistema, construindo um novo que seja justo para todos os envolvidos.



3) Você: quais são os pilares da cloudwalk?

Agente:
Os pilares da Cloudwalk são:

* **Best Product (Melhor Produto):** Entregamos nossos serviços com os mais altos padrões tecnológicos, com IA e Blockchain, combinados com uma experiência de usuário de primeira linha.
* **Customer Engagement (Engajamento do Cliente):** Nossos clientes desempenham um papel vital em tudo o que fazemos. Eles são nossos melhores promotores de vendas e também detêm a capacidade de mudar o produto e o negócio a qualquer momento.
* **Disruptive Economics (Economia Disruptiva):** Nosso objetivo é oferecer o melhor preço para nossos clientes, para ajudá-los a liberar o poder de compra. Projetamos nosso modelo de negócios para transformar a maneira como os comerciantes vendem e lucram.



4) Você: fale sobre o produto infinitepay

Agente:
A InfinitePay é uma plataforma financeira que oferece diversos produtos, incluindo:

* **Maquininha:** Permite vendas no Pix, débito e no crédito à vista ou parcelado, inserindo o cartão ou por aproximação (NFC).
* **InfiniteTap:** Transforma seu celular com NFC em uma maquininha de cartão.
* **Link de pagamento:** Permite criar e compartilhar links de cobrança com seus clientes.
* **Pix:** Receba pagamentos instantâneos com taxa zero.

Além disso, a InfinitePay oferece:

* Conta digital para receber os valores das vendas.
* Empréstimo sem burocracia para investir no seu negócio.
* Suporte com alta avaliação (RA 1000).
* Taxas menores que a concorrência.
* Recebimento na hora ou em 1 dia útil.
