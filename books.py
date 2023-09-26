import requests
import json

from flask import Flask, jsonify , request 
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

@app.route('/')
def home():
    return "Welcome to the Book HELOOOOOOOOOOOOOOOOOOOOOOOOOOOO API!"


#DEFINING BOOK MODEL
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'book_name': self.book_name,
            'author': self.author,
            'publisher': self.publisher
    }

#CRUD ROUTES

#MAKE NEW BOOK
@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()

    new_book = Book(
        book_name=data['book_name'],
        author=data['author'],
        publisher=data['publisher']
    )
    db.session.add(new_book)
    db.session.commit()
    
    return jsonify({"message": "Book created successfully!"}), 201


#GET ALL BOOKS

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.serialize for book in books])


# Convert Book object to a dictionary.



    

# GET A SPECIFIC BOOK

@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    return jsonify(book.serialize)

# UPDATE BOOK

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    
    data = request.get_json()
    book.book_name = data['book_name']
    book.author = data['author']
    book.publisher = data['publisher']

    db.session.commit()

    return jsonify({"message": "Book updated successfully!"})


#DELETE A BOOK 

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    
    db.session.delete(book)
    db.session.commit()

    return jsonify({"message": "Book deleted successfully!"})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
