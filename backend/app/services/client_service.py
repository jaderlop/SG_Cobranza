from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.client import Client
from app.schemas.client import ClientResponse, ClientCreate, ClientUpdate

## Get all clients
def get_clients_service(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Client).offset(skip).limit(limit).all()

## Get client by id
def get_client_by_id_service(db: Session, client_id: int):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return client

## Create client
def create_new_client_service(db: Session, client_data: ClientCreate):
    if client_data.tax_id:
        existing = db.query(Client).filter(Client.tax_id == client_data.tax_id).first()
        
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Client with this tax ID already exists")

    client = Client(**client_data.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

## Update client
def update_client_service(db: Session, client_id: int, client_data: ClientUpdate):
    
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="Client not found")

    update_data = client_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(client, field, value)

    db.commit()
    db.refresh(client)
    return client
    
## Delete client
def delete_client_service(db: Session, client_id: int):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail="Client not found")
    db.delete(client)
    db.commit()
    return client