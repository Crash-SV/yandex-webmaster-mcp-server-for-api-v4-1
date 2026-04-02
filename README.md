# Яндекс Вебмастер MCP-сервер

MCP-сервер для Яндекс Вебмастер API v4.1 — полное покрытие: индексация, поисковые запросы, диагностика, переобход, карты сайта, ссылки, мониторинг важных URL.

## Возможности

37 инструментов, покрывающих весь Яндекс Вебмастер API:

- **Пользователь и сайты** — список сайтов, добавление/удаление, информация о сайте
- **Верификация** — статус подтверждения, запуск подтверждения, список владельцев
- **Сводка и ИКС** — общая информация по сайту с индексом качества, история ИКС
- **Поисковые запросы** — популярные запросы (ТОП-3000), история запросов с позициями/кликами/показами, аналитика запросов
- **Переобход** — квота на переобход, отправка URL на переиндексацию, отслеживание задач
- **Диагностика** — проблемы сайта и рекомендации
- **Индексация** — история индексации по HTTP-статусам, примеры проиндексированных страниц
- **Важные URL** — мониторинг критичных страниц, отслеживание изменений
- **Страницы в поиске** — страницы в выдаче (история + примеры), события появления/исчезновения
- **Карты сайта** — автоматически обнаруженные и добавленные вручную карты сайта
- **Ссылки** — внешние обратные ссылки, битые внутренние ссылки

## Установка

```bash
pip install -e .
```

## Настройка

### Переменная окружения

```bash
export YANDEX_WEBMASTER_API_KEY=ваш_oauth_токен
```

### Claude Desktop

Добавьте в `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "yandex-webmaster": {
      "command": "python",
      "args": ["/путь/к/yandex-webmaster-mcp-server-python/src/yandex_webmaster_mcp/server.py"],
      "env": {
        "YANDEX_WEBMASTER_API_KEY": "ваш_oauth_токен"
      }
    }
  }
}
```

### Claude Code

Добавьте в `settings.json`:

```json
{
  "mcpServers": {
    "yandex-webmaster": {
      "command": "python",
      "args": ["/путь/к/yandex-webmaster-mcp-server-python/src/yandex_webmaster_mcp/server.py"],
      "env": {
        "YANDEX_WEBMASTER_API_KEY": "ваш_oauth_токен"
      }
    }
  }
}
```

## Получение OAuth-токена

1. Создайте приложение на https://oauth.yandex.ru/client/new
2. Выберите права: `webmaster:hostinfo` и `webmaster:verify`
3. Получите токен: `https://oauth.yandex.ru/authorize?response_type=token&client_id=ВАШ_CLIENT_ID`
4. Токен действует 6 месяцев

## Примеры использования

```
# Получить user_id
get_user_id()

# Список всех сайтов
get_hosts(user_id="12345")

# Популярные запросы с позициями
get_popular_queries(
    user_id="12345",
    host_id="https:example.com:443",
    date_from="2026-03-01",
    date_to="2026-03-31",
    query_indicator="TOTAL_SHOWS,TOTAL_CLICKS,AVG_SHOW_POSITION"
)

# Отправить страницу на переобход
request_recrawl(
    user_id="12345",
    host_id="https:example.com:443",
    url="https://example.com/updated-page/"
)

# Мониторинг важных страниц
get_important_urls(
    user_id="12345",
    host_id="https:example.com:443"
)
```

## Формат host_id

Яндекс Вебмастер использует особый формат идентификаторов сайтов:
- `https:example.com:443` (не URL — протокол:домен:порт без слешей)
- `http:example.com:80`

Сервер автоматически URL-кодирует host_id при отправке запросов к API.

## Лицензия

MIT
