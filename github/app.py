# -*- coding: utf-8 -*-
#!/usr/bin/python2.7
import os, re, time
from flask import Flask, render_template, session, redirect, url_for, request, g, flash, jsonify, json
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.script import Manager, Shell
# config file  
import config
from models import db, app, DrawTree, DrawGraphs, DrawDef
from sqlalchemy import distinct
import graphsub
import threading
from datetime import datetime
import rdsapi
import searchRDSinstance
import requests
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.cache import Cache

cache = Cache()
app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
cache.init_app(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'max-age=30'
    return response

@app.route("/check", methods=["GET","POST"])
def check():
##################ESC DB Insert########################
    r = request.args.get('check')
    if r == 'ecs':
        bj_command_state = "/testproject/packages/nagios-api-1.2.2/nagios-cli --host='10.170.195.128' --port='3721' --raw state"
        hz_command_state = "/testproject/packages/nagios-api-1.2.2/nagios-cli --host='120.26.80.50' --port='3721' --raw state"
        ####update table: draw_graphs
        DSS = {'est_tcp':['est_tcp','Count'],
              'total_processes':['total_processes','Count'],
              'memory':['memory_free,memory_used','Byte'],
              'disk_free':['root,root_dev_shm,root_data','Byte'],
              'load':['load_1min,load_5min,load_15min',''],
              'ping':['ping_rta','ms'],
              'network_eth0':['network_rx,network_tx','bps'],
              'mem_disk_ping_percent':['memory_used_percent,root_used_percent,data_used_percent,ping_percent','Percent'],
              'xvda_io':['read_iops,write_iops,iowait','ms'],
              'xvdb_io':['read_iops,write_iops,iowait','ms']}
        for DS in DSS:
            dsname = DS
            itemname = DSS[DS][:-1][0]
            units = DSS[DS][-1:][0]
            ds = db.session.query(DrawGraphs).filter_by(itemname=itemname).all()
            if not ds:
                ds_info = DrawGraphs(dsname=dsname, itemname=itemname, units=units)
                db.session.add(ds_info)
        state_all = []
        bj_state = os.popen(bj_command_state).readlines()
        hz_state = os.popen(hz_command_state).readlines()
        state_all = bj_state + hz_state
        for state in state_all:
            resp_state = json.loads(state.decode('utf-8'))
            for host in resp_state:
                sgms = host.split('-')
                if len(sgms) == 4:
                    region = sgms[2]
                    classname_tmp = "".join(re.findall(r'(\D+)', sgms[3]))
                if 'hk' in host:
                    region = 'beijing'
                    classname_tmp = 'hk'
                if 'jp' in host:
                    region = 'beijing'
                    classname_tmp = 'jp'
                if 'hz' in host:
                    region = 'hangzhou'
                if classname_tmp:
                    classname = classname_tmp
                    hostname = host
                    content = resp_state[host]
                    graphname = ""
                    draw = '1'
                    type = 'ali_ecs'
                    for key in content['services'].iteritems():
                        if 'PING' in key:
                            graphname = graphname + 'ping,'
                        if 'Memory usage' in key:
                            graphname = graphname + 'memory,'
                        if 'Network eth0' in key:
                            graphname = graphname + 'network_eth0,'
                        if 'Load' in key:
                            graphname = graphname + 'load,'
                        if 'Root Partition' in key:
                            graphname = graphname + 'disk_free,mem_disk_ping_percent,'
                        if 'Total Processes' in key:
                            graphname = graphname + 'total_processes,'
                        if 'est tcp' in key:
                            graphname = graphname + 'est_tcp,'
                        if 'xvda io' in key:
                            graphname = graphname + 'xvda_io,'
                        if 'xvdb io' in key:
                            graphname = graphname +'xvdb_io,'
                    graphname = graphname[:-1]
                    server = db.session.query(DrawTree).filter_by(hostname=hostname).all()
                    if not server:
                        info = DrawTree(region=region, classname=classname, hostname=hostname, graphname=graphname, draw=draw, type=type) 
                        db.session.add(info)
        db.session.commit()
        return redirect(url_for('index'))
    ########################################################
    if r == 'rds':
        dir = '/data/apps/rrd_db/rds'
        monitor_items = ['MySQL_COMDML',
                               'MySQL_CpuUsage',
                               'MySQL_InnoDBBufferRatio',
                               'MySQL_InnoDBDataReadWriten',
                               'MySQL_InnoDBLogWrites',
                               'MySQL_IOPS',
                               'MySQL_NetworkTraffic',
                               'MySQL_QPSTPS',
                               'MySQL_RowDML',
                               'MySQL_Sessions',
                               'MySQL_SpaceUsage',
                               'MySQL_TempDiskTableCreates']
        graphname = ','.join(monitor_items)
        monitor_items_tmp = monitor_items[:]
        PERIODTIME = 6
        draw = 1
        type = 'ali_rds'
        for region in ['beijing', 'hangzhou']:
            searchRDSinstance.get_instance(region)
            vlist = open(BASE_DIR+'/cn-' + region + '.id', 'r')
            vms = vlist.readlines()
            for vm in vms:
                vm_ali = "".join(vm).split(',')[0]
                vm_us = "".join(vm).split(',')[1].strip('\n')
                DIR = os.path.join(dir, region)
                DIMENSIONS = "{instanceId:'" + vm_ali + "'}"
                rrddir = os.path.join(DIR, vm_us.strip('\n'))
                #mlist = open(BASE_DIR+'/rds.monitor.items', 'r')
                for monitor_item in monitor_items:
                    os.environ['TZ'] = 'UTC'
                    ds = "N:"
                    #fields = ms.split("\t")
                    METRIC_NAME = monitor_item
                    ####################Update table 'draw_graphs'############
                    if monitor_items_tmp:
                        monitor_items_tmp.remove(monitor_item)
                        dsname_q = db.session.query(DrawGraphs).filter_by(dsname=monitor_item).all()
                        if not dsname_q:
                            #PERIOD = fields[1].strip('\n') + 'm'
                            #PERIODTIME = int(fields[1]) + 1
                            rrdname = str(os.path.join(rrddir, METRIC_NAME + '.rrd'))
                            MaxAllowRetryNumber = 5
                            for tries in range(MaxAllowRetryNumber + 1):
                                url = str(rdsapi.query_data(METRIC_NAME, DIMENSIONS, PERIODTIME))
                                apidata = requests.get(url)
                                contents = json.loads(apidata.content)
                                #print ms, '---',contents
                                if 'Datapoints' in contents and contents['Datapoints']['Datapoint']:
                                    itemname = ""
                                    for content in contents['Datapoints']['Datapoint']:
                                        data = json.loads(content)
                                        ds_len = len(data['type'])
                                        if ds_len > 19:
                                            data['type'] = data['type'][ds_len-19:]
                                        itemname = itemname + data['type'] + ','
                                    ds_info = DrawGraphs(dsname=METRIC_NAME, itemname=itemname[:-1], units=data['unit'])
                                    #print '--',rrdname,'--',itemname[:-1]
                                    db.session.add(ds_info)
                                    #return json.dumps(dsname)
                                    break
                                else:
                                    #print "---Retry %s for %s ..." % (METRIC_NAME, tries)
                                    continue
                                    if tries == MaxAllowRetryNumber:
                                        print "!!! Failed To Get Data for %s !!!" % (METRIC_NAME)
                            db.session.commit()
                    ####################Update table 'drawtree'#################'
                    server = db.session.query(DrawTree).filter_by(hostname=vm_us).all()
                    if not server:
                        if 'kefu' in vm_us: classname = 'kefu'
                        elif 'ejabberd' in vm_us: classname = 'ejabberd'
                        elif 'chuchu' in vm_us: classname = 'kefu'
                        else: classname = 'others'
                        info = DrawTree(region=region, classname=classname, hostname=vm_us, graphname=graphname, draw=draw, type=type)
                        db.session.add(info)
                    db.session.commit()
            vlist.close()            #print vm_us,'--',classname,'--',region,'---',monitor_item
    return redirect(url_for('index'))
#       #########################
@app.route("/index", methods=["GET","POST"])
def index():
    results = {}
    type_q = db.session.query(distinct(DrawTree.type)).all()
    for type in type_q:
        types = {}
        region_q = db.session.query(distinct(DrawTree.region)).filter_by(type=type[0]).all()
        for region in region_q:
            classname_q = db.session.query(distinct(DrawTree.classname)).filter_by(type=type[0]).filter_by(region=region[0]).all()
            classes = {}
            for classname in classname_q:
                host_list = []
                host_q = db.session.query(DrawTree.hostname).filter_by(type=type[0]).filter_by(region=region[0]).filter_by(classname=classname[0]).order_by(DrawTree.hostname).all()
                for host in host_q:
                    host_list.append(host[0])
                classes[classname[0]] = host_list
            types[region[0]] = classes
        results[type[0]] = types
    return render_template('drawindex.html', results = results)

@app.route("/draw", methods=["GET","POST"])
def draw():
    os.environ['TZ'] = 'Asia/Shanghai'
    type = request.args.get('type')
    region = request.args.get('region')
    hostname = request.args.get('host')
    if type == 'ali_ecs': 
        dir = r"/data/apps/rrd_db"
        rpath = os.path.join(dir, 'ali_'+region, hostname)
    if type == 'ali_rds': 
        dir = r"/data/apps/rrd_db/rds"
        rpath = os.path.join(dir, region, hostname)
    #pngdir = r"/data/apps/rrd_db/static/images/rrdpng"
    pngdir = r"static/images/rrdpng"
    strtime = str(int(time.time()- 86400))
    gdatas = []
    pngs = []
    graph_q = db.session.query(DrawTree.graphname).filter_by(type=type).filter_by(region=region).filter_by(hostname=hostname).all()
    for graph in graph_q:
        graphname = graph[0]
        ppath = os.path.join(pngdir, hostname)
        if not os.path.exists(ppath):
            os.makedirs(ppath)
        graphs = graphname.split(',')
        for dsname in graphs:
            item_q = db.session.query(DrawGraphs.itemname,DrawGraphs.units).filter_by(dsname=dsname).all()
            for item in item_q:
                dss = item[:-1][0]
                unit = item[-1:][0]
                ds = dss.split(',')
            rfile = os.path.join(rpath, dsname+'.rrd')
            pfile = 'images/rrdpng/'+hostname+'/'+dsname+'.png'
            pname = os.path.join(ppath, dsname+'.png')
            gdata = {'pname':pname, 'gname':dsname, 'rrdpath':rfile, 'pitem':ds, 'flag':'Daily', 'stime':strtime, 'host':hostname, 'cols':'', 'itypes':'','unit':unit}
            url_img = url_for('static', filename=pfile)
            pngs.append({'pngpath':url_img, 'drawal':type+'&'+region+'&'+hostname+'&'+dsname})
            print "----graphing ",rfile
            if len(gdata['pitem']) == 1: graphsub.dItem01(gdata)
            if len(gdata['pitem']) == 2: graphsub.dItem02(gdata)
            if len(gdata['pitem']) == 3: graphsub.dItem03(gdata)
            if len(gdata['pitem']) == 4: graphsub.dItem04(gdata)
            if len(gdata['pitem']) == 5: graphsub.dItem05(gdata)
            if len(gdata['pitem']) == 6: graphsub.dItem06(gdata)
            if len(gdata['pitem']) == 7: graphsub.dItem07(gdata)
        #graphsub.dmanage(gdata)
    return render_template('drawgraph.html', pngs=pngs)

@app.route("/draw/drawall/<drawal>", methods=["GET","POST"])
def drawall(drawal):
    os.environ['TZ'] = 'Asia/Shanghai'
    gdatas = []
    pngs = []
    dir_tmp = "/data/apps/rrd_db"
    pngdir = "images/rrdpng/cache"
    png_tmp = drawal.split('&')
    type = png_tmp[0]
    region = png_tmp[1]
    hostname = png_tmp[2]
    dsname = png_tmp[3]
    if type == 'ali_ecs':
        rpath = os.path.join(dir_tmp, 'ali_'+region, hostname, dsname+".rrd")
    if type == 'ali_rds':
        rpath = os.path.join(dir_tmp, 'rds', region, hostname, dsname+".rrd")
    ppath = os.path.join('static/'+pngdir, hostname)
    fdir = os.path.join(pngdir, hostname)
    if not os.path.exists(ppath):
        os.makedirs(ppath)
    png2d = os.path.join(ppath, dsname+"_2d.png")
    f2d = os.path.join(fdir, dsname+"_2d.png")
    url2d = url_for('static', filename=f2d)
    pngs.append(url2d)
    png1w = os.path.join(ppath, dsname+"_1w.png")
    f1w = os.path.join(fdir, dsname+"_1w.png")
    url1w = url_for('static', filename=f1w)
    pngs.append(url1w)
    png1m = os.path.join(ppath, dsname+"_1m.png")
    f1m = os.path.join(fdir, dsname+"_1m.png")
    url1m = url_for('static', filename=f1m)
    pngs.append(url1m)
    png1y = os.path.join(ppath, dsname+"_1y.png")
    f1y = os.path.join(fdir, dsname+"_1y.png")
    url1y = url_for('static', filename=f1y)
    pngs.append(url1y)
#    #######################################################
    item_q = db.session.query(DrawGraphs.itemname,DrawGraphs.units).filter_by(dsname=dsname).all()
    for item in item_q:
        dss = item[:-1][0].split(',')
        unit = item[-1:][0]
#    ###########################
    strtime = str(int(time.time()- 172800))
    gdata = {'pname':png2d, 'gname':dsname, 'rrdpath':rpath, 'pitem':dss, 'unit':unit,
            'cols':'', 'itypes':'', 'host':hostname, 'stime':strtime, 'flag':'2 Days'}
    gdatas.append(gdata)
#    ###########################
    strtime = str(int(time.time()- 604800))
    gdata = {'pname':png1w, 'gname':dsname, 'rrdpath':rpath, 'pitem':dss, 'unit':unit,
            'cols':'', 'itypes':'', 'host':hostname, 'stime':strtime, 'flag':'Weekly'}
    gdatas.append(gdata)
    ###########################
    strtime = str(int(time.time()- 2592000))
    gdata = {'pname':png1m, 'gname':dsname, 'rrdpath':rpath, 'pitem':dss, 'unit':unit,
            'cols':'', 'itypes':'', 'host':hostname, 'stime':strtime, 'flag':'Monthly'}
    gdatas.append(gdata)
    ###########################
    strtime = str(int(time.time()- 31536000))
    gdata = {'pname':png1y, 'gname':dsname, 'rrdpath':rpath, 'pitem':dss, 'unit':unit,
            'cols':'', 'itypes':'', 'host':hostname, 'stime':strtime, 'flag':'Yearly'}
    gdatas.append(gdata)
    ##########################
    #print gdatas,'---',pngs
    for gdata in gdatas:
        #if os.path.isfile(gdata['pname']): os.remove(gdata['pname'])
        print "----graphing ",gdata['pname']
        if len(gdata['pitem']) == 1: graphsub.dItem01(gdata)
        if len(gdata['pitem']) == 2: graphsub.dItem02(gdata)
        if len(gdata['pitem']) == 3: graphsub.dItem03(gdata)
        if len(gdata['pitem']) == 4: graphsub.dItem04(gdata)
        if len(gdata['pitem']) == 5: graphsub.dItem05(gdata)
        if len(gdata['pitem']) == 6: graphsub.dItem06(gdata)
        if len(gdata['pitem']) == 7: graphsub.dItem07(gdata)
    return render_template('drawall.html', pngs=pngs)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

