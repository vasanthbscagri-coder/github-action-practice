import csv
import os

def extract(input_file):
    print("Starting data extraction...")

    with open(input_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = list(reader)

    print(f"Extracted {len(data)} records")
    return data


def transform(data):
    print("Starting data transformation...")

    cleaned_data = []
    seen_ids = set()

    for row in data:
        customer_id = row["customer_id"].strip()
        name = row["name"].strip()
        city = row["city"].strip()

        try:
            amount = float(row["amount"])
        except (ValueError, TypeError):
            print(f"Skipping invalid amount for customer {customer_id}")
            continue

        # Remove duplicate customer IDs
        if customer_id in seen_ids:
            print(f"Duplicate found: customer {customer_id}")
            continue

        # Remove invalid or negative amounts
        if amount < 0 or not customer_id or not name:
            print(f"Invalid record skipped: customer {customer_id}")
            continue

        seen_ids.add(customer_id)

        cleaned_data.append({
            "customer_id": customer_id,
            "name": name,
            "city": city,
            "amount": amount
        })

    print(f"Records after cleaning: {len(cleaned_data)}")
    return cleaned_data


def load(data, output_file):
    print("Loading cleaned data...")

    if not data:
        raise ValueError("No valid records to load")

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["customer_id", "name", "city", "amount"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(data)

    print(f"Successfully loaded {len(data)} records")
    print(f"Output saved to: {output_file}")


def main():
    input_file = "customers.csv"
    output_file = "cleaned_customers.csv"

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    data = extract(input_file)
    transformed_data = transform(data)
    load(transformed_data, output_file)

    print("ETL pipeline completed successfully!")


if __name__ == "__main__":
    main()
