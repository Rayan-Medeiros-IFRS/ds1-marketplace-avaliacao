# Marketplace API em Django REST Framework

Projeto desenvolvido para colocar em prática os principais conceitos do Django REST Framework (DRF), criando a estrutura de backend para um marketplace simples. A API conta com cadastro de vendedores, produtos, controle de pedidos, autenticação via JWT e relatórios agregados.

### O que foi implementado no projeto

• Modelos e Relacionamentos: Estrutura completa com perfil de vendedor (1:1 com o usuário do Django), produtos (com tags via ManyToMany) e pedidos com itens em tabela intermediária.
• Baixa de Estoque Automática (Signal): Toda vez que um item é adicionado a um pedido, um signal (`post_save`) desconta automaticamente a quantidade comprada do estoque do produto.
• Filtro Customizado (Custom Manager): Criado o método `disponiveis()` no manager de produtos para filtrar rápido apenas itens ativos e com estoque maior que zero.
• Relatório de Faturamento (ORMs Avançados): Endpoint especial que usa `annotate`, `Sum` e `F` para calcular o valor total vendido por cada loja.
• Serializer Aninhado (Nested): O endpoint de pedidos já devolve a lista completa dos seus itens formatada dentro do próprio JSON.
• Autenticação Segura: Login e renovação de acesso via tokens JWT com a biblioteca `simplejwt`. Rotas sensíveis (como a de pedidos) exigem autenticação.

### Como rodar o projeto localmente

Para colocar a API para rodar no seu computador, basta seguir este passo a passo rápido no terminal:

• 1. Clonar o repositório: `git clone <URL_DO_REPOSITORIO>` e entrar na pasta do projeto com `cd <NOME_DA_PASTA>`.
• 2. Criar e ativar o ambiente virtual: `python -m venv venv` e depois `venv\Scripts\activate`
• 3. Instalar as dependências: `pip install django djangorestframework djangorestframework-simplejwt`
• 4. Aplicar as migrações no banco: `python manage.py makemigrations` e em seguida `python manage.py migrate`
• 5. Criar um superusuário para os testes: `python manage.py createsuperuser`
• 6. Subir o servidor: `python manage.py runserver`

A API fjca disponível no endereço `http://127.0.0.1:8000/api/`.

### Principais Endpoints da API

• `POST /api/token/` - Envia `username` e `password` para receber os tokens de acesso (`access` e `refresh`).
• `POST /api/token/refresh/` - Envia o token de `refresh` para gerar um novo token de acesso válido.
• `GET /api/vendedores/` - Lista todos os vendedores cadastrados.
• `GET /api/vendedores/relatorio-faturamento/` - Retorna a lista de vendedores com o cálculo do faturamento total de cada um.
• `GET` e `POST /api/produtos/` - Lista ou cadastra produtos no sistema.
• `GET /api/produtos/?apenas_disponiveis=true` - Usa o Custom Manager para listar apenas produtos em estoque.
• `GET` e `POST /api/pedidos/` - Consulta e criação de pedidos (rota protegida, requer token de autenticação).


### Como testar a autenticação no Postman ou Thunder Client

• 1. Teste de bloqueio: Tente fazer um `GET` para `http://127.0.0.1:8000/api/pedidos/` sem nenhum cabeçalho. A API deve retornar status `401 Unauthorized`.
• 2. Gerando o Token: Faça uma requisição `POST` em `http://127.0.0.1:8000/api/token/` passando o JSON do seu usuário e senha. Copie a chave `access` gerada.
• 3. Acessando a rota protegida: Volte para a requisição de `/api/pedidos/`, vá na aba de Headers e adicione `Authorization` com o valor `Bearer <SEU_TOKEN_ACCESS>`. Agora o acesso será liberado.