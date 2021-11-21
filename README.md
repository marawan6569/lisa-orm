**__# lisa-orm
Lisa is an ORM semi like django ORM:

### Available fields now:
    - CharField()
    - IntegerField()
    - BooleanField()
    - FloatField()
    - TextField()
    - DateField() -> not fully ready
    - DateTimeField() -> not fully ready

### Available actions now:
    - add() -> to add recordes to DB
    - drop() -> to drop tables(models)
    - delete_field() -> to delete fields

### Available search methods:
    - get_all() -> to return all records in DB
    - get() -> to return specific record in DB 
        - not finshed yet (only geting first record in DB now)
<hr>

#### [>> github](https://github.com/marawan6569/lisa-orm)
#### [>> my linked in](https://www.linkedin.com/in/marwan6569/)
#### [>> my linktr.ee](https://linktr.ee/marawan6569)
#### [>> my facebook](https://www.facebook.com/marwanmo7amed8)
#### [>> my twitter](https://twitter.com/Marwan_Mo7amed_)
#### [>> my instagram](https://www.instagram.com/marwan_mohamed_0_0/)
<hr>

# Getting started:



## First: create your model:
  - create python file ex: ```my_model.py``` and write your model into it
```python
from lisa_orm.db import models


class MyModel(metaclass=models.ModelMeta):
  table_name = 'my_table_name' # -> Name your model it's mandatory
  
  my_field_one = models.CharField(max_length=40, null=True)
  my_field_two = models.IntegerField(unique=True)
```
  - then run your model by ```pythonX my_model.py ``` 
  - X is python version
 
 ## Second: make migrations:
   - create new file name it ```make_migrations.py``` 
   - or name it anything you want
   - write into it:
  ```python
from lisa_orm.migrations import make_migrations
  
  
make_migrations()
  ```
  - just run your  ```make_migrations.py``` 
  - by ```pythonX make_migrations.py```

## Third: migrate your model:
- create file ```migrate.py```
- or anything you want
- and write into it:
```python
from lisa_orm.migrate import migrate


migrate()
```
- run you ```migrate.py``` 
- by ```pythonX migrate.py```

## Note: I will make ```manage.py``` to make_migrations and migrate and some other actions (إن شاء الله)

<hr>

## Congratulations, you have just created your first model 😊

<hr>

# Now you can edit and add data and edit your model

- ## let's add some data:
```python
from lisa_orm.actions import add
from my_model import MyModel


add(
  model=MyModel,
  my_field_one = 'hello world!',
  my_field_two = 20
  )
  
add(
  model=MyModel,
  my_field_one = 'i love python',
  my_field_two = 50
  )
  
add(
  model=MyModel,
  my_field_one = 'i love lisa',
  my_field_two = 100
  )
```
- now run your file ```pythonX run your_file.py```
- you should see this output :
 ```
 data added successfully
 data added successfully
 data added successfully
 ```
 
 - you can delete a field from your model ... lets do it
 ```python
from lisa_orm.actions import delete_field
from my_model import MyModel
 
 
delete_field(
    model=MyModel,
    field_name='my_field_two'
 )
 ```
 - run your file
 - you should see this output:
 ```deleted field my_field_two successfully```


- And yo can drop your model also:
```python
from lisa_orm.actions import drop
from my_model import MyModel

drop(model=MyModel)
```
- run your file and you should see this output:
```
deleted model MyModel successfully
```

<hr>

# Let's get our data:
- ## you can get your all data by get_all():
```python
from lisa_orm.search import get_all
from my_model import MyModel

my_data_as_dict = get_all(model=MyModel)
my_data_as_json = get_all(model=MyModel, export_to_json=True)

# by default get_all and all methods in search  returns fetched data as a dict 
# but you can get data as json by passing export_to_json=True
```
- ## you can also get 1 record from DB with get():
```python
from lisa_orm.search import get
from my_model import MyModel

my_data_as_dict = get(model=MyModel)
my_data_as_json = get(model=MyModel, export_to_json=True)

# it is like get_all()
# It's not finished yet ... it is return only first record on DB
```

<hr>


# بس دي كل حاجة حتى الأن (: