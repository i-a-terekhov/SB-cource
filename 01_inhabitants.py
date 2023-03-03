# Вывести на консоль жителей комнат (модули room_1 и room_2)
# Формат: В комнате room_1 живут: ...

import room_1 as apart_1
import room_2 as apart_2


for room_number in [apart_1, apart_2]:
    print(f'В комнате {room_number.__name__} живут:', room_number.folks)

