import os  # Для работы с операционной системой, например, для доступа к переменным окружения.

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
# APIRouter: для организации маршрутов API.
# UploadFile, File: для обработки загружаемых файлов.
# Depends: для инъекции зависимостей.
# HTTPException: для возврата HTTP-ошибок.

from easy_async_tg_notify import Notifier
# Notifier: для асинхронной отправки уведомлений в Telegram.

from app.api.schemas import Message
# Message: схема данных (Pydantic) для описания структуры сообщения.

from app.auth.dependencies import get_notifier, get_current_admin_user
# get_notifier: зависимость для уведомлений.
# get_current_admin_user: зависимость для проверки прав администратора.

from app.auth.models import User
# User: модель пользователя из модуля авторизации.

from app.config import settings
# settings: настройки приложения.
router = APIRouter(prefix='/api', tags=['API'])
@router.post('/send_text')
async def send_text(message: Message,
                    notifier: Notifier = Depends(get_notifier),
                    user_data: User = Depends(get_current_admin_user)):
    try:
        await notifier.send_text(message.text, settings.CHAT_ID)
        return {"status": "success", "message": "Текстовое сообщение отправлено"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.post('/send_photo')
async def send_photo(caption: str = None,
                     file: UploadFile = File(...),
                     notifier: Notifier = Depends(get_notifier),
                     user_data: User = Depends(get_current_admin_user)):
    try:
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        await notifier.send_photo(file_path, settings.CHAT_ID, caption=caption)
        os.remove(file_path)
        return {"status": "success", "message": "Фото отправлено"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.post('/send_document')
async def send_document(caption: str = None,
                        file: UploadFile = File(...),
                        notifier: Notifier = Depends(get_notifier),
                        user_data: User = Depends(get_current_admin_user)):
    try:
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        await notifier.send_document(file_path, settings.CHAT_ID, caption=caption)
        os.remove(file_path)
        return {"status": "success", "message": "Документ отправлен"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
