// Данные приложения
const appData = {
  providers: [
    {"id": "openai", "name": "OpenAI", "icon": "🤖", "models": ["gpt-4.1-mini", "gpt-4o"]},
    {"id": "anthropic", "name": "Anthropic", "icon": "🧠", "models": ["claude-3.5-sonnet"]},
    {"id": "google", "name": "Google", "icon": "🔍", "models": ["gemini-pro"]},
    {"id": "github", "name": "GitHub", "icon": "🐙", "models": []}
  ],
  languages: [
    {"id": "python", "name": "Python", "frameworks": ["FastAPI", "Django", "Flask"]},
    {"id": "javascript", "name": "JavaScript", "frameworks": ["React", "Vue", "Express"]},
    {"id": "typescript", "name": "TypeScript", "frameworks": ["Next.js", "Nest.js"]},
    {"id": "java", "name": "Java", "frameworks": ["Spring Boot", "Quarkus"]}
  ],
  mcpServers: [
    {"name": "Sandbox", "status": "connected", "tools": 5},
    {"name": "Testing", "status": "connected", "tools": 8},
    {"name": "Documentation", "status": "connected", "tools": 12},
    {"name": "GitHub", "status": "connected", "tools": 15},
    {"name": "Bright Data", "status": "disconnected", "tools": 0}
  ],
  sampleTasks: [
    "Создай REST API для управления пользователями с авторизацией",
    "Разработай веб-приложение для управления задачами",
    "Создай микросервис для обработки платежей",
    "Напиши парсер для анализа логов сервера"
  ],
  metrics: {
    totalRequests: 1247,
    successRate: 94.2,
    averageTime: 15.6,
    costToday: 12.45,
    tokensUsed: 156789
  }
};

// Состояние приложения
class AppState {
  constructor() {
    this.currentSection = 'home';
    this.theme = localStorage.getItem('theme') || 'light';
    this.apiKeys = JSON.parse(localStorage.getItem('apiKeys')) || {};
    this.settings = JSON.parse(localStorage.getItem('settings')) || {
      agentTimeout: 300,
      maxTokens: 4000,
      temperature: 0.7,
      autoSave: true,
      notifications: true,
      analytics: false
    };
    this.generatedCode = null;
    this.isGenerating = false;
  }

  saveApiKeys() {
    localStorage.setItem('apiKeys', JSON.stringify(this.apiKeys));
  }

  saveSettings() {
    localStorage.setItem('settings', JSON.stringify(this.settings));
  }
}

const state = new AppState();

