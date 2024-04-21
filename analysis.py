import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
data = pd.read_csv('PC1 results.csv')

# Function to create the first plot
def plot_relevance_vs_influence(platform_filter):
    # Convert the daily social media usage column to a numeric type
    usage_map = {'Less than 1 hour': 0.5, '1-2 hours': 1.5, '3-4 hours': 3.5, 'More than 4 hours': 5}
    data['How many hours per day do you typically spend on social media?'] = data['How many hours per day do you typically spend on social media?'].map(usage_map)

    # Filter the data based on the platform filter
    if platform_filter:
        filtered_data = data[data['Which social media platforms do you use most frequently?'].apply(lambda x: any(p in x for p in platform_filter))]
    else:
        filtered_data = data.copy()

    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(filtered_data['On a scale of 1-5, how relevant do you find the ads you see on social media to your interests and needs?'],
                         filtered_data['On a scale of 1-5, how significant was the influence of social media on your decision to purchase the product?'],
                         c=filtered_data['How many hours per day do you typically spend on social media?'],
                         cmap='viridis')
    cbar = ax.figure.colorbar(scatter, ax=ax)
    cbar.ax.set_ylabel('Daily Social Media Usage (Hours)', rotation=-90, va="bottom")
    ax.set_xlabel('Relevance of Social Media Ads')
    ax.set_ylabel('Influence of Social Media on Purchase Decision')
    ax.set_title('Social Media Usage vs. Ad Relevance and Purchase Influence')
    return fig

# Function to create the second plot
def plot_ad_type_vs_age(platform_filter):
    filtered_data = data[data['Which social media platforms do you use most frequently?'].apply(lambda x: any(p in x for p in platform_filter))]
    fig, ax = plt.subplots(figsize=(10, 6))
    ad_types_by_age = filtered_data.groupby('Age?')['What type of social media ads are you most likely to interact with?'].apply(lambda x: x.str.get_dummies(sep=';').sum() / len(x))
    ad_types_by_age.T.plot(kind='pie', subplots=True, ax=ax, autopct='%1.1f%%', startangle=90)
    ax.set_title(f'Ad Type vs. Age for Platform(s): {", ".join(platform_filter)}')
    return fig

# Function to create the third plot
def plot_gender_vs_usage(platform_filter):
    filtered_data = data[data['Which social media platforms do you use most frequently?'].apply(lambda x: any(p in x for p in platform_filter))]
    fig, ax = plt.subplots(figsize=(10, 6))
    usage_by_gender = filtered_data.groupby('Gender?')['How many hours per day do you typically spend on social media?'].value_counts(normalize=True).unstack('Gender?')
    usage_by_gender.plot(kind='bar', ax=ax)
    ax.set_xlabel('Daily Social Media Usage (Hours)')
    ax.set_ylabel('Proportion')
    ax.set_title(f'Gender vs. Daily Social Media Usage for Platform(s): {", ".join(platform_filter)}')
    return fig

# Function to create the fourth plot
def plot_impulse_purchase_vs_age(platform_filter):
    filtered_data = data[data['Which social media platforms do you use most frequently?'].apply(lambda x: any(p in x for p in platform_filter))]
    fig, ax = plt.subplots(figsize=(10, 6))
    impulse_purchase_by_age = filtered_data.groupby('Age?')['Have you ever made an impulse purchase because of a social media ad?'].value_counts(normalize=True).unstack()
    impulse_purchase_by_age.plot(kind='bar', ax=ax)
    ax.set_xlabel('Age')
    ax.set_ylabel('Proportion')
    ax.set_title(f'Impulse Purchase vs. Age for Platform(s): {", ".join(platform_filter)}')
    return fig

# Function to create the fifth plot
def plot_impulse_purchase_vs_usage(platform_filter):
    filtered_data = data[data['Which social media platforms do you use most frequently?'].apply(lambda x: any(p in x for p in platform_filter))]
    fig, ax = plt.subplots(figsize=(10, 6))
    impulse_purchase_by_usage = filtered_data.groupby('How many hours per day do you typically spend on social media?')['Have you ever made an impulse purchase because of a social media ad?'].value_counts(normalize=True).unstack()
    impulse_purchase_by_usage.plot(kind='pie', subplots=True, ax=ax, autopct='%1.1f%%', startangle=90)
    ax.set_title(f'Impulse Purchase vs. Daily Social Media Usage for Platform(s): {", ".join(platform_filter)}')
    return fig

# Streamlit app
def main():
    st.title("Social Media Ads Analysis")

    # Plot 1: Relevance vs. Influence
    st.subheader("Relevance of Social Media Ads vs. Influence on Purchase Decision")
    platform_filter = st.multiselect("Select Social Media Platforms", data['Which social media platforms do you use most frequently?'].str.get_dummies().columns)

    if platform_filter:
        fig = plot_relevance_vs_influence(platform_filter)
        st.pyplot(fig)

        # Plot 2: Ad Type vs. Age
        st.subheader("Ad Type vs. Age")
        fig = plot_ad_type_vs_age(platform_filter)
        st.pyplot(fig)

        # Plot 3: Gender vs. Daily Social Media Usage
        st.subheader("Gender vs. Daily Social Media Usage")
        fig = plot_gender_vs_usage(platform_filter)
        st.pyplot(fig)

        # Plot 4: Impulse Purchase vs. Age
        st.subheader("Impulse Purchase vs. Age")
        fig = plot_impulse_purchase_vs_age(platform_filter)
        st.pyplot(fig)

        # Plot 5: Impulse Purchase vs. Daily Social Media Usage
        st.subheader("Impulse Purchase vs. Daily Social Media Usage")
        fig = plot_impulse_purchase_vs_usage(platform_filter)
        st.pyplot(fig)

if __name__ == "__main__":
    main()
