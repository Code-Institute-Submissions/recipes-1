###### Ramanathan Annes 
## Burger Recipes
These website have a recipes of different types of burgers and it's easy to access by the user and it's easy to understand by new user.

### UX
These website for a person who want to try new burgers recipes.They can easily achieve by the instruction I gave on these website for example the timing.
And also I gave best **Ingredients** and the **method of preparation**.Overall my **Target Audience** are amature chefs and young adult.
[Wrieframe](https://www.lucidchart.com/invitations/accept/a82d7d7a-2498-4d61-b1f5-f6fac3c6be33)

#### Quick intro about how these website work
 - If user new to these website they have to register first 
 - if already existing user they can straightly login and access the recipes
 - if anything wrong about recipes user can edit that and they can get the credit

### Features 
### Existing Features
  - Firstly, This website have user login and user registration form. In login form If user enter wrong Password the **Password Incorrect** will be display on bottom of the form.
  - Secondly, If the user liked the recipe or did they actually made that recipe they can show us with like button.
  - Thirdly, If we missed out any magic Ingredients or our method is wrong user can edit that via edit button on top of recipes.
  - Furthermore, If user know any new burgers recipes they can add it via add recipes.
  - Finally, If user want to edit there details or delete their account they can do that in their account page.

### Features Left to Implement
I have a idea to add three more features may be in next update
 - Firstly, viewers count so that acutually help us morely to insight our wesite more that users
 - secondly, Pin the recipe so that recipe will show on our account page 
 - finally, review the recipe by the user

### Technologies Used 
In this section, I  mention all of the languages, frameworks, libraries, and any other tools that I used to construct this project.
  - [Bootstrap](https://getbootstrap.com/docs/4.0/getting-started/introduction/): 
       * I used a **Bootstrap** for design and UX
  - [Flask](http://flask.pocoo.org/docs/1.0/): 
     * The whole project mainly depend on **Flask**.
  - [Materialize css](https://materializecss.com/):
      * I used **materializecss** to design and icons. 
  - [MONGODB](https://mlab.com/):
      * I used **Mongodb** to secure and store my website users details and recipes.

### Testing 
Manual testing to confirm that the recipes was being passed to the page.
   I did some testing for check the register form is working[Test File](https://github.com/Ramanathan03/recipes/blob/master/test_app.py).
##### Different screen sizes:
   I used  **Chrome development tool** to testing my website responsible  in smaller screen and in large screen.
   

### Deployment 
This project was deployed on Heroku 
###### Here is the way to I depolyed to heroku 
 - git remote add heroku 
 - create procfile 
 - ps:scale web=1
 - Push to Heroku --> $ git push heroku master
 
* Procfile will help to declares types -> web
 [Website](https://get-recipes.herokuapp.com/)

##### Config Vars --> IP = 0.0.0.0, PORT = 5000

## Credits
### Media 
The background images used in this site were obtained from [PxHere](https://pxhere.com/)

### Acknowledgements
Code Institute Mentor **Chris Zielinski** 

