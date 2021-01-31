# Import module models (i.e. User)
from my_app.models import *


def make_superadmin(email):
    user_to_update = User.query.filter_by(email=email).first()
    if user_to_update:
        is_admin_field = user_to_update.is_admin
        if is_admin_field:
            print(f"{email} est déjà à 1")
            return False
        else:
            user_to_update.is_admin = 1
            db.session.commit()
            print(f"{email} a été modifié")
            db.session.commit()
            return True