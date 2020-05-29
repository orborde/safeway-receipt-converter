#!/usr/bin/env python3

import csv
import sys

_, inp = sys.argv


class ParseFailure(Exception):
    pass

def parseprice(line):
    assert len(line) == 38
    clubcode = line[:7].strip()
    s1 = line[7]
    if s1 != ' ':
        raise ParseFailure('first space not present', repr(line), s1)
    item = line[8:28].strip()
    if item == '':
        raise ParseFailure('blank item', repr(line))
    s2 = line[28]
    if s2 != ' ':
        raise ParseFailure('second space not present', repr(line), s2)
    price = line[29:36].strip()
    minus = line[36]
    if minus not in [' ', '-']:
        raise ParseFailure('nonsensical minus code', repr(line), minus)
    pricegroup = (minus+price).strip()
    if pricegroup == '':
        raise ParseFailure('no price', repr(line), price, minus)
    endcode = line[37].strip()
    return clubcode, item, pricegroup, endcode

c = csv.writer(sys.stdout)
with open(inp, 'r') as i:
    itembuf = []
    for line in i:
        line = line.strip('\n')
        if line == '':
            continue

        try:
            parse = parseprice(line)
        except ParseFailure as e:
            print(repr(line), file=sys.stderr)
            print(e, file=sys.stderr)
            itembuf.append(line)
            continue

        clubcode, item, pricegroup, endcode = parse
        itembuf.append((clubcode+' '+item).strip())
        c.writerow(['\n'.join(itembuf), pricegroup])
        itembuf = []

assert len(itembuf) == 0
