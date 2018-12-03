import requests
import re
import traceback
import json
from bs4 import BeautifulSoup

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

# 获取体育部第一页通知的部分url
def getSpoNoticeList(snl,infoURL):
    html = getHTMLText(infoURL)
    soup = BeautifulSoup(html, 'html.parser')  #煮汤
    a = soup.find_all('a')  #寻找其中所有a标签的数据
    for i in a:
        try:
            href = i.attrs['href'] #获取a标签的href里的信息
            snl.append(re.findall(r"/\d{4}/\d{4}/[a-z0-9]{12}/", href)[0]) #使用正则将所需数据抽取出来给snl数组

        except:
            continue


def getSpoNoticeInfo(snl, sinfoURL, fpth):
    count = 0
    for sport in snl:
        url = sinfoURL + sport + 'page.htm' #将url拼接完成
        html = getHTMLText(url)
        try:
            if html == "":
                continue
            infoDist = {} #给个字典
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.find_all('td', attrs={'class':'biaoti3'})[0] #将td标签 + class=biaoti3的所有数据抽取

            infoDist.update({'通知标题': title.text.split()[0]}) #加入字典

            contentList = soup.find_all('meta', attrs={'name':'description'}) #抽取meta + name=description 所有抽取

            for i in range(len(contentList)):
                content = contentList[i].attrs['content'] #获取meta里的content数据
                con = "content"
                infoDist[con] = [content]

            with open(fpth, 'a', encoding='utf-8') as f:
                f.write(str(infoDist) + '\n')
                count = count + 1  # 进度条优化用户体验
                print('\r抓取体育通知当前速度：{: .2f}%'.format(count * 100 / len(snl)), end='') # 进度条

        except:
            count = count + 1  # 进度条优化用户体验
            print('\r当前速度：{: .2f}%'.format(count * 100 / len(snl)), end='')
            traceback.print_exc()  # 如果错误，报告错误信息
            continue


def getEduNoticeList(enl,eduURL):
    html = getHTMLText(eduURL)
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a')

    for i in a:
        try:
            href = i.attrs['href']
            enl.append(re.findall(r"/\d{4}/\d{4}/[a-z0-9]{12}/", href)[0])

        except:
            continue

def getEduNoticeInfo(enl,einfoURL,ePath):
    count = 0
    for Edu in enl:
            url = einfoURL + Edu + 'page.htm'
            html = getHTMLText(url)
            try:
                if html == "":
                    continue
                eInfoDict = {}
                soup = BeautifulSoup(html, 'html.parser')
                title = soup.title.string

                eInfoDict.update({'eduInfo': title}) #教务部通知的名称

                # i = soup.find_all('i', attrs={'class':'author'})
                # time = re.findall(r'\d{4}-\d{2}-\d{2}', i)

                contentList = soup.find_all('div', attrs={'class':'wp_articlecontent'})

                for i in range(len(contentList)):
                    content = contentList[i].text.split()[0] #获取meta里的content数据
                    con = "eduContent"
                    eInfoDict[con] = [content] #通知内容

                mm = json.dumps(eInfoDict, ensure_ascii=False) #将字典转换为JSON
                print(mm)

            except:
                traceback.print_exc()
                continue

def main():
    depth = 2 #可用于设置抓取的深度
    spoURL = 'http://tyb.xujc.com/tygg/list1.htm'
    tkkURL = 'http://tyb.xujc.com'
    spoOutput = 'D:\\Info.txt'
    spoList = []
    getSpoNoticeList(spoList, spoURL)
    getSpoNoticeInfo(spoList, tkkURL, spoOutput)
    eduURL = 'http://jwb.xujc.com/tzgg/list1.htm'
    eduTKK = 'http://jwb.xujc.com'
    eduOutput = 'D:\\EduInfo.txt'
    eduList = []
    getEduNoticeList(eduList, eduURL)
    getEduNoticeInfo(eduList, eduTKK, eduOutput)

main()