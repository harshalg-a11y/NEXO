"""Initial migration with all tables

Revision ID: 648ac56b1234
Revises: 
Create Date: 2024-02-10 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '648ac56b1234'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('role', sa.String(length=50), nullable=False, server_default='user'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    
    # Create contacts table
    op.create_table('contacts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('address', sa.String(length=255), nullable=True),
        sa.Column('city', sa.String(length=100), nullable=True),
        sa.Column('country', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_contacts_id'), 'contacts', ['id'], unique=False)
    op.create_index(op.f('ix_contacts_user_id'), 'contacts', ['user_id'], unique=False)
    
    # Create cars table
    op.create_table('cars',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('make', sa.String(length=100), nullable=False),
        sa.Column('model', sa.String(length=100), nullable=False),
        sa.Column('year', sa.Integer(), nullable=True),
        sa.Column('license_plate', sa.String(length=50), nullable=False),
        sa.Column('daily_rate', sa.Float(), nullable=True),
        sa.Column('available', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cars_id'), 'cars', ['id'], unique=False)
    op.create_index(op.f('ix_cars_license_plate'), 'cars', ['license_plate'], unique=True)
    
    # Create car_bookings table
    op.create_table('car_bookings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('car_id', sa.Integer(), nullable=False),
        sa.Column('pickup_location', sa.String(length=255), nullable=True),
        sa.Column('dropoff_location', sa.String(length=255), nullable=True),
        sa.Column('pickup_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('dropoff_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('total_price', sa.Float(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['car_id'], ['cars.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_car_bookings_id'), 'car_bookings', ['id'], unique=False)
    op.create_index(op.f('ix_car_bookings_user_id'), 'car_bookings', ['user_id'], unique=False)
    op.create_index(op.f('ix_car_bookings_car_id'), 'car_bookings', ['car_id'], unique=False)
    
    # Create hotel_bookings table
    op.create_table('hotel_bookings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('hotel_name', sa.String(length=255), nullable=False),
        sa.Column('room_type', sa.String(length=100), nullable=True),
        sa.Column('check_in_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('check_out_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('total_price', sa.Float(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_hotel_bookings_id'), 'hotel_bookings', ['id'], unique=False)
    op.create_index(op.f('ix_hotel_bookings_user_id'), 'hotel_bookings', ['user_id'], unique=False)
    
    # Create nexo_paisa_transactions table
    op.create_table('nexo_paisa_transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(length=10), nullable=False, server_default='NPR'),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='pending'),
        sa.Column('reference', sa.String(length=255), nullable=True),
        sa.Column('description', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_nexo_paisa_transactions_id'), 'nexo_paisa_transactions', ['id'], unique=False)
    op.create_index(op.f('ix_nexo_paisa_transactions_user_id'), 'nexo_paisa_transactions', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_nexo_paisa_transactions_user_id'), table_name='nexo_paisa_transactions')
    op.drop_index(op.f('ix_nexo_paisa_transactions_id'), table_name='nexo_paisa_transactions')
    op.drop_table('nexo_paisa_transactions')
    
    op.drop_index(op.f('ix_hotel_bookings_user_id'), table_name='hotel_bookings')
    op.drop_index(op.f('ix_hotel_bookings_id'), table_name='hotel_bookings')
    op.drop_table('hotel_bookings')
    
    op.drop_index(op.f('ix_car_bookings_car_id'), table_name='car_bookings')
    op.drop_index(op.f('ix_car_bookings_user_id'), table_name='car_bookings')
    op.drop_index(op.f('ix_car_bookings_id'), table_name='car_bookings')
    op.drop_table('car_bookings')
    
    op.drop_index(op.f('ix_cars_license_plate'), table_name='cars')
    op.drop_index(op.f('ix_cars_id'), table_name='cars')
    op.drop_table('cars')
    
    op.drop_index(op.f('ix_contacts_user_id'), table_name='contacts')
    op.drop_index(op.f('ix_contacts_id'), table_name='contacts')
    op.drop_table('contacts')
    
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
