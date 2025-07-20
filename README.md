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
