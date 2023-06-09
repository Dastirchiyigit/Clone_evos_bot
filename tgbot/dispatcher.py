from telegram.ext import (
    Dispatcher, Filters,
    CommandHandler, MessageHandler,
    CallbackQueryHandler,
)

from dtb.settings import DEBUG
from tgbot.handlers.broadcast_message.manage_data import CONFIRM_DECLINE_BROADCAST
from tgbot.handlers.broadcast_message.static_text import broadcast_command
from tgbot.handlers.onboarding.manage_data import SECRET_LEVEL_BUTTON
from tgbot.handlers.menu import handlers as menu_handlers
from tgbot.handlers.menu import static_text as menu_text 

from tgbot.handlers.utils import files, error
from tgbot.handlers.admin import handlers as admin_handlers
from tgbot.handlers.location import handlers as location_handlers
from tgbot.handlers.onboarding import handlers as onboarding_handlers
from tgbot.handlers.broadcast_message import handlers as broadcast_handlers
from tgbot.main import bot

#       ALISHER



from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

from tgbot.handlers.onboarding import fikr_bildir as onboarding_fikir_bildir
#       ALISHER

def setup_dispatcher(dp):
    """
    Adding handlers for events from Telegram
    """
    
    # onboarding
    dp.add_handler(CommandHandler("start", onboarding_handlers.command_start))

    # admin commands
    dp.add_handler(CommandHandler("admin", admin_handlers.admin))
    dp.add_handler(CommandHandler("stats", admin_handlers.stats))
    dp.add_handler(CommandHandler('export_users', admin_handlers.export_users))

# AYMURAT

    HOME, MENU, MY_ORDERS, COMMENT, SETTINGS, MY_ADDRESSES, SEND_LOCATION, ADDRESSES_LIST, = range(8)

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, menu_handlers.home_page)],
        states={
            HOME: [MessageHandler(Filters.text, menu_handlers.home_page)],
            MENU: [MessageHandler(Filters.regex(f"^{menu_text.home_menu}$"),  menu_handlers.click_menu)],
            # MY_ORDERS: [MessageHandler(Filters.regex(f"^{menu_text.home_my_orders}"), )],
            # COMMENT: [],
            # SETTINGS: [],
            MY_ADDRESSES: [MessageHandler(Filters.regex(f"^{menu_text.address_my_addresses}$"), menu_handlers.address_list)],
            SEND_LOCATION: [MessageHandler(Filters.regex(f"^{menu_text.address_send_location}$"), menu_handlers.)]
        },
        fallbacks=[],
    )

    dp.add_handler(conv_handler)

# AYMURAT  

#          ALISHER
    # GET_CONTACT, GET_SUGGETIONS= range(2)


    # conv_handler = ConversationHandler(
    #     entry_points=[MessageHandler(Filters.regex("^✍️ Fikr bildirish$"), onboarding_fikir_bildir.boshlaa)],
    #     states={
    #         GET_CONTACT: [MessageHandler(Filters.contact,  onboarding_fikir_bildir.for_contact),MessageHandler(Filters.regex("^⬅️ Ortga$"), onboarding_fikir_bildir.for_ortga)],
    #         GET_SUGGETIONS: [MessageHandler(Filters.text,  onboarding_fikir_bildir.for_suggestion)],

    #     },
    #     fallbacks=[],
    # )

    # dp.add_handler(conv_handler)

#           ALISHER

    # location
    dp.add_handler(CommandHandler("ask_location", location_handlers.ask_for_location))
    dp.add_handler(MessageHandler(Filters.location, location_handlers.location_handler))

    # secret level
    dp.add_handler(CallbackQueryHandler(onboarding_handlers.secret_level, pattern=f"^{SECRET_LEVEL_BUTTON}"))

    # broadcast message
    dp.add_handler(
        MessageHandler(Filters.regex(rf'^{broadcast_command}(/s)?.*'), broadcast_handlers.broadcast_command_with_message)
    )
    dp.add_handler(
        CallbackQueryHandler(broadcast_handlers.broadcast_decision_handler, pattern=f"^{CONFIRM_DECLINE_BROADCAST}")
    )

    # files
    dp.add_handler(MessageHandler(
        Filters.animation, files.show_file_id,
    ))

    # handling errors
    dp.add_error_handler(error.send_stacktrace_to_tg_chat)

    # EXAMPLES FOR HANDLERS
    # dp.add_handler(MessageHandler(Filters.text, <function_handler>))
    # dp.add_handler(MessageHandler(
    #     Filters.document, <function_handler>,
    # ))
    # dp.add_handler(CallbackQueryHandler(<function_handler>, pattern="^r\d+_\d+"))
    # dp.add_handler(MessageHandler(
    #     Filters.chat(chat_id=int(TELEGRAM_FILESTORAGE_ID)),
    #     # & Filters.forwarded & (Filters.photo | Filters.video | Filters.animation),
    #     <function_handler>,
    # ))

    return dp


n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True))

