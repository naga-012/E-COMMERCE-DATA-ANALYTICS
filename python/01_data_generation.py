"""
01_data_generation.py
======================
E-Commerce Sales, Customer & Profitability Analytics
Synthetic Data Generation Pipeline

Generates realistic, reproducible, multi-year e-commerce data for an Indian marketplace:
- Customers (5,000+ records)
- Products (500+ records)
- Orders (50,000+ records)
- Payments (50,000+ records)
- Returns (Several thousand records)

Features realistic demographics, product pricing margins, seasonal spikes (festivals),
strict financial formula validation, and controlled data-quality issues in the raw dataset.
"""

import os
import random
import datetime
import numpy as np
import pandas as pd

# Set random seed for 100% reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

RAW_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw")
os.makedirs(RAW_DATA_DIR, exist_ok=True)

# Geographic master data (Realistic Indian cities, states, and geographic regions)
GEOGRAPHY_DATA = [
    {"city": "Mumbai", "state": "Maharashtra", "region": "West", "weight": 0.12},
    {"city": "Delhi", "state": "Delhi", "region": "North", "weight": 0.11},
    {"city": "Bengaluru", "state": "Karnataka", "region": "South", "weight": 0.10},
    {"city": "Hyderabad", "state": "Telangana", "region": "South", "weight": 0.08},
    {"city": "Chennai", "state": "Tamil Nadu", "region": "South", "weight": 0.07},
    {"city": "Kolkata", "state": "West Bengal", "region": "East", "weight": 0.06},
    {"city": "Pune", "state": "Maharashtra", "region": "West", "weight": 0.06},
    {"city": "Ahmedabad", "state": "Gujarat", "region": "West", "weight": 0.05},
    {"city": "Jaipur", "state": "Rajasthan", "region": "North", "weight": 0.04},
    {"city": "Lucknow", "state": "Uttar Pradesh", "region": "North", "weight": 0.04},
    {"city": "Chandigarh", "state": "Punjab", "region": "North", "weight": 0.03},
    {"city": "Indore", "state": "Madhya Pradesh", "region": "Central", "weight": 0.03},
    {"city": "Bhopal", "state": "Madhya Pradesh", "region": "Central", "weight": 0.03},
    {"city": "Kochi", "state": "Kerala", "region": "South", "weight": 0.03},
    {"city": "Patna", "state": "Bihar", "region": "East", "weight": 0.03},
    {"city": "Bhubaneswar", "state": "Odisha", "region": "East", "weight": 0.02},
    {"city": "Coimbatore", "state": "Tamil Nadu", "region": "South", "weight": 0.03},
    {"city": "Surat", "state": "Gujarat", "region": "West", "weight": 0.03},
    {"city": "Nagpur", "state": "Maharashtra", "region": "West", "weight": 0.02},
    {"city": "Visakhapatnam", "state": "Andhra Pradesh", "region": "South", "weight": 0.02},
    {"city": "Guwahati", "state": "Assam", "region": "East", "weight": 0.01}
]

# Normalize weights
geo_weights = [g["weight"] for g in GEOGRAPHY_DATA]
geo_weights = [w / sum(geo_weights) for w in geo_weights]

FIRST_NAMES_MALE = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan",
    "Shaurya", "Atharv", "Dhruv", "Kabir", "Rohan", "Rahul", "Amit", "Vikram", "Suresh", "Ramesh",
    "Manish", "Rajesh", "Deepak", "Anand", "Nikhil", "Kunal", "Siddharth", "Gaurav", "Pranav", "Varun"
]

FIRST_NAMES_FEMALE = [
    "Saanvi", "Aanya", "Aadhya", "Aarohi", "Ananya", "Diya", "Gauri", "Isha", "Kavya", "Khushi",
    "Meera", "Navya", "Pari", "Prisha", "Riya", "Sneha", "Pooja", "Anjali", "Priyanka", "Neha",
    "Divya", "Swati", "Shreya", "Tanvi", "Sunita", "Anita", "Deepa", "Rekha", "Nandini", "Pallavi"
]

LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Malhotra", "Bhatia", "Saxena", "Mehta", "Patel", "Shah", "Joshi",
    "Reddy", "Rao", "Nair", "Pillai", "Menon", "Iyer", "Iyengar", "Chatterjee", "Banerjee", "Mukherjee",
    "Singh", "Kaur", "Das", "Dutta", "Choudhury", "Mishra", "Pandey", "Yadav", "Tripathi", "Agarwal"
]

CATEGORY_CATALOG = {
    "Electronics": {
        "subcategories": ["Smartphones", "Laptops", "Audio & Headphones", "Smartwatches", "Cameras", "Accessories"],
        "brands": ["Samsung", "OnePlus", "Apple", "boAt", "Noise", "Sony", "Dell", "HP", "Xiaomi", "Realme"],
        "price_range": (800, 75000),
        "margin_range": (0.12, 0.26),
        "suppliers": ["Apex Electronics Ltd", "Zenith Tech Distribution", "Metro Gadget Hub"]
    },
    "Fashion": {
        "subcategories": ["Men's Wear", "Women's Wear", "Footwear", "Ethnic Wear", "Kids Wear", "Winter Wear"],
        "brands": ["Allen Solly", "FabIndia", "Biba", "Levi's", "Puma", "Nike", "Raymond", "Peter England", "W", "Zudio"],
        "price_range": (499, 5999),
        "margin_range": (0.35, 0.62),
        "suppliers": ["Vibrant Textiles Corp", "Royal Garments Supply", "Heritage Weaves"]
    },
    "Home & Kitchen": {
        "subcategories": ["Cookware", "Small Appliances", "Home Decor", "Bedding & Linen", "Storage & Org"],
        "brands": ["Prestige", "Hawkins", "Philips", "Bajaj", "Milton", "Cello", "Spaces", "Bombay Dyeing"],
        "price_range": (350, 8500),
        "margin_range": (0.28, 0.48),
        "suppliers": ["HomeCraft Distributors", "Sterling Kitchenware", "Urban Living Goods"]
    },
    "Beauty": {
        "subcategories": ["Skincare", "Haircare", "Makeup", "Fragrances", "Men's Grooming"],
        "brands": ["Lakme", "Mamaearth", "Nykaa", "Maybelline", "L'Oreal", "The Derma Co", "Biotique", "Forest Essentials"],
        "price_range": (199, 3500),
        "margin_range": (0.38, 0.65),
        "suppliers": ["PureGlow Cosmetics", "Aura Personal Care", "Divine Botanicals"]
    },
    "Sports": {
        "subcategories": ["Fitness Equipment", "Sports Apparel", "Outdoor Gear", "Cycling", "Racket Sports"],
        "brands": ["Decathlon", "Nivia", "Cosco", "Yonex", "Puma Sports", "Kiprun", "Domyos"],
        "price_range": (299, 12000),
        "margin_range": (0.25, 0.45),
        "suppliers": ["Action Sports Distribution", "FitNation Logistics", "Olympus Gear"]
    },
    "Books": {
        "subcategories": ["Fiction", "Non-Fiction", "Self-Help", "Academic & Test Prep", "Children's Books"],
        "brands": ["Penguin", "HarperCollins", "Rupa Publications", "Jaico", "Arihant", "Oxford University Press"],
        "price_range": (150, 1200),
        "margin_range": (0.22, 0.38),
        "suppliers": ["Global Book Importers", "National Book Depot", "Scholar Press Logistics"]
    },
    "Grocery": {
        "subcategories": ["Staples & Grains", "Snacks & Beverages", "Organic Foods", "Cooking Essentials", "Breakfast & Dairy"],
        "brands": ["Tata Sampann", "Fortune", "Aashirvaad", "Nestle", "Amul", "Haldiram's", "Catch", "Dabur"],
        "price_range": (60, 1500),
        "margin_range": (0.10, 0.22),
        "suppliers": ["Annapurna FMCG Wholesale", "FarmFresh Agro Supplies", "Bharat Foodworks"]
    },
    "Accessories": {
        "subcategories": ["Bags & Backpacks", "Watches", "Eyewear", "Jewelry & Belts", "Travel Gear"],
        "brands": ["Titan", "Fastrack", "Wildcraft", "American Tourister", "Lenskart", "Voylla", "Skybags"],
        "price_range": (250, 6500),
        "margin_range": (0.40, 0.68),
        "suppliers": ["Optima Accessories", "Prism Lifestyle Supply", "Vanguard Leather Works"]
    }
}


