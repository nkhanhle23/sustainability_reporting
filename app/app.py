import streamlit as st
import psycopg2
import pandas as pd

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="db-postgresql-sustainability-group-do-user-14262231-0.b.db.ondigitalocean.com",
    port=25060,
    database="defaultdb",
    user="doadmin",
    password="AVNS_xJlGYQTQBtMI5V_xcj1",
    sslmode="require"
)

# Dropdown menu options
list_industries = ['Financial Institution', 'Insurance', 'Pension Funds', 'Auditor', 'Extractive', 'Industry', 'Large Infrastructure', 'Company']
list_industries_sfdr = ['Investment firms', 'pension funds', 'asset managers', 'insurance companies', 'banks', 'venture capital funds', 'credit institutions offering portfolio management', 'financial advisors']
company_sizes = ['>500 employees', '>250 employees', '<250 employees']
listed_on_regulated_markets_options = ['Yes', 'No']
total_asset_options = ['>20Mio', '<20Mio']
net_revenue_options = ['>40Mio', '<40Mio']

# Variable selection
industry_var = st.sidebar.selectbox('Select Industry:', list_industries)
company_size_var = st.sidebar.selectbox('Select Company Size:', company_sizes)
listed_on_regulated_markets_var = st.sidebar.selectbox('Listed on Regulated Markets:', listed_on_regulated_markets_options)
total_asset_var = st.sidebar.selectbox('Select Total Asset:', total_asset_options)
net_revenue_var = st.sidebar.selectbox('Select Net Revenue:', net_revenue_options)

# Button to trigger processing
if st.sidebar.button('Go'):
    df_directives = pd.DataFrame(columns=['directive', 'start_date'])
    start_of_rep = ''

    cur = conn.cursor()

    # query the csrd description
    query_csrd_name = "SELECT csrd_name FROM csrd"
    query_csrd_description = "SELECT csrd_description FROM csrd"

    # check for csrd
    if company_size_var == '>500 employees' and (industry_var in list_industries or listed_on_regulated_markets_var == 'Yes'):
        df_directives.loc[len(df_directives)] = ['CSRD', '2025 (for 2024)']

    elif (company_size_var == '>250 employees' and total_asset_var == '>20Mio') or (company_size_var == '>250 employees' and net_revenue_var == '>40Mio') or (total_asset_var == '>20Mio' and net_revenue_var == '>40Mio'):
        df_directives.loc[len(df_directives)] = ['CSRD', '2026 (for 2025)']

    elif (company_size_var == '<250 employees' and total_asset_var == '<20Mio' and listed_on_regulated_markets_var == 'Yes'):
        df_directives.loc[len(df_directives)] = ['CSRD', '2026 (for 2025)']

    else:
        pass

    # nfdr
    if company_size_var == '>500 employees' and (industry_var in list_industries or listed_on_regulated_markets_var == 'Yes'):
        df_directives.loc[len(df_directives)] = ['NFRD', '2017 until 2025']

    # EU-Taxonomy
    if company_size_var == '>500 employees' and (industry_var in list_industries or listed_on_regulated_markets_var == 'Yes'):
        df_directives.loc[len(df_directives)] = ['EU-Taxonomy', '2022']

    # sfdr
    if industry_var in list_industries_sfdr:
        df_directives.loc[len(df_directives)] = ['SFDR Level 1', '2021']
        df_directives.loc[len(df_directives)] = ['SFDR Level 2', '2023']

    result_df = pd.DataFrame(columns=['directive', 'start_date', 'csrd_name', 'csrd_description'])

    for index, row in df_directives.iterrows():
        directive = row['directive']
        start_date = row['start_date']

        if directive == 'CSRD':
            # Query the "csrd" table
            cur.execute("SELECT csrd_name FROM csrd")
            csrd_names = cur.fetchall()

            cur.execute("SELECT csrd_description FROM csrd")
            csrd_descriptions = cur.fetchall()

            for name, description in zip(csrd_names, csrd_descriptions):
                result_df.loc[len(result_df)] = ['CSRD', start_date, name[0], description[0]]

        elif directive == 'NFRD':
            # Query the "nfrd" table
            cur.execute("SELECT nfrd_name FROM nfrd")
            nfrd_names = cur.fetchall()

            cur.execute("SELECT nfrd_description FROM nfrd")
            nfrd_descriptions = cur.fetchall()

            for name, description in zip(nfrd_names, nfrd_descriptions):
                result_df.loc[len(result_df)] = ['NFRD', start_date, name[0], description[0]]

        elif directive == 'EU-Taxonomy':
            # Query the "Eu-Taxonomy" table
            cur.execute("SELECT eu_taxonomy_name FROM eu_taxonomy")
            eu_taxonomy_names = cur.fetchall()

            cur.execute("SELECT eu_taxonomy_description FROM eu_taxonomy")
            eu_taxonomy_descriptions = cur.fetchall()

            for name, description in zip(eu_taxonomy_names, eu_taxonomy_descriptions):
                result_df.loc[len(result_df)] = ['EU-Taxonomy', start_date, name[0], description[0]]

        elif directive == 'SFDR Level 1':
            # Query the "Eu-Taxonomy" table
            cur.execute("SELECT sfdr_name FROM sfdr WHERE sfdr_name LIKE 'Level 1%'")
            sfdr_names = cur.fetchall()

            cur.execute("SELECT sfdr_description FROM sfdr WHERE sfdr_name LIKE 'Level 1%'")
            sfdr_descriptions = cur.fetchall()

            for name, description in zip(sfdr_names, sfdr_descriptions):
                result_df.loc[len(result_df)] = ['SFDR Level 1', start_date, name[0], description[0]]

        elif directive == 'SFDR Level 2':
            # Query the "Eu-Taxonomy" table
            cur.execute("SELECT sfdr_name FROM sfdr WHERE sfdr_name LIKE 'Level 2%'")
            sfdr_names = cur.fetchall()

            cur.execute("SELECT sfdr_description FROM sfdr WHERE sfdr_name LIKE 'Level 2%'")
            sfdr_descriptions = cur.fetchall()

            for name, description in zip(sfdr_names, sfdr_descriptions):
                result_df.loc[len(result_df)] = ['SFDR Level 2', start_date, name[0], description[0]]

        else:
            break

    # Close the cursor and connection
    cur.close()
    conn.close()

    # Display the result
    if result_df.empty:
        st.info('No directives applied to your company.')
    else:
        st.success('Here are the directives applied to your company:')

        directives = result_df['directive'].unique()

        for directive in directives:
            st.header(f"Directive: {directive}")

            filtered_df = result_df[result_df['directive'] == directive]
            start_dates = filtered_df['start_date'].unique()

            for start_date in start_dates:
                st.subheader(f"Start Date: {start_date}")

                filtered_data = filtered_df[filtered_df['start_date'] == start_date]

                table_data = {
                    'Name': filtered_data['csrd_name'].tolist(),
                    'Description': filtered_data['csrd_description'].tolist()
                }

                st.table(table_data)
