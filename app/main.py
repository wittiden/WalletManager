from app.core.logger import add_logger
from app.parsers.currencies_name_parser import load_currencies_name_into_enum, start_currencies_name_parser


def main() -> None:

    add_logger()

    currencies_zipper = start_currencies_name_parser()
    load_currencies_name_into_enum(currencies_zipper)


if __name__ == '__main__':
    main()