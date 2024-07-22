from aiogram.types import update
from aiogram.filters.callback_data import CallbackContext

def has_permission(update: update.Update, role: str) -> bool:
    user_id = update.message.from_user.id
    # Проверка роли пользователя в базе данных или в памяти
    return check_user_role_in_db(user_id, role)

def check_user_role_in_db(user_id, role):
    if(user_id == '1000'):
        if(role in ['admin', 'user']):
            return True
    if role == 'user':
        return True
    return False

def admin_command(update: update.Update, func):
    if has_permission(update, 'admin'):
        return func
    else:
        print(f'Вы не админ, чтобы тут {func.__name__}')
