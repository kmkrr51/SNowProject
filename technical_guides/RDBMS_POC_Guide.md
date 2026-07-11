# RDBMS Choices for Python-Based Backend Microservices - POC Grade
## Evaluation Guide & Recommendations

### Document Information
- **Focus:** Small RDBMS for Python microservices POC
- **Use Case:** Proof of Concept, MVP, Small-scale deployments
- **Date:** 2026-07-10
- **Version:** 1.0

---

## Executive Summary

For Python-based backend microservices at POC grade, you need lightweight, easy-to-setup RDBMS solutions that don't require complex infrastructure. This guide evaluates suitable options based on ease of use, Python integration, scalability, and operational overhead.

**Recommendation Priority:**
1. **PostgreSQL** – Best overall for POC (recommended)
2. **SQLite** – Fastest to start, limited scalability
3. **MySQL/MariaDB** – Good alternative, simpler than PostgreSQL
4. **DuckDB** – Excellent for analytics-heavy POC

---

## 1. PostgreSQL (Recommended for Most POC)

### Overview
- **Type:** Open-source relational database
- **Best For:** Production-ready POC, complex queries, JSON support
- **Maturity:** Highly mature, production-proven
- **Cost:** Free, open-source

### Advantages
✅ **Python Integration**
- Excellent psycopg2 driver (most popular)
- SQLAlchemy ORM support (excellent)
- Async support via asyncpg (high performance)
- Type hints and modern Python support

✅ **Features**
- ACID compliance
- Advanced data types (JSON, Arrays, UUID)
- Full-text search
- Window functions
- Common Table Expressions (CTEs)
- Extensible (custom types, functions)

✅ **POC Benefits**
- Easy local setup (Docker: 1 command)
- Excellent documentation
- Large community
- Scales well from POC to production
- Free and open-source

### Disadvantages
❌ Resource-intensive compared to SQLite
❌ Slightly steeper learning curve than MySQL
❌ More configuration options (can be overwhelming)

### Setup for POC

**Docker Setup (Recommended):**
```bash
docker run --name postgres-poc \
  -e POSTGRES_PASSWORD=poc_password \
  -e POSTGRES_DB=poc_db \
  -p 5432:5432 \
  -d postgres:15-alpine
```

**Python Connection:**
```python
import asyncpg
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

# Sync connection
engine = create_engine('postgresql://user:password@localhost/poc_db')

# Async connection (recommended for microservices)
async_engine = create_async_engine(
    'postgresql+asyncpg://user:password@localhost/poc_db'
)
```

### Use Cases
- ✅ Complex business logic POC
- ✅ Multi-service microservices POC
- ✅ Data-heavy applications
- ✅ Real-time analytics POC
- ✅ Production-grade POC

### Cost & Resources
- **Cost:** Free
- **Memory:** 200-500 MB (minimal)
- **Disk:** 100 MB base
- **Setup Time:** 5 minutes with Docker

### Scaling Path
- POC → MVP → Production (same database)
- Excellent upgrade path

---

## 2. SQLite (Fastest to Start)

### Overview
- **Type:** Embedded relational database
- **Best For:** Single-service POC, rapid prototyping, testing
- **Maturity:** Extremely mature, battle-tested
- **Cost:** Free, public domain

### Advantages
✅ **Simplicity**
- Zero setup required
- File-based (no server needed)
- Perfect for rapid prototyping
- Excellent for testing

✅ **Python Integration**
- Built-in sqlite3 module (no external dependency)
- SQLAlchemy support
- Excellent for development

✅ **POC Benefits**
- Fastest time to first query
- No infrastructure needed
- Perfect for single-service POC
- Excellent for learning

### Disadvantages
❌ **Scalability Issues**
- Single file-based
- Limited concurrent writes
- Not suitable for multi-service POC
- Performance degrades with large datasets

❌ **Production Concerns**
- Not designed for production
- Limited concurrency
- No network access (by default)
- Difficult to scale horizontally

### Setup for POC

**Python Connection:**
```python
import sqlite3
from sqlalchemy import create_engine

# Direct connection
conn = sqlite3.connect('poc.db')

# SQLAlchemy
engine = create_engine('sqlite:///poc.db')
```

### Use Cases
- ✅ Single-service POC
- ✅ Rapid prototyping
- ✅ Learning/experimentation
- ✅ Unit testing
- ✅ Desktop applications

### Cost & Resources
- **Cost:** Free
- **Memory:** Minimal (< 50 MB)
- **Disk:** Variable (starts at 0)
- **Setup Time:** 0 minutes

### Scaling Path
- POC → Need to migrate to PostgreSQL/MySQL
- Not suitable for production

---

## 3. MySQL 8.0 / MariaDB

