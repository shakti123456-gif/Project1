from fastapi import FastAPI,HTTPException,Depends,status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine,SessionLocal
from sqlalchemy.orm  import session
from geopy.distance import geodesic

app=FastAPI()

models.Base.metadata.create_all(bind=engine)


class AddressCreate(BaseModel):
    name: str
    latitude: float
    longitude: float

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/addresses/")
def create_address(address: AddressCreate):
    db = SessionLocal()
    new_address = models.Address(**address.dict())
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    db.close()
    return new_address

# Update an address by ID
@app.put("/addresses/{address_id}")
def update_address(address_id: int, address: AddressCreate):
    db = SessionLocal()
    existing_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if existing_address is None:
        db.close()
        raise HTTPException(status_code=404, detail="Address not found")
    for field, value in address.dict().items():
        setattr(existing_address, field, value)
    db.commit()
    db.refresh(existing_address)
    db.close()
    return existing_address

# Delete an address by ID
@app.delete("/addresses/{address_id}")
def delete_address(address_id: int):
    db = SessionLocal()
    address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if address is None:
        db.close()
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(address)
    db.commit()
    db.close()
    return address

# Retrieve addresses within a given distance and location coordinates
@app.get("/addresses/")
def get_addresses_within_distance(
    latitude: float, longitude: float, max_distance: float = 10
) :
    db = SessionLocal()
    all_addresses = db.query(models.Address).all()
    addresses_within_distance = []
    user_location = (latitude, longitude)
    for address in all_addresses:
        address_location = (address.latitude, address.longitude)
        distance = geodesic(user_location, address_location).miles
        if distance <= max_distance:
            addresses_within_distance.append(address)
    db.close()
    return addresses_within_distance

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
