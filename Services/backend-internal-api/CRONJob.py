from crontab import CronTab

# Cron job class, singleton; We only need one instance of this
class CronJob:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    # Initiate an instance of CronTab and setup a self.jobs dictionary we can use to store all our jobs
    def __init__(self):
        self.cron = CronTab(user=True)
        self.jobs = {}

    # Stop all the jobs
    def stop_all_jobs(self):
        self.cron.remove_all()
        self.cron.write()
        self.jobs = {}

    # Start all the jobs
    def start_all_jobs(self):
        for job in self.jobs.values():
            job.enable()
        self.cron.write()

    # Start a specific job
    def start_job(self, job_name):
        if job_name not in self.jobs:
            raise ValueError(f"Job '{job_name}' does not exist.")
        self.jobs[job_name].enable()
        self.cron.write()

    # Stop a specific job
    def stop_job(self, job_name):
        if job_name not in self.jobs:
            raise ValueError(f"Job '{job_name}' does not exist.")
        self.jobs[job_name].disable()
        self.cron.write()
    
    # Create a job dynamically
    def add_job(self, job_name, job_py_type, time, *args, **kwargs):
        if job_name in self.jobs:
            raise ValueError(f"Job '{job_name}' already exists.")

        job = JobFactory.create_job(job_py_type, time, *args, **kwargs)
        cron_job = self.cron.new(command=job.command)
        cron_job.setall(job.schedule)
        self.cron.write()

        self.jobs[job_name] = cron_job

        return 'Cron job' + job_name + 'has started successfully with time: ' + str(time)
    
    # Remove a job
    def remove_job(self, job_name):
        if job_name in self.jobs:
            self.jobs[job_name].delete()
            del self.jobs[job_name]
        else:
            raise ValueError(f"Job '{job_name}' not found.")
    
    def get_job_names(self):
        return list(self.jobs.keys())

# Factory to make jobs
class JobFactory:

    # Predefined cron jobs
    __10_min = '*/10 * * * *'
    __30_min = '*/30 * * * *'
    __60_min = '0 * * * *'

    types = {'10': __10_min, '30': __30_min, '60': __60_min}

    def __init__(self, cron_job):
        self.cron_job = cron_job
    
    def create_job(self, name, type):
        command = 'python ./Jobs/' + str(name) + '.py'
        self.cron_job.add_job('job1', command, self.types[type])  # run at 1:00am every day