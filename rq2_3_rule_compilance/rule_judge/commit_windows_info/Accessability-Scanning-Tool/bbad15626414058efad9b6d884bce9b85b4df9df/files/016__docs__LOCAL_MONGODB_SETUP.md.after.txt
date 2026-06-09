# Local MongoDB Development Setup

This document provides comprehensive instructions for setting up and using a local MongoDB instance for development.

## Overview

The project includes a complete local MongoDB development environment using Docker Compose. This allows you to develop and test with a full MongoDB stack without needing a cloud instance.

## Prerequisites

- **Docker**: Version 20.10+ 
- **Docker Compose**: Version 2.0+
- **Node.js**: Version 18+
- **npm**: Version 8+

## Quick Start

### 1. Automatic Setup (Recommended)

```bash
# Generate secure secrets for local development
npm run secrets:generate

# Validate environment configuration (optional but recommended)
npm run validate:env

# Start complete development environment
npm run dev:full
```

This command will:
- Generate secure secrets for MongoDB and application keys
- Validate environment configuration for correctness
- Check for Docker and Docker Compose
- Start all MongoDB services
- Wait for services to be ready
- Auto-populate environment configuration
- Start the development server
- Open the web interface

### 2. Manual Setup

```bash
# Start MongoDB services
npm run mongodb:start

# Start development server
npm run dev
```

## Local MongoDB Services

When running locally, the following services are available:

| Service | URL | Port | Description |
|---------|-----|------|-------------|
| **MongoDB** | `localhost:27017` | 27017 | Main database |
| **MongoDB Express** | `http://localhost:8081` | 8081 | Database management UI |
| **Application** | `http://localhost:3000` | 3000 | Web interface |

## Management Commands

### Start Services
```bash
npm run mongodb:start
```

### Stop Services
```bash
npm run mongodb:stop
```

### Check Status
```bash
npm run mongodb:status
```

### View Logs
```bash
npm run mongodb:logs
```

### Reset Database (Delete All Data)
```bash
npm run mongodb:reset
```

### Development with MongoDB
```bash
# Start complete development environment (MongoDB + app)
npm run dev:full

# Start only MongoDB services
npm run mongodb:start

# Start only development server (requires DB to be running)
npm run dev:app-only
```

## Environment Configuration

The application uses the following environment variables for MongoDB:

```env
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/accessibility-testing
MONGODB_DB_NAME=accessibility-testing

# Application Configuration
NODE_ENV=development
PORT=3000
```

## Database Schema

The MongoDB database contains the following collections:

- **reports**: Stores accessibility test reports and results
- **scans**: Stores scan metadata and progress information
- **configurations**: Stores application configuration settings

## Database Architecture

This project uses MongoDB as the primary database for improved performance and flexibility. The architecture includes:

- **Database**: MongoDB with document-based storage
- **API**: Native MongoDB driver for direct database access
- **Authentication**: Custom authentication system (if needed)
- **Storage**: File system storage for reports and assets
- **Real-time**: Socket.IO for real-time communication

## Troubleshooting

### Common Issues

1. **Port Conflicts**: Ensure ports 27017 and 8081 are available
2. **Docker Issues**: Make sure Docker is running and accessible
3. **Permission Issues**: Check file permissions for data directories
4. **Connection Issues**: Verify MongoDB URI and network connectivity

### Reset Everything

```bash
# Stop all services
npm run mongodb:stop

# Remove all containers and volumes
docker-compose down -v

# Start fresh
npm run mongodb:start
```

## Development Workflow

1. **Start MongoDB**: `npm run mongodb:start`
2. **Start Application**: `npm run dev`
3. **Run Tests**: `npm test`
4. **Access Database**: Open MongoDB Express at http://localhost:8081
5. **Stop Services**: `npm run mongodb:stop`

## Production Considerations

For production deployment:

- Use MongoDB Atlas or a managed MongoDB service
- Configure proper authentication and authorization
- Set up database backups and monitoring
- Use environment-specific configuration
- Implement proper security measures

---

**Note**: This document provides comprehensive MongoDB setup instructions for local development. 