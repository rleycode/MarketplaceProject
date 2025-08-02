"""Add updated_at trigger

Revision ID: 6b6f4a084282
Revises: f26b121d8dd3
Create Date: 2025-08-01 21:44:00.085611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b6f4a084282'
down_revision: Union[str, None] = 'f26b121d8dd3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)

    op.execute("""
        CREATE TRIGGER update_updated_at_trigger
        BEFORE UPDATE ON marketplace_categories
        FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
    """)


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS update_updated_at_trigger ON marketplace_categories;")
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column();")
