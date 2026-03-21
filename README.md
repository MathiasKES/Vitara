# Vitara

Vitara is a minimal, privacy-first web application for journaling and fitness tracking. It features a social feed, progressive photo tracking, and a robust fitness logger with both strength and cardio support.

## Features

- **Journal**: Rich-text journaling with mood tracking (Quill.js integration).
- **Social Feed**: Share progress photos with a beautiful, minimal interface.
- **Fitness Tracker**:
    - Log Strength workouts (sets, reps, weight).
    - Log Cardio (Running, Swimming, Cycling, Walking) with distance and pace tracking.
    - Automatic unit conversion (Metric/Imperial) based on user preference.
    - Personal Record (PR) tracking.
    - Visual progress stats with Chart.js.
- **Privacy & Admin**:
    - Private sign-up flow with Admin approval.
    - Secure invitation system for family and friends.
    - Dark/Light mode support.

## Setup & Installation

### Prerequisites

- Python 3.11 or higher
- Conda (recommended) or `venv`

### Initial Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Vitara
   ```

2. **Environment Setup**:
   Using Conda:
   ```bash
   conda env create -f environment.yml
   conda activate Vitara
   ```
   Or using pip:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory:
   ```bash
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///app.db
   ```

4. **Initialize Database**:
   ```bash
   flask db upgrade
   ```

5. **Run the Application**:
   ```bash
   python run.py
   ```
   The app will be available at `http://localhost:5000`.

## Administrative Tasks

### User Management CLI

You can manage users directly from the terminal using `user_management.py`.

- **Create a New Admin**:
  ```bash
  python user_management.py --newadmin "Admin Name" admin@example.com "securepassword"
  ```

- **Generate an Invitation Link** (for auto-approved signups):
  ```bash
  python user_management.py --newuser
  ```

- **Remove a User**:
  ```bash
  python user_management.py --removeuser user@example.com
  ```

- **Promote an Existing User to Admin**:
  ```bash
  python user_management.py --promote user@example.com
  ```

- **Revoke Admin Access**:
  ```bash
  python user_management.py --revoke user@example.com
  ```

## Invitations

Users can generate one-time invitation links from their **Profile Settings** page. These links allow invited friends to sign up and receive **automatic approval**, bypassing the standard admin gatekeeper.

## License

Personal project by Mathias.
