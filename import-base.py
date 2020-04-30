#!/usr/bin/env python

from gdp import GDP, GSP, State, db

import csv

from datetime import date

infile = 'datasrc/GDP.csv'

tas = State('Tasmania', 'TAS')
nsw = State('New South Wales', 'NSW')
qld = State('Queensland', 'QLD')
vic = State('Victoria', 'VIC')
act = State('Australian Capital Territory', 'ACT')
sa = State('South Austrlia', 'SA')
nt = State('Northern Territory', 'NT')
wa = State('Western Australia', 'WA')

db.session.add(nsw)
db.session.add(act)
db.session.add(qld)
db.session.add(vic)
db.session.add(sa)
db.session.add(nt)
db.session.add(wa)
db.session.add(tas)
db.session.commit()
