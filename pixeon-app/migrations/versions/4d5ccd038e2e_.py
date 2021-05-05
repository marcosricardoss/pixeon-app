"""empty message

Revision ID: 4d5ccd038e2e
Revises: 32b0462231b0
Create Date: 2021-05-05 04:36:19.641269

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d5ccd038e2e'
down_revision = '32b0462231b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('exame_order')
    op.drop_table('physician_exame')
    op.add_column('exam', sa.Column('order_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'exam', 'order', ['order_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'exam', type_='foreignkey')
    op.drop_column('exam', 'order_id')
    op.create_table('physician_exame',
    sa.Column('physician_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('exam_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['exam_id'], ['exam.id'], name='physician_exame_exam_id_fkey'),
    sa.ForeignKeyConstraint(['physician_id'], ['physician.id'], name='physician_exame_physician_id_fkey')
    )
    op.create_table('exame_order',
    sa.Column('order_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('exam_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['exam_id'], ['exam.id'], name='exame_order_exam_id_fkey'),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], name='exame_order_order_id_fkey')
    )
    # ### end Alembic commands ###
