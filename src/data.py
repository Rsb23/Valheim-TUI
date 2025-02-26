import re


class InterpretData():
    def __init__(self, pathToData: str) -> None:
        self.filePath = pathToData

        # global variables that will remain static, the dynamic ones are given individual functions so they can be called more often because they change the only the most recent one is the true one, no point in storing variables for that
        self.loaded_world_name = ""
        self.server_steam_ID = ""
        self.valheim_version = ""
        self.network_version = ""
        self.join_code = ""
        self.external_ip_port = ""
    
    def get_start_data(self) -> list:
        """
        
        """
        with open(self.filePath, "r") as file:
            fileLines = file.readlines()
            file.close()
        
        for index, line in enumerate(fileLines):
            # specific regex pattern(s) for match_server_start
            match_join_code = re.compile("[0-9][0-9][0-9][0-9][0-9][0-9]")
            match_ip = re.compile("[0-9][0-9].[0-9][0-9].[0-9][0-9][0-9].[0-9][0-9][0-9]:[0-9][0-9][0-9][0-9]")
            match_players = re.compile("[0-9] player\(s\)")
            match_players_count = re.compile("[0-9]")

            # specific regex pattern(s) for match_new_player
            match_playfab_ID = re.compile("[0-9][0-9][0-9][0-9][0-9][A-Z][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]")
            match_steam_ID = re.compile("[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]")

            # specific regex pattern(s) for match_character_name
            match_character_name = re.compile("(?<=Got character ZDOID from )(.*)( :)")

            # specific regex pattern(s) for match_connections
            match_connections_count = re.compile(" [0-10] ")

            # general regex_pattern(s)
            match_timestamp = re.compile("[0-1][0-9]/[0-3][0-9]/202[5-9] [0-2][0-2]:[0-5][0-9]:[0-5][0-9]")

            # oneshot regex (directly returns the data as opposed to identifying the line and then doing that)
            match_world_name = re.compile("([0-1][0-9]/[0-3][0-9]/202[5-9] [0-2][0-2]:[0-5][0-9]:[0-5][0-9]: Get create world )(.*)")
            match_server_steam_ID = re.compile("([0-1][0-9]/[0-3][0-9]/202[5-9] [0-2][0-2]:[0-5][0-9]:[0-5][0-9]: Using steam APPID:)(.*)")
            match_server_ID = re.compile("([0-1][0-9]/[0-3][0-9]/202[5-9] [0-2][0-2]:[0-5][0-9]:[0-5][0-9]: Server ID )(.*)")
            match_valheim_version = re.compile("([0-1][0-9]/[0-3][0-9]/202[5-9] [0-2][0-2]:[0-5][0-9]:[0-5][0-9]: Valheim version: )(.*) (\(network version [0-9][0-9]\))")

            # main regex patterns to find
            match_server_start = re.compile("[0-1][0-9]/[0-3][0-9]/202[5-9] [0-2][0-2]:[0-5][0-9]:[0-5][0-9]: Session \"Thy Quaint Little Village\" with")
            
            match_new_player = re.compile("[0-1][0-9]/[0-3][0-9]/202[5-9] [0-2][0-2]:[0-5][0-9]:[0-5][0-9]: PlayFab socket with remote ID playfab")
            match_new_character = re.compile("[0-1][0-9]/[0-3][0-9]/202[5-9] [0-2][0-2]:[0-5][0-9]:[0-5][0-9]: Got character ZDOID from")
            
            match_world_saved = re.compile("[0-1][0-9]/[0-3][0-9]/202[5-9] [0-2][0-2]:[0-5][0-9]:[0-5][0-9]: World saved")
            
            if match_world_name.match(line):
                print(f"Loaded World: {match_world_name.match(line).groups()[1]}")
            
            elif match_server_steam_ID.match(line):
                print(f"Server Steam ID: {match_server_steam_ID.match(line).groups()[1]}")
            
            elif match_server_ID.match(line):
                print(f"Server ID: {match_server_ID.match(line).groups()[1]}")

            elif match_valheim_version.match(line):
                print(f"Valheim Version: {match_valheim_version.match(line).groups()[1]}")

                match_network_version = re.compile("(network version )(.*)(\))")
                print(f"Network Version: {match_network_version.search(line).groups()[1]}")

            elif match_server_start.match(line):
                result_match_join_code = match_join_code.search(line)
                if result_match_join_code:
                    print(f"Join Code: {result_match_join_code.group()}")

                result_match_ip = match_ip.search(line)
                if result_match_ip:
                    print(f"External IP/PORT: {result_match_ip.group()}")

                result_match_players = match_players.search(line)
                if result_match_players:
                    result_match_players_count = match_players_count.match(line)
                    if result_match_players_count:
                        print(f"Starting Players: {result_match_players_count.group().strip()}")

            elif match_new_player.match(line):
                playfab_ID = match_playfab_ID.search(line).group()
                steam_ID = match_steam_ID.search(line).group()
                print(f"New Player")
                print(f"\tPlayFab ID: {playfab_ID}")
                print(f"\tSteam   ID: {steam_ID}")
            
            elif match_new_character.match(line):
                print(f"Character Name: {match_character_name.search(line).groups()[0]}")
            
            elif match_connections.match(line):
                results_match_connections = match_connections.search(line)
                if results_match_connections:
                    results_match_connections_count = match_connections_count.search(line)
                    if results_match_connections_count:
                        print(f"Players: {results_match_connections_count.group().strip()}")
            
            elif match_world_saved.match(line):
                world_save_timestamp = match_timestamp.match(line).group()
                print(f"World Last Saved: {world_save_timestamp}")
        
        def get_player_count(self) -> int:
            player_count = 0

            match_connections = re.compile("[0-1][0-9]/[0-3][0-9]/202[5-9] [0-2][0-2]:[0-5][0-9]:[0-5][0-9]:  Connections")
            match_connections_count = re.compile(" [0-10] ")
            
            with open(self.filePath, "r") as file:
                fileLines = file.readlines()
                file.close()

            for line in fileLines:
                if match_connections.match(line):
                    player_count = int(match_connections_count.search(line).group().strip())
            
            return player_count



            


_InterpretData = InterpretData("/home/r34_runna/Documents/python/Valheim-TUI/samplelog.txt")
_InterpretData.get_data()
print(_InterpretData.get_player_count())
