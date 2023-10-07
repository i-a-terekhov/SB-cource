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


# ChatGPT так же не смог помочь:
# Кажется, проблема всё ещё связана с правами доступа к файлу базы данных. Возможно, у вас нет прав на запись в текущей
# директории или в месте, где находится файл "weather_database.bd".
# # Попробуйте следующее:
# # 1. Убедитесь, что файл "weather_database.bd" находится в директории, где вы выполняете вашу программу.
# # 2. Убедитесь, что у вас есть права на запись в этой директории. Если у вас нет прав на запись, вы можете
# попробовать выполнить программу с правами администратора или переместить файл базы данных в директорию, где у вас
# есть права на запись.
# # 3. Убедитесь, что файл "weather_database.bd" не открыт другой программой, так как SQLite может блокировать файл,
# если он уже открыт для записи.
# # Если ни одно из этих действий не помогло, попробуйте создать новую базу данных с другим именем файла в директории,
# где вы уверены, что у вас есть права на запись, и попробуйте подключиться к ней. Если это сработает, это может
# указывать на проблему с самим файлом "weather_database.bd".
