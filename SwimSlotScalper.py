from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import smtplib

#Swim Lane Reservation Scalper Bot
#Automates purchasing of City of Henderson pools' swim lane reservations upon release to public

######################################################################################################################

""""PREREQUISITES:
#Must install geckodriver for Selenium use with browser, https://selenium-python.readthedocs.io/installation.html"""

######################################################################################################################
###################     Please fill in all variables marked with an 'X'   ############################################
######################################################################################################################

browser = 'X' #Insert the browser you are using, 'Firefox' or 'Chrome'

######################################################################################################################

"""Information required from user 
MUST FILL THESE OUT EVERY NEW RESERVATION"""

#Refer to SwimSlotDatabase.txt for a general listing of swim slots
#Check City of Henderson Rectrac for updates and most accurate listings:
#Multigen - https://web2.myvscloud.com/wbwsc/nvhendersonwt.wsc/search.html?display=listing&location=hmgc&module=AR&search=yes&type=reservelane 
#Whitney - https://web2.myvscloud.com/wbwsc/nvhendersonwt.wsc/search.html?display=listing&location=wrip&module=AR&search=yes&type=reservelane 
#Heritage - https://web2.myvscloud.com/wbwsc/nvhendersonwt.wsc/search.html?display=listing&location=hpac&module=AR&search=yes&type=reservelane 

slotDescription = 'X' #Insert the description of the slot, includes pool name and time
                                     #Can find master list of these in SwimSlotDatabase.txt
                                     #Ex: HPAC 3:00-4:00pm

day = 'X' #Insert the initial for day of week for the slot
          #Ex: Tu

familymember = 'X' #Insert legal first name of swimmer

######################################################################################################################

username = 'X' #Insert City of Henderson Rectrac username
password = 'X' #Insert City of Henderson Rectrac password

billingfirstname = 'X' #Insert first name             
billinglastname = 'X' #Insert last name
billingphone = 'X' #Insert phone number, no dashes or parentheses
billingemail = 'X' #insert email

cardholder = 'X' #Insert name of cardholder that appears on card
creditcardnumber = 'X' #Insert credit card number
cardpaymentmethod = 'X'   #choose between: VISA, Master Card, or Discover (Case sensitive, please follow as shown)
exp_month = 'X' #Insert expiration month of card as two digits
                #Ex: 04
exp_year = 'X' #Insert expiration year of card as four digits
               #Ex: 2024
cvv = 'X' #Insert CVV
billingaddress = 'X' #Insert billing address
billingzipcode = 'X' #Insert billing zip code

######################################################################################################################

"""If you would like to receive a text upon the confirmation of your swim slot, enter phone info here:"""

phonenumberSMS = 'X' #Insert phone number here, no dashes or parentheses

phonenumbercarrier = 'x' #choose from the following: att, tmobile, verizon, or sprint (Case sensitive, please follow as shown)

######################################################################################################################

#These are the two places where Firefox may be installed, please put these into binary variable if default doesn't work
#C:/Users/INSERT_USERNAME_HERE/AppData/Local/Mozilla Firefox/firefox.exe
#C:/Program Files/Mozilla Firefox/firefox.exe

#Sets selenium broswer to Firefox
if (browser == 'Firefox'):
    binary = FirefoxBinary('C:/Program Files/Mozilla Firefox/firefox.exe')
    driver = webdriver.Firefox(firefox_binary=binary)

#Sets selenium browser to Chrome
if (browser == 'Chrome'):
    driver = webdriver.Chrome() #Insert correct path to Chrome exe if default doesn't work

######################################################################################################################
################################    DO NOT EDIT PAST THIS POINT     ##################################################
################################    DO NOT EDIT PAST THIS POINT     ##################################################
################################    DO NOT EDIT PAST THIS POINT     ##################################################
################################    DO NOT EDIT PAST THIS POINT     ##################################################
################################    DO NOT EDIT PAST THIS POINT     ##################################################
######################################################################################################################

#Establishes system for sending messages, DO NOT EDIT

carriers = {
    'att':    '@mms.att.net',
    'tmobile':' @tmomail.net',
    'verizon':  '@vtext.com',
    'sprint':   '@page.nextel.com'
}

def send(message):
        # Replace number in main function
    to_number = phonenumberSMS + '{}'.format(carriers[phonenumbercarrier])
    auth = ('cohswimslotscalper@gmail.com', 'Sw1mSl0tScalp3r') #Enter in gmail login to send text messages through gmail servers, used due to no cost

    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP( "smtp.gmail.com", 587 )
    server.starttls()
    server.login(auth[0], auth[1])

    # Send text message through SMS gateway of destination number
    server.sendmail( auth[0], to_number, message)

