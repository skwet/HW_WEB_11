from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.database.models import Contact
from src.schemas import ContactBase
from datetime import datetime,timedelta

async def get_contacts(db: Session) -> List[Contact]:
    return db.query(Contact).all()

async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()

async def create_contact(body: ContactBase, db: Session) -> Contact:
    contact = Contact(first_name=body.first_name,
                  last_name = body.last_name,
                  email = body.email,
                  phone_num = body.phone_num,
                  birthday = body.birthday.strftime("%Y-%m-%d"))
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

async def update_contact(contact_id: int, body: ContactBase, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.email = body.email
        contact.phone_num = body.phone_num

        db.commit()
        
        return contact
    
async def delete_contact(contact_id: int, db: Session)  -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact

async def get_birthdays(db: Session) -> Contact | None:
    today = datetime.now().date()

    end = today + timedelta(days=7)

    birthday_contacts = []

    for contact in db.query(Contact).all():
        contact_birthday = contact.birthday.replace(year=today.year)
        if today <= contact_birthday <= end:
            birthday_contacts.append(contact)

    return birthday_contacts

async def find_contact(query: str, db: Session) -> Contact:
    
    results = db.query(Contact).filter(
        Contact.first_name.ilike(f"%{query}%") |  
        Contact.last_name.ilike(f"%{query}%") |  
        Contact.email.ilike(f"%{query}%")  
    ).all()
    
    return results