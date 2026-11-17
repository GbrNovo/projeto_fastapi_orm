"""Módulo biblioteca: livros e empréstimos.

Revision ID: b1b11017c026
Revises: d457a4c9930e
Create Date: 2026-11-17
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'b1b11017c026'
down_revision: Union[str, Sequence[str], None] = 'd457a4c9930e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'tb_livros',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('titulo', sa.String(length=255), nullable=False),
        sa.Column('autor', sa.String(length=255), nullable=False),
        sa.Column('isbn', sa.String(length=20), nullable=True),
    )
    op.create_table(
        'tb_emprestimos',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('aluno_id', sa.Integer(), sa.ForeignKey('tb_alunos.id'), nullable=False),
        sa.Column('livro_id', sa.Integer(), sa.ForeignKey('tb_livros.id'), nullable=False),
        sa.Column('data_emprestimo', sa.DateTime(timezone=True), nullable=False),
        sa.Column('data_devolucao', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('tb_emprestimos')
    op.drop_table('tb_livros')