// Утилиты
class Utils {
  static showNotification(title, message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification--${type}`;
    
    const icons = {
      success: '✅',
      error: '❌',
      warning: '⚠️',
      info: 'ℹ️'
    };

    notification.innerHTML = `
      <div class="notification__icon">${icons[type]}</div>
      <div class="notification__content">
        <div class="notification__title">${title}</div>
        <div class="notification__message">${message}</div>
      </div>
      <button class="notification__close">×</button>
    `;

    document.getElementById('notifications').appendChild(notification);

    // Автоматическое удаление через 5 секунд
    setTimeout(() => {
      notification.remove();
    }, 5000);

    // Закрытие по клику
    notification.querySelector('.notification__close').addEventListener('click', () => {
      notification.remove();
    });
  }

  static showModal(title, content, actions = []) {
    const modal = document.getElementById('modal');
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');
    const modalFooter = document.getElementById('modalFooter');

    modalTitle.textContent = title;
    modalBody.innerHTML = content;
    
    modalFooter.innerHTML = '';
    actions.forEach(action => {
      const button = document.createElement('button');
      button.className = `btn ${action.class || 'btn--primary'}`;
      button.textContent = action.text;
      button.addEventListener('click', action.handler);
      modalFooter.appendChild(button);
    });

    modal.classList.add('active');
  }

  static hideModal() {
    document.getElementById('modal').classList.remove('active');
  }

  static showProgress(text = 'Загрузка...') {
    const progressBar = document.getElementById('progressBar');
    const progressText = progressBar.querySelector('.progress-bar__text');
    progressText.textContent = text;
    progressBar.classList.add('active');
  }

  static updateProgress(percent) {
    const fill = document.querySelector('.progress-bar__fill');
    fill.style.width = `${percent}%`;
  }

  static hideProgress() {
    document.getElementById('progressBar').classList.remove('active');
    Utils.updateProgress(0);
  }

  static formatCode(code, language) {
    // Простая подсветка синтаксиса
    let formatted = code
      .replace(/(def|class|import|from|return|if|else|elif|for|while|try|except|with|as)\b/g, '<span class="keyword">$1</span>')
      .replace(/(["'])((?:\\.|(?!\1)[^\\])*?)\1/g, '<span class="string">$1$2$1</span>')
      .replace(/(#.*$)/gm, '<span class="comment">$1</span>');
    
    return `<div class="code-content">${formatted}</div>`;
  }

  static downloadFile(content, filename) {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }
}

// Навигация
class Navigation {
  static init() {
    // Клики по навигации
    document.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', (e) => {
        const section = e.target.dataset.section;
        Navigation.showSection(section);
      });
    });

    // Кнопки навигации в контенте
    document.querySelectorAll('[data-navigate]').forEach(button => {
      button.addEventListener('click', (e) => {
        const section = e.target.dataset.navigate;
        Navigation.showSection(section);
      });
    });

    // Применение темы
    Navigation.applyTheme();
  }

  static showSection(sectionId) {
    // Скрыть все секции
    document.querySelectorAll('.section').forEach(section => {
      section.classList.remove('active');
    });

    // Показать выбранную секцию
    document.getElementById(sectionId).classList.add('active');

    // Обновить активную навигацию
    document.querySelectorAll('.nav-link').forEach(link => {
      link.classList.remove('active');
    });
    
    const activeLink = document.querySelector(`[data-section="${sectionId}"]`);
    if (activeLink) {
      activeLink.classList.add('active');
    }

    state.currentSection = sectionId;

    // Инициализация специфичного контента
    switch (sectionId) {
      case 'generator':
        CodeGenerator.init();
        break;
      case 'apikeys':
        ApiKeyManager.render();
        break;
      case 'monitoring':
        Monitoring.init();
        break;
      case 'settings':
        Settings.init();
        break;
    }
  }

  static applyTheme() {
    document.documentElement.setAttribute('data-color-scheme', state.theme);
    const themeIcon = document.querySelector('.theme-icon');
    themeIcon.textContent = state.theme === 'dark' ? '☀️' : '🌙';
  }
}

// Управление API ключами
class ApiKeyManager {
  static render() {
    const grid = document.getElementById('apiKeysGrid');
    grid.innerHTML = '';

    appData.providers.forEach(provider => {
      const hasKey = state.apiKeys[provider.id];
      const card = document.createElement('div');
      card.className = 'api-key-card';
      card.innerHTML = `
        <div class="api-key-card__header">
          <div class="api-key-card__provider">
            <div class="api-key-card__icon">${provider.icon}</div>
            <div class="api-key-card__name">${provider.name}</div>
          </div>
          <div class="api-key-card__actions">
            ${hasKey ? `
              <button class="btn btn--sm btn--outline" onclick="ApiKeyManager.editKey('${provider.id}')">Изменить</button>
              <button class="btn btn--sm btn--secondary" onclick="ApiKeyManager.deleteKey('${provider.id}')">Удалить</button>
            ` : `
              <button class="btn btn--sm btn--primary" onclick="ApiKeyManager.addKey('${provider.id}')">Добавить</button>
            `}
          </div>
        </div>
        <div class="api-key-card__info">
          <div class="api-key-card__item">
            <span class="api-key-card__label">Статус:</span>
            <span class="api-key-card__value">
              <span class="status ${hasKey ? 'status--success' : 'status--error'}">
                ${hasKey ? 'Настроен' : 'Не настроен'}
              </span>
            </span>
          </div>
          ${hasKey ? `
            <div class="api-key-card__item">
              <span class="api-key-card__label">Ключ:</span>
              <span class="api-key-card__value">****${state.apiKeys[provider.id].slice(-4)}</span>
            </div>
            <div class="api-key-card__item">
              <span class="api-key-card__label">Модели:</span>
              <span class="api-key-card__value">${provider.models.length || 'N/A'}</span>
            </div>
          ` : ''}
        </div>
      `;
      grid.appendChild(card);
    });
  }

  static addKey(providerId) {
    const provider = appData.providers.find(p => p.id === providerId);
    const content = `
      <div class="form-group">
        <label class="form-label">API Ключ для ${provider.name}</label>
        <input type="password" class="form-control" id="apiKeyInput" placeholder="Введите API ключ">
      </div>
      <div class="form-group">
        <label class="form-label">Название (опционально)</label>
        <input type="text" class="form-control" id="apiKeyName" placeholder="Мой ключ ${provider.name}">
      </div>
    `;

    Utils.showModal(`Добавить ключ ${provider.name}`, content, [
      {
        text: 'Отмена',
        class: 'btn--outline',
        handler: Utils.hideModal
      },
      {
        text: 'Сохранить',
        class: 'btn--primary',
        handler: () => {
          const key = document.getElementById('apiKeyInput').value.trim();
          const name = document.getElementById('apiKeyName').value.trim();
          
          if (!key) {
            Utils.showNotification('Ошибка', 'Введите API ключ', 'error');
            return;
          }

          state.apiKeys[providerId] = key;
          state.saveApiKeys();
          Utils.hideModal();
          ApiKeyManager.render();
          Utils.showNotification('Успешно', `API ключ для ${provider.name} добавлен`, 'success');
        }
      }
    ]);
  }

  static editKey(providerId) {
    const provider = appData.providers.find(p => p.id === providerId);
    const currentKey = state.apiKeys[providerId];
    
    const content = `
      <div class="form-group">
        <label class="form-label">API Ключ для ${provider.name}</label>
        <input type="password" class="form-control" id="apiKeyInput" value="${currentKey}" placeholder="Введите API ключ">
      </div>
    `;

    Utils.showModal(`Изменить ключ ${provider.name}`, content, [
      {
        text: 'Отмена',
        class: 'btn--outline',
        handler: Utils.hideModal
      },
      {
        text: 'Сохранить',
        class: 'btn--primary',
        handler: () => {
          const key = document.getElementById('apiKeyInput').value.trim();
          
          if (!key) {
            Utils.showNotification('Ошибка', 'Введите API ключ', 'error');
            return;
          }

          state.apiKeys[providerId] = key;
          state.saveApiKeys();
          Utils.hideModal();
          ApiKeyManager.render();
          Utils.showNotification('Успешно', `API ключ для ${provider.name} обновлен`, 'success');
        }
      }
    ]);
  }

  static deleteKey(providerId) {
    const provider = appData.providers.find(p => p.id === providerId);
    
    Utils.showModal(`Удалить ключ ${provider.name}`, 
      `<p>Вы уверены, что хотите удалить API ключ для ${provider.name}?</p>`, [
      {
        text: 'Отмена',
        class: 'btn--outline',
        handler: Utils.hideModal
      },
      {
        text: 'Удалить',
        class: 'btn--secondary',
        handler: () => {
          delete state.apiKeys[providerId];
          state.saveApiKeys();
          Utils.hideModal();
          ApiKeyManager.render();
          Utils.showNotification('Успешно', `API ключ для ${provider.name} удален`, 'success');
        }
      }
    ]);
  }
}

// Генератор кода
class CodeGenerator {
  static init() {
    const languageSelect = document.getElementById('languageSelect');
    const frameworkSelect = document.getElementById('frameworkSelect');
    
    // Заполнение языков
    languageSelect.innerHTML = '<option value="">Выберите язык</option>';
    appData.languages.forEach(lang => {
      const option = document.createElement('option');
      option.value = lang.id;
      option.textContent = lang.name;
      languageSelect.appendChild(option);
    });

    // Обработка изменения языка
    languageSelect.addEventListener('change', (e) => {
      const languageId = e.target.value;
      frameworkSelect.innerHTML = '<option value="">Выберите фреймворк</option>';
      frameworkSelect.disabled = !languageId;

      if (languageId) {
        const language = appData.languages.find(l => l.id === languageId);
        language.frameworks.forEach(framework => {
          const option = document.createElement('option');
          option.value = framework;
          option.textContent = framework;
          frameworkSelect.appendChild(option);
        });
        frameworkSelect.disabled = false;
      }
    });

    // Примеры задач
    CodeGenerator.renderSampleTasks();

    // Кнопка генерации
    document.getElementById('generateCode').addEventListener('click', CodeGenerator.generateCode);

    // Кнопки действий с кодом
    document.getElementById('downloadCode').addEventListener('click', CodeGenerator.downloadCode);
    document.getElementById('shareToGit').addEventListener('click', CodeGenerator.shareToGit);
  }

  static renderSampleTasks() {
    const grid = document.querySelector('.sample-tasks__grid');
    grid.innerHTML = '';

    appData.sampleTasks.forEach(task => {
      const taskElement = document.createElement('div');
      taskElement.className = 'sample-task';
      taskElement.textContent = task;
      taskElement.addEventListener('click', () => {
        document.getElementById('taskDescription').value = task;
      });
      grid.appendChild(taskElement);
    });
  }

  static async generateCode() {
    const languageSelect = document.getElementById('languageSelect');
    const frameworkSelect = document.getElementById('frameworkSelect');
    const taskDescription = document.getElementById('taskDescription');
    const includeTests = document.getElementById('includeTests');
    const includeDocumentation = document.getElementById('includeDocumentation');
    const includeDocker = document.getElementById('includeDocker');

    // Валидация
    if (!languageSelect.value || !taskDescription.value.trim()) {
      Utils.showNotification('Ошибка', 'Выберите язык и опишите задачу', 'error');
      return;
    }

    // Проверка API ключей
    const hasOpenAI = state.apiKeys.openai;
    const hasAnthropic = state.apiKeys.anthropic;
    
    if (!hasOpenAI && !hasAnthropic) {
      Utils.showNotification('Ошибка', 'Добавьте хотя бы один API ключ для генерации', 'error');
      Navigation.showSection('apikeys');
      return;
    }

    state.isGenerating = true;
    Utils.showProgress('Генерация кода...');

    try {
      // Симуляция генерации кода
      await CodeGenerator.simulateGeneration();
      
      const language = appData.languages.find(l => l.id === languageSelect.value);
      const framework = frameworkSelect.value || 'без фреймворка';
      
      const generatedCode = CodeGenerator.generateSampleCode(
        language.name, 
        framework, 
        taskDescription.value,
        {
          tests: includeTests.checked,
          docs: includeDocumentation.checked,
          docker: includeDocker.checked
        }
      );

      state.generatedCode = {
        language: language.name,
        framework: framework,
        code: generatedCode,
        timestamp: new Date().toISOString()
      };

      CodeGenerator.displayCode(generatedCode);
      Utils.showNotification('Успешно', 'Код успешно сгенерирован!', 'success');

    } catch (error) {
      Utils.showNotification('Ошибка', 'Не удалось сгенерировать код', 'error');
    } finally {
      state.isGenerating = false;
      Utils.hideProgress();
    }
  }

  static async simulateGeneration() {
    const steps = [
      { text: 'Анализ требований...', progress: 20 },
      { text: 'Генерация структуры проекта...', progress: 40 },
      { text: 'Создание основного кода...', progress: 60 },
      { text: 'Добавление тестов и документации...', progress: 80 },
      { text: 'Финализация...', progress: 100 }
    ];

    for (const step of steps) {
      document.querySelector('.progress-bar__text').textContent = step.text;
      Utils.updateProgress(step.progress);
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }

  static generateSampleCode(language, framework, task, options) {
    // Генерация примера кода на основе параметров
    let code = '';
    
    if (language === 'Python' && framework === 'FastAPI') {
      code = `from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="Generated API", description="${task}")

# Модель данных
class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    
# Временное хранилище
users_db = []

@app.get("/")
async def root():
    return {"message": "API успешно запущен"}

@app.post("/users/", response_model=User)
async def create_user(user: User):
    user.id = len(users_db) + 1
    users_db.append(user)
    return user

@app.get("/users/", response_model=List[User])
async def get_users():
    return users_db

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="Пользователь не найден")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)`;

      if (options.tests) {
        code += `

# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API успешно запущен"}

def test_create_user():
    response = client.post(
        "/users/",
        json={"name": "Test User", "email": "test@example.com"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test User"`;
      }

      if (options.docker) {
        code += `

# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# requirements.txt
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0`;
      }
    } else {
      code = `// Сгенерированный код для ${language} ${framework}
// Задача: ${task}

console.log("Код успешно сгенерирован!");

// TODO: Реализация функциональности
class CodeGenerator {
    constructor() {
        this.initialized = true;
    }
    
    async generateCode(requirements) {
        // Основная логика генерации
        return "Сгенерированный код";
    }
}

export default CodeGenerator;`;
    }

    return code;
  }

  static displayCode(code) {
    const preview = document.getElementById('codePreview');
    const content = preview.querySelector('.code-preview__content');
    
    content.innerHTML = Utils.formatCode(code, 'python');
    
    // Активация кнопок
    document.getElementById('downloadCode').disabled = false;
    document.getElementById('shareToGit').disabled = false;
  }

  static downloadCode() {
    if (!state.generatedCode) return;
    
    const filename = `generated_${state.generatedCode.language.toLowerCase()}_${Date.now()}.py`;
    Utils.downloadFile(state.generatedCode.code, filename);
    Utils.showNotification('Успешно', 'Код скачан', 'success');
  }

  static shareToGit() {
    if (!state.generatedCode) return;
    
    Utils.showNotification('Информация', 'Интеграция с Git в разработке', 'info');
  }
}

