"""Edit Date on Events

Revision ID: a5295c53e0a8
Revises: f24e3d81adbf
Create Date: 2025-01-28 22:22:50.597771

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5295c53e0a8'
down_revision: Union[str, None] = 'f24e3d81adbf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('events', 'date',
               existing_type=sa.DATE(),
               type_=sa.DateTime(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('events', 'date',
               existing_type=sa.DateTime(),
               type_=sa.DATE(),
               existing_nullable=False)
    # ### end Alembic commands ###
