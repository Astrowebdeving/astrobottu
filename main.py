import asyncio
import logging
import os
from typing import Any

import aiohttp
import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("astrobot")

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")
BOT_API_KEY = os.getenv("BOT_API_KEY", "")
QUESTION_TIMEOUT_SECONDS = float(os.getenv("QUESTION_TIMEOUT_SECONDS", "10"))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="a!", intents=intents)


class AstroBotAPIError(RuntimeError):
    """Raised when the question API cannot return usable data."""


async def api_get(path: str) -> Any:
    """Fetch JSON from the Django API without blocking Discord's event loop."""
    # keep api calls off the discord event loop
    headers = {"X-API-Key": BOT_API_KEY} if BOT_API_KEY else {}
    timeout = aiohttp.ClientTimeout(total=5)
    url = f"{API_BASE_URL}/{path.lstrip('/')}"

    try:
        async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()
    except (aiohttp.ClientError, TimeoutError, ValueError) as exc:
        raise AstroBotAPIError(f"GET {url} failed: {exc}") from exc


async def get_question() -> tuple[str, int, str, str, int]:
    """Return a formatted four-answer question from the Django API."""
    json_data = await api_get("api/random/")
    if not isinstance(json_data, list) or not json_data:
        raise AstroBotAPIError("The API has no active questions")

    question = json_data[0]
    answers = question.get("answer", [])
    if len(answers) != 4:
        raise AstroBotAPIError("A trivia question must have exactly four answers")

    correct_answers = [
        (index, item) for index, item in enumerate(answers, start=1) if item.get("is_correct")
    ]
    if len(correct_answers) != 1:
        raise AstroBotAPIError("A trivia question must have exactly one correct answer")

    title = str(question["title"])
    points = int(question["points"])
    lines = ["Question:", title]
    lines.extend(
        f"{index}. {item['answer']}" for index, item in enumerate(answers, start=1)
    )

    answer_number, correct_answer = correct_answers[0]
    return (
        "\n".join(lines),
        answer_number,
        str(correct_answer["answer"]),
        title,
        points,
    )


async def parse_users() -> Any:
    """Return users from the existing leaderboard endpoint."""
    return await api_get("api/allusers/")


def textCheck(value: str, answer_number: int, answer_text: str) -> tuple[bool, str]:
    """Keep the original answer-checking helper with explicit inputs."""
    if value == str(answer_number):
        return True, f"Correct. {answer_text} is the answer."
    return False, "Incorrect."


def textsend(message: str) -> str:
    return message


class ButtonView(discord.ui.View):
    def __init__(
        self,
        *,
        answer_number: int,
        answer_text: str,
        timeout: float = QUESTION_TIMEOUT_SECONDS,
    ) -> None:
        super().__init__(timeout=timeout)
        # keep answers isolated to this question message
        self.answer_number = answer_number
        self.answer_text = answer_text
        self.clicked_user_ids: set[int] = set()
        self.correct_users: list[str] = []

    async def handle_answer(
        self, interaction: discord.Interaction, value: str
    ) -> None:
        user_id = interaction.user.id
        if user_id in self.clicked_user_ids:
            await interaction.response.send_message(
                "You have already answered.", ephemeral=True
            )
            return

        self.clicked_user_ids.add(user_id)
        is_correct, message = textCheck(value, self.answer_number, self.answer_text)
        if is_correct:
            self.correct_users.append(interaction.user.display_name)
        await interaction.response.send_message(textsend(message), ephemeral=True)

    async def on_error(
        self,
        interaction: discord.Interaction,
        error: Exception,
        item: discord.ui.Item,
    ) -> None:
        logger.exception("Button interaction failed", exc_info=error)
        if not interaction.response.is_done():
            await interaction.response.send_message(
                "The answer could not be recorded.", ephemeral=True
            )

    @discord.ui.button(label="1", row=0, style=discord.ButtonStyle.blurple)
    async def blurple_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await self.handle_answer(interaction, "1")

    @discord.ui.button(label="2", row=0, style=discord.ButtonStyle.gray)
    async def gray_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await self.handle_answer(interaction, "2")

    @discord.ui.button(label="3", row=1, style=discord.ButtonStyle.green)
    async def green_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await self.handle_answer(interaction, "3")

    @discord.ui.button(label="4", row=1, style=discord.ButtonStyle.red)
    async def red_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await self.handle_answer(interaction, "4")


@bot.event
async def on_ready() -> None:
    logger.info("Connected to Discord as %s", bot.user)


@bot.command()
@commands.guild_only()
async def info(ctx: commands.Context) -> None:
    await ctx.send(f"Server ID: {ctx.guild.id}")


@bot.command()
@commands.guild_only()
async def quest(ctx: commands.Context) -> None:
    try:
        question, answer_number, answer_text, title, points = await get_question()
    except AstroBotAPIError as exc:
        logger.warning("Question request failed: %s", exc)
        await ctx.send("No question is available. Check the API and question data.")
        return

    view = ButtonView(answer_number=answer_number, answer_text=answer_text)
    message = await ctx.send(question, view=view)
    # keep the round length fixed even after button interactions
    await asyncio.sleep(QUESTION_TIMEOUT_SECONDS)
    view.stop()

    for item in view.children:
        item.disabled = True
    try:
        await message.edit(view=view)
    except discord.HTTPException:
        logger.warning("Could not disable buttons on message %s", message.id)

    if view.correct_users:
        names = ", ".join(view.correct_users)
        result = f"Correct: {names}. The answer to {title} is {answer_text} ({points} points)."
    else:
        result = f"No correct answers. The answer to {title} is {answer_text}."
    await ctx.send(result)


def run_bot() -> None:
    token = os.getenv("DISCORD_BOT_TOKEN") or os.getenv("envtoken")
    if not token:
        raise RuntimeError(
            "Set DISCORD_BOT_TOKEN in the environment (legacy envtoken is also accepted)"
        )
    bot.run(token, log_handler=None)


if __name__ == "__main__":
    run_bot()
