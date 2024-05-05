from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/intellicompare_comparison'
db = SQLAlchemy(app)

class Category(db.Model):
    __tablename__ = 'Categories'
    CategoryID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)

class Source(db.Model):
    __tablename__ = 'Sources'
    SourceID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)

class Product(db.Model):
    __tablename__ = 'Products'
    ProductID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    Brand = db.Column(db.String(100))
    Description = db.Column(db.Text)
    Price = db.Column(db.DECIMAL(10, 2))
    Rating = db.Column(db.DECIMAL(3, 2))
    ImageURL = db.Column(db.String(255))
    ProductURL = db.Column(db.String(255))
    CategoryID = db.Column(db.Integer, db.ForeignKey('Categories.CategoryID'))
    SourceID = db.Column(db.Integer, db.ForeignKey('Sources.SourceID'))
class ProductReview(db.Model):
    __tablename__ = 'ProductReviews'
    ReviewID = db.Column(db.Integer, primary_key=True)
    ProductID = db.Column(db.Integer, db.ForeignKey('Products.ProductID'))
    ReviewText = db.Column(db.Text)
    Rating = db.Column(db.DECIMAL(3, 2))
    Date = db.Column(db.Date)

    product = db.relationship('Product', backref=db.backref('reviews', lazy=True))

class ProductDetail(db.Model):
    __tablename__ = 'ProductDetails'
    ProductDetailID = db.Column(db.Integer, primary_key=True)
    ProductID = db.Column(db.Integer, db.ForeignKey('Products.ProductID'))
    Specification = db.Column(db.String(255))
    Value = db.Column(db.String(255))

    product = db.relationship('Product', backref=db.backref('details', lazy=True))


from flask import request, jsonify
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.json

    # Extract data from the request
    name = data['name']
    brand = data['brand']
    description = data['description']
    price = data['price']
    rating = data['rating']
    image_url = data['image_url']
    product_url = data['product_url']
    category_name = data['category_name']
    source_name = data['source_name']
    review_text = data.get('review_text')  # Get review text if provided
    review_rating = data.get('review_rating')  # Get review rating if provided
    detail_specification = data.get('detail_specification')  # Get detail specification if provided
    detail_value = data.get('detail_value')  # Get detail value if provided

    # Check if category exists, if not, create it
    category = Category.query.filter_by(Name=category_name).first()
    if not category:
        category = Category(Name=category_name)
        db.session.add(category)
        db.session.commit()

    # Check if source exists, if not, create it
    source = Source.query.filter_by(Name=source_name).first()
    if not source:
        source = Source(Name=source_name)
        db.session.add(source)
        db.session.commit()

    # Create a new product object
    new_product = Product(
        Name=name,
        Brand=brand,
        Description=description,
        Price=price,
        Rating=rating,
        ImageURL=image_url,
        ProductURL=product_url,
        CategoryID=category.CategoryID,
        SourceID=source.SourceID
    )

    # Add the new product to the database
    db.session.add(new_product)
    db.session.commit()

    # Add product reviews if provided
    if review_text and review_rating:
        new_review = ProductReview(
            ProductID=new_product.ProductID,
            ReviewText=review_text,
            Rating=review_rating
        )
        db.session.add(new_review)

    # Add product details if provided
    if detail_specification and detail_value:
        new_detail = ProductDetail(
            ProductID=new_product.ProductID,
            Specification=detail_specification,
            Value=detail_value
        )
        db.session.add(new_detail)

    db.session.commit()

    return jsonify({'message': 'Product added successfully'}), 201

if __name__ == "__main__":
    app.run(debug=True, port=3000)