
# 🪙 WalletManager

WalletManager is a backend service for managing users, wallets, balances, and transactions.
The project is built using **Clean Architecture / DDD-lite principles** with a clear separation of domain logic, infrastructure, and application use cases.

---

# 🚀 Key Features

* 👤 User management (registration, login, blocking)
* 👛 Wallet management (creation, blocking, closing)
* 💰 Balance management:

  * regular (single currency)
  * multi-currency (multiple assets per wallet)
* 💳 Transaction management:

  * deposit
  * withdrawal
  * exchange
* 🏭 Factory + Registry pattern for all domain entities
* 🔄 Mapper layer (domain ↔ database)
* 🧠 Domain invariants (DomainInvariant)
* 🪝 Event signaling via blinker
* 🗄 SQLAlchemy + PostgreSQL integration
* 📦 Facade layer for use cases

---

# 🧠 Project Architecture

The project is structured according to **Clean Architecture principles**.

---

## 📌 Domain Layer

Pure business logic.
**Does not depend on database, frameworks, or infrastructure.**

### 👤 Users

* `UserBase`, `Client`, `Admin`
* domain invariants (email, name, password)
* user status handling

### 👛 Wallets

* `DebitWallet`, `CreditWallet`
* ownership relation
* blocking / closing logic

### 💰 Balances

* `RegularBalance` — single currency
* `ForeignBalance` — multiple currencies
* stored internally as `dict[currency -> amount]`

### 💳 Transactions

* `DepositTransaction`
* `WithdrawTransaction`
* `ExchangeTransaction`

📌 Domain layer contains:

* no ORM
* no SQL
* only business rules and invariants

---

## 📌 Infrastructure Layer

Handles persistence and external dependencies.

### 🗄 Database (SQLAlchemy)

* `UserTable`
* `WalletTable`
* `BalanceTable`
* `TransactionTable`

---

### 🔄 Mappers

Responsible for transforming:

```
Domain ↔ ORM (SQLAlchemy models)
```

* `UserMapper`
* `WalletMapper`
* `BalanceMapper`
* `TransactionMapper`

📌 Important detail:

* `ForeignBalance` is stored as **multiple rows in DB**
* and reconstructed via grouping

---

### 📦 Repositories

Split into:

* `commands` — write operations (insert/update/delete)
* `queries` — read operations

Examples:

* `UserCommandsRepository`
* `WalletQueriesRepository`
* `BalanceCommandsRepository`

---

## ⚙️ Application / Use-cases Layer

Encapsulates business workflows.

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

## 🎭 Facade Layer

Provides a simplified interface:

* `UserServiceFacade`
* `WalletServiceFacade`
* `BalanceServiceFacade`
* `TransactionServiceFacade`

📌 Avoids direct interaction with multiple services

---

## 🏭 Factory + Registry

Each domain has:

* Factory — creates instances
* Registry — maps type → class

Example:

```
BalanceTypesEnum.FOREIGN → ForeignBalance
```

📌 Benefits:

* extensibility
* no hardcoded conditionals
* easy addition of new types

---

## 🧩 Core Layer

Shared components:

* 🔢 Enums (User, Wallet, Balance, Transaction)
* ⚠️ DomainInvariant (validation rules)
* 🪝 Signals (blinker)
* 🧰 utilities / decorators
* 📊 logging

---

# 🔥 Implementation Highlights

### 1. Multi-currency balance

Stored in DB as:

```
wallet_id | currency | amount
```

In domain:

```
{ "BTC": 2, "USDT": 3, "TON": 5 }
```

📌 Reconstructed using:

```
grouped[obj.balance_id]
```

---

### 2. Domain invariants

Validation happens inside domain models:

```python
DomainInvariant.no_empty(...)
DomainInvariant.is_instance(...)
```

📌 Ensures consistent object state

---

### 3. Signals (blinker)

On state change:

```python
user_upgrade_signal.send(...)
```

📌 Enables:

* logging
* auditing
* event-driven extensions

---

### 4. Mapper layer

Clear separation:

```
Database model ≠ Domain model
```

📌 Prevents ORM leakage into business logic

---

# 🧩 Design Patterns Used

* 🏭 Factory Pattern
* 🗂 Registry Pattern
* 🎭 Facade Pattern
* 🧱 Mapper Pattern
* 🪝 Observer Pattern (via signals)
* 🧠 DDD-lite principles

---

# 🔮 Possible Improvements

### 🔹 Architecture

* Unit of Work pattern
* CQRS (separate read/write models)
* Domain Events (instead of direct signals)

### 🔹 Infrastructure

* Proper Alembic migration setup
* Async SQLAlchemy
* Redis (caching / locks)

### 🔹 Dependency Injection

* Integrate DI container (e.g. Dishka)

### 🔹 API Layer

* FastAPI integration
* Pydantic DTOs for request/response

---

# 🎯 Project Goal

This project demonstrates:

* strong backend architecture design skills
* separation of concerns
* clean domain modeling
* practical usage of design patterns
* building scalable, production-ready systems
