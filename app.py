from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'chave-secreta-aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    cargo = db.Column(db.String(20), nullable=False)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def checar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

class ModuloConcluido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    nome_modulo = db.Column(db.String(100), nullable=False)
    data_conclusao = db.Column(db.DateTime, nullable=False)
    usuario = db.relationship('Usuario', backref=db.backref('modulos_concluidos', lazy=True))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    if 'usuario_id' in session:
        if session.get('usuario_cargo') == 'professor':
            return render_template('home1.html', nome=session.get('usuario_nome'))
        elif session.get('usuario_cargo') == 'aluno':
            return render_template('home2.html', nome=session.get('usuario_nome'))
    return redirect('/login')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        cargo = request.form.get('tipo_conta')

        if Usuario.query.filter_by(email=email).first() or Usuario.query.filter_by(nome=nome).first():
            flash('Usuário já cadastrado!')
            return redirect('/cadastro')

        usuario = Usuario(nome=nome, email=email, cargo=cargo)
        usuario.set_senha(senha)
        db.session.add(usuario)
        db.session.commit()
        flash('Cadastro realizado com sucesso! Faça login.')
        return redirect('/login')
    return render_template('cadastro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario:
            flash('Usuário não está cadastrado!')
            return redirect('/login')
        if usuario.checar_senha(senha):
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            session['usuario_cargo'] = usuario.cargo
            if usuario.cargo == 'aluno':
                return redirect('/aluno')
            elif usuario.cargo == 'professor':
                return redirect('/professor')
        else:
            flash('Email ou senha inválidos.')
            return redirect('/login')
    return render_template('login.html')

@app.route('/editar', methods=['GET', 'POST'])
def editar():
    if 'usuario_id' not in session:
        return redirect('/login')
    usuario = Usuario.query.get(session['usuario_id'])
    if request.method == 'POST':
        acao = request.form.get('acao')
        if acao == 'excluir':
            try:
                tipo = usuario.cargo
                
                ModuloConcluido.query.filter_by(usuario_id=usuario.id).delete()
                db.session.delete(usuario)
                db.session.commit()
                session.clear()
                flash('Conta excluída com sucesso!')
                if tipo == 'professor':
                    return redirect('/professor')
                else:
                    return redirect('/aluno')
            except Exception as e:
                flash('Falha ao excluir a conta.')
                return redirect('/editar')
        else:
            try:
                nome = request.form.get('nome')
                email = request.form.get('email')
                senha = request.form.get('senha')
                cargo = request.form.get('tipo_conta')

                if email != usuario.email and Usuario.query.filter_by(email=email).first():
                    flash('Email já cadastrado!')
                    return redirect('/editar')
                usuario.nome = nome
                usuario.email = email
                usuario.cargo = cargo
                if senha:
                    usuario.set_senha(senha)
                db.session.commit()
                flash('Conta editada com sucesso!')

                if usuario.cargo == 'professor':
                    return redirect('/professor')
                else:
                    return redirect('/aluno')
            except Exception as e:
                flash('Falha ao editar a conta.')
                return redirect('/editar')
    return render_template('editar.html', usuario=usuario)

@app.route('/aluno', methods=['GET'])
def aluno():
    if 'usuario_id' not in session:
        return redirect('/login')
    if session.get('usuario_cargo') != 'aluno':
        return redirect('/login')
    return render_template('home2.html', nome=session.get('usuario_nome'))

@app.route('/professor', methods=['GET'])
def professor():
    if 'usuario_id' not in session:
        return redirect('/login')
    if session.get('usuario_cargo') != 'professor':
        return redirect('/login')
    return render_template('home1.html', nome=session.get('usuario_nome'))


@app.route('/introducao')
def introducao():
    return render_template('introducao.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Você foi desconectado.')
    return redirect('/login')

from datetime import datetime

@app.route('/concluir_modulo', methods=['POST'])
def concluir_modulo():
    if 'usuario_id' not in session:
        return 'erro', 401
    modulo = request.form.get('modulo')
    if not modulo:
        return 'erro', 400
    try:
        ja_concluido = ModuloConcluido.query.filter_by(usuario_id=session['usuario_id'], nome_modulo=modulo).first()
        if ja_concluido:
            return 'ok'  
        novo = ModuloConcluido(
            usuario_id=session['usuario_id'],
            nome_modulo=modulo,
            data_conclusao=datetime.now()
        )
        db.session.add(novo)
        db.session.commit()
        return 'ok'
    except Exception as e:
        return 'erro', 500

if __name__ == '__main__':
    app.run(debug=True)
