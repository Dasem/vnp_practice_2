import re
import json
import os


class FeatureCollector(object):

    def __init__(self, file_path):
        self.file_path = file_path
        self.file_bytes = open(file_path, 'rb').read()
        self.features = []

    def parse(self, parse_fun):
        return parse_fun(self.file_bytes)

    def add_feature(self, feature):
        self.features.append(feature)

    def add_feature_if_match(self, pattern):
        if re.search(pattern, self.file_bytes):
            self.add_feature(1)
        else:
            self.add_feature(0)

    def default_analyze(self):
        # 1 for (i = 0; i < n; i++)
        # (самый дефолтный цикл)
        self.add_feature_if_match(
            b'\xc7\x85.{0,20}\xff\xff.{0,20}\x00\x00.{0,20}\xeb\x0f.{0,20}\x8b\x85.{0,20}\xff\xff.{0,20}\x83\xc0\x01\x89\x85.{0,20}\xff\xff.{0,20}\xff\xff.{0,20}\x7d\x25')

        # 2 sum += A[i]
        # (сложение инта с элементом массива)
        self.add_feature_if_match(
            b'\x8b\x85.{0,20}\xff\xff\x8b\x8d.{0,20}\xff\xff\x03\x8c\x85.{0,20}\xff\xff\x89\x8d.{0,20}\xff\xff')

        # 3 min > A[i]
        # (сравнение инта с элементом массива)
        self.add_feature_if_match(
            b'\x8b\x85.{0,20}\xff\xff\x8b\x8d.{0,20}\xff\xff\x3b\x8c\x85.{0,20}\xff\xff\x7e\x13')

        # 4 min = A[i]
        # (присвоение инту элемента массива)
        self.add_feature_if_match(
            b'\x8b\x85.{0,20}\xfe\xff\xff\x8b\x8c\x85\x68\xfe\xff\xff\x89\x8d.{0,20}\xfe\xff\xff')

        # 5 temp = A[j];
        # A[j] = A[j + 1];
        # A[j + 1] = temp;
        # (свап элементов, часто при сортировках)
        self.add_feature_if_match(
            b'\x8B\x85.{0,20}\xFE\xFF\xFF\x8B\x8C\x85\x68\xFE\xFF\xFF\x89\x8D.{0,20}\xFE\xFF\xFF\x8B\x85.{0,20}\xFE\xFF\xFF\x8B\x8D.{0,20}\xFE\xFF\xFF\x8B\x94\x8D\x6C\xFE\xFF\xFF\x89\x94\x85\x68\xFE\xFF\xFF\x8B\x85.{0,20}\xFE\xFF\xFF\x8B\x8D.{0,20}\xFE\xFF\xFF\x89\x8C\x85\x6C\xFE\xFF\xFF')

        # 6 A[j] < A[min]
        # (сравнение элементов массива)
        self.add_feature_if_match(
            b'\x8b\x85.{0,20}\xff\xff\x8b\x8d.{0,20}\xff\xff\x8b\x94\x85.{0,20}\xff\xff\x3b\x94\x8d.{0,20}\xff\xff.{0,20}\x40')

        # 7 A[i] = A[min]
        # (присвоение элемента массива элементу массива)
        self.add_feature_if_match(
            b'\x8b\x85.{0,20}\xff\xff\x8b\x8d.{0,20}\xff\xff\x8b\x94\x8d.{0,20}\xff\xff\x89\x94\x85.{0,20}\xff\xff')

        # 8 sum += i (сложение инта с интом; i++ не считается)
        self.add_feature_if_match(b'\x8B\x45.{0,20}\x03\x45.{0,20}\x89\x45')

        # 9 pr *= i (умножение инта на инт)
        self.add_feature_if_match(b'\x8B\x45.{0,20}\x0F\xAF\x45.{0,20}\x89\x45')

        # 10 sum = 0
        # (присвоение переменной константы)
        self.add_feature_if_match(b'\xc7\x45.{0,20}\x00\x00\x00')

        # Заполнение элемента случайным числом A[i] = rand()
        self.add_feature(0)  # всё равно у меня такой фигни нет

        # Чтение с консоли cin >> x
        self.add_feature_if_match(b'\xff\x15\xa0\xd0')  # всё равно у меня такой фигни нет

        # Вывод в консоль cout << x
        self.add_feature(1)  # всё равно у меня такая фигня везде

        # Присваивание элементу массива инта A[i] =x
        self.add_feature_if_match(b'\x8b\x8d.{0,20}\xfe\xff\xff\x89\x8c.{0,20}\xfe\xff\xff')

    def get_features_dict(self):
        print(f'Features list: {self.features} for file: {self.file_path}')
        names = ['f' + str(ordinal) for ordinal in range(len(self.features))]
        for_json = dict(zip(names, self.features))
        return for_json

    def get_features_json(self):
        return json.dumps(self.get_features_dict())

    @staticmethod
    def analyze_folder(folder, result_ds_path=None):
        file_list = []
        for root, dirs, files in os.walk(folder):
            for filename in files:
                file_list.append(root + '\\' + filename)

        result_dict = []
        for filename in file_list:
            collector = FeatureCollector(filename)
            collector.default_analyze()
            result_dict.append(collector.get_features_dict())
        json_string = json.dumps(result_dict)
        if result_ds_path:
            with open(result_ds_path, 'w') as export:
                export.write(json_string)
        return json_string


if __name__ == "__main__":
    json = FeatureCollector.analyze_folder("progs", 'result_ds.json')
