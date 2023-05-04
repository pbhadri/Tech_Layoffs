import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache
def load_data(): #Function that loads data, puts it in a dataframe, and converts the date 
    data = pd.read_csv('tech_layoffs.csv', index_col='index')
    return data

# Load the dataset
def load_data():
    data = pd.read_csv('tech_layoffs.csv')
    data['Date'] = pd.to_datetime(data['reported_date'])
    data['Month'] = data['Date'].dt.month
    data['Year'] = data['Date'].dt.year
    return data


data = load_data()

df = load_data()
page = st.sidebar.radio("Select a Visualization Below to View", ('About the Data','Data Overview','Total layoffs by company','layoffs by industry','layoffs by location')) 

if page == 'About the Data':
    st.header('Post Pandemic Tech Layoff ')
    st.header('About the Data')
    st.write('ITCS 4122/5122 - Visual Analytics, Spring 2023')
    st.write('Project Team 04 : Pallavi Bhadri, Sushma Narne, Betty Bangali')

    st.subheader('Project Overview')
    
    st.write(
        " Following the recent layoffs taking place in the USA, this Visualization shows a depiction from a set of collected  data that shows the layoffs that occured between 2022- 2023. For more insght to this data see please refer to (https://www.kaggle.com/datasets/salimwid/technology-company-layoffs-20222023-data), [Tech Layoffs in the USA]  " + 
        "\n \n This data set is pulled from different sources as well as direct company websites including but not limited to: TechCrunch, GeekWire, CNBC, World Street Journal, Linkedin, Bloomberg and Business Insider. " + "This data set has been collected from over 450 companies." 
    )
    st.image('images/layoffs.png',use_column_width='Auto')
    
    with st.expander("Dataset Attributes"):
        st.write(
            'The tech_layoffs dataset consisted of over 450 companies from Mid-2022-2023. For this project, we chose to focus on the ' +
            'following key attributes:'
        )
        data_col1, data_col2,= st.columns(2)
        with data_col1:
            """
                Key Categorical Attributes
                * Company
                * Industry
                * location
                * status
                
                
            """

        with data_col2:
            """
                Key Quantitative Attributes
                * Total layoffs
                * Impacted workforce percentage
                * Status/Sectors
            """
  
    with st.expander("Target Demographic"):
        st.write(' The information would be most useful for indivduals to see what Industry sector are mostly impacted.'
        )
    with st.expander("Application Implementation"):
        st.write('Streamlit, the web framework we chose for our project, made it simple for us to create a web page. ' +
                    ' Altair was also implemented to construct the charts and graphs for our visualizations ' +
                    'so that the dataset could be interacted with '+ 
                    'Additionally, we use python, Pandas and Numpy to analyze the dataset'
                )  
#Sector= df.status        
# Data overview page
if page == 'Data Overview':
    st.header('Data Overview ')
    #st.write( ' Please use selector on the sidebar for this page')
    #st.sidebar(
    Sector = st.multiselect(label='Select Sector',
                            options=df['status'].unique(),
                            default=df['status'].unique())
Sector= df.status   
df.query('status == @Sector')

total_layoffs = float(df['total_layoffs'].sum())
total_impacted = float(df['impacted_workforce_percentage'].sum())

Layoffs,Impacted = st.columns(2,gap='large')

with Layoffs:
    st.image('images/workforce.png',use_column_width='Auto')
    st.metric(label = 'Total Layoffs', value=(total_layoffs))
with Impacted :
    st.image('images/production.png',use_column_width='Auto')
    st.metric(label = 'Total Impactec percentage', value=(total_impacted))
               
    
# Filter the data by year
st.sidebar.header("Filter by Year")
year = st.sidebar.slider("Year", min_value=2022, max_value=2023, value=2022, step=1)
filtered_data = data[data["Year"] == year]

# Display the total layoffs by company
if page == 'Total layoffs by company':
    
    st.header('Total Layoffs by Company')
    company_layoffs = filtered_data.groupby("company")["total_layoffs"].sum().sort_values(ascending=False).reset_index()
    fig1 = px.bar(company_layoffs, x='company', y='total_layoffs', title='Total Layoffs by Company', labels={'total_layoffs': 'Total Layoffs', 'company': 'Company'})
    fig1.update_traces(hovertemplate='<b>Company:</b> %{x}<br><b>Total Layoffs:</b> %{y}')
    fig1.update_layout(hoverlabel=dict(bgcolor="rgb(100, 149, 237)", font_size=16, font_family="Arial"))
    st.plotly_chart(fig1)

# Display the layoffs by industry
if page == 'layoffs by industry':
    
    st.header('Layoffs by Industry')
    industry_layoffs = filtered_data.groupby("industry")["total_layoffs"].sum().sort_values(ascending=False).reset_index()
    fig2 = px.bar(industry_layoffs, x='industry', y='total_layoffs', title='Layoffs by Industry', labels={'total_layoffs': 'Total Layoffs', 'industry': 'Industry'})
    fig2.update_traces(hovertemplate='<b>Industry:</b> %{x}<br><b>Total Layoffs:</b> %{y}')
    fig2.update_layout(hoverlabel=dict(bgcolor="rgb(100, 149, 237)", font_size=16, font_family="Arial"))
    st.plotly_chart(fig2)

# Display layoffs by headquarter_location
if page == 'layoffs by location':
    
    st.header('Layoffs by Headquarter Location')
    location_layoffs = filtered_data.groupby("headquarter_location")["total_layoffs"].sum().sort_values(ascending=False).reset_index()
    fig3 = px.bar(location_layoffs, x='headquarter_location', y='total_layoffs', title='Layoffs by Headquarter Location', labels={'total_layoffs': 'Total Layoffs', 'headquarter_location': 'Headquarter Location'})
    fig3.update_traces(hovertemplate='<b>Headquarter Location:</b> %{x}<br><b>Total Layoffs:</b> %{y}')
    fig3.update_layout(hoverlabel=dict(bgcolor="rgb(100, 149, 237)", font_size=16, font_family="Arial"))
    st.plotly_chart(fig3)
