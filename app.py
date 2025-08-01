from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vanshika_traders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(200), nullable=True)
    rate = db.Column(db.Integer, nullable=True)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        product = request.form['product']
        new_product = Product(product=product)
        db.session.add(new_product)
        db.session.commit()
    
    all_products = Product.query.all()
    return render_template("index.html", all_products=all_products)

@app.route("/search")
def search():
    query = request.args.get("query")
    if query:
        results = Product.query.filter(Product.product.ilike(f"%{query}%")).all()
    else:
        results = []
    return render_template("search.html", search_results=results, query=query)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)