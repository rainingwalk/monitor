#!/usr/bin/env python
#coding=utf-8
import rrdtool
 
def dItem01(data):
    pngname = str(data['pname'])
    start = data['stime']
    graphname = str(data['gname'] + "(" + data['host'] + ")" + "(" + data['flag'] + ")")
    DEF = str(r"DEF:a="+data['rrdpath']+r':'+data['pitem'][0]+r":AVERAGE")
    if data['cols'] or data['itypes']:
        if not data['cols']:
            dtype = str(data['itypes'][0][0]+r":a#EAAF00FF:"+data['pitem'][0][1])
        elif not data['itypes']:
            dtype = str(r"AREA:a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
        else:
            dtype = str(data['itypes'][0][0]+r":a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
    else:
        dtype = str(r"AREA:a#EAAF00FF:"+data['pitem'][0])
    unit = str(data['unit'])
    if not unit:
        unit = ' '
    max = 'GPRINT:a:MAX:Max\:%.2lf %s'
    min = 'GPRINT:a:MIN:Min\:%.2lf %s'
    avg = 'GPRINT:a:AVERAGE:Avg\:%.2lf %s'
    now = 'GPRINT:a:LAST:Now\:%.2lf %s'
    rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start,
                '-t', graphname, '-v', unit, DEF, 'COMMENT: \\n', dtype, now, avg, min, max, 'COMMENT: \\n')
###################################################################################################################
def dItem02(data):
    pngname = str(data['pname'])
    start = data['stime']
    graphname = str(data['gname']  + "(" + data['host'] + ")" + "(" + data['flag'] + ")")
    DEFa = str(r"DEF:a="+data['rrdpath']+r':'+data['pitem'][0]+r":AVERAGE")
    DEFb = str(r"DEF:b="+data['rrdpath']+r':'+data['pitem'][1]+r":AVERAGE")
    unit = str(data['unit'])
    if not unit:
        unit = ' '
    if data['cols'] or data['itypes']:
        if not data['cols']:
            dtypea = str(data['itypes'][0][0]+r":a#00CF00FF:"+data['pitem'][0][1])
            dtypeb = str(data['itypes'][0][1]+r":b#002A97FF:"+data['pitem'][1][1])
        elif not data['itypes']:
            dtypea = str(r"AREA:a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
            dtypeb = str(r"LINE2:b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
        else:
            dtypea = str(data['itypes'][0][0]+r":a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
            dtypeb = str(data['itypes'][0][1]+r":b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
    else:
        dtypea = str(r"AREA:a#00CF00FF:"+data['pitem'][0])
        dtypeb = str(r"LINE1:b#FF0000:"+data['pitem'][1])
    maxa = 'GPRINT:a:MAX:Max\:%.2lf %s'
    mina = 'GPRINT:a:MIN:Min\:%.2lf %s'
    avga = 'GPRINT:a:AVERAGE:Avg\:%.2lf %s'
    nowa = 'GPRINT:a:LAST:Now\:%.2lf %s'
    maxb = 'GPRINT:b:MAX:Max\:%.2lf %s'
    minb = 'GPRINT:b:MIN:Min\:%.2lf %s'
    avgb = 'GPRINT:b:AVERAGE:Avg\:%.2lf %s'
    nowb = 'GPRINT:b:LAST:Now\:%.2lf %s'
    rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start,
                '-t', graphname, '-v', unit, DEFa, DEFb, 'COMMENT: \\n', dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n',
                dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n')
###################################################################################################################
def dItem03(data):
    pngname = str(data['pname'])
    start = data['stime']
    graphname = str(data['gname']  + "(" + data['host'] + ")" + "(" + data['flag'] + ")")
    DEFa = str(r"DEF:a="+data['rrdpath']+r':'+data['pitem'][0]+r":AVERAGE")
    DEFb = str(r"DEF:b="+data['rrdpath']+r':'+data['pitem'][1]+r":AVERAGE")
    DEFc = str(r"DEF:c="+data['rrdpath']+r':'+data['pitem'][2]+r":AVERAGE")
    unit = str(data['unit'])
    if not unit:
        unit = ' '
    if data['cols'] or data['itypes']:
        if not data['cols']:
            dtypea = str(data['itypes'][0][0]+r":a#00CF00FF:"+data['pitem'][0][1])
            dtypeb = str(data['itypes'][0][1]+r":b#002A97FF:"+data['pitem'][1][1])
        elif not data['itypes']:
            dtypea = str(r"AREA:a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
            dtypeb = str(r"LINE2:b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
        else:
            dtypea = str(data['itypes'][0][0]+r":a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
            dtypeb = str(data['itypes'][0][1]+r":b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
    else:
        dtypea = str(r"AREA:a#F0E68C:"+data['pitem'][0])
        dtypeb = str(r"LINE1:b#DC143C:"+data['pitem'][1])
        dtypec = str(r"LINE1:c#1E90FF:"+data['pitem'][2])
    maxa = 'GPRINT:a:MAX:Max\:%.2lf %s'
    mina = 'GPRINT:a:MIN:Min\:%.2lf %s'
    avga = 'GPRINT:a:AVERAGE:Avg\:%.2lf %s'
    nowa = 'GPRINT:a:LAST:Now\:%.2lf %s'
    maxb = 'GPRINT:b:MAX:Max\:%.2lf %s'
    minb = 'GPRINT:b:MIN:Min\:%.2lf %s'
    avgb = 'GPRINT:b:AVERAGE:Avg\:%.2lf %s'
    nowb = 'GPRINT:b:LAST:Now\:%.2lf %s'
    maxc = 'GPRINT:c:MAX:Max\:%.2lf %s'
    minc = 'GPRINT:c:MIN:Min\:%.2lf %s'
    avgc = 'GPRINT:c:AVERAGE:Avg\:%.2lf %s'
    nowc = 'GPRINT:c:LAST:Now\:%.2lf %s'
    rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start,
                '-t', graphname, '-v', unit, DEFa, DEFb, DEFc, 'COMMENT: \\n', dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n',
                dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n',
                dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n')
###################################################################################################################
def dItem04(data):
    pngname = str(data['pname'])
    start = data['stime']
    graphname = str(data['gname']  + "(" + data['host'] + ")" + "(" + data['flag'] + ")")
    DEFa = str(r"DEF:a="+data['rrdpath']+r':'+data['pitem'][0]+r":AVERAGE")
    DEFb = str(r"DEF:b="+data['rrdpath']+r':'+data['pitem'][1]+r":AVERAGE")
    DEFc = str(r"DEF:c="+data['rrdpath']+r':'+data['pitem'][2]+r":AVERAGE")
    DEFd = str(r"DEF:d="+data['rrdpath']+r':'+data['pitem'][3]+r":AVERAGE")
    unit = str(data['unit'])
    if not unit:
        unit = ' '
    if data['cols'] or data['itypes']:
        if not data['cols']:
            dtypea = str(data['itypes'][0][0]+r":a#00CF00FF:"+data['pitem'][0][1])
            dtypeb = str(data['itypes'][0][1]+r":b#002A97FF:"+data['pitem'][1][1])
        elif not data['itypes']:
            dtypea = str(r"AREA:a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
            dtypeb = str(r"LINE2:b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
        else:
            dtypea = str(data['itypes'][0][0]+r":a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
            dtypeb = str(data['itypes'][0][1]+r":b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
    else:
        dtypea = str(r"LINE1:a#008000:"+data['pitem'][0])
        dtypeb = str(r"LINE1:b#FF0000:"+data['pitem'][1])
        dtypec = str(r"LINE1:c#FFD700:"+data['pitem'][2])
        dtyped = str(r"LINE1:d#4169E1:"+data['pitem'][3])
    maxa = 'GPRINT:a:MAX:Max\:%.2lf %s'
    mina = 'GPRINT:a:MIN:Min\:%.2lf %s'
    avga = 'GPRINT:a:AVERAGE:Avg\:%.2lf %s'
    nowa = 'GPRINT:a:LAST:Now\:%.2lf %s'
    maxb = 'GPRINT:b:MAX:Max\:%.2lf %s'
    minb = 'GPRINT:b:MIN:Min\:%.2lf %s'
    avgb = 'GPRINT:b:AVERAGE:Avg\:%.2lf %s'
    nowb = 'GPRINT:b:LAST:Now\:%.2lf %s'
    maxc = 'GPRINT:c:MAX:Max\:%.2lf %s'
    minc = 'GPRINT:c:MIN:Min\:%.2lf %s'
    avgc = 'GPRINT:c:AVERAGE:Avg\:%.2lf %s'
    nowc = 'GPRINT:c:LAST:Now\:%.2lf %s'
    maxd = 'GPRINT:d:MAX:Max\:%.2lf %s'
    mind = 'GPRINT:d:MIN:Min\:%.2lf %s'
    avgd = 'GPRINT:d:AVERAGE:Avg\:%.2lf %s'
    nowd = 'GPRINT:d:LAST:Now\:%.2lf %s'
    rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start,
                '-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, 'COMMENT: \\n', dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n',
                dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n',
                dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
                dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n')
###################################################################################################################
def dItem05(data):
    pngname = str(data['pname'])
    start = data['stime']
    graphname = str(data['gname']  + "(" + data['host'] + ")" + "(" + data['flag'] + ")")
    DEFa = str(r"DEF:a="+data['rrdpath']+r':'+data['pitem'][0]+r":AVERAGE")
    DEFb = str(r"DEF:b="+data['rrdpath']+r':'+data['pitem'][1]+r":AVERAGE")
    DEFc = str(r"DEF:c="+data['rrdpath']+r':'+data['pitem'][2]+r":AVERAGE")
    DEFd = str(r"DEF:d="+data['rrdpath']+r':'+data['pitem'][3]+r":AVERAGE")
    DEFe = str(r"DEF:e="+data['rrdpath']+r':'+data['pitem'][4]+r":AVERAGE")
    unit = str(data['unit'])
    if not unit:
        unit = ' '
    if data['cols'] or data['itypes']:
        if not data['cols']:
            dtypea = str(data['itypes'][0][0]+r":a#00CF00FF:"+data['pitem'][0][1])
            dtypeb = str(data['itypes'][0][1]+r":b#002A97FF:"+data['pitem'][1][1])
        elif not data['itypes']:
            dtypea = str(r"AREA:a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
            dtypeb = str(r"LINE2:b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
        else:
            dtypea = str(data['itypes'][0][0]+r":a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
            dtypeb = str(data['itypes'][0][1]+r":b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
    else:
        dtypea = str(r"LINE1:a#FF0000:"+data['pitem'][0])
        dtypeb = str(r"LINE1:b#DAA520:"+data['pitem'][1])
        dtypec = str(r"LINE1:c#228B22:"+data['pitem'][2])
        dtyped = str(r"LINE1:d#87CEFA:"+data['pitem'][3])
        dtypee = str(r"LINE1:e#9ACD32:"+data['pitem'][4])
    maxa = 'GPRINT:a:MAX:Max\:%.2lf %s'
    mina = 'GPRINT:a:MIN:Min\:%.2lf %s'
    avga = 'GPRINT:a:AVERAGE:Avg\:%.2lf %s'
    nowa = 'GPRINT:a:LAST:Now\:%.2lf %s'
    maxb = 'GPRINT:b:MAX:Max\:%.2lf %s'
    minb = 'GPRINT:b:MIN:Min\:%.2lf %s'
    avgb = 'GPRINT:b:AVERAGE:Avg\:%.2lf %s'
    nowb = 'GPRINT:b:LAST:Now\:%.2lf %s'
    maxc = 'GPRINT:c:MAX:Max\:%.2lf %s'
    minc = 'GPRINT:c:MIN:Min\:%.2lf %s'
    avgc = 'GPRINT:c:AVERAGE:Avg\:%.2lf %s'
    nowc = 'GPRINT:c:LAST:Now\:%.2lf %s'
    maxd = 'GPRINT:d:MAX:Max\:%.2lf %s'
    mind = 'GPRINT:d:MIN:Min\:%.2lf %s'
    avgd = 'GPRINT:d:AVERAGE:Avg\:%.2lf %s'
    nowd = 'GPRINT:d:LAST:Now\:%.2lf %s'
    maxe = 'GPRINT:e:MAX:Max\:%.2lf %s'
    mine = 'GPRINT:e:MIN:Min\:%.2lf %s'
    avge = 'GPRINT:e:AVERAGE:Avg\:%.2lf %s'
    nowe = 'GPRINT:e:LAST:Now\:%.2lf %s'
    rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start,
                '-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, DEFe, 'COMMENT: \\n', dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n',
                dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n',
                dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
                dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n',
				dtypee, nowe, avge, mine, maxe, 'COMMENT: \\n')
##################################################################################################################
def dItem06(data):
    pngname = str(data['pname'])
    start = data['stime']
    graphname = str(data['gname']  + "(" + data['host'] + ")" + "(" + data['flag'] + ")")
    DEFa = str(r"DEF:a="+data['rrdpath']+r':'+data['pitem'][0]+r":AVERAGE")
    DEFb = str(r"DEF:b="+data['rrdpath']+r':'+data['pitem'][1]+r":AVERAGE")
    DEFc = str(r"DEF:c="+data['rrdpath']+r':'+data['pitem'][2]+r":AVERAGE")
    DEFd = str(r"DEF:d="+data['rrdpath']+r':'+data['pitem'][3]+r":AVERAGE")
    DEFe = str(r"DEF:e="+data['rrdpath']+r':'+data['pitem'][4]+r":AVERAGE")
    DEFf = str(r"DEF:f="+data['rrdpath']+r':'+data['pitem'][5]+r":AVERAGE")
    unit = str(data['unit'])
    if not unit:
        unit = ' '
    if data['cols'] or data['itypes']:
        if not data['cols']:
            dtypea = str(data['itypes'][0][0]+r":a#00CF00FF:"+data['pitem'][0][1])
            dtypeb = str(data['itypes'][0][1]+r":b#002A97FF:"+data['pitem'][1][1])
        elif not data['itypes']:
            dtypea = str(r"AREA:a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
            dtypeb = str(r"LINE2:b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
        else:
            dtypea = str(data['itypes'][0][0]+r":a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
            dtypeb = str(data['itypes'][0][1]+r":b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
    else:
        dtypea = str(r"LINE1:a#DAA520:"+data['pitem'][0])
        dtypeb = str(r"LINE1:b#DC143C:"+data['pitem'][1])
        dtypec = str(r"LINE1:c#ADFF2F:"+data['pitem'][2])
        dtyped = str(r"LINE1:d#228B22:"+data['pitem'][3])
        dtypee = str(r"LINE1:e#0000FF:"+data['pitem'][4])
        dtypef = str(r"LINE1:e#7CFC00:"+data['pitem'][5])
    maxa = 'GPRINT:a:MAX:Max\:%.2lf %s'
    mina = 'GPRINT:a:MIN:Min\:%.2lf %s'
    avga = 'GPRINT:a:AVERAGE:Avg\:%.2lf %s'
    nowa = 'GPRINT:a:LAST:Now\:%.2lf %s'
    maxb = 'GPRINT:b:MAX:Max\:%.2lf %s'
    minb = 'GPRINT:b:MIN:Min\:%.2lf %s'
    avgb = 'GPRINT:b:AVERAGE:Avg\:%.2lf %s'
    nowb = 'GPRINT:b:LAST:Now\:%.2lf %s'
    maxc = 'GPRINT:c:MAX:Max\:%.2lf %s'
    minc = 'GPRINT:c:MIN:Min\:%.2lf %s'
    avgc = 'GPRINT:c:AVERAGE:Avg\:%.2lf %s'
    nowc = 'GPRINT:c:LAST:Now\:%.2lf %s'
    maxd = 'GPRINT:d:MAX:Max\:%.2lf %s'
    mind = 'GPRINT:d:MIN:Min\:%.2lf %s'
    avgd = 'GPRINT:d:AVERAGE:Avg\:%.2lf %s'
    nowd = 'GPRINT:d:LAST:Now\:%.2lf %s'
    maxe = 'GPRINT:e:MAX:Max\:%.2lf %s'
    mine = 'GPRINT:e:MIN:Min\:%.2lf %s'
    avge = 'GPRINT:e:AVERAGE:Avg\:%.2lf %s'
    nowe = 'GPRINT:e:LAST:Now\:%.2lf %s'
    maxf = 'GPRINT:f:MAX:Max\:%.2lf %s'
    minf = 'GPRINT:f:MIN:Min\:%.2lf %s'
    avgf = 'GPRINT:f:AVERAGE:Avg\:%.2lf %s'
    nowf = 'GPRINT:f:LAST:Now\:%.2lf %s'
    rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start,
                '-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, DEFe, DEFf, 'COMMENT: \\n', dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n',
                dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n',
                dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
                dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n',
				dtypee, nowe, avge, mine, maxe, 'COMMENT: \\n',
				dtypef, nowf, avgf, minf, maxf, 'COMMENT: \\n')
##################################################################################################################
def dItem07(data):
    pngname = str(data['pname'])
    start = data['stime']
    graphname = str(data['gname']  + "(" + data['host'] + ")" + "(" + data['flag'] + ")")
    DEFa = str(r"DEF:a="+data['rrdpath']+r':'+data['pitem'][0]+r":AVERAGE")
    DEFb = str(r"DEF:b="+data['rrdpath']+r':'+data['pitem'][1]+r":AVERAGE")
    DEFc = str(r"DEF:c="+data['rrdpath']+r':'+data['pitem'][2]+r":AVERAGE")
    DEFd = str(r"DEF:d="+data['rrdpath']+r':'+data['pitem'][3]+r":AVERAGE")
    DEFe = str(r"DEF:e="+data['rrdpath']+r':'+data['pitem'][4]+r":AVERAGE")
    DEFf = str(r"DEF:f="+data['rrdpath']+r':'+data['pitem'][5]+r":AVERAGE")
    DEFg = str(r"DEF:g="+data['rrdpath']+r':'+data['pitem'][6]+r":AVERAGE")
    unit = str(data['unit'])
    if not unit:
        unit = ' '
    if data['cols'] or data['itypes']:
        if not data['cols']:
            dtypea = str(data['itypes'][0][0]+r":a#00CF00FF:"+data['pitem'][0][1])
            dtypeb = str(data['itypes'][0][1]+r":b#002A97FF:"+data['pitem'][1][1])
        elif not data['itypes']:
            dtypea = str(r"AREA:a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
            dtypeb = str(r"LINE2:b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
        else:
            dtypea = str(data['itypes'][0][0]+r":a"+data['cols'][0][0]+r":"+data['pitem'][0][1])
            dtypeb = str(data['itypes'][0][1]+r":b"+data['cols'][0][1]+r":"+data['pitem'][1][1])
    else:
        dtypea = str(r"LINE1:a#800080:"+data['pitem'][0])
        dtypeb = str(r"LINE1:b#7CFC00:"+data['pitem'][1])
        dtypec = str(r"LINE1:c#7B68EE:"+data['pitem'][2])
        dtyped = str(r"LINE1:d#0000FF:"+data['pitem'][3])
        dtypee = str(r"LINE1:e#00BFFF:"+data['pitem'][4])
        dtypef = str(r"LINE1:e#228B22:"+data['pitem'][5])
        dtypeg = str(r"LINE1:e#FF1493:"+data['pitem'][6])
    maxa = 'GPRINT:a:MAX:Max\:%.2lf %s'
    mina = 'GPRINT:a:MIN:Min\:%.2lf %s'
    avga = 'GPRINT:a:AVERAGE:Avg\:%.2lf %s'
    nowa = 'GPRINT:a:LAST:Now\:%.2lf %s'
    maxb = 'GPRINT:b:MAX:Max\:%.2lf %s'
    minb = 'GPRINT:b:MIN:Min\:%.2lf %s'
    avgb = 'GPRINT:b:AVERAGE:Avg\:%.2lf %s'
    nowb = 'GPRINT:b:LAST:Now\:%.2lf %s'
    maxc = 'GPRINT:c:MAX:Max\:%.2lf %s'
    minc = 'GPRINT:c:MIN:Min\:%.2lf %s'
    avgc = 'GPRINT:c:AVERAGE:Avg\:%.2lf %s'
    nowc = 'GPRINT:c:LAST:Now\:%.2lf %s'
    maxd = 'GPRINT:d:MAX:Max\:%.2lf %s'
    mind = 'GPRINT:d:MIN:Min\:%.2lf %s'
    avgd = 'GPRINT:d:AVERAGE:Avg\:%.2lf %s'
    nowd = 'GPRINT:d:LAST:Now\:%.2lf %s'
    maxe = 'GPRINT:e:MAX:Max\:%.2lf %s'
    mine = 'GPRINT:e:MIN:Min\:%.2lf %s'
    avge = 'GPRINT:e:AVERAGE:Avg\:%.2lf %s'
    nowe = 'GPRINT:e:LAST:Now\:%.2lf %s'
    maxf = 'GPRINT:f:MAX:Max\:%.2lf %s'
    minf = 'GPRINT:f:MIN:Min\:%.2lf %s'
    avgf = 'GPRINT:f:AVERAGE:Avg\:%.2lf %s'
    nowf = 'GPRINT:f:LAST:Now\:%.2lf %s'
    maxg = 'GPRINT:g:MAX:Max\:%.2lf %s'
    ming = 'GPRINT:g:MIN:Min\:%.2lf %s'
    avgg = 'GPRINT:g:AVERAGE:Avg\:%.2lf %s'
    nowg = 'GPRINT:g:LAST:Now\:%.2lf %s'
    rrdtool.graph(pngname, '-w', '600', '-h', '144', '-l', '0', '-s', start,
                '-t', graphname, '-v', unit, DEFa, DEFb, DEFc, DEFd, DEFe, DEFf, DEFg, 'COMMENT: \\n', dtypea, nowa, avga, mina, maxa, 'COMMENT: \\n',
                dtypeb, nowb, avgb, minb, maxb, 'COMMENT: \\n',
                dtypec, nowc, avgc, minc, maxc, 'COMMENT: \\n',
                dtyped, nowd, avgd, mind, maxd, 'COMMENT: \\n',
				dtypee, nowe, avge, mine, maxe, 'COMMENT: \\n',
				dtypef, nowf, avgf, minf, maxf, 'COMMENT: \\n',
				dtypeg, nowg, avgg, ming, maxg, 'COMMENT: \\n')
