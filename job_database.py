import pandas as pd
from jobspy import scrape_jobs

import loader

env = loader.Config()

class Job:
    id = -1
    site = ''
    url = ''
    title = ''
    company = ''
    location = ''
    date = None
    salary_type = ''
    salary_interval = (0,0)
    remote = False
    description = ''
    company_url = ''
    company_photo = ''

class JobDatabase:
    df_job_db = None
    job_db = []
    temp_db = []

    def __init__(self):
        self.df_job_db = pd.read_csv('database_export.csv')
        print("# of loaded entries: " + str(len(self.df_job_db)))
        self.job_db = []
        for index, row in self.df_job_db.iterrows():
            jb = createJobRecord(row)
            self.job_db.append(jb)
        #print(f"Test - first loaded row ID: {self.job_db[0].id}")

    def updateDB(self):

        self.temp_db = []

        jobs = scrape_jobs(
            search_term=env.SEARCH_TERM,
            location=env.LOCATION,
            results_wanted=env.MAX_RESULTS,
            hours_old=env.PERIODICITY,  # (only Linkedin/Indeed is hour specific, others round up to days old)
            country_indeed=env.COUNTRY,  # only needed for indeed / glassdoor
            distance=env.DISTANCE,
            linkedin_fetch_description=True
            #proxies=env.PROXIES,
        )

        for index, row in jobs.iterrows():
            jb = createJobRecord(row)
            idList = [x.id for x in self.job_db]
            if jb.id not in idList:
                if len(self.df_job_db.index) >= int(env.MAX_DB_SIZE):
                    self.df_job_db = self.df_job_db.iloc[5:]
                new_df = pd.DataFrame([row])
                self.df_job_db = pd.concat([self.df_job_db, new_df], axis=0, ignore_index=True)
                self.job_db.append(jb)
                self.temp_db.append(jb)

        self.df_job_db.to_csv('database_export.csv')

        print("Finished gathering jobs.")

def createJobRecord(row):
    jb = Job()
    jb.id = row['id']
    jb.site = row['site']
    jb.title = row['title']
    jb.company = row['company']
    jb.url = row['job_url']
    jb.location = row['location']
    jb.date = row['date_posted']
    jb.salary_type = row['interval']
    jb.salary_interval = (row['min_amount'],row['max_amount'])
    jb.remote = row['is_remote']
    jb.description = row['description']
    jb.company_url = row['company_url']
    jb.company_photo = row['logo_photo_url']
    return jb
