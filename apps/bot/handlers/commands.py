from telegram import Update, User
from telegram.ext import CommandHandler
from telegram.ext.callbackcontext import CallbackContext

from .. import dispatcher
from ..models import User as DBUser


def handle_start_command(update: Update, context: CallbackContext) -> None:
    user: User = update.effective_user

    DBUser.update_or_create(user)

    help_text = (
        "Здравствуйте\! Здесь вы можете поиграть в шахматы с реальными людьми\. "
        "Для того чтобы начать партию напишите `@username` пользователя с которым "
        "вы желаете играть\.\n\n*Важно\! Бот должен знать вашего оппонента, "
        f"попросите его открыть бота @dev\_chess\_bot и нажать /start*"
    )
    user.send_message(help_text, parse_mode="MarkdownV2")

    if not user.username:
        text = (
            "Я вижу что у вас не установлен `@username`\.\n"
            "*Другие игроки не смогут предложить вам сыграть партию\!*\n"
            "О том как установить `@username` и что это такое вы можете прочитать "
            "[здесь](https://telegram.org/faq#q-what-are-usernames-how-do-i-get-one)\."
            "\n\nПосле того как вы установили или изменили `@username` "
            "запустите снова команду /start чтобы я запомнил его\."
            "\n\nЕсли вы не хотите устанавливать себе `@username`, "
            "то напишите `@username` соперника\."
        )
        user.send_message(text, parse_mode="MarkdownV2", disable_web_page_preview=True)


def handle_help_command(update: Update, context: CallbackContext) -> None:
    user: User = update.effective_user
    help_text = "Справочная информация"
    user.send_message(help_text, parse_mode="MarkdownV2")


def handle_finish_game_command(update: Update, context: CallbackContext) -> None:
    player: User = update.effective_user
    player_db: DBUser = DBUser.objects.filter(id=player.id).first()

    if not player_db:
        player_db = DBUser.update_or_create(player)

    if not player_db.in_game:
        player.send_message("Вы не играете")

    else:
        player_db.in_game = player_db.opponent.in_game = False
        player_db.save()
        player_db.opponent.save()
        
        context.bot.send_message(
            chat_id=player_db.opponent.id, text="Ваш соперник сдался"
        )
        player.send_message("Партия закончена, вы проиграли")


dispatcher.add_handler(CommandHandler("start", handle_start_command))
dispatcher.add_handler(CommandHandler("help", handle_help_command))
dispatcher.add_handler(CommandHandler("finish_game", handle_finish_game_command))
