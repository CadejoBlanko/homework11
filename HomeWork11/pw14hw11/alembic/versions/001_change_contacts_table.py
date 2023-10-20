from alembic import op
import sqlalchemy as sa


revision = '001'
down_revision = None

def upgrade():
    op.add_column('contacts', sa.Column('additional_info', sa.String, nullable=True))

def downgrade():
    op.drop_column('contacts', 'additional_info')
