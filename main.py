import argparse
import logging
import yaml
from src.one_time_pad import OneTimePadSystem

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_config(config_path: str = "config/config.yaml") -> dict:
    """Load configuration from YAML file"""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="One-Time Pad Stream Cipher System")
    parser.add_argument("mode", choices=["sender", "receiver"], help="Operating mode")
    parser.add_argument(
        "--config", default="config/config.yaml", help="Configuration file path"
    )
    parser.add_argument("--input", help="Input file path (for sender)")
    parser.add_argument("--output", help="Output file path (for receiver)")
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Logging level (DEBUG, INFO, WARNING, ERROR)",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    system = OneTimePadSystem(config)

    if args.mode == "sender":
        if not args.input:
            raise ValueError("Input file required for sender mode")
        system.sender(args.input)
    else:
        if not args.output:
            raise ValueError("Output file required for receiver mode")
        system.receiver(args.output)


if __name__ == "__main__":
    main()
