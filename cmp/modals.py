from nextcord import *
import db
import tetrio
from typing import Union
from .emojis import *
from .buttons import *

class SignUp(ui.Modal):
    def __init__(self) -> None:
        super().__init__(title = "가입", timeout=600)
        self.nick = ui.TextInput(label="닉네임", min_length=2, max_length=30, placeholder="5-23 is babo")
        self.tetrio_id = ui.TextInput(label="테트리오 id", min_length=2, max_length=30, placeholder="5-23")
        self.add_item(self.nick)
        self.add_item(self.tetrio_id)

    async def callback(self, inter: Interaction) -> None:
        await inter.response.defer()
        status = db.User().push(inter.user.id, self.nick.value, self.tetrio_id.value)
        embed = Embed(title = f"성공! {verified}", description="가입성공함", color = 0xa1dba5)
        if status[0] != 200:
            embed = Embed(title = f"실패({status[0]})", description = status[1], color = 0xff7033)
        if status[0] == 500:
            embed.set_image(url="https://images-ext-1.discordapp.net/external/vLiAmVFPZG--6nAXWTs8eNr29w2Cg8ZZqBna5Dyn4k4/https/www.qcgames.org/img/bot/profile_link_small.gif?width=400&height=400")
        await inter.followup.send(embed = embed)


class Clan(ui.Modal):
    def __init__(self, name: str, des: str, rating: Union[int, str], pw: str) -> None:
        super().__init__(title = "클랜만들기")

        self.name = ui.TextInput(label="이름", min_length=1, max_length=30, placeholder = "이에ㅔㅔㅔ", default_value=name)
        self.des = ui.TextInput(label="설명", min_length=1, placeholder="대충 엄청난 클랜", default_value=des, style=TextInputStyle.paragraph)
        
        self.rating = ui.TextInput(label="레이팅 조건", min_length=1, placeholder="0", default_value=rating)
        self.pw = ui.TextInput(label="비밀번호(선택)", min_length=1, default_value=pw, required=False, placeholder="123456789")

        self.add_item(self.name)
        self.add_item(self.des)
        self.add_item(self.rating)
        self.add_item(self.pw)

    async def callback(self, inter: Interaction) -> None:
        status = db.Clan().push(inter.user.id, self.name.value, self.des.value, self.rating.value, self.pw.value)
        if status[0] == 200:
            return await inter.response.send_message(embed = Embed(title = "생성 성공!", description = f"[{self.name.value}]클랜을 성공적으로 만듬"))
        await inter.response.send_message(embed=Embed(title = f"실패({status[0]})", description=status[1]), view = ReClan(inter.user.id, self.name.value, self.des.value, self.rating.value, self.pw.value))


class SignUpClan(ui.Modal):
    def __init__(self, clan: tetrio.Clan) -> None:
        super().__init__(title="클랜가입")
        self.clan = clan
        self.pw = ui.TextInput(label="비밀번호", placeholder="123456789")
        self.add_item(self.pw)

    async def callback(self, inter: Interaction):
        if self.pw.value == self.clan.pw:
            db.User().add_clan(inter.user.id, self.clan)
            await inter.response.send_message(embed = Embed(title = f"성공{verified}", description=f"[{self.clan.name}]에 가입을 성공함", color=0xa1dba5))
        else:
            await inter.response.send_message(embed = Embed(title = f"실패(505)", description=f"비밀번호가 틀림", color=0xff7033))