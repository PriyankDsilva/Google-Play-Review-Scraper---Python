from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import codecs
import re,os
from lxml import html
import time

def ReviewScraper(url,i):

    #driver = webdriver.Firefox()
    driver = webdriver.Chrome()
    driver.get(url)



    appname_temp=driver.find_element_by_class_name('document-title').text
    #print(appname_temp)
    appname=re.sub('[^A-Za-z0-9]+', '', appname_temp)
    #print(appname)

    #Wait for the presence of the expand button
    element = WebDriverWait(driver, 36000).until(EC.presence_of_element_located((By.CLASS_NAME,'expand-button')))

    #click the expand button for the first time
    button=driver.find_elements_by_class_name('expand-button')
    button[3].click()

    review_file_name=str(i)+str(appname_temp)
    review_file_name=re.sub('[^A-Za-z0-9]+', '', review_file_name)
    review_file_name=review_file_name+'.txt'

    f = codecs.open(review_file_name, 'w', encoding='utf8')
    f.write(appname_temp+'\n')

    count=1
    data_xpath='.//div[@class="review-body"]/text()'
    name_xpath='.//div/div/span[@class="author-name"]/a/text()'
    other_name_xpath='.//div/div/span[@class="author-name"]/text()'
    date_xpath='.//span[@class="review-date"]/text()'
    rating_xpath='.//div[@class="tiny-star star-rating-non-editable-container"]/@aria-label'

    #get initial reviews
    review=driver.find_elements_by_class_name('single-review')

    x=1


    while True:
    #find reviews
        try:
            #print('Loop :',x)
            review_count=len(review[count-1:])
            #print('Review Count :',review_count)
            for item in review[count-1:]:
                html_data=html.fromstring(item.get_attribute('innerHTML'))
                f.write(str(count)+'\n')

                try:
                    f.write(str(html_data.xpath(name_xpath)[0]).lstrip().rstrip()+'\n')
                except:
                    f.write(str(html_data.xpath(other_name_xpath)[0]).lstrip().rstrip()+'\n')

                f.write(str(html_data.xpath(date_xpath)[0]).lstrip().rstrip()+'\n')
                f.write(str(html_data.xpath(rating_xpath)[0]).lstrip().rstrip()+'\n')
                f.write(str(html_data.xpath(data_xpath)[1]).lstrip().rstrip()+'\n')

                count+=1

        except Exception as e:
            print('Error while fetching Review :\"',e,'\"',sep='')
            f.close()
            driver.close()

            return False

        try:

            if count > 600:
                #print('600 Reviews Fetched...Quit')
                f.close()
                driver.close()

                return False



            Refresh_Count=1
            while review==driver.find_elements_by_class_name('single-review') and Refresh_Count < 30:
                time.sleep(1)
                Refresh_Count+=1

                try:
                    button[3].click()
                except:
                    time.sleep(2)

            if  Refresh_Count == 30:
                f.close()
                driver.close()

                return False

            #print('Refresh Count :',Refresh_Count)

            review=driver.find_elements_by_class_name('single-review')




            x+=1
        except Exception as e:
            f.close()
            driver.close()
            print('Error1 : ',e)

    try:
        f.close()
        driver.close()

    except Exception as e:
        print('Error2 : ',e)

#call scrape function
#ReviewScraper(url,1)
#print('End Time : ',strftime("%Y-%m-%d %H:%M:%S", gmtime()))

def get_app_urls(file_name):

    #loop through the file
    counter=1
    for url in open(file_name,'r'):


        try:
            ReviewScraper(url.strip('\n').split(',')[1],url.strip('\n').split(',')[0])
        except Exception as e:
            print('Error :',e)
        counter+=1



def get_file():
    filelist=[]
    for i in os.listdir():
        if 'Social' in i and '.txt' in i:
            filelist.append(i)
    return filelist


def main():

    #file_name='EntertainmentList1.txt'
    #Validation to check if file exists

    filelist=get_file()
    file_name=filelist[0]
    print(file_name)


    if os.path.isfile(file_name) is False:
        print('File : '+file_name+' does not exist !!!')
        return 0

    try:
        get_app_urls(file_name)
    except Exception as e:
        print('Errorr : ',e)
    else:
        os.remove(file_name)

main()