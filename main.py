import configurations
from runners.runners_factory import RunnersFactory
from exceptions import InternetException
import traceback


def main():
    try:
        runner = RunnersFactory(configurations.RUN_TYPE)
        runner.launch()

    except InternetException:
        print(traceback.format_exc())


if __name__ == "__main__":
    main()