def generate_customers(n_customers=5200):
    """Generates customer dataset with realistic demographics, tenure, and segments."""
    customers = []
    start_date = datetime.date(2021, 1, 1)
    end_date = datetime.date(2024, 6, 30)
    days_range = (end_date - start_date).days

    for i in range(1, n_customers + 1):
        cid = f"CUST-{i:05d}"
        gender = np.random.choice(["Male", "Female", "Other"], p=[0.51, 0.47, 0.02])
        if gender == "Male":
            name = f"{random.choice(FIRST_NAMES_MALE)} {random.choice(LAST_NAMES)}"
        elif gender == "Female":
            name = f"{random.choice(FIRST_NAMES_FEMALE)} {random.choice(LAST_NAMES)}"
        else:
            name = f"{random.choice(FIRST_NAMES_MALE)} {random.choice(LAST_NAMES)}"

        # Realistic age distribution (peaks between 22 and 45)
        age = int(np.clip(np.random.normal(33, 11), 18, 70))
        
        # Select geography
        geo = np.random.choice(GEOGRAPHY_DATA, p=geo_weights)
        
        # Signup date
        signup_offset = random.randint(0, days_range)
        signup_date = start_date + datetime.timedelta(days=signup_offset)

        # Initial segment assignment based on tenure and pseudo-spend potential
        tenure_days = (datetime.date(2024, 12, 31) - signup_date).days
        prob_tier = random.random()
        if tenure_days < 180:
            segment = "New Customer"
        elif prob_tier > 0.85:
            segment = "VIP Customer"
        elif prob_tier > 0.55:
            segment = "Loyal Customer"
        else:
            segment = "Regular Customer"

        customers.append({
            "customer_id": cid,
            "customer_name": name,
            "gender": gender,
            "age": age,
            "city": geo["city"],
            "state": geo["state"],
            "region": geo["region"],
            "signup_date": signup_date.strftime("%Y-%m-%d"),
            "customer_segment": segment
        })

    df_customers = pd.DataFrame(customers)

    # Intentionally inject realistic raw data flaws
    # 1. Trailing/leading whitespace and casing issues in city/state
    noisy_indices = df_customers.sample(frac=0.03, random_state=RANDOM_SEED).index
    for idx in noisy_indices:
        case_type = random.choice(["upper", "lower", "space_both", "space_end"])
        val = df_customers.loc[idx, "city"]
        if case_type == "upper":
            df_customers.loc[idx, "city"] = val.upper()
        elif case_type == "lower":
            df_customers.loc[idx, "city"] = val.lower()
        elif case_type == "space_both":
            df_customers.loc[idx, "city"] = f"  {val} "
        else:
            df_customers.loc[idx, "city"] = f"{val}   "

    # 2. Missing values in city/region for ~35 rows
    null_indices = df_customers.sample(n=35, random_state=RANDOM_SEED + 1).index
    df_customers.loc[null_indices, "city"] = np.nan

    # 3. Duplicate customer records (~25 rows duplicated)
    dup_rows = df_customers.sample(n=25, random_state=RANDOM_SEED + 2)
    df_customers = pd.concat([df_customers, dup_rows], ignore_index=True)

    # 4. Outlier / invalid ages (e.g. -5, 999) for 6 rows
    invalid_age_idx = df_customers.sample(n=6, random_state=RANDOM_SEED + 3).index
    for i, idx in enumerate(invalid_age_idx):
        df_customers.loc[idx, "age"] = -1 if i % 2 == 0 else 999

    return df_customers


