from lxml import etree
import csv
import requests

url = "oa.hz.zj.mof"
msg = {'Username': 'admin_hz', 'Password': 'domino2006'}
count = '189'
intoxml = str(msg['Username']+".xml")
outcsv = str(msg['Username']+".csv")


def xmlfile(url1=url,msg1=msg,count1=count,intoxml1=intoxml):
    session = requests.session()
    reqlogin = 'http://'+url1+'/names.nsf?Login'
    reqxml = 'http://'+url1+'/czoadv/receivedoc.nsf/0?readviewentries&start=1&Count='+count1
    print(reqxml)
    session.post(url=reqlogin, data=msg1)
    xmlcontent = session.get(url=reqxml)
    xmlcontent.encoding = "utf-8"
    with open(intoxml1,'w',encoding="utf-8") as f:
        f.write(xmlcontent.text)
    return

def xmlcontent(intoxml2=intoxml,outcsv2=outcsv):
    '''
    :param intoxml2: 解析xml文件
    :param outcsv2: 导出csv文件
    '''
    xmlemt = etree.parse(intoxml2)
    csvfile=open(outcsv2, 'w',newline='')
    writer = csv.writer(csvfile)
    # 计算文件行数
    n=int(xmlemt.xpath('//viewentry[last()]')[0].get('position'))
    # 计算文件列数
    x=int(xmlemt.xpath('//viewentry[@position=1]/entrydata[last()]')[0].get('columnnumber'))
    m=x+2
    for j in range(1,n):
        L=[]
        unid=xmlemt.xpath('//viewentry[@position=' + str(j) + ']')[0].get('unid')
        L.append(unid)
        for i in range(1, m):
            xpathemt = ['//viewentry[@position='+str(j)+']/entrydata[' + str(i) + ']/*']
            for n in xpathemt:
                node = xmlemt.xpath(''.join(n))
                while node[0].text is None:
                    xpathemtof = '//viewentry[@position=' + str(j) + ']/entrydata[' + str(i) + ']/*/*'
                    N=[]
                    for a in xmlemt.xpath(xpathemtof):
                        N.append(a.text)
                    L.append(N)
                    break
                else:
                    L.append(node[0].text)
        writer.writerow(L)
    csvfile.close()
    return

if __name__ == '__main__':
    print("*"*64)
    print("* 登录地址：", url)
    print("* 用户名及密码：", msg["Username"], msg["Password"])
    print("*"*64)
    print("开始生成XML文件..........\n",intoxml)
    xmlfile()
    print("*" * 64)
    print("正在导出CSV文件共"+count+"条...........\n",outcsv)
    xmlcontent()
    print("*" * 64)