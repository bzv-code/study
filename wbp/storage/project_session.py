from pathlib import Path
from datetime import datetime



class ProjectSession:


    def __init__(
            self
    ):


        folder = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )


        self.path = (

            Path(__file__)
            .parent
            .parent
            /
            "data"
            /
            "sessions"
            /
            folder

        )


        self.path.mkdir(
            parents=True,
            exist_ok=True
        )



    def file(
            self,
            name
    ):

        return self.path / name