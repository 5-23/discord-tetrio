from nextcord import *
import db
import cmp
INTENTS = Intents().all()
cli = Client(intents = INTENTS)

@cli.event
async def on_ready():
    print("시작됨")


@cli.slash_command(name="가입", description="가입을 함")
async def sign_up(inter: Interaction):
    await inter.response.send_modal(cmp.modal.signUp())

@cli.slash_command(name="정보", description="테스트용 커멘드")
async def info(inter: Interaction):
    a = db.User().get(inter.user.id)
    print(a.blitz.point)
    await inter.response.send_message("성공")


cli.run(open(".token").read())