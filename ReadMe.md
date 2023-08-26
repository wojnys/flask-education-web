![image](https://github.com/wojnys/flask-education-web/assets/77916807/686f83df-8d10-4ee5-8e55-f23aafc85d94)

# Flask education project 
- This project is about to help students to get new knowledge and new information

# What will be inclueded
1. Setup 
    - User will setup account and chose these options
      - University
      - Field of study
      - Year Born, Gender, Profile picture
2. Quiz Mode
   - User can test his knowledge with a quiz (questions are randomly generated)
3. All questions
   - User can display all questions and learn them by hard
4. Add questions 
   - User can make request and add own question or answer - admin has to approve it 

### NOTE:
importing from file market.__init__ but init is initializing file,
so it is not neccesary to write it before - just type "market" and import data from market.__init__ file

### How to create new DB from command line 
1. python3
2. from market import app, db
3. app.app_context().push()
4. db.create_all()

### How to run project 
1. python3 run.py
