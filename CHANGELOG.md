# 📦 Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- 🐳 **Dockerized** the application with multi-stage builds
- 🔒 **Security hardened** JWT configuration with refresh token rotation
- 📊 **Code coverage enforcement** (95%+ threshold)
- 🧪 **Full test suite** covering auth, ML pipeline, and API endpoints
- 📝 **Comprehensive .sample_env** template with security best practices
- 🔍 **Parallel test execution** with pytest-xdist
- 🚀 **Production-ready** docker-compose.yml with MongoDB, Redis
- 📈 **Model versioning** in MongoDB with performance metrics storage

### Changed
- 🔧 **Upgraded dependencies** to latest stable versions
- 🛠️ **Refactored ML pipeline** for better performance
- 📁 **Reorganized project structure** for better maintainability
- 🔄 **Improved CSV importer** with data validation
- ⚡ **Optimized Docker builds** with layer caching

### Fixed
- 🐞 **Fixed security vulnerabilities** in dependency chain
- 🛠️ **Resolved race conditions** in model training
- 🧹 **Cleaned up deprecated** API endpoints

### Security
- 🔐 **Encrypted sensitive fields** in MongoDB documents
- 🛡️ **Added Bandit/Safety** security scanning to CI
- 🔒 **Hardened JWT** token settings (15min expiry)
- 🚫 **Disabled DEBUG mode** in production configs

---

## [1.1.0] - 2025-07-15

### Added
- 🔧 Integrated **MongoDB with MongoEngine** for medical data storage
- 📥 **CSV import functionality** for MongoDB collections
- 🤖 **Model training** using XGBoost classifier
- 🌐 **REST API endpoints** for model results and predictions
- 🔐 **JWT authentication** system
- ⚙️ **Management commands** for data import

### Changed
- 🗃️ Refined MongoDB schema for medical data
- 🔄 Improved model training pipeline
- 💾 Enhanced model persistence in MongoDB

### Fixed
- 🐛 CSV import column handling
- 🛠️ Model training edge cases
- 🔄 MongoDB data duplication issues

---

## [1.0.0] - 2025-07-15

### Added
- 🏗️ Initial Django + MongoDB setup
- 🔒 JWT authentication
- 📡 Basic REST API endpoints
- 🧠 Model training endpoint
- 📥 CSV import functionality
- 🛠️ Data preprocessing pipeline

---

## [0.1.0] - 2025-07-15

### Added
- 📝 Basic project documentation
- 🐳 Docker/PostgreSQL setup
- 📦 Initial requirements.txt

---

## 🔄 Versioning

This project uses **Semantic Versioning** (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New backward-compatible features
- **PATCH**: Backward-compatible bug fixes

---

## 📌 Legend

- 🚀 **Added** - New features  
- 🔧 **Changed** - Existing functionality modifications  
- 🗑️ **Deprecated** - Soon-to-be removed features  
- ❌ **Removed** - Deprecated features removed  
- 🐞 **Fixed** - Bug fixes  
- 🛡️ **Security** - Vulnerability fixes  
- 📈 **Performance** - Optimizations  
- 🧪 **Tests** - Testing related changes