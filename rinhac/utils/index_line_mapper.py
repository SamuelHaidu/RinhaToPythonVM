class IndexLineMapper:

    def __init__(self, file_path):
        self.file_path = file_path
        self.index_line_map = {}

        with open(self.file_path) as f:
            char_count = 0
            for index, line in enumerate(f):
                line_number = index + 1
                self.index_line_map[line_number] = {}
                self.index_line_map[line_number]['start'] = char_count
                char_count += len(line)
                self.index_line_map[line_number]['end'] = char_count - 1


    def get_line_number(self, char_index: int) -> int:
        for index, line in self.index_line_map.items():
            if line['start'] <= char_index <= line['end']:
                return index
        raise Exception('char_index out of bounds')
