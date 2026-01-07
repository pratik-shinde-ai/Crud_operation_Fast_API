from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models, schemas
from database import engine, SessionLocal, Base

app = FastAPI()

# ---------------- CREATE TABLES ----------------
Base.metadata.create_all(bind=engine)

# ---------------- DB DEPENDENCY ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- AUTO INSERT DATA ----------------
def init_db():
    db = SessionLocal()

    try:
        # Prevent duplicate insert
        if db.query(models.Product).first():
            return

        products = [
            schemas.ProductCreate(
                name="Laptop",
                description="Gaming laptop",
                price=75000,
                quantity=10
            ),
            schemas.ProductCreate(
                name="Mobile",
                description="Android phone",
                price=25000,
                quantity=20
            ),
            schemas.ProductCreate(
                name="Headphones",
                description="Noise cancelling",
                price=5000,
                quantity=15
            )
        ]

        for product in products:
            db.add(models.Product(**product.model_dump()))

        db.commit()
        print("✅ Default products inserted")

    except Exception as e:
        db.rollback()
        print("❌ Insert failed:", e)

    finally:
        db.close()

# ---------------- RUN ON STARTUP ----------------
@app.on_event("startup")
def startup_event():
    init_db()

# ---------------- APIs ----------------
@app.get("/")
def demo():
    return "Welcome to FastAPI"

@app.post("/products", response_model=schemas.Product)
def add_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products", response_model=list[schemas.Product])
def show_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@app.get("/product/{id}", response_model=schemas.Product)
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        return {"message": "Product not found"}
    return product

@app.delete("/product/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        return {"message": "Product not found"}
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}