def generate_products(n_products=550):
    """Generates product catalog with consistent category, subcategory, and margin profiles."""
    products = []
    categories = list(CATEGORY_CATALOG.keys())
    # Distribute products across categories
    cat_weights = [0.20, 0.22, 0.15, 0.12, 0.10, 0.08, 0.07, 0.06]

    for i in range(1, n_products + 1):
        pid = f"PROD-{i:04d}"
        cat_name = np.random.choice(categories, p=cat_weights)
        cat_info = CATEGORY_CATALOG[cat_name]
        
        subcat = random.choice(cat_info["subcategories"])
        brand = random.choice(cat_info["brands"])
        supplier = random.choice(cat_info["suppliers"])

        # Name synthesis
        descriptors = ["Pro", "Max", "Classic", "Plus", "Ultra", "Elite", "Prime", "Essentials", "Series 5", "Premium"]
        p_name = f"{brand} {subcat} {random.choice(descriptors)}"

        # Price and margin logic
        min_p, max_p = cat_info["price_range"]
        # Log-uniform distribution for prices so cheaper items are more frequent
        raw_price = np.exp(np.random.uniform(np.log(min_p), np.log(max_p)))
        # Round to psychological retail points (.00, .99, .49)
        selling_price = round(round(raw_price / 10) * 10 - (1 if raw_price > 100 else 0), 2)
        if selling_price < min_p:
            selling_price = float(min_p)

        # Margin
        min_m, max_m = cat_info["margin_range"]
        margin_pct = np.random.uniform(min_m, max_m)
        cost_price = round(selling_price * (1 - margin_pct), 2)
        
        stock = random.randint(15, 600)

        products.append({
            "product_id": pid,
            "product_name": p_name,
            "category": cat_name,
            "subcategory": subcat,
            "brand": brand,
            "cost_price": cost_price,
            "selling_price": selling_price,
            "supplier": supplier,
            "stock_quantity": stock
        })

    df_products = pd.DataFrame(products)

    # Intentionally inject raw defects:
    # 1. Extra whitespace in category/brand
    prod_noisy_idx = df_products.sample(n=20, random_state=RANDOM_SEED + 4).index
    for idx in prod_noisy_idx:
        df_products.loc[idx, "category"] = f"  {df_products.loc[idx, 'category']}  "
    
    # 2. Duplicate rows (~10 duplicates)
    dup_products = df_products.sample(n=10, random_state=RANDOM_SEED + 5)
    df_products = pd.concat([df_products, dup_products], ignore_index=True)

    return df_products


