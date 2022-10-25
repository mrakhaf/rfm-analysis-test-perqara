import pandas as pd
import matplotlib.pyplot as plt

def main():
    new_customer = {
        'customer_unique_id': '123456789',
        'recency': 10,
        'frequency': 10,
        'monetary': 1000
    }
    data = load_data()
    data = input_data_and_save(new_customer, data)
    data = process_data(data)
    if input_data_summarize(data, new_customer['customer_unique_id']).empty:
        print('Customer not found')
    else:
        print('Customer Id', new_customer['customer_unique_id'], 'at segment', input_data_summarize(data, new_customer['customer_unique_id'])['RFMLabel'].values[0])
    visualize_data(data)

def load_data():
    df = pd.read_csv('data_rfm/rfm_data.csv')
    return df

def input_data_and_save(new_customer, data):
    customer_unique_id, recency, frequency, monetary = new_customer.values()
    data = data.append({'customer_unique_id': customer_unique_id, 'recency': recency, 'frequency': frequency, 'monetary': monetary}, ignore_index=True)
    data.to_csv('data_rfm/rfm_data.csv', index=False)
    return data

def RScore(x, p, d):
    if x <= d[p][0.25]:
        return 4
    elif x <= d[p][0.50]:
        return 3
    elif x <= d[p][0.75]:
        return 2
    else:
        return 1

def FMScore(x, p, d):
    if x <= d[p][0.25]:
        return 1
    elif x <= d[p][0.50]:
        return 2
    elif x <= d[p][0.75]:
        return 3
    else:
        return 4

def rfm_label(df):
    if df['RFMScore'] >= 10:
        return 'Top Customers'
    elif ((df['RFMScore'] >= 8) and (df['RFMScore'] < 10)):
        return 'High Value Customers'
    elif ((df['RFMScore'] >= 6) and (df['RFMScore'] < 8)):
        return 'Medium Value Customers'
    elif ((df['RFMScore'] >= 4) and (df['RFMScore'] < 6)):
        return 'Low Value Customers'
    elif (df['RFMScore'] < 4):
        return 'Lost Customer'

def process_data(data):
    quantiles = data.quantile(q=[0.25, 0.5, 0.75])
    quantiles = quantiles.to_dict()

    data['r_quartile'] = data['recency'].apply(RScore, args=('recency', quantiles,))
    data['f_quartile'] = data['frequency'].apply(FMScore, args=('frequency', quantiles,))
    data['m_quartile'] = data['monetary'].apply(FMScore, args=('monetary', quantiles,))

    data['RFMScoreString'] = data.r_quartile.map(str) \
                            + data.f_quartile.map(str) \
                            + data.m_quartile.map(str)

    data['RFMScore'] = data.r_quartile + data.f_quartile + data.m_quartile

    data['RFMLabel'] = data.apply(rfm_label, axis=1)
    
    return data  

def visualize_data(data):
    data['RFMLabel'].value_counts().plot(kind='barh', figsize=(10, 5))
    for index, value in enumerate(data['RFMLabel'].value_counts().values):
        plt.text(value, index, str(value))
    plt.show()         

def input_data_summarize(data, customer_unique_id):
    df_rfm = data[data['customer_unique_id'] == customer_unique_id]
    return df_rfm

main()    
         