// Мониторинг
class Monitoring {
  static init() {
    Monitoring.updateMetrics();
    Monitoring.renderServers();
    Monitoring.initChart();
  }

  static updateMetrics() {
    document.getElementById('totalRequests').textContent = appData.metrics.totalRequests.toLocaleString();
    document.getElementById('successRate').textContent = `${appData.metrics.successRate}%`;
    document.getElementById('averageTime').textContent = `${appData.metrics.averageTime}s`;
    document.getElementById('costToday').textContent = `$${appData.metrics.costToday}`;
  }

  static renderServers() {
    const grid = document.getElementById('serversGrid');
    grid.innerHTML = '';

    appData.mcpServers.forEach(server => {
      const card = document.createElement('div');
      card.className = 'server-card';
      card.innerHTML = `
        <div class="server-card__header">
          <div class="server-card__name">${server.name}</div>
          <span class="status ${server.status === 'connected' ? 'status--success' : 'status--error'}">
            ${server.status === 'connected' ? 'Подключен' : 'Отключен'}
          </span>
        </div>
        <div class="server-card__tools">
          Инструментов: ${server.tools}
        </div>
      `;
      grid.appendChild(card);
    });
  }

  static initChart() {
    const canvas = document.getElementById('usageChart');
    const ctx = canvas.getContext('2d');
    
    // Простой график использования
    const data = [65, 78, 82, 90, 85, 88, 95];
    const labels = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];
    
