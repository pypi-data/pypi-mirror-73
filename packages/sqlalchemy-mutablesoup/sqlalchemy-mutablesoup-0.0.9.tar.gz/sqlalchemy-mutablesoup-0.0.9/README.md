SQLAlchemy-MutableSoup defines a mutable [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) [SQLAlchemy](https://www.sqlalchemy.org/) database type.

## Installation

```
$ pip install sqlalchemy-mutablesoup
```

## Quickstart

```python
from sqlalchemy_mutablesoup import MutableSoupType

from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# standard session creation
engine = create_engine('sqlite:///:memory:')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()
Base = declarative_base()

# define and instantiate a model with a MutableSoupType column.
class Model(Base):
    __tablename__ = 'model'
    id = Column(Integer, primary_key=True)
    soup = Column(MutableSoupType)
    
Base.metadata.create_all(engine)

model = Model()
session.add(model)
```

You can now treat `model.soup` as a `bs4.BeautifulSoup` object.

## Citation

```
@software{bowen2020sqlalchemy-mutablesoup,
  author = {Dillon Bowen},
  title = {SQLAlchemy-MutableSoup},
  url = {https://dsbowen.github.io/sqlalchemy-mutablesoup/},
  date = {2020-06-04},
}
```

## License

Users must cite this package in any publications which use it.

It is licensed with the MIT [License](https://github.com/dsbowen/sqlalchemy-mutablesoup/blob/master/LICENSE).