######################################################################################################################



#Global variables
counter = 1     #Helps iterate between pages in change_page()
thingsincart = 0    #Keeps track of whether wanted slot has been bought in begin_buy()
familymembercounter = 1     #Helps iterate through family members based on their xpath in choose_family_member()
calendardate = ''          #Used to give date of reservation when sending SMS to user
wantedSlot = slotDescription + ' on ' + day #creates wantedSlot to search for, DO NOT EDIT

#logs into City of Henderson Webtrac website
def login():
    login_link = driver.find_element_by_id('menu_myaccount')
    login_link.click()
    username_box = driver.find_element_by_id('weblogin_username')
    username_box.click()
    username_box.send_keys(username)
    password_box = driver.find_element_by_id('weblogin_password')
    password_box.click()
    password_box.send_keys(password)
    login_button = driver.find_element_by_id('weblogin_buttonlogin')
    login_button.click()

#Chooses reservations/rentals tile to begin swim reservation process
def init_press():
    reserve_swim_time_slot_link = driver.find_element_by_xpath('//a[@href="splash.html?ccode=RRSplash"]')
    print('Reservations & Rentals tile clicked')
    reserve_swim_time_slot_link.click()

#Chooses the Multigen and its pools to look for swim slots
def choose_multigen():
    multigen_link = driver.find_element_by_xpath('//a[@href="search.html?display=listing&location=hmgc&module=AR&search=yes&type=reservelane"]')
    multigen_link.click() 

#Chooses Whitney Ranch and its pool to look for swim slots
def choose_whitney_ranch():
    whitney_ranch_link = driver.find_element_by_xpath('//a[@href="search.html?display=listing&location=wrip&module=AR&search=yes&type=reservelane"]')
    whitney_ranch_link.click()

#chooses Heritage and its pools to look for swim slots
def choose_heritage():
    heritage_link = driver.find_element_by_xpath('//a[@href="search.html?display=listing&location=hpac&module=AR&search=yes&type=reservelane"]')
    heritage_link.click()

#Makes decision on what pool to look for slots in based on wanted slot
def choose_pool():
    global wantedSlot
    if ('HMIP' in wantedSlot):
        choose_multigen()
    elif ('HMCP' in wantedSlot):
        choose_multigen()
    elif ('WRIP' in wantedSlot):
        choose_whitney_ranch()
    elif ('HPAC' in wantedSlot):
        choose_heritage()
    else:
        print('Could not find a pool with wanted slot, please recheck inputs')
        quit()

#Adds available swim slot to cart
def add_to_cart(resultnum):
    global thingsincart
    add_to_cart_link = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/form/div[1]/div[2]/div/div[1]/table/tbody/tr[' + str(resultnum) + ']/td[1]')
    add_to_cart_link.click()
    thingsincart += 1

#When finished adding items to cart, will go to family selection screen
def go_to_family_selection():
    element_present = EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div/div/button[2]'))
    timeout = 10
    WebDriverWait(driver, timeout).until(element_present)
    go_to_family_selection_link = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/button[2]')
    go_to_family_selection_link.click()

#if program doesn't check out, gets rid of swim slot being left in cart
def clear_cart_from_cookies():
    clear_selection_button = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/button[1]')
    if (clear_selection_button.is_displayed()):
        clear_selection_button.click()

#Chooses correct family member for swim slot
def choose_family_member():
    family_clicked = False
    global familymembercounter
    while family_clicked != True:
        family_member_select = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/form/div[' + str(familymembercounter) + ']/h1/span')
        if familymember.lower() in family_member_select.text.lower():
            family_member_checkbox = driver.find_elements_by_xpath('//button[@role="checkbox"]')[familymembercounter - 1] 
            family_member_checkbox.click()
            family_clicked = True
        else:
            familymembercounter += 1
    
