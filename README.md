# Smart Cart API

This is a Flask-based RESTful API for a smart shopping cart system. It allows users to:

- Add products to a cart
- Remove items
- Set customer info (for loyalty discounts)
- Retrieve the final cart total (with tax, category-based, bulk, and loyalty discounts)

---

## Features

- Add products with category, price, and quantity
- Discounts:
  - 15% on **Electronics** (if quantity > 2)
  - 10% bulk discount on total > $200
  - Loyalty discounts: Silver, Gold, Platinum
- SQLite database (auto-created)
- Fully containerized with **Docker**
- CORS enabled

---

## Tech Stack

- Python 3
- Flask + SQLAlchemy
- SQLite
- Docker

---

##  Docker Instructions

### Build the image

```bash
docker build -t smart_cart .
```

### Run the Container

```bash
docker run -d -p 5000:5000 -v $(pwd)/instance:/app/instance smart_cart:latest
```


## Test API Locally Using curl

```bash
### Add Items
curl -X POST http://127.0.0.1:5000/cart \
  -H "Content-Type: application/json" \
  -d '{
    "Items": [
      {"name": "Laptop", "category": "Electronics", "price": 1000, "quantity": 3},
      {"name": "Book", "category": "Books", "price": 20, "quantity": 2}
    ]
  }'

### Set Customer
curl -X POST http://127.0.0.1:5000/customer \
  -H "Content-Type: application/json" \
  -d '{
    "Customer": {
      "loyalty_level": "Gold"
    }
  }'

### Get Cart
curl http://127.0.0.1:5000/cart

### Remove Item
curl -X DELETE http://127.0.0.1:5000/cart/1

```