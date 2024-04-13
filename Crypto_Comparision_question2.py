import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # Enhanced graph styling

# Configuring Seaborn for better graph aesthetics
sns.set(style="whitegrid")

# Avoid deprecation warning for pyplot global use
st.set_option('deprecation.showPyplotGlobalUse', False)

# Function to retrieve cryptocurrency market data from the CoinGecko API
def get_crypto_data(crypto_id, days):
    base_url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
        "x_cg_demo_api_key": "CG-TF4rSWCUx8ctAL7TiqwzYnbN"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        prices_data = response.json()['prices']
        data_frame = pd.DataFrame(prices_data, columns=['timestamp', 'price'])
        data_frame['timestamp'] = pd.to_datetime(data_frame['timestamp'], unit='ms')
        return data_frame
    else:
        st.error(f"Failed to retrieve data: {response.status_code}")
        return None

def main():
    st.sidebar.title("Crypto Market Trends")

    # Retrieving the list of cryptocurrencies from the CoinGecko API
    coins_url = "https://api.coingecko.com/api/v3/coins/list?x_cg_demo_api_key=CG-TF4rSWCUx8ctAL7TiqwzYnbN"
    coins_response = requests.get(coins_url)
    coins_data = coins_response.json()
    crypto_options = {coin['id']: coin['name'] for coin in coins_data}

    # Sidebar inputs for selecting two cryptocurrencies
    first_crypto = st.sidebar.selectbox("Choose a cryptocurrency", options=list(crypto_options.values()))
    first_crypto_id = [id for id, name in crypto_options.items() if name == first_crypto][0]

    second_crypto = st.sidebar.selectbox("Choose another cryptocurrency", options=list(crypto_options.values()))
    second_crypto_id = [id for id, name in crypto_options.items() if name == second_crypto][0]

    # Sidebar input for selecting the timeframe for data comparison
    time_periods = {"1 Week": 7, "1 Month": 30, "1 Year": 365, "5 Years": 1825}
    chosen_period = st.sidebar.selectbox("Time period", options=list(time_periods.keys()))

    # Fetching market data for the selected cryptocurrencies
    first_market_data = get_crypto_data(first_crypto_id, time_periods[chosen_period])
    second_market_data = get_crypto_data(second_crypto_id, time_periods[chosen_period])

    if first_market_data is not None and second_market_data is not None:
        # Plotting the price comparison
        st.subheader(f"Price Comparison: {first_crypto} vs {second_crypto}")
        plt.figure(figsize=(10, 6))
        plt.plot(first_market_data['timestamp'], first_market_data['price'], label=first_crypto, color='teal', linewidth=2.5)
        plt.plot(second_market_data['timestamp'], second_market_data['price'], label=second_crypto, color='salmon', linewidth=2.5)
        plt.title(f"Market Trends over {chosen_period}")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.legend()
        plt.grid(True)
        st.pyplot()

if __name__ == "__main__":
    main()
