import logging

from date_controller import DateController

logging.basicConfig(format='%(asctime)s |%(levelname)s| %(message)s', level=logging.DEBUG)

if __name__ == "__main__":
    try:
        while True:
            while True:
                try:
                    date = input("Hello user. Enter the date as sample: 30.02.2000 (dd.mm.yyyy) or ctr+C if you want to exit from the program:\t")
                    DateController.validate_date(date)            
                except (TypeError, ValueError) as error:
                    logging.error(f"{error}.\n\t\t\tPlease, try again!")
                else:
                    break
            while True:
                days_to_add = input("Enter the quantity of days that should be added to date:\t")
                if days_to_add.isdigit():
                    break
                else:
                    logging.warning(
                        "The entered days are not in valid format, please,"
                        "try to write only numeric symbols (for e.g. 10)"
                    )

            splitted_date = date.split(".")
            date_controller = DateController(*splitted_date)
            date_data = date_controller.add_date(days_to_add)
            logging.info("RESULT: %s.%s.%s\n", *date_data)
    except KeyboardInterrupt:
        logging.info("\nExit from the program.")