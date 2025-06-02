"""
API для управления ключами различных провайдеров
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer
from cryptography.fernet import Fernet
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import logging
from datetime import datetime
import base64

# Локальные импорты (будут созданы)
from .auth import get_current_user
from ..security.encryption import KeyEncryption
from ..core.llm_client import LLMClient
from ..mcp.key_validation import McpKeyValidator

logger = logging.getLogger("api_keys")
router = APIRouter()
security = HTTPBearer()
key_encryption = KeyEncryption()
mcp_validator = McpKeyValidator()

# Модели данных
class ApiKeyCreate(BaseModel):
    provider: str
    key_name: str
    api_key: str
    monthly_limit: float = 100.0


class ApiKeyResponse(BaseModel):
    id: str
    provider: str
    key_name: str
    is_active: bool
    last_used: Optional[datetime]
    monthly_usage: float
    monthly_limit: float
    created_at: datetime


class ApiKeyUpdate(BaseModel):
    key_name: Optional[str] = None
    monthly_limit: Optional[float] = None
    is_active: Optional[bool] = None


# Временное хранилище (в продакшене должна быть база данных)
api_keys_storage = {}
usage_storage = {}


@router.post("/keys", response_model=Dict[str, Any])
async def add_api_key(
    key_data: ApiKeyCreate, 
    user_id: str = Depends(get_current_user)
):
    """Добавление нового API ключа с валидацией и шифрованием"""
    try:
        # Валидация ключа через соответствующий провайдер
        is_valid = await validate_key_with_provider(key_data.provider, key_data.api_key)
        
        if not is_valid:
            raise HTTPException(status_code=400, detail="Недействительный API ключ")
        
        # Шифрование ключа
        encrypted_key = key_encryption.encrypt_api_key(key_data.api_key)
        
        # Генерация ID для ключа
        key_id = f"{user_id}_{key_data.provider}_{len(api_keys_storage)}"
        
        # Сохранение в хранилище
        api_keys_storage[key_id] = {
            'id': key_id,
            'user_id': user_id,
            'provider': key_data.provider,
            'key_name': key_data.key_name,
            'encrypted_key': encrypted_key,
            'monthly_limit': key_data.monthly_limit,
            'is_active': True,
            'created_at': datetime.now(),
            'last_used': None
        }
        
        # Инициализация статистики использования
        usage_storage[key_id] = {
            'total_requests': 0,
            'monthly_cost': 0.0,
            'monthly_tokens': 0
        }
        
        logger.info(f"API key added for user {user_id}, provider {key_data.provider}")
        
        return {
            "status": "success", 
            "key_id": key_id,
            "message": f"API ключ {key_data.key_name} успешно добавлен"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding API key: {e}")
        raise HTTPException(status_code=500, detail=f"Ошибка добавления ключа: {str(e)}")


@router.get("/keys", response_model=List[ApiKeyResponse])
async def get_user_keys(user_id: str = Depends(get_current_user)):
    """Получение списка ключей пользователя (без расшифровки)"""
    user_keys = []
    
    for key_id, key_data in api_keys_storage.items():
        if key_data['user_id'] == user_id:
            usage = usage_storage.get(key_id, {})
            
            user_keys.append(ApiKeyResponse(
                id=key_data['id'],
                provider=key_data['provider'],
                key_name=key_data['key_name'],
                is_active=key_data['is_active'],
                last_used=key_data['last_used'],
                monthly_usage=usage.get('monthly_cost', 0.0),
                monthly_limit=key_data['monthly_limit'],
                created_at=key_data['created_at']
            ))
    
    return user_keys


@router.put("/keys/{key_id}", response_model=Dict[str, Any])
async def update_api_key(
    key_id: str,
    update_data: ApiKeyUpdate,
    user_id: str = Depends(get_current_user)
):
    """Обновление настроек API ключа"""
    if key_id not in api_keys_storage:
        raise HTTPException(status_code=404, detail="API ключ не найден")
    
    key_data = api_keys_storage[key_id]
    if key_data['user_id'] != user_id:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    
    # Обновляем только переданные поля
    if update_data.key_name is not None:
        key_data['key_name'] = update_data.key_name
    if update_data.monthly_limit is not None:
        key_data['monthly_limit'] = update_data.monthly_limit
    if update_data.is_active is not None:
        key_data['is_active'] = update_data.is_active
    
    logger.info(f"API key {key_id} updated by user {user_id}")
    
    return {"status": "success", "message": "API ключ обновлен"}


@router.delete("/keys/{key_id}")
async def delete_api_key(
    key_id: str,
    user_id: str = Depends(get_current_user)
):
    """Удаление API ключа"""
    if key_id not in api_keys_storage:
        raise HTTPException(status_code=404, detail="API ключ не найден")
    
    key_data = api_keys_storage[key_id]
    if key_data['user_id'] != user_id:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    
    # Удаляем ключ и статистику
    del api_keys_storage[key_id]
    if key_id in usage_storage:
        del usage_storage[key_id]
    
    logger.info(f"API key {key_id} deleted by user {user_id}")
    
    return {"status": "success", "message": "API ключ удален"}


@router.post("/keys/validate")
async def validate_api_key(
    data: Dict[str, str],
    user_id: str = Depends(get_current_user)
):
    """Валидация API ключа без сохранения"""
    provider = data.get("provider")
    api_key = data.get("api_key")
    
    if not provider or not api_key:
        raise HTTPException(status_code=400, detail="Не указан провайдер или API ключ")
    
    try:
        is_valid = await validate_key_with_provider(provider, api_key)
        
        return {
            "valid": is_valid,
            "message": "API ключ действителен" if is_valid else "API ключ недействителен"
        }
        
    except Exception as e:
        logger.error(f"Validation error: {e}")
        return {"valid": False, "message": f"Ошибка валидации: {str(e)}"}


@router.get("/usage/stats")
async def get_usage_stats(user_id: str = Depends(get_current_user)):
    """Статистика использования API ключей"""
    user_keys = [k for k in api_keys_storage.values() if k['user_id'] == user_id]
    
    total_requests = 0
    monthly_cost = 0.0
    provider_costs = {}
    
    for key_data in user_keys:
        key_id = key_data['id']
        usage = usage_storage.get(key_id, {})
        
        total_requests += usage.get('total_requests', 0)
        monthly_cost += usage.get('monthly_cost', 0.0)
        
        provider = key_data['provider']
        if provider not in provider_costs:
            provider_costs[provider] = 0.0
        provider_costs[provider] += usage.get('monthly_cost', 0.0)
    
    top_providers = [
        {"name": provider, "cost": cost}
        for provider, cost in sorted(provider_costs.items(), key=lambda x: x[1], reverse=True)
    ]
    
    return {
        "total_requests": total_requests,
        "monthly_cost": monthly_cost,
        "top_providers": top_providers,
        "active_keys": len([k for k in user_keys if k['is_active']])
    }


async def validate_key_with_provider(provider: str, api_key: str) -> bool:
    """Валидация API ключа через соответствующий провайдер"""
    try:
        if provider == "openai":
            client = LLMClient(api_key, provider="openai")
            return await client.validate_api_key()
            
        elif provider == "anthropic":
            client = LLMClient(api_key, provider="anthropic")
            return await client.validate_api_key()
            
        elif provider in ["brightdata", "github"]:
            # Валидация через MCP-сервер
            return await mcp_validator.validate_mcp_key(provider, api_key)
            
        else:
            logger.warning(f"Unknown provider for validation: {provider}")
            return False
            
    except Exception as e:
        logger.error(f"Error validating {provider} key: {e}")
        return False


def get_decrypted_key(user_id: str, provider: str) -> Optional[str]:
    """Получение расшифрованного ключа для использования в агентах"""
    for key_data in api_keys_storage.values():
        if (key_data['user_id'] == user_id and 
            key_data['provider'] == provider and 
            key_data['is_active']):
            
            try:
                return key_encryption.decrypt_api_key(key_data['encrypted_key'])
            except Exception as e:
                logger.error(f"Error decrypting key: {e}")
                return None
    
    return None


async def track_api_usage(key_id: str, tokens_used: int, cost: float):
    """Отслеживание использования API"""
    if key_id not in usage_storage:
        usage_storage[key_id] = {
            'total_requests': 0,
            'monthly_cost': 0.0,
            'monthly_tokens': 0
        }
    
    usage = usage_storage[key_id]
    usage['total_requests'] += 1
    usage['monthly_cost'] += cost
    usage['monthly_tokens'] += tokens_used
    
    # Обновляем время последнего использования
    if key_id in api_keys_storage:
        api_keys_storage[key_id]['last_used'] = datetime.now()
    
    # Проверяем лимиты
    if key_id in api_keys_storage:
        key_data = api_keys_storage[key_id]
        if usage['monthly_cost'] >= key_data['monthly_limit']:
            key_data['is_active'] = False
            logger.warning(f"API key {key_id} disabled due to cost limit exceeded")
            
            # Здесь можно добавить отправку уведомления пользователю