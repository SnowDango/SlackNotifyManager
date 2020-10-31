import os


def logger(date, error):
    file_name = "error.log"
    if not os.path.isfile(file_name):
        with open(file_name, mode='w') as f:
            f.write(str(date))
            f.write(str(error))
    else:
        with open(file_name, mode='a') as f:
            f.write(str(date))
            f.write(str(error))
