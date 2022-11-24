# -*- coding: utf-8 -*-   
#python2
import socket
import Queue
import threading
import traceback
import time

from uwan_performance import *

lock = threading.Lock()
nodeNum = 0
shareQueue = Queue.Queue(maxsize=0)#构造一个FIFO队列，maxsize可以限制队列的大小。如果队列的大小达到了队列的上限，就会加锁，加入就会阻塞，直到队列的内容被消费掉。maxsize的值小于等于0，那么队列的尺寸就是无限制的

def waitNodePort(UISocket, addr):
    print 'line15'
    port = UISocket.recv(1024)
    if (port == 1024):
        print 'this is 1024'
        clientSocket.close()
        os._exit(0)
    print 'this is not 1024'
    time.sleep(2)

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#用到connect函数就是客户端，服务器端是相应用accept函数.
    clientSocket.connect(('127.0.0.1', int(port)))#开了几个节点这个trace客户端就开了几个
    wnp=clientSocket.getsockname()
    thisfilefd=clientSocket.fileno()
    duimianaddr=clientSocket.getpeername()
    print 'connect to ', port, ' successfully','dui mian de address : ',duimianaddr,'this fd is:', thisfilefd
    print 'here s port ', wnp, ' successfully'
    while True:
        print 'line23',port,wnp
        traceMsg = clientSocket.recv(1024)#会阻塞
        print 'line25',port,wnp,'traceMsg:' ,traceMsg
        if traceMsg:
            # print 'receive message ->', traceMsg
            shareQueue.put(traceMsg)
            print 'line31',port,wnp
        else:
            print 'line33',port,wnp
            clientSocket.close()#这个客户端从头连到尾
            break

def nodeNumIncrease():
    print 'line32'
    lock.acquire()#因为要操作全局变量，所以先锁住
    try:
        global nodeNum
        nodeNum += 1
    finally:
        lock.release()

def getNodeNum():
    print 'line41'
    lock.acquire()
    try:
        global nodeNum
        return nodeNum
    finally:
        lock.release()

def startService():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('127.0.0.1', 16888))
    serverSocket.listen(10)#10代表着最大等待的连接数量
    print 'start in port 16888, waiting for node message......'

    while True:
        UISocket, addr = serverSocket.accept()#其中UISocket是新的套接字对象，可以用来接收和发送数据（就是说用这个uisocket可以使用send和recv函数。add是连接客户端的地址.没收到前程序会一直阻塞在这里.这里的uisocket是testnode。py里面的客户端.这里从testnode。py里的客户端收到节点的端口号
        print("line57(1)")
        print(UISocket)
        print(addr)#testnode。py客户端地址
        print("line57(2)")
        nodeNumIncrease()
        t = threading.Thread(target=waitNodePort, args=(UISocket, addr))
        t.start()
        print 'line 57'
def put_log(uwan):
    print 'line 64'
    while 1:
        msg = shareQueue.get()#会阻塞
        msg_list = msg.splitlines()
        print 'line 69',(msg)
        print 'line 69.5',(msg_list)
        for msg in msg_list: 
            #print 'receive message ->', msg, 'number of node ->', getNodeNum()
            sendtotest(msg)
            log_dict = uwan.init_msg(msg)
            print 'line 69.6',(log_dict)
            if log_dict is not None:
                print 'line 69.7'
                uwan.loglist.append(uwan.init_msg(msg))
        
def sendtotest(msg):
    print 'line 69.8',msg
    title = ['time', 'layerID','protocolID', 
                 'packetID', 'length', 
                 'srcID', 'lastID', 'nextID', 'destID', 'helloSeq',
                 'mSrcID', 'mDestID', 'ackSeq',
                 'ptype', 'status']
    msglist = msg.split(':')
    if len(msglist) != 15:
        print "ERROR: length != 15"
        pass
    else:
        msg_dict = {title[i]: msglist[i] for i in range(len(title))}
        if msg_dict['status'] == 'threesendUp':
            print 'line 70 prepare sending to qt'
            t1 = threading.Thread(target=sendmsgtoqttype1, args=())
            t1.start()



def sendmsgtoqttype1():
    print 'line70.1'
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.connect(('127.0.0.1', 16777))
    print 'connect to 16777 successfully'
    str11 = 'test1'
    s1.send(str11)
    s1.close()




def performanceAnalysis():
    print 'line 80'
    t = threading.Thread(target=startService, args=())
    print 'line 82'
    t.start()#程序不会卡在这
    start_time = time.time()
    last_time = start_time
    print 'line 83'
    uwan = UWANPerformance() # 性能计算
    print 'line 85',uwan#<uwan_performance.UWANPerformance object at 0x7f9f4a680550>
    '''
      针对每个性能生成图
      Route: deli_rate_clean 净收包率
             delay 端到端时延
        throughput 网络吞吐量
      Mac:   delay 点到点时延
             throughput MAC层吞吐量
             total_deli_rate 总收包/总发包
    '''
    layer_index = ['MAC-deli_rate_without_broadcast', 'MAC-Throughput', 'MAC-Delay',
                   'Route-deli_rate_clean', 'Route-Throughput', 'Route-Delay']
    location_num = [231, 232, 233, 234, 235, 236]
    # 生成画布
    plt.style.use('seaborn-notebook')
    fig = plt.figure(figsize=(40, 30))
    fig.suptitle('HSM Stack Protocol Performance Display -- Running...')
    plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.3, hspace=0.25)
    plt.ion()
    display_list = []
    for i, item in enumerate(layer_index):
        layer = item.split('-')[0]
        index = item.split('-')[1]
        print 'line121',layer,index
#MAC deli_rate_without_broadcast
#MAC Throughput
#MAC Delay
#Route deli_rate_clean
#Route Throughput
#Route Delay
        performance_display = Display(layer, index)
        performance_display.generate(fig, location_num[i])
        display_list.append(performance_display)

    putlog_thread = threading.Thread(target=put_log, args=(uwan,))
    putlog_thread.start()
    while True:
        try:
            uwan.node_num = getNodeNum()
            print "uwan node_num: ", uwan.node_num
            if uwan.node_num < 2:
                print "running node is 1, pass"
                pass
            else:
                #print len(uwan.loglist)
                uwan.performance_detail()#有个输出：routelist  []，还未看函数
                result = uwan.json_data
                print 'line142',"result: ", result
                endTime = datetime_timestamp(result['Overall']['end_time'])
                if time.time() - endTime >= 100 and endTime != 0:
                    print "line 145"
                    stopTime = time.time() - endTime
                    fig.suptitle("HSM Stack Protocol Performance Display -- Elapsed Time since Last Refresh: %ds..." % stopTime)
                    print "No Data Transfer in %ds" % stopTime 
                    plt.pause(0.001)
                else:
                    for item in display_list:
                        print "line 152"
                        layer = item.layer
                        index = item.index
                        value = result[layer][index]
                        if value != "" and endTime != 0 and (time.time() - endTime < 100):
                            print "line 157"
                            simu_time = time.time() - start_time # 仿真进行持续时间
                            item.add_scatter(simu_time, value)
                            plt.pause(0.001) 
                        else:
                            print "No Data Transfer Now, Please Wait! "
                            break
        except Exception as ex:
            print 'traceback.print_exc():'; traceback.print_exc()
        # 每 5s 计算一次性能
        time.sleep(10)

if __name__ == '__main__':
    performanceAnalysis();
