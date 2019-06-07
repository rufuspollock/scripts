from StringIO import StringIO
test_data = '''"Date","Description","Debit","Credit","Balance","Comments"
04/05/04,"XXXX",-29.94,,0.0,
10/05/04,"YYYY",-11.33,,0.0,"onething"
13/05/04,"CREDIT",,203,0.0,"repayment"
13/05/04,"ZZZZ",-50.29,,0.0,"onething"
14/05/04,"PHONE",-113.38,,0.0,"anotherthing"
17/05/04,"CREDIT",,30,0.0,IR
'''
testfo = StringIO(test_data)

import csv2qif


def ourmapper(row, key):
    mappings = {
        'D': 0,
        'M': 1,
        'P': 1,
        'L': 5,
        }
    if key == 'T':
        if row[2].strip():
            return row[2]
        else:
            return row[3]
    elif key in mappings:
        return row[mappings[key]]
    else:
        return ''

def test_1():
    out = csv2qif.convert(testfo, ourmapper)
    assert len(out) > 0
    lines = out.split()
    assert lines[0] == '!Type:Bank'
    assert lines[1] == 'D05/04/04', lines[1]
    assert lines[2] == 'PXXXX'

