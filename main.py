import os
import argparse
from typing import List, Dict


class PhoneBook:
    def __init__(self, filename: str) -> None:
        """
        Инициализация телефонного справочника.
        :param filename: имя файла для хранения данных.
        """
        if filename is None:
            filename = 'phonebook.txt'

        self.filename = filename
        self.contacts = []
        self.load_contacts()
        self.contact_field = {
            1: "surname",
            2: "first_name",
            3: "patronymic",
            4: "organization",
            5: "work_phone",
            6: "personal_phone"
        }

    def load_contacts(self) -> None:
        """
        Загрузка данных их файла в справочник.
        """
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                for line in file:
                    contact = line.strip().split(', ')
                    self.contacts.append({
                        "surname": contact[0],
                        "first_name": contact[1],
                        "patronymic": contact[2],
                        "organization": contact[3],
                        "work_phone": contact[4],
                        "personal_phone": contact[5]
                    })

    def save_contacts(self, contact: Dict[str, str] | None = None) -> None:
        """
        Сохранение записей из справочника в файл.
        :param contact: запись в телефонном справочнике.
        """
        with open(self.filename, 'a', encoding='utf-8') as file:
            if contact is not None:
                line = '\n' + ', '.join(contact.values())
                file.write(line)
                return

            for contact in self.contacts:
                line = '\n' + ', '.join(contact.values())
                file.write(line)

    def display_contacts(self, page_size: int = None) -> None:
        """
        Вывод постранично записей из справочника на экран.
        :param page_size: количество записей на странице.
        """
        if page_size is None:
            for i, contact in enumerate(self.contacts):
                print(f'{i + 1}. {contact["surname"]}, {contact["first_name"]}, {contact["patronymic"]}, '
                      f'{contact["organization"]}, {contact["work_phone"]}, {contact["personal_phone"]}')
            return

        for i, contact in enumerate(self.contacts):
            if i % page_size == 0 and i != 0:
                user_input = input(
                    'Нажмите Enter для перехода к следующей странице справочника'
                    ' или введите "N", чтобы завершить просмотр записей справочника: '
                )
                if user_input.upper() == 'N':
                    return
            print(f'{i + 1}. {contact["surname"]}, {contact["first_name"]}, {contact["patronymic"]}, '
                  f'{contact["organization"]}, {contact["work_phone"]}, {contact["personal_phone"]}')

    def add_contact(
            self, surname: str, first_name: str, patronymic: str,
            organization: str, work_phone: str, personal_phone: str
    ) -> None:
        """
        Добавление новой записи в справочник.
        :param surname: фамилия.
        :param first_name: имя.
        :param patronymic: отчество.
        :param organization: название организации.
        :param work_phone: телефон рабочий.
        :param personal_phone: телефон личный.
        """
        new_contact = {
            "surname": surname,
            "first_name": first_name,
            "patronymic": patronymic,
            "organization": organization,
            "work_phone": work_phone,
            "personal_phone": personal_phone
        }
        self.contacts.append(new_contact)
        self.save_contacts(new_contact)

    def edit_contact(self, index: int, field: int, new_value: str) -> None:
        """
        Редактирование записи в справочнике.
        :param index: индекс записи в справочнике.
        :param field: характеристика записи для редактирования.
        :param new_value: новое значение записи для данной характеристики.
        :return:
        """
        name_field = self.contact_field[field]
        self.contacts[index][name_field] = new_value
        self.save_contacts()

    def search_contacts(
            self, result_contact: List[Dict[str, str]],
            field: int, value: str
    ) -> List[Dict[str, str]]:
        """
        Поиск записей по одной или нескольким характеристикам в справочнике.
        :param result_contact: список найденных записей.
        :param field: характеристика записи для поиска.
        :param value: значение характеристики для поиска.
        :return: список найденных записей.
        """
        result = []
        name_field = self.contact_field[field]

        if not result_contact:
            for contact in self.contacts:
                if value.lower() in contact[name_field].lower():
                    result.append(contact)
        else:
            for contact in result_contact:
                if value.lower() in contact[name_field].lower():
                    result.append(contact)

        return result

    def is_empty(self) -> bool:
        """
        Проверка справочника на наличие записей.
        """
        if not self.contacts:
            return True