### Overview
- **Type:** Open-source relational database
- **Best For:** Web application POC, simpler alternative to PostgreSQL
- **Maturity:** Highly mature
- **Cost:** Free, open-source

### Advantages
✅ **Simplicity**
- Easier to learn than PostgreSQL
- Simpler configuration
- Good documentation

✅ **Python Integration**
- mysql-connector-python
- PyMySQL (pure Python)
- SQLAlchemy support
- Async support via aiomysql

✅ **POC Benefits**
- Easy Docker setup
- Good performance for typical workloads
- Familiar to many developers
- Scales reasonably well

### Disadvantages
❌ **Feature Limitations**
- Fewer advanced features than PostgreSQL
- Limited JSON support (improving in MySQL 8.0)
- No native array types
- Less powerful query optimization

❌ **Python Integration**
- Drivers less mature than PostgreSQL
- Async support less robust

### Setup for POC

**Docker Setup:**
```bash
docker run --name mysql-poc \
  -e MYSQL_ROOT_PASSWORD=poc_password \
  -e MYSQL_DATABASE=poc_db \
  -p 3306:3306 \
  -d mysql:8.0
```

**Python Connection:**
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

# Sync connection
engine = create_engine('mysql+pymysql://root:password@localhost/poc_db')

# Async connection
async_engine = create_async_engine(
    'mysql+aiomysql://root:password@localhost/poc_db'
)
```

### Use Cases
- ✅ Web application POC
- ✅ CRUD-heavy applications
- ✅ Simple business logic POC
- ✅ Team familiar with MySQL

### Cost & Resources
- **Cost:** Free
- **Memory:** 200-400 MB
- **Disk:** 100 MB base
- **Setup Time:** 5 minutes

### Scaling Path
- POC → MVP → Production (same database)
- Good upgrade path

---

## 4. DuckDB (Analytics-Heavy POC)

### Overview
- **Type:** In-process analytical database
- **Best For:** Analytics POC, data processing, OLAP workloads
- **Maturity:** Rapidly maturing, increasingly popular
- **Cost:** Free, open-source

### Advantages
✅ **Performance**
- Extremely fast for analytical queries
- Excellent for data processing
- In-process (no network overhead)

✅ **Python Integration**
- Native Python API
- Pandas integration (excellent)
- Parquet support
- SQL interface

✅ **POC Benefits**
- Zero setup
- Perfect for data-heavy POC
- Excellent for prototyping analytics
- Great for batch processing

### Disadvantages
❌ **Not for OLTP**
- Designed for analytics, not transactions
- Limited concurrent write support
- Not suitable for real-time transactional workloads

❌ **Microservices Concerns**
- In-process only (not network accessible)
- Not suitable for multi-service POC
- Limited concurrency

### Setup for POC

**Python Connection:**
```python
import duckdb

# In-process connection
conn = duckdb.connect('poc.duckdb')

# In-memory (for testing)
conn = duckdb.connect(':memory:')

# SQL queries
result = conn.execute('SELECT * FROM table').fetchall()

# Pandas integration
import pandas as pd
df = conn.execute('SELECT * FROM table').df()
```

### Use Cases
- ✅ Analytics POC
- ✅ Data processing pipeline POC
- ✅ OLAP workloads
- ✅ Batch processing
- ✅ Data exploration

### Cost & Resources
- **Cost:** Free
- **Memory:** Minimal (< 100 MB)
- **Disk:** Variable
- **Setup Time:** 0 minutes

### Scaling Path
- POC → Need to migrate to PostgreSQL/Snowflake
- Not suitable for production transactional systems

---

## 5. Comparison Matrix

| Feature | PostgreSQL | SQLite | MySQL | DuckDB |
|---------|-----------|--------|-------|--------|
| **Setup Time** | 5 min | 0 min | 5 min | 0 min |
| **Python Integration** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Scalability** | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Concurrency** | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Features** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Production Ready** | ✅ | ❌ | ✅ | ❌ |
| **Multi-Service** | ✅ | ❌ | ✅ | ❌ |
| **Analytics** | ✅ | ⚠️ | ⚠️ | ⭐⭐⭐⭐⭐ |
| **Memory Usage** | Medium | Low | Medium | Low |
| **Cost** | Free | Free | Free | Free |

---

## 6. POC Scenario Recommendations

### Scenario 1: Multi-Service Microservices POC
**Recommendation:** PostgreSQL
```
- Multiple independent services
- Shared database or service-specific databases
- Complex business logic
- Need for transactions

Setup:
docker-compose with PostgreSQL + 3-4 microservices
```

### Scenario 2: Single-Service POC / MVP
**Recommendation:** PostgreSQL or MySQL
```
- Single service
- Simple to moderate complexity
- Production-grade requirements

