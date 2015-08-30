import os
from flask import Flask, render_template, session, redirect, url_for, request, g, flash, jsonify, json
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import rrdtool
import time,os
#from graph import drawnetwork
app = Flask(__name__)

DB_CONNECT_STRING = 'mysql+mysqldb://root@localhost/nagios?charset=utf8'
engine = create_engine(DB_CONNECT_STRING, echo=True)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)


#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/serverinfo?charset=utf8'
#app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
#db = SQLAlchemy(app)


@app.route("/", methods=["GET"])
def index():
    return render_template("11.html")



@app.route("/groups", methods=["GET","POST"])
def projectlist():
    groups = session.execute('select alias from nagios_hostgroups;')
    return render_template("index.html", groups = groups)
    #return jsonify(groups)

@app.route("/groups/<host>")
def drawnetwork(host):
    rrd = os.path.join("/testproject/draw/draw/rrdb/%s.rrd" % host)
    png = os.path.join("/testproject/draw/draw/png/%s_network.png" % (host))
    #rrd = os.path.join(RRD,"%s.rrd" % host)
    #png = os.path.join(PNG, "%s_eth0.png" % server)
    data = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    title="network_eth0 flow for %s  (update:%s)" % (host, data)

    rrdtool.graph(png, "--start", "-1d","--vertical-label=Bytes/s","--x-grid","MINUTE:15:HOUR:1:HOUR:1:0:%H", "--width","650","--height","230", "-w", "700", "--title",title,
    "DEF:inoctets=%s:network_eth0_rx:AVERAGE" % rrd,
    "DEF:outoctets=%s:network_eth0_tx:AVERAGE" % rrd,
    "CDEF:total=inoctets,outoctets,+",
    "LINE2:total#FF8833:Total traffic",
    "AREA:inoctets#00FF00:In traffic",
    "LINE1:outoctets#0000FF:Out traffici       ",
    "HRULE:6144#FF0000:Alarm value",
    "CDEF:inbits=inoctets,8,*", 
    "CDEF:outbits=outoctets,8,*",
    "COMMENT:\\n",
    "GPRINT:inbits:AVERAGE:Avg In traffic\: %6.2lf %Sbps\\t",
    "GPRINT:inbits:MAX:Max In traffic\: %6.2lf %Sbps\\t", 
    "GPRINT:inbits:MIN:MIN In traffic\: %6.2lf %Sbps",
    "GPRINT:outbits:AVERAGE:Avg Out traffic\: %6.2lf %Sbps\\t",
    "GPRINT:outbits:MAX:Max Out traffic\: %6.2lf %Sbps\\t",
    "GPRINT:outbits:MIN:MIN Out traffic\: %6.2lf %Sbps")

    #services = ['est_tcp', 'total_processes', 'memory_usage', 'root_partition', 'load_5min', 'ping_package_loss','network_eth0']
    return render_template("index.html", png = png)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