def fill_out_waivers():
    def go_to_waivers():
        continue_button = driver.find_element_by_id('button201')
        continue_button.click()
    
    go_to_waivers()
    
    #If slot is actually fully enrolled but still says available, notifies user and quits program
    text = 'The MAX ENROLLED Count has been reached and no waitlist is allowed.'
    if (text in driver.page_source):
        print('Sorry, this slot is actually filled up, please choose a time other than ' + wantedSlot)
        quit()

    #If user is already enrolled for this slot, notifies user and quits program
    dupl_text = 'Duplicate enrollment.'
    if (dupl_text in driver.page_source):
        print('You have already signed up for this slot. Quitting program...')
        quit()

    #Accesses drop down menus to sign COVID waivers
    select = driver.find_elements_by_xpath('//button[@class="combobox"]')[0] #accesses first dropdown menu
    select.click()
    select = driver.find_elements_by_class_name('listitem__text')[1] #clicks yes in activated dropdown menu
    select.click()

    select = driver.find_elements_by_xpath('//button[@class="combobox"]')[1] #accessses second dropdown menu
    select.click()
    select = driver.find_elements_by_class_name('listitem__text')[1] #clicks yes in activated dropdown menu
    select.click()

    select = driver.find_element_by_xpath('//button[@role="checkbox"]')
    select.click()

    select = driver.find_element_by_id('processingprompts_buttoncontinue')
    select.click()

#Goes to checkout after filling out waivers
def proceed_to_checkout():
    select = driver.find_element_by_id('webcart_buttoncheckout')
    select.click()

#Enters basic billing info if not already filled out by WebTrac, 
def enter_billing_info():
    firstname = driver.find_element_by_id('webcheckout_billfirstname')
    if firstname.get_attribute(''):
        firstname.click()
        firstname.send_keys(billingfirstname)

    lastname = driver.find_element_by_id('webcheckout_billlastname')
    if lastname.get_attribute(''):
        lastname.click()
        lastname.send_keys(billinglastname)

    phone = driver.find_element_by_id('webcheckout_billphone')
    if phone.get_attribute(''):
        phone.click()
        phone.send_keys(billingphone)

    email = driver.find_element_by_id('webcheckout_billemail')
    if email.get_attribute(''):
        email.click()
        email.send_keys(billingemail)

    email2 = driver.find_element_by_id('webcheckout_billemail_2')
    if email2.get_attribute(''):
        email2.click()
        email2.send_keys(billingemail)

    continue_link = driver.find_element_by_id('webcheckout_buttoncontinue')
    continue_link.click()

#Enters payment info regarding credit card and address
#This is required only if swimmer does not have a membership tied to their name in RecTrac
def enterpaymentinfo():
    #Enters card payment method
    select = Select(driver.find_element_by_id('webcheckout_requiredmethod'))
    select.select_by_visible_text(str(cardpaymentmethod))

    #Enters cardholder's name
    cardholder_enter = driver.find_element_by_id('webcheckout_nameoncard')
    cardholder_enter.click()
    cardholder_enter.send_keys(cardholder)

    #Enters credit card number 
    driver.switch_to_frame("tokenFrame") #ccn input is inside i-frame, so must go into it
    creditcardnumber_enter = driver.find_element_by_id('ccnumfield')
    creditcardnumber_enter.click()
    creditcardnumber_enter.send_keys(creditcardnumber)
    driver.switch_to.default_content() #must go out of i-frame to access other contents

    #Enters expiration month
    datavaluexpathlink = "//*[@data-value='" #Used by both expiration month and year
    exp_month_enter = driver.find_element_by_id('webcheckout_expirationmonth_vm_3_button')
    exp_month_enter.click()
    month = driver.find_element_by_xpath(datavaluexpathlink + str(exp_month) + "']")
    actions = ActionChains(driver)
    actions.move_to_element(month).perform()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, datavaluexpathlink + str(exp_month) + "']"))).click() 
    
    #Enters expiration year
    exp_year_enter = driver.find_element_by_id('webcheckout_expirationyear_vm_4_button')
    exp_year_enter.click()
    month = driver.find_element_by_xpath(datavaluexpathlink + str(exp_year) + "']")
    actions = ActionChains(driver)
    actions.move_to_element(month).perform()
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, datavaluexpathlink + str(exp_year) + "']"))).click() 

    #Enters CVV
    cvv_enter = driver.find_element_by_id('webcheckout_cvv')
    cvv_enter.click()
    cvv_enter.send_keys(str(cvv))

    #Enters billing address
    billingaddress_enter = driver.find_element_by_id('webcheckout_billingaddress')
    billingaddress_enter.click()
    billingaddress_enter.send_keys(str(billingaddress))

    #Enters billing zip code
    billingzipcode_enter = driver.find_element_by_id('webcheckout_billingzipcode')
    billingzipcode_enter.click()
    billingzipcode_enter.send_keys(str(billingzipcode))

