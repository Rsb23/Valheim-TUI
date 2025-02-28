from datetime import datetime

from data import InterpretData

from art import text2art

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Collapsible, Label, Header, Footer, Static


class StatusApp(App):
    CSS_PATH = "main.tcss"

    def __init__(self, driver_class = None, css_path = None, watch_css = False, ansi_color = False):
        super().__init__(driver_class, css_path, watch_css, ansi_color)    

        self._InterpretData = InterpretData("./samplelog.txt")

        self.server_start_data = self._InterpretData.get_start_data()

        self.theme = "tokyo-night"

    def compose(self) -> ComposeResult:  
        yield Header()
        yield Static(text2art("Valheim"), id="title_1_label")
        yield Static(text2art("Server Dashboard"), id="title_2_label")    
        with Collapsible(title="General"):
            with Collapsible(title="Server Details"):
                yield Label(f"Loaded World: {self.server_start_data[0]}")
                yield Label(f"Server Steam ID: {self.server_start_data[1]}")
                yield Label(f"Server ID: {self.server_start_data[2]}")      
                yield Label(f"Valheim Version: {self.server_start_data[3]}")
                yield Label(f"Network Version: {self.server_start_data[4]}")
            with Collapsible(title="Joining"):
                yield Label(f"Join Code: {self.server_start_data[5]}")
                yield Label(f"External IP/PORT: {self.server_start_data[6]}")

        with Collapsible(title=f"Connected Players: {self._InterpretData.get_connection_count()}", id="players_collapsible", disabled=True):  # TODO: update this automatically with get_connection_count()       
            pass  # TODO: call get_players() and add collapsible for each with labels for name, playfab id, and steam id

        # https://stackoverflow.com/questions/78814860/adding-status-text-to-a-textual-footer
        with Horizontal(id="footer_outer"):
            with Horizontal(id="footer_inner"):
                yield Footer()
            yield Label(f"Last Updated: {datetime.now().time()}", id="last_updated_label")  # TODO: update automatically
        
    def on_mount(self) -> None:
        self.set_interval(1 / 60, self.update_all)

    def update_all(self) -> None:
        self.update_player_count()
        # TODO: add more here

        self.update_last_updated_label()
    
    def update_player_count(self) -> None:
        player_count = self._InterpretData.get_connection_count()

        if player_count > 0:
            self.get_widget_by_id("players_collapsible").disabled = False
            # self.update_player_list() TODO: implement
        elif player_count == 0:
            self.get_widget_by_id("players_collapsible").disabled = True
        else:
            raise ValueError("Can't have negative players!")
    
    def update_player_list(self) -> None:
        pass

    def update_last_updated_label(self) -> None:
        self.get_widget_by_id("last_updated_label").update(f"Last Updated: {datetime.now().time()}")



    
if __name__ == "__main__":
    app = StatusApp()
    app.run()