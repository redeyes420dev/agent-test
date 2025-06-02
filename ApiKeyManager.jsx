import React, { useState, useEffect } from 'react';
import './ApiKeyManager.css';

const ApiKeyManager = () => {
  const [keys, setKeys] = useState([]);
  const [newKey, setNewKey] = useState({
    provider: 'openai',
    keyName: '',
    apiKey: '',
    monthlyLimit: 100
  });
  const [isValidating, setIsValidating] = useState(false);
  const [showAddForm, setShowAddForm] = useState(false);
  const [notification, setNotification] = useState(null);

  // Загрузка ключей при монтировании компонента
  useEffect(() => {
    loadKeys();
  }, []);

  const loadKeys = async () => {
    try {
      const response = await fetch('/api/keys', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      if (response.ok) {
        const keysData = await response.json();
        setKeys(keysData);
      }
    } catch (error) {
      showNotification('Ошибка загрузки ключей', 'error');
    }
  };

  const handleAddKey = async (e) => {
    e.preventDefault();
    
    if (!newKey.apiKey || !newKey.keyName) {
      showNotification('Заполните все обязательные поля', 'error');
      return;
    }

    setIsValidating(true);
    
    try {
      // Сначала валидируем ключ
      const validationResponse = await fetch('/api/keys/validate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          provider: newKey.provider,
          api_key: newKey.apiKey
        })
      });

      const validationResult = await validationResponse.json();
      
      if (!validationResult.valid) {
        showNotification('API ключ недействителен', 'error');
        setIsValidating(false);
        return;
      }

      // Если валидация прошла успешно, добавляем ключ
      const addResponse = await fetch('/api/keys', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          provider: newKey.provider,
          key_name: newKey.keyName,
          api_key: newKey.apiKey,
          monthly_limit: newKey.monthlyLimit
        })
      });

      if (addResponse.ok) {
        showNotification('API ключ успешно добавлен', 'success');
        loadKeys();
        setNewKey({ provider: 'openai', keyName: '', apiKey: '', monthlyLimit: 100 });
        setShowAddForm(false);
      } else {
        const error = await addResponse.json();
        showNotification(error.detail || 'Ошибка добавления ключа', 'error');
      }

    } catch (error) {
      showNotification('Ошибка при добавлении ключа', 'error');
    } finally {
      setIsValidating(false);
    }
  };

  const handleDeleteKey = async (keyId) => {
    if (!confirm('Вы уверены, что хотите удалить этот API ключ?')) {
      return;
    }

    try {
      const response = await fetch(`/api/keys/${keyId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (response.ok) {
        showNotification('API ключ удален', 'success');
        loadKeys();
      } else {
        showNotification('Ошибка удаления ключа', 'error');
      }
    } catch (error) {
      showNotification('Ошибка удаления ключа', 'error');
    }
  };

  const toggleKeyStatus = async (keyId, currentStatus) => {
    try {
      const response = await fetch(`/api/keys/${keyId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          is_active: !currentStatus
        })
      });

      if (response.ok) {
        showNotification(
          `Ключ ${!currentStatus ? 'активирован' : 'деактивирован'}`, 
          'success'
        );
        loadKeys();
      }
    } catch (error) {
      showNotification('Ошибка изменения статуса ключа', 'error');
    }
  };

  const showNotification = (message, type) => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 5000);
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('ru-RU', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const getProviderIcon = (provider) => {
    const icons = {
      openai: '🤖',
      anthropic: '🧠',
      google: '🔍',
      azure: '☁️',
      brightdata: '🌐',
      github: '🐙'
    };
    return icons[provider] || '🔑';
  };

  const getProviderName = (provider) => {
    const names = {
      openai: 'OpenAI',
      anthropic: 'Anthropic',
      google: 'Google',
      azure: 'Azure OpenAI',
      brightdata: 'Bright Data',
      github: 'GitHub'
    };
    return names[provider] || provider;
  };

  return (
    <div className="api-key-manager">
      {notification && (
        <div className={`notification ${notification.type}`}>
          {notification.message}
        </div>
      )}

      <div className="header">
        <h2>🔑 Управление API ключами</h2>
        <button 
          className="btn-primary"
          onClick={() => setShowAddForm(!showAddForm)}
        >
          {showAddForm ? 'Отменить' : 'Добавить ключ'}
        </button>
      </div>

      {showAddForm && (
        <div className="add-key-form">
          <h3>Добавить новый API ключ</h3>
          <form onSubmit={handleAddKey}>
            <div className="form-group">
              <label>Провайдер:</label>
              <select 
                value={newKey.provider}
                onChange={(e) => setNewKey({...newKey, provider: e.target.value})}
                required
              >
                <option value="openai">OpenAI (GPT-4.1-mini)</option>
                <option value="anthropic">Anthropic (Claude)</option>
                <option value="google">Google (Gemini)</option>
                <option value="azure">Azure OpenAI</option>
                <option value="brightdata">Bright Data</option>
                <option value="github">GitHub</option>
              </select>
            </div>

            <div className="form-group">
              <label>Название ключа:</label>
              <input
                type="text"
                placeholder="Например: Основной OpenAI ключ"
                value={newKey.keyName}
                onChange={(e) => setNewKey({...newKey, keyName: e.target.value})}
                required
              />
            </div>

            <div className="form-group">
              <label>API ключ:</label>
              <input
                type="password"
                placeholder="Введите ваш API ключ"
                value={newKey.apiKey}
                onChange={(e) => setNewKey({...newKey, apiKey: e.target.value})}
                required
              />
            </div>

            <div className="form-group">
              <label>Месячный лимит ($):</label>
              <input
                type="number"
                min="1"
                max="10000"
                value={newKey.monthlyLimit}
                onChange={(e) => setNewKey({...newKey, monthlyLimit: parseInt(e.target.value)})}
                required
              />
            </div>

            <div className="form-actions">
              <button 
                type="submit"
                className="btn-primary"
                disabled={isValidating || !newKey.apiKey || !newKey.keyName}
              >
                {isValidating ? '🔄 Проверка...' : '✅ Добавить ключ'}
              </button>
              <button 
                type="button"
                className="btn-secondary"
                onClick={() => setShowAddForm(false)}
              >
                Отменить
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="keys-list">
        {keys.length === 0 ? (
          <div className="empty-state">
            <p>У вас пока нет добавленных API ключей</p>
            <button 
              className="btn-primary"
              onClick={() => setShowAddForm(true)}
            >
              Добавить первый ключ
            </button>
          </div>
        ) : (
          keys.map(key => (
            <KeyCard 
              key={key.id} 
              keyData={key} 
              onDelete={handleDeleteKey}
              onToggleStatus={toggleKeyStatus}
              formatCurrency={formatCurrency}
              getProviderIcon={getProviderIcon}
              getProviderName={getProviderName}
            />
          ))
        )}
      </div>
    </div>
  );
};

// Компонент карточки ключа
const KeyCard = ({ 
  keyData, 
  onDelete, 
  onToggleStatus, 
  formatCurrency, 
  getProviderIcon, 
  getProviderName 
}) => {
  const [showDetails, setShowDetails] = useState(false);

  const usagePercentage = (keyData.monthly_usage / keyData.monthly_limit) * 100;
  const isNearLimit = usagePercentage > 80;
  const isOverLimit = usagePercentage > 100;

  return (
    <div className={`key-card ${!keyData.is_active ? 'inactive' : ''}`}>
      <div className="key-header">
        <div className="key-info">
          <span className="provider-icon">
            {getProviderIcon(keyData.provider)}
          </span>
          <div>
            <h4>{keyData.key_name}</h4>
            <span className="provider-name">
              {getProviderName(keyData.provider)}
            </span>
          </div>
        </div>
        <div className="key-status">
          <span className={`status-badge ${keyData.is_active ? 'active' : 'inactive'}`}>
            {keyData.is_active ? 'Активен' : 'Неактивен'}
          </span>
        </div>
      </div>

      <div className="usage-info">
        <div className="usage-bar">
          <div 
            className={`usage-fill ${isOverLimit ? 'over-limit' : isNearLimit ? 'near-limit' : ''}`}
            style={{ width: `${Math.min(usagePercentage, 100)}%` }}
          ></div>
        </div>
        <div className="usage-text">
          {formatCurrency(keyData.monthly_usage)} / {formatCurrency(keyData.monthly_limit)}
          <span className="usage-percentage">
            ({usagePercentage.toFixed(1)}%)
          </span>
        </div>
      </div>

      {keyData.last_used && (
        <div className="last-used">
          Последнее использование: {new Date(keyData.last_used).toLocaleString('ru-RU')}
        </div>
      )}

      <div className="key-actions">
        <button
          className="btn-secondary"
          onClick={() => setShowDetails(!showDetails)}
        >
          {showDetails ? 'Скрыть' : 'Подробнее'}
        </button>
        <button
          className={`btn-secondary ${keyData.is_active ? 'deactivate' : 'activate'}`}
          onClick={() => onToggleStatus(keyData.id, keyData.is_active)}
        >
          {keyData.is_active ? 'Деактивировать' : 'Активировать'}
        </button>
        <button
          className="btn-danger"
          onClick={() => onDelete(keyData.id)}
        >
          Удалить
        </button>
      </div>

      {showDetails && (
        <div className="key-details">
          <div className="detail-row">
            <span>ID:</span>
            <span className="monospace">{keyData.id}</span>
          </div>
          <div className="detail-row">
            <span>Создан:</span>
            <span>{new Date(keyData.created_at).toLocaleString('ru-RU')}</span>
          </div>
          <div className="detail-row">
            <span>Статус:</span>
            <span className={keyData.is_active ? 'text-success' : 'text-danger'}>
              {keyData.is_active ? 'Активен' : 'Неактивен'}
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

export default ApiKeyManager;