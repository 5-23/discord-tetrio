from nextcord import *
import db
import cmp
INTENTS = Intents().all()
cli = Client(intents = INTENTS)

from datetime import datetime
import time, math

@cli.event
async def on_ready():
    print("시작됨")


@cli.slash_command(name="가입", description="가입을 함")
async def sign_up(inter: Interaction):
    await inter.response.send_modal(cmp.modal.signUp())

@cli.slash_command(name="정보", description="테트리오 정보를 불러옴")
async def info(inter: Interaction):
    try: data = db.User().get(inter.user.id)
    except: return await inter.response.send_message(embed = Embed(title = "404(Not Founded)", description="가입을 먼저 해야함", color = 0xff7033), ephemeral = True)
    
    await inter.response.defer()

    embeds = [Embed(title = f"{data.nick}(`{data.name}`)", color=0xa1dba5)]
    embeds[0].set_thumbnail(url=data.avatar_img)
    if data.name == data.nick: embeds[0].title = data.name
    embeds[0].add_field(name="이긴수/게임한수", value=f"{data.gamewon}/{data.gameplayed}")
    
    if data.l40.ok:
        embeds.append(Embed(title = f"40 Line", color=0xa1dba5))
        embeds[len(embeds)-1].add_field(name="시간", value=f"{int(data.l40.time/60)}분 {int(data.l40.time%60)}초")
        # embeds[len(embeds)-1].add_field(name="~전에 완료", value=f"{time.mktime(datetime.strptime(data.l40.ts, '%Y-%m %H:%M:%S.%R').timetuple())}")
    if data.blitz.ok:
        embeds.append(Embed(title = f"Blitz", color=0xa1dba5))
        embeds[len(embeds)-1].add_field(name="점수", value=f"{data.blitz.point}점")
        # embeds[len(embeds)-1].add_field(name="~전에 완료", value=f"{time.mktime(datetime.strptime(data.l40.ts, '%Y-%m %H:%M:%S.%R').timetuple())}")
    embeds[len(embeds)-1].set_image(url=data.banner_img)

    await inter.followup.send(embeds = embeds)

cli.run(open(".token").read())