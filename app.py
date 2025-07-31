from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vanshika_traders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(200), nullable=False)
    
    def _repr_(self) -> str:
        return f"{self.Sno} - {self.product}"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        product_name = request.form['product']
        new_product = Product(product=product_name)
        db.session.add(new_product)
        db.session.commit()

    allProduct = Product.query.all()
    return render_template("index.html", allProduct=allProduct)

@app.route("/search")
def search():
    query = request.args.get('query', '')
    if query:
        allProduct = Product.query.filter(Product.product.ilike(f"%{query}%")).all()
    else:
        allProduct = []
    return render_template("index.html", allProduct=allProduct)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
        print("✔ Database created successfully")
    app.run(debug=True)