Routes that we have access to:
```
/forgotpassword
/index.html
/login
/logout
/profile (requires login)
```
At `/forgotpassword` you could see this:
![](escalator-cred.png)
near the bottom of `Inspect` (credentials might be different for each user)

You can connect to the mysql database using the MySQL workbence (DBS!). From there, we find the login information in the `users` table. The passwords are hashed so we will have to find some way to deal with that before getting our login. (Also, I'm not sure if this is still part of the first task or I just completely skipped it)