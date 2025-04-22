import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Step 1: Create MySQL database connection
def create_database_connection():
    engine = create_engine('mysql+pymysql://ipl_user:ipl_pass123@localhost:3306/ipl_players_db')
    return engine

# Step 2: Load CSV into MySQL
def load_csv_to_mysql(engine, csv_path):
    df = pd.read_csv(csv_path)
    df.to_sql("players", con=engine, if_exists='replace', index=False)
    print("✅ CSV data loaded into MySQL 'players' table.")

# Step 3: Load data from MySQL into DataFrame
def load_data_from_db(engine):
    query = "SELECT Player_Name, Team, Age, Matches_Played, Runs, Wickets, Role FROM players"
    df = pd.read_sql(query, engine)
    df = df.drop_duplicates(subset=['Player_Name'])
    print(f"✅ Data loaded: {df.shape[0]} rows, {df.shape[1]} columns.")
    return df

# Step 4: Display column names
def check_columns(df):
    print("📋 DataFrame Columns:", df.columns.tolist())

# Step 5: Compare two players and plot results
def compare_players(df, player1, player2, stat):
    stat = stat.capitalize()
    player1_data = df[df['Player_Name'].str.lower() == player1.lower()][['Player_Name', stat]]
    player2_data = df[df['Player_Name'].str.lower() == player2.lower()][['Player_Name', stat]]
    comparison = pd.concat([player1_data, player2_data])

    print(f"\n📊 --- {stat} Comparison ---")
    print(comparison)

    plt.figure(figsize=(8, 5))
    plt.bar(comparison['Player_Name'], comparison[stat], color=['blue', 'orange'])
    plt.xlabel('Player Name')
    plt.ylabel(stat)
    plt.title(f'{stat} Comparison: {player1} vs {player2}')
    plt.tight_layout()
    plt.show()

# Step 6: Main execution
def main():
    print("🚀 Starting IPL Player Comparator...")

    engine = create_database_connection()

    # Load data from CSV to MySQL
    csv_path = csv_path = "C:/Users/91812/OneDrive/Desktop/IPL_player analysis/ipl_players.csv"  # Use uploaded file path
    load_csv_to_mysql(engine, csv_path)

    # Load data from MySQL
    df = load_data_from_db(engine)
    check_columns(df)

    # Show all available players
    print("\n📋 All Available Players:")
    print(df[['Player_Name', 'Team', 'Role']])

    # Choose role
    role = input("\n🔎 Select player category (Batsman / Bowler / All-rounder): ").strip()
    available_players = df[df['Role'].str.lower() == role.lower()]

    if not available_players.empty:
        print(f"\n👥 Available {role}s:")
        print(available_players[['Player_Name', 'Team']])
    else:
        print(f"❌ No {role}s found.")
        return

    # Input player names and stat
    player1 = input("\n👤 Enter first player name to compare: ")
    player2 = input("👤 Enter second player name to compare: ")
    stat = input("📈 Compare based on (Runs / Wickets): ").lower()

    if stat not in ['runs', 'wickets']:
        print("❌ Invalid stat. Choose 'runs' or 'wickets'.")
        return

    compare_players(df, player1, player2, stat)

if __name__ == "__main__":
    main()

