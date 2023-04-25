import json, requests
from nextcord import Member
from typing import Union
class Data:
    def __init__(self) -> None:
        with open("json/info.json", "r", encoding="UTF-8") as f:
            try: self.file = json.load(f)
            except: self.file = {}
    
    def push(self, id: int,  user_name: str, user_id: str = None) -> tuple[Union[int, str]]:
        req: dict = requests.get(f"https://ch.tetr.io/api/users/{user_id}").json()
        try: conn = req["data"]["user"]["connections"].get("discord", 0)
        except: return (404, "유저를 찾을수 없음")
        
        if conn:
            if str(id) != conn["id"]:
                return (400, "그거 너 아님")

            with open("json/info.json", "w", encoding="UTF-8") as f:
                a = self.file.get(str(id), 0)
                self.file[str(id)] = req["data"]["user"]
                self.file[str(id)]["nick"] = user_name
                json.dump(self.file, f, indent=4, ensure_ascii=False)
                if a: return (200, "변경사항 저장 성공")
            return (200, "성공")
        return (500, "discord계정을 연결안함")
        

if __name__ == "__main__":
    print(Data().push(577266050769485844, "hb", "5-23"))