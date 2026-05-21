from flask import Flask, render_template, request, redirect, flash
from pymongo import MongoClient
import uuid

app = Flask(__name__)
app.secret_key = "secret"

client = MongoClient("mongodb://localhost:27017/")
db = client["order_management"]
orders = db["orders"]


@app.route("/")
def home():

    total = orders.count_documents({})
    pending = orders.count_documents({"order_status":"Pending"})
    shipped = orders.count_documents({"order_status":"Shipped"})
    delivered = orders.count_documents({"order_status":"Delivered"})

    data = orders.find()

    return render_template(
        "index.html",
        total=total,
        pending=pending,
        shipped=shipped,
        delivered=delivered,
        data=data
    )


@app.route("/add", methods=["POST"])
def add():

    order = {
        "order_id": str(uuid.uuid4())[:6],
        "customer_name": request.form["customer"],
        "product_name": request.form["product"],
        "quantity": request.form["quantity"],
        "price": request.form["price"],
        "order_date": request.form["date"],
        "order_status": request.form["status"]
    }

    orders.insert_one(order)

    flash("Order Added Successfully")

    return redirect("/")


@app.route("/delete/<id>")
def delete(id):

    orders.delete_one({"order_id":id})

    flash("Order Deleted")

    return redirect("/")


@app.route("/update/<id>", methods=["POST"])
def update(id):

    orders.update_one(
        {"order_id":id},
        {"$set":{"order_status":request.form["status"]}}
    )

    flash("Order Updated")

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)