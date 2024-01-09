from flask import Flask, render_template, request, flash, jsonify
import requests

app = Flask(__name__)

USERS_URL = 'http://127.0.0.1:8000/users/'
TODOS_URL = 'http://127.0.0.1:8000/todos/'
POSTS_URL = 'http://127.0.0.1:8000/posts/'
COMMENTS_URL = 'http://127.0.0.1:8000/comments/'

@app.route('/')
def index():
    return 'Bem-vindo à minha API!'

@app.route('/users')
def list_users():
    users = requests.get(USERS_URL).json()
    return render_template('users.html', users=users)

@app.route('/user/<int:user_id>')
def get_user(user_id):
    user = requests.get(f'{USERS_URL}{user_id}/').json()
    return render_template('user_detail.html', user=user)

@app.route('/user/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        user_data = {
            'id': request.form['id'],
            'nome': request.form['nome'],
            'nome_de_usuario': request.form['nome_de_usuario'],
            'email': request.form['email'],
            'rua': request.form['rua'],
            'suíte': request.form['suíte'],
            'cidade': request.form['cidade'],
            'código_postal': request.form['código_postal'],
            'lat': request.form['lat'],
            'lng': request.form['lng'],
            'telefone': request.form['telefone'],
            'site': request.form['site'],
            'empresa_nome': request.form['empresa_nome'],
            'empresa_catchPhrase': request.form['empresa_catchPhrase'],
            'empresa_bs': request.form['empresa_bs']
        }
        response = requests.post(USERS_URL, json=user_data)
        if response.status_code == 201:
            flash('Usuário criado com sucesso!')
        else:
            flash('Falha ao criar o usuário.')
    return render_template('create.html')

todos = [
    {"id": 1, "title": "Todo 1", "completed": False},
    {"id": 2, "title": "Todo 2", "completed": True},
    # Adicione mais dados de exemplo para os Todos
]

# Endpoint para obter todos os Todos
@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

# Endpoint para obter um Todo específico por ID
@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = next((t for t in todos if t["id"] == todo_id), None)
    return jsonify(todo) if todo else ('', 404)

# Endpoint para criar um novo Todo
@app.route('/todos', methods=['POST'])
def create_todo():
    new_todo = request.json
    if "title" not in new_todo or "completed" not in new_todo:
        return jsonify({"error": "Title and Completed fields are required"}), 400
    
    new_todo["id"] = max(t["id"] for t in todos) + 1
    todos.append(new_todo)
    return jsonify(new_todo), 201

# Endpoint para atualizar um Todo existente
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    
    update_data = request.json
    todo.update(update_data)
    return jsonify(todo)

# Endpoint para deletar um Todo existente
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [t for t in todos if t["id"] != todo_id]
    return '', 204

posts = [
    {"id": 1, "title": "Post 1", "body": "This is the body of post 1"},
    {"id": 2, "title": "Post 2", "body": "This is the body of post 2"},
    # Adicione mais dados de exemplo para os Posts
]

# Endpoint para obter todos os Posts
@app.route('/posts', methods=['GET'])
def get_posts():
    return jsonify(posts)

# Endpoint para obter um Post específico por ID
@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = next((p for p in posts if p["id"] == post_id), None)
    return jsonify(post) if post else ('', 404)

# Endpoint para criar um novo Post
@app.route('/posts', methods=['POST'])
def create_post():
    new_post = request.json
    if "title" not in new_post or "body" not in new_post:
        return jsonify({"error": "Title and Body fields are required"}), 400
    
    new_post["id"] = max(p["id"] for p in posts) + 1
    posts.append(new_post)
    return jsonify(new_post), 201

# Endpoint para atualizar um Post existente
@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    
    update_data = request.json
    post.update(update_data)
    return jsonify(post)

# Endpoint para deletar um Post existente
@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global posts
    posts = [p for p in posts if p["id"] != post_id]
    return '', 204

comments = [
    {"id": 1, "post_id": 1, "name": "John", "body": "This is a comment on post 1"},
    {"id": 2, "post_id": 1, "name": "Alice", "body": "Another comment on post 1"},
    # Adicione mais dados de exemplo para os Comments
]

# Endpoint para obter todos os Comments
@app.route('/comments', methods=['GET'])
def get_comments():
    return jsonify(comments)

# Endpoint para obter um Comment específico por ID
@app.route('/comments/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    comment = next((c for c in comments if c["id"] == comment_id), None)
    return jsonify(comment) if comment else ('', 404)

# Endpoint para criar um novo Comment
@app.route('/comments', methods=['POST'])
def create_comment():
    new_comment = request.json
    if "post_id" not in new_comment or "name" not in new_comment or "body" not in new_comment:
        return jsonify({"error": "Post ID, Name, and Body fields are required"}), 400
    
    new_comment["id"] = max(c["id"] for c in comments) + 1
    comments.append(new_comment)
    return jsonify(new_comment), 201

# Endpoint para atualizar um Comment existente
@app.route('/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    comment = next((c for c in comments if c["id"] == comment_id), None)
    if not comment:
        return jsonify({"error": "Comment not found"}), 404
    
    update_data = request.json
    comment.update(update_data)
    return jsonify(comment)

# Endpoint para deletar um Comment existente
@app.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    global comments
    comments = [c for c in comments if c["id"] != comment_id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
