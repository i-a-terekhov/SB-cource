import peewee

database = peewee.SqliteDatabase('weather_database.bd')


class BaseTable(peewee.Model):
    class Meta:
        database = database


class Day(BaseTable):
    day = peewee.CharField()


class TimeOfDay(BaseTable):
    time = peewee.CharField()


class WeatherData(BaseTable):
    day = peewee.ForeignKeyField(Day)
    time = peewee.ForeignKeyField(TimeOfDay)
    weekday = peewee.CharField()
    content = peewee.CharField()
    weather = peewee.CharField()
    full_date = peewee.CharField()


database.connect()
database.create_tables([Day, TimeOfDay, WeatherData])
