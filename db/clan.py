import json
class Clan:
    def __init__(self) -> None:
        with open("json/clan.json", "r", encoding="UTF-8") as f:
            try: self.file = json.load(f)
            except: self.file = {}

    def push(self, id: int , name: str, rating: str) -> tuple[int, str]:
        if rating != "":
            try:
                int(rating)
                rating = 0
            except: return (505, "레이팅이 숫자가 아님")
        if self.file.get(name, 0): return (500, "이미있는 이름")
        
        self.file[name] = {
            "rating": int(rating),
            "members": [id]
        }

        with open("json/info.json", "w", encoding="UTF-8") as f:
            json.dump(self.file, f, indent=4, ensure_ascii=False)
        return (200, "성공")