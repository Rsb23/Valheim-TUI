from datetime import datetime

from data import InterpretData

from textual.app import App, ComposeResult
from textual.widgets import Collapsible, Label, Header, Footer


class StatusApp(App):
    CSS = """
    Screen { align: center middle; }
    Digits { width: auto; }
    """
    def __init__(self, driver_class = None, css_path = None, watch_css = False, ansi_color = False):
        super().__init__(driver_class, css_path, watch_css, ansi_color)

        self._InterpretData = InterpretData("./samplelog.txt")
        self.server_start_data = self._InterpretData.get_start_data()

    def compose(self) -> ComposeResult:  
        yield Header()
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
        with Collapsible(title=f"Connected Players: {self.server_start_data[7]}"):  # TODO: update this automatically with get_connection_count()       
            pass  # TODO: call get_players() and add collapsible for each with labels for name, playfab id, and steam id
        yield Footer()

    
if __name__ == "__main__":
    app = StatusApp()
    app.run()