from sqlalchemy import Table, Column, Integer, String, ForeignKey

def createTable(metadata):
    comic = Table(
        "comic",
        metadata,
        Column("id", String(255), primary_key=True),
        Column("digital_id", String(255), nullable=True),
        Column("title", String(255), nullable=True),
        Column("description", String(255), nullable=True),
        Column('villain_id', String(255), ForeignKey('villain.id'))
    )
    
    return comic