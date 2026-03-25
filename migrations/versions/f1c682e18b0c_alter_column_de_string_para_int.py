"""alter column de string para int

Revision ID: f1c682e18b0c
Revises: daa3e4058ab8
Create Date: 2026-03-24 20:15:23.972143

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1c682e18b0c'
down_revision = 'daa3e4058ab8'
branch_labels = None
depends_on = None

def upgrade():
    # 1. cria a nova coluna (nullable temporariamente)
    op.add_column('leitura', sa.Column('cor_agua', sa.Integer(), nullable=True))

    # 2. preenche com valores de 1 a 5 (aleatório)
    op.execute("""
        UPDATE leitura
        SET "cor_agua" = FLOOR(RANDOM() * 5 + 1)::int
    """)

    # 3. remove a coluna antiga
    op.drop_column('leitura', 'imagem_cor')

    # 4. torna NOT NULL
    op.alter_column('leitura', 'cor_agua', nullable=False)


def downgrade():
    # recria como string (caso volte)
    op.add_column('leitura', sa.Column('imagem_cor', sa.String(length=50), nullable=True))

    # opcional: converter de volta
    op.execute("""
        UPDATE leitura
        SET imagem_cor = cor_agua::text
    """)

    op.drop_column('leitura', 'cor_agua')