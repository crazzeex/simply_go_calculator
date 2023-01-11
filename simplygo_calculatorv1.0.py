from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import time
from datetime import datetime, timedelta

import os, pdfquery

def banner():
    print("""""
*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*
| This script was developed to help collate the total charges for a particular credit card for the previous month |
| (e.g. running this script in January 2023 will give you the total bill for December 2022)                       | 
| In order to run this script successfully, you will have to edit the following fields below:                     |
| In the simply_go_download function:                                                                             |
| (1) Username                                                                                                    |
| (2) Password                                                                                                    |
| (3) Label of credit card (refer to your simplygo dropdown box for this value)                                   |
|                                                                                                                 |
| In the pdf_converter function:                                                                                  |
| (1) Change the path of the download folder to the path of your download                                         |
*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*
""")


def simply_go_download():
    print("Accessing SimplyGo URL to login and download past month's MRT/Bus transactions...")
    #using chrome to access web
    driver = webdriver.Chrome()

    #open website
    driver.get('https://simplygo.transitlink.com.sg/')

    #select the username box & password box by id
    username_box = driver.find_element(By.ID,'username')
    password_box = driver.find_element(By.ID,'Password')

    #send login information
    username_box.send_keys('<username>')                              #<----------------- replace with your own username to simplygo ---------------------->
    password_box.send_keys('<password>')                              #<----------------- replace with your own password to simplygo ---------------------->

    #select the button using xpath
    login_btn = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/form/fieldset/div/span[5]/input")

    #click login
    login_btn.click()
    time.sleep(8)

    #select "sc smart" card from the dropdown
    cards = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/form/fieldset/div/p[1]/select")
    dropdown = Select(cards)
    dropdown.select_by_visible_text("<label of credit card>")         #<----------------- replace with the label of your credit card (refer to the text in the dropdown box) ----------------------->
    time.sleep(8)


    #select start date from calendar
    default_start_date_cal = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/form/fieldset/div/p[2]/input")
    default_start_date_cal.click()
    time.sleep(8)
    prev_start_date_cal = driver.find_element(By.XPATH,"/html/body/div[2]/div/a[1]/span")
    prev_start_date_cal.click()
    time.sleep(8)
    
    #since the UI displays date as a table, need to determine which columnn the 1st day of the month is in
    #/html/body/div[2]/table/tbody/tr[1]/td[5]/a (1st Dec 22 is on Thurs -> 1st row 5th column)
    #/html/body/div[2]/table/tbody/tr[1]/td[3]/a (1st Nov 22 is on  Tues -> 1st row 3rd Column)

    #tag day of the week to a number
    day_dict = {
        "Sunday" : "1",
        "Monday" : "2",
        "Tuesday" : "3",
        "Wednesday" : "4",
        "Thursday" : "5",
        "Friday" : "6",
        "Saturday" : "7",
    }

    date_today = datetime.now()
    first_date_current_month = date_today.replace(day=1)
    last_date_prev_month = first_date_current_month -  timedelta(days=1)
    first_date_prev_month = last_date_prev_month.replace(day=1)
    
    prev_first_day_of_month = first_date_prev_month.strftime('%A')
    prev_last_day_of_month = last_date_prev_month.strftime('%A')
    
    #determine start date xpath & click on start date
    start_date_xpath = "/html/body/div[2]/table/tbody/tr[1]/td[{}]/a".format(day_dict[prev_first_day_of_month])
    prev_start_date = driver.find_element(By.XPATH,start_date_xpath)
    prev_start_date.click()
    time.sleep(8)

    #select end date from calendar
    default_end_date_cal = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/form/fieldset/div/p[3]/input")
    default_end_date_cal.click()
    time.sleep(8)
    
    try: 
        prev_end_date_cal = driver.find_element(By.XPATH,"/html/body/div[2]/div/a[1]/span")
        prev_end_date_cal.click()
        time.sleep(8)

        #determine end date xpath & click on end date
        end_date_xpath = "/html/body/div[2]/table/tbody/tr[1]/td[{}]/a".format(day_dict[prev_last_day_of_month])
        prev_last_date = driver.find_element(By.XPATH(end_date_xpath))
        prev_last_date.click()
        time.sleep(8)

        #click download
        download_btn = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/form/div/input[2]')
        download_btn.click()
        time.sleep(10)

    
    except:
        #click download
        download_btn = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/form/div/input[2]')
        download_btn.click()
        time.sleep(10)



def pdf_converter():
    print("Extracting all charges to card...")
    os.chdir(r'C:\Users\<user>\Downloads')                           #<----------------- replace with your own path to your downloads folder ---------------------->
    downloads_folder = os.listdir(r'C:\Users\<user>\Downloads')      #<----------------- replace with your own path to your downloads folder ---------------------->
    
    #reads only the first Simplygo downloaded file in the downloads folder
    for file in downloads_folder:
        if file.startswith('TL-SimplyGo-TransactionHistory') and file.endswith('.pdf'):
            simplygo_pdf = pdfquery.PDFQuery(file)
            break
    

    simplygo_pdf.load()
    #simplygo_pdf.tree.write('simplygo.xml', pretty_print = True)

    #number of pages for pdf
    pages = simplygo_pdf.doc.catalog['Pages'].resolve()['Count']

    num_of_charges = 0
    total_charges = 0
    for i in range(pages):
        simplygo_pdf.load(i)

        #counts number of posted
        posted_label = (simplygo_pdf.pq('LTTextBoxHorizontal:contains("{}")'.format("POSTED"))) #finds the posted and stores in a class
        num_of_posted = len(([a.text() for a in posted_label.items('LTTextBoxHorizontal')])) #counts number of posted there are in this page
    
        #for each posted, assign the x and y coordinates of the box
        for j in range(num_of_posted):
            posted_label = simplygo_pdf.pq('LTTextBoxHorizontal:contains("{}")'.format("POSTED"))[j]
            x0 = float(posted_label.get('x0',0)) 
            y0 = float(posted_label.get('y0',0))
            x1 = float(posted_label.get('x1',0)) 
            y1 = float(posted_label.get('y1',0))     
            x0_charge = x0 + 336.96     #find the charge x0 coordinates since it always a fix distance away from POSTED
            x1_charge = x1 + 324.036    #find the charge x1 coordinates since it always a fix distance away from POSTED
            #print(x0_charge,y0,x1_charge,y1)
            
            #finds the amount charged based on the box coordinates and extracts the text
            charge = float(simplygo_pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (x0_charge,y0,x1_charge,y1)).text().split("$")[1])
            total_charges += charge
            num_of_charges += 1
            print("Charge #{0}: ${1:.2f}".format(num_of_charges,charge)) #<----comment this out if you do not want to see each charge on the card --------------------------->
    
    #cleans up the downloaded file  <--------------------- comment the below for loop out if you do not wish to remove pdf file from your downloads folder ------------------>
    for file in downloads_folder:
        if file.startswith('TL-SimplyGo-TransactionHistory') and file.endswith('.pdf'):
            simplygo_pdf.file.close()
            os.remove(file)

    print ("Total amount spent on MRT/Bus: ${:.2f}".format(total_charges))
    time.sleep(30)

if __name__ == "__main__":
    banner()
    simply_go_download()
    pdf_converter()

