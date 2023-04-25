from nextcord import *

cli = Client()

@cli.slash_command(name="가입")
async def sign_up(inter: Interaction, name: str, id: str):
    ...
    


cli.run(open("token").read())