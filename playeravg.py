import requests
from bs4 import BeautifulSoup

# Function to format player's name and draft order into a URL-friendly string.
def convert_name(plr, draft_order):
    if len(str(draft_order)) == 1:
        draft_order = "0" + str(draft_order)
    if "'" in plr:
        plr = plr.replace("'", "")
    if "-" in plr:
        plr = plr.replace("-", "")
    plr_li = plr.split(' ')
    # Make the player string based on the format on the website.
    plr_str = plr_li[1][:5].lower() + plr_li[0][:2].lower() + str(draft_order) + ".html" if len(plr_li[1]) > 5 else plr_li[1].lower() + plr_li[0][:2].lower() + str(draft_order) + ".html"
    return plr_str

# Converts the season input into a string to be put in the link.
def convert_season(season):
    return f"{season-1}-{season}" if len(str(season)) == 4 else "0" if season == 0 else None

# Function to get the HTML content of a given URL.
def get_page(url):
    response = requests.get(url)
    return response.text

# Function to parse the HTML content and extract player statistics.
def parse(bbr, season):
    soup = BeautifulSoup(bbr, "lxml")
    # Find the specific table row with the season's data.
    avgs_szn = soup.find("tr", id=f"per_game.{season.split('-')[1]}") if season != "0" else soup.find("div", id="all_per_game-playoffs_per_game").find("tfoot")
    # Extracting and storing the statistics in a dictionary.
    stats = {
        "NAME": soup.find("div", id="info").find("span").text,
        "PPG": avgs_szn.find("td", {"data-stat": "pts_per_g"}).text,
        "APG": avgs_szn.find("td", {"data-stat": "ast_per_g"}).text,
        "RPG": avgs_szn.find("td", {"data-stat": "trb_per_g"}).text,
        "SPG": avgs_szn.find("td", {"data-stat": "stl_per_g"}).text,
        "BPG": avgs_szn.find("td", {"data-stat": "blk_per_g"}).text,
        "TOPG": avgs_szn.find("td", {"data-stat": "tov_per_g"}).text,
        "MPG": avgs_szn.find("td", {"data-stat": "mp_per_g"}).text
    }
    # Adding additional information for career statistics.
    if season == "0":
        stats["seasons_played"] = len(soup.find("div", id="all_per_game-playoffs_per_game").find("tbody").find_all("th", {"data-stat": "season"}))
    return stats

# Function to create and print the output based on the parsed data.
def create_output(data, stats, season):
    title_str = f"{stats['NAME']}'s Career Averages" if season == "0" else f"{stats['NAME']}'s {season} Averages"
    print(title_str)
    for key, value in stats.items():
        if key != 'NAME':
            print(f"{key}: {value}")

# Main function to handle the overall process: input, processing, and output.
def averages(player, draft_order=1, season=0):
    plr_str = convert_name(player, draft_order)
    plr_szn = convert_season(season)
    data = get_page(f"https://www.basketball-reference.com/players/{plr_str[0]}/{plr_str}")
    stats = parse(data, plr_szn)
    create_output(data, stats, plr_szn)

if __name__ == "__main__":
    # Taking user input for player's name, draft order, and season.
    player = input("Enter player's name: ")
    draft_order = int(input("Enter draft order (default 1): ") or "1")
    season = int(input("Enter season (default current year): ") or "0")
    averages(player, draft_order, season)
