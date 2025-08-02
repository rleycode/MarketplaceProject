"""Add marketplace_enum type

Revision ID: d380561dfb97
Revises: dfa5aa4c8d1c
Create Date: 2025-08-01 19:08:50.590157

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd380561dfb97'
down_revision: Union[str, None] = 'dfa5aa4c8d1c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

marketplace_enum = postgresql.ENUM('ozon', 'wb', 'yandex', name='marketplace_enum')


def upgrade():
    # Создаём тип enum
    marketplace_enum.create(op.get_bind(), checkfirst=True)

    # Меняем тип столбца на новый enum
    op.alter_column(
        'marketplace_categories', 
        'marketplace',
        type_=marketplace_enum,
        postgresql_using='marketplace::text::marketplace_enum'
    )

def downgrade():
    # В откате меняем обратно на String (или как было)
    op.alter_column(
        'marketplace_categories',
        'marketplace',
        type_=sa.String(),
        postgresql_using='marketplace::text'
    )

    # Удаляем тип enum
    marketplace_enum.drop(op.get_bind(), checkfirst=True)
