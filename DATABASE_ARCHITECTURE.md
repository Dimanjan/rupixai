# RupixAI Database Architecture

## Overview

RupixAI uses PostgreSQL as the primary database for production environments, with SQLite as a fallback for development. The database is designed to handle user authentication, image generation jobs, payment transactions, and social login integration.

## Database Schema

### Core Tables

#### 1. User Management
- **auth_user**: Django's built-in user model
  - `id`: Primary key
  - `username`: Unique username
  - `email`: User email (optional)
  - `password`: Hashed password
  - `first_name`, `last_name`: User names
  - `is_active`, `is_staff`, `is_superuser`: User permissions
  - `date_joined`, `last_login`: Timestamps

#### 2. User Profiles
- **api_profile**: Extended user information
  - `id`: Primary key
  - `user_id`: Foreign key to auth_user
  - `credits`: Available credits for image generation
  - `total_images_generated`: Usage statistics

#### 3. Chat System
- **api_chatthread**: Conversation threads
  - `id`: Primary key
  - `user_id`: Foreign key to auth_user
  - `title`: Thread title
  - `created_at`, `updated_at`: Timestamps

- **api_chatmessages**: Individual messages
  - `id`: Primary key
  - `thread_id`: Foreign key to api_chatthread
  - `role`: 'user' or 'assistant'
  - `content`: Message content
  - `created_at`: Timestamp

#### 4. Image Generation
- **api_imagejob**: Image generation requests
  - `id`: Primary key
  - `user_id`: Foreign key to auth_user
  - `thread_id`: Foreign key to api_chatthread (nullable)
  - `provider`: 'openai' or 'gemini'
  - `model`: Specific model name (e.g., 'dall-e-3')
  - `prompt`: User's text prompt
  - `input_images`: JSON array of input images
  - `output_images`: JSON array of generated image URLs
  - `status`: 'pending', 'processing', 'completed', 'failed'
  - `created_at`, `completed_at`: Timestamps
  - `credits_spent`: Credits consumed for this job

#### 5. Payment System
- **api_paymenttransaction**: Payment records
  - `id`: Primary key
  - `user_id`: Foreign key to auth_user
  - `gateway`: Payment provider ('khalti', 'esewa', 'stripe', 'razorpay', 'binance')
  - `transaction_id`: Unique transaction identifier
  - `amount`: Payment amount
  - `credits_purchased`: Credits bought
  - `status`: 'pending', 'completed', 'failed', 'cancelled'
  - `created_at`, `completed_at`: Timestamps
  - `gateway_data`: JSON field for provider-specific data

#### 6. Password Reset
- **api_passwordresettoken**: Password reset tokens
  - `id`: Primary key
  - `user_id`: Foreign key to auth_user
  - `token`: UUID token for reset
  - `created_at`, `expires_at`: Timestamps
  - `used`: Boolean flag for token usage

#### 7. Social Authentication (Django Allauth)
- **socialaccount_socialapp**: OAuth applications
- **socialaccount_socialaccount**: Linked social accounts
- **socialaccount_socialtoken**: OAuth tokens
- **account_emailaddress**: Email addresses
- **sites_site**: Django sites framework

## Database Configuration

### PostgreSQL Settings
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rupixai_db',
        'USER': 'rupixai_user',
        'PASSWORD': 'rupixai_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Connection Pooling (Production)
```python
DATABASES['default']['CONN_MAX_AGE'] = 600  # 10 minutes
```

## Indexes and Performance

### Recommended Indexes
```sql
-- User lookups
CREATE INDEX idx_auth_user_username ON auth_user(username);
CREATE INDEX idx_auth_user_email ON auth_user(email);

-- Image jobs by user and status
CREATE INDEX idx_api_imagejob_user_status ON api_imagejob(user_id, status);
CREATE INDEX idx_api_imagejob_created_at ON api_imagejob(created_at);

-- Payment transactions
CREATE INDEX idx_api_payment_user_status ON api_paymenttransaction(user_id, status);
CREATE INDEX idx_api_payment_transaction_id ON api_paymenttransaction(transaction_id);

-- Chat threads
CREATE INDEX idx_api_chatthread_user ON api_chatthread(user_id);
CREATE INDEX idx_api_chatmessages_thread ON api_chatmessages(thread_id);

-- Password reset tokens
CREATE INDEX idx_api_passwordresettoken_token ON api_passwordresettoken(token);
CREATE INDEX idx_api_passwordresettoken_expires ON api_passwordresettoken(expires_at);
```

## Data Migration

### From SQLite to PostgreSQL
1. Export data from SQLite:
   ```bash
   python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > data_backup.json
   ```

2. Create PostgreSQL database and user:
   ```sql
   CREATE DATABASE rupixai_db;
   CREATE USER rupixai_user WITH PASSWORD 'rupixai_password';
   GRANT ALL PRIVILEGES ON DATABASE rupixai_db TO rupixai_user;
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Import data:
   ```bash
   python manage.py loaddata data_backup.json
   ```

## Backup and Recovery

### Database Backup
```bash
# Full backup
pg_dump -h localhost -U rupixai_user rupixai_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Schema only
pg_dump -h localhost -U rupixai_user -s rupixai_db > schema_backup.sql

# Data only
pg_dump -h localhost -U rupixai_user -a rupixai_db > data_backup.sql
```

### Database Restore
```bash
# Restore from backup
psql -h localhost -U rupixai_user rupixai_db < backup_file.sql
```

## Security Considerations

### Database Security
1. **User Permissions**: Limited database user with only necessary privileges
2. **Connection Security**: Use SSL in production
3. **Password Security**: Strong passwords and regular rotation
4. **Access Control**: Restrict database access to application servers only

### Data Protection
1. **Encryption**: Sensitive data encrypted at rest
2. **Backup Encryption**: Encrypted backup storage
3. **Audit Logging**: Track database access and changes
4. **Data Retention**: Implement data retention policies

## Monitoring and Maintenance

### Performance Monitoring
- Query performance analysis
- Connection pool monitoring
- Index usage statistics
- Database size monitoring

### Maintenance Tasks
- Regular VACUUM and ANALYZE
- Index maintenance
- Log file rotation
- Backup verification

## Scaling Considerations

### Read Replicas
- Implement read replicas for read-heavy workloads
- Use connection routing for read/write separation

### Partitioning
- Consider table partitioning for large datasets
- Partition by date for time-series data (image jobs, payments)

### Caching
- Redis for session storage
- Application-level caching for frequently accessed data
- CDN for static assets

## Environment-Specific Configurations

### Development
- SQLite for simplicity
- Minimal logging
- Debug mode enabled

### Staging
- PostgreSQL with limited resources
- Production-like configuration
- Test data

### Production
- PostgreSQL with high availability
- Connection pooling
- Comprehensive logging
- Monitoring and alerting
- Automated backups
