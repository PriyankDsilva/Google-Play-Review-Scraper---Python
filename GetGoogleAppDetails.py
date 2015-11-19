from lxml import html
import requests
from bs4 import BeautifulSoup
import re,os
from AppParser import parser as html_parser
from bs4 import BeautifulSoup

import codecs


def fetch_NonTextInfo(url,file_name):

    app_page_data=requests.get(url)
    soup = BeautifulSoup(app_page_data.content, "lxml")
    Info_file=os.path.splitext(file_name)[0]+'_NonTextInfo.xls'

    if 'We\'re sorry, the requested URL was not found on this server.' in soup.html.body.get_text():
        f = codecs.open(Info_file, 'a', encoding='utf8')
        f.write('App Not Found'+'\t'+url+'\t'+'\n')
        f.close()
    else:
        try:
            parser = html_parser()
            app = parser.parse_app_data(app_page_data.text)
        except:
            f = codecs.open(Info_file, 'a', encoding='utf8')
            f.write('Error While Fetching'+'\t'+url+'\t'+'\n')
            f.close()
            return 0



        #privacy Policy
        if str(app['DeveloperPrivacyPolicy']) =='None':
            IsPrivacyPolicy='0'
        else:
            IsPrivacyPolicy='1'

        #Trailer
        if str(app['Video']) =='None':
            IsTrailer='0'
        else:
            IsTrailer='1'

        #Top Developer
        if app['IsTopDeveloper']==True:
            IsTopDeveloper='1'
        else:
            IsTopDeveloper='0'


        f = codecs.open(Info_file, 'a', encoding='utf8')
        f.write(app['Name']+'\t'+url+'\t'+str(app['Price'])+'\t'+str(len(app['Screenshots']))+'\t'+str(app['Count'])+'\t'+str(app['Reviewers'])+'\t'+str(app['FiveStars'])+'\t'+str(app['FourStars'])+'\t'+str(app['ThreeStars'])+'\t'+str(app['TwoStars'])+'\t'+str(app['OneStars'])+'\t'+IsTopDeveloper+'\t'+IsTrailer+'\t'+IsPrivacyPolicy+'\n')
        f.close()

def get_app_urls(file_name):

    for url in open(file_name,'r'):
        fetch_NonTextInfo(url.strip('\n').split(',')[1],file_name)
        #print(url.strip('\n').split(',')[1])



def create_structure(file_name):

    #makecsv file
    Info_file=os.path.splitext(file_name)[0]+'_NonTextInfo.xls'
    f = codecs.open(Info_file, 'w', encoding='utf8')
    f.write('\"Application Name\"\t\"Application URL\"\t\"Price\"\t\"# of  Screenshots\"\t\"Average Rating\"\t\"Total # of Raters\"\t\"5 Stars\"\t\"4 Stars\"\t\"3 Stars\"\t\"2 Stars\"\t\"1 Star\"\t\"Top Developer Badge\"\t\"Demo Video\"\t\"Privacy Policy\"\n')
    f.close()




def main():
    file_name='ToolsList.txt'
    #Validation to check if file exists
    if os.path.isfile(file_name) is False:
        print('File : '+file_name+' does not exist !!!')
        return 0

    create_structure(file_name)
    get_app_urls(file_name)



main()
