"""
Система шифрования для защиты API ключей
"""

from cryptography.fernet import Fernet
import os
import base64
import logging
from typing import Optional

logger = logging.getLogger("encryption")


class KeyEncryption:
    """Класс для шифрования и расшифровки API ключей"""
    
    def __init__(self):
        """Инициализация с ключом шифрования"""
        # Получаем ключ из переменной окружения или генерируем новый
        encryption_key = os.getenv('ENCRYPTION_KEY')
        
        if encryption_key:
            # Используем существующий ключ
            self.key = encryption_key.encode()
        else:
            # Генерируем новый ключ
            self.key = Fernet.generate_key()
            logger.warning("Сгенерирован новый ключ шифрования. Установите ENCRYPTION_KEY в переменные окружения.")
        
        self.cipher = Fernet(self.key)
    
    def encrypt_api_key(self, api_key: str) -> str:
        """Шифрование API ключа"""
        if not api_key:
            raise ValueError("API ключ не может быть пустым")
        
        try:
            # Шифруем ключ
            encrypted_bytes = self.cipher.encrypt(api_key.encode('utf-8'))
            
            # Кодируем в base64 для хранения в БД
            encrypted_base64 = base64.b64encode(encrypted_bytes).decode('utf-8')
            
            return encrypted_base64
            
        except Exception as e:
            logger.error(f"Ошибка шифрования API ключа: {e}")
            raise
    
    def decrypt_api_key(self, encrypted_key: str) -> str:
        """Расшифровка API ключа"""
        if not encrypted_key:
            raise ValueError("Зашифрованный ключ не может быть пустым")
        
        try:
            # Декодируем из base64
            encrypted_bytes = base64.b64decode(encrypted_key.encode('utf-8'))
            
            # Расшифровываем
            decrypted_bytes = self.cipher.decrypt(encrypted_bytes)
            
            # Возвращаем строку
            return decrypted_bytes.decode('utf-8')
            
        except Exception as e:
            logger.error(f"Ошибка расшифровки API ключа: {e}")
            raise
    
    def generate_new_key(self) -> str:
        """Генерация нового ключа шифрования"""
        new_key = Fernet.generate_key()
        return new_key.decode('utf-8')
    
    def rotate_key(self, old_key: str, new_key: str, encrypted_data: str) -> str:
        """Поворот ключа: расшифровка старым ключом и шифрование новым"""
        try:
            # Создаем шифры для старого и нового ключей
            old_cipher = Fernet(old_key.encode())
            new_cipher = Fernet(new_key.encode())
            
            # Расшифровываем старым ключом
            encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
            decrypted_data = old_cipher.decrypt(encrypted_bytes)
            
            # Шифруем новым ключом
            new_encrypted_bytes = new_cipher.encrypt(decrypted_data)
            new_encrypted_base64 = base64.b64encode(new_encrypted_bytes).decode('utf-8')
            
            return new_encrypted_base64
            
        except Exception as e:
            logger.error(f"Ошибка поворота ключа: {e}")
            raise


class SecureStorage:
    """Безопасное хранение чувствительных данных"""
    
    def __init__(self):
        self.encryption = KeyEncryption()
    
    def store_sensitive_data(self, data: dict) -> dict:
        """Шифрование чувствительных полей в словаре"""
        encrypted_data = data.copy()
        
        # Поля, которые нужно шифровать
        sensitive_fields = ['api_key', 'password', 'token', 'secret']
        
        for field in sensitive_fields:
            if field in encrypted_data and encrypted_data[field]:
                encrypted_data[field] = self.encryption.encrypt_api_key(str(encrypted_data[field]))
        
        return encrypted_data
    
    def retrieve_sensitive_data(self, encrypted_data: dict) -> dict:
        """Расшифровка чувствительных полей в словаре"""
        decrypted_data = encrypted_data.copy()
        
        # Поля, которые нужно расшифровать
        sensitive_fields = ['api_key', 'password', 'token', 'secret']
        
        for field in sensitive_fields:
            if field in decrypted_data and decrypted_data[field]:
                try:
                    decrypted_data[field] = self.encryption.decrypt_api_key(decrypted_data[field])
                except Exception as e:
                    logger.warning(f"Не удалось расшифровать поле {field}: {e}")
                    decrypted_data[field] = None
        
        return decrypted_data


def mask_api_key(api_key: str, visible_chars: int = 4) -> str:
    """Маскирование API ключа для логирования и отображения"""
    if not api_key or len(api_key) <= visible_chars * 2:
        return "*" * 10
    
    return f"{api_key[:visible_chars]}{'*' * (len(api_key) - visible_chars * 2)}{api_key[-visible_chars:]}"


def validate_encryption_setup() -> bool:
    """Проверка корректности настройки шифрования"""
    try:
        encryption = KeyEncryption()
        
        # Тестируем шифрование/расшифровку
        test_data = "test_api_key_12345"
        encrypted = encryption.encrypt_api_key(test_data)
        decrypted = encryption.decrypt_api_key(encrypted)
        
        if decrypted == test_data:
            logger.info("Система шифрования настроена корректно")
            return True
        else:
            logger.error("Ошибка в системе шифрования: данные не совпадают")
            return False
            
    except Exception as e:
        logger.error(f"Ошибка проверки системы шифрования: {e}")
        return False


# Утилиты для работы с шифрованием
def setup_encryption_key():
    """Настройка ключа шифрования в переменных окружения"""
    if not os.getenv('ENCRYPTION_KEY'):
        new_key = Fernet.generate_key().decode('utf-8')
        print(f"Добавьте в .env файл: ENCRYPTION_KEY={new_key}")
        return new_key
    else:
        print("Ключ шифрования уже настроен")
        return os.getenv('ENCRYPTION_KEY')


if __name__ == "__main__":
    # Тестирование системы шифрования
    print("Тестирование системы шифрования...")
    
    if validate_encryption_setup():
        print("✅ Система шифрования работает корректно")
    else:
        print("❌ Ошибка в системе шифрования")
    
    # Демонстрация маскирования
    test_key = "sk-1234567890abcdef1234567890abcdef"
    masked = mask_api_key(test_key)
    print(f"Исходный ключ: {test_key}")
    print(f"Замаскированный: {masked}")
    
    # Настройка ключа шифрования
    setup_encryption_key()