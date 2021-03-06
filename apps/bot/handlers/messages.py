from telegram import Message, MessageEntity, Update, User
from telegram.ext import Filters, MessageHandler
from telegram.ext.callbackcontext import CallbackContext

from .. import dispatcher
from ..builders import AskStartGameMessage
from ..models import User as DBUser


def handle_username_message(update: Update, context: CallbackContext) -> None:
    player: User = update.effective_user
    opponent_username = context.match.string[1:]  # remove @ symbol

    if opponent_username == player.username:
        text = "Вы не можете начать партию с собой."
        player.send_message(text)
        return

    opponent_db: DBUser = DBUser.objects.filter(username=opponent_username).first()

    if not opponent_db:
        text = (
            "ChessBot не знает этого пользователя."
            "Возможно он не открывал этого бота. "
            "Используйте команду /help_how_to_start чтобы узнать больше."
        )
        player.send_message(text)

    else:
        message = AskStartGameMessage(player, opponent_db)
        context.bot.send_message(opponent_db.id, **message.build())

        text = (
            f"Я отправил ваше предложение @{opponent_username}. "
            "Партия начнётся когда он(а) согласится."
        )
        player.send_message(text)


def handle_unknown_message(update: Update, context: CallbackContext) -> None:
    message = f"Моя твоя не понимать\.\nНапиши /help, чтобы узнать, что я понимаю\."
    update.effective_user.send_message(message, parse_mode="MarkdownV2")


filter_for_username = Filters.regex("^@[a-zA-Z0-9_]{5,}$")
dispatcher.add_handler(MessageHandler(filter_for_username, handle_username_message))

filter_for_any_message = Filters.all
dispatcher.add_handler(MessageHandler(filter_for_any_message, handle_unknown_message))
