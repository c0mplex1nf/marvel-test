from sqlalchemy import Table, MetaData, Column, Integer, String, Date, ForeignKey

def createTable(metadata):
    villain = Table(
        "villain",
        metadata,
        Column("id", String(255), primary_key=True, nullable=False),
        Column("name", String(255), nullable=True),
        Column("description", String(255), nullable=True),
        Column("image", String(255), nullable=True),
    )

    return villain
