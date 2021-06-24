# Cornershop's Backend Test
Hi There, In this repository I will show you the implementation for the Conrenershop's Backend Test.

# Features
- The admin can create a menu for a specif date
- Send a Slack reminder with today's menu to all employes
- Just the admin can delete/update the menu that has been create
- The admin is the only user to be able to see what the Cornershop employees have requested.
- There are two roles of user Chef and Employer
- The employees are be able to choose their preferred meal (until 11 Am CLT)
- The employer can customizations (e.g no tamatoes in the salad).

# Specifications

- Celery for async task setup
- Slack to notify reminder form employer
- Django to develop the web project


# How work this project?
I have two differents type of user "chef" and "employer" for this I implemented the AbstractUser model and switch the AUTH_USER_MODEL on our settings, I never use the built-in Django User model directly, even if the built-in Django User implementation fulfill al the requirements on our application this is because the built-in Django model have some old design decisions (which are kept that way because of backwards compatibility)

The users have different roles, I implemented  <a href="https://github.com/JorgitoR/Cornershop-s-Backend-Test/blob/main/Menu/decorators.py">decorators</a> for this, eg the employer can't create a menu or see what request your coworkers
