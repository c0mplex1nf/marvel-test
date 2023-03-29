from sqlalchemy import Table, MetaData, Column, Integer, String, DateTime, ForeignKey


def createTable(metadata):
    log = Table(
        "log",
        metadata,
        Column("id", String(255), primary_key=True, nullable=False),
        Column("villain_name", String(255), nullable=False),
        Column("created_at", DateTime(), nullable=False),
    )

    return log
