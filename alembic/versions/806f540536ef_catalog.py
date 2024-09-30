"""Catalog

Revision ID: 806f540536ef
Revises: 
Create Date: 2024-08-08 17:46:20.247987

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '806f540536ef'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('catalog',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('bucketName', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('originalName', sa.String(), nullable=True),
    sa.Column('path', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('level', sa.Integer(), nullable=True),
    sa.Column('createUp', sa.DateTime(), nullable=True),
    sa.Column('updateUp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('catalog')
    # ### end Alembic commands ###
