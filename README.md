Claro! Aqui está o README.md completo atualizado para o seu projeto, já refletindo a estrutura que você enviou:

```markdown
# Sistema de Gestão de Biblioteca Escolar

## Descrição do Projeto
Este projeto consiste em um **Sistema de Gestão de Biblioteca Escolar**, desenvolvido com **Python, Django e MySQL**, com o objetivo de facilitar o gerenciamento de livros, alunos, empréstimos e devoluções em uma biblioteca escolar. O sistema permite o controle eficiente do acervo, histórico de empréstimos e geração de relatórios para a equipe responsável.

O desenvolvimento segue metodologias ágeis, garantindo entregas rápidas e iterativas, com foco na qualidade e na experiência do usuário (UX/UI).

---

## Tecnologias Utilizadas
- **Back-end:** Python, Django  
- **Banco de Dados:** MySQL  
- **Front-end / UX/UI:** HTML, CSS, JavaScript, Bootstrap (integrados ao Django)  
- **Design de Interfaces:** Figma  
- **Gerenciamento de Tarefas:** Trello  
- **Metodologias Ágeis:** Scrum, RAD (Rapid Application Development)  

---

## Funcionalidades
- Cadastro e gerenciamento de livros e suas categorias  
- Controle de cadastro de alunos e usuários  
- Empréstimos e devoluções de livros com registro histórico  
- Consulta de disponibilidade de livros em tempo real  
- Emissão de relatórios de empréstimos, devoluções e livros disponíveis  

---

## Instalação e Configuração

1. Clone o repositório:
```bash
git clone https://github.com/seuusuario/biblioteca_escolar.git
cd biblioteca_escolar
````

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure o banco de dados MySQL no arquivo `config/settings.json` ou diretamente no `settings.py`, conforme sua arquitetura.

5. Execute as migrações para criar as tabelas no banco:

```bash
python manage.py migrate
```

6. Crie um superusuário para acessar o painel administrativo:

```bash
python manage.py createsuperuser
```

7. Inicie o servidor localmente:

```bash
python manage.py runserver
```

8. Acesse o sistema no navegador:

```
http://127.0.0.1:8000
```

---

## Metodologia de Desenvolvimento

* **Scrum:** Utilizamos sprints curtos para planejamento, reuniões diárias e entregas contínuas.
* **RAD (Rapid Application Development):** Foco na prototipagem rápida e feedback constante para ajustes imediatos.
* **Trello:** Controle e acompanhamento das tarefas e backlog do projeto.
* **Figma:** Design das interfaces e protótipos para garantir uma ótima experiência do usuário (UX/UI).

---

## Contribuição

Contribuições são muito bem-vindas! Para colaborar com o projeto:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature:

   ```bash
   git checkout -b feature/nova-funcionalidade
   ```
3. Faça commit das alterações:

   ```bash
   git commit -m "Adiciona nova funcionalidade"
   ```
4. Envie para o seu repositório remoto:

   ```bash
   git push origin feature/nova-funcionalidade
   ```
5. Abra um Pull Request para revisão.

---

## Contato

* Desenvolvido por: **Eduardo Galvão, Daniel David e Murilo Chagas**
* Repositório GitHub: **https://github.com/eduardocgalvao/sistema-biblioteca**

---

## Licença

Este projeto está licenciado sob a **MIT License**.

```
