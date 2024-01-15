import seaborn as sns
from matplotlib import pyplot as plt
from DataParser.StatementParser import *
from RDBMS.PostgreSQL import PostgreSQL


def plot_data(df: pd.DataFrame):
    charges_sum = df.groupby('category')['charge_amount'].sum()

    # Create a pie chart using Seaborn's style
    plt.figure(figsize=(8, 6))
    sns.set_palette("pastel")
    plt.pie(charges_sum, labels=charges_sum.index, autopct='%1.1f%%', startangle=140)

    # Add labels and title

    # Show the plot
    plt.show()

lp = MaxParser(r'Files/Input/MAX_AUG.xlsx')
# cp = CalOnlineParser(r'Files/Output/CAL-AUG_parsed.xlsx').get_df()
# mp = MaxParser(r'Files/Output/MAX_AUG_parsed.xlsx').get_df()
# all_df = pd.concat([lp, cp])
# all_df = pd.concat([all_df, mp]).reset_index(drop=True)
# all_df.drop(all_df.columns[0], axis=1, inplace=True)
#plot_data(lp.parse())
# leumi_parser = LeumiParser(file_path=r'Files/Input/BankLeumi_15_8_2023.xlsx')
# print(leumi_parser.parse())
#
# cal_online_parser = CalOnlineParser(file_path=r'Files/Input/CAL-AUG.xlsx')
# print(cal_online_parser.parse())
#
# max_parser = MaxParser(file_path=r'Files/Input/MAX_AUG.xlsx')
# print(max_parser.parse())

db_instance = PostgreSQL()

db_instance.add_record(table_name='transactions', new_data= {
                            'date_of_purchase': '01/01/1980',
                            'business_name': 'סתם עסק',
                            'charge_amount': 10.0,
                            'payment_type': 'עסקה רגילה',
                            'total_amount': 100.0,
                            'sha1_identifier': '45454545454545'
                            })

db_instance.close_connection()