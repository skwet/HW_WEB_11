from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactBase,ContactResponse,ContactUpdate
from src.repository import contacts

router = APIRouter(prefix='/contacts', tags=["contacts"])

@router.get('/', response_model=List[ContactResponse])
async def read_contacts(db: Session = Depends(get_db)):
    contacts_l = await contacts.get_contacts(db)
    return contacts_l

@router.get('/{contact_id}', response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await contacts.get_contact(contact_id,db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.post('/', response_model=ContactResponse)
async def create_contact(body: ContactBase, db: Session = Depends(get_db)):
    return await contacts.create_contact(body, db)

@router.patch('/{contact_id}', response_model=ContactResponse)
async def update_cont(body: ContactUpdate, contact_id: int, db: Session = Depends(get_db)):
    contact = await contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.delete('/{contact_id}', response_model=ContactResponse)
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    tag = await contacts.delete_contact(contact_id, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return tag

@router.get('/birthdays/',response_model=List[ContactResponse])
async def get_birth(db: Session = Depends(get_db)):
    birthday = await contacts.get_birthdays(db)

    if birthday:
        return birthday
    else:
        return []
    
@router.get('/search/',response_model=List[ContactResponse])
async def search_contacts(query: str, db: Session = Depends(get_db)):
    search_results = await contacts.find_contact(query,db)
    if not search_results:
        return []
    return search_results