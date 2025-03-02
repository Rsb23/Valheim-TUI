from datetime import datetime

from data import InterpretData

from art import text2art

from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalGroup
from textual.widgets import Collapsible, Label, Header, Footer, Static
from textual.color import Color


class StatusApp(App):
    CSS_PATH = "main.tcss"

    def __init__(self, driver_class = None, css_path = None, watch_css = False, ansi_color = False):
        super().__init__(driver_class, css_path, watch_css, ansi_color)    

        self._InterpretData = InterpretData("./samplelog2.txt")  # FOR TESTING: use samplelog2.txt for 1 player connection, and samplelog.txt for no players connected

        self.server_start_data = self._InterpretData.get_start_data()
        self.server_start_timestamp = self.server_start_data[7]

        self.theme = "tokyo-night"

    def compose(self) -> ComposeResult:  
        yield Header()
        yield Static(text2art("Valheim"), id="title_1_label")
        yield Static(text2art("Server Dashboard"), id="title_2_label")    
        with Collapsible(title="General"):
            yield Label(f"Started: {self.server_start_timestamp}", id="server_started_label")
            yield Label("Uptime: ", id="server_uptime_label")  # updated later by update_server_uptime()
            yield Label("\n")
            with Collapsible(title="Server Details"):
                yield Label(f"Loaded World: {self.server_start_data[0]}")
                yield Label(f"Server Steam ID: {self.server_start_data[1]}")
                yield Label(f"Server ID: {self.server_start_data[2]}")      
                yield Label(f"Valheim Version: {self.server_start_data[3]}")
                yield Label(f"Network Version: {self.server_start_data[4]}")
            with Collapsible(title="Joining"):
                yield Label(f"Join Code: {self.server_start_data[5]}")
                yield Label(f"External IP/PORT: {self.server_start_data[6]}")

        with Collapsible(title=f"Connected Players: {self._InterpretData.get_connection_count()}", id="players_collapsible", disabled=True):      
            yield VerticalGroup(id="players_vertical_group")

        # https://stackoverflow.com/questions/78814860/adding-status-text-to-a-textual-footer
        with Horizontal(id="footer_outer"):
            with Horizontal(id="footer_inner"):
                yield Footer()
            yield Label(f"Last Updated: {datetime.now().time()}", id="last_updated_label")
                    
    def on_mount(self) -> None:
        self.set_interval(1 / 30, self.update_all)
    
    def update_all(self) -> None:
        self.update_player_count()
        self.update_server_uptime()
        self.update_last_updated_label()
    
    def update_player_count(self) -> None:
        player_count = self._InterpretData.get_connection_count()

        self.query_one("#players_collapsible").title = f"Connected Players: {player_count}"

        if player_count > 0:
            self.get_widget_by_id("players_collapsible").disabled = False
            self.update_player_list()
        elif player_count == 0:
            self.get_widget_by_id("players_collapsible").disabled = True
        else:
            raise ValueError("Can't have negative players!")
    
    def update_player_list(self):
        data = self._InterpretData.get_players()

        vertical_group = self.query_one("#players_vertical_group", VerticalGroup)

        # clear players_collapsible of possible previous before adding current players
        vertical_group.remove_children()

        for index, playfab_id in enumerate(data[0]):
            if len(data[0]) != 0:                    
                vertical_group.mount(Label(f"{data[2][index]}\n\tJoined: {data[3][index]}\n\tPlaying For: {datetime.now() - datetime.strptime(data[3][index], '%m/%d/%Y %H:%M:%S')}\n\tSteam ID: {data[1][index]}\n\tPlayfab ID: {data[0][index]}", classes="player_info_label"))  # name, join time, connection time (derived from join time), steam_id, playfab_id, TODO: maybe make this another collapsible with the name as title and ids under)
    
    def update_server_uptime(self) -> None:
        self.get_widget_by_id("server_uptime_label").update(f"Server Uptime: {datetime.now() - datetime.strptime(self.server_start_timestamp, '%m/%d/%Y %H:%M:%S')}")
    
    def update_last_updated_label(self) -> None:
        self.get_widget_by_id("last_updated_label").update(f"Last Updated: {datetime.now().time()}")

    
if __name__ == "__main__":
    app = StatusApp()
    app.run()