from app.services.client_service import update_client_service
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_current_user
from app.models.user import User

from app.services.client_service import (
    get_clients_service,
    get_client_by_id_service,
    create_new_client_service,
    update_client_service
)   

from app.core.database import get_db
from app.schemas.client import ClientCreate, ClientUpdate, ClientResponse

router = APIRouter()

# Get all clients
@router.get("/", response_model=List[ClientResponse])
async def get_clients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_clients_service(db, skip, limit)

# Get client by id
@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific client by ID"""
    return get_client_by_id_service(db, client_id)

# Create client
@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
async def create_client(
    client_data: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new client"""
    return(create_new_client_service(db, client_data))

# Update client
@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: int,
    client_data: ClientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a client"""
    return(update_client_service(db, client_id, client_data))

# Delete client
@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a client"""
    return(delete_client_service(db, client_id))