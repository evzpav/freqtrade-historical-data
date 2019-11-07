# Freqtrade Historical Data - Binance

Get historical data on Freqtrade format

```bash
# Create env
virtualenv -p python3 env

# Activate
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create binance folder
mkdir binance

cp .env_example .env
# Add your binance api keys to .env file

# Run
python main.py


# historical data files will be inside binance folder

```

Edit file main.py with pairs and timeframe needed.