"""post 添加一个评论字段

Revision ID: 349d1b825d93
Revises: f7f27424037f
Create Date: 2018-06-05 22:23:35.203194

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '349d1b825d93'
down_revision = 'f7f27424037f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('comment', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'comment')
    # ### end Alembic commands ###
