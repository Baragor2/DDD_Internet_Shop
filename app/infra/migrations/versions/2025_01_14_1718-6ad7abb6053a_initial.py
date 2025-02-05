"""initial

Revision ID: 6ad7abb6053a
Revises: 
Create Date: 2025-01-14 17:18:49.092688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ad7abb6053a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('carts',
    sa.Column('oid', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('oid')
    )
    op.create_table('categories',
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('oid', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('oid')
    )
    op.create_table('product_images',
    sa.Column('product_id', sa.Uuid(), nullable=False),
    sa.Column('image', sa.LargeBinary(), nullable=False),
    sa.Column('oid', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('oid')
    )
    op.create_table('products',
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('price', sa.Numeric(), nullable=False),
    sa.Column('image_oid', sa.Uuid(), nullable=True),
    sa.Column('category_oid', sa.Uuid(), nullable=False),
    sa.Column('characteristics', sa.JSON(), nullable=False),
    sa.Column('oid', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['category_oid'], ['categories.oid'], ),
    sa.ForeignKeyConstraint(['image_oid'], ['product_images.oid'], ),
    sa.PrimaryKeyConstraint('oid')
    )
    op.create_table('users',
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password_hash', sa.LargeBinary(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('cart_oid', sa.Uuid(), nullable=False),
    sa.Column('oid', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['cart_oid'], ['carts.oid'], ),
    sa.PrimaryKeyConstraint('oid'),
    sa.UniqueConstraint('cart_oid'),
    sa.UniqueConstraint('email')
    )
    op.create_table('orders',
    sa.Column('user_oid', sa.Uuid(), nullable=False),
    sa.Column('price', sa.Numeric(), nullable=False),
    sa.Column('oid', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_oid'], ['users.oid'], ),
    sa.PrimaryKeyConstraint('oid')
    )
    op.create_table('cart_items',
    sa.Column('cart_oid', sa.Uuid(), nullable=False),
    sa.Column('order_oid', sa.Uuid(), nullable=True),
    sa.Column('product_oid', sa.Uuid(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('oid', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['cart_oid'], ['carts.oid'], ),
    sa.ForeignKeyConstraint(['order_oid'], ['orders.oid'], ),
    sa.ForeignKeyConstraint(['product_oid'], ['products.oid'], ),
    sa.PrimaryKeyConstraint('oid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cart_items')
    op.drop_table('orders')
    op.drop_table('users')
    op.drop_table('products')
    op.drop_table('product_images')
    op.drop_table('categories')
    op.drop_table('carts')
    # ### end Alembic commands ###
