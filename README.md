# SEMapper
A tool to map GPS points input in a Discord message board or from a static file. 

Creates a Plotly and Matplotlib index.html file, which can be upload to a website.


To build the tool you will need to be running Python 3.8.


1) Clone the Repository 
    
      
        git clone https://github.com/Makr91/SEMapper
        
2) Navigate inside of the Directory
    
        
        cd SEMapper
        
3) Create a Python Virtual Environment

        
        python3.8 -m venv .
        
4) Activate the Virtual Environment

          
        source bin/activate
        
5) Edit the conf.yaml file with your Discord Developer Logins and the Factions Name
        
         
        nano conf.yaml
         
6) Install all the require pip modules
        
         
        pip3 install -r requirements.txt
          
7) Run the Application
        
          
        python3.8 plot.py
          

Once it is up and running you can then paste any set of stock GPS coordinates from Space engineers and it will map it. 

Any string starting with GPS: will be evaluated to be a proper GPS string. Faction, Nation, and Sector Tags can be appened. This will be documented later.

GPS:Stormcatz #1:2388385.42:-1102126.01:-3710825.53:#75C9F1::::

![image](https://user-images.githubusercontent.com/11012628/122722314-29211400-d237-11eb-8841-0dcf5edc1c69.png)


To Generate a Map with the currently collected list of cooridnates run:

GG:

![image](https://user-images.githubusercontent.com/11012628/122722741-b49aa500-d237-11eb-9202-1866fde22c30.png)

