# SecureBank: Modern Banking System Simulation

SecureBank is a comprehensive online banking simulation built with Django, featuring advanced security measures and a modern Tailwind CSS interface. This application simulates a real banking environment with user authentication, account management, KYC verification, fund transfers, and card management capabilities.

![SecureBank Dashboard](static/img/dashboard-preview.png)

## Features

- **Secure User Authentication**
  - Email verification
  - PIN-based security
  - Session management with automatic timeout
  - Protection against brute force attacks

- **Account Management**
  - Account creation and viewing
  - Balance tracking
  - PIN changing
  - Transaction history

- **Know Your Customer (KYC)**
  - Document uploading
  - Identity verification process
  - Admin verification interface

- **Transactions**
  - Internal transfers between accounts
  - Transaction history with filtering
  - Secure transaction validation

- **Virtual Card Management**
  - Create virtual debit and credit cards
  - Fund cards from main account
  - Withdraw from cards to account
  - Card status management (active/inactive)

- **Admin Dashboard**
  - User management
  - KYC approval workflow
  - System monitoring
  - Administrative controls

- **Modern UI**
  - Responsive design with Tailwind CSS
  - Intuitive navigation
  - Mobile-friendly interface
  - Professional green color scheme

## Technical Details

- **Framework**: Django 5.2
- **Database**: PostgreSQL
- **Frontend**: Tailwind CSS, HTML5, JavaScript
- **Security Features**:
  - CSRF protection
  - XSS prevention
  - SQL injection protection
  - Password hashing with Django's auth system
  - Data validation and sanitization
  - Session security

## Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/securebank.git
   cd securebank
   ```

2. Set up virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with the following variables:
   ```
   DJANGO_DEBUG=True
   DJANGO_SECRET_KEY=your-secret-key
   DATABASE_URL=postgres://user:password@localhost:5432/securebank
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. Access the application at http://localhost:8000

## Production Deployment

For production deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## Architecture

The application follows a modular architecture with the following key components:

- **users**: User authentication and profile management
- **accounts**: Banking account management
- **transactions**: Fund transfer and transaction history
- **cards**: Virtual card creation and management
- **kyc**: Know Your Customer document management
- **dashboard**: User and admin dashboards

## Security Considerations

This application implements multiple layers of security:

1. **Authentication Security**:
   - Password hashing
   - Email verification
   - PIN for sensitive operations
   - Multi-factor authentication ready

2. **Data Security**:
   - Input validation
   - SQL injection prevention
   - XSS protection
   - CSRF protection

3. **Session Security**:
   - Automatic session timeout
   - Secure cookie settings
   - HTTPS enforcement

4. **Infrastructure Security**:
   - Database connection pooling
   - Rate limiting
   - Environment variable management for secrets

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This is a simulation for educational purposes only. It is not intended for processing real financial transactions.