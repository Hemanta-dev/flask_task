from app import app

@app.route("/product/add")
def add():
    return "this is page of product add"