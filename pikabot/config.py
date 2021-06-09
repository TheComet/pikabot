import toml
import logging
import collections

logger = logging.getLogger(__name__)


def merge_dict(d1, d2):
    """
    Modifies d1 in-place to contain values from d2.  If any value
    in d1 is a dictionary (or dict-like), *and* the corresponding
    value in d2 is also a dictionary, then merge them in-place.
    """
    for k, v2 in d2.items():
        v1 = d1.get(k)  # returns None if v1 has no value for this key
        if (isinstance(v1, collections.Mapping) and
                isinstance(v2, collections.Mapping)):
            merge_dict(v1, v2)
        else:
            d1[k] = v2


class Config:
    def __init__(self, *config_files):
        """
        Loads and merges a list of config files, or if the list is empty, the config dict will be an empty dict.
        :param config_files: List of files to load.
        """
        self.__config = dict()

        for file in config_files:
            self.load_append(file)

    def load_append(self, filename):
        """
        Loads a config file and appends (merges) it with the existing config dict. Any values that already exist in the
        dict are overwritten with new values from the file.
        :return: Returns True if the file was loaded and merged, False if otherwise (e.g. the file does not exist).
        """
        try:
            logger.info(f"Loading config file {filename}")
            self.append(toml.load(filename))
        except Exception:
            logger.exception(f"Failed to load config file {filename}")
            return False

        return True

    def append(self, other_dict):
        merge_dict(self.__config, other_dict)

    def save(self, filename):
        logger.info(f"Saving config file {filename}")
        with open(filename, "wb") as f:
            f.write(toml.dumps(self.__config).encode("utf-8"))

    def __getitem__(self, item):
        return self.__config[item]
