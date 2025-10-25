from sqlalchemy import Column, Integer, String, Text, DateTime, func, Float
from app.core.database import Base


class Customer(Base):
    __tablename__ = "customer_log"

    id = Column(String(10), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    balance = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Customer(id='{self.id}', name='{self.name}', address='{self.address}', balance={self.balance})>"