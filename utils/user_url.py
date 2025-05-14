from aiogram.types import Message
def get_user_link_html(user:Message) -> str:
    """
    Generate a clickable link to a Telegram user based on their username or ID.
    attr user: Message object containing user information"""
    if user.username:
        link = f"https://t.me/{user.username}"
        display = user.username
    else:
        link = f"tg://user?id={user.id}"
        display = user.full_name
    
    return f'<a href="{link}">{display}</a>'
