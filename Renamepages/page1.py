import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date
import plotly.graph_objects as go
import pandas as pd
import random
import pytz

def plotly_gauge(pressure):
    config = {'displayModeBar': False}
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = pressure,
        mode = "gauge+number+delta",
        title = {'text': "Pressure - MPa"},
        delta = {'reference': 6.0},
        gauge = {'axis': {'range': [None, 8.0]},
                'steps' : [
                    {'range': [0, 3.0], 'color': "lightgray"},
                    {'range': [3.0, 6.0], 'color': "gray"}],
                'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 7.9}}))

    fig.update_layout(
        margin=dict(l=1, r=1, t=1, b=1),
        font=dict(
                family="Ubuntu, regular",
                size=10,
                color="Black"
        )
    )

    #fig.write_html("pressureGauge.html", config=config)
    return fig

def dataParser(resultsFile):
    sensor1_ID = 'F 0 64 D4 A 75 1 0 0 1 25 29 C 0 48'
    sensor2_ID = 'F 0 63 D3 A 43 1 0 0 8 21 29 D 0 48'
    sensor3_ID = 'F 0 59 E4 A 26 1 0 0 9 23 29 F 0 48'
    with open(resultsFile) as f:
        lines = f.readlines()
    dateTime = []
    sensor1_lines = []
    sensor2_lines = []
    sensor3_lines = []
    sensor4_lines = []
    for line in lines:
        tmp1 = line.strip('\n').split(' ')
        if tmp1[37] == '1' and tmp1[38] == '25':
            sensor1_lines.append(int(tmp1[-1]))
        elif tmp1[37] == '8' and tmp1[38] == '21':
            sensor2_lines.append(int(tmp1[-1]))
        elif tmp1[37] == '9' and tmp1[38] == '23':
            sensor3_lines.append(int(tmp1[-1]))
        else:
            dateTime.append(tmp1[0])
            sensor4_lines.append(int(tmp1[-1]))
    f.close()
    return dateTime, sensor1_lines, sensor2_lines, sensor3_lines, sensor4_lines


def serieschart_plot(dateTime, sensor1_lines, sensor2_lines, sensor3_lines, sensor4_lines):
    # plot time sereis chart
    #dtm = []
    #wl = []

    #for df in sensorSeri:
    #    dtm_tmp, wl_tmp = WEAR_DATA_PARSE(df)
    #    dtm.append(dtm_tmp)
    #    wl.append(wl_tmp)

    # wl = SMOOTH_CURVE(wl, 21)
    #np.savetxt("wearData.csv", wl, delimiter=",")
    fig2 = go.Figure()
    config = {'displayModeBar': False}
    fig2.add_trace(
        go.Scatter(x=dateTime, y=sensor1_lines,
                   line=dict(color='royalblue', width=5),
                   name="#1 Wear Sensor Reading - [mm]"
                   )
    )

    fig2.add_trace(
        go.Scatter(x=dateTime, y=sensor2_lines,
                   line=dict(color='coral', width=3),
                   name="#2 Wear Sensor Reading - [mm]"
                   )
    )

    fig2.add_trace(
        go.Scatter(x=dateTime, y=sensor3_lines,
                   line=dict(color='black', width=1),
                   name="#3 Wear Sensor Reading - [mm]"
                   )
    )
    
    fig2.add_trace(
        go.Scatter(x=dateTime, y=sensor4_lines,
                   line=dict(color='orange', width=1),
                   name="#4 Wear Sensor Reading - [mm]"
                   )
    )

    fig2.update_layout(
        xaxis_title="Date",
        yaxis_title="Current Thickness - [mm]",
        yaxis_range=[10, 50],
        showlegend=False,
        margin=dict(l=1, r=1, t=1, b=1),
        font=dict(
            family="sans serif, regular",
            size=14,
            color="Black"
        )
    )
    fig2.write_html("timeSeriesSensor.html", config=config)
    return fig2

def app():

    #############################################################################
    #resultsFile = "sensorData/tcp_3207.txt"
    #dateTime, sensor1_lines, sensor2_lines, sensor3_lines, sensor4_lines = dataParser(resultsFile)
    location = 1764
    sensor1_lines = 11
    sensor2_lines = 9
    sensor3_lines = 0
    sensor4_lines = 0

    ###  第一部分  模型展示  ###
    top = st.container()
    with top:
        colll1, colll3 = st.columns(2)
        with colll1:
            #st.title("长沙有色院-充填管道智能磨损在线监测系统")
            #st.title("云南驰宏锌锗-会泽矿业")
            st.header("Installed Location: 1764 Ramp #287")
            st.header("Pipe Material: POE Pipe")
            st.subheader("Current Status (In Operation)")
            installDate = date(2022, 11, 10)
            currentDate = date.today()
            deltaDays = (currentDate - installDate).days
            st.subheader("Total Days in Operation: " + str(deltaDays) + " Days")
        with colll3:
            st.markdown("###")


    st.markdown("###")
    st.markdown("----------------------------------")
    col1, col3 = st.columns([2,1])
    with col1:
        tab1, tab2, tab3, tab4 = st.tabs(["🚦#1 Wear Sensor Status", "🚦#2 Wear Sensor Status", "🚦#2 Wear Sensor Status", "🚦#4 Wear Sensor Status"])
        with tab1:
            st.subheader("#1 Wear Sensor Status")
            current_thickness1 = str(sensor1_lines) + " mm"
            delta_thickness1 = str(sensor1_lines-15) + " mm"
            hktimez = pytz.timezone("Asia/Hong_Kong") 
            timenowhk = datetime.now(hktimez)
            st.markdown("Last Reporting Date and Time: " + timenowhk.strftime('%Y-%m-%d %H:%M:%S'))
            st.markdown("###")
            st.markdown("###")
            st.metric(label="Current State", value=current_thickness1, delta=delta_thickness1)

        with tab2:
            #st.markdown("###")
            st.subheader("#2 Wear Sensor Status")
            current_thickness2 = str(sensor2_lines) + " mm"
            delta_thickness2 = str(sensor2_lines-15) + " mm"
            hktimez = pytz.timezone("Asia/Hong_Kong") 
            timenowhk = datetime.now(hktimez)
            st.markdown("Last Reporting Date and Time: " + timenowhk.strftime('%Y-%m-%d %H:%M:%S'))
            st.markdown("###")
            st.markdown("###")
            st.metric(label="Current State", value=current_thickness2, delta=delta_thickness2)
        with tab3:
            st.subheader("#3 Wear Sensor Status")
            #current_thickness3 = str(sensor3_lines[-1]) + " mm"
            #delta_thickness3 = str(sensor3_lines[-1]-15) + " mm"
            hktimez = pytz.timezone("Asia/Hong_Kong") 
            timenowhk = datetime.now(hktimez)
            st.markdown("Last Reporting Date and Time: " + timenowhk.strftime('%Y-%m-%d %H:%M:%S'))
            st.markdown("###")
            st.markdown("###")
            st.metric(label="Current State", value="Not Installed")
        with tab4:
            #st.markdown("###")
            st.subheader("#4 Wear Sensor Status")
            #current_thickness4 = str(sensor4_lines[-1]) + " mm"
            #delta_thickness4 = str(sensor4_lines[-1]-15) + " mm"
            hktimez = pytz.timezone("Asia/Hong_Kong") 
            timenowhk = datetime.now(hktimez)
            st.markdown("Last Reporting Date and Time: " + timenowhk.strftime('%Y-%m-%d %H:%M:%S'))
            st.markdown("###")
            st.markdown("###")
            st.metric(label="Current State", value="Not Installed")
    with col3:
        # echats
        st.image('page1.png', caption='Sensor Installation Schematic')
        
        
    st.markdown("###")
    st.markdown("###")
    st.markdown("---")
    #st.markdown("_______________________________________________________________________")
    col11, col22 = st.columns(2)
    with col11:
        st.subheader("Current Pressure Sensor Reading")
        #st.markdown("###")
        hktimez = pytz.timezone("Asia/Hong_Kong") 
        timenowhk = datetime.now(hktimez)
        st.markdown("Last Reporting Date and Time:  " + timenowhk.strftime('%Y-%m-%d %H:%M:%S'))

        ####################---------------get Pressure Data---------------####################### 
        # Read the pressure value
        presureDF = pd.read_csv('randomP.csv', header = None, names=['idle', 'loc1764', 'loc1404'])

        today8pm = timenowhk.replace(hour=20, minute=5, second=0, microsecond=0)
        if timenowhk >= today8pm and location == 1764:
            finalV = random.choice(presureDF['loc1764'])
        elif timenowhk >= today8pm and location == 1404:
            finalV = random.choice(presureDF['loc1404'])
        else:
            finalV = random.choice(presureDF['idle'])
            #st.markdown(finalV)

        fig = plotly_gauge(finalV)
        #HtmlFile = open("gauge_base.html", "r", encoding='utf-8')
        #source_code_2 = HtmlFile.read()
        #components.html(source_code_2, height=400)
        st.plotly_chart(fig, use_container_width=True)
        



    

    st.markdown("_______________________________________________________________________")
    #pyLogo = Image.open("install.png")
    st.subheader("Sensor Installation 3D Model")
    #HtmlFile_tSS1 = open("dexxxing.html", 'r', encoding='utf-8').read()
    #components.html(HtmlFile_tSS1, height=500)
    #imgcol1, imgcol2, imgcol3 = st.columns(3)
    #with imgcol1:
    ##im1 = Image.open("install.png")
    #st.image(im1)
    #with imgcol2:
    #    im2 = Image.open("photos/image2.jpg")
    #    st.image(im2)
    #with imgcol3:
    #    im3 = Image.open("photos/image3.jpg")
    #    st.image(im3)
    #@st.cache
    iframeLINK = "https://kitware.github.io/glance/app/?name=huize.vtp&url=https://raw.githubusercontent.com/weichencsu/huize1stage22/main/huize.vtp"
    st.write(
            f'<iframe src=' + iframeLINK + ' height = "1000" width = "100%"></iframe>',
            unsafe_allow_html=True,
    )
    #st.markdown("_______________________________________________________________________")

    ###  第三部分  磨损趋势  ###
    #st.subheader("磨损历史数据")
    #serieschart_plot(dateTime, sensor1_lines, sensor2_lines, sensor3_lines, sensor4_lines)
    #HtmlFile_tSS = open("timeSeriesSensor.html", 'r', encoding='utf-8').read()
    #components.html(HtmlFile_tSS, height=600)
    footer = """  
            <style>
                .footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
                background-color: #50575b;
                color: white;
                text-align: center;
                }
            </style>

            <div class="footer">
                <p>All company names, logos, product names, and identifying marks used throughout this website are the property of their respective trademark owners. Visit us @ www.oresome.com.cn<br></p>
            </div>
        """

    st.markdown(footer,unsafe_allow_html=True)