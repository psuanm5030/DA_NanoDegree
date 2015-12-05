__author__ = 'Miller'

"""
Your task is to check the "productionStartYear" of the DBPedia autos datafile for valid values.
The following things should be done:
- check if the field "productionStartYear" contains a year
- check if the year is in range 1886-2014
- convert the value of the field to be just a year (not full datetime)
- the rest of the fields and values should stay the same
- if the value of the field is a valid year in range, as described above,
  write that line to the output_good file
- if the value of the field is not a valid year,
  write that line to the output_bad file
- discard rows (neither write to good nor bad) if the URI is not from dbpedia.org
- you should use the provided way of reading and writing data (DictReader and DictWriter)
  They will take care of dealing with the header.

You can write helper functions for checking the data and writing the files, but we will call only the
'process_file' with 3 arguments (inputfile, output_good, output_bad).
"""
import csv
import pprint

INPUT_FILE = '/Users/Miller/GitHub/GhNanoDegree/Class_DataWrangling/Lesson3_AuditData/autos.csv'
OUTPUT_GOOD = '/Users/Miller/GitHub/GhNanoDegree/Class_DataWrangling/Lesson3_AuditData/autos-valid.csv'
OUTPUT_BAD = '/Users/Miller/GitHub/GhNanoDegree/Class_DataWrangling/Lesson3_AuditData/FIXME-autos.csv'

def process_file(input_file, output_good, output_bad):

    with open(input_file, "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames

        # cnt = 0
        # for row in reader:
        #     #print "new row-----> \n"
        #     #pprint.pprint(row)
        #     print 'dbpedia' in row['URI']
        #     if cnt == 4:
        #         #break
        #         pass
        #
        #     cnt += 1

        good_output = []
        bad_output = []
        cnt = 0
        for row in reader:
            print 'row --> ', cnt
            cnt+=1
            test = check_validity(row)
            print 'RESULT!!! ', test
            if test == 'discard':
                continue
            elif test == 'write_good':
                row['productionStartYear'] = row['productionStartYear'][:4]
                good_output.append(row)
            elif test == 'write_bad':
                bad_output.append(row)
            else:
                print 'SOMETHING WRONG!'
    # print 'WRITE GOOD LIST: \n', good_output
    # Write the two files - Good List
    with open(output_good,'w') as g:
        writer = csv.DictWriter(g, delimiter = ",", fieldnames=header)
        writer.writeheader()
        for row in good_output:
            writer.writerow(row)
    # print 'WRITE bad LIST: \n', bad_output
    # Write the two files - Bad List
    with open(output_bad,'w') as b:
        writer = csv.DictWriter(b, delimiter = ",", fieldnames=header)
        writer.writeheader()
        for row in bad_output:
            writer.writerow(row)

    print 'Completed...'
    return

def check_validity(checkRow):
    """
    Check for NULL and for extraneous values.
    :param val:
    :return:
    """

    val = checkRow['productionStartYear']

    # Perform major checks first:
    print 'uri --> ', checkRow['URI'], ' --- year --> ', val
    if 'dbpedia' not in checkRow['URI']:
        # print 'yes - this row to be discarded',checkRow['URI']
        print 'DISCARD'
        return 'discard'
    elif val == 'NULL':
        print 'WRITE_BAD'
        return 'write_bad'

    # Perform secondary checks:
    try:
        new_val = int(val[:4])
        if (int(val[:4]) >= 1886 and int(val[:4]) <= 2014):
            print 'WRITE_GOOD'
            return 'write_good'
        else:
            print 'WRITE_BAD 2'
            return 'write_bad'
    except:
        print 'Value in secondary checks cannot be converted to an integer!'
        return

def test():

    process_file(INPUT_FILE, OUTPUT_GOOD, OUTPUT_BAD)


if __name__ == "__main__":
    test()