import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}" \
    .format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    """
    setup_db(app)
    binds a flask application and a SQLAlchemy service
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

    return db


def insert_mock_data():
    drink = Drink(
        title='Drink 1',
        recipe=json.dumps([{
            'name': 'Drink 1 - Part',
            'color': 'red',
            'parts': 1
        }])
    )
    drink.insert()
    drink = Drink(
        title='Drink 2',
        recipe=json.dumps([
            {
                'name': 'Drink 2 - Part 1',
                'color': 'green',
                'parts': 1
            },
            {
                'name': 'Drink 2 - Part 2',
                'color': 'yellow',
                'parts': 1
            }
        ])
    )
    drink.insert()
    drink = Drink(
        title='Drink 3',
        recipe=json.dumps([
            {
                'name': 'Drink 3 - Part 1',
                'color': 'pink',
                'parts': 1
            },
            {
                'name': 'Drink 3 - Part 2',
                'color': 'black',
                'parts': 1
            }
        ])
    )
    drink.insert()


def db_drop_and_create_all():
    """
    db_drop_and_create_all()
        drops the database tables and starts fresh
        can be used to initialize a clean database
        !!NOTE you can change the database_filename variable to
        have multiple versions of a database
    """
    db.drop_all()
    db.create_all()
    insert_mock_data()


class Drink(db.Model):
    """
    Drink
    a persistent drink entity, extends the base SQLAlchemy Model
    """
    # Auto-incrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Title
    title = Column(String(80), unique=True)
    # the ingredients blob - this stores a lazy json blob
    # the required datatype is
    # [{'color': string, 'name':string, 'parts':number}]
    recipe = Column(String(180), nullable=False)

    def short(self):
        """
        short()
            short form representation of the Drink model
        """
        # print(json.loads(self.recipe))
        short_recipe = [{'color': r['color'], 'parts': r['parts']}
                        for r in json.loads(self.recipe)]
        return {
            'id': self.id,
            'title': self.title,
            'recipe': short_recipe
        }

    def long(self):
        """
        long()
            long form representation of the Drink model
        """
        return {
            'id': self.id,
            'title': self.title,
            'recipe': json.loads(self.recipe)
        }

    def insert(self):
        """
        insert()
            inserts a new model into a database
            the model must have a unique name
            the model must have a unique id or null id
            EXAMPLE
                drink = Drink(title=req_title, recipe=req_recipe)
                drink.insert()
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        delete()
            deletes a new model into a database
            the model must exist in the database
            EXAMPLE
                drink = Drink(title=req_title, recipe=req_recipe)
                drink.delete()
        """
        db.session.delete(self)
        db.session.commit()

    def update(self):
        """
        update()
            updates a new model into a database
            the model must exist in the database
            EXAMPLE
                drink = Drink.query.filter(Drink.id == id).one_or_none()
                drink.title = 'Black Coffee'
                drink.update()
        """
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())


def drinks_list_short(drink_list):
    """Return the short form of Drink for a list"""
    return [drink.short() for drink in drink_list]


def drinks_list_complete(drink_list):
    """Return the long form of Drink for a list"""
    return [drink.long() for drink in drink_list]
