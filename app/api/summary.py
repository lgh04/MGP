from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..models.bill import Bill
from ..db import get_db

router = APIRouter()

@router.get("/summary")
def get_bill_summary(db: Session = Depends(get_db)):
    result = {}

    for status in ["draft", "enacted"]:
        bills = (
            db.query(Bill)
            .filter(Bill.status == status)
            .order_by(desc(Bill.created_at))
            .limit(7)
            .all()
        )

        result[status] = [
            {
                "name": bill.name,
                "description": bill.description,
                "created_at": bill.created_at
            }
            for bill in bills
        ]

    return result
