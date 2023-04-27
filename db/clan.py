import json, tetrio

class Clan:
    # from .user import User
    def __init__(self) -> None:
        with open("json/clan.json", "r", encoding="UTF-8") as f:
            try: self.file = json.load(f)
            except: self.file = {}

    def push_user(self, name: str, id: int):
        self.file[name]["members"].append(id)
        with open("json/clan.json", "w", encoding="UTF-8") as f:
            json.dump(self.file, f, indent=4, ensure_ascii=False)

    def delete(self, user, name: str):
        data = self.get(name)
        del self.file[name]
        for member in data.members:
            user().change_clan(member, None)

        with open("json/clan.json", "w", encoding="UTF-8") as f:
            json.dump(self.file, f, indent=4, ensure_ascii=False)
    
    def change(self, user, org_name: str, admin: int , name: str, des: str,  rating: str, pw: str, members: list[int]):
        del self.file[org_name]
        self.push(admin, name, des, rating, pw)

        for member in members:
            user().change_clan(member, name)

        with open("json/clan.json", "w", encoding="UTF-8") as f:
            json.dump(self.file, f, indent=4, ensure_ascii=False)
    

    def push(self, admin: int , name: str, des: str,  rating: str, pw: str = None) -> tuple[int, str]:
        with open("json/info.json", "r", encoding="UTF-8") as f:j = json.load(f)
        j[str(admin)]["clan"] = name
        
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
            "members": [admin],
            "admin": admin,
            "pw": pw,
        }

        with open("json/clan.json", "w", encoding="UTF-8") as f:
            json.dump(self.file, f, indent=4, ensure_ascii=False)
        
        with open("json/info.json", "w", encoding="UTF-8") as f:
            json.dump(j, f, indent=4, ensure_ascii=False)
        
        return (200, "성공")

    def get(self, name: str) -> tetrio.Clan:
        data = self.file[name]
        return tetrio.Clan(
            name    = name,
            des     = data["des"],
            rating  = data["rating"],
            members = data["members"],
            admin   = data["admin"],
            pw      = data["pw"],
        )