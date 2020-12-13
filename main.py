
import urllib.request
from bs4 import BeautifulSoup
import json
import io



def write_json(data):
    # just write to json file
    with open('results.json', 'a', encoding='utf-8') as outfile:
        outfile.write(json.dumps(data, indent=4))
        outfile.write(",")
        outfile.close()

def remove(soup,arg):
    for a in soup.find_all('{}'.format(arg)):
        a.replaceWithChildren()


def preprocess(url,category):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "lxml")

    tag_to_delete = ['a','span','b','i','bdi']

    for tag in tag_to_delete:
        remove(soup,tag)

    for a in soup.find_all('sup'):
        a.decompose()


    title = str(soup.select('h1')[0].text.strip())

    content = soup.find_all('p')

    cnt = 0
    my_details = {}
    for i in content :
            cnt +=1
            my_details["parag num{}".format(cnt)] = {

                    'length' : len(str(i)),
                    'content' : str(i)
            }

    output = {}
    output[title] = {'category' : category,
                    'title': title,
                      'url': url,
              'paragraphs' : my_details
                }
    write_json(output)


cnt = 0
def category(url,type):

    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "lxml")
    tmp  = soup.select('table > tbody > tr > td > a ')

    global cnt

    for i in tmp:

        cnt +=1
        print('+++ subject :   ' + str (i['title']))

        preprocess('https://fa.wikipedia.org'+i['href'],type)
        print(cnt)


def most_visit():

    url = 'https://fa.wikipedia.org/wiki/%D9%88%DB%8C%DA%A9%DB%8C%E2%80%8C%D9%BE%D8%AF%DB%8C%D8%A7:%D9%81%D9%87%D8%B1%D8%B3%D8%AA_%D9%85%D9%82%D8%A7%D9%84%D8%A7%D8%AA_%D9%BE%D8%B1%D8%A8%DB%8C%D9%86%D9%86%D8%AF%D9%87_%D8%A8%D8%B1_%D9%BE%D8%A7%DB%8C%D9%87_%D9%85%D9%88%D8%B6%D9%88%D8%B9#%D8%B9%D9%84%D9%88%D9%85_%D8%A7%D9%86%D8%B3%D8%A7%D9%86%DB%8C_%D9%88_%D8%A7%D8%AF%DB%8C%D8%A7%D9%86'
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "lxml")
    categories = soup.find_all("div", class_=['column-count column-count-۵','column-count column-count-۳'])

    for i in categories:
        tmp= i.find_all('a')
        for j in tmp :
            title = str(j['title']).replace('ویکی‌پدیا:پربیننده/', '')
            print('category :  we are in ----> '+title)
            category('https://fa.wikipedia.org'+j['href'],title)


most_visit()


