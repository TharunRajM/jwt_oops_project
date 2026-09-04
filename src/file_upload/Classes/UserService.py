class UserService:

    def __init__(self, user_database):
        self.user_database = user_database


    def find_user_by_email(self, email):

        for user in self.user_database:

            if user.email == email:
                return user

        return None


    def find_user_by_id(self, user_id):

        for user in self.user_database:

            if user.id == user_id:
                return user

        return None


    def add_user(self, user):

        self.user_database.append(user)

        return user