def generate_orders_and_related(df_clean_cust, df_clean_prod, n_orders=52500):
    """
    Generates orders, payments, and returns with consistent financial formulas and seasonality.
    """
    orders = []
    payments = []
    returns = []

    # Map customers and products for quick reference
    cust_list = df_clean_cust.to_dict("records")
    prod_list = df_clean_prod.to_dict("records")

    # Weights by customer segment for order probability
    segment_order_multiplier = {
        "VIP Customer": 3.5,
        "Loyal Customer": 2.2,
        "Regular Customer": 1.0,
        "New Customer": 0.5
    }
    cust_weights = [segment_order_multiplier.get(c.get("customer_segment", "Regular Customer"), 1.0) for c in cust_list]
    cust_weights = np.array(cust_weights) / sum(cust_weights)

    # Product popularity weights (lower priced and high demand items ordered more)
    prod_weights = []
    for p in prod_list:
        p_price = p["selling_price"]
        w = 1.0 / (np.sqrt(p_price) + 1)
        if p["category"] in ["Fashion", "Electronics", "Beauty"]:
            w *= 1.4
        prod_weights.append(w)
    prod_weights = np.array(prod_weights) / sum(prod_weights)

    start_date = datetime.date(2022, 1, 1)
    end_date = datetime.date(2024, 12, 31)
    total_days = (end_date - start_date).days

    # Daily seasonality weights: Oct-Nov festive surge (Diwali), Jan New Year, June Summer Sale
    day_weights = []
    for day_offset in range(total_days + 1):
        cur_date = start_date + datetime.timedelta(days=day_offset)
        m = cur_date.month
        d = cur_date.day
        w = 1.0
        # Festival surge (October - November)
        if m in [10, 11]:
            w *= 1.85
        # Summer sales (May - June)
        elif m in [5, 6]:
            w *= 1.30
        # New year & Republic day sale (January)
        elif m == 1:
            w *= 1.25
        # Weekend boost (Saturday, Sunday)
        if cur_date.weekday() in [5, 6]:
            w *= 1.20
        # YoY growth factor (Marketplace grows over time: 2022=1.0x, 2023=1.25x, 2024=1.55x)
        growth_factor = 1.0 + 0.55 * (day_offset / total_days)
        day_weights.append(w * growth_factor)

    day_weights = np.array(day_weights) / sum(day_weights)

    payment_methods = ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash on Delivery", "Wallet"]
    payment_method_probs = [0.42, 0.24, 0.12, 0.08, 0.10, 0.04]

    return_reasons = [
        "Size Issue", "Damaged Product", "Quality Issue", 
        "Wrong Product", "Changed Mind", "Late Delivery", "Other"
    ]
    # Return reason probability by category
    cat_return_reason_probs = {
        "Fashion": [0.45, 0.10, 0.18, 0.08, 0.12, 0.05, 0.02],
        "Electronics": [0.02, 0.35, 0.25, 0.15, 0.08, 0.10, 0.05],
        "default": [0.05, 0.25, 0.22, 0.18, 0.15, 0.10, 0.05]
    }

    order_counter = 1
    return_counter = 1

    # Pre-select customers, products, and day offsets for performance
    chosen_cust_indices = np.random.choice(len(cust_list), size=n_orders, p=cust_weights)
    chosen_prod_indices = np.random.choice(len(prod_list), size=n_orders, p=prod_weights)
    chosen_day_offsets = np.random.choice(total_days + 1, size=n_orders, p=day_weights)

    for i in range(n_orders):
        cust = cust_list[chosen_cust_indices[i]]
        prod = prod_list[chosen_prod_indices[i]]
        day_off = chosen_day_offsets[i]

        order_date = start_date + datetime.timedelta(days=int(day_off))
        
        # Ensure order_date is not earlier than customer signup date
        cust_signup = datetime.datetime.strptime(cust["signup_date"], "%Y-%m-%d").date()
        if order_date < cust_signup:
            order_date = cust_signup + datetime.timedelta(days=random.randint(1, 30))
            if order_date > end_date:
                order_date = end_date

        order_id = f"ORD-{order_counter:07d}"
        order_counter += 1

        # Quantity distribution: 1 (72%), 2 (18%), 3 (6%), 4 (3%), 5 (1%)
        qty = int(np.random.choice([1, 2, 3, 4, 5], p=[0.72, 0.18, 0.06, 0.03, 0.01]))
        unit_price = float(prod["selling_price"])
        cost_price = float(prod["cost_price"])

        # Discount logic: higher during festivals, low otherwise
        is_festive = order_date.month in [10, 11]
        if is_festive:
            discount_pct = float(np.random.choice([0, 10, 15, 20, 25, 30], p=[0.20, 0.25, 0.25, 0.15, 0.10, 0.05]))
        else:
            discount_pct = float(np.random.choice([0, 5, 10, 15, 20], p=[0.50, 0.22, 0.15, 0.08, 0.05]))

        # Financial formulas strictly enforced:
        # gross_sales = quantity * unit_price
        # discount_amount = gross_sales * discount_percentage / 100
        # sales_amount = gross_sales - discount_amount
        # cost_amount = quantity * cost_price
        # profit_amount = sales_amount - cost_amount
        gross_sales = round(qty * unit_price, 2)
        discount_amt = round(gross_sales * (discount_pct / 100.0), 2)
        sales_amt = round(gross_sales - discount_amt, 2)
        cost_amt = round(qty * cost_price, 2)
        profit_amt = round(sales_amt - cost_amt, 2)

        # Category-dependent return rate: Fashion (~14%), Electronics (~8%), Books (~2%), etc.
        cat = prod["category"]
        if cat == "Fashion":
            ret_prob = 0.13
        elif cat == "Electronics":
            ret_prob = 0.08
        elif cat == "Home & Kitchen":
            ret_prob = 0.07
        elif cat == "Grocery":
            ret_prob = 0.02
        else:
            ret_prob = 0.05

        cancel_prob = 0.06
        delivered_prob = max(0.0, 1.0 - (ret_prob + cancel_prob))
        status = np.random.choice(
            ["Delivered", "Returned", "Cancelled"], 
            p=[delivered_prob, ret_prob, cancel_prob]
        )

        orders.append({
            "order_id": order_id,
            "customer_id": cust["customer_id"],
            "product_id": prod["product_id"],
            "order_date": order_date.strftime("%Y-%m-%d"),
            "quantity": qty,
            "unit_price": unit_price,
            "discount_percentage": discount_pct,
            "discount_amount": discount_amt,
            "sales_amount": sales_amt,
            "cost_amount": cost_amt,
            "profit_amount": profit_amt,
            "city": cust["city"],
            "state": cust["state"],
            "region": cust["region"],
            "order_status": status
        })

        # Payment record
        pmethod = np.random.choice(payment_methods, p=payment_method_probs)
        pay_date = order_date + datetime.timedelta(days=0 if pmethod != "Cash on Delivery" else random.randint(2, 5))
        
        if status == "Cancelled":
            pay_status = np.random.choice(["Refunded", "Failed"], p=[0.70, 0.30])
        elif status == "Returned":
            pay_status = "Refunded"
        else:
            pay_status = "Success"

        payment_id = f"PAY-{i+1:07d}"
        payments.append({
            "payment_id": payment_id,
            "order_id": order_id,
            "payment_date": pay_date.strftime("%Y-%m-%d"),
            "payment_method": pmethod,
            "payment_status": pay_status,
            "payment_amount": sales_amt
        })

        # Return record (only for Returned orders)
        if status == "Returned":
            ret_id = f"RET-{return_counter:06d}"
            return_counter += 1
            ret_date = order_date + datetime.timedelta(days=random.randint(2, 10))
            
            reasons_dist = cat_return_reason_probs.get(cat, cat_return_reason_probs["default"])
            reason = np.random.choice(return_reasons, p=reasons_dist)
            
            # Returned quantity (usually full, occasionally partial if qty > 1)
            ret_qty = qty if qty == 1 else random.randint(1, qty)
            # Refund proportional to returned quantity
            unit_effective_sale = sales_amt / qty
            refund_amt = round(unit_effective_sale * ret_qty, 2)

            returns.append({
                "return_id": ret_id,
                "order_id": order_id,
                "return_date": ret_date.strftime("%Y-%m-%d"),
                "return_reason": reason,
                "return_quantity": ret_qty,
                "refund_amount": refund_amt
            })

    df_orders = pd.DataFrame(orders)
    df_payments = pd.DataFrame(payments)
    df_returns = pd.DataFrame(returns)

    # Intentionally inject raw defects into Orders & Payments:
    # 1. Trailing whitespaces in order status
    order_noise_idx = df_orders.sample(n=40, random_state=RANDOM_SEED + 6).index
    for idx in order_noise_idx:
        df_orders.loc[idx, "order_status"] = f" {df_orders.loc[idx, 'order_status']} "

    # 2. Date format inconsistency in 25 orders (DD/MM/YYYY)
    date_noise_idx = df_orders.sample(n=25, random_state=RANDOM_SEED + 7).index
    for idx in date_noise_idx:
        cur_d = datetime.datetime.strptime(df_orders.loc[idx, "order_date"], "%Y-%m-%d")
        df_orders.loc[idx, "order_date"] = cur_d.strftime("%d/%m/%Y")

    # 3. Duplicate payments (~30 duplicate rows)
    dup_pay = df_payments.sample(n=30, random_state=RANDOM_SEED + 8)
    df_payments = pd.concat([df_payments, dup_pay], ignore_index=True)

    # 4. Duplicate orders (~20 duplicate rows)
    dup_ord = df_orders.sample(n=20, random_state=RANDOM_SEED + 9)
    df_orders = pd.concat([df_orders, dup_ord], ignore_index=True)

    return df_orders, df_payments, df_returns


