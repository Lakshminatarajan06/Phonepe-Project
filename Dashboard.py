# importing required libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Connecting with MySql
import mysql.connector
mydb=mysql.connector.connect(host='localhost',user='root',password='lakshmiraj')
mycursor=mydb.cursor(buffered=True)
print(mydb)

# Dashboard setup
st.set_page_config(layout='wide')
st.markdown('<h1 style="text-align: center; color: violet;">PHONEPE DATA VISUALIZATION</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: green;">DATA PERIOD: 2018-2023 (upto-Q3)</p>', unsafe_allow_html=True)


# Options setting
option = st.radio('Select your option:',('All India', 'State wise'),horizontal=True)

if option == 'All India':

    # Transaction Analysis
    type,year,quarter=st.columns(3)
    with type:
        type_1= st.selectbox("Select Type:", ('Transaction', 'User'))
    
    with year:
        year_1= st.selectbox(':violet Select Year:', ('2018','2019','2020','2021','2022','2023'))
        
    with quarter:
        quarter_1 = st.selectbox('Select Quarter:', ('1','2','3','4'))


    if type_1== 'Transaction':           
          
        col1,col2,col3=st.columns(3)
        with col1:

                st.write('<span style="color: blue; font-size: 50px;">Transaction-India</span>', unsafe_allow_html=True)
                st.write('<span style="color: blue; font-size: 20px;">All Phonepe Transaction (UPI+CARDS+WALLETS)</span>', unsafe_allow_html=True)
                query=f"SELECT sum(Transaction_count) as trans_count FROM phonepe.agg_trans where year= {year_1} and Quarter= {quarter_1};"
                mycursor.execute(query)
                result=mycursor.fetchall()
                value = result[0][0]
                st.write(f'<span style="color: Violet; font-size: 40px;">{value}</span>', unsafe_allow_html=True)

                colx,coly=st.columns(2)
                with colx:

                    st.write('Total Payment Value')
                    query=f"SELECT sum(Transaction_amount) as trans_sum FROM phonepe.agg_trans where year= {year_1} and Quarter= { quarter_1};"
                    mycursor.execute(query)
                    result_1=mycursor.fetchall()
                    value_1 = result_1[0][0]
                    st.write(f'<span style="color: Violet; font-size: 20px;">{value_1}</span>', unsafe_allow_html=True)

                with coly:
                    st.write('Avg Payment Value')
                    query=f"SELECT (SUM(Transaction_amount) / sum(Transaction_count)) AS Avg_Trans_value FROM phonepe.agg_trans WHERE Year = {year_1} AND Quarter ={quarter_1};"
                    mycursor.execute(query)
                    result_2=mycursor.fetchall()
                    value_2 = result_2[0][0]
                    st.write(f'<span style="color: Violet; font-size: 20px;">{value_2}</span>', unsafe_allow_html=True)


        with col2:

            st.write('<span style="color: green; font-size: 20px;">Categories</span>', unsafe_allow_html=True)
            query=f"SELECT Transaction_Type, sum(Transaction_amount) as trans_sum FROM phonepe.agg_trans\
                    where year={year_1} and Quarter={quarter_1}\
                    group by Transaction_Type\
                    order by trans_sum desc;"
            mycursor.execute(query)
            result_3=mycursor.fetchall()
            value_3 =pd.DataFrame(result_3,columns=['Transaction_Type','Amount'])
            df= pd.DataFrame(result_3, columns=['Transaction_Type', 'Amount'])

            # Display specific columns in a table without index column
            table_html = df[['Transaction_Type', 'Amount']].to_html(index=False)
            st.write(table_html, unsafe_allow_html=True)  

        with col3:

            col1,col2=st.columns(2)
            with col1:
                
                States=st.button("States")
                if States:
                    st.write(':violet Top 10 States')
                    query=(f"SELECT State, SUM(Transaction_amount) as Transact FROM phonepe.agg_trans where year={year_1} and Quarter={quarter_1} GROUP BY State ORDER BY Transact DESC LIMIT 10;")
                    mycursor.execute(query)
                    results=mycursor.fetchall()
                    df_state=pd.DataFrame(results,columns=['States', 'Amount'])
                    # Display specific columns in a table without index column
                    table_html = df_state[['States', 'Amount']].to_html(index=False)
                    st.write(table_html, unsafe_allow_html=True)
                    
            with col2:

                Districts=st.button("Districts")
                if Districts:
                    st.write(':violet Top 10 Districts')
                    query=(f"SELECT District, SUM(Amount) as Transact FROM phonepe.map_trans where year={year_1} and Quarter={quarter_1} GROUP BY District ORDER BY Transact DESC LIMIT 10;")
                    mycursor.execute(query)
                    result=mycursor.fetchall()
                    df_district=pd.DataFrame(result,columns=['District','Amount'])
                    table_1= df_district[['District','Amount']].to_html(index=False)
                    st.write(table_1, unsafe_allow_html=True)

        # Transaction Analysis - India Map using Geojson.
                    
        query = "SELECT State, sum(Transaction_amount) as total_trans, sum(Transaction_count) as total_count FROM phonepe.agg_trans \
                WHERE Year=%s AND Quarter=%s GROUP BY State;"
        mycursor.execute(query, (year_1, quarter_1))
        state_trans = mycursor.fetchall()
        df_state_trans = pd.DataFrame(state_trans, columns=['States', 'Transaction_amount', 'Transaction_count'],index=range(1,len(state_trans)+1))

        # Define the mapping of old state names to new state names
        state_name_mapping = {
            'andaman-&-nicobar-islands': 'Andaman & Nicobar',
            'andhra-pradesh': 'Andhra Pradesh',
            'arunachal-pradesh': 'Arunachal Pradesh',
            'assam': 'Assam',
            'bihar': 'Bihar',
            'chandigarh': 'Chandigarh',
            'chhattisgarh': 'Chhattisgarh',
            'dadra-&-nagar-haveli-&-daman-&-diu': 'Dadra and Nagar Haveli and Daman and Diu',
            'delhi': 'Delhi',
            'goa': 'Goa',
            'gujarat': 'Gujarat',
            'haryana': 'Haryana',
            'himachal-pradesh': 'Himachal Pradesh',
            'jammu-&-kashmir': 'Jammu & Kashmir',
            'jharkhand': 'Jharkhand',
            'karnataka': 'Karnataka',
            'kerala': 'Kerala',
            'ladakh': 'Ladakh',
            'lakshadweep': 'Lakshadweep',
            'madhya-pradesh': 'Madhya Pradesh',
            'maharashtra': 'Maharashtra',
            'manipur': 'Manipur',
            'meghalaya': 'Meghalaya',
            'mizoram': 'Mizoram',
            'nagaland': 'Nagaland',
            'odisha': 'Odisha',
            'puducherry': 'Puducherry',
            'punjab': 'Punjab',
            'rajasthan': 'Rajasthan',
            'sikkim': 'Sikkim',
            'tamil-nadu': 'Tamil Nadu',
            'telangana': 'Telangana',
            'tripura': 'Tripura',
            'uttar-pradesh': 'Uttar Pradesh',
            'uttarakhand': 'Uttarakhand',
            'west-bengal': 'West Bengal'
        }
        df_state_trans['States'].replace(state_name_mapping,inplace=True)

        fig_transaction = px.choropleth(
                        df_state_trans,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        color='Transaction_amount',
                        locations='States',
                        color_continuous_scale='thermal',
                        title='Transaction Amount Heatmap'
                    )

        fig_transaction.update_geos(fitbounds="locations", visible=False)
        fig_transaction.update_layout(title_font=dict(size=33), title_font_color='#6739b7', height=1000)

        # Display the plot
        st.plotly_chart(fig_transaction, use_container_width=True)

    # Users Data Analysis.
        
    elif type_1== 'User':

        column_widths = [5,10]
        col1,col2=st.columns(column_widths)
        with col1:

            st.write('<span style="color: blue; font-size: 50px;">Users-India</span>', unsafe_allow_html=True)
            st.write('<span style="color: blue; font-size: 20px;">Registered Phonepe Users</span>', unsafe_allow_html=True)

            query=f"SELECT sum(Count) as user_count FROM phonepe.agg_user\
                    where year= {year_1} and Quarter={quarter_1};"
            mycursor.execute(query)
            result_user=mycursor.fetchall()
            value_4 = result_user[0][0]
            st.write(f'<span style="color: Violet; font-size: 40px;">{value_4}</span>', unsafe_allow_html=True)

            column_widths = [5,6]
            cola,colb=st.columns(column_widths)
            with cola:
            
                States=st.button("States")
                if States:
                    st.write(':violet Top 10 States')
                    query=(f"SELECT State, SUM(count) as users FROM phonepe.agg_user where Year={year_1} and quarter= {quarter_1} GROUP BY State ORDER BY users DESC LIMIT 10;")
                    mycursor.execute(query)
                    result_user1=mycursor.fetchall()
                    df_result_user1=pd.DataFrame(result_user1,columns=['State','Users'])
                    table_6=df_result_user1[['State','Users']].to_html(index=False)
                    st.write(table_6, unsafe_allow_html=True)
        
            with colb:
                Districts=st.button("Districts")
                if Districts:
                    st.write(':violet Top 10 Districts')
                    query=(f"SELECT District, sum(Users_Count) as user_count FROM phonepe.map_user where year={year_1} and quarter={quarter_1} group by District order by user_count desc limit 10;")
                    mycursor.execute(query)
                    result_user2=mycursor.fetchall()
                    df_result_user2=pd.DataFrame(result_user2,columns=['District','Users'])
                    table_7=df_result_user2[['District','Users']].to_html(index=False)
                    st.write(table_7, unsafe_allow_html=True)
                           

        with col2:
            # Users Analysis - India Map - geojson
            query = "SELECT State, sum(Users_Count) as reg_users FROM phonepe.map_user where year=%s and Quarter=%s group by state;"
            mycursor.execute(query, (year_1, quarter_1))
            state_count = mycursor.fetchall()
            df_state_count = pd.DataFrame(state_count, columns=['States', 'Registered_Users'],index=range(1,len(state_count)+1))
            
            # Define the mapping of old state names to new state names
            state_name_mapping = {
                'andaman-&-nicobar-islands': 'Andaman & Nicobar',
                'andhra-pradesh': 'Andhra Pradesh',
                'arunachal-pradesh': 'Arunachal Pradesh',
                'assam': 'Assam',
                'bihar': 'Bihar',
                'chandigarh': 'Chandigarh',
                'chhattisgarh': 'Chhattisgarh',
                'dadra-&-nagar-haveli-&-daman-&-diu': 'Dadra and Nagar Haveli and Daman and Diu',
                'delhi': 'Delhi',
                'goa': 'Goa',
                'gujarat': 'Gujarat',
                'haryana': 'Haryana',
                'himachal-pradesh': 'Himachal Pradesh',
                'jammu-&-kashmir': 'Jammu & Kashmir',
                'jharkhand': 'Jharkhand',
                'karnataka': 'Karnataka',
                'kerala': 'Kerala',
                'ladakh': 'Ladakh',
                'lakshadweep': 'Lakshadweep',
                'madhya-pradesh': 'Madhya Pradesh',
                'maharashtra': 'Maharashtra',
                'manipur': 'Manipur',
                'meghalaya': 'Meghalaya',
                'mizoram': 'Mizoram',
                'nagaland': 'Nagaland',
                'odisha': 'Odisha',
                'puducherry': 'Puducherry',
                'punjab': 'Punjab',
                'rajasthan': 'Rajasthan',
                'sikkim': 'Sikkim',
                'tamil-nadu': 'Tamil Nadu',
                'telangana': 'Telangana',
                'tripura': 'Tripura',
                'uttar-pradesh': 'Uttar Pradesh',
                'uttarakhand': 'Uttarakhand',
                'west-bengal': 'West Bengal'
            }

            df_state_count['States'].replace(state_name_mapping,inplace=True)

            fig_user = px.choropleth(
                            df_state_count,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            color='Registered_Users',
                            locations='States',
                            color_continuous_scale='plasma',
                            # color_continuous_scale='thermal',
                            title='Registered Phonepe Users'
                        )
            fig_user.update_geos(fitbounds="locations", visible=False)
            fig_user.update_layout(title_font=dict(size=33), title_font_color='#6739b7', height=1000)

            # Display the plot
            st.plotly_chart(fig_user, use_container_width=True)

