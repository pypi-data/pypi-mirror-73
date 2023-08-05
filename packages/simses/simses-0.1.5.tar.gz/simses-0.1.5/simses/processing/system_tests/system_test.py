from configparser import ConfigParser
import os
from simses.processing.batch_processing import BatchProcessing


class TestBatchProcessing(BatchProcessing):

    def __init__(self):
        super().__init__(do_simulation=True, do_analysis=True)

    def _setup_config(self) -> dict:
        # test set for config setup
        i = 0
        configs: dict = dict()
        config: ConfigParser = ConfigParser()
        configs['Test_' + str(i)] = config
        i += 1
        dir = os.path.join(os.path.dirname(__file__), 'data')
        for file in os.listdir(dir):
            if file.endswith('.ini'):
                config: ConfigParser = ConfigParser()
                config.read(os.path.join(dir, file))
                configs['Test_' + str(i)] = config
                i += 1
        return configs


if __name__ == "__main__":
    batch_processing: BatchProcessing = TestBatchProcessing()
    batch_processing.run()
