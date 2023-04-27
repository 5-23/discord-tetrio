import json, requests
from nextcord import Member
from typing import Union
import math
import tetrio
from .clan import Clan
class User:
    def __init__(self) -> None:
        with open("json/info.json", "r", encoding="UTF-8") as f:
            try: self.file = json.load(f)
            except: self.file = {}
    
    def change_clan(self, id: int, name: str):
        self.file[str(id)]["clan"] = name
        
        with open("json/info.json", "w", encoding="UTF-8") as f:
            json.dump(self.file, f, indent=4, ensure_ascii=False)

    def push(self, id: int,  user_nick: str, user_id: str = None) -> tuple[Union[int, str]]:
        URL = f"https://ch.tetr.io/api/users/{user_id.lower()}"
        
        req: dict = requests.get(URL).json()
        try: conn = req["data"]["user"]["connections"].get("discord", 0)
        except:
            print(URL)
            return (404, "유저를 찾을수 없음")
        
        try: records: dict = requests.get(f"{URL}/records").json()["data"]["records"]
        except: ...
        
        if conn:
            if str(id) != conn["id"]:
                return (400, "그거 너 아님")

            a = self.file.get(str(id), 0)
            data = req["data"]["user"]
            self.file[str(id)] = {

                "name":          data["username"],
                "nick":          user_nick,
                "discord_name":  conn["username"],
                "friend":        data["friend_count"],
                "gametime":      math.ceil(data["gametime"]),
                "gameplayed":    data["gamesplayed"],
                "gamewon":       data["gameswon"],
                
                "badges": [  { "title": badge["id"], "description": badge["label"] } for badge in data["badges"]  ],

                "league": {
                    "rank":       data["league"]["rank"],
                    "best_rank":  data["league"].get("bestrank", "z"),
                    "rating":     math.ceil(data["league"]["rating"]),
                    "apm":        data["league"]["apm"],
                    "pps":        data["league"]["pps"],
                    "vs":         data["league"]["vs"],
                },

                "40l": {
                    "time": math.ceil(records.get("40l", {}).get("record", {}).get("endcontext", {}).get("finalTime", 0)/1000.),
                    "point": None,
                    "ts": records.get("40l", {}).get("record", {}).get("ts", "0.0").split(".")[0],
                    "ok": records.get("40l", 0) != 0,
                },

                "blitz": {
                    "time": None,
                    "point": records.get("blitz", {}).get("record", {}).get("endcontext", {}).get("score", 0),
                    "ts": records.get("blitz", {}).get("record", {}).get("ts", "0.0").split(".")[0],
                    "ok": records.get("blitz", 0) != 0,
                },



                "avatar_img": f"https://tetr.io/user-content/avatars/{data['_id']}.jpg?rv={data.get('avatar_revision', '')}",
                "banner_img": f"https://tetr.io/user-content/banners/{data['_id']}.jpg?rv={data.get('banner_revision', '')}",
                "clan": self.file.get(str(id), {}).get("clan", None)
            }

            with open("json/info.json", "w", encoding="UTF-8") as f:
                json.dump(self.file, f, indent=4, ensure_ascii=False)
                if a: return (200, "변경사항 저장 성공")
            return (200, "성공")
        return (500, "discord계정을 연결안함")

    def add_clan(self, id: int, clan: tetrio.Clan):
        
        self.file[str(id)]["clan"] = clan.name
        Clan().push_user(clan.name, id)
        with open("json/info.json", "w", encoding="UTF-8") as f:
            json.dump(self.file, f, indent=4, ensure_ascii=False)
        
    def get(self, id: int) -> tetrio.Data:
        data = self.file[str(id)]
        return tetrio.Data(
            name         = data["name"],
            nick         = data["nick"],
            discord_name = data["discord_name"],
            friend       = data["friend"],
            gametime     = data["gametime"],
            gameplayed   = data["gameplayed"],
            gamewon      = data["gamewon"],
                    
            badges       = [  tetrio.Badge(title = badge["title"], description = ["description"]) for badge in data["badges"]  ],

            league       = tetrio.League(
                rank          = data["league"]["rank"],
                best_rank     = data["league"]["best_rank"],
                rating        = data["league"]["rating"],
                apm           = data["league"]["apm"],
                pps           = data["league"]["pps"],
                vs            = data["league"]["vs"],
            ),


            l40          = tetrio.Solo(
                time          = data["40l"]["time"],
                point         = data["40l"]["point"],
                ts            = data["40l"]["ts"],
                ok            = data["40l"]["ok"],
            ),
            blitz        = tetrio.Solo(
                time          = data["blitz"]["time"],
                point         = data["blitz"]["point"],
                ts            = data["blitz"]["ts"],
                ok            = data["blitz"]["ok"],
            ),

            avatar_img   = data["avatar_img"],
            banner_img   = data["banner_img"],
            clan         = data["clan"],

        )