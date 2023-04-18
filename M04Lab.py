#Reece Harkness
#M04Lab.py
#4/17/23

from flask import Flask, request, json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Book(id={self.id}, book_name='{self.book_name}', author='{self.author}', publisher='{self.publisher}')"

# Create
@app.route('/books', methods=['POST'])
def create_book():
    book_data = request.json
    new_book = Book(book_name=book_data['book_name'], author=book_data['author'], publisher=book_data['publisher'])
    db.session.add(new_book)
    db.session.commit()
    return json({'message': 'Book created successfully!', 'data': new_book.__repr__()})

# Read
@app.route('/books', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    results = []
    for book in books:
        results.append(book.__repr__())
    return json(results)

@app.route('/books/<id>', methods=['GET'])
def get_book_by_id(id):
    book = Book.query.get(id)
    if book:
        return json(book.__repr__())
    else:
        return json({'message': 'Book not found.'})

# Update
@app.route('/books/<id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)
    if book:
        book_data = request.json
        book.book_name = book_data['book_name']
        book.author = book_data['author']
        book.publisher = book_data['publisher']
        db.session.commit()
        return json({'message': 'Book updated successfully!', 'data': book.__repr__()})
    else:
        return json({'message': 'Book not found.'})

# Delete
@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return json({'message': 'Book deleted successfully!'})
    else:
        return json({'message': 'Book not found.'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)