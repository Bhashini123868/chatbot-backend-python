from sqlalchemy import Column, String, Float, Integer
from app.core.database import Base


class Item(Base):
    __tablename__ = "item_log"

    code = Column(String(10), primary_key=True, index=True)
    description = Column(String(100), nullable=False)
    unitPrice = Column(Float, nullable=False)
    qtyOnHand = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Item(code='{self.code}', description='{self.description}', unitPrice={self.unitPrice}, qtyOnHand={self.qtyOnHand})>"
