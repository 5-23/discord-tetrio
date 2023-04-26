from nextcord import *
import db
from typing import Union
from .emojis import *

import cmp

class ReClan(ui.View):
    def __init__(self, id: int, name: str, rating: Union[int, str]) -> None:
        super().__init__(timeout=600)
        self.id = id
        self.name = name
        self.rating = rating
    
    @ui.button(label = "다시만들기")
    async def ok(self, btn, inter: Interaction):
        if self.id != inter.user.id:
            return await inter.response.send_message("너가만든거 아님", ephemeral = True)
        await inter.response.send_modal(cmp.modals.Clan(self.name, self.rating))