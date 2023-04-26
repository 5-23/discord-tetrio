import json, tetrio

class Clan:
    def __init__(self) -> None:
        with open("json/clan.json", "r", encoding="UTF-8") as f:
            try: self.file = json.load(f)
            except: self.file = {}

    def push_user(self, name: str, id: int):
        self.file[name]["members"].append(id)
        with open("json/clan.json", "w", encoding="UTF-8") as f:
            json.dump(self.file, f, indent=4, ensure_ascii=False)

        

    def push(self, id: int , name: str, des: str,  rating: str, pw: str = None) -> tuple[int, str]:
        with open("json/info.json", "r", encoding="UTF-8") as f:j = json.load(f)
        j[str(id)]["clan"] = name
        
        if rating != "":
            try:
                int(rating)
            except: return (505, "레이팅이 숫자가 아님")

        if self.file.get(name, 0): return (500, "이미있는 이름")
        if pw == "":
            pw = None

        self.file[name] = {
            "name": name,
            "des": des,
            "rating": int(rating),
            "members": [id],
            "admin": id,
            "pw": pw,
        }

        with open("json/clan.json", "w", encoding="UTF-8") as f:
            json.dump(self.file, f, indent=4, ensure_ascii=False)
        
        with open("json/info.json", "w", encoding="UTF-8") as f:
            json.dump(j, f, indent=4, ensure_ascii=False)
        
        return (200, "성공")

    def get(self, name: int) -> tetrio.Clan:
        data = self.file[str(name)]
        return tetrio.Clan(
            name    = data["name"],
            des     = data["des"],
            rating  = data["rating"],
            members = data["members"],
            admin   = data["admin"],
            pw      = data["pw"],
        )