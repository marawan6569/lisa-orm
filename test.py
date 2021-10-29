from db import models


class User(models.Model):
    table_name ='User'

    user_id = models.IntegerField(table=table_name, unique=True)
    username = models.CharField(table=table_name, unique=True)
    f_name = models.CharField(table=table_name)
    m_name = models.CharField(table=table_name, null=True)
    l_name = models.CharField(table=table_name)

class Trainer(models.Model):
    table_name = 'Trainer'

    name = models.CharField(table=table_name)
    category = models.CharField(table=table_name)

user = User()
user.make_migrations()
user.user_id.make_migrations()
user.username.make_migrations()
user.f_name.make_migrations()
user.m_name.make_migrations()
user.l_name.make_migrations()

trainer = Trainer()
trainer.make_migrations()
trainer.name.make_migrations()
trainer.category.make_migrations()

user.migrate()
trainer.migrate()