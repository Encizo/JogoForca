# 🎯 Jogo da Forca - Django

Este é um projeto web do **Jogo da Forca** desenvolvido com Django, que permite:
- Professores criarem **temas e palavras**
- Alunos jogarem com ou sem login
- Visualizar relatórios de partidas
- Gerar PDFs de atividades
- Jogar partidas interativas com desenho da forca

## 🚀 Funcionalidades

- ✅ Cadastro e autenticação de usuários (professores e alunos)
- ✅ Professores podem:
  - Criar temas e palavras
  - Visualizar relatório de partidas por tema e período
  - Gerar PDF de atividades
  - Excluir palavras e temas
- ✅ Alunos (com ou sem login) podem:
  - Escolher temas e jogar
  - Visualizar dicas
- ✅ Sistema de partidas com:
  - Desenho da forca SVG conforme os erros
  - Registro de tentativas e acertos
- ✅ Filtro de temas por nome ou professor

## 🛠️ Tecnologias

- Python 3.10+
- Django 4+
- SQLite (ou MySQL compatível)
- Bootstrap 5
- `xhtml2pdf` para geração de PDF

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/jogo-da-forca-django.git
cd jogo-da-forca-django
```
2. Crie e ative o ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```
3. Instale as dependências:

```bash
pip install -r requirements.txt
```
4. Rode as migrações e crie um superusuário:

```bash
python manage.py migrate
python manage.py createsuperuser
```
5. Inicie o servidor:

```bash
python manage.py runserver
```

