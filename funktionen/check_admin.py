import discord



class AuthorView(discord.ui.View):
    def __init__(self, author_id: int, timeout: float | None = None):
        super().__init__(timeout=timeout)
        self.author_id = author_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Das ist nicht dein Button!", ephemeral=True)
            return False
        return True