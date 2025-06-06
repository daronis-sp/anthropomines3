
import pandas as pd
import streamlit as st
from datetime import datetime

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        return datetime.strptime(date_str, "%m/%Y")

def calculate_man_months(start_date, end_date):
    start_date = parse_date(start_date)
    end_date = parse_date(end_date)
    delta = end_date - start_date
    return delta.days / 30

def merge_periods(periods):
    if not periods:
        return 0
    periods = sorted(periods, key=lambda x: x[0])
    merged = [periods[0]]
    for current in periods[1:]:
        last = merged[-1]
        if current[0] <= last[1]:
            merged[-1] = (last[0], max(last[1], current[1]))
        else:
            merged.append(current)
    total_man_months = sum((end - start).days / 30 for start, end in merged)
    return total_man_months

def process_excel(file):
    df = pd.read_excel(file, engine='openpyxl')
    man_months = []
    for index, row in df.iterrows():
        periods = row.dropna()
        period_list = []
        for period in periods:
            start_date, end_date = period.split('-')
            period_list.append((parse_date(start_date.strip()), parse_date(end_date.strip())))
        total_man_months = merge_periods(period_list)
        man_months.append(total_man_months)
    df['Ανθρωπομήνες'] = man_months
    df.loc['Σύνολο'] = df.sum(numeric_only=True)
    return df

st.title('Υπολογισμός Ανθρωπομηνών από Excel')
uploaded_file = st.file_uploader("Ανέβασε αρχείο Excel", type=["xlsx"])

if uploaded_file is not None:
    processed_df = process_excel(uploaded_file)
    st.write(processed_df)
    processed_df.to_excel("processed_file.xlsx", index=False)
    st.download_button(label="Κατέβασε το νέο αρχείο", data=open("processed_file.xlsx", "rb"), file_name="processed_file.xlsx")