    const chartHeight = 300;
    const chartWidth = canvas.width;
    const maxValue = Math.max(...data);
    
    // Очистка canvas
    ctx.clearRect(0, 0, chartWidth, chartHeight);
    
    // Настройка стилей
    ctx.strokeStyle = '#21808D';
    ctx.fillStyle = '#21808D20';
    ctx.lineWidth = 3;
    
    // Рисование графика
    ctx.beginPath();
    data.forEach((value, index) => {
      const x = (index / (data.length - 1)) * chartWidth;
      const y = chartHeight - (value / maxValue) * chartHeight;
      
      if (index === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
    });
    
    ctx.stroke();
    
    // Заливка под графиком
    ctx.lineTo(chartWidth, chartHeight);
    ctx.lineTo(0, chartHeight);
    ctx.closePath();
    ctx.fill();
    
    // Подписи
    ctx.fillStyle = '#626C71';
    ctx.font = '12px var(--font-family-base)';
    ctx.textAlign = 'center';
    
    labels.forEach((label, index) => {
      const x = (index / (labels.length - 1)) * chartWidth;
      ctx.fillText(label, x, chartHeight + 20);
    });
  }
}

// Настройки
class Settings {
  static init() {
    Settings.loadSettings();
    Settings.bindEvents();
  }

