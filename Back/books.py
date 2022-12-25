
from flask import Blueprint, request
books = Blueprint('books',__name__)
from dbLayer import db, Books
import json


@books.route('/books', methods=['GET', 'POST', 'DELETE'])
@books.route('/books/<id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def crude_Books(id=-1):
    if request.method == 'POST':
        requestData = request.get_json()
        # print(request_data['city'])
        name = requestData['name']
        author = requestData["author"]
        yearPublished = requestData["yearPublished"]
        type = requestData["type"]

        newBook = Books(name, author, yearPublished, type)
        db.session.add(newBook)
        db.session.commit()
        return {"message": "new book was added"}
    if request.method == 'GET':
        res = []
        for book in Books.query.all():
            res.append({"id": book.id, "name": book.name, "author": book.author,
                       "yearPublished": book.year_published, "type": book.type})
        return (json.dumps(res))
    if request.method == 'DELETE':
        me=Books.query.get(id)
        db.session.delete(me)
        db.session.commit()
        return {"msg":"row deleted"}


@books.route('/bookSearch/<searchName>', methods=['GET'])
def bookSearch(searchName):
    res = []
    searchName = f"%{searchName}%"
    for book in Books.query.filter(Books.name.ilike(searchName)).all():
        res.append(
            {"id": book.id, "name": book.name, "author": book.author, "yearPublished": book.year_published, "type": book.type})
    return (json.dumps(res))


    # if request.method == 'PUT': #not implemented yet
    #     me=customers.query.get(id)
    #     request_data = request.get_json()
    #     # print(request_data['city'])
    #     me.books = request_data['books']
    #     me.loans = request_data['loans']
    #     db.session.commit()
    #     return {"msg":"row updated - TADA"}

# model

