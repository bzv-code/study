from pathlib import Path

from datetime import datetime



class BrowserSessionChecker:


    def __init__(
            self,
            session_dir,
            refresh_hours
    ):

        self.session_dir = Path(
            session_dir
        )

        self.refresh_hours = refresh_hours



    def is_valid(self):


        files = [

            "cookies.json",

            "headers.json",

            "api.json"

        ]



        for file in files:


            path = (

                self.session_dir
                /
                file

            )


            if not path.exists():

                return False



        modified = datetime.fromtimestamp(

            self.session_dir.stat().st_mtime

        )



        age = (

            datetime.now()

            -

            modified

        ).total_seconds() / 3600



        return age < self.refresh_hours