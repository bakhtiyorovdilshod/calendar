"""delete entities

Revision ID: 525f1fcfe26a
Revises: e850184eead5
Create Date: 2024-05-29 10:41:20.764777

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '525f1fcfe26a'
down_revision: Union[str, None] = 'e850184eead5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('DELETE FROM note_users')
    op.execute('DELETE FROM notes')


def downgrade() -> None:
    pass
