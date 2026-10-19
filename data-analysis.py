import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data_file = 'market_prices.csv'

# Step 1: Automatically generate mock data if it doesn't exist yet
if not os.path.exists(data_file):
    print("No existing dataset found. Generating mock market price data...")
    np.random.seed(42)
    date_range = pd.date_range(start='2025-01-01', end='2026-10-01', freq='D')
    
    # Simulate a realistic price trend with upward drift and seasonal variation
    base_price = 2200 + np.linspace(0, 400, len(date_range))
    seasonal = 150 * np.sin(2 * np.pi * date_range.dayofyear / 365.25)
    noise = np.random.normal(0, 45, len(date_range))
    prices = np.clip(base_price + seasonal + noise, 1000, None)
    
    mock_df = pd.DataFrame({
        'date': date_range,
        'commodity': 'Wheat',
        'market': 'Central Mandi',
        'modal_price': prices
    })
    mock_df.to_csv(data_file, index=False)
    print(f"Mock dataset saved to {data_file}")

# Step 2: Load and Clean the Data
print(f"Loading data from {data_file}...")
df = pd.read_csv(data_file)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')
df = df.dropna(subset=['modal_price'])

# Step 3: Analyze Data
commodity_df = df[df['commodity'] == 'Wheat'].copy()

# Calculate monthly averages and a 30-day moving average trend
commodity_df['year_month'] = commodity_df['date'].dt.to_period('M')
monthly_avg = commodity_df.groupby('year_month')['modal_price'].mean()
commodity_df['rolling_avg'] = commodity_df['modal_price'].rolling(window=30).mean()

print("\n--- Recent Monthly Average Prices ---")
print(monthly_avg.tail())

# Step 4: Visualize and Save Output Chart
print("\nGenerating trend chart...")
plt.figure(figsize=(12, 6))
plt.plot(commodity_df['date'], commodity_df['modal_price'], label='Daily Price', alpha=0.3, color='gray')
plt.plot(commodity_df['date'], commodity_df['rolling_avg'], label='30-Day Moving Average', color='blue', linewidth=2)

plt.title('Wheat Price Trends and Moving Average', fontsize=14, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Price (₹ / Quintal)', fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

# Save output chart (must match the filename expected by your GitHub Actions workflow)
output_filename = 'price_trend_analysis.png'
plt.savefig(output_filename)
print(f"Analysis complete! Chart successfully saved as '{output_filename}'.")