Setup:
Docker with PostgreSQL/MySQL + single service
```

### Scenario 3: Rapid Prototyping / Learning
**Recommendation:** SQLite
```
- Quick experimentation
- Learning database concepts
- No infrastructure needed

Setup:
SQLite file + Python script
```

### Scenario 4: Analytics / Data Processing POC
**Recommendation:** DuckDB
```
- Data processing pipeline
- Analytics queries
- Batch processing

Setup:
DuckDB in-process + Python scripts
```

### Scenario 5: Hybrid Approach (Recommended for Complex POC)
**Recommendation:** PostgreSQL + DuckDB
```
- PostgreSQL for transactional data
- DuckDB for analytics/reporting

Setup:
PostgreSQL for OLTP + DuckDB for OLAP
```

---

## 7. Python ORM & Driver Recommendations

### For PostgreSQL
**Recommended Stack:**
```python
# Async (recommended for microservices)
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import AsyncSession
import asyncpg

# Sync (simpler, good for POC)
from sqlalchemy import create_engine
import psycopg2

# Direct async (highest performance)
import asyncpg
```

### For MySQL
**Recommended Stack:**
```python
# Async
from sqlalchemy.ext.asyncio import create_async_engine
import aiomysql

# Sync
from sqlalchemy import create_engine
import pymysql
```

### For SQLite
**Recommended Stack:**
```python
# Built-in
import sqlite3

# SQLAlchemy
from sqlalchemy import create_engine
```

### For DuckDB
**Recommended Stack:**
```python
import duckdb
import pandas as pd
```

---

## 8. Quick Start Guide

### PostgreSQL POC (5 minutes)

**Step 1: Start Database**
```bash
docker run --name pg-poc -e POSTGRES_PASSWORD=poc -p 5432:5432 -d postgres:15-alpine
```

**Step 2: Create Python Service**
```python
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String

app = FastAPI()
DATABASE_URL = "postgresql+asyncpg://postgres:poc@localhost/postgres"

engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_fetch=False)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)

@app.post("/users/")
async def create_user(name: str):
    async with async_session() as session:
        user = User(name=name)
        session.add(user)
        await session.commit()
        return user
```

**Step 3: Run**
```bash
pip install fastapi sqlalchemy asyncpg uvicorn
uvicorn main:app --reload
```

### SQLite POC (2 minutes)

**Step 1: Create Python Service**
```python
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI()
DATABASE_URL = "sqlite:///./poc.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)

Base.metadata.create_all(bind=engine)

@app.post("/users/")
def create_user(name: str):
    db = SessionLocal()
    user = User(name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
```

**Step 2: Run**
```bash
pip install fastapi sqlalchemy uvicorn
uvicorn main:app --reload
```

---

## 9. Migration Path

### SQLite → PostgreSQL
```python
# Export from SQLite
import sqlite3
import json

conn = sqlite3.connect('poc.db')
cursor = conn.cursor()

# Import to PostgreSQL
import psycopg2
pg_conn = psycopg2.connect("dbname=poc_db user=postgres")
```

### MySQL → PostgreSQL
```bash
# Using pg_chameleon or similar tools
# Or manual migration with scripts
```

---

## 10. Recommendations Summary

### Best Overall for POC: **PostgreSQL**
- ✅ Production-ready
- ✅ Excellent Python support
- ✅ Scales from POC to production
- ✅ Rich feature set
- ✅ Easy to learn

**Setup Time:** 5 minutes
**Recommendation:** Use this for most POC scenarios

### Best for Rapid Prototyping: **SQLite**
- ✅ Zero setup
- ✅ Perfect for learning
- ✅ Excellent for single-service POC

**Setup Time:** 0 minutes
**Recommendation:** Use for quick experiments, then migrate to PostgreSQL

### Best for Analytics: **DuckDB**
- ✅ Extremely fast
- ✅ Excellent Pandas integration
- ✅ Zero setup

**Setup Time:** 0 minutes
**Recommendation:** Use for analytics/data processing POC

### Best for Simplicity: **MySQL**
- ✅ Simpler than PostgreSQL
- ✅ Good performance
- ✅ Familiar to many

**Setup Time:** 5 minutes
**Recommendation:** Use if team prefers MySQL

---

## 11. Conclusion

For Python-based backend microservices POC:

1. **Start with PostgreSQL** – Best all-around choice
2. **Use SQLite** – If you need zero setup
3. **Consider DuckDB** – If analytics-heavy
4. **Choose MySQL** – If team prefers it

All are free, have excellent Python support, and can be set up in minutes with Docker.

---

**Document Classification:** Technical Guide
**Last Updated:** 2026-07-10
**Next Review:** 2026-08-10
