"""add_confirmed_email

Revision ID: 002
Revises: 2786be9b09e3
Create Date: 2023-10-22 13:29:06.596572
"""

# import necessary libraries
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '5db63297d8dc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add confirmed_email column to users table
    op.add_column('users', sa.Column('confirmed_email', sa.Boolean(), nullable=True))

def downgrade():
    # Remove confirmed_email column from users table
    op.drop_column('users', 'confirmed_email')
