from nextcord import *
import db
import cmp
from cmp import emojis
INTENTS = Intents().all()
cli = Client(intents = INTENTS)

import datetime, time, math

@cli.event
async def on_ready():
    print("시작됨")


@cli.slash_command(name="가입", description="가입을 함")
async def sign_up(inter: Interaction):
    await inter.response.send_modal(cmp.modals.SignUp())

@cli.slash_command(name="새로고침", description="자신의 테트리오 정보를 다시 불러옴")
async def refresh(inter: Interaction):
    await inter.response.send_message("> 새로고침중")
    try: before = db.User().get(id=inter.user.id)
    except: return await inter.edit_original_message(content = "> 가입 먼저해야함")
    
    db.User().push(inter.user.id, before.nick, before.name)
    await inter.edit_original_message(content = "> 새로고침 완료")

@cli.slash_command(name="정보", description="테트리오 정보를 불러옴")
async def info(inter: Interaction):
    try: data = db.User().get(inter.user.id)
    except: return await inter.response.send_message(embed = Embed(title = "404(Not Founded)", description="가입을 먼저 해야함", color = 0xff7033), ephemeral = True)
    
    await inter.response.defer()

    embeds = [Embed(title = f"{data.nick}(`{data.name}`)", color=0xa1dba5)]
    embeds[0].set_thumbnail(url=data.avatar_img)
    if data.name == data.nick: embeds[0].title = data.name
    embeds[0].add_field(name="이김/플레이", value=f"{data.gamewon}/{data.gameplayed}", inline = False)
    
    if data.l40.ok:
        embeds.append(Embed(title = f"40 Line", color=0xa1dba5))
        embeds[len(embeds)-1].add_field(name="시간", value=f"{int(data.l40.time/60)}분 {int(data.l40.time%60)}초", inline = False)
        ts = int(time.mktime(datetime.datetime.strptime(data.l40.ts, "%Y-%m-%dT%H:%M:%S").timetuple()))
        embeds[len(embeds)-1].add_field(name="~전에 완료", value=f"<t:{ts}:R>", inline = False)
    
    if data.blitz.ok:
        embeds.append(Embed(title = f"Blitz", color=0xa1dba5))
        embeds[len(embeds)-1].add_field(name="점수", value=f"{data.blitz.point}점")
        ts = int(time.mktime(datetime.datetime.strptime(data.l40.ts, "%Y-%m-%dT%H:%M:%S").timetuple()))
        embeds[len(embeds)-1].add_field(name="~전에 완료", value=f"<t:{ts}:R>", inline = False)
    

    if len(data.badges):
        description = ""
        for badge in data.badges:
            description += f"{emojis.badges.get(badge.title, badge.title)} "
        embeds.append(Embed(title = f"Badge", color=0xa1dba5, description = description))
    

    if data.league.rank != 'z':
        embeds.append(Embed(title = f"Tetra League", color=0xa1dba5))
        embeds[len(embeds)-1].add_field(name="레이팅", value=f"**{data.league.rating}**TR", inline = False)
        embeds[len(embeds)-1].add_field(name="랭크", value=f"{emojis.ranks[data.league.rank]}")
        embeds[len(embeds)-1].add_field(name="최고랭크", value=f"{emojis.ranks[data.league.best_rank]}")
        embeds[len(embeds)-1].add_field(name="apm (Attack Per Minute)", value=f"{data.league.apm}", inline = False)
        embeds[len(embeds)-1].add_field(name="pps (Pieces Per Seconds)", value=f"{data.league.pps}")
        embeds[len(embeds)-1].add_field(name="vs (VerSus)", value=f"{data.league.vs}")
    
    
    
    embeds[len(embeds)-1].set_image(url=data.banner_img)

    await inter.followup.send(embeds = embeds)


@cli.slash_command(name="클랜생성", description="클랜을 생성함")
async def sign_up(inter: Interaction):
    try: data = db.User().get(inter.user.id)
    except: return await inter.response.send_message(embed = Embed(title = "404(Not Founded)", description="가입을 먼저 해야함", color = 0xff7033), ephemeral = True)
    if data.clan != None:
        return await inter.response.send_message("이미 클랜에 있음")
    await inter.response.send_modal(cmp.modals.Clan("", "", "", ""))

@cli.slash_command(name="클랜참가", description="클랜에 참가를 요청함")
async def join_clan(inter: Interaction, name: str = SlashOption(name="클랜명", description="참가 할 클랜명")):
    try: db.User().get(inter.user.id)
    except: return await inter.response.send_message(embed = Embed(title = "404(Not Founded)", description="가입을 먼저 해야함", color = 0xff7033), ephemeral = True)
    
    clan = db.Clan().get(name)
    if clan.pw == None:
        db.User().add_clan(inter.user.id, clan)
        await inter.response.send_message(embed = Embed(title = f"성공{emojis.verified}", description=f"[{clan.name}]에 가입을 성공함", color=0xa1dba5))
    else:
        await inter.response.send_modal(cmp.modals.SignUpClan(clan))        

@join_clan.on_autocomplete("name")
async def join_clan_auto(inter: Interaction, name: str):
    auto = ["입력"]
    if name != "":
        auto = [i for i in db.Clan().file if name.lower() in i]
        if auto == []:
            auto = ["검색결과 없음"]

    await inter.response.send_autocomplete(auto)






cli.run(open(".token").read())