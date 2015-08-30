# -*- coding: utf-8 -*-
#!/usr/bin/python
import rrdtool
import time,os

#class Draw():
#    def __init__(self, host):
#        RRD = os.path.join("/testproject/draw/draw/rrdb/%s.rrd" % host)
#        PNG = os.path.join("/testproject/draw/draw/png/%s_network.png" % (host))
##BASE_DIR = os.path.dirname(os.path.abspath(__file__))
##BASE_DIR = "/testproject/draw/draw"
##RRD = os.path.join(BASE_DIR,'rrdb')
##PNG = os.path.join(BASE_DIR,'png')
#        data = time.strftime('%Y-%m-%d',time.localtime(time.time()))
#        title = "network for %s (update: %s)" % (host, data)

def drawnetwork(host):
    RRD = os.path.join("/testproject/draw/draw/rrdb/%s.rrd" % host)
    PNG = os.path.join("/testproject/draw/draw/png/%s_network.png" % (host))
    #rrd = os.path.join(RRD,"%s.rrd" % host)
    #png = os.path.join(PNG, "%s_eth0.png" % server)
    data = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    title="network_eth0 flow for %s  (update:%s)" % (host, data)

    rrdtool.graph(PNG, "--start", "-1d","--vertical-label=Bytes/s","--x-grid","MINUTE:15:HOUR:1:HOUR:1:0:%H", "--width","650","--height","230", "-w", "700", "--title",title,
    #"DEF:inoctets=Flow.rrd:eth0_in:AVERAGE",#指定网卡入流量数据源DS及CF
    "DEF:inoctets=%s:network_eth0_rx:AVERAGE" % RRD,#指定网卡出流量数据源DS及CF
    "DEF:outoctets=%s:network_eth0_tx:AVERAGE" % RRD,#指定网卡出流量数据源DS及CF
    #"DEF:outoctets=Flow.rrd:eth0_out:AVERAGE",#指定网卡出流量数据源DS及CF
    "CDEF:total=inoctets,outoctets,+",#通过CDEF合并网卡出入流量，得出总流量total
    "LINE2:total#FF8833:Total traffic",#以线条方式绘制总流量
    "AREA:inoctets#00FF00:In traffic",#以面积风湿绘制入流量
    "LINE1:outoctets#0000FF:Out traffic          ",#以线条方式绘制出流量
    "HRULE:6144#FF0000:Alarm value",#绘制水平线，作为警告线，阈值为6.1 K
    "CDEF:inbits=inoctets,8,*",#将入流量换算成bit，即*8，计算结果给inbits
    "CDEF:outbits=outoctets,8,*",#将出流量换算成bit，即*8，计算结果给outbits
    "COMMENT:\\n",#在网格下方输出一个换行符
    "GPRINT:inbits:AVERAGE:Avg In traffic\: %6.2lf %Sbps\\t",#绘制入流量平均值
    "GPRINT:inbits:MAX:Max In traffic\: %6.2lf %Sbps\\t",#绘制入流量最大值
    "GPRINT:inbits:MIN:MIN In traffic\: %6.2lf %Sbps",#绘制入流量最小值
    "GPRINT:outbits:AVERAGE:Avg Out traffic\: %6.2lf %Sbps\\t",#绘制出流量平均值
    "GPRINT:outbits:MAX:Max Out traffic\: %6.2lf %Sbps\\t",#绘制出流量最大值
    "GPRINT:outbits:MIN:MIN Out traffic\: %6.2lf %Sbps")#绘制出流量最小值 
