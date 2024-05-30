import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from PIL import Image

# Load company logo
logo = Image.open("LOGO2.png")

# Custom CSS for the app
st.markdown(
    """
    <style>
    .main {
        background-color: #f7f7f9;
        font-family: 'Helvetica Neue', sans-serif;
    }
    h1 {
        color: #2e3b4e;
        font-weight: 700;
    }
    .sidebar .sidebar-content {
        background-color: #ececec;
    }
    .css-1aumxhk, .css-2trqyj {
        background-color: #2e3b4e;
        color: white;
    }
    .result-good {
        color: green;
        font-weight: bold;
        font-size: 1.1em;
    }
    .result-bad {
        color: red;
        font-weight: bold;
        font-size: 1.1em;
    }
    .logo-container {
        display: flex;
        justify-content: flex-end;
        align-items: center;
    }
    .logo-container img {
        width: 120px;
    }
    .app-description {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .footer {
        text-align: center;
        margin-top: 50px;
        font-size: 0.9em;
        color: #888888;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App title and logo
st.markdown(
    """
    <div class="app-description">
        <h1>Employee Performance Dashboard</h1>
        <div class="logo-container">
            <img src="data:image/png;base64,{}" alt="Company Logo">
        </div>
    </div>
    """.format(base64.b64encode(open("LOGO2.png", "rb").read()).decode()),
    unsafe_allow_html=True
)

st.markdown("""
This app helps managers track and analyze employee performance and engagement.
* **Python libraries:** pandas, streamlit, matplotlib, seaborn
""")

# Sidebar - Upload CSV file
st.sidebar.header('Upload Your CSV Data')
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=['csv'])

# Function to load data
@st.cache_data
def load_data(file):
    data = pd.read_csv(file)
    return data

# "How to Use" button
if st.sidebar.button('How to Use'):
    st.sidebar.markdown("""
    ### How to Use
    1. **Upload CSV**: Upload a CSV file containing employee performance data.
    2. **Select Metrics**: Choose which performance metrics to visualize.
    3. **Feedback**: Provide feedback for specific employees.
    4. **Download Data**: Download the data as a CSV or Excel file.

    ### Data Structure
    The CSV file should have the following columns:
    - Employee ID: Unique identifier for each employee
    - Department: Categorization of employees into different departments
    - Region: Geographical region of the employee's work location
    - Education: Employee's educational background
    - Gender: Distribution of employees by gender
    - Recruitment Channel: Source through which employees were recruited
    - Number of Trainings: Count of training programs attended by each employee
    - Age: Age of employees
    - Previous Year Rating: Performance rating of employees from the previous year
    - Length of Service: Duration of employment with the company
    """)

# If file is uploaded, load the data
if uploaded_file is not None:
    df = load_data(uploaded_file)
    st.subheader('Employee Data')
    st.write(df.head())

    # Determine the default metrics that exist in the dataset
    default_metrics = ['Task Completion', 'Quality Score', 'Attendance', 'Engagement Score']
    available_default_metrics = [metric for metric in default_metrics if metric in df.columns]

    # Select performance metrics
    st.sidebar.header('Select Performance Metrics')
    metrics = st.sidebar.multiselect('Metrics', list(df.columns), available_default_metrics)

    # Performance Segmentation
    st.sidebar.header('Select Segments')
    segments = st.sidebar.multiselect('Segments', list(df.columns), ['Department', 'Education', 'Gender'])

    # Summary Statistics
    if st.sidebar.checkbox('Show Summary Statistics'):
        st.subheader('Summary Statistics')
        st.write(df.describe())

    # Performance Segmentation
    if segments:
        st.subheader('Performance Segmentation')
        for segment in segments:
            st.write(f"### {segment} Segmentation")
            st.write(df.groupby(segment).mean())

    # Correlation Analysis
    if st.sidebar.checkbox('Show Correlation Analysis'):
        st.subheader('Correlation Analysis')
        corr = df.corr()
        plt.figure(figsize=(12, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
        st.pyplot(plt.gcf())

    # Distribution of Performance Ratings
    ratings_column = st.sidebar.selectbox('Select Ratings Column', list(df.columns))
    if ratings_column:
        st.subheader('Distribution of Performance Ratings')
        plt.figure(figsize=(10, 6))
        sns.histplot(df[ratings_column], kde=True)
        st.pyplot(plt.gcf())

    # Detailed Analytics for Each Metric
    if metrics:
        st.subheader('Performance Metrics Visualization')
        for metric in metrics:
            plt.figure(figsize=(10, 6))
            sns.barplot(x='Employee', y=metric, data=df)
            plt.title(f'{metric} by Employee')
            plt.xticks(rotation=90)
            st.pyplot(plt.gcf())

    # Summary of Results
    st.subheader('Summary of Results')
    for metric in metrics:
        average = df[metric].mean()
        st.write(f"### {metric}")
        if average >= 75:
            st.markdown(f"<span class='result-good'>Good Performance 😊</span> (Average: {average:.2f})", unsafe_allow_html=True)
        else:
            st.markdown(f"<span class='result-bad'>Needs Improvement 😟</span> (Average: {average:.2f})", unsafe_allow_html=True)

    # Feedback Section
    st.sidebar.header('Employee Feedback')
    employee = st.sidebar.selectbox('Select Employee', df['Employee'].unique())
    feedback = st.sidebar.text_area('Feedback', 'Enter feedback here...')
    if st.sidebar.button('Submit Feedback'):
        st.write(f'Feedback for {employee}: {feedback}')
        # Here you can add code to save feedback to a database or file

    # Download data as CSV or Excel
    def filedownload(df, file_type):
        if file_type == 'CSV':
            data = df.to_csv(index=False)
        elif file_type == 'Excel':
            data = df.to_excel(index=False)
        b64 = base64.b64encode(data.encode()).decode()  # strings <-> bytes conversions
        href = f'<a href="data:file/{file_type.lower()};base64,{b64}" download="Employee_Performance.{file_type.lower()}">Download {file_type} File</a>'
        return href

    st.markdown(filedownload(df, 'CSV'), unsafe_allow_html=True)
    st.markdown(filedownload(df, 'Excel'), unsafe_allow_html=True)

else:
    st.info('Awaiting for CSV file to be uploaded.')
    if st.button('Press to use Example Data'):
        # Example data for testing
        data = {
            'Employee': ['AMAL', 'EMAD', 'OSAMA', 'FARAH'],
            'Task Completion': [80, 90, 85, 88],
            'Quality Score': [75, 82, 78, 80],
            'Attendance': [95, 90, 93, 92],
            'Engagement Score': [70, 85, 80, 75]
        }
        df = pd.DataFrame(data)
        st.write(df)

        # Automatically show analytics for example data
        st.subheader('Summary Statistics')
        st.write(df.describe())

        st.subheader('Performance Segmentation')
        for segment in ['Employee']:
            st.write(f"### {segment} Segmentation")
            st.write(df.groupby(segment).mean())

        st.subheader('Correlation Analysis')
        corr = df.corr()
        plt.figure(figsize=(12, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
        st.pyplot(plt.gcf())

        st.subheader('Distribution of Performance Ratings')
        ratings_column = 'Task Completion'
        plt.figure(figsize=(10, 6))
        sns.histplot(df[ratings_column], kde=True)
        st.pyplot(plt.gcf())

        st.subheader('Performance Metrics Visualization')
        for metric in ['Task Completion', 'Quality Score', 'Attendance', 'Engagement Score']:
            plt.figure(figsize=(10, 6))
            sns.barplot(x='Employee', y=metric, data=df)
            plt.title(f'{metric} by Employee')
            plt.xticks(rotation=90)
            st.pyplot(plt.gcf())

        # Summary of Results for example data
        st.subheader('Summary of Results')
        for metric in ['Task Completion', 'Quality Score', 'Attendance', 'Engagement Score']:
            average = df[metric].mean()
            st.write(f"### {metric}")
            if average >= 75:
                st.markdown(f"<span class='result-good'>Good Performance 😊</span> (Average: {average:.2f})", unsafe_allow_html=True)
            else:
                st.markdown(f"<span class='result-bad'>Needs Improvement 😟</span> (Average: {average:.2f})", unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div class="footer">
        <p><strong>Data Analytics Project</strong></p>
        <p>Created by: Amal Alkraimeen</p>
        <p>Email: <a href="mailto:Amall@ieee.org">Amall@ieee.org</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
