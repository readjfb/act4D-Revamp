import os


class data_saver(object):
    """
    data_saver encapsulates a cache of data to be saved as well as the underlying code to save the data
    """

    def __init__(self, save_directory, state):
        """
        Construct a new 'data_saver' object.

        :param save_directory: The name of the directory within the /data/ folder to be saved to
        :return: returns new datasaver object
        """
        self.data_cache = []
        self.save_dir = os.getcwd() + "/data/" + save_directory

        self.state = state

        self.header = None

    def add_data(self, line):
        """Add a list to be appended

        Args:
            line list[any]: List that will be saved as it's own row
        """
        self.data_cache.append(line)

    def clear(self):
        """
        Clear the data cache AND the header

        :return: returns nothing
        """
        self.header = None
        self.data_cache.clear()

    def add_header(self, header_list):
        """Adds a header. Care should be taken S.T. the header has the proper order

        Args:
            header_list list[any]: Ordered list of desired header
        """

        self.header = header_list

    def save_data(self, mode):
        """
        Command that creates and writes a new file based on the cache

        :param mode: tell the object the mode, which informs the directory to
        be saved in

        :return: returns nothing
        """

        path = f"{self.save_dir}/{mode}/"

        try:
            os.makedirs(path)
        except OSError:
            # print("Creation of the directory %s failed" % path)
            pass
        else:
            print("Successfully created the directory %s" % path)

        i = 0
        while os.path.exists(f"{path}{mode}_data{i}.csv"):
            i += 1

        with open(f"{path}{mode}_data{i}.csv", "w") as file:
            if self.header:
                file.write(",".join([str(x) for x in self.header]) + "\n")

            for line in self.data_cache:
                file.write(",".join([str(x) for x in line]) + "\n")

        print(f"Successfully wrote to file {path}{mode}_data{i}.csv")
        return


if __name__ == "__main__":
    save = data_saver("test_test", "Testing")

    save.add_data([1, 2, 3, 4])
    save.add_data([2, 5, 1, 5])
    save.add_data([3, 7, 7, 7])
    save.add_data([4, 8, 8, 8])

    save.add_header(["Index", "Round", "Par1", "Par2"])

    save.save_data("MVT_L")
