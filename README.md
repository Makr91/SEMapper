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


I have also begun to add support for factions, nations, sectors and other features.
