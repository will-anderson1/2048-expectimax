import csv

# Define the path to your CSV file
file_path = 'results.csv'

# Initialize your data structure
countMaxTiles = {
    1: {2048: [0, 0], 1024: [0, 0], 512: [0, 0], "totalScore": 0, "totalTime": 0, "totalMoveCount": 0},
    2: {2048: [0, 0], 1024: [0, 0], 512: [0, 0], "totalScore": 0, "totalTime": 0, "totalMoveCount": 0},
    3: {2048: [0, 0], 1024: [0, 0], 512: [0, 0], "totalScore": 0, "totalTime": 0, "totalMoveCount": 0},
    4: {2048: [0, 0], 1024: [0, 0], 512: [0, 0], "totalScore": 0, "totalTime": 0, "totalMoveCount": 0}
}

# Open the CSV file and process each line
with open(file_path, 'r', newline='') as file:
    csv_reader = csv.reader(file)
    headers = next(csv_reader)  # Skip the header row
    headers = [header.strip() for header in headers]  # Clean up header names

    for row in csv_reader:
        row = [item.strip() for item in row]  # Strip spaces from data
        heuristic = row[0].lower()
        depth = int(row[3])
        maxTile = int(row[7])
        steps = int(row[8])
        score = int(row[6])
        time = float(row[1])

        # Determine the experiment number
        if heuristic == 'default':
            experimentNum = 1 if depth == 6 else 2
        else:
            experimentNum = 3 if depth == 6 else 4

        # Update counters based on maxTile
        if maxTile in countMaxTiles[experimentNum]:
            countMaxTiles[experimentNum][maxTile][0] += 1
            countMaxTiles[experimentNum][maxTile][1] += steps

        # Update other statistics
        countMaxTiles[experimentNum]["totalScore"] += score
        countMaxTiles[experimentNum]["totalTime"] += time
        countMaxTiles[experimentNum]["totalMoveCount"] += steps

# Print the formatted results
for i in range(1, 5):
    data = countMaxTiles[i]
    avg_move_time = data["totalTime"] / max(data["totalMoveCount"], 1)  # Avoid division by zero
    print(f"Experiment {i}:")
    print(f"  2048 Tile Count: {data[2048][0]}, Average Moves for 2048: {data[2048][1] / max(data[2048][0], 1):.2f}")
    print(f"  1024 Tile Count: {data[1024][0]}, Average Moves for 1024: {data[1024][1] / max(data[1024][0], 1):.2f}")
    print(f"  512 Tile Count: {data[512][0]}, Average Moves for 512: {data[512][1] / max(data[512][0], 1):.2f}")
    print(f"  Average Score: {data['totalScore'] / 25:.2f}")
    print(f"  Average Total Time: {data['totalTime'] / 25:.2f} seconds")
    print(f"  Average Move Time: {avg_move_time:.2f} seconds per move")
    print(f"  Average Total Moves: {data['totalMoveCount'] / 25:.2f}")
    print()