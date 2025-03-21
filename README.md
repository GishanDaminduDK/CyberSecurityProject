Crud application main.py code 



# # Database URL (modify with your credentials)
# DATABASE_URL = "postgresql://postgres:Gishan123@localhost:5433/mydatabase"


# # SQLAlchemy setup
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# app = FastAPI()

# # Define database model
# class ItemDB(Base):
#     __tablename__ = "items"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     price = Column(Float)
#     description = Column(String, nullable=True)

# # Create tables
# Base.metadata.create_all(bind=engine)

# # Pydantic model for API validation
# class Item(BaseModel):
#     name: str
#     price: float
#     description: Optional[str] = None

# # Dependency for database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# ### CREATE: Add a new item to the database ###
# @app.post("/items/", status_code=200)
# async def create_item(item: Item, db: Session = Depends(get_db)):
#     new_item = ItemDB(**item.dict())
#     db.add(new_item)
#     db.commit()
#     db.refresh(new_item)
#     print("Item created successfully",item)
#     return {"message": "Item created successfully", "item": new_item}

# ### READ: Get all items from the database ###
# @app.get("/items/", response_model=List[Item])
# async def get_items(db: Session = Depends(get_db)):
#     return db.query(ItemDB).all()

# ### READ: Get a single item by ID ###
# @app.get("/items/{item_id}", response_model=Item)
# async def get_item(item_id: int, db: Session = Depends(get_db)):
#     item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
#     if item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return item

# ### UPDATE: Modify an item ###
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, updated_item: Item, db: Session = Depends(get_db)):
#     item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
#     if item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     item.name = updated_item.name
#     item.price = updated_item.price
#     item.description = updated_item.description
#     db.commit()
#     return {"message": "Item updated successfully", "item": item}

# ### DELETE: Remove an item ###
# @app.delete("/items/{item_id}")
# async def delete_item(item_id: int, db: Session = Depends(get_db)):
#     item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
#     if item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     db.delete(item)
#     db.commit()
#     return {"message": "Item deleted successfully"}
# FastAPI endpoint to trigger PDF processing and query generation