


# 🪙 WalletManager

WalletManager — это backend-сервис для управления пользователями, кошельками, балансами и транзакциями.
Проект построен на принципах **Clean Architecture / DDD-lite** с явным разделением домена, инфраструктуры и сценариев использования.

---

# 🚀 Основные возможности

* 👤 Управление пользователями (регистрация, логин, блокировка)
* 👛 Управление кошельками (создание, блокировка, закрытие)
* 💰 Управление балансами:

  * обычные (1 валюта)
  * мультивалютные (несколько валют в одном кошельке)
* 💳 Управление транзакциями:

  * пополнение
  * вывод
  * обмен
* 🏭 Factory + Registry для всех доменных сущностей
* 🔄 Mapper слой (domain ↔ database)
* 🧠 Инварианты домена (DomainInvariant)
* 🪝 Сигналы через blinker (реакция на изменения)
* 🗄 SQLAlchemy + PostgreSQL
* 📦 Facade слой для use-cases

---

# 🧠 Архитектура проекта

Проект разделён на слои в стиле **Clean Architecture**.

---

## 📌 Domain layer

Чистая бизнес-логика.
**Не зависит от БД, фреймворков и инфраструктуры.**

### 👤 Users

* `UserBase`, `Client`, `Admin`
* инварианты (email, name, password)
* статус пользователя

### 👛 Wallets

* `DebitWallet`, `CreditWallet`
* связь с пользователем
* блокировка / закрытие

### 💰 Balances

* `RegularBalance` — одна валюта
* `ForeignBalance` — несколько валют
* хранение как `dict[currency -> amount]`

### 💳 Transactions

* `DepositTransaction`
* `WithdrawTransaction`
* `ExchangeTransaction`

📌 В домене:

* нет ORM
* нет SQL
* только логика и инварианты

---

## 📌 Infrastructure layer

Работа с БД и внешними зависимостями.

### 🗄 Database (SQLAlchemy)

* `UserTable`
* `WalletTable`
* `BalanceTable`
* `TransactionTable`

### 🔄 Mappers

Преобразование:

```
Domain ↔ ORM (SQLAlchemy)
```

* `UserMapper`
* `WalletMapper`
* `BalanceMapper`
* `TransactionMapper`

📌 Важный момент:

* ForeignBalance хранится **как несколько строк в БД**
* и собирается обратно через grouping

---

### 📦 Repositories

Разделены на:

* `commands` — запись (insert/update/delete)
* `queries` — чтение

Пример:

* `UserCommandsRepository`
* `WalletQueriesRepository`
* `BalanceCommandsRepository`

---

## ⚙️ Application / Use-cases layer

Сценарии использования системы.

### 👤 Users

* `CreateUserService`
* `LoginUserService`
* `BlockUserService`
* `CloseUserService`

### 👛 Wallets

* `CreateWalletService`
* `BlockWalletService`
* `CloseWalletService`

### 💰 Balances

* `CreateBalanceService`
* `FreezeBalanceService`
* `ShowBalanceService`

### 💳 Transactions

* `CreateTransactionService`
* `ShowTransactionService`
* `SortTransactionService`

---

## 🎭 Facade layer

Упрощает работу с системой:

* `UserServiceFacade`
* `WalletServiceFacade`
* `BalanceServiceFacade`
* `TransactionServiceFacade`

📌 Позволяет не работать напрямую с кучей сервисов

---

## 🏭 Factory + Registry

Для каждой сущности:

* Factory — создаёт объект
* Registry — хранит соответствие типа → класса

Пример:

```
BalanceTypesEnum.FOREIGN → ForeignBalance
```

📌 Это даёт:

* расширяемость
* отсутствие if/else
* гибкую регистрацию новых типов

---

## 🧩 Core layer

Общие компоненты:

* 🔢 Enums (User, Wallet, Balance, Transaction)
* ⚠️ DomainInvariant (валидация)
* 🪝 Signals (blinker)
* 🧰 utils / decorators
* 📊 logging

---

# 🔥 Особенности реализации

### 1. Мультивалютный баланс

В БД:

```
wallet_id | currency | amount
```

В домене:

```
{ "BTC": 2, "USDT": 3, "TON": 5 }
```

📌 Сборка происходит через:

```
grouped[obj.balance_id]
```

---

### 2. Domain invariants

Валидация прямо в домене:

```python
DomainInvariant.no_empty(...)
DomainInvariant.is_instance(...)
```

📌 Гарантирует корректное состояние объектов

---

### 3. Signals (blinker)

При изменении:

```python
user_upgrade_signal.send(...)
```

📌 Можно легко добавить:

* логирование
* аудит
* события

---

### 4. Mapper слой

Ты явно разделил:

```
DB модель ≠ Domain модель
```

📌 Это очень сильное архитектурное решение

---

# 🧩 Используемые паттерны

* 🏭 Factory Pattern
* 🗂 Registry Pattern
* 🎭 Facade Pattern
* 🧱 Mapper Pattern
* 🪝 Observer (через signals)
* 🧠 DDD-lite (агрегаты + инварианты)

---

# 🔮 Возможные улучшения

Если идти дальше:

### 🔹 Архитектура

* Unit of Work
* CQRS (разделить read/write модели)
* Domain Events (вместо прямых сигналов)

### 🔹 Инфраструктура

* Alembic migrations (нормально настроить)
* async SQLAlchemy
* Redis (кэш / блокировки)

### 🔹 DI

* подключить DI (например Dishka)

### 🔹 API

* FastAPI слой
* Pydantic DTO для входа/выхода

---

# 🎯 Цель проекта

Проект демонстрирует:

* умение строить **сложную backend архитектуру**
* разделение ответственности
* работу с ORM без протекания в домен
* применение паттернов на практике
* подготовку к production-level системам