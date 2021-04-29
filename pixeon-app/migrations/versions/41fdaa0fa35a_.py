"""empty message

Revision ID: 41fdaa0fa35a
Revises: e90ad196e02c
Create Date: 2021-04-29 20:15:13.858270

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41fdaa0fa35a'
down_revision = 'e90ad196e02c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('physician_exame')
    op.add_column('exam', sa.Column('physician_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'exam', 'physician', ['physician_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'exam', type_='foreignkey')
    op.drop_column('exam', 'physician_id')
    op.create_table('physician_exame',
    sa.Column('physician_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('exam_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['exam_id'], ['exam.id'], name='physician_exame_exam_id_fkey'),
    sa.ForeignKeyConstraint(['physician_id'], ['physician.id'], name='physician_exame_physician_id_fkey')
    )
    # ### end Alembic commands ###
