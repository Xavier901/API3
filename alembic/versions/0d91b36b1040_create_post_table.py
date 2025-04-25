"""Create post table

Revision ID: 0d91b36b1040
Revises: 
Create Date: 2025-04-25 03:40:08.125334

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d91b36b1040'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



#    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)

def upgrade():
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                    sa.Column('title',sa.String(),nullable=False) ,
                    sa.Column('Content',sa.String(),nullable=False), 
                    sa.Column('published',sa.Boolean(),server_default='TRUE',nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                      nullable=False,server_default=sa.text('now()'))
                )
    pass


def downgrade():
    op.drop_table('posts')
    pass
