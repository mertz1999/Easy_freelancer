from datetime import datetime
import requests



class Freelancer():
    def __init__(self) -> None:
        self.projects_id = []
        # self.skills_id = [1558]
        self.skills_id = [292,761,913,999,1199,1402,1558,1601]

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

