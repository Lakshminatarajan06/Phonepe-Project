# Phonepe-Project
Data Science - Phonepe Pulse Data Visualization Project

**Phonepe Pulse**
The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With over 45% market share, PhonePe's data is representative of the country's digital payment habits. The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.

**Libraries/Modules needed for the project!**
Plotly - (To plot and visualize the data)
Pandas - (To Create a DataFrame with the scraped data)
mysql.connector - (To store and retrieve the data)
Streamlit - (To Create Graphical user Interface)
json - (To load the json files)
!git clone - (To clone the GitHub repository)
import os - (to read and write files in github)

**Workflow**

**Step 1:**
Importing the Libraries:

Importing the libraries. As I have already mentioned above the list of libraries/modules needed for the project. First we have to import all those libraries. If the libraries are not installed already use the below piece of code to install.

    !pip install ["Name of the library"]

**Step 2:**
Data extraction:

Clone the Github using scripting to fetch the data from the Phonepe pulse Github repository and store it in a suitable format such as JSON. Use the below syntax to clone the phonepe github repository into your local drive.

!git clone https://github.com/PhonePe/pulse.git

**Step 3:**

Data transformation:

In this step the JSON files that are available in the folders are converted into the readeable and understandable DataFrame format by using the for loop and iterating file by file and then finally the DataFrame is created. In order to perform this step I've used os, json and pandas packages. And finally converted the dataframe into CSV file and storing in the local drive.

path1 = "Path of the JSON files"
agg_trans_list = os.listdir(path1)

# Give any column names that you want
columns1 = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_type': [], 'Transaction_count': [],'Transaction_amount': []}

Looping through each and every folder and opening the json files appending only the required key and values and creating the dataframe.

for i in agg_state_list:
    p_i = os.path.join(path, i)
    Agg_year_list = os.listdir(p_i)
    # print(Agg_year_list)
    for j in Agg_year_list:
        p_j = os.path.join(p_i, j)
        Agg_quarter_list = os.listdir(p_j)
        # print(Agg_quarter_list)

        for k in Agg_quarter_list:
            p_k = os.path.join(p_j, k)
            # print(p_k)
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['transactionData']:
              Name=z['name']
              count=z['paymentInstruments'][0]['count']
              amount=z['paymentInstruments'][0]['amount']
              country['Transaction_type'].append(Name)
              country['Transaction_amount'].append(amount)
              country['Trasaction_count'].append(count)
              country['State'].append(i)
              country['Year'].append(j)
              country['Quarter'].append(int(k.strip('.json')))
              Agg_trans=pd.DataFrame(country)
              
****Converting the dataframe into csv file**
csv_file_path = '/content/pulse/Agg_trans.csv'

# Save the DataFrame to a CSV file without including the index
Agg_trans.to_csv(csv_file_path, index=False)

Likewise Data Transformation, Looping and converting CSV file for all Useful datas.

**Step 4:**

Database insertion:

To insert the datadrame into SQL first I've created a new database and tables using "mysql-connector-python" library in Python to connect to a MySQL database and insert the transformed data using SQL commands.

**Creating the connection between python and mysql**

import mysql.connector
mydb=mysql.connector.connect(host="localhost", username="root", password="lakshmiraj")
mycursor=mydb.cursor(buffered=True)
print(mydb)

**Creating tables**

mycursor.execute("CREATE TABLE Phonepe.Agg_trans (State VARCHAR (200), Year int(10), Quarter int(10), Transaction_Type VARCHAR (200), Transaction_count int (10), Transaction_amount bigint(25))")

**Data Insertion in table**

data=pd.read_csv(r"C:\Users\Antony\Desktop\Phonepe project\Agg_transaction.csv")

for index, row in data.iterrows():
    State=row['State']
    Year=row['Year']
    Quarter=row['Quarter']
    Transaction_Type=row['Transaction_type']
    Transaction_count=row['Trasaction_count']
    Transaction_amount=row['Transaction_amount']
    
    # print(State,Quarter)
    sql=("INSERT INTO Phonepe.agg_trans (State, Year, Quarter, Transaction_Type, Transaction_count, Transaction_amount) VALUES(%s,%s,%s,%s,%s,%s)")
    values=(State, Year, Quarter, Transaction_Type, Transaction_count, Transaction_amount)

    mycursor.execute(sql,values)
    mydb.commit()
Likewise craeting table and data insertion for useful datas.

**Step 5:**

Dashboard creation:

To create colourful and insightful dashboard I've used Plotly libraries in Python to create an interactive and visually appealing dashboard. Plotly's built-in Pie, Bar, Geo map functions are used to display the data on a charts and map and Streamlit is used to create a user-friendly interface with multiple dropdown options for users to select different facts and figures to display.

