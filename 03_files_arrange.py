

# Нужно написать скрипт для упорядочивания фотографий (вообще любых файлов)
# Скрипт должен разложить файлы из одной папки по годам и месяцам в другую.
# Например, так:
#   исходная папка
#       icons/cat.jpg
#       icons/man.jpg
#       icons/new_year_01.jpg
#   результирующая папка
#       icons_by_year/2018/05/cat.jpg
#       icons_by_year/2018/05/man.jpg
#       icons_by_year/2017/12/new_year_01.jpg
#
# Входные параметры основной функции: папка для сканирования, целевая папка.
# Имена файлов в процессе работы скрипта не менять, год и месяц взять из времени создания файла.
# Обработчик файлов делать в обьектном стиле - на классах.
#
# Файлы для работы взять из архива icons.zip - раззиповать проводником в папку icons перед написанием кода.
# Имя целевой папки - icons_by_year (тогда она не попадет в коммит)
#
# Пригодятся функции:
#   os.walk
#   os.path.dirname
#   os.path.join
#   os.path.normpath
#   os.path.getmtime
#   time.gmtime
#   os.makedirs
#   shutil.copy2
#
# Чтение документации/гугла по функциям - приветствуется. Как и поиск альтернативных вариантов :)
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.

import os, time, shutil
import zipfile


class Failer():
    """Класс распределения файлов из папки/архива в новые папки согласно дате создания"""

    def __init__(self, source_folder='icons.zip', resulting_folder='icons_by_year'):
        self.source_folder = source_folder
        self.resulting_folder = resulting_folder

    def _folder_is_zip(self):
        if self.source_folder.endswith('zip'):
            return True
        else:
            return False

    def read_address(self):
        if self._folder_is_zip():
            self._read_zip()
        else:
            print('Файл не является архивом')

    def _read_zip(self):
        os.makedirs('temp', exist_ok=True)
        with zipfile.ZipFile(self.source_folder, 'r') as zip_file:
            for each_file in zip_file.infolist():
                if not each_file.is_dir():
                    # Создаем папку для файла на основании метаданных
                    data_of_create = each_file.date_time[:3]
                    year, month, day = data_of_create
                    new_folder = os.path.join(self.resulting_folder, str(year), f'{month:02d}', f'{day:02d}')
                    os.makedirs(new_folder, exist_ok=True)

                    # Создаем буфер, куда перемещаем файл перед копированием в папку назначения
                    _, file_name = os.path.split(each_file.filename)
                    address_of_new_file = os.path.join(new_folder, file_name)
                    temp_path = os.path.join('temp', file_name)
                    with zip_file.open(each_file) as old_file, open(temp_path, 'wb') as temp_file:
                        shutil.copyfileobj(old_file, temp_file)
                    shutil.move(temp_path, address_of_new_file)

                    # Меняем временные метки
                    access_time = modification_time = int(time.mktime(each_file.date_time + (0, 0, -1)))
                    os.utime(address_of_new_file, (access_time, modification_time))
        shutil.rmtree('temp')


raspredelytor = Failer()
raspredelytor.read_address()

# Усложненное задание (делать по желанию)
# Нужно обрабатывать zip-файл, содержащий фотографии, без предварительного извлечения файлов в папку.
# Основная функция должна брать параметром имя zip-файла и имя целевой папки.
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828
