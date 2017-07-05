class LoadFile(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        result = []
        with open(self.file_path) as f:
            for line in f.readlines():
                result.append(line.strip())

        return result



