
from cgitb import text
from oauth2client.client import AUTHORIZED_USER
import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
# import pyautogui
from PIL import Image
import plotly.figure_factory as ff
import plotly.graph_objects as go



menu_touchup="""
<style>
#MainMenu {
    visibility: hidden;
}
footer:before {
    content: 'Developer [Rajinder Singh]';    
    display: block;
    max-width: 1000px;
    margin:0px auto;
    width: 100%;
    height: 30px;
    position: center;
    text-align: center;
    padding: 5px;  
    top: 3px;
    background: #666;
    color: white;

</style>
"""




scope=['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets']



def main():
    # img=Image.open("D:\\Office\\Python\\Arvind sir\\logo.png")
    # st.image(img,width=200)
    st.markdown('<h1 style="text-align: center;">Shipment Status Tracker</h1>', unsafe_allow_html=True) 
    st.markdown('''---------------------------------------------------------------------------------------------------------''')
    st.markdown(menu_touchup,unsafe_allow_html=True)

    btn1=st.button('Track Shipment Status')

    if btn1:

    
    
        googlesheeturl='https://docs.google.com/spreadsheets/d/17EW9CAOOwmefEP4toLAubQhj7q-NgsjLRAlzCeKvIIs/edit#gid=1757221736'
        creds=ServiceAccountCredentials.from_json_keyfile_name("./keys.json",scope)
        client=gspread.authorize(creds)
        sheet=client.open_by_url(googlesheeturl)
        main_worksheet=sheet.worksheet('Sheet3')
        pasted_value_worksheet=sheet.worksheet('Sheet3')
        # worksheet=sheet.get_worksheet(0)
        # sheet_runs = sheet.get_worksheet(0)


        df=main_worksheet.get_all_values()
        df=pd.DataFrame(df,columns=['Portal','Po No','Appointment_Date','FC','Courier','Status'])

        df.drop(df.index[0],inplace=True)
        df.drop(df.index[2],inplace=True)
        df.drop(df.index[2],inplace=True)
        df=df[df['Status']!='Delivered']
        df=df[df['Status']!='Cancel']
        df=df[df['Appointment_Date']!='Pending']
        df['Appointment_Date']=pd.to_datetime(df['Appointment_Date'])
        df=df[df['Appointment_Date']<pd.to_datetime(date.today())]
        # st.write(df)

        if df.empty:
            st.write('No Shipment to track')
        else:
            st.write('Total Shipment to track: ',len(df))
            # st.table(df)
            st.write('https://api.whatsapp.com/send?phone=919811648522&text=Hi%20Mam,%20The%20Status%20has%20not%20been%20updated%20for%20the%20following%20POs%20')
#             st.table(df)
            fig=go.Figure(data=[go.Table(
                columnorder=[1,2,3,4,5,6],
                columnwidth=[250,250,250,250,250,200],
                header=dict(values=['Portal','Po No','Appointment_Date','FC','Courier','Status'],height=30,align='center',font=dict(size=15,color='white'),fill_color='#3D9970'),
                cells=dict(values=[df['Portal'],df['Po No'],df['Appointment_Date'].dt.strftime('%d-%b-%Y'),df['FC'],df['Courier'],df['Status']]))])
            fig.update_layout(width=1000,height=1500)
            st.plotly_chart(fig) 





#             time.sleep(4)
#             ss=pyautogui.screenshot()
#             img=np.array(ss)
#             img=Image.fromarray(img)
#             w,h=img.size
#             st.write(w,h)
#             img=img.crop((400,600,w-20,h-80))
#             st.image(img,width=1500)
            # for i in range(len(df)):
            #     st.write('PO No: ', df.iloc[i]['PO No']
            #     ,'\nCourier: ',df.iloc[i]['Courier']
            #     ,'\nFC: ',df.iloc[i]['FC']
            #     ,'\nAppointment Date: ',df.iloc[i]['Appointment_Date']
            #     ,'\nPortal: ',df.iloc[i]['Portal'])


if __name__ == '__main__':
    main()
