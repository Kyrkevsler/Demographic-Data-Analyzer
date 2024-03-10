from ucimlrepo import fetch_ucirepo
import pandas as pd
import numpy as np

def calculate_demographic_data(print_data= True):
    ''' This function returns the demographic analytics on the 1994 Census database '''

    # Fetch dataset from repo
    adult = fetch_ucirepo(id=2)
    
    # Data (as pandas dataframes)
    x = adult.data.features
    y = adult.data.targets
    
    # Convert features and salary into pandas DataFrame
    census_df = pd.DataFrame(data=x)
    census_df['salary'] = y
    
    # Count all the different races in the dataset
    race_counts = census_df['race'].value_counts()
    
    # Find the average age of men
    avg_age_men = round(census_df.loc[census_df['sex'] == 'Male', 'age'].mean(), 1)
    
    #Find the percentage of people who have a Bachelor's degree
    percentage_bachelors = round(census_df.loc[census_df['education'] == 'Bachelors', 'education'].count() / census_df.shape[0] * 100, 1)
    
    # Find the percentage of people with advanced education (Bachelors, Masters, or Doctorate) who make more than 50K.
    adv_education = census_df[census_df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]
    more_than_50k = adv_education[adv_education['salary'] == '>50K']
    percentage_more_than_50k = round((len(more_than_50k) / len(adv_education)) * 100, 1)
    
    # Find the percentage of people without advanced education who make more than 50k
    no_adv_education = census_df[~census_df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]
    more_than_50k_not_adv = no_adv_education[no_adv_education['salary'] == '>50K']
    not_adv_percentage_more_than_50k = round((len(more_than_50k_not_adv) / len(no_adv_education)) * 100, 1)
    
    # Find the minimum number of hours a person works per week.
    min_work_hours = census_df['hours-per-week'].min()
    
    # Find the percentage of the people who work the minimum number of hours per week with a salary of more than 50K.
    percentage_min_hour = census_df.groupby('hours-per-week')['salary'].apply(lambda x: (x == '>50K').mean() * 100)
    percentage_more_than_50k_min_hours = round(percentage_min_hour[min_work_hours], 1)
    
    # Find the country with the highest percentage of people that earn >50K and its percentage.
    country_counts = census_df.groupby('native-country')['salary'].apply(lambda x: (x == '>50K').mean() * 100)
    highest_earning_country = country_counts.idxmax()
    highest_earning_country_percentage = round(country_counts.max(), 1)
    
    # Filter the dataframe for individuals earning >50K and from India
    indian_high_income = census_df[(census_df['salary'] == '>50K') & (census_df['native-country'] == 'India')]
    
    # Group the filtered dataframe by occupation, count, and then find the most popular occupation.
    most_popular_occupation = indian_high_income['occupation'].value_counts().idxmax() 

    # Do not Modify code below:
    
    if print_data:
        print("Number of each race:\n", race_counts)
        print("Average age of men:", avg_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {percentage_more_than_50k}%")
        print(f"Percentage without higher education that earn >50K: {not_adv_percentage_more_than_50k}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {percentage_more_than_50k_min_hours}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", most_popular_occupation)
    
    return {
        'race_count': race_counts,
        'average_age_men': float("{:.1f}".format(avg_age_men)),
        'percentage_bachelors': float("{:.1f}".format(percentage_bachelors)),
        'higher_education_rich': float("{:.1f}".format(percentage_more_than_50k)),
        'lower_education_rich': float("{:.1f}".format(not_adv_percentage_more_than_50k)),
        'min_work_hours': min_work_hours,
        'rich_percentage': percentage_more_than_50k_min_hours,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage': float("{:.1f}".format(highest_earning_country_percentage)),
        'top_IN_occupation': most_popular_occupation
    }