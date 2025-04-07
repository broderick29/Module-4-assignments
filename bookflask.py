from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

#intialize app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE-URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Book model class
class book(db.model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Book {self.bok_name}>"
    
#Creating database
def create_tables():
    db.create_all()

#Route to get books
def get_books():
    books = Book.query.all()
    result = []
    for book in books:
        result.append({
            'id': book.id,
            'book_name': book.book_name,
            'author': book.author,
            'publisher': book.publisher
        })
    return jsonify(result)

#Single book Id

def get_book(id):
    book = Book.query.get(id)
    if book:
        return jsonify({
            'id': book.id,
            'book_name': book.book_name,
            'author': book.author,
            'publisher': book.publisher
        })
    return jsonify({"message": "Book not found"}), 404

#add new book

def add_book():
    data = request.get_json()
    new_book = Book(
        book_name=data['book_name'],
        author=data['author'],
        publisher=data['publisher']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book added"}), 201

#Update a book

def update_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    
    data = request.get_json()
    book.book_name = data['book_name']
    book.author = data['author']
    book.publisher = data['publisher']
    db.session.commit()
    return jsonify({"message": "Book updated"})

#Run app
if __name__ == '__main__':
    app.run(debug=True)

