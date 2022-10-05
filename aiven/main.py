import argparse

from aiven.consumer import run_consumer
from aiven.producer import run_producer

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("app")
    args = parser.parse_args()
    match args.app:
        case "consumer":
            run_consumer()
        case "producer":
            run_producer()
        case _:
            raise RuntimeError(
                "Application not allowed. It must be either consumer or producer."
            )
