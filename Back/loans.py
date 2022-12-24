from flask import Blueprint,  request
loans = Blueprint('loans',__name__)
from dbLayer import db, Loans, Books
import json
from datetime import date, timedelta



@loans.route('/loans/', methods=['GET', 'POST', 'DELETE'])
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
        return_date = date.today() + timedelta(days=daysToAdd)
       
        newLoan = Loans(customer_id, book_id, loan_date, return_date)
        db.session.add(newLoan)
        db.session.commit()
        return "new loan was added"
    if request.method == 'GET':
        res = []
        for loan in Loans.query.all():
            res.append(
                {"customerId": loan.customer_id, "bookId": loan.book_id, "loanDate": loan.loan_date, "returnDate": loan.return_date, })
        return (json.dumps(res))

