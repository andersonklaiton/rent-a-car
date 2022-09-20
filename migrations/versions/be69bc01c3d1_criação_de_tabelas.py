"""Criação de tabelas

Revision ID: be69bc01c3d1
Revises: 
Create Date: 2022-09-20 11:37:50.368212

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be69bc01c3d1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_category_car',
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('body_types', sa.String(), nullable=False),
    sa.Column('fuel_type', sa.String(), nullable=False),
    sa.Column('engine_power', sa.String(), nullable=False),
    sa.Column('km_per_liter', sa.Float(), nullable=False),
    sa.Column('allowed_category_cnh', sa.String(length=2), nullable=False),
    sa.Column('differentials', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('category_id')
    )
    op.create_table('tb_maintenance_car',
    sa.Column('maintenance_id', sa.Integer(), nullable=False),
    sa.Column('last_maintenance', sa.DateTime(), nullable=False),
    sa.Column('next_maintenance', sa.DateTime(), nullable=False),
    sa.Column('repaired_items', sa.ARRAY(sa.String()), nullable=False),
    sa.Column('maintenance_price', sa.Float(), nullable=False),
    sa.Column('car_license_plate', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('maintenance_id')
    )
    op.create_table('tb_states',
    sa.Column('state_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('state_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('tb_address',
    sa.Column('address_id', sa.Integer(), nullable=False),
    sa.Column('street', sa.String(), nullable=False),
    sa.Column('number', sa.String(), nullable=False),
    sa.Column('district', sa.String(), nullable=False),
    sa.Column('zip_code', sa.String(length=8), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('reference', sa.String(), nullable=False),
    sa.Column('state_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['state_id'], ['tb_states.state_id'], ),
    sa.PrimaryKeyConstraint('address_id')
    )
    op.create_table('tb_cars',
    sa.Column('chassis', sa.String(), nullable=False),
    sa.Column('license_plate', sa.String(length=7), nullable=False),
    sa.Column('brand', sa.String(), nullable=False),
    sa.Column('model', sa.String(), nullable=False),
    sa.Column('year', sa.String(), nullable=False),
    sa.Column('car_collor', sa.String(), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.Column('current_km', sa.Float(), nullable=False),
    sa.Column('licensing_expiration', sa.DateTime(), nullable=False),
    sa.Column('daily_rental_price', sa.Float(), nullable=False),
    sa.Column('daily_fixe_km', sa.Integer(), nullable=False),
    sa.Column('available', sa.Boolean(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('maintenance_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['tb_category_car.category_id'], ),
    sa.ForeignKeyConstraint(['maintenance_id'], ['tb_maintenance_car.maintenance_id'], ),
    sa.PrimaryKeyConstraint('chassis'),
    sa.UniqueConstraint('license_plate')
    )
    op.create_table('tb_users',
    sa.Column('cnh', sa.String(length=11), nullable=False),
    sa.Column('cpf', sa.String(length=11), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phone', sa.String(length=11), nullable=False),
    sa.Column('category_cnh', sa.String(length=2), nullable=False),
    sa.Column('id_address', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_address'], ['tb_address.address_id'], ),
    sa.PrimaryKeyConstraint('cnh'),
    sa.UniqueConstraint('cpf'),
    sa.UniqueConstraint('email')
    )
    op.create_table('tb_rental_cars',
    sa.Column('rental_id', sa.Integer(), nullable=False),
    sa.Column('rental_date', sa.DateTime(), nullable=False),
    sa.Column('rental_return_date', sa.DateTime(), nullable=False),
    sa.Column('rental_real_return_date', sa.DateTime(), nullable=True),
    sa.Column('returned_car', sa.Boolean(), nullable=True),
    sa.Column('rental_total_days', sa.Integer(), nullable=False),
    sa.Column('rental_real_total_days', sa.Integer(), nullable=True),
    sa.Column('initial_km', sa.Float(), nullable=False),
    sa.Column('final_km', sa.Float(), nullable=True),
    sa.Column('total_fixed_km', sa.Integer(), nullable=False),
    sa.Column('total_returned_km', sa.Float(), nullable=True),
    sa.Column('rental_value', sa.Float(), nullable=False),
    sa.Column('rental_real_value', sa.Float(), nullable=True),
    sa.Column('customer_cnh', sa.String(), nullable=False),
    sa.Column('car_license_plate', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['car_license_plate'], ['tb_cars.license_plate'], ),
    sa.ForeignKeyConstraint(['customer_cnh'], ['tb_users.cnh'], ),
    sa.PrimaryKeyConstraint('rental_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tb_rental_cars')
    op.drop_table('tb_users')
    op.drop_table('tb_cars')
    op.drop_table('tb_address')
    op.drop_table('tb_states')
    op.drop_table('tb_maintenance_car')
    op.drop_table('tb_category_car')
    # ### end Alembic commands ###
