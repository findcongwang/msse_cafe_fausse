from sqlalchemy.orm import Session
from typing import List
from app.models import Table

async def create_table(db: Session, table_number: int, capacity: int) -> Table:
    table = Table(table_number=table_number, capacity=capacity)
    db.add(table)
    await db.commit()
    await db.refresh(table)
    return table

async def get_all_tables(db: Session) -> List[Table]:
    return await db.query(Table).filter(Table.is_active == True).all() 