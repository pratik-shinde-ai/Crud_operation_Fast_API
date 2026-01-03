
from fastapi import FastAPI
from models import Product

app=FastAPI()

@app.get("/")

def demo():
    return "welcome to fastapi"
products=[
    Product(id=1,name="iphone",description="pro 16",price=100.2,quantity=2),
    Product(id=2,name="vivo",description="vovo new",price=229.2,quantity=10),
    Product(id=3,name="1+",description="it good on charging",price=229.2,quantity=10),
    Product(id=4,name="poco",description="new made gowing",price=293.3,quantity=1),
    Product(id=5, name="samsung",description="for strog services",price=32.32,quantity=3),
    Product(id=6,name="poco",description="Battery back up good",price=433.43,quantity=4)
]
@app.get("/products")

def show_product():
    return products

@app.get("/product/{id}")

def get_product(id:int):
    return products[id-1]

@app.post("/addp")
def add_product(product:Product):
    products.append(product)
    return product


@app.put("/product/{id}")
def update_product(id: int, product: Product):
    for i in range(len(products)):
        if products[i].id == id:
            product.id = id
            products[i] = product
            return {"message": "Product updated successfully"}

    return "Prdcut not found"


@app.delete("/product/{id}")
def delete_product(id: int):
    for i in range(len(products)):
        if products[i].id == id:
            remove_product=products.pop(i)
            return {
                "message": "Product deleted successfully",
                "deleted_product": remove_product
            }
    return "Product Not Delete"

 













