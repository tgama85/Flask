#import das bibliotecas necessárias ao funcionamento do código
from flask import Flask, flash, request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pessoas.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

#Classe com os campos da tabela
class pessoas(db.Model):
    pessoa_id = db.Column('pessoa_id', db.Integer, primary_key = True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefone = db.Column(db.String(11))
    nascimento = db.Column(db.String(10))

    def __init__(self, nome, email, telefone, nascimento):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.nascimento = nascimento

#Mostra a página inicial    
@app.route('/')
def home():
    return render_template('home.html', persons = pessoas.query.all()) #realiza o SELECT * FROM na tabela

#Coleta os dados da tabela
@app.route('/dados', methods=['GET', 'POST'])
def dados():
    if request.method == 'POST':
        if not request.form['nome'] or not request.form['email'] or not request.form['telefone'] or not request.form['nascimento']:
            flash('Por favor preencha todos os campos', 'error')
        else:
            pessoa = pessoas(request.form['nome'], request.form['email'], request.form['telefone'], request.form['nascimento'])
            
            db.session.add(pessoa)
            db.session.commit()
            flash('Dados foram adicionados com sucesso.')
            return redirect(url_for('home'))
    return render_template('dados.html')

#Executa a exclusão dos dados da tabela
@app.route("/delete", methods=['GET', 'POST'])
def delete(action=None):
    if request.method == 'POST':
        id_pessoa = request.form['pessoa_id']
        print(id_pessoa)
        pessoa = pessoas.query.filter_by(pessoa_id = id_pessoa).first()
        db.session.delete(pessoa)
        db.session.commit()
        flash('Dados foram excluídos com sucesso.')       
        
    return redirect('/')   

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)