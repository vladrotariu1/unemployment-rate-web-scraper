from bs4 import BeautifulSoup
import requests
import pandas as pd


def get_data_sets_links(relative_link):
    link = "https://data.gov.ro" + relative_link

    html_text = requests \
        .get(link) \
        .text

    soup = BeautifulSoup(html_text, 'lxml')
    data_sets_section = soup.find('section', id='dataset-resources')
    data_sets_links = data_sets_section.find_all('a', class_='resource-url-analytics')

    return data_sets_links[0]['href'], data_sets_links[3]['href']


def prepare_total_unemployment_data(total_unemployment_data_set_link):
    raw_df = pd.read_csv(total_unemployment_data_set_link)

    final_df = raw_df\
        .drop(raw_df.columns[[4, 5, 6, 7, 8, 9]], axis=1)\
        .dropna()

    return final_df


def prepare_total_unemployment_by_age_data(total_unemployment_by_age_data_set_link):
    raw_df = pd.read_csv(total_unemployment_by_age_data_set_link)

    final_df = raw_df \
        .drop(raw_df.columns[[1]], axis=1) \
        .dropna()

    return final_df


def get_monthly_data(relative_link):
    total_unemployment_data_set_link, \
    total_unemployment_by_age_data_set_link = get_data_sets_links(relative_link)

    total_unemployment_df = prepare_total_unemployment_data(total_unemployment_data_set_link)
    total_unemployment_by_age_df = prepare_total_unemployment_by_age_data(total_unemployment_by_age_data_set_link)
    final_df = total_unemployment_df \
        .join(total_unemployment_by_age_df.drop(total_unemployment_by_age_df.columns[[0]], axis=1))

    return final_df


def get_counties_list():
    df = get_monthly_data('februarie', 2020)
    counties_list = df[df.columns[0]]

    return counties_list


def get_last_n_monthly_updates(n):
    html_text = requests \
        .get('https://data.gov.ro/dataset?tags=somaj&q=somaj&sort=metadata_modified+desc&res_format=.csv&page=1') \
        .text

    soup = BeautifulSoup(html_text, 'lxml')
    data_sets_html_headings = soup.find_all('h3', class_='dataset-heading')
    data_sets_dates = [x.find('a').text.split(' ')[-2:] for x in data_sets_html_headings]

    return data_sets_dates[0:n]


def get_last_n_monthly_updates_links(n):
    html_text = requests \
        .get('https://data.gov.ro/dataset?tags=somaj&q=somaj&sort=metadata_modified+desc&res_format=.csv&page=1') \
        .text

    soup = BeautifulSoup(html_text, 'lxml')
    data_sets_html_headings = soup.find_all('h3', class_='dataset-heading')
    data_sets_links = [x.find('a')['href'] for x in data_sets_html_headings]

    return data_sets_links[0:n]
