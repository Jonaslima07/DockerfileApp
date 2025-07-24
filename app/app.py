from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/atv4'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@postgres_container:5432/atv4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    idade = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nome}>'


with app.app_context():
    db.create_all()


@app.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.get_json()
    if not data.get('nome') or not data.get('idade'):
        return jsonify({'erro': 'Campos "nome" e "idade" são obrigatórios'}), 400

    novo_usuario = Usuarios(nome=data['nome'], idade=data['idade'])
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({'mensagem': 'Usuário criado', 'id': novo_usuario.id}), 201


@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Usuarios.query.all()
    return jsonify([
        {'id': usuario.id, 'nome': usuario.nome, 'idade': usuario.idade}
        for usuario in usuarios
    ])


@app.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    usuario = Usuarios.query.get_or_404(id)
    return jsonify({'id': usuario.id, 'nome': usuario.nome, 'idade': usuario.idade})


@app.route('/usuarios/<int:id>', methods=['PUT'])
def update_usuario(id):
    usuario = Usuarios.query.get_or_404(id)
    data = request.get_json()
    usuario.nome = data.get('nome', usuario.nome)
    usuario.idade = data.get('idade', usuario.idade)
    db.session.commit()
    return jsonify({'mensagem': 'Usuário atualizado'})


@app.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    usuario = Usuarios.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'mensagem': 'Usuário deletado'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
