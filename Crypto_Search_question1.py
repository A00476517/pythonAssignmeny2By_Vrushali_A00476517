import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # for improved plot styling

# Setting up the aesthetics for plots using Seaborn
sns.set(style="whitegrid")

st.set_option('deprecation.showPyplotGlobalUse', False)

# Function to fetch market data for a specified cryptocurrency
def fetch_market_data(crypto_id):
    api_url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
    query_params = {
        "vs_currency": "usd",
        "days": 365,
        "x_cg_demo_api_key": "CG-TF4rSWCUx8ctAL7TiqwzYnbN"
    }
    response = requests.get(api_url, params=query_params)
    if response.status_code == 200:
        json_data = response.json()
        market_prices = json_data['prices']
        df = pd.DataFrame(market_prices, columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    else:
        st.error("Failed to fetch data")

def main():
    st.sidebar.title("Cryptocurrency Insights")

    # Fetching available cryptocurrency data
    coins_api_url = "https://api.coingecko.com/api/v3/coins/list?x_cg_demo_api_key=CG-TF4rSWCUx8ctAL7TiqwzYnbN"
    coins_response = requests.get(coins_api_url)
    coins_list = coins_response.json()
    crypto_dict = {coin['id']: coin['name'] for coin in coins_list}

    # User selects a cryptocurrency from the sidebar
    selected_crypto = st.sidebar.selectbox("Choose a cryptocurrency", options=list(crypto_dict.values()))
    crypto_id = [id for id, name in crypto_dict.items() if name == selected_crypto][0]

    # Retrieve and display market data for the selected cryptocurrency
    market_data = fetch_market_data(crypto_id)
    if market_data is not None:
        # Plotting the price data over the last year
        st.subheader(f"Price Trend for {selected_crypto}")
        plt.figure(figsize=(10, 6))
        plt.plot(market_data['timestamp'], market_data['price'], marker='', color='darkcyan', linewidth=2.5)
        plt.title(f"{selected_crypto} Price Trend Over The Last Year")
        plt.xlabel("Date")
        plt.ylabel("Price in USD")
        plt.grid(True)  # Enable grid for better readability
        st.pyplot()

        # Displaying maximum and minimum price details
        highest_price = market_data['price'].max()
        lowest_price = market_data['price'].min()
        highest_price_date = market_data.loc[market_data['price'].idxmax(), 'timestamp']
        lowest_price_date = market_data.loc[market_data['price'].idxmin(), 'timestamp']

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Highest Price:** ${highest_price:.2f}")
            st.markdown(f"**Date:** {highest_price_date.strftime('%Y-%m-%d')}")
        with col2:
            st.markdown(f"**Lowest Price:** ${lowest_price:.2f}")
            st.markdown(f"**Date:** {lowest_price_date.strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    main()
