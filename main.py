import psycopg2
try:
    connection = psycopg2.connect(
        user='nikita',
        password='1234',
        host='localhost',
        port='5438',
        database='db'
    )
    def select():
        with connection.cursor() as cursor:
            print('''Что вывести? 
             1 - Виды сенсоров 
             2 - Сенсоры метеостанции 
             3 - Все метеостанции
             4 - Записи наблюдений
             5 - Формулы для вычислений''')
            x = int(input("Введите номер варианта: "))
            if x == 1:
                cursor.execute(f'SELECT * FROM sensors;')
                for raw in cursor.fetchall():
                    print(raw)
            elif x == 2:
                cursor.execute(f'SELECT * FROM meteostations_sensors;')
                for raw in cursor.fetchall():
                    print(raw)
            elif x == 3:
                cursor.execute(f'SELECT * FROM meteostations;')
                for raw in cursor.fetchall():
                    print(raw)
            elif x == 4:
                cursor.execute(f'select sensor_inventory_number, measurement_value, measurement_ts, type_name FROM measurements join measurements_type on measurement_type = type_id;')
                for raw in cursor.fetchall():
                    print(raw)
            elif x == 5:
                cursor.execute(f'select sensor_name, type_name, measurment_formula from public.sensors_measurements join public.sensors on sensors.sensor_id = sensors_measurements.sensor_id join public.measurements_type  on measurements_type.type_id = sensors_measurements.type_id')
                for raw in cursor.fetchall():
                    print(raw)
            else:
                print('Неправильная команда!!!')

        print('Ещё что-нибудь?')

    def insert():
        with connection.cursor() as cursor:
            print('Что вы хотите добавить? \n 1 - Данные наблюдений. \n 2 - Новую станцию.')
            f = int(input('Введите номер варианта: '))
            if f ==1:
                print('Какой номер у сенсора, который вы использовали?')
                x = int(input('Введите номер: '))
                print('Что показывает сенсор?')
                y = float(input('Введите число: '))
                print('Когда были сделаны записи?')
                t = str(input('Введите точное время в формате "ГГГГ-ММ-ДД ЧЧ:ММ:СС": '))
                print('Какой тип измерений проводился?')
                cursor.execute(f'SELECT type_id, type_name  FROM measurements_type;')
                for raw in cursor.fetchall():
                    print(raw)
                s = int(input('Введите id: '))
                cursor.execute(f'''INSERT INTO measurements(sensor_inventory_number, measurement_value, measurement_ts, measurement_type)
                                                    values({x},{y},'{t}',{s});''')
            elif f == 2:
                x = str(input('Введите название новой станции: '))
                print('Введём координаты.')
                y = float(input('Введите долготу (формат 5,2): '))
                t = float(input('Введите широту (формат 5,2): '))
                cursor.execute(f'''INSERT INTO meteostations(station_name, station_longitude, station_latitude)
                                                                values('{x}',{y},{t});''')
            else:
                print('Неправильная команда!!!')
            print('Ещё что-нибудь?')

    def update():
        with connection.cursor() as cursor:
            print('Что вы хотите исправить? \n1 - Название станции.\n2 - Координаты станции.\n3 - Данные наблюдений.')
            f = int(input('Введите номер варианта: '))
            if f == 1:
                cursor.execute('SELECT * FROM meteostations;')
                for raw in cursor.fetchall():
                    print(raw)
                x = int(input('Введите id станции, которой нужно заменить название: '))
                y = str(input('Введите новое название: '))
                cursor.execute(f"UPDATE meteostations SET station_name = '{y}' WHERE station_id = {x};")
            elif f == 2:
                cursor.execute('SELECT * FROM meteostations;')
                for raw in cursor.fetchall():
                    print(raw)
                x = int(input('Введите id станции, которой нужно заменить координаты: '))
                y = float(input('Введите новоую долготу: '))
                s = float(input('Введите новоую широту: '))
                cursor.execute(
                            f"UPDATE meteostations SET station_longitude = {y}, station_latitude = {s} WHERE id = {x};")
            elif f == 3:
                cursor.execute(f'SELECT sensor_inventory_number, measurement_value, measurement_ts, type_name, type_units FROM measurements join measurements_type on measurements.measurement_type = measurements_type.type_id;')
                for raw in cursor.fetchall():
                    print(raw)
                print('Показатели какого сенсора нужно заменить?')
                x = str(input('Введите номер: '))
                print('Что показывает сенсор?')
                y = float(input('Введите температуру: '))
                print('Когда были сделаны записи?')
                t = str(input('Введите точное время в формате "ГГГГ-ММ-ДД ЧЧ:ММ:СС": '))
                print('Какой тип измерений проводился?')
                cursor.execute(f'SELECT type_id, type_name  FROM measurements_type;')
                for raw in cursor.fetchall():
                    print(raw)
                s = int(input('Введите id: '))
                cursor.execute(f'''UPDATE measurements SET measurement_value = {y}, measurement_ts = '{t}', measurement_type = {s} WHERE sensor_inventory_number = '{x}';''')
            else:
                print('Неправильная команда!!!')
                print('Ещё что-нибудь?')

    def delete():
        with connection.cursor() as cursor:
            print('Какую запись удалить: \n 1 - Наблюдения \n 2 - Метеостанцию')
            x = int(input("Введите число: "))
            if x == 1:
                cursor.execute('SELECT * FROM measurements;')
                for raw in cursor.fetchall():
                    print(raw)
                print('Запись с какой датой удалить: ')
                y = str(input('Введите точное время в формате "ГГГГ-ММ-ДД ЧЧ:ММ:СС": '))
                cursor.execute(f"DELETE FROM measurements WHERE measurement_ts = '{y}';")
            elif x == 2:
                cursor.execute('SELECT * FROM meteostations;')
                for raw in cursor.fetchall():
                    print(raw)
                print('Какую станцию удалить')
                y = int(input('Введите id: '))
                cursor.execute(f"DELETE FROM meteostations WHERE station_id = {y};")
            else:
                print('Неправильная команда')
        print('Ещё что-нибудь?')


    connection.autocommit = True

    print('Что вы хотите сделать?')
    while True:
        print('1 - Посмотреть данные')
        print('2 - Добавить новую запись')
        print('3 - Удалить запись наблюдений')
        print('4 - Исправить данные')
        print('5 - Завершить работу')
        f = int(input('Введите номер варианта: '))
        if f == 1:
            select()
        elif f == 2:
            insert()
        elif f == 3:
            delete()
        elif f == 4:
            update()
        elif f == 5:
            break
        else:
            print('Неверная команда!')

    print('Заходите ещё!')

except Exception as ex:
    print("[info] Error while working with PostgreSQL",ex)
finally:
    if connection:
        connection.close()
        print('[INFO] PostgreSQL connection closed')