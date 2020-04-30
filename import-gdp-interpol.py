#!/usr/bin/env python

from gdp import GDP, GSP, State, db, GDP2

import csv

from datetime import date

infile = 'datasrc/GDP2.csv'

tas = State.query.filter_by(short='TAS').first()
vic = State.query.filter_by(short='VIC').first()
nsw = State.query.filter_by(short='NSW').first()
qld = State.query.filter_by(short='QLD').first()
sa = State.query.filter_by(short='SA').first()
nt = State.query.filter_by(short='NT').first()
act = State.query.filter_by(short='ACT').first()
wa = State.query.filter_by(short='WA').first()

m = {}
m['Jan'] = 1
m['Feb'] = 2
m['Mar'] = 3
m['Apr'] = 4
m['May'] = 5
m['Jun'] = 6
m['Jul'] = 7
m['Aug'] = 8
m['Sep'] = 9
m['Oct'] = 10
m['Nov'] = 11
m['Dec'] = 12

with open(infile, 'rb') as csvfile:
  creader = csv.reader(csvfile, delimiter=',', quotechar='"')
  ln=0
  for row in creader:
    if ln >0:
      m2, y = row[0].split('-')
      period = date(month=m[m2], year=int(y), day=1)
      gdp = GDP2(period, gdp=int(row[9]), nsw=int(row[1]), vic=int(row[2]), qld=int(row[3]), sa=int(row[4]), wa=int(row[5]), tas=int(row[6]), nt=int(row[7]), act=int(row[8]))
      db.session.add(gdp)
      db.session.commit()
    ln += 1