import sqlalchemy as sa
from sqlalchemy.orm import relationship

from storage.db_config import Base


class Product(Base):
    __tablename__ = 'product'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50), nullable=False)
    description = sa.Column(sa.String(100))
    price = sa.Column(sa.DECIMAL(10, 2), nullable=False)
    quantity = sa.Column(sa.Integer)
    user_username = sa.Column(
        sa.String(50), sa.ForeignKey('users.username'), nullable=False
    )
    user = relationship('User', backref='products')


class Auction(Base):
    __tablename__ = 'auction'

    id = sa.Column(sa.Integer, primary_key=True)
    product_id = sa.Column(
        sa.Integer, sa.ForeignKey('product.id'), nullable=True
    )
    product = relationship('Product', backref='auctions')
    start_price = sa.Column(sa.DECIMAL(10, 2))
    # status = 


class Bid(Base):
    __tablename__ = 'bid'

    id = sa.Column(sa.Integer, primary_key=True)
    auction_id = sa.Column(
        sa.Integer, sa.ForeignKey('auction.id'), nullable=False
    )
    auction = relationship('Auction', backref='bids')
    user_username = sa.Column(
        sa.String(50), sa.ForeignKey('users.username'), nullable=False
    )
    user = relationship('User', backref='bids')
    amount = sa.Column(sa.DECIMAL(10, 2), nullable=False)