#Fills out entire checkout page, with info of billing address and payment method
def checkout():
    global phonenumberSMS
    global calendardate
    enter_billing_info()
    payment_present = EC.presence_of_element_located((By.ID, 'webcheckout_group6'))
    try:
        payment_present = EC.presence_of_element_located((By.ID, 'webcheckout_group6'))
        if (payment_present): #distinguishes those who have pool membership tied to family member
            enterpaymentinfo()
    except NoSuchElementException:
        pass
    try:
        end_continue = driver.find_element_by_id('webcheckout_buttoncontinue')
        end_continue.click()
    except NoSuchElementException:
        pass
    print(wantedSlot + ' has been reserved for ' + familymember + '.')
    if (phonenumberSMS != ''):
        print('Sending text message...')
        confirmedreservation = '\n\n' + wantedSlot + ' ' + calendardate + ' has been reserved for ' + familymember + '.'
        send(confirmedreservation)

#Begins buying process once wanted slot is added to cart
def beginbuy():
    global thingsincart
    if (thingsincart > 0):
        go_to_family_selection()
        choose_family_member()
    else:
        #will iterate through program until wanted slot is available
        while (thingsincart == 0):
            iterate_pages()
            
#Clicks button to switch between pages 1-4, based on counter variable
def change_page():
    global counter
    counter += 1
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #in cart overlay blocks page numbers, so must scroll to bottom
    time.sleep(2)
    beginpagelink = '/html/body/div[1]/div[1]/div/div/form/div[1]/div[2]/div/div[1]/ul/li['
    endpagelink = ']/button'
    if (counter == 3):  #this fixes program checking page 2 twice, not sure if problem is on my end or website
        counter += 1
    if (counter == 6): #hits page 4, then goes back to page 1
        counter = 1
    page = driver.find_element_by_xpath(beginpagelink + str(counter) + endpagelink)
    page.click()

#goes through page of swim slots, and adds to cart those that match user's description/are available
def choose_slot():
    global calendardate
    global counter
    slot_times = []
    slot_availability = []
    day_of_week_letter = []
    date = []
    description = []

    for i in range(1, 21):
        #tr[%i] determines what element it is, 1-21 per page
        slot_times.append(driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/form/div[1]/div[2]/div/div[1]/table/tbody/tr[%i]/td[5]' %(i)))
        slot_availability.append(driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/form/div[1]/div[2]/div/div[1]/table/tbody/tr[%i]/td[10]' %(i)))
        day_of_week_letter.append(driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/form/div[1]/div[2]/div/div[1]/table/tbody/tr[%i]/td[6]' %(i)))
        date.append(driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/form/div[1]/div[2]/div/div[1]/table/tbody/tr[%i]/td[4]/a/span[1]' %(i)))
        description.append(driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/form/div[1]/div[2]/div/div[1]/table/tbody/tr[%i]/td[3]' %(i)))
        
        slots = description[i-1].text + ' on ' + day_of_week_letter[i-1].text

        if (wantedSlot in slots):
            #Tells user that slot is available and adds to cart
            if slot_availability[i-1].text == 'Available':
                print((description[i - 1].text + ' on ' + day_of_week_letter[i - 1].text + ' ' + date[i - 1].text) + ' is available')
                print('Adding to cart...')
                calendardate = date[i - 1].text
                add_to_cart(i) #clicks add to cart of available slot
                
            #Tells user that slot is full, quits program
            elif (slot_availability[i-1].text == 'Full'):
                print((description[i - 1].text + ' on ' + day_of_week_letter[i - 1].text + ' ' + date[i - 1].text) + ' is full')
                print('please choose another slot that is either Available or Unavailable')
                print('Quitting program')
                time.sleep(2)
                quit()

            #Tells user that slot is not yet available, will loop through pages until slot becomes available in beginbuy()
            elif (slot_availability[i-1].text == 'Unavailable'):
                print((description[i - 1].text + ' on ' + day_of_week_letter[i - 1].text + ' ' + date[i - 1].text) + ' is not available yet')

#process done on each page, choosing slots, then going to next page
def iteration():
    choose_slot()
    change_page()
    element_present = EC.presence_of_element_located((By.ID, 'arwebsearch_buttonsearch'))
    timeout = 10
    WebDriverWait(driver, timeout).until(element_present)

#iterates through all listings of swim slots for 4 pages
def iterate_pages():
    iteration()
    iteration()
    iteration()
    
print('Slot wanted: ' + wantedSlot)
driver.get('https://web2.myvscloud.com/wbwsc/nvhendersonwt.wsc/splash.html?InterfaceParameter=WebTrac')
login()
init_press()
choose_pool()
clear_cart_from_cookies()
iterate_pages()
beginbuy()
fill_out_waivers()
proceed_to_checkout()
checkout()
exit()

