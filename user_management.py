import argparse
import sys
from app import create_app, db
from app.models.user import User
from app.models.invite import InviteToken
from flask import url_for

def get_app_context():
    app = create_app()
    return app.app_context()

def create_invitation():
    with get_app_context():
        # We need a request context for url_for with _external=True
        # But for a CLI, we can just print the token or a relative URL if domain isn't known.
        # However, the user asked for a link. I'll mock a base URL if needed or just use current_app config.
        new_invite = InviteToken(creator_id=1) # Default to first user or system
        # If no users exist yet, this might fail. Let's find first admin.
        admin = User.query.filter_by(is_admin=True).first()
        if admin:
            new_invite.creator_id = admin.id
        else:
            # Fallback if no admin exists
            user = User.query.first()
            if user:
                new_invite.creator_id = user.id
            else:
                print("Error: No users exist to 'create' an invitation. Create an admin first.")
                return

        db.session.add(new_invite)
        db.session.commit()
        
        # Since we are in CLI, url_for might not have server_name. 
        # I'll just provide the token and the path.
        print(f"Invitation Token Created: {new_invite.token}")
        print(f"Registration Link: http://localhost:5000/register?invite={new_invite.token}")

def remove_user(email):
    with get_app_context():
        user = User.query.filter_by(email=email).first()
        if not user:
            print(f"Error: User with email '{email}' not found.")
            return
        
        db.session.delete(user)
        db.session.commit()
        print(f"Success: User '{email}' has been removed.")

def create_admin(display_name, email, password):
    with get_app_context():
        existing = User.query.filter_by(email=email).first()
        if existing:
            print(f"Error: User with email '{email}' already exists.")
            return
        
        user = User(display_name=display_name, email=email, is_admin=True, is_approved=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"Success: Admin user '{display_name}' ({email}) created.")

def promote_admin(email):
    with get_app_context():
        user = User.query.filter_by(email=email).first()
        if not user:
            print(f"Error: User with email '{email}' not found.")
            return
        user.is_admin = True
        user.is_approved = True
        db.session.commit()
        print(f"Success: User '{email}' is now an admin.")

def revoke_admin(email):
    with get_app_context():
        user = User.query.filter_by(email=email).first()
        if not user:
            print(f"Error: User with email '{email}' not found.")
            return
        user.is_admin = False
        db.session.commit()
        print(f"Success: Admin privileges revoked for '{email}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vitara User Management CLI")
    parser.add_argument("--newuser", action="store_true", help="Generate an invitation link")
    parser.add_argument("--removeuser", metavar="EMAIL", help="Remove a user by email")
    parser.add_argument("--newadmin", nargs=3, metavar=("NAME", "EMAIL", "PASSWORD"), help="Create a new admin account")
    parser.add_argument("--promote", metavar="EMAIL", help="Promote an existing user to admin")
    parser.add_argument("--revoke", metavar="EMAIL", help="Revoke admin privileges from a user")

    args = parser.parse_args()

    if args.newuser:
        create_invitation()
    elif args.removeuser:
        remove_user(args.removeuser)
    elif args.newadmin:
        create_admin(*args.newadmin)
    elif args.promote:
        promote_admin(args.promote)
    elif args.revoke:
        revoke_admin(args.revoke)
    else:
        parser.print_help()
