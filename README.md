
# 🪙 WalletManager

WalletManager — это backend-сервис для управления кошельками, пользователями и транзакциями. Проект построен на принципах **Clean Architecture / DDD-lite** и предоставляет гибкий слой абстракции для работы с бизнес-логикой, валидацией и хранением данных.

---

# 🚀 Основные возможности

* 📦 Управление транзакциями (CRUD операции)
* 👤 Управление пользователями (регистрация, хранение, обработка данных)
* 👛 Управление кошельками (балансы, привязка к пользователям, операции)
* 🏗 Реестр типов сущностей (Transaction / User / Wallet Registry)
* 🏭 Раздельные фабрики для создания объектов каждого домена
* 🧾 Валидация входных данных через слой схем (Pydantic-based DTO)
* ⚡ In-memory репозитории (легко заменяются на PostgreSQL / Redis)
* ❗ Доменные исключения вместо использования `None`
* 🧩 Расширяемая архитектура под новые типы операций и бизнес-сущности
* 💱 Встроенные парсеры валют и подготовка к интеграции с rate providers

---

# 🧠 Архитектура проекта

Проект разделён на несколько ключевых слоёв в соответствии с принципами **Clean Architecture / DDD-lite**.

---

## 📌 Domain layer

Содержит бизнес-сущности и инварианты предметной области. Не зависит от инфраструктуры.

### 💳 Transactions

* `TransactionBase` — базовая доменная модель транзакции
* `TransactionTypesEnum` — типы транзакций
* `TransactionStatusesEnum` — статусы операций

### 👤 Users

* `UserBase` — доменная модель пользователя
* базовые правила и ограничения пользователя

### 👛 Wallets

* `WalletBase` — доменная модель кошелька
* баланс, ownership и связи с пользователями

---

## 📌 Application layer

Слой бизнес-логики и оркестрации доменных объектов.

### 💳 Transactions

* `TransactionFactory` — создание транзакций по типу
* `TransactionRegistry` — регистрация доступных типов транзакций

### 👤 Users

* `UserFactory` — создание пользователей
* `UserService` — бизнес-операции над пользователями

### 👛 Wallets

* `WalletFactory` — создание кошельков
* `WalletService` — бизнес-логика кошельков (балансы, операции)

---

## ⚙️ Use-cases layer

Слой сценариев использования системы (application orchestration).

* `CreateTransactionUseCase`
* `RegisterUserUseCase`
* `CreateWalletUseCase`
* `TransferBetweenWalletsUseCase`
* `ProcessTransactionUseCase`

📌 Отвечает за описание бизнес-процессов, а не реализацию деталей.

---

## 📌 Schemas layer (DTO / Validation layer)

Слой входных и выходных моделей на базе Pydantic.

### 💳 Transactions schemas

* `CreateTransactionSchema`
* `TransactionResponseSchema`

### 👤 Users schemas

* `CreateUserSchema`
* `UserResponseSchema`

### 👛 Wallets schemas

* `CreateWalletSchema`
* `WalletResponseSchema`

📌 Используется для API и строгой валидации данных.

---

## 📌 Infrastructure layer

Слой хранения данных и внешних интеграций.

### 💳 Transactions

* `TransactionRepository` — in-memory storage

### 👤 Users

* `UserRepository` — хранилище пользователей

### 👛 Wallets

* `WalletRepository` — хранилище кошельков

### 💱 Parsers

* `currency_parser.py` — парсинг валют
* подготовка к интеграции с external rate providers

---

## 📌 Core layer

Общие компоненты системы:

* 🔢 Enums (transactions / users / wallets)
* 🧰 Utilities (helpers, decorators, parsers)
* ⚠️ Validations (exceptions, invariants)
* 📊 Logging configuration

---

# 🧩 Используемые архитектурные паттерны

Проект реализует комбинацию современных паттернов:

* 🏭 Factory Pattern — создание объектов домена
* 🗂 Registry Pattern — динамическая регистрация типов
* 🎭 Strategy Pattern — вариативное поведение кошельков/операций
* 🧱 Facade Pattern — упрощение взаимодействия с подсистемами
* 🪝 Decorator Pattern — расширение логики без изменения кода

---

# 🔮 Возможные улучшения

* 🗄 PostgreSQL / SQLAlchemy repository layer
* ⚡ Async architecture (FastAPI integration)
* 📡 Event-driven system (domain events)
* 🔄 Unit of Work pattern
* 📊 CQRS (разделение read/write моделей)
* 🌐 External exchange rate API integration

---

# 🎯 Цель проекта

Проект создан как демонстрация:

* архитектурного мышления в backend-разработке
* применения Clean Architecture / DDD-lite
* работы с паттернами проектирования
* построения расширяемых систем уровня production backend
