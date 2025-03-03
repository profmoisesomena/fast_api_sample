from typing import Union, List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from pydantic import BaseModel

from database import get_db, ItemDB, create_tables

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    is_offer: Union[bool, None] = None
    
    class Config:
        orm_mode = True


app = FastAPI()

# Create database tables on startup
@app.on_event("startup")
def startup_event():
    create_tables()


@app.get("/")
def read_root():
    return {"message": "Esta é uma API de exemplo com FastAPI e PostgreSQL"}


@app.get("/items", response_model=List[ItemResponse])
def list_items(db: Session = Depends(get_db)):
    """Get all items from the database"""
    items = db.query(ItemDB).all()
    return items


@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    # Query the database for the item
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    
    # Return 404 if item is not found
    if db_item is None:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")
    
    # Return the item data
    return {
        "item_id": db_item.id, 
        "name": db_item.name, 
        "price": db_item.price, 
        "is_offer": db_item.is_offer

    }


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item, db: Session = Depends(get_db)):
    # Create a new database item or update existing one
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    
    if db_item:
        # Update existing item
        db_item.name = item.name
        db_item.price = item.price
        db_item.is_offer = item.is_offer
    else:
        # Create new item
        db_item = ItemDB(id=item_id, name=item.name, price=item.price, is_offer=item.is_offer)
        db.add(db_item)
    
    # Commit changes to database
    db.commit()
    db.refresh(db_item)
    
    return {"item_name": db_item.name, "item_id": db_item.id}


@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete an item from the database by ID"""
    # Find the item
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    
    # Return 404 if item is not found
    if db_item is None:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")
    
    # Delete the item
    db.delete(db_item)
    db.commit()
    
    return {"message": f"Item with id {item_id} has been deleted"}