from sqlalchemy import Table, Column, Integer, String, ForeignKey

def createTable(metadata):
    character = Table(
        "character",
        metadata,
        Column("id", String(255), primary_key=True, nullable=True),
        Column("name", String(255), nullable=True),
        Column("uri", String(255), nullable=True),
        Column('comic_id', String(255), ForeignKey('comic.id'))
    )
    
    return character