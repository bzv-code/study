import json

from pathlib import Path
from datetime import datetime



TOKEN_FILE = (

    Path(__file__)
    .parent
    .parent
    / "data"
    / "cookies.json"

)



class TokenStorage:



    def save(
            self,
            token,
            cookies,
            user_agent
    ):


        data = {


            "token": token,


            "cookies": cookies,


            "user_agent": user_agent,


            "created_at": datetime.now().isoformat()


        }



        TOKEN_FILE.parent.mkdir(

            exist_ok=True

        )



        with open(

                TOKEN_FILE,

                "w",

                encoding="utf-8"

        ) as f:



            json.dump(

                data,

                f,

                ensure_ascii=False,

                indent=4

            )



        print(

            f"Токен сохранен: {TOKEN_FILE}"

        )




    def load(self):


        if not TOKEN_FILE.exists():


            print(

                "Файл cookies.json отсутствует"

            )


            return None




        with open(

                TOKEN_FILE,

                encoding="utf-8"

        ) as f:


            data = json.load(f)




        if not data.get("token"):


            print(

                "В cookies.json нет токена"

            )


            return None



        return data




    def clear(self):


        if TOKEN_FILE.exists():


            TOKEN_FILE.unlink()


            print(

                "Старый токен удален"

            )