from flask import Blueprint, render_template
from flask_login import login_required
from app.forms import TableAssignmentForm
from app.models import Table, Order

bp = Blueprint("orders", __name__, url_prefix="")


@bp.route("/")
@login_required
def index():
    return render_template('orders.html')

@bp.route("/tables")
@login_required
def assign_table():
    form=TableAssignmentForm
    # Get the tables and open orders
    tables = Table.query.order_by(Table.number).all()
    open_orders = Order.query.filter(Order.finished == False)

    # Get the table ids for the open orders
    busy_table_ids = [order.table_id for order in open_orders]

    # Filter the list of tables for only the open tables
    open_tables = [table for table in tables if table.id not in busy_table_ids]

    # Finally, convert those tables to tuples for the select field and set the
    # choices property to it
    form.tables.choices = [(t.id, f"Table {t.number}") for t in open_tables]

    return render_template('orders.html', form=form)
