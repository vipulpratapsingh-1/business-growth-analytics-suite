"""
Dataset Generator for Business Growth Analytics Suite.
Generates a highly realistic 100,000-row sales dataset.
"""

import sys
import os
from pathlib import Path
import numpy as np
import pandas as pd

# Force UTF-8 encoding for Windows terminals
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Add parent directory to sys.path to import config
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config

def generate_sales_dataset(num_rows=config.TOTAL_ROWS, seed=config.RANDOM_SEED):
    """
    Generate a realistic enterprise sales dataset with exact row count matching specification.
    """
    np.random.seed(seed)
    print(f"[+] Generating dataset with exactly {num_rows:,} rows...")

    # 1. Realistic City & State Mapping (Indian Commercial Hubs)
    city_state_map = [
        ("Mumbai", "Maharashtra"),
        ("Pune", "Maharashtra"),
        ("Nagpur", "Maharashtra"),
        ("Bengaluru", "Karnataka"),
        ("Mysuru", "Karnataka"),
        ("Hyderabad", "Telangana"),
        ("Chennai", "Tamil Nadu"),
        ("Coimbatore", "Tamil Nadu"),
        ("New Delhi", "Delhi"),
        ("Gurugram", "Haryana"),
        ("Noida", "Uttar Pradesh"),
        ("Lucknow", "Uttar Pradesh"),
        ("Ahmedabad", "Gujarat"),
        ("Surat", "Gujarat"),
        ("Kolkata", "West Bengal"),
        ("Jaipur", "Rajasthan"),
        ("Kochi", "Kerala"),
        ("Indore", "Madhya Pradesh"),
        ("Chandigarh", "Punjab"),
        ("Bhubaneswar", "Odisha")
    ]
    
    # 2. Products Catalog by Category with base prices & profit margin ratios
    product_catalog = [
        # Technology
        ("MacBook Pro 16-inch", "Technology", 219900.0, 0.22),
        ("Dell XPS 15 Laptop", "Technology", 145000.0, 0.20),
        ("iPhone 15 Pro", "Technology", 134900.0, 0.25),
        ("Samsung Galaxy S24 Ultra", "Technology", 129999.0, 0.24),
        ("Sony WH-1000XM5 Headphones", "Technology", 29990.0, 0.30),
        ("iPad Air M2", "Technology", 59900.0, 0.22),
        ("Logitech MX Master 3S Mouse", "Technology", 9995.0, 0.35),
        ("Dell 27-inch 4K Monitor", "Technology", 32500.0, 0.25),
        ("Anker Power Bank 20000mAh", "Technology", 4499.0, 0.38),
        ("Keychron K2 Mechanical Keyboard", "Technology", 8999.0, 0.32),
        
        # Furniture
        ("Ergonomic Mesh Office Chair", "Furniture", 16499.0, 0.28),
        ("Electric Standing Desk", "Furniture", 34999.0, 0.25),
        ("Executive Leather Chair", "Furniture", 24999.0, 0.30),
        ("Bookshelf Unit (5-Tier)", "Furniture", 8999.0, 0.32),
        ("Wooden Study Table", "Furniture", 12500.0, 0.28),
        ("Pedestal Storage Cabinet", "Furniture", 7499.0, 0.35),
        ("Conference Table 8-Seater", "Furniture", 58900.0, 0.26),
        
        # Office Supplies
        ("High-Speed Document Shredder", "Office Supplies", 6499.0, 0.30),
        ("Thermal Label Printer", "Office Supplies", 11200.0, 0.28),
        ("Heavy-Duty Laminator", "Office Supplies", 3899.0, 0.35),
        ("A4 Printing Paper Box (5 Reams)", "Office Supplies", 1499.0, 0.18),
        ("Ergonomic Footrest", "Office Supplies", 2199.0, 0.40),
        ("Whiteboard & Marker Kit", "Office Supplies", 1850.0, 0.42),
        ("Desk Organizer & Cable Manager", "Office Supplies", 1299.0, 0.45)
    ]

    # 3. First and Last Name pools for realistic customer names
    first_names = [
        "Aarav", "Ananya", "Rohan", "Priya", "Vikram", "Neha", "Aditya", "Pooja", 
        "Karan", "Sneha", "Rahul", "Ishita", "Siddharth", "Kavya", "Amit", "Riya",
        "Arjun", "Tanvi", "Varun", "Meera", "Manish", "Divya", "Suresh", "Shreya",
        "Deepak", "Swati", "Nikhil", "Simran", "Rajesh", "Nisha"
    ]
    last_names = [
        "Sharma", "Verma", "Patel", "Mehta", "Iyer", "Nair", "Gupta", "Reddy",
        "Singh", "Chawla", "Deshmukh", "Joshi", "Bhat", "Rao", "Kulkarni",
        "Agarwal", "Bhasin", "Trivedi", "Banerjee", "Sengupta", "Das", "Kapoor"
    ]
    
    # Pre-generate 5,000 unique Customer Profiles
    num_customers = 5000
    cust_ids = [f"CUST-{10000 + i}" for i in range(num_customers)]
    cust_names = [f"{np.random.choice(first_names)} {np.random.choice(last_names)}" for _ in range(num_customers)]

    # 4. Generate Core Arrays
    # Order IDs
    order_ids = [f"ORD-2024-{100000 + i}" for i in range(num_rows)]

    # Customer Selection
    cust_indices = np.random.randint(0, num_customers, size=num_rows)
    selected_cust_ids = [cust_ids[idx] for idx in cust_indices]
    selected_cust_names = [cust_names[idx] for idx in cust_indices]

    # City & State Selection
    city_indices = np.random.randint(0, len(city_state_map), size=num_rows)
    cities = [city_state_map[idx][0] for idx in city_indices]
    states = [city_state_map[idx][1] for idx in city_indices]

    # Product Selection
    product_indices = np.random.randint(0, len(product_catalog), size=num_rows)
    products = [product_catalog[idx][0] for idx in product_indices]
    categories = [product_catalog[idx][1] for idx in product_indices]
    unit_prices = np.array([product_catalog[idx][2] for idx in product_indices])
    base_margins = np.array([product_catalog[idx][3] for idx in product_indices])

    # Date Generation (Between 2023-01-01 and 2024-12-31)
    start_dt = pd.to_datetime(config.START_DATE)
    end_dt = pd.to_datetime(config.END_DATE)
    total_days = (end_dt - start_dt).days
    random_days = np.random.randint(0, total_days + 1, size=num_rows)
    random_seconds = np.random.randint(0, 86400, size=num_rows)
    order_dates = [
        (start_dt + pd.Timedelta(days=int(d), seconds=int(s))).strftime("%Y-%m-%d %H:%M:%S")
        for d, s in zip(random_days, random_seconds)
    ]

    # Quantity (Skewed towards 1-5, occasionally up to 10 for enterprise bulk)
    quantity = np.random.choice([1, 2, 3, 4, 5, 8, 10], size=num_rows, p=[0.45, 0.25, 0.15, 0.08, 0.04, 0.02, 0.01])

    # Discount (0%, 5%, 10%, 15%, 20%, 25%)
    discount_rates = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25]
    discounts = np.random.choice(discount_rates, size=num_rows, p=[0.50, 0.20, 0.15, 0.08, 0.05, 0.02])

    # Calculations: Sales and Profit
    # Sales = Quantity * Unit Price * (1 - Discount)
    gross_amount = quantity * unit_prices
    sales = np.round(gross_amount * (1.0 - discounts), 2)

    # Profit Margin Logic: Higher discounts lower the profit margin; high volume gets small overhead penalty
    effective_margin = base_margins - (discounts * 1.2) + np.random.uniform(-0.03, 0.03, size=num_rows)
    profit = np.round(sales * effective_margin, 2)

    # Payment Methods
    payment_methods = np.random.choice(
        ["UPI", "Credit Card", "Net Banking", "Debit Card", "Cash on Delivery"],
        size=num_rows,
        p=[0.42, 0.28, 0.15, 0.10, 0.05]
    )

    # 5. Assemble DataFrame
    df = pd.DataFrame({
        "Order ID": order_ids,
        "Order Date": order_dates,
        "Customer ID": selected_cust_ids,
        "Customer Name": selected_cust_names,
        "City": cities,
        "State": states,
        "Product": products,
        "Category": categories,
        "Quantity": quantity,
        "Unit Price": unit_prices,
        "Discount": discounts,
        "Sales": sales,
        "Profit": profit,
        "Payment Method": payment_methods
    })

    # Sort chronologically by Order Date
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df = df.sort_values("Order Date").reset_index(drop=True)
    df["Order Date"] = df["Order Date"].dt.strftime("%Y-%m-%d %H:%M:%S")

    # 6. Save dataset
    config.ensure_directories_exist()
    output_file = config.DATASET_PATH
    df.to_csv(output_file, index=False)
    
    print(f"[OK] Successfully created dataset at: {output_file}")
    print(f"[INFO] Dataset Shape: {df.shape[0]:,} rows x {df.shape[1]} columns")
    return df

if __name__ == "__main__":
    generate_sales_dataset()
