from nextcord import *
import db
from typing import Union
from .emojis import *

import cmp

class ReClan(ui.View):
    def __init__(self, id: int, name: str, des: str, rating: Union[int, str], pw: str) -> None:
        super().__init__(timeout=600)
        self.id = id
        self.name = name
        self.des = des
        self.rating = rating
        self.pw = pw
    
    @ui.button(label = "다시만들기")
    async def ok(self, btn, inter: Interaction):
        if self.id != inter.user.id:
            return await inter.response.send_message("너가만든거 아님", ephemeral = True)
        await inter.response.send_modal(cmp.modals.Clan(self.name, self.des, self.rating, self.pw))

class RankBtn(ui.View):
    def __init__(self, arr: list):
        super().__init__(timeout = 600)
        self.arr = arr
        self.index = 0
        
        if self.index == 0:
            self.children[0].disabled = True
        else:
            self.children[0].disabled = False


        if (self.index+1)*5 >= len(self.arr):
            self.children[1].disabled = True
        else: 
            self.children[1].disabled = False


    @ui.button(label="<", style=ButtonStyle.green)
    async def before(self, button: ui.Button, inter: Interaction):
        self.index -= 1
        embed = self.refresh(inter)
        
        if self.index == 0:
            self.children[0].disabled = True
        else:
            self.children[0].disabled = False


        if (self.index+1)*5 >= len(self.arr):
            self.children[1].disabled = True
        else: 
            self.children[1].disabled = False
        
        await inter.message.edit(embed = embed, view = self)

        
    
    @ui.button(label=">", style=ButtonStyle.green)
    async def after(self, button: ui.Button, inter: Interaction):
        self.index += 1

        embed = self.refresh(inter)
        
        if self.index == 0:
            self.children[0].disabled = True
        else:
            self.children[0].disabled = False


        if (self.index+1)*5 >= len(self.arr):
            self.children[1].disabled = True
        else: 
            self.children[1].disabled = False
        
        await inter.message.edit(embed = embed, view = self)

    def refresh(self, inter: Interaction):
        i = self.index*5
        try: 
            embed = Embed(title=inter.message.embeds[0].title, color = 0xff7033)
        except:
            embed = Embed(title="?", color = 0xff7033)

        for rank in self.arr[self.index*5 : (self.index+1)*5]:
            i += 1
            embed.add_field(name=f"{i}등 | {rank[2].nick}({rank[2].name})", value=rank[1], inline=False)
        
        return embed
            