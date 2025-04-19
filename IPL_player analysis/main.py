import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Step 1: Create a connection to your MySQL database
def create_database_connection():
    engine = create_engine('mysql+pymysql://ipl_user:ipl_pass123@localhost:3306/ipl_players_db')
    return engine

# Step 2: Load data from MySQL database into DataFrame
def load_data_from_db(engine):
    query = "SELECT Player_Name, Team, Age, Matches_Played, Runs, Wickets, Role FROM players"
    df = pd.read_sql(query, engine)
    
    # Remove duplicates based on Player_Name
    df = df.drop_duplicates(subset=['Player_Name'])
    
    print(f"Data loaded: {df.shape[0]} rows, {df.shape[1]} columns.")
    return df

# Step 3: Check and print the columns of the DataFrame
def check_columns(df):
    print("DataFrame Columns:", df.columns)

# Step 4: Compare two players based on selected stats (Runs or Wickets)
def compare_players(df, player1, player2, stat):
    stat = stat.capitalize()  # Make sure 'runs' -> 'Runs' and 'wickets' -> 'Wickets'
    
    player1_data = df[df['Player_Name'].str.lower() == player1.lower()][['Player_Name', stat]]
    player2_data = df[df['Player_Name'].str.lower() == player2.lower()][['Player_Name', stat]]

    # Merge the two dataframes to have the comparison in one table
    comparison = pd.concat([player1_data, player2_data])

    print(f"\n--- {stat.capitalize()} Comparison ---")
    print(comparison)

    # Plotting the bar graph for comparison
    plt.figure(figsize=(8, 5))
    plt.bar(comparison['Player_Name'], comparison[stat], color=['blue', 'orange'])
    plt.xlabel('Player Name')
    plt.ylabel(stat.capitalize())
    plt.title(f'{stat.capitalize()} Comparison: {player1} vs {player2}')
    plt.show()

# Step 5: Main function to run the entire process
def main():
    print("Starting the process...")
    
    # Create database connection
    engine = create_database_connection()
    
    # Load data from the MySQL database
    df = load_data_from_db(engine)
    
    # Check the columns of the DataFrame
    check_columns(df)
    
    # Display all players from the database (Batsman, Bowler, and All-rounder)
    print("\nAll Available Players:")
    print(df[['Player_Name', 'Team', 'Role']])

    # Step 6: Ask for player category (Batsman, Bowler, All-rounder)
    role = input("Select player category (Batsman / Bowler / All-rounder): ").strip()
    available_players = df[df['Role'].str.lower() == role.lower()]

    # Display available players based on selected role
    if not available_players.empty:
        print(f"\nAvailable {role}s:")
        print(available_players[['Player_Name', 'Team']])
    else:
        print(f"\nNo {role}s found in the database.")
    
    # Step 7: Get player names and comparison criteria from the user
    player1 = input("\nEnter first player name to compare: ")
    player2 = input("Enter second player name to compare: ")
    stat = input("Compare based on (Runs / Wickets): ").lower()

    # Validate user input for valid stats
    if stat not in ['runs', 'wickets']:
        print("Invalid stat. Please choose either 'runs' or 'wickets'.")
        return

    # Perform the comparison
    compare_players(df, player1, player2, stat)

if __name__ == "__main__":
    main()
