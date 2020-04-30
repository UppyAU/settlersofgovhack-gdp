#!/usr/bin/env python

from gdp import GDP, GSP, State, db

import csv

from datetime import date

infile = 'datasrc/GDP.csv'

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
m['Dev'] = 12

with open(infile, 'rb') as csvfile:
  creader = csv.reader(csvfile, delimiter=',', quotechar='"')
  ln=0
  for row in creader:
    if ln >0:
      m2, y = row[0].split('-')
      p = '01-' + row[0]
      period = date(month=m[m2], year=int(y), day=1)
      gdp = GDP(period, row[9])
      gsp_tas = GSP(tas, period, row[6])
      gsp_nsw = GSP(nsw, period, row[1])
      gsp_vic = GSP(vic, period, row[2])
      gsp_qld = GSP(qld, period, row[3])
      gsp_sa = GSP(sa, period, row[4])
      gsp_wa = GSP(wa, period, row[5])
      gsp_nt = GSP(nt, period, row[7])
      gsp_act = GSP(act, period, row[8])
      db.session.add(gdp)
      db.session.add(gsp_nsw)
      db.session.add(gsp_vic)
      db.session.add(gsp_tas)
      db.session.add(gsp_qld)
      db.session.add(gsp_act)
      db.session.add(gsp_nt)
      db.session.add(gsp_sa)
      db.session.add(gsp_wa)
      db.session.commit()
    ln += 1