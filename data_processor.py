class data_processor:
    # Processes one data stream at a time
    # Eventually, the jacobean logic may go in here
    def __init__(self):
        self.zero_value = 0

    def data_point(self, point):
        return point - self.zero_value
