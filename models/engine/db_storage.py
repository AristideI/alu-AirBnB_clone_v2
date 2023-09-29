#!/usr/bin/python3
"""This is the db storage class for AirBnB"""
import datetime
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage():
    """
    Database Engine for AirBnB project
    """
    __engine = None
    __session = None

    def __init__(self):
        """Init method"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """Returns dictionary with all objects depending
        of the class name (argument cls)"""
        if cls:
            objs = self.__session.query(self.classes()[cls])
        else:
            objs = self.__session.query(State).all()
            objs += self.__session.query(City).all()
            objs += self.__session.query(User).all()
            objs += self.__session.query(Place).all()
            objs += self.__session.query(Amenity).all()
            objs += self.__session.query(Review).all()

        dic = {}
        for obj in objs:
            k = '{}.{}'.format(type(obj).__name__, obj.id)
            dic[k] = obj
        return dic

    def new(self, obj):
        """Add the object to the current
        database session (self.__session)"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current
        database session (self.__session)"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create the current database session (self.__session) from
        the engine (self.__engine) by using a sessionmaker"""
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        Base.metadata.create_all(self.__engine)
        self.__session = sessionmaker(bind=self.__engine,
                                      expire_on_commit=False)
        Session = scoped_session(self.__session)
        self.__session = Session()

    def close(self):
        """Removes the session"""
        self.__session.close()

    def classes(self):
        """Returns a dictionary of valid classes and their references."""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review}
        return classes

    def attributes(self):
        """Returns the valid attributes and their types for classname."""
        attributes = {
            "BaseModel":
                     {"id": str,
                      "created_at": datetime.datetime,
                      "updated_at": datetime.datetime},
            "User":
                     {"email": str,
                      "password": str,
                      "first_name": str,
                      "last_name": str},
            "State":
                     {"name": str},
            "City":
                     {"state_id": str,
                      "name": str},
            "Amenity":
                     {"name": str},
            "Place":
                     {"city_id": str,
                      "user_id": str,
                      "name": str,
                      "description": str,
                      "number_rooms": int,
                      "number_bathrooms": int,
                      "max_guest": int,
                      "price_by_night": int,
                      "latitude": float,
                      "longitude": float,
                      "amenity_ids": list},
            "Review":
            {"place_id": str,
                         "user_id": str,
                         "text": str}
        }
        return attributes

# #!/usr/bin/python3
# """Defines the DBStorage engine."""
# import datetime
# from os import getenv
# from sqlalchemy.orm import sessionmaker, scoped_session, relationship
# from sqlalchemy import create_engine
# from models.base_model import BaseModel, Base
# from models.amenity import Amenity
# from models.city import City
# from models.place import Place
# from models.review import Review
# from models.state import State
# from models.user import User

# class DBStorage:
#     """Represents a database storage engine.
#     Attributes:
#         __engine (sqlalchemy.Engine): The working SQLAlchemy engine.
#         __session (sqlalchemy.Session): The working SQLAlchemy session.
#     """

#     __engine = None
#     __session = None

#     def __init__(self):
#         """Initialize a new DBStorage instance."""
#         self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
#                                       format(getenv("HBNB_MYSQL_USER"),
#                                              getenv("HBNB_MYSQL_PWD"),
#                                              getenv("HBNB_MYSQL_HOST"),
#                                              getenv("HBNB_MYSQL_DB")),
#                                       pool_pre_ping=True)
#         if getenv("HBNB_ENV") == "test":
#             Base.metadata.drop_all(self.__engine)

#     def all(self, cls=None):
#         """Query on the curret database session all objects of the given class.
#         If cls is None, queries all types of objects.
#         Return:
#             Dict of queried classes in the format <class name>.<obj id> = obj.
#         """
#         if cls is None:
#             objs = self.__session.query(State).all()
#             objs.extend(self.__session.query(City).all())
#             objs.extend(self.__session.query(User).all())
#             objs.extend(self.__session.query(Place).all())
#             objs.extend(self.__session.query(Review).all())
#             objs.extend(self.__session.query(Amenity).all())
#         else:
#             if isinstance(cls, str):
#                 cls = eval(cls)
#             objs = self.__session.query(cls)
#         return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}

#     def new(self, obj):
#         """Add obj to the current database session."""
#         self.__session.add(obj)

#     def save(self):
#         """Commit all changes to the current database session."""
#         self.__session.commit()

#     def delete(self, obj=None):
#         """Delete obj from the current database session."""
#         if obj is not None:
#             self.__session.delete(obj)

#     def reload(self):
#         """Create all tables in the database and initialize a new session."""
#         Base.metadata.create_all(self.__engine)
#         session_factory = sessionmaker(bind=self.__engine,
#                                        expire_on_commit=False)
#         Session = scoped_session(session_factory)
#         self.__session = Session()

#     def close(self):
#         """Close the working SQLAlchemy session."""
#         self.__session.close()