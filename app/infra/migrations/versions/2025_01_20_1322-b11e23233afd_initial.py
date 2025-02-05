"""initial

Revision ID: b11e23233afd
Revises: f527fa23de8d
Create Date: 2025-01-20 13:22:49.305884

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b11e23233afd'
down_revision: Union[str, None] = 'f527fa23de8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('carts_user_oid_key', 'carts', type_='unique')
    op.drop_constraint('carts_user_oid_fkey', 'carts', type_='foreignkey')
    op.drop_column('carts', 'user_oid')
    op.create_unique_constraint(None, 'categories', ['title'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'categories', type_='unique')
    op.add_column('carts', sa.Column('user_oid', sa.UUID(), autoincrement=False, nullable=False))
    op.create_foreign_key('carts_user_oid_fkey', 'carts', 'users', ['user_oid'], ['oid'])
    op.create_unique_constraint('carts_user_oid_key', 'carts', ['user_oid'])
    # ### end Alembic commands ###