def print_fields():
    """
    Вывод на экран характеристик записей в телефонном спрвочнике.
    """
    print('1. Фамилия')
    print('2. Имя')
    print('3. Отчество')
    print('4. Название организации')
    print('5. Рабочий телефон')
    print('6. Личный телефон')


def main():
    """
    Консольный интерфейс программы.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-file', help='Filename of the phonebook', default=None, type=str, nargs='?')
    args = parser.parse_args()

    phone_book = PhoneBook(args.file)

    while True:
        print('\n')
        print('_-' * 20)
        print(' ' * 12, 'PhoneBook')
        print('_-' * 20)
        print('1. Вывести записи из справочника')
        print('2. Добавить новую запись в справочник')
        print('3. Редактировать запись в справочнике')
        print('4. Поиск записей по одной или нескольким характеристикам')
        print('5. Выход')

        choice = input('Введите номер вашего действия: ').strip()

        if choice == '1':
            if phone_book.is_empty():
                print('Пустой справочник.')
                continue

            page_size = input('Введите количество записей на странице: ').strip()
            while not page_size.isdigit() or page_size == '0':
                page_size = input('Введите целое число больше нуля: ').strip()

            phone_book.display_contacts(int(page_size))

        elif choice == '2':
            surname = input('Введите фамилию: ').strip()
            first_name = input('Введите имя: ').strip()
            patronymic = input('Введите отчество: ').strip()
            organization = input('Введите название организации: ').strip()
            work_phone = input('Введите рабочий телефон: ').strip()
            personal_phone = input('Введите личный телефон: ').strip()
            phone_book.add_contact(
                surname, first_name, patronymic, organization,
                work_phone, personal_phone
            )
            print('Запись добавлена в справочник.')

        elif choice == '3':
            if phone_book.is_empty():
                print('Пустой справочник.')
                continue

            phone_book.display_contacts()
            contact_index = input('Введите номер записи для редактирования: ').strip()
            while not contact_index.isdigit() or not 0 < int(contact_index) <= len(phone_book.contacts):
                contact_index = input('Введите правильный номер записи: ').strip()

            print_fields()
            contact_field = input(
                'Введите номер характеристики, которую хотите отредактировать,'
                ' или "N", чтобы завершить редактирование: '
            ).strip()
            if contact_field.upper() == 'N':
                continue

            while contact_field.upper() != 'N':
                while not contact_field.isdigit() or not 0 < int(contact_field) <= 6:
                    contact_field = input('Введите указанные номера характеристик: ').strip()

                new_value = input('Введите новое значение: ').strip()
                phone_book.edit_contact(int(contact_index) - 1, int(contact_field), new_value)

                print_fields()
                contact_field = input(
                    'Введите еще номер характеристики, которую хотите отредактировать,'
                    ' или "N", чтобы завершить редактирование: '
                ).strip()

            print('Редактирование записи завершено.')

        elif choice == '4':
            if phone_book.is_empty():
                print('Пустой справочник.')
                continue

            result = []
            print_fields()
            contact_field = input(
                'Введите номер характеристики для поиска записи в справочнике,'
                ' или "N", чтобы завершить поиск: '
            ).strip()
            if contact_field.upper() == 'N':
                continue

            while contact_field.upper() != 'N':
                while not contact_field.isdigit() or not 0 < int(contact_field) <= 6:
                    contact_field = input('Введите указанные номера характеристик: ').strip()

                search_value = input('Введите значение для поиска в справочнике: ').strip()
                result = phone_book.search_contacts(result, int(contact_field), search_value)

                print_fields()
                contact_field = input(
                    'Введите еще номер характеристики для поиска записи в справочнике,'
                    ' или "N", чтобы завершить поиск: '
                ).strip()

            if not result:
                print('Указанные записи в справочнике не найдены.')
                continue

            print('Результаты поиска:')
            for i, contact in enumerate(result):
                print(f'{i + 1}. {contact["surname"]}, {contact["first_name"]}, {contact["patronymic"]}, '
                      f'{contact["organization"]}, {contact["work_phone"]}, {contact["personal_phone"]}')

        elif choice == '5':
            break

        else:
            print('Несуществующий номер. Введите правильный номер действия: ')


if __name__ == '__main__':
    main()
