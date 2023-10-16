if __name__ == "__main__":
    source = """\
\nimport pandas as pd\n\n# read csv files\ndf_aaa = pd.read_csv('AAA.csv')\ndf_bbb = pd.read_csv('BBB.csv')\n\n# merge two dataframes\ndf = pd.merge(df_aaa, df_bbb, on='col1')\n\n# update col5\ndf['col5'] = df['col2']\n\n# write to csv file\ndf.to_csv('update.csv', index=False)\n \
"""
    
    exec(source)
    