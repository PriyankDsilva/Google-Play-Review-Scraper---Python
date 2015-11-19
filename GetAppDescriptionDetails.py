from lxml import html
import requests
from bs4 import BeautifulSoup
import re,os
import codecs


#Function to get the Application Name and the Privacy Policy url and create file
def get_name_privacy_url(url,i,file_name):

    #log file
    log_file=r'./'+os.path.splitext(file_name)[0]+r'/'+os.path.splitext(file_name)[0]+'_log.csv'

    #get page data from google play
    try:
        app_page_data=requests.get(url)
    except Exception as e:
        #print('Error while fetching data from app url page.')
        write_to_log(log_file,'',url,'',i)
        return 0

    html_data=html.fromstring(app_page_data.text)

    #xpath for app name and the developer links
    app_name_xpath="//div[@class='info-container']/div[@class='document-title' and @itemprop='name']/div/text()"
    description_xpath="//div[@class='show-more-content text-body' and @itemprop='description']/div/text()|//div[@class='show-more-content text-body' and @itemprop='description']/div/p/text()"

    #get the details for the app name and the developer urls
    try:
        application_name=str(html_data.xpath(app_name_xpath)[0])#.encode('utf-8','replace')
    except Exception as e:
        write_to_log(log_file,'',url,'',i)
        return 0


    #function to get the text info using xpath
    def extract_node_text(map,is_list=False):

        #xpath = XPath.xPaths[key]
        description_xpath="//div[@class='show-more-content text-body' and @itemprop='description']/div/text()|//div[@class='show-more-content text-body' and @itemprop='description']/div/p/text()"
        node = map.xpath(description_xpath)

        if not node:
            return None

        if not is_list:
            return node[0].strip()
        else:
            # Distinct elements found
            seen = set()
            return [x for x in node if x not in seen and not seen.add(x)]


    app_data = dict()

    try:
        app_data['Description'] = "\n".join(extract_node_text(html_data, True))
    except:
        write_to_log(log_file,application_name,url,'No',i)



    #create a pricavy policy for the file
    desc_file_name=str(i)+str(application_name)
    desc_file_name=re.sub('[^A-Za-z0-9]+', '', desc_file_name)
    desc_file_name=r'./'+os.path.splitext(file_name)[0]+r'/'+desc_file_name+'.txt'

    try:
        f = codecs.open(desc_file_name, 'w', encoding='utf8')
        f.write(app_data['Description'])
        f.close
    except:
        write_to_log(log_file,application_name,url,'No',i)
    else:
        write_to_log(log_file,application_name,url,'Yes',i)




def get_app_urls(file_name):

    #loop through the file
    counter=1
    for url in open(file_name,'r'):
        get_name_privacy_url(url.strip('\n').split(',')[1],url.strip('\n').split(',')[0],file_name)
        counter+=1

def create_structure(file_name):
    #make dir for the category
    if not os.path.exists(os.path.splitext(file_name)[0]):
        os.makedirs(os.path.splitext(file_name)[0])

    #make log file for the run
    log_file=r'./'+os.path.splitext(file_name)[0]+r'/'+os.path.splitext(file_name)[0]+'_log.csv'
    f=open(log_file,'w')
    f.write('\"Applicaion Name\",\"App URL\",\"Description Captured\"\n')
    f.close()

def write_to_log(log_file,app_name,app_url,desc_captured,i):
    f=open(log_file,'a')
    try:
        if app_name=='':
            app_name='NOT FOUND'
            print('Google Play App Name ['+str(i)+'] : Not Captured')
        else:
            print('Google Play App Name ['+str(i)+'] :',app_name)
        f.write('\"'+str(app_name)+'\",\"'+str(app_url)+'\",\"'+str(desc_captured)+'\"\n')
    except Exception as e:
        print('Special characters Encountered')
        f.write('\"SPECIAL CHARACTERS\",\"'+str(app_url)+'\",\"'+str(desc_captured)+'\"\n')
    f.close()



def main():
    #file_name='GameLink.txt'
    file_name='ToolsList.txt'
    #Validation to check if file exists
    if os.path.isfile(file_name) is False:
        print('File : '+file_name+' does not exist !!!')
        return 0

    create_structure(file_name)
    get_app_urls(file_name)

main()