def main():
    print("=" * 60)
    print("STARTING REALISTIC E-COMMERCE DATASET GENERATION")
    print(f"Random Seed: {RANDOM_SEED}")
    print("=" * 60)

    # 1. Customers
    print("[1/4] Generating Customers (5,000+ records)...")
    df_raw_customers = generate_customers(n_customers=5200)
    cust_path = os.path.join(RAW_DATA_DIR, "customers.csv")
    df_raw_customers.to_csv(cust_path, index=False)
    print(f" -> Generated {len(df_raw_customers):,} raw customer rows. Saved to {cust_path}")

    # 2. Products
    print("[2/4] Generating Products (500+ records)...")
    df_raw_products = generate_products(n_products=550)
    prod_path = os.path.join(RAW_DATA_DIR, "products.csv")
    df_raw_products.to_csv(prod_path, index=False)
    print(f" -> Generated {len(df_raw_products):,} raw product rows. Saved to {prod_path}")

    # Create temporary clean reference copies for relational consistency during order generation
    clean_cust_ref = df_raw_customers.dropna(subset=["city"]).drop_duplicates(subset=["customer_id"])
    clean_prod_ref = df_raw_products.drop_duplicates(subset=["product_id"])

    # 3. Orders, Payments, Returns
    print("[3/4] Generating Orders, Payments, and Returns (50,000+ records)...")
    df_raw_orders, df_raw_payments, df_raw_returns = generate_orders_and_related(
        clean_cust_ref, clean_prod_ref, n_orders=52500
    )

    ord_path = os.path.join(RAW_DATA_DIR, "orders.csv")
    pay_path = os.path.join(RAW_DATA_DIR, "payments.csv")
    ret_path = os.path.join(RAW_DATA_DIR, "returns.csv")

    df_raw_orders.to_csv(ord_path, index=False)
    df_raw_payments.to_csv(pay_path, index=False)
    df_raw_returns.to_csv(ret_path, index=False)

    print(f" -> Generated {len(df_raw_orders):,} raw order rows. Saved to {ord_path}")
    print(f" -> Generated {len(df_raw_payments):,} raw payment rows. Saved to {pay_path}")
    print(f" -> Generated {len(df_raw_returns):,} raw return rows. Saved to {ret_path}")

    print("\n[4/4] Data Generation Summary:")
    print(f" - Customers CSV: {os.path.getsize(cust_path) / 1024:.1f} KB")
    print(f" - Products CSV:   {os.path.getsize(prod_path) / 1024:.1f} KB")
    print(f" - Orders CSV:     {os.path.getsize(ord_path) / 1024 / 1024:.2f} MB")
    print(f" - Payments CSV:   {os.path.getsize(pay_path) / 1024 / 1024:.2f} MB")
    print(f" - Returns CSV:    {os.path.getsize(ret_path) / 1024:.1f} KB")
    print("=" * 60)
    print("RAW DATA GENERATION COMPLETED SUCCESSFULLY.")
    print("=" * 60)


if __name__ == "__main__":
    main()
