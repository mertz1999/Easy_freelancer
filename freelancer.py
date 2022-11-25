from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
import requests
import time



class Freelancer():
    def __init__(self, username, password, driver_path="./driver/chromedriver.exe") -> None:
        self.projects_id = []
        self.username    = username
        self.password    = password
        self.skills_id   = [292,761,913,999,1199,1402,1558,1601]
        self.service     = Service(executable_path= driver_path)
        self.driver      = webdriver.Chrome(service=self.service)


    # Trying to find new projects
    def fetch_projects(self):
        new_projects = []
        for id in self.skills_id:
            # Request to freelancer.com
            r = requests.get(f'https://www.freelancer.com/api/projects/0.1/projects/active?jobs[]={id}&full_description=True&limit=5')
            projects =  r.json()['result']['projects']

            for p in projects:
                # Check this project has been record or not
                if p['id'] not in self.projects_id:
                    self.projects_id.append(p['id'])
                    new_projects.append(p)
                
                if len(self.projects_id) > 30:
                    self.projects_id = self.projects_id[1:]     

        return new_projects
    
    # Make telegram message based on project json
    def make_message(self,in_json):
        project_id  = in_json['id']
        title       = in_json['title']
        url         = in_json['seo_url']
        currency    = in_json['currency']['sign']
        description = in_json['description']
        now         = datetime.now()
        submitted   = datetime.fromtimestamp(in_json['submitdate'])
        budget_type = 'per hour' if in_json['type'] == 'hourly' else 'fixed price'
        budget      = in_json['budget']
        bids_info   = f'Total: {in_json["bid_stats"]["bid_count"]}  Avg: {int(in_json["bid_stats"]["bid_avg"])}'
        
        max_hours_str = ''
        if in_json['type'] == 'hourly':
            max_hours = in_json['hourly_project_info']['commitment']['hours']
            max_hours_str = f'max hours: {max_hours}'

        msg_maked = f'''
✅ (( Freelancer #{project_id} )) 

🕓 Now time: {now}
🕓 Submit time: {submitted}

💰 Budget:
{currency}{int(budget['minimum'])} - {currency}{int(budget['maximum'])} {budget_type}
{max_hours_str}

▶ Bids:
{bids_info}

💠 Title: 
{title} 

💠 Description:
{description}

🌐 https://www.freelancer.com/projects/{url} 
                    '''

        return msg_maked

    # Login
    def login(self):
        if ('freelancer' not in self.driver.current_url) or ('login' in self.driver.current_url):
            try:
                # Get login url
                self.driver.get("https://www.freelancer.com/login")

                # Send email address
                inputs = self.driver.find_elements(By.XPATH, "//input[@id='emailOrUsernameInput']")
                inputs[1].send_keys(self.username)

                # Send password
                inputs = self.driver.find_elements(By.XPATH, "//input[@id='passwordInput']")
                inputs[1].send_keys(self.password)

                time.sleep(3)
                buttun = self.driver.find_elements(By.XPATH, "//app-login-signup-button")
                buttun[0].click()

                time.sleep(5)

                return True
            except:
                return False
        else:
            return True
    

    # Set Bid on projects
    def send_bid(self, url, priod, amount, prop_path='proposals\prop'):
        if self.login():
            # Check login don`t require verification
            total_page = self.driver.find_elements(By.TAG_NAME, "body")
            total_page = total_page[0].text
            if '2-Step Verification' in total_page:
                print("Verification need")
                return False
            
            # Redirect to project url path
            try:
                self.driver.get(url)
                time.sleep(10)

                # set display=None for messaging
                self.driver.execute_script("document.getElementsByTagName('app-messaging')[0].style.display = 'none';")

                # Send priod
                inputs = self.driver.find_elements(By.ID, "periodInput")
                inputs[0].clear()
                inputs[0].send_keys(priod) 

                time.sleep(2)

                # Send amout of money
                inputs = self.driver.find_elements(By.ID, "bidAmountInput")
                inputs[0].clear()
                inputs[0].send_keys(0)
                for i in range(10):
                    inputs[0].send_keys(Keys.BACK_SPACE)
                inputs[0].send_keys(amount)

                # Send proposal
                inputs = self.driver.find_elements(By.ID, "descriptionTextArea")
                proposal_file = open(prop_path,"r")
                proposal = proposal_file.read()
                inputs[0].send_keys(proposal)

                # Set bid
                time.sleep(3)
                buttun = self.driver.find_elements(By.XPATH, "//fl-button[@class='BidFormBtn']")
                buttun[0].click()

                time.sleep(3)

                return True
            except:
                return False

            

        else:
            print("Login not completed!")
            return False



# Test This class

# freelancer = Freelancer(username= "hihellosalam2022@gmail.com", password="@Rezatz1378")

# print(freelancer.send_bid("https://www.freelancer.com/projects/python/DDOs-attack-simuation-using-Machine", priod=10, amount=170))