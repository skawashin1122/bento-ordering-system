"""Create users table and related tables

Revision ID: 2e6f4384dac1
Revises: 
Create Date: 2025-10-05 08:45:01.434744

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e6f4384dac1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False, comment='ユーザーID'),
        sa.Column('email', sa.String(length=255), nullable=False, comment='メールアドレス（ログインID）'),
        sa.Column('name', sa.String(length=100), nullable=False, comment='ユーザー名'),
        sa.Column('hashed_password', sa.String(length=255), nullable=False, comment='ハッシュ化されたパスワード'),
        sa.Column('role', sa.Enum('customer', 'store', name='userrole'), nullable=False, comment='ユーザーロール（顧客 or 店舗管理者）'),
        sa.Column('is_active', sa.Boolean(), nullable=False, comment='アカウント有効フラグ'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='作成日時'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新日時'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Create menus table
    op.create_table(
        'menus',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False, comment='メニューID'),
        sa.Column('name', sa.String(length=100), nullable=False, comment='商品名'),
        sa.Column('description', sa.Text(), nullable=True, comment='商品説明'),
        sa.Column('price', sa.Numeric(precision=10, scale=0), nullable=False, comment='価格（円）'),
        sa.Column('category', sa.Enum('meat', 'fish', 'vegetable', 'other', name='menucategory'), nullable=False, comment='カテゴリ'),
        sa.Column('image_url', sa.String(length=500), nullable=True, comment='商品画像URL'),
        sa.Column('is_available', sa.Boolean(), nullable=False, comment='販売可能フラグ'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='作成日時'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新日時'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create orders table
    op.create_table(
        'orders',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False, comment='注文ID'),
        sa.Column('user_id', sa.BigInteger(), nullable=False, comment='注文者ユーザーID'),
        sa.Column('status', sa.Enum('pending', 'preparing', 'ready', 'delivered', 'cancelled', name='orderstatus'), nullable=False, comment='注文ステータス'),
        sa.Column('total_amount', sa.Numeric(precision=10, scale=0), nullable=False, comment='合計金額（円）'),
        sa.Column('delivery_address', sa.Text(), nullable=False, comment='配達先住所'),
        sa.Column('delivery_time', sa.DateTime(timezone=True), nullable=True, comment='希望配達時間'),
        sa.Column('notes', sa.Text(), nullable=True, comment='注文備考'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='注文日時'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='更新日時'),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
    op.create_index(op.f('ix_orders_user_id'), 'orders', ['user_id'], unique=False)
    op.create_index(op.f('ix_orders_status'), 'orders', ['status'], unique=False)

    # Create order_details table
    op.create_table(
        'order_details',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False, comment='注文詳細ID'),
        sa.Column('order_id', sa.BigInteger(), nullable=False, comment='注文ID'),
        sa.Column('menu_id', sa.BigInteger(), nullable=False, comment='メニューID'),
        sa.Column('quantity', sa.Integer(), nullable=False, comment='数量'),
        sa.Column('unit_price', sa.Numeric(precision=10, scale=0), nullable=False, comment='注文時の単価（円）'),
        sa.Column('subtotal', sa.Numeric(precision=10, scale=0), nullable=False, comment='小計（円）= quantity × unit_price'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='作成日時'),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['menu_id'], ['menus.id'], ondelete='RESTRICT')
    )
    op.create_index(op.f('ix_order_details_order_id'), 'order_details', ['order_id'], unique=False)
    op.create_index(op.f('ix_order_details_menu_id'), 'order_details', ['menu_id'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index(op.f('ix_order_details_menu_id'), table_name='order_details')
    op.drop_index(op.f('ix_order_details_order_id'), table_name='order_details')
    op.drop_table('order_details')
    
    op.drop_index(op.f('ix_orders_status'), table_name='orders')
    op.drop_index(op.f('ix_orders_user_id'), table_name='orders')
    op.drop_table('orders')
    
    op.drop_table('menus')
    
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    
    # Drop enum types (PostgreSQL specific)
    op.execute('DROP TYPE IF EXISTS orderstatus')
    op.execute('DROP TYPE IF EXISTS menucategory')
    op.execute('DROP TYPE IF EXISTS userrole')