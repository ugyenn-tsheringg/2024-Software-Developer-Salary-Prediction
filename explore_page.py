import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_category(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else: 
            categorical_map[categories.index[i]] = 'Other'

    return categorical_map

def clean_experience(x):
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

def clean_educationlevel(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x:
        return 'Professional degree'
    return 'Less than a Bachelors'


# @st.cache

def load_data():
    df = pd.read_csv("dataset/survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    df = df.rename({"ConvertedCompYearly":"Salary"}, axis=1)
    df = df[df["Salary"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed, full-time"]
    df = df.drop("Employment", axis=1)
    country_map = shorten_category(df['Country'].value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)
    df = df[df["Salary"] <= 250000]
    df = df[df["Salary"] >= 100000]
    df = df[df["Country"] != 'Other']
    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_experience)
    df['EdLevel'] = df['EdLevel'].apply(clean_educationlevel)

    return df

df = load_data()

def show_explore_page():
    st.title("Explore Developers Salaries")
    st.write("""### Stack Overflow Developer Survey""")

    data = df["Country"].value_counts()

    # Get the top 4 countries
    top_countries = data.nlargest(5).index

    fig1, ax1 = plt.subplots()

    # Custom autopct function to display percentages only for the top 4 countries
    def custom_autopct(pct):
        return ('%1.1f%%' % pct) if pct > (data[top_countries[-1]] / data.sum() * 100) else ''

    # Plot the pie chart with all countries but show percentages only for the top 4
    ax1.pie(data, labels=None, autopct=custom_autopct, startangle=90)
    ax1.axis("equal")

    # Add the legend on the right side of the pie chart
    ax1.legend(data.index, title="Countries", loc="center left", bbox_to_anchor=(1, 0.5))

    # fig1, ax1 = plt.subplots()
    # ax1.pie(data, labels=None, autopct="%1.1f%%", startangle=90)
    # ax1.axis("equal")

    # # Add the legend on the right side of the pie chart
    # ax1.legend(data.index, title="Countries", loc="center left", bbox_to_anchor=(1, 0.5))

    st.write("""#### Number of Data from different countries""")
    st.pyplot(fig1)

    st.write(
        """
        #### Mean Salary Based on Country"""
    )
    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(
        """
        ### Mean Salary Based on Experience"""
    )

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)