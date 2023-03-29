import os
from sqlalchemy import orm, create_engine
from app.shared.infraestructure.migrations.villain import createTable as creatVillainTable
from app.shared.infraestructure.migrations.comic import createTable as createComicTable
from app.shared.infraestructure.migrations.character import createTable as createCharacterTable
from app.shared.infraestructure.migrations.log import createTable as createLogTable
from app.shared.domain.models.comic import Comic
from app.shared.domain.models.character import Character
from app.shared.domain.models.villain import Villain
from app.shared.domain.models.log import Log


registry = orm.registry()


def start_mappers():
    db_villain = creatVillainTable(registry.metadata)
    db_comic = createComicTable(registry.metadata)
    db_character = createCharacterTable(registry.metadata)
    db_log = createLogTable(registry.metadata)

    registry.map_imperatively(Villain, db_villain, properties={
        'comics': orm.relationship(Comic, backref='villain', order_by=db_comic.c.id)
    })

    registry.map_imperatively(Comic, db_comic, properties={
        'characters': orm.relationship(Character, backref='comic', order_by=db_character.c.id)
    })

    registry.map_imperatively(Character, db_character)
    registry.map_imperatively(Log, db_log)

    return registry.metadata


def get_session():
    engine = create_engine(os.environ.get("DATABASE_URL"))
    session = orm.sessionmaker(bind=engine)
    return session()
