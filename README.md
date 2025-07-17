# Public Market Management System

A comprehensive Django application for managing public markets (marchés publics) with PostgreSQL database.

## Features

- **Complete CRUD Operations** for all 10 tables:
  - Maître d'ouvrage (Project Owner)
  - Prestataire (Service Provider)
  - Marché (Market/Contract)
  - Service
  - Maintenance
  - Fourniture (Supply)
  - Ordre de service (Service Order)
  - Décompte (Payment breakdown)
  - PV (Official Report)
  - Document

- **PDF Generation** for contracts and reports
- **Advanced Search and Filtering**
- **User Authentication and Authorization**
- **Responsive Bootstrap UI**
- **File Upload Management**
- **Dashboard with Statistics**

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd public-market-management
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup PostgreSQL Database**
```bash
# Create database
createdb public_market_db

# Or using psql
psql -U postgres
CREATE DATABASE public_market_db;
\q
```

5. **Environment Configuration**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

6. **Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Create Superuser**
```bash
python manage.py createsuperuser
```

8. **Load Sample Data (Optional)**
```bash
python manage.py loaddata fixtures/sample_data.json
```

9. **Run Development Server**
```bash
python manage.py runserver
```

## Database Schema

### Core Tables
- **MaitreOuvrage**: Project owners/clients
- **Prestataire**: Service providers/contractors
- **Marche**: Main contracts/markets

### Market Components
- **Service**: Service items within markets
- **Maintenance**: Maintenance items within markets
- **Fourniture**: Supply items within markets

### Management Tables
- **OrdreService**: Service orders
- **Decompte**: Payment breakdowns/invoices
- **PV**: Official reports (Procès-Verbaux)
- **Document**: File storage and management

## Key Features

### PDF Generation
- Contract generation with ReportLab
- Custom templates for different document types
- Automatic formatting and styling

### Search and Filtering
- Advanced search across multiple fields
- Filter by type, status, date ranges
- Pagination for large datasets

### User Interface
- Modern Bootstrap 5 design
- Responsive layout for mobile devices
- French language interface
- Intuitive navigation and forms

### Security
- Django authentication system
- CSRF protection
- File upload validation
- User permission management

## Usage

1. **Access the application** at `http://localhost:8000`
2. **Login** with your superuser credentials
3. **Navigate** through the sidebar menu
4. **Create** new records using the "+" buttons
5. **Generate PDFs** from the market detail pages
6. **Upload documents** through the document management section

## API Endpoints

The application provides a web interface, but you can extend it with Django REST Framework for API access.

## Deployment

### Production Settings
1. Set `DEBUG=False` in settings
2. Configure proper database credentials
3. Set up static file serving
4. Configure email settings for notifications
5. Set up proper logging

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please create an issue in the repository.