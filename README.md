# PerifaEnsina

**Um país onde todos aprendem!**

## Sobre o projeto

O PerifaEnsina nasceu como projeto de hackathon para enfrentar um problema concreto: a desigualdade no acesso à educação de qualidade, que atinge especialmente regiões periféricas do Brasil. Falta de professores capacitados e infraestrutura precária nas escolas públicas comprometem a formação dos alunos desde cedo, alimentando um ciclo de déficit educacional e desemprego.

A proposta do PerifaEnsina é uma aplicação web de formação continuada para professores da rede pública, ensinando metodologias ativas de ensino que facilitam a compreensão de conteúdo por alunos com base escolar deficiente. O objetivo final é duplo: melhorar a qualidade do ensino oferecido em sala e ampliar as oportunidades no mercado de trabalho — tanto para os professores quanto para os alunos.

## O que a plataforma oferece

- **Metodologias ativas de ensino** aplicadas e explicadas na prática (Design Thinking, Gamificação, Sala de Aula Invertida, Estudo de Casos, Seminários e Debates, entre outras)
- **Trilha de módulos** com acompanhamento de progresso para o usuário
- **Contas diferenciadas por perfil**: professor e aluno, cada uma com sua própria página inicial
- **Curso de formação continuada** voltado a professores de escolas públicas em regiões periféricas

## Stack utilizada

- **Backend:** Python + Flask
- **Banco de dados:** SQLite, via Flask-SQLAlchemy
- **Autenticação:** sessões Flask + hashing de senha com Werkzeug
- **Frontend:** HTML, CSS e JavaScript

## Como rodar o projeto localmente

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd PerifaEnsina

# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instale as dependências
pip install flask flask-sqlalchemy

# Rode a aplicação
python app.py
```

A aplicação sobe em `http://127.0.0.1:5000/`. No primeiro acesso, crie uma conta pela tela de cadastro escolhendo o perfil (professor ou aluno).

> ⚠️ Este projeto está em desenvolvimento ativo. Configurações sensíveis (como chave secreta e variáveis de ambiente) ainda estão sendo migradas para fora do código-fonte — não utilize esta versão em produção.

## Estrutura do projeto

```
PerifaEnsina/
├── app.py              # Aplicação Flask (rotas, modelos, lógica de negócio)
├── templates/           # Páginas HTML (login, cadastro, edição de conta, módulos)
├── static/               # CSS, JS e imagens
└── instance/            # Banco de dados local (não versionado)
```

## Equipe

Projeto criado por **Caio Henrique**, **Tarcísio Soares** e **Arthur Miguel**.

## Licença

Este projeto está licenciado sob a licença MIT — veja o arquivo [LICENSE](LICENSE) para mais detalhes.
