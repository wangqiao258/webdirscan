#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import time  #时间模块
import queue  #队列
import argparse  #参数
import requests  #request请求
import threading  #多线程
import re  #正则表达式

class Dirscan(object):

    def __init__(self, scanSite, scanDict, scanOutput,threadNum):
        print('目录扫描正在运行！')
        if re.match(r'^https?:/{2}\w.+$', scanSite) or re.match(r'^http?:/{2}\w.+$', scanSite):  #判断scanSite传参是否为http开头或https开头
            self.scanSite =scanSite


        print('测试目标：',self.scanSite)
        self.scanDict = scanDict
        self.scanOutput = scanSite.replace('https://', '').replace('http://', '').replace('/','-').replace(':','-')+'.txt'  if scanOutput == 0 else scanOutput  #如果没有指定输出文件名则按域名保存
        print("保存:",self.scanOutput)
        truncate = open(self.scanOutput,'w', encoding='utf-8')
        truncate.close()
        self.threadNum = threadNum
        self.lock = threading.Lock()
        self._loadHeaders()
        self._loadDict(self.scanDict)
        self._analysis404()
        self.STOP_ME = False

    def _loadDict(self, dict_list):
        self.q = queue.Queue()
        with open(dict_list, encoding='utf-8') as f:
            for line in f:
                if line[0:1] != '#':
                    self.q.put(line.strip())
        if self.q.qsize() > 0:
            print('字典大小：',self.q.qsize())
        else:
            print('Dict is Null ???')
            quit()

    def _loadHeaders(self):
        self.headers = {
            'Accept': '*/*',
            'Referer': 'http://www.baidu.com',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; ',
            'Cache-Control': 'no-cache',
        }
    def _analysis404(self):
        if self.scanSite[-1] != "/":
            self.scanSite = self.scanSite +"/"
        notFoundPage = requests.get(self.scanSite + '/songgeshigedashuaibi/hello.html', allow_redirects=False)
        self.notFoundPageText = notFoundPage.text.replace('/songgeshigedashuaibi/hello.html', '')


    def _writeOutput(self, result):
        self.lock.acquire()
        with open(self.scanOutput, 'a+', encoding='utf-8') as f:
            f.write(result + '\n')
        self.lock.release()

    def _scan(self, url):
        html_result = 0
        try:
            html_result = requests.get(url, headers=self.headers, allow_redirects=False, timeout=15)
        except requests.exceptions.ConnectionError:
            # print 'Request Timeout:%s' % url
            pass
        finally:
            if html_result != 0:
                if html_result.status_code == 200 and html_result.text != self.notFoundPageText:
                    print('[%i]%s' % (html_result.status_code, html_result.url))
                    self._writeOutput('[%i]%s' % (html_result.status_code, html_result.url))


    def run(self):
        while not self.q.empty() and self.STOP_ME == False:
            url = self.scanSite + self.q.get()
            self._scan(url)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()  #创建一个解析对象
    parser.add_argument('scanSite', help="帮助信息", type=str)
    parser.add_argument('-d', '--dict', dest="scanDict", help="选择字典", type=str, default="dict/dict.txt")
    parser.add_argument('-o', '--output', dest="scanOutput", help="输出结果", type=str, default=0)
    parser.add_argument('-t', '--thread', dest="threadNum", help="线程数", type=int, default=60)
    args = parser.parse_args()

    scan = Dirscan(args.scanSite, args.scanDict, args.scanOutput, args.threadNum)

    for i in range(args.threadNum):
        t = threading.Thread(target=scan.run)
        t.setDaemon(True)
        t.start()

    while True:
        if threading.activeCount() <= 1 :
            break
        else:
            try:
                time.sleep(0.1)
            except KeyboardInterrupt as e:
                print('\n[WARNING] User aborted, wait all slave threads to exit, current(%i)' % threading.activeCount())
                scan.STOP_ME = True

    print('扫描结束 !!!')
