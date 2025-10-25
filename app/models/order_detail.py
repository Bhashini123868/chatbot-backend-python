from sqlalchemy import Column, String, Integer, Float, ForeignKey
from app.core.database import Base


class OrderDetail(Base):
    __tablename__ = "order_detail"

    orderId = Column(String(10), primary_key=True, index=True)
    itemCode = Column(String(10), ForeignKey("item_log.code"), primary_key=True)
    qty = Column(Integer, nullable=False)
    unitPrice = Column(Float, nullable=False)

    def __repr__(self):
        return f"<OrderDetail(orderId='{self.orderId}', itemCode='{self.itemCode}', qty={self.qty}, unitPrice={self.unitPrice})>"

