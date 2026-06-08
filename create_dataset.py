import pandas as pd
import random
import os

os.makedirs("data", exist_ok=True)

names = [
    "Asha", "Ravi", "Sita", "Rahul", "Meena",
    "John", "Kavya", "Arjun", "Divya", "Sai",
    "Priya", "Kiran", "Anjali", "Vamsi", "Sneha",
    "Nikhil", "Pooja", "Manoj", "Deepika", "Charan"
]

cities = [
    "Guntur",
    "Vijayawada",
    "Hyderabad",
    "Bangalore",
    "Chennai"
]

genders = [
    "Male",
    "Female"
]

categories = [
    "Beauty",
    "Electronics",
    "Fashion",
    "Grocery"
]

products = {
    "Beauty": ["Face Cream", "Shampoo", "Lipstick"],
    "Electronics": ["Headphones", "Smart Watch", "Keyboard"],
    "Fashion": ["Saree", "Kurti", "T-Shirt"],
    "Grocery": ["Rice Bag", "Oil Packet", "Sugar"]
}

customer_data = []

for i in range(1, 101):

    category = random.choice(categories)

    customer_data.append({
        "customer_id": 1000 + i,
        "name": random.choice(names) + str(i),
        "age": random.randint(18, 60),
        "gender": random.choice(genders),
        "city": random.choice(cities),
        "category": category,
        "total_spent": random.randint(2000, 50000),
        "purchase_count": random.randint(1, 20),
        "last_purchase_days": random.randint(1, 180),
        "churn": random.choice([0, 1]),
        "product": random.choice(products[category])
    })

df = pd.DataFrame(customer_data)

df.to_csv(
    "data/old_customers.csv",
    index=False
)

print("✅ old_customers.csv created successfully")
print(f"✅ Total Records: {len(df)}")