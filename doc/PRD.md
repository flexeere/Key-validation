# Product Requirements Document (PRD)
**Project Title**: B2B Company Registration & Validation Portal
**Primary Technology**: Django (Python)
**Document Status**: Draft for Review (Targeted for OpenAI CodeX evaluation)

---

## 1. Executive Summary
The objective of this project is to build a robust and secure web-based portal using the Django framework. The portal allows corporate entities to register their business credentials (such as Company Name, Address, Contact details, and GST information). To ensure the authenticity of the registration, a secure validation process is implemented wherein a unique authentication key is generated, synchronized with a validation URL, and dispatched to the designated contact email. 

## 2. Product Scope
*   **Public Registration Interface**: A user-friendly form for companies to submit their details.
*   **Key Generation & Verification Engine**: Backend microservice/logic for securely creating validation tokens and verifying them.
*   **Email Dispatch System**: Asynchronous email delivery containing the validation payload.
*   **Admin Dashboard**: A secure back-office interface (leveraging Django Admin) for internal staff to monitor, audit, and manually manage corporate registrations.

## 3. User Roles & Permissions
1.  **Unregistered Client**: Has access strictly to the public registration forms.
2.  **Pending Company Profile**: User whose registration is submitted but pending email verification.
3.  **Verified Company Profile**: User whose company has successfully passed the URL/Key validation check.
4.  **System Administrator**: Has superuser privileges to access the Django Admin panel, view all company records, resend verification emails, and revoke access if necessary.

## 4. Functional Requirements

### 4.1. Registration Module
*   **Data Capture**:
    *   `Company Name` (Required, String)
    *   `Company Address` (Required, Text)
    *   `Customer/Contact Name` (Required, String)
    *   `Contact Email` (Required, Valid Email Format, Unique)
    *   `GST Details / Tax ID` (Required, Alphanumeric, Unique)
*   **Validation**: The system must enforce unique constraints on Email and GST details. If a duplicate is detected, a user-friendly error message must be presented.

### 4.2. Token Generation & Sync
*   **Secure Key Creation**: Upon successful validation and database commit of the company details, the system must generate a cryptographically secure token (e.g., `secrets.token_urlsafe` or `UUID4`).
*   **URL Sync**: A fully qualified absolute URL must be constructed concatenating the application's base domain with the token (e.g., `https://[app-domain]/verify/?key=abc123xyz`).
*   **Lifespan**: The key must have a TTL (Time-To-Live). Recommended expiration is 24 to 48 hours for security purposes.

### 4.3. Email Notification
*   The system sends an automated welcome email strictly to the `Contact Email` provided.
*   The email must contain the generated Key and the Validation URL dynamically rendered via Django templates.

### 4.4. Validation & Activation Module
*   The portal must expose a secure GET endpoint/view to handle the URL click.
*   The portal may also expose a form where the user can manually paste the key.
*   **State Transition**: Upon validation, the company's status flag transitions from `Pending` to `Verified`. The specific key is then invalidated/discarded to prevent replay attacks.

### 4.5. Admin Panel (Django Admin)
*   **List Views**: Display lists of companies with quick-glance columns (Name, Email, GST, Status, Created Date).
*   **Filters & Search**: Ability to filter by verification status and search via Company Name or GST number.
*   **Immutability**: Validation keys should be hashed or hidden from standard admins to prevent manual interception, emphasizing security.

## 5. Non-Functional Requirements
*   **Security**: 
    *   Protection against CSRF, XSS, and SQL Injection (handled natively by Django ORM and templates).
    *   Rate limiting on the registration endpoint to prevent bot spam and email abuse.
*   **Performance / Async Tasks**: 
    *   Email sending should not block the HTTP request thread. Implementing Celery with Redis/RabbitMQ, or at minimum Django background tasks, is strongly recommended.
*   **Scalability**: The database schema must be normalized to support future extensions (e.g., adding multiple users/employees to a single Company Profile).

## 6. Proposed Data Architecture (Django Models)

### `Company`
*   `id`: Primary Key (UUID preferred)
*   `name`: CharField
*   `address`: TextField
*   `contact_name`: CharField
*   `email`: EmailField (unique=True)
*   `gst_number`: CharField (unique=True, index=True)
*   `is_verified`: BooleanField (default=False)
*   `created_at`: DateTimeField(auto_now_add=True)
*   `updated_at`: DateTimeField(auto_now=True)

### `ValidationKey`
*   `company`: OneToOneField(Company, on_delete=CASCADE)
*   `token`: CharField(max_length=128, unique=True, db_index=True)
*   `expires_at`: DateTimeField
*   `is_used`: BooleanField (default=False)

## 7. User Flows

1.  **Registration Flow**:
    *   User loads `/register/`.
    *   Submits details -> Django validates -> System creates `Company` + `ValidationKey`.
    *   System kicks off async email task.
    *   User sees confirmation UI: "Check your inbox".
2.  **Activation Flow**:
    *   User clicks magic link in email `/verify/?key=<token>`.
    *   Django View intercepts -> Queries `ValidationKey`.
    *   If token valid & not expired -> Mark `Company` as verified -> Mark token used.
    *   Redirect to Welcome/Login page.

## 8. Development Phases
1.  **Phase 1**: Django Setup, Models creation, and Admin panel configuration.
2.  **Phase 2**: Core Registration Form & validation logic (Views & Templates).
3.  **Phase 3**: Key Generation algorithm and Email integration (SMTP/SendGrid + Async workers).
4.  **Phase 4**: Verification View and state transitions.
5.  **Phase 5**: Unit Testing, Security Hardening (rate limiting), and Documentation.

***

> **Note for CodeX Evaluators**: This PRD emphasizes a decoupling of the company data from the temporary validation keys, prioritizes asynchronous I/O for email delivery, and highlights security best practices inherent to modern Django application design.
