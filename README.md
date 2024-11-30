# Referral System

## Описание функционала

**Реферальная система** позволяет пользователям:

### 1. Авторизация по номеру телефона
- Пользователь вводит номер телефона.
- Генерируется и отправляется **4-значный код подтверждения** (эмуляция).
- Пользователь вводит код для завершения авторизации.
- При первом входе создается новый пользователь в базе данных.

### 2. Работа с реферальными кодами
- При создании каждого пользователя автоматически генерируется **уникальный 6-значный инвайт-код** (цифры и символы).
- Пользователь может ввести чужой инвайт-код, чтобы зарегистрироваться как реферал.

### 3. Управление рефералами
- В профиле пользователя отображается:
  - Личный **реферальный код**.
  - Инвайт-код, который пользователь активировал (если есть).
  - Список номеров телефонов пользователей, которые использовали его реферальный код.

---

## API

API предоставляет следующие эндпоинты:

### 1. **Авторизация по номеру телефона**
- **URL**: `/api/login/`
- **Метод**: `POST`
- **Описание**: Отправка кода подтверждения на номер телефона и завершение авторизации.

1. Авторизация по номеру телефона
POST /api/login/
Отправляет код подтверждения (симуляция).

Тело запроса:
json
```
{
  "phone_number": "+1234567890"
}
```
Ответ:
json
```
{
  "message": "OTP sent"
}
```
2. Подтверждение OTP
POST /api/verify/
Подтверждает введенный код и завершает авторизацию.

Тело запроса:
json
```
{
  "otp": "1234"
}
```
Ответ:
json
```
{
  "user_id": 1,
  "created": true
}
```
3. Получение профиля пользователя
GET /api/profile/<user_id>/
Возвращает данные профиля.

Пример запроса:


GET /api/profile/1/
Ответ:
json
```
{
  "id": 1,
  "phone_number": "+1234567890",
  "invite_code": "AB12CD",
  "referred_by": "XY34ZQ",
  "referred_users": [
    "+0987654321",
    "+1122334455"
  ]
}
```
4. Активация инвайт-кода
POST /api/profile/<user_id>/
Позволяет пользователю ввести реферальный код.

Тело запроса:
json
```
{
  "invite_code": "XY34ZQ"
}
```
Ответ:
json
```
{
  "message": "Referral code activated"
}
```
Если код уже был использован:

json
```
{
  "error": "Referral code already used"
}
```
Если код не найден:

json
```
{
  "error": "Invalid invite code"
}
```
Тестирование API
Все эндпоинты можно протестировать через Postman:

Импортируйте файл postman_collection.json в Postman.
Запустите соответствующие запросы по шагам:
Авторизация (/login/ → /verify/).
Работа с профилем (/profile/<user_id>/).
