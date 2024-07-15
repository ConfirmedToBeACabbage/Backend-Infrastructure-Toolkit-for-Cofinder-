# Abstract
This is simply the area where we are composing out backend-db. The reason for using docker-compose for this task is so that we can easily setup the database on restart. 

# How to | DEV
To actually run this, you have to make sure you have docker installed on your system, which will give you the CLI commands. Whether this is Linux or Windows. Make sure that you also turned on virtualization on your system. This is usually CPU virtualization, and is an option found in your BIOS.   
  
For more assistance on that, check your systems specified motherboard model and search up the BIOS associated. Then lookup "How do I turn on CPU virtualization with BIOS [NAME]". This can be different for every system, so this requirment is subjective.   
  
You must make sure likewise that you have PostgresSQL installed on your system. The latest installations can be found here https://www.enterprisedb.com/downloads/postgres-postgresql-downloads . This will be required, as we're using the postgres:latest image.When this image is composed and built, we will require PSQL cli commands to actually get into the database. You can only access this image properly from the postgres account, not ROOT on Linux. This is done for security reasons from the creators of the POSTGRES docker image.    

### Restart Steps:   
I've made both a batch and a bash file for Windows and Linux respectively. If the init.sql file is changed, then you must get rid of the data file first for it to actually function properly.     
  
1) Run clean.bat or clean.sh  
2) Verify data is deleted, or data/* is clean respectively for Windows vs Linux  
  
### Steps:     
1) Clone the latest files to get the latest backend-db files.   
2) Using your CLI use docker-compose up in the backend-db file location  
3) You should get in your terminal the image being built   
4) When successful, in a different terminal, use the following command to connect  
      
    psql -h localhost -p 5432 -U postgres  
  
5) Write \dt to get the database tables  
6) Write \q to quit  
7) Write docker-compose down in the same file location to actually close down the connection.   