  static loadSettings() {
    document.getElementById('agentTimeout').value = state.settings.agentTimeout;
    document.getElementById('maxTokens').value = state.settings.maxTokens;
    document.getElementById('temperature').value = state.settings.temperature;
    document.getElementById('autoSave').checked = state.settings.autoSave;
    document.getElementById('notifications').checked = state.settings.notifications;
    document.getElementById('analytics').checked = state.settings.analytics;
    
    // Обновление отображения значения температуры
    document.querySelector('.range-value').textContent = state.settings.temperature;
  }

  static bindEvents() {
    // Сохранение при изменении
    ['agentTimeout', 'maxTokens', 'autoSave', 'notifications', 'analytics'].forEach(id => {
      const element = document.getElementById(id);
      element.addEventListener('change', Settings.saveSettings);
    });

    // Температура с отображением значения
    const temperatureSlider = document.getElementById('temperature');
    temperatureSlider.addEventListener('input', (e) => {
      document.querySelector('.range-value').textContent = e.target.value;
      Settings.saveSettings();
    });

    // Экспорт/импорт
    document.getElementById('exportSettings').addEventListener('click', Settings.exportSettings);
    document.getElementById('importSettings').addEventListener('click', Settings.importSettings);
  }

  static saveSettings() {
    state.settings = {
      agentTimeout: parseInt(document.getElementById('agentTimeout').value),
      maxTokens: parseInt(document.getElementById('maxTokens').value),
      temperature: parseFloat(document.getElementById('temperature').value),
      autoSave: document.getElementById('autoSave').checked,
      notifications: document.getElementById('notifications').checked,
      analytics: document.getElementById('analytics').checked
    };
    
    state.saveSettings();
    Utils.showNotification('Успешно', 'Настройки сохранены', 'success');
  }

  static exportSettings() {
    const exportData = {
      settings: state.settings,
      apiKeys: Object.keys(state.apiKeys).reduce((acc, key) => {
        acc[key] = '***ENCRYPTED***';
        return acc;
      }, {}),
      timestamp: new Date().toISOString()
    };
    
    Utils.downloadFile(JSON.stringify(exportData, null, 2), 'code-agent-settings.json');
    Utils.showNotification('Успешно', 'Настройки экспортированы', 'success');
  }

  static importSettings() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    
    input.onchange = (e) => {
      const file = e.target.files[0];
      if (!file) return;
      
      const reader = new FileReader();
      reader.onload = (event) => {
        try {
          const data = JSON.parse(event.target.result);
          if (data.settings) {
            state.settings = data.settings;
            state.saveSettings();
            Settings.loadSettings();
            Utils.showNotification('Успешно', 'Настройки импортированы', 'success');
          }
        } catch (error) {
          Utils.showNotification('Ошибка', 'Неверный формат файла', 'error');
        }
      };
      reader.readAsText(file);
    };
    
    input.click();
  }
}

