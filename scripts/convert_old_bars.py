import csv

__author__ = 'Robbert Harms'
__date__ = "2015-09-20"
__maintainer__ = "Robbert Harms"
__email__ = "robbert.harms@maastrichtuniversity.nl"


def convert_file(filename, result_dir):
    lh_list = []
    rh_list = []

    with open(filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csv_reader:
            lh = [row[4], row[0]]
            if row[2]:
                lh.append(row[2])

            rh = [row[4], row[1]]
            if row[3]:
                rh.append(row[3])

            lh_list.append(lh)
            rh_list.append(rh)

    with open(result_dir + '_lh.txt', 'w') as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        csv_writer.writerows(lh_list)

    with open(result_dir + '_rh.txt', 'w') as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        csv_writer.writerows(rh_list)

convert_file('/home/robbert/programming/python/musical-games/musical_games/data/kirnberger/menuet_trio/piano/bars_menuet.txt',
             '/home/robbert/programming/python/musical-games/musical_games/data/kirnberger/menuet_trio/piano/bars_menuet')