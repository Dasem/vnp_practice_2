import re
import json


class FeatureCollector(object):

    def __init__(self, file_path):
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

    @staticmethod
    def features_json(features_arr):
        names = ['f' + str(ordinal) for ordinal in range(len(features_arr))]
        for_json = dict(zip(names, zip(*features_arr)))
        return json.dumps(for_json)


if __name__ == "__main__":
    collector = FeatureCollector('3sortPuz.exe')

    # for (i = 0; i < n; i++)
    # (самый дефолтный цикл)
    collector.add_feature_if_match(b'\xc7\x85.{0,20}\xff\xff.{0,20}\x00\x00.{0,20}\xeb\x0f.{0,20}\x8b\x85.{0,20}\xff\xff.{0,20}\x83\xc0\x01\x89\x85.{0,20}\xff\xff.{0,20}\xff\xff.{0,20}\x7d\x25')
    print("done 1-st")

    # sum += A[i]
    # (сложение инта с элементом массива)
    collector.add_feature_if_match(b'\x8b\x85.{0,20}\xff\xff\x8b\x8d.{0,20}\xff\xff\x03\x8c\x85.{0,20}\xff\xff\x89\x8d.{0,20}\xff\xff')
    print("done 2-nd")

    # min > A[i]
    # (сравнение инта с элементом массива)
    collector.add_feature_if_match(b'\x8b\x85.{0,20}\xff\xff\x8b\x8d.{0,20}\xff\xff\x3b\x8c\x85.{0,20}\xff\xff\x7e\x13')
    print("done 3-rd")

    # min = A[i] TODO: перепроверить
    # (присвоение инту элемента массива)
    collector.add_feature_if_match(b'\x8b\x85.{0,20}\xff\xff\x8b\x8d.{0,20}\xff\xff\x03\x8c\x85.{0,20}\xff\xff\x89\x8d.{0,20}\xff\xff')
    print("done 4-th")

    # temp = A[j];
    # A[j] = A[j + 1];
    # A[j + 1] = temp;
    # (свап элементов, часто при сортировках)
    collector.add_feature_if_match(b'\x8B\x85.{0,20}\xFE\xFF\xFF\x8B\x8C\x85\x68\xFE\xFF\xFF\x89\x8D.{0,20}\xFE\xFF\xFF\x8B\x85.{0,20}\xFE\xFF\xFF\x8B\x8D.{0,20}\xFE\xFF\xFF\x8B\x94\x8D\x6C\xFE\xFF\xFF\x89\x94\x85\x68\xFE\xFF\xFF\x8B\x85.{0,20}\xFE\xFF\xFF\x8B\x8D.{0,20}\xFE\xFF\xFF\x89\x8C\x85\x6C\xFE\xFF\xFF')
    print("done 5-th")

    print(collector.features)
