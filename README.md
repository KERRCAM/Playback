## Playback

### Overview
Playback is a desktop app for analysing your Spotify extended streaming history.

### Setup:
You will need a Python installation version 3.9 or later.

You will then need the following dependencies.

#### Custom Tkinter:
```
pip3 install customtkinter
```

#### numpy:
```
pip3 install numpy
```

#### MySQL connector:
```
pip3 install mysql-connector-python
```

#### matplot:
```
pip3 install matplotlib
```

#### Database:
You will need to download a MySQL server from this link: https://www.oracle.com/mysql/technologies/mysql-enterprise-edition-downloads.html.

After installation, run the SQL commands from the databaseInitialisation.sql file on your local server to set up the database.

### How to use:
When you start the app, it will display the login page. 
![LoginMenu](https://github.com/user-attachments/assets/24f18261-d590-458c-8cee-61f1917d2254)

If you don’t have an account yet, click the Sign Up button to go to the registration page.
![LoginPointingSignUp](https://github.com/user-attachments/assets/bbb16fc4-50e1-415e-b971-762783fe8f14)

Enter your details in the sign-up form.
![signUpMenu](https://github.com/user-attachments/assets/c7387305-b2f4-45c0-8bf1-d133be5f3901)

![signUpMenuFilled](https://github.com/user-attachments/assets/bfaf78be-6849-4525-9cd5-1cbe3fb81833)

If your username and password meet the requirements, you’ll see a confirmation message. If they don’t, you’ll be notified as well.
![signUpAlert](https://github.com/user-attachments/assets/18a3f818-eeef-4c88-b377-81217fc954f4)

Once signed up, you’ll return to the login page. 
![LoginMenuFilled](https://github.com/user-attachments/assets/065333ca-b063-4724-8331-8525271352c6)

Enter your credentials and click the red button to log in. If the details are correct, you’ll be redirected to the upload page.
![loginPointingUpload](https://github.com/user-attachments/assets/b36c2d8e-ffdf-485c-937a-d3074c873864)

There, you’ll see two buttons: one for selecting a ZIP file (marked in red) and another for extracting it (marked in green).
![UploadPointing](https://github.com/user-attachments/assets/c7940171-05c6-46db-9bca-487d050b4509)

After extraction, you’ll receive a confirmation message.
![ExtractAlert](https://github.com/user-attachments/assets/10330752-0764-41f1-a99c-0d4203ffb5c5)

Finally, you can view your listening statistics on the main menu. The data can be sorted by Song, Album, Artist, Streaming Time, Most Listened, and other categories.
<img width="1506" alt="Screenshot 2025-06-05 at 15 21 09" src="https://github.com/user-attachments/assets/62ea87cd-0859-4c49-93c8-1b7fd9a699ef" />