# Data Analysis on Statewise - option =2
elif option == 'State wise':

    
    State_1 = st.selectbox("Choose State:", ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam', 'bihar', \
            'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', \
            'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh', 'maharashtra', 'manipur', \
            'meghalaya', 'mizoram', 'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', \
            'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'))


    # Selectbox
    type,year,quarter=st.columns(3)
    with type:
        type_2= st.selectbox("Select Type:", ('Transaction', 'User'),key=type)
    
    with year:
        year_1= st.selectbox('Select Year', ('2018','2019','2020','2021','2022','2023'),key=year)

    with quarter:
        quarter_1 = st.selectbox('Select Quarter', ('1','2','3','4'),key=quarter)

    if type_2== 'Transaction':
        
        column_widths = [8, 10,10]
        col1,col2,col3=st.columns(column_widths)
        with col1:

            st.write(f'<span style="color: blue; font-size: 25px;">Transaction-{State_1}</span>', unsafe_allow_html=True)
            st.write('<span style="color: blue; font-size: 15px;">All Phonepe Transaction (UPI+CARDS+WALLETS)</span>', unsafe_allow_html=True)

            query=f"SELECT SUM(Count) AS total_trans FROM phonepe.map_trans WHERE year = {year_1} AND Quarter = {quarter_1} AND State = '{State_1}';"
            mycursor.execute(query)
            result_5=mycursor.fetchall()
            value_5 = result_5[0][0]
            st.write(f'<span style="color: Violet; font-size: 40px;">{value_5}</span>', unsafe_allow_html=True)

            st.write('Total Payment Value')
            query=f"SELECT sum(Amount) as total_trans FROM phonepe.map_trans where year= {year_1} and Quarter= { quarter_1} and State='{State_1}';"  
            mycursor.execute(query)
            result_6=mycursor.fetchall()
            value_6 = result_6[0][0]
            st.write(f'<span style="color: Violet; font-size: 20px;">{value_6}</span>', unsafe_allow_html=True)

        
            st.write('Avg Payment Value')
            query=f"SELECT (sum(Amount)/sum(Count)) as avg_trans FROM phonepe.map_trans where year={year_1} and Quarter={quarter_1} and State='{State_1}';"
            mycursor.execute(query)
            result_7=mycursor.fetchall()
            value_7 = result_7[0][0]
            st.write(f'<span style="color: Violet; font-size: 20px;">{value_7}</span>', unsafe_allow_html=True)

        with col2:

            st.write('<span style="color: green; font-size: 20px;">Categories</span>', unsafe_allow_html=True)
            query=f"SELECT Transaction_Type, sum(Transaction_amount) as Trans_sum FROM phonepe.agg_trans where Year={year_1} and Quarter={quarter_1} and State='{State_1}'\
                    group by Transaction_Type\
                    order by Trans_sum desc;"
            mycursor.execute(query)
            result_8=mycursor.fetchall()
            value_8 =pd.DataFrame(result_8,columns=['Transaction Type','Amount'])
            table_2= value_8[['Transaction Type','Amount']].to_html(index=False)
            st.write(table_2,unsafe_allow_html=True)


        with col3:

            Districts=st.button("Districts")
                
            st.write(':violet Top 10 Districts')
            query=(f"SELECT District, SUM(Amount) as Transact FROM phonepe.map_trans WHERE Year={year_1} and Quarter={quarter_1} and State='{State_1}' GROUP BY District ORDER BY Transact DESC LIMIT 10;")
            mycursor.execute(query)
            result=mycursor.fetchall()
            df_result=pd.DataFrame(result,columns=['District','Amount'])
            table_3=df_result[['District','Amount']].to_html(index=False)
            st.write(table_3,unsafe_allow_html=True)

    elif type_2== 'User':

        col1,col2,col3=st.columns(3)
        with col1:

            st.write(f'<span style="color: blue; font-size: 25px;">Users-{State_1}</span>', unsafe_allow_html=True)
            st.write('<span style="color: blue; font-size: 15px;">Registered Phonepe Users </span>', unsafe_allow_html=True)
            query=f"SELECT sum(Users_Count) as total_users FROM phonepe.map_user where year={year_1} and Quarter={quarter_1} and State='{State_1}';"
            mycursor.execute(query)
            result_user=mycursor.fetchall()
            value_9 = result_user[0][0]
            st.write(f'<span style="color: Violet; font-size: 40px;">{value_9}</span>', unsafe_allow_html=True)

        with col2:
    
            Districts=st.button("Districts")             
            st.write(':violet Top 10 Districts')
            query=(f"SELECT District, sum(Users_Count) as total_user FROM phonepe.map_user where year={year_1} and Quarter={quarter_1} and State='{State_1}'\
                    group by District\
                    order by total_user desc limit 10;")
            mycursor.execute(query)
            result=mycursor.fetchall()
            df_result=pd.DataFrame(result,columns=['District','Users'])
            table_4=df_result[['District','Users']].to_html(index=False)
            st.write(table_4,unsafe_allow_html=True)

        with col3:

            Mobile=st.button("Mobile-Brand")         
            st.write(':violet Mobile Brands')
            query=(f"SELECT User_Brand, Percentage FROM phonepe.agg_user where year={year_1} and Quarter={quarter_1} and State='{State_1}';")
            mycursor.execute(query)
            result_1=mycursor.fetchall()
            df_result1=pd.DataFrame(result_1,columns=['Brand','Contribution'])
            table_5=df_result1[['Brand','Contribution']].to_html(index=False)
            st.write(table_5,unsafe_allow_html=True)
            


       

        

    