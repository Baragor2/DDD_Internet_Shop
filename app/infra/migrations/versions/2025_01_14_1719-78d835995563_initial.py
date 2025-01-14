"""initial

Revision ID: 78d835995563
Revises: 6ad7abb6053a
Create Date: 2025-01-14 17:19:50.536283

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78d835995563'
down_revision: Union[str, None] = '6ad7abb6053a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('carts', sa.Column('user_oid', sa.Uuid(), nullable=False))
    op.create_unique_constraint(None, 'carts', ['user_oid'])
    op.create_foreign_key(None, 'carts', 'users', ['user_oid'], ['oid'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'carts', type_='foreignkey')
    op.drop_constraint(None, 'carts', type_='unique')
    op.drop_column('carts', 'user_oid')
    # ### end Alembic commands ###
