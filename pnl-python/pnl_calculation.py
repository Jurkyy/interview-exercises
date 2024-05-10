import csv
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np # Comment this if using np is not allowed.


# Function to read data from a CSV file, pandas could be used instead of std-lib's csv.
def read_csv(filename):
    data = []
    with open(filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            data.append(row)
    return data


# Function to calculate the total gross PnL.
def calculate_total_gross_pnl(data):
    pnl_totals = {"Total": 0}
    cumulative_pnls = []
    timestamps = []
    cumulative_pnl = 0

    for row in data:
        # Skip if the action is not filled, as it won't have an effect on the PnL.
        if row["action"] and row["action"] != "filled":
            continue;

        # Check if all required keys are present and not empty.
        required_keys = [
            "tradePx",
            "tradeAmt",
            "orderSide",
            "orderProduct",
            "currentTime",
        ]

        if not all(key in row and row[key] for key in required_keys):
            continue  # Skip the current iteration if any key is missing or empty.

        try:
            trade_px = float(row["tradePx"])
            trade_amount = int(row["tradeAmt"])
            side = 1 if row["orderSide"] == "sell" else -1
            pnl = trade_px * trade_amount * side
        except ValueError:
            # Skip the current iteration if conversion fails.
            continue

        # For plotting the cumulative gross PnL.
        cumulative_pnl += pnl
        cumulative_pnls.append(cumulative_pnl)

        try:
            timestamp = (
                int(row["currentTime"]) / 10**9
            )  # Convert nanoseconds to seconds.
            timestamps.append(
                datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")
            )  # Format to display only time.
        except Exception as e:
            print(f"Error processing timestamp: {e}")
            continue

        security = row["orderProduct"]
        pnl_totals[security] = pnl_totals.get(security, 0) + pnl
        pnl_totals["Total"] += pnl

    return pnl_totals, cumulative_pnls, timestamps


# Function to draw the cumulative gross PnL over time.
def draw_cumulative_pnl(cumulative_pnls, timestamps):
    plt.figure(figsize=(10, 6))  # Larger figure size for better readability.
    plt.plot(
        cumulative_pnls, marker="o", linestyle="-", color="blue"
    )  # Enhanced plot aesthetics.
    plt.xlabel("Time")
    plt.ylabel("Cumulative Gross PnL")

    # Dynamically choose a reasonable number of xticks based on data length.
    max_labels = 20
    step = max(1, len(timestamps) // max_labels)

    # Selecting indices with np.
    selected_indices = np.arange(0, len(timestamps), step)

    # Approach without np, uncomment this and comment the above if you do not have it.
    # selected_indices = [i for i in range(0, len(timestamps), step)]

    selected_timestamps = [timestamps[i] for i in selected_indices]

    plt.xticks(
        selected_indices, selected_timestamps, rotation=45, ha="right"
    )  # Improved label formatting.
    plt.tight_layout()  # Adjust layout to prevent clipping of labels.
    plt.show()


if __name__ == "__main__":
    # Read in the data.
    filename = "test_logs.csv"
    data = read_csv(filename)

    # Calculate the results.
    total_pnl, cumulative_pnls, timestamps = calculate_total_gross_pnl(data)

    # 1. Calculate total gross PnL.
    print(f"Total Gross PnL: {total_pnl['Total']}")

    # 2. Calculate total gross PnL over each security ID.
    print("Total Gross PnL per Security:")
    for security, pnl in total_pnl.items():
        if security != "Total":
            print(f"- {security} : {pnl}")

    # 3. Draw cumulative gross PnL.
    draw_cumulative_pnl(cumulative_pnls, timestamps)
