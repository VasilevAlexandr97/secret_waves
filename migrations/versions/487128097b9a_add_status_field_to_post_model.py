"""add status field to post model

Revision ID: 487128097b9a
Revises: f3e133dd41a0
Create Date: 2025-07-02 15:27:44.857311

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '487128097b9a'
down_revision: Union[str, None] = 'f3e133dd41a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('status', sa.String(), server_default='pending', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'status')
    # ### end Alembic commands ###
