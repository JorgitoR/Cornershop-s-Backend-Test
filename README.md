# Cornershop's Backend Test
Hi There, In this repository I will show you the implementation for the Conrenershop's Backend Test.

<a href="https://www.youtube.com/watch?v=UN4rPLz9wQk">You can watch the video HERE!!</a>

# Features
- The admin can create a menu for a specific date
- Send a Slack reminder with today's menu to all employes
- Just the admin can delete/update the menu that has been create
- The admin is the only user to be able to see what the Cornershop employees have requested.
- There are two roles of user Chef and Employee
- The employees are be able to choose their preferred meal (until 11 Am CLT)
- The employee can customizations (e.g no tamatoes in the salad).

# Specifications

- Celery for async task setup
- Slack to notify reminder for employes
- Django to develop the web project


# How work this project?
I have two differents type of user "chef" and "employee" for this I implemented the AbstractUser model and switch the AUTH_USER_MODEL on our settings, I never use the built-in Django User model directly, even if the built-in Django User implementation fulfill all the requirements on our application this is because the built-in Django model have some old design decisions (which are kept that way because of backwards compatibility)

The users have different roles, I implemented  <a href="https://github.com/JorgitoR/Cornershop-s-Backend-Test/blob/main/Menu/decorators.py">decorators</a> for this, eg the employee can't create a menu or see what request your coworkers

# Chef
Just The user with this tag <strong>Chef</strong> can create a menu, update the menu, update the options and see what the Cornershop employees have requested.


# Employee
This user whit this tag <strong>Employee</strong> is be able to choose his preferred meal (until 11 Am CLT) and customizations his order



# Building instructions
- Cloning the repository

Start by cloning this repository to your computer by typing the next instruction in your command lines windor:
git clone https://github.com/JorgitoR/Cornershop-s-Backend-Test.git

- Setting up your Slack enviroment in your file settings.py

```
TOKEN_SLACK = '<your token here>'
```

- Administration Credentiales

So at this point the developmet server has you redirected to an authentication page. This is what Nora would actually see if she were the administrator. To login use the next superuser credentials:

- username: nora
- password: cornershop

As you get it done so you will be in front of the main administrative page for nora just like the next image


<img src="https://i.ibb.co/8Kk55v8/image-4-1.png">
<img src="https://i.ibb.co/4Nxt6w9/image-1.png">
<img src="https://i.ibb.co/9WGnthD/image-2-1.png">
<img src="https://i.ibb.co/QYR61KQ/image-3-1.png">


At this point if you want to interact with the page as an employee (Instead of Nora), so you can use the next common users (employee) to request today's menu or something by entering to the generated link in the Slack reminder:

- username: jorgito
- password: cornershop

<img src="https://i.ibb.co/Kzj3YdZ/image-2.png">
<img src="https://i.ibb.co/JHYpQsD/image-1-1.png">






