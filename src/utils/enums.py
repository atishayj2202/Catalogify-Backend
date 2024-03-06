from enum import Enum


class AuthType(Enum):
    google = "google"
    facebook = "facebook"
    github = "github"
    apple = "apple"
    email = "email"
    phone = "phone"


class PostCategory(Enum):
    electronics = "electronics"
    fashion = "fashion"
    grocery = "grocery"
    medicine = "medicine"
    toys = "toys"
    sports = "sports"
    books = "books"
