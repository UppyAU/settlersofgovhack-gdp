#!/usr/bin/env python
import json
from datetime import datetime
from datetime import date
from flask import Flask, request, session, url_for, redirect, abort, render_template, jsonify, flash
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user

from flask.ext.sqlalchemy import SQLAlchemy

# Define flask app
app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

# Data Model
class State(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(60), unique=True)
  short = db.Column(db.String(10), unique=True)

  def __init__(self, name, short):
    self.name = name
    self.short = short
    
  def __repr__(self):
    return '<State %r>' % self.name

class GDP(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  period = db.Column(db.Date, unique=True)
  gdp = db.Column(db.Integer)
  
  def __init__(self, period, gdp):
    self.period = period
    self.gdp = gdp
  
  def __repr__(self):
    return '<GDP %r-%r:%r>' % (self.period.year, self.period.month, self.gdp)

class GSP(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  state_id = db.Column(db.Integer, db.ForeignKey('state.id'))
  state = db.relationship('State', backref=db.backref('gsp', lazy='dynamic'))
  period = db.Column(db.Date)
  gsp = db.Column(db.Integer)

  def __init__(self, state, period, gsp):
    self.state = state
    self.period = period
    self.gsp = gsp
    
  def __repr__(self):
    return '<GSP %r:%r-%r:%r>' % (self.state.short, self.period.year, self.period.month, self.gsp)

class GDP2(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  period = db.Column(db.Date)
  gdp_aus = db.Column(db.Integer)
  gsp_nsw = db.Column(db.Integer)
  gsp_vic = db.Column(db.Integer)
  gsp_qld = db.Column(db.Integer)
  gsp_tas = db.Column(db.Integer)
  gsp_act = db.Column(db.Integer)
  gsp_sa = db.Column(db.Integer)
  gsp_nt = db.Column(db.Integer)
  gsp_wa = db.Column(db.Integer)
  
  def __init__(self, period, gdp, nsw, vic, qld, tas, act, sa, nt, wa):
    self.period = period
    self.gdp_aus = gdp
    self.gsp_nsw = nsw
    self.gsp_vic = vic
    self.gsp_qld = qld
    self.gsp_tas = tas
    self.gsp_act = act
    self.gsp_sa = sa
    self.gsp_nt = nt
    self.gsp_wa = wa
    
  def __repr__(self):
    return '<GSP2 object>'


# Flask Views

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/api/gdp/<int:year>/<int:month>')
def json_gdp(year, month):
  out = {}
  if year >= 1990 and year <= 2015:
    if month >=1 and month <= 12:
      p = date(day=1, month=month, year=year)
      gsp = GSP.query.filter_by(period=p).all()
      if len(gsp) > 0:
        for s in gsp:
          out[s.state.short] = s.gsp
      else:
        out['error'] = "FAIL: no data"
    else:
      out['error'] = "FAIL: Outside date range"
  else:
    out['error'] = "FAIL: Outside date range"
  return jsonify(**out)

@app.route('/api/gdp2')
def json_gdp2():
  o = {}
  out = []
  gsp = GDP2.query.order_by('period').all()
  if len(gsp) > 0:
    for s in gsp:
      rec = {}
      rec['period'] = s.period.strftime('%b-%Y')
      rec['gdp_aus'] = s.gdp_aus
      rec['gsp_nsw'] = s.gsp_nsw
      rec['gsp_vic'] = s.gsp_vic
      rec['gsp_qld'] = s.gsp_qld
      rec['gsp_tas'] = s.gsp_tas
      rec['gsp_act'] = s.gsp_act
      rec['gsp_sa'] = s.gsp_sa
      rec['gsp_nt'] = s.gsp_nt
      rec['gsp_wa'] = s.gsp_wa
      out.append(rec)
    o['gdp'] = out
  else:
    o['error'] = "FAIL: no data"
  return jsonify(**o)

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0')