// Git интеграция
class GitIntegration {
  static init() {
    document.getElementById('cloneRepo').addEventListener('click', GitIntegration.cloneRepo);
    document.getElementById('createBranch').addEventListener('click', GitIntegration.createBranch);
    document.getElementById('createCommit').addEventListener('click', GitIntegration.createCommit);
  }

  static async cloneRepo() {
    const repoUrl = document.getElementById('repoUrl').value.trim();
    if (!repoUrl) {
      Utils.showNotification('Ошибка', 'Введите URL репозитория', 'error');
      return;
    }

    Utils.showProgress('Клонирование репозитория...');
    
    // Симуляция клонирования
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    Utils.hideProgress();
    Utils.showNotification('Успешно', 'Репозиторий успешно клонирован', 'success');
  }

  static async createBranch() {
    const branchName = document.getElementById('branchName').value.trim();
    if (!branchName) {
      Utils.showNotification('Ошибка', 'Введите название ветки', 'error');
      return;
    }

    Utils.showProgress('Создание ветки...');
    
    // Симуляция создания ветки
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    Utils.hideProgress();
    Utils.showNotification('Успешно', `Ветка "${branchName}" создана`, 'success');
  }

  static async createCommit() {
    const commitMessage = document.getElementById('commitMessage').value.trim();
    if (!commitMessage) {
      Utils.showNotification('Ошибка', 'Введите сообщение коммита', 'error');
      return;
    }

    Utils.showProgress('Создание коммита...');
    
    // Симуляция создания коммита
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    Utils.hideProgress();
    Utils.showNotification('Успешно', 'Коммит успешно создан', 'success');
  }
}

// Инициализация приложения
document.addEventListener('DOMContentLoaded', () => {
  // Инициализация навигации
  Navigation.init();
  
  // Обработка переключения темы
  document.getElementById('themeToggle').addEventListener('click', () => {
    state.theme = state.theme === 'light' ? 'dark' : 'light';
    localStorage.setItem('theme', state.theme);
    Navigation.applyTheme();
    Utils.showNotification('Тема изменена', `Переключено на ${state.theme === 'dark' ? 'темную' : 'светлую'} тему`, 'info');
  });

  // Обработка кнопки добавления API ключа
  document.getElementById('addApiKey').addEventListener('click', () => {
    Utils.showModal('Выберите провайдера', `
      <div class="providers-grid">
        ${appData.providers.map(provider => `
          <div class="provider-option" onclick="ApiKeyManager.addKey('${provider.id}'); Utils.hideModal();">
            <div class="provider-icon">${provider.icon}</div>
            <div class="provider-name">${provider.name}</div>
          </div>
        `).join('')}
      </div>
      <style>
        .providers-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
        .provider-option { padding: 16px; border: 1px solid var(--color-border); border-radius: 8px; text-align: center; cursor: pointer; transition: all 0.2s; }
        .provider-option:hover { border-color: var(--color-primary); background: var(--color-secondary); }
        .provider-icon { font-size: 24px; margin-bottom: 8px; }
        .provider-name { font-weight: 500; }
      </style>
    `, [
      {
        text: 'Отмена',
        class: 'btn--outline',
        handler: Utils.hideModal
      }
    ]);
  });

  // Закрытие модального окна
  document.getElementById('modalClose').addEventListener('click', Utils.hideModal);
  document.getElementById('modal').addEventListener('click', (e) => {
    if (e.target.id === 'modal') {
      Utils.hideModal();
    }
  });

  // Инициализация Git интеграции
  GitIntegration.init();

  // Показ приветствия
  if (!localStorage.getItem('welcomed')) {
    setTimeout(() => {
      Utils.showNotification(
        'Добро пожаловать!', 
        'Добро пожаловать в агент автоматизированной разработки кода. Начните с настройки API ключей.', 
        'info'
      );
      localStorage.setItem('welcomed', 'true');
    }, 1000);
  }

  // Симуляция WebSocket подключения
  setTimeout(() => {
    Utils.showNotification('Подключение', 'WebSocket соединение установлено', 'success');
  }, 2000);
});