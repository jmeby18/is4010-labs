from numbers import Number


def calculate_average_age(users):
    """Return the average of users' numeric ages, or ``0.0`` if none are valid."""
    ages = [
        user["age"]
        for user in users
        if "age" in user and isinstance(user["age"], Number)
        and not isinstance(user["age"], bool)
    ]
    return sum(ages) / len(ages) if ages else 0.0


def get_active_user_emails(users):
    """Return email values for users that are active and have an email key."""
    return [
        user["email"]
        for user in users
        if user.get("is_active") and "email" in user
    ]