from datetime import datetime
from decimal import Decimal
from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
import bisect


class CarService:
    STR_LENGTH = 200

    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path
        self.file_path_models = root_directory_path + "models.txt"
        self.file_path_models_idx = root_directory_path + "models_index.txt"
        self.file_path_cars = root_directory_path + "cars.txt"
        self.file_path_cars_idx = root_directory_path + "cars_index.txt"
        self.file_path_sales = root_directory_path + "sales.txt"
        self.file_path_sales_idx = root_directory_path + "sales_index.txt"

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:

        with open(self.file_path_models, "a") as f: 
             f.write(f"{model.id};{model.name};{model.brand}".ljust(self.STR_LENGTH) + "\n")
        
        #Считаем номер строки, которую только что вставили
        with open(self.file_path_models, "r") as f:
            lines = f.readlines()
            line_number = len(lines)  # Количество строк в файле = номер строки для новой модели

        # Запись индекса в файл "models_index.txt"
        with open(self.file_path_models_idx, 'a') as file:
            pass

        with open(self.file_path_models_idx, "r") as index_file:
            lines = index_file.readlines()
        if lines == []:
            lines.insert(0, f"{model.id};{line_number}\n")
        else:
            for index, line in enumerate(lines):
                if int(line.split(';')[0]) < model.id:
                    if index == len(lines) -1:
                        lines.insert(index + 1, f"{model.id};{line_number}\n")
                        break
                    else:
                        continue
                else:
                    lines.insert(index, f"{model.id};{line_number}\n")
                    break
        with open(self.file_path_models_idx, "w") as index_file:
            index_file.writelines(lines)


    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        with open(self.file_path_cars, "a") as f: 
            f.write(f"{car.vin};{car.model};{car.price};{car.date_start};{car.status}".ljust(self.STR_LENGTH) + "\n")
        
        #Считаем номер строки, которую только что вставили
        with open(self.file_path_cars, "r") as f:
            lines = f.readlines()
            line_number = len(lines)  # Количество строк в файле = номер строки для новой модели

        # Запись индекса в файл "models_index.txt"
        self.add_cars_idx(car.vin, line_number)

    def add_cars_idx(self, vin: str, line_number: int) -> None:
        with open(self.file_path_cars_idx, "a") as file:
            pass

        with open(self.file_path_cars_idx, "r") as index_file:
            lines = index_file.readlines()
        if lines == []:
            lines.insert(0, f"{vin};{line_number}\n")
        else:
            for index, line in enumerate(lines):
                if line.split(';')[0] < vin:
                    if index == len(lines) -1:
                        lines.insert(index + 1, f"{vin};{line_number}\n")
                        break
                    else:
                        continue
                else:
                    lines.insert(index, f"{vin};{line_number}\n")
                    break

        with open(self.file_path_cars_idx, "w") as index_file:
            index_file.writelines(lines)

    #########################################################################3
    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:

        with open(self.file_path_sales, "a") as f: # r+ нужен для того, чтобы была возможность писать в тот же файл, что читаем.
            f.write(f"{sale.sales_number};{sale.car_vin};{sale.sales_date};{sale.cost}".ljust(self.STR_LENGTH) + "\n")
        
        #Считаем номер строки, которую только что вставили
        with open(self.file_path_sales, "r") as f:
            lines = f.readlines()
            line_number = len(lines)  # Количество строк в файле = номер строки для новой модели

        # Запись индекса в файл "models_index.txt"
        self.add_sales_idx(vin=sale.car_vin,line_number=line_number)

        # Ищем в файле cars_index номер строки, в которой в таблице car хранится информация о машине
        row_number = self.get_row_number_by_idx(self.file_path_cars_idx, sale.car_vin)
        #print("Sales row_number = ", row_number)
        self.change_car_status(row_number, CarStatus.sold)

    def get_row_number_by_idx(self, file_path: str, target_id) -> int | None:
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            print("Ключ не найден.")
            return None

        # Разбиваем строки на кортежи (id, row_number)
        data = [(line.split(';')[0], int(line.split(';')[1])) for line in lines]

        # Получаем список только с id для бинарного поиска
        ids = [item[0] for item in data]

        # Находим индекс, где может быть наш id
        index = bisect.bisect_left(ids, target_id)

        # Если индекс валиден и найден элемент
        if index < len(ids) and ids[index] == target_id:
            return data[index][1]  # Возвращаем row_number
        else:
            return None  # Если id не найден
        
    def add_sales_idx(self, vin: str, line_number: int) -> None:   
        with open(self.file_path_sales_idx, "a") as file:
            pass

        with open(self.file_path_sales_idx, "r") as index_file:
            lines = index_file.readlines()
        if lines == []:
            lines.insert(0, f"{vin};{line_number}\n")
        else:
            for index, line in enumerate(lines):
                if line.split(';')[0] < vin:
                    if index == len(lines) -1:
                        lines.insert(index + 1, f"{vin};{line_number}\n")
                        break
                    else:
                        continue
                else:
                    lines.insert(index, f"{vin};{line_number}\n")
                    break

        with open(self.file_path_sales_idx, "w") as index_file:
            index_file.writelines(lines)


    def change_car_status(self, row_number: int, status: CarStatus) -> None:
        # Обновляем статус машины
        with open(self.file_path_cars, "r+") as f:  # Открываем файл в режиме чтения и записи
            f.seek((row_number - 1) * (self.STR_LENGTH + 2))  # Перемещаем указатель на нужную строку (self.STR_LENGTH + \r\n)
            line = f.read(self.STR_LENGTH)  # Читаем строку длиной self.STR_LENGTH символов
            print("sell_car old line =", repr(line))
            new_line = line.replace(line.split(';')[-1], status, 1)  # Заменяем статус
            print("sell_car new line =", repr(new_line.ljust(self.STR_LENGTH)))
            f.seek((row_number - 1)  * (self.STR_LENGTH + 2))  # Возвращаемся в то же место, чтобы записать измененную строку
            f.write(f"{new_line}".ljust(self.STR_LENGTH))  # Записываем новую строку (дополняем до self.STR_LENGTH символов)

    ########################################################################################
    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:

        with open(self.file_path_cars,"r") as f:
            lines = f.readlines()

        # Разбиваем строки на кортежи (id, row_number)
        cars_in_status = []
        cars_data = [(line.split(';')[0], int(line.split(';')[1]), line.split(';')[2], line.split(';')[3], line.split(';')[4]) for line in lines]
        for car in cars_data:
            if car[4].strip() == str(status):
                cars_in_status.append(Car(vin=car[0], model=int(car[1]), price=Decimal(car[2]), date_start=datetime.strptime(car[3], '%Y-%m-%d %H:%M:%S').date(), status= status))
        
        return cars_in_status
 
    ####################################################
    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:

        car_row_number = self.get_row_number_by_idx(self.file_path_cars_idx, vin)
        if car_row_number is None:
            print("vin не найден в базе данных")
            return None
        with open(self.file_path_cars, "r") as f:  # Открываем файл в режиме чтения
            f.seek((car_row_number - 1) * (self.STR_LENGTH + 2))  # Перемещаем указатель на нужную строку
            car_info = f.read(self.STR_LENGTH)  # Читаем строку длиной self.STR_LENGTH символов

        model_row_number =  self.get_row_number_by_idx(self.file_path_models_idx, car_info.split(';')[1])   
        with open(self.file_path_models, "r") as f:  
            f.seek((model_row_number - 1) * (self.STR_LENGTH + 2))  # Перемещаем указатель на нужную строку
            model_info = f.read(self.STR_LENGTH)  # Читаем строку длиной self.STR_LENGTH символов

        sale_row_number = self.get_row_number_by_idx(self.file_path_sales_idx, vin)
        if sale_row_number is None:
            return CarFullInfo(vin=vin,car_model_name=model_info.split(';')[1].strip(), car_model_brand=model_info.split(';')[2].strip(),
                           price=Decimal(car_info.split(';')[2]), date_start=datetime.strptime(car_info.split(';')[3], '%Y-%m-%d %H:%M:%S'),status=CarStatus[car_info.split(';')[4].strip()],
                           sales_date=None,sales_cost=None)
        else:
            with open(self.file_path_sales, "r") as f:  # Открываем файл в режиме чтения и записи
                f.seek((sale_row_number - 1) * (self.STR_LENGTH + 2))  # Перемещаем указатель на нужную строку
                sales_info = f.read(self.STR_LENGTH)  # Читаем строку длиной self.STR_LENGTH символов
            return CarFullInfo(vin=vin,car_model_name=model_info.split(';')[1].strip(), car_model_brand=model_info.split(';')[2].strip(),
                           price=Decimal(car_info.split(';')[2]), date_start=datetime.strptime(car_info.split(';')[3], '%Y-%m-%d %H:%M:%S'),status=CarStatus[car_info.split(';')[4].strip()],
                           sales_date=datetime.strptime(sales_info.split(';')[2], '%Y-%m-%d %H:%M:%S'),sales_cost=Decimal(sales_info.split(';')[3]))
    
    ####################################################
    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
        row_number = self.get_row_number_by_idx(self.file_path_cars_idx, vin)
        if row_number is None:
            print("vin не найден в базе данных")
            return None
        # Обновляем vin машины в файле cars.txt
        with open(self.file_path_cars, "r+") as f:  # Открываем файл в режиме чтения и записи
            f.seek((row_number - 1) * (self.STR_LENGTH + 2))  # Перемещаем указатель на нужную строку
            line = f.read(self.STR_LENGTH)  # Читаем строку длиной self.STR_LENGTH символов
            print("update_vin old line = ", line)
            new_line = line.replace(line.split(';')[0], new_vin, 1)  # Заменяем vin на new_vin
            new_line = new_line.strip()
            print("update_vin new line = ", new_line)
            f.seek((row_number - 1)  * (self.STR_LENGTH + 2))  # Возвращаемся в то же место, чтобы записать измененную строку
            f.write((new_line).ljust(self.STR_LENGTH) + "\n")  # Записываем новую строку (дополняем до self.STR_LENGTH символов)

        # Обновляем vin машины в файле cars_idx.txt
        with open(self.file_path_cars_idx,"r+") as f:
            lines = f.readlines()

        index_data = [(line.split(';')[0], int(line.split(';')[1])) for line in lines]

        #удаляем файл cars_idx.txt и добавляем записи в новый файл cars_idx.txt
        with open(self.file_path_cars_idx, 'w') as f:
            pass

        for line in index_data:
            if line[0] == vin:
                self.add_cars_idx(new_vin, line[1])
            else:
                self.add_cars_idx(line[0], line[1])
        
    #####################################################
    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        vin = sales_number.split('#')[-1]
        vin = vin.strip()
        print("revert_sale vin = ", vin)

        # Ищем в файле cars_index номер строки, в которой в таблице car хранится информация о машине
        row_number_sale = self.get_row_number_by_idx(self.file_path_sales_idx, vin)
        row_number_car = self.get_row_number_by_idx(self.file_path_cars_idx, vin)

        # Обновляем статус машины на available
        self.change_car_status(row_number_car, CarStatus.available)
            
        #Добавляем флаг is_deleted! к записи о сорвавшейся продаже
        with open(self.file_path_sales, "r+") as f:  # Открываем файл в режиме чтения и записи
            f.seek((row_number_sale - 1) * (self.STR_LENGTH + 2))  # Перемещаем указатель на нужную строку
            line = f.read(self.STR_LENGTH)  # Читаем строку длиной self.STR_LENGTH символов
            new_line = "is_deleted!" + line.strip()  # Заменяем vin на new_vin
            f.seek((row_number_sale - 1)  * (self.STR_LENGTH + 2))  # Возвращаемся в то же место, чтобы записать измененную строку
            f.write((new_line).ljust(self.STR_LENGTH))  # Записываем новую строку (дополняем до self.STR_LENGTH символов)

        #Удаляем запись о продаже из файла sales_idx.txt
        with open(self.file_path_sales_idx,"r") as f:
            lines = f.readlines()

        index_data = [(line.split(';')[0], int(line.split(';')[1])) for line in lines]

        #удаляем записи из sales_idx.txt и добавляем записи в новый файл sales_idx.txt
        with open(self.file_path_sales_idx, 'w') as f:
            pass

        for line in index_data:
            if line[0] != vin:
               self.add_sales_idx(line[0], line[1])

    #######################################################
    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        top_models = dict()

        with open(self.file_path_sales_idx, "r") as f:
            lines = f.readlines()

        vin_data = [line.split(";")[0] for line in lines]

        for vin in vin_data:
            model_info = self.get_car_info(vin=vin)
            model = model_info.car_model_name
            if model in dict.keys(top_models):
                sales_count, price, brand = top_models[model]
                top_models[model] = (sales_count + 1, model_info.price, model_info.car_model_brand)
            else:
                top_models[model] = (1, model_info.price, model_info.car_model_brand)

        sorted_top_models = sorted(top_models.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)

        top_3_models = [ModelSaleStats(car_model_name=model, brand=brand, sales_number=sales_count)
                         for model, (sales_count, price, brand) in sorted_top_models[:3]]

        return top_3_models

