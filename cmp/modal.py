from nextcord import *
import db
from .emojis import *

class signUp(ui.Modal):
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

        await inter.followup.send(embed = embed)