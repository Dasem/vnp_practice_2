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

    @staticmethod
    def features_json(features_arr):
        names = ['f' + str(ordinal) for ordinal in range(len(features_arr))]
        for_json = dict(zip(names, zip(*features_arr)))
        return json.dumps(for_json)


if __name__ == "__main__":
    collector = FeatureCollector('test.exe')

    if re.search(b'\xc7\x85.*\xfe\xff\xff.*\x00\x00.*\xeb\x0f.*\x8b\x85.*\xfe\xff\xff.*\x83\xc0\x01\x89\x85.*\xfe\xff\xff.*\xfe\xff\xff.*\x7d\x25', collector.file_bytes):
        collector.add_feature(1)
    else:
        collector.add_feature(0)

    print(collector.features)
