from flask import Flask  
from flask.ext.sqlalchemy import SQLAlchemy  
from sqlalchemy import Table, Column, Integer, String, Date, Float
import config 

# DB class  
app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] =  config.DB_URI  
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app) 

# Create your models here.
#################################################
class DrawTree(db.Model):
    __tablename__ = 'drawtree'

    drawtreeid = db.Column('drawtreeid', Integer, primary_key=True)
    region = db.Column('region', String(24))
    classname = db.Column('classname', String(64))
    hostname = db.Column('hostname', String(64), unique=True)
    graphname = db.Column('graphname', String(128))
    draw = db.Column('draw', String(2))
    type = db.Column('type', String(32))

    def __init__(self, region=None, classname=None, hostname=None,graphname=None, draw=None, type=None):  
        self.region = region
        self.classname = classname 
        self.hostname = hostname
        self.graphname = graphname
        self.draw = draw
        self.type = type
   
    def __repr__(self):  
        return '<region %s, classname %s, hostname %s, graphname %s>' % (self.region, self.classname, self.hostname, self.graphname)  
 
################################################
class DrawGraphs(db.Model):
    __tablename__ = 'draw_graphs'
    
    drawgraphsid = db.Column('drawgraphsid', Integer, primary_key=True)
    dsname = db.Column('dsname', String(24), unique=True)
    itemname = db.Column('itemname', String(128))
    units = db.Column('units', String(32))
    
    def __init__(self, dsname=None, itemname=None, units=None):
        self.dsname = dsname
        self.itemname = itemname
        self.units = units

    def __repr__(self):
        return '<dsname %s, itemname %s, units %s>' % (self.dsname, self.itemname, self.units)
#################################################
class DrawDef(db.Model):
    drawdefid = db.Column('drawdefid', Integer, primary_key=True)
    graphname = db.Column('graphname', String(128))
    cols = db.Column('cols', String(256))
    types = db.Column('types', String(256))

    def __init__(self, graphname=None, cols=None, types=None):
        self.graphname = graphname
        self.cols = cols
        self.types = types

    def __repr__(self):
        return '<graphname %s, cols %s, types %s>' % (self.graphname, self.cols, self.types)

if __name__ == '__main__':  
    #create table from up model  
    db.create_all()  
