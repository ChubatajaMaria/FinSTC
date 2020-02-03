import argparse

from lxml import etree


def validate(xml_string, xsd_string):
    """Валидирует xml-файл по xsd-схеме"""
    xsd_schema_root = etree.XML(xsd_string)
    schema = etree.XMLSchema(xsd_schema_root)
    parser = etree.XMLParser(schema=schema)
    try:
        etree.fromstring(xml_string, parser)
    except etree.XMLSyntaxError:
        print("Ошибка валидации")
        return False
    print("Валидация прошла успешно")
    return True


def reconstruct(xml_filepath, xslt_string):
    """Преобразование xml-файла по xslt-правилу"""
    xslt_root = etree.XML(xslt_string)
    transform = etree.XSLT(xslt_root)
    doc = etree.parse(xml_filepath)
    print("Преобразование прошло успешно")
    return transform(doc)


def _parse_args():
    parser = argparse.ArgumentParser(
        description='Скрипт, который валидирует и преобразовывает xml-файл',
    )
    parser.add_argument('xml_filepath', help='Путь до исходного xml-файла')
    parser.add_argument('xsd_filepath', help='Путь до валидирующей xsd-схемы')
    parser.add_argument(
        'xslt_filepath', help='Путь до преобразующего xslt-файла',
    )
    parser.add_argument('result_filename', help='Имя результирующего файла')
    return parser.parse_args()


def main():
    args = _parse_args()
    # Открываем все преданные файлы и считываем.
    try:
        with open(args.xml_filepath, 'rb') as xml_file:
            xml_string = xml_file.read()

        with open(args.xsd_filepath, 'rb') as xsd_file:
            xsd_string = xsd_file.read()

        with open(args.xslt_filepath, 'rb') as xslt_file:
            xslt_string = xslt_file.read()
    except FileNotFoundError as exc:
        print(f'Не найден файл {exc.filename}')
        return
    else:
        print(f'Все файлы успешно открыты')

    correct = validate(xml_string, xsd_string)

    if correct:
        result_tree = reconstruct(args.xml_filepath, xslt_string)
        with open(args.result_filename, 'wb') as newfile:
            newfile.write(etree.tostring(result_tree))
        print(f'Файл {args.result_filename} успешно сохранён')


if __name__ == '__main__':
    main()

