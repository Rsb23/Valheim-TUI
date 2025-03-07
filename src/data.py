import re


class InterpretData():
    def __init__(self, pathToData: str) -> None:
        self.filePath = pathToData
    
    def get_start_data(self) -> tuple:
        """
        
        """
        with open(self.filePath, "r") as file:
            fileLines = file.readlines()
            file.close()
        
        for line in fileLines:
            match_join_code = re.compile("[0-9][0-9][0-9][0-9][0-9][0-9]")
            match_ip = re.compile("[0-9][0-9].[0-9][0-9].[0-9][0-9][0-9].[0-9][0-9][0-9]:[0-9][0-9][0-9][0-9]")

            match_timestamp = re.compile("[0-1][0-9]/[0-3][0-9]/202[5-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]") 

            match_world_name = re.compile("([0-1][0-9]/[0-3][0-9]/202[5-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]: Get create world )(.*)")
            match_server_steam_ID = re.compile("([0-1][0-9]/[0-3][0-9]/202[5-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]: Using steam APPID:)(.*)")
            match_server_ID = re.compile("([0-1][0-9]/[0-3][0-9]/202[5-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]: Server ID )(.*)")
            match_valheim_version = re.compile("([0-1][0-9]/[0-3][0-9]/202[5-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]: Valheim version: )(.*) (\(network version [0-9][0-9]\))")

            # main regex pattern
            match_server_start = re.compile("[0-1][0-9]/[0-3][0-9]/202[5-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]: Session \"Thy Quaint Little Village\" with")             
            
            if match_world_name.match(line):
                world_name = match_world_name.match(line).groups()[1]

                server_start_timestamp = match_timestamp.search(line).group()
            
            elif match_server_steam_ID.match(line):
                server_steam_ID = match_server_steam_ID.match(line).groups()[1]
            
            elif match_server_ID.match(line):
                server_ID = match_server_ID.match(line).groups()[1]

            elif match_valheim_version.match(line):
                valheim_version = match_valheim_version.match(line).groups()[1]

                match_network_version = re.compile("(network version )(.*)(\))")
                network_version = match_network_version.search(line).groups()[1]

            elif match_server_start.match(line):
                result_match_join_code = match_join_code.search(line)
                if result_match_join_code:
                    join_code = result_match_join_code.group()

                result_match_ip = match_ip.search(line)
                if result_match_ip:
                    ip_port = result_match_ip.group()
        
        return (world_name, server_steam_ID, server_ID, valheim_version, network_version, join_code, ip_port, server_start_timestamp)

        
    def get_players(self) -> tuple[list]:
        player_playfab_ids = []
        player_steam_ids = []
        character_names = []
        join_times = []
        
        match_player_join = re.compile("[0-1][0-9]/[0-3][0-9]/202[5-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]: PlayFab socket with remote ID playfab")
        match_player_leave = re.compile("[0-1][0-9]/[0-3][0-9]/202[5-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]: Keep socket for playfab/")
        
        match_playfab_ID = re.compile("[0-1][0-9]/[0-3][0-9]/202[5-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]: (PlayFab socket with remote ID playfab/)(.*)( received local Platform ID)")
        match_steam_ID = re.compile("[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]")
        
        match_new_character = re.compile("[0-1][0-9]/[0-3][0-9]/202[5-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]: Got character ZDOID from")    
        match_character_name = re.compile("(?<=Got character ZDOID from )(.*)( :)")
        match_timestamp = re.compile("[0-1][0-9]/[0-3][0-9]/202[5-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]")

        with open(self.filePath, "r") as file:
            fileLines = file.readlines()
            file.close()

        for line in fileLines:
             if match_player_join.match(line):
                 player_playfab_ids.append(match_playfab_ID.search(line).groups()[1])
                 player_steam_ids.append(match_steam_ID.search(line).group())
                 join_times.append(match_timestamp.search(line).group())
             elif match_new_character.match(line):
                 character_names.append(match_character_name.search(line).groups()[0])
             elif match_player_leave.match(line):
                 leaving_player_playfab_id = match_playfab_ID.search(line).group()
                 for index, id in enumerate(player_playfab_ids):
                     if id == leaving_player_playfab_id:
                         player_steam_ids.pop(index)
                         character_names.pop(index)
                         join_times.pop(index)
                         player_playfab_ids.pop(index)
         
        return (player_playfab_ids, player_steam_ids, character_names, join_times)
        
    def get_connection_count(self) -> int:
        player_count = 0

        match_connections = re.compile("[0-1][0-9]/[0-3][0-9]/202[5-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]:  Connections")
        match_connections_count = re.compile(" [0-10] ")
        
        with open(self.filePath, "r") as file:
            fileLines = file.readlines()
            file.close()

        for line in fileLines:
            if match_connections.match(line):
                player_count = int(match_connections_count.search(line).group().strip())
        
        return player_count

    def get_last_save(self) -> str:
        last_save = ""

        match_world_saved = re.compile("[0-1][0-9]/[0-3][0-9]/202[5-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]: World saved")
        match_timestamp = re.compile("[0-1][0-9]/[0-3][0-9]/202[5-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]")

        with open(self.filePath, "r") as file:
            fileLines = file.readlines()
            file.close()
        
        for line in fileLines:
            if match_world_saved.match(line):
                last_save = match_timestamp.match(line).group()

        return last_save

_InterpretData = InterpretData("samplelog3.txt")
print(_InterpretData.get_players())