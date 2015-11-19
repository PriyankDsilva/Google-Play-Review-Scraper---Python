from lxml import html
import requests
from bs4 import BeautifulSoup
import re,os


#Function to get the Application Name and the Privacy Policy url and create file
def get_name_privacy_url(url,i,file_name):

    #log file
    log_file=r'./'+os.path.splitext(file_name)[0]+r'/'+os.path.splitext(file_name)[0]+'_log.csv'

    #get page data from google play
    try:
        app_page_data=requests.get(url)
    except Exception as e:
        #print('Error while fetching data from app url page.')
        write_to_log(log_file,'',url,'','',e,i)
        return 0

    html_data=html.fromstring(app_page_data.text)

    #xpath for app name and the developer links
    app_name_xpath="//div[@class='info-container']/div[@class='document-title' and @itemprop='name']/div/text()"
    dev_urls_xpath="//div[@class='content contains-text-link']/a[@class='dev-link']"

    #get the details for the app name and the developer urls
    try:
        application_name=str(html_data.xpath(app_name_xpath)[0])#.encode('utf-8','replace')
    except Exception as e:
        write_to_log(log_file,'',url,'','',e,i)
        return 0

    developer_urls=html_data.xpath(dev_urls_xpath)

    #loop through the developer urls to get the privacy policy url
    dev_privacy_policy_url=''
    for dev_url in developer_urls:
        if 'Privacy Policy' in dev_url.text:
            dev_privacy_policy_url = dev_url.attrib['href']#.replace('https://www.google.com/url?q=', '')
        else:
            dev_privacy_policy_url='NA'

    #create a pricavy policy for the file
    privacy_policy_file_name=str(i)+str(application_name)
    privacy_policy_file_name=re.sub('[^A-Za-z0-9]+', '', privacy_policy_file_name)
    privacy_policy_file_name=r'./'+os.path.splitext(file_name)[0]+r'/'+privacy_policy_file_name+'.txt'



    #get the policy data into a file
    if dev_privacy_policy_url != 'NA':
        #if there exists a url for the app
        #get the data from the policy page
        try:
            policy_page_data=requests.get(dev_privacy_policy_url)
        except Exception as e:
            #print('Error while fetching data from policy url page.')
            write_to_log(log_file,application_name,url,dev_privacy_policy_url,'',e,i)
            #print('Google Play App Name : ',application_name)
            return 0

        soup = BeautifulSoup(policy_page_data.content, "lxml")

        #check to see if its a redirecting url,if so then capture the redirecting url
        if 'Redirecting you to' in soup.html.body.get_text():
            redirect_url=re.search("(?P<url>https?://[^\s]+)", soup.html.body.get_text()).group("url")

            try:
                redirect_page_data=requests.get(redirect_url)
            except Exception as e:
                #print('Error while fetching data from policy redirected page.')
                write_to_log(log_file,application_name,url,dev_privacy_policy_url,redirect_url,e,i)
                #print('Google Play App Name : ',application_name)
                return 0

            soup2=BeautifulSoup(redirect_page_data.content, "lxml")


            #if any error occours while fetching the data from the policy url then capture it
            try:
                policy_file=open(privacy_policy_file_name,'w',encoding='utf-8', errors='replace')
                #policy_file=open(privacy_policy_file_name,'w')#,encoding='utf-8', errors='replace')
                #policy_file.write(soup2.get_text())
                policy_file.write(soup2.html.body.get_text())
                policy_file.close()
                write_to_log(log_file,application_name,url,dev_privacy_policy_url,redirect_url,'Privacy Policy Captured',i)

            except Exception as e:
                policy_file.close()
                write_to_log(log_file,application_name,url,dev_privacy_policy_url,redirect_url,e,i)

        else:
            try:
                policy_file=open(privacy_policy_file_name,'w',encoding='utf-8', errors='replace')
                #policy_file=open(privacy_policy_file_name,'w')#,encoding='utf-8', errors='replace')
                #policy_file.write(soup.get_text())
                policy_file.write(soup.html.body.get_text())
                policy_file.close()
                write_to_log(log_file,application_name,url,dev_privacy_policy_url,'','Privacy Policy Captured',i)

            except Exception as e:
                policy_file.close()
                write_to_log(log_file,application_name,url,dev_privacy_policy_url,'',e,i)

    else:
        #if there dosent exists a url for the app just create an empty file
        policy_file=open(privacy_policy_file_name,'w')
        policy_file.close()
        write_to_log(log_file,application_name,url,'Privacy Policy URL Not Found!!!','','Empty Policy File',i)

    #display the outputs
    #print('Google Play App Name : ',application_name)


def get_app_urls(file_name):

    #loop through the file
    for url in open(file_name,'r'):
        get_name_privacy_url(url.strip('\n').split(',')[1],url.strip('\n').split(',')[0],file_name)


def create_structure(file_name):
    #make dir for the category
    if not os.path.exists(os.path.splitext(file_name)[0]):
        os.makedirs(os.path.splitext(file_name)[0])

    #make log file for the run
    log_file=r'./'+os.path.splitext(file_name)[0]+r'/'+os.path.splitext(file_name)[0]+'_log.csv'
    f=open(log_file,'w')
    f.write('\"Applicaion Name\",\"App URL\",\"Privacy Policy URL\",\"Privacy Policy Redirected URL\",\"Status\"\n')
    f.close()

def write_to_log(log_file,app_name,app_url,policy_url,policy_redirect_url,status,i):
    f=open(log_file,'a')
    try:
        if app_name=='':
            app_name='NOT FOUND'
            print('Google Play App Name ['+str(i)+'] : Not Captured')
        else:
            print('Google Play App Name ['+str(i)+'] :',app_name)
        f.write('\"'+str(app_name)+'\",\"'+str(app_url)+'\",\"'+str(policy_url)+'\",\"'+str(policy_redirect_url)+'\",\"'+str(status)+'\"\n')
    except Exception as e:
        print('Special characters Encountered')
        f.write('\"SPECIAL CHARACTERS\",\"'+str(app_url)+'\",\"'+str(policy_url)+'\",\"'+str(policy_redirect_url)+'\",\"'+str(status)+'\"\n')
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