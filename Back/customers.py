from flask import Blueprint,  request
customers = Blueprint('customer',__name__)
from dbLayer import db, Customers
import json

@customers.route('/customers', methods=['GET', 'POST', 'DELETE'])
@customers.route('/customers/<id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def crude_customers(id=-1):
    if request.method == 'POST':
        request_data = request.get_json()
        # print(request_data['city'])
        name = request_data['name']
        city = request_data["city"]
        age = request_data["age"]

        newCustomer = Customers(name, city, age)
        db.session.add(newCustomer)
        db.session.commit()
        return {"message": "new customers was added"}
    if request.method == 'GET':
        res = []
        for customer in Customers.query.all():
            res.append(
                {"id": customer.id, "name": customer.name, "city": customer.city, "age": customer.age})
        return (json.dumps(res))

@customers.route('/customersSearch/<searchName>', methods=['GET'])
def customersSearch(searchName):
    res = []
    searchName = f"%{searchName}%"
    for customer in Customers.query.filter(Customers.name.ilike(searchName)).all():
        res.append(
            {"id": customer.id, "name": customer.name, "city": customer.city, "age": customer.age})
    return (json.dumps(res))