if __name__ == '__main__':
    file_path = "C:\\Users\\oblad\\Desktop\\Practicum\\bibip\\"
    car_service = CarService(file_path)
    # add models
    """
    car_service.add_model(Model(id=3, name="Optima", brand="Kia"))
    car_service.add_model(Model(id=2, name="Sorento", brand="Kia"))
    car_service.add_model(Model(id=1, name="3", brand="Mazda"))
    car_service.add_model(Model(id=4, name="Pathfinder", brand="Nissan"))
    car_service.add_model(Model(id=5, name="Logan", brand="Renault"))
    """
    # add cars
    """
    car_service.add_car(Car(vin="KNAGM4A77D5316538", model=1, price=Decimal("2000"), date_start=datetime(2024, 2, 8), status=CarStatus.available,))
    car_service.add_car(Car(vin="5XYPH4A10GG021831", model=2, price=Decimal("2300"), date_start=datetime(2024, 2, 20), status=CarStatus.reserve,))
    car_service.add_car(Car(vin="KNAGH4A48A5414970", model=1, price=Decimal("2100"), date_start=datetime(2024, 4, 4),  status=CarStatus.available,))
    car_service.add_car(Car(vin="JM1BL1M58C1614725", model=2, price=Decimal("2100"), date_start=datetime(2024, 4, 7),  status=CarStatus.available,))
    cars = [
         Car(
            vin="5N1CR2MN9EC641864",
            model=4,
            price=Decimal("3100"),
            date_start=datetime(2024, 6, 1),
            status=CarStatus.available,
        ),
        Car(
            vin="JM1BL1L83C1660152",
            model=3,
            price=Decimal("2635.17"),
            date_start=datetime(2024, 6, 1),
            status=CarStatus.available,
        ),
        Car(
            vin="5N1CR2TS0HW037674",
            model=4,
            price=Decimal("3100"),
            date_start=datetime(2024, 6, 1),
            status=CarStatus.available,
        ),
        Car(
            vin="5N1AR2MM4DC605884",
            model=4,
            price=Decimal("3200"),
            date_start=datetime(2024, 7, 15),
            status=CarStatus.available,
        ),
        Car(
            vin="VF1LZL2T4BC242298",
            model=5,
            price=Decimal("2280.76"),
            date_start=datetime(2024, 8, 31),
            status=CarStatus.delivery,
        )
    ]
    for car in cars:
        car_service.add_car(car)
    """

    """
    sales = [
            Sale(
                sales_number="20240903#KNAGM4A77D5316538",
                car_vin="KNAGM4A77D5316538",
                sales_date=datetime(2024, 9, 3),
                cost=Decimal("1999.09"),
            ),
            Sale(
                sales_number="20240903#KNAGH4A48A5414970",
                car_vin="KNAGH4A48A5414970",
                sales_date=datetime(2024, 9, 4),
                cost=Decimal("2100"),
            ),
            Sale(
                sales_number="20240903#5N1CR2MN9EC641864",
                car_vin="5N1CR2MN9EC641864",
                sales_date=datetime(2024, 9, 5),
                cost=Decimal("7623"),
            ),
            Sale(
                sales_number="20240903#5N1CR2TS0HW037674",
                car_vin="5N1CR2TS0HW037674",
                sales_date=datetime(2024, 9, 6),
                cost=Decimal("2334"),
            ),
            Sale(
                sales_number="20240903#5N1AR2MM4DC605884",
                car_vin="5N1AR2MM4DC605884",
                sales_date=datetime(2024, 9, 7),
                cost=Decimal("451"),
            ),
            Sale(
                sales_number="20240903#VF1LZL2T4BC242298",
                car_vin="VF1LZL2T4BC242298",
                sales_date=datetime(2024, 9, 8),
                cost=Decimal("9876"),
            ),
            Sale(
                sales_number="20240903#5XYPH4A10GG021831",
                car_vin="5XYPH4A10GG021831",
                sales_date=datetime(2024, 9, 9),
                cost=Decimal("1234"),
            ),
        ]

    for sale in sales:
        car_service.sell_car(sale)
    """

    """
    sale1 = Sale(
            sales_number="20240903#KNAGM4A77D5316538",
            car_vin="KNAGM4A77D5316538",
            sales_date=datetime(2024, 9, 3),
            cost=Decimal("2399.99"),
        )
    car_service.sell_car(sale1)
   
    sale2 = Sale(
            sales_number="20240903#5XYPH4A10GG021831",
            car_vin="5XYPH4A10GG021831",
            sales_date=datetime(2024, 9, 3),
            cost=Decimal("2399.99"),
        )
    car_service.sell_car(sale2)
   
    sale3 = Sale(
            sales_number="20241003#KNAGH4A48A5414970",
            car_vin="KNAGH4A48A5414970",
            sales_date=datetime(2024, 9, 3),
            cost=Decimal("2399.99"),
        )
    car_service.sell_car(sale3)
    """
    #car_service.revert_sale("20240903#5XYPH4A10GG021831")
    #car_service.revert_sale("20240903#KNAGH4A48A5414970")

    #print(car_service.get_car_info("JM1BL1M58C1614725"))
    #print(car_service.get_car_info("KNAGM4A77D5316538"))

    #print(car_service.get_cars(CarStatus.available))
    #print(car_service.get_car_info("KNAGM4A77D5316538")) 
    #print(car_service.get_car_info("KNAGH4A48A5414970")) 
    #car_service.update_vin("KNAGH4A48A5414970", "3NAGH4A48A5414970")
    #car_service.revert_sale("20240903#JM1BL1M58C1614725")
    #print(car_service.top_models_by_sales())