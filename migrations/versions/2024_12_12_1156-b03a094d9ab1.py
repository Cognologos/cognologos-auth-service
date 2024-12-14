"""Create auth_sessions table

Revision ID: b03a094d9ab1
Revises: dba4166dbc94
Create Date: 2024-12-12 11:56:00.600194+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "b03a094d9ab1"
down_revision: Union[str, None] = "dba4166dbc94"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "auth_sessions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("user_ip", sa.String(length=128), nullable=False),
        sa.Column("user_agent", sa.String(length=256), nullable=True),
        sa.Column("access_token", sa.Uuid(), nullable=True),
        sa.Column("refresh_token", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("auth_sessions")
