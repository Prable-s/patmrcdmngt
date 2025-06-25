from datetime import datetime
from typing import Optional


class Patient:
    def __init__(
        self,
        id: str,
        full_name: str,
        age: int,
        gender: str,
        contact_information: str,
        address: str,
        emergency_contact: str,
        date_created: datetime,
        date_updated: datetime,
        date_deleted: Optional[datetime] = None,
    ):
        self.id = id
        self.full_name = full_name
        self.age = age
        self.gender = gender
        self.contact_information = contact_information
        self.address = address
        self.emergency_contact = emergency_contact
        self.date_created = date_created
        self.date_updated = date_updated
        self.date_deleted = date_deleted

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "age": self.age,
            "gender": self.gender,
            "contact_information": self.contact_information,
            "address": self.address,
            "emergency_contact": self.emergency_contact,
            "date_created": self.date_created.isoformat(),
            "date_updated": self.date_updated.isoformat(),
            "date_deleted": (
                self.date_deleted.isoformat() if self.date_deleted else None
            ),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            full_name=data["full_name"],
            age=data["age"],
            gender=data["gender"],
            contact_information=data["contact_information"],
            address=data["address"],
            emergency_contact=data["emergency_contact"],
            date_created=datetime.fromisoformat(data["date_created"]),
            date_updated=datetime.fromisoformat(data["date_updated"]),
            date_deleted=datetime.fromisoformat(
                data["date_deleted"]) if data["date_deleted"] else None,
        )
