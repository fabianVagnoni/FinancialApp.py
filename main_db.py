import jsonFileCreator
import dbUpdaterHistorical
import dbUpdaterRatios

def main():
    db1 = jsonFileCreator.jsonFileCreator()
    db2= dbUpdaterRatios.dbUpdaterRatios()
    db3 = dbUpdaterHistorical.dbUpdaterHistorical()


main()