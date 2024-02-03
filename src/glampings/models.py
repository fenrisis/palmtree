from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData, ForeignKey, Numeric, Text, JSON

metadata = MetaData()

# Таблица для глемпингов
glamping = Table(
    "glamping",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("description", Text),
    Column("price_per_night", Numeric, nullable=False),
    Column("capacity", Integer, nullable=False),
    Column("location", String),
    Column("amenities", JSON),
    Column("owner_id", Integer, ForeignKey("user.id")),
)

# Таблица для аренды
rental = Table(
    "rental",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("glamping_id", Integer, ForeignKey("glamping.id")),
    Column("start_date", TIMESTAMP, nullable=False),
    Column("end_date", TIMESTAMP, nullable=False),
    Column("total_cost", Numeric, nullable=False),
    Column("status", String, nullable=False),
)