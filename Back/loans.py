from flask import Blueprint,  request
loans = Blueprint('loans',__name__)
from dbLayer import db, Loans, Books, Customers
import json
from datetime import date, timedelta

@loans.route('/loans', methods=['GET', 'POST', 'DELETE'])
@loans.route('/loans/<id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def crude_loans(id=-1):
    if request.method == 'POST':
        request_data = request.get_json()
        # print(request_data['city'])
        customer_id = request_data['customer_id']
        book_id = request_data["book_id"]
        book = Books.query.get(book_id)
        loan_date = date.today()
        daysToAdd = 0 
        if book.type == 1:
            daysToAdd = 10
        if book.type == 2:
            daysToAdd = 5
        if book.type == 3:
            daysToAdd = 2

        # For testing of expired loan
        if book.type == 4:
            daysToAdd = -1
        return_date = date.today() + timedelta(days=daysToAdd)
       
        newLoan = Loans(customer_id, book_id, loan_date, return_date)
        db.session.add(newLoan)
        db.session.commit()
        return {"message": "new book loan was added"}
    if request.method == 'GET':
        res = []
        for loan in Loans.query.join(Customers, Customers.id == Loans.customer_id).\
            join(Books, Books.id == Loans.book_id).\
            add_columns(Loans.id, Loans.customer_id, Loans.book_id, Loans.loan_date, Loans.return_date, Customers.name.label("customer_name"), Books.name.label("book_name")).all():
            res.append(
                {"id": loan.id, "customerId": loan.customer_id, "customerName": loan.customer_name, "bookName": loan.book_name, "bookId": loan.book_id, "loanDate": loan.loan_date.strftime('%d/%m/%Y'), "returnDate": loan.return_date.strftime('%d/%m/%Y'), })
        # for loan in Loans.query.all():
        #     res.append(
        #         {"id": loan.id, "customerId": loan.customer_id, "bookId": loan.book_id, "loanDate": loan.loan_date.strftime('%d/%m/%Y'), "returnDate": loan.return_date.strftime('%d/%m/%Y'), })
        return (json.dumps(res))
    if request.method == 'DELETE':
        me=Loans.query.get(id)
        db.session.delete(me)
        db.session.commit()
        return {"message": "row deleted"}

@loans.route('/expiredLoans', methods=['GET'])
def expired_loans():
    res = []
    for loan in Loans.query.join(Customers, Customers.id == Loans.customer_id).\
        join(Books, Books.id == Loans.book_id).\
        add_columns(Loans.id, Loans.customer_id, Loans.book_id, Loans.loan_date, Loans.return_date, Customers.name.label("customer_name"), Books.name.label("book_name")).filter(Loans.return_date < date.today()).all():
            res.append(
                {"id": loan.id, "customerId": loan.customer_id, "customerName": loan.customer_name, "bookId": loan.book_id, "bookName": loan.book_name, "loanDate": loan.loan_date.strftime('%d/%m/%Y'), "returnDate": loan.return_date.strftime('%d/%m/%Y'), })
    return (json.dumps(res))
