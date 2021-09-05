# Foodies App
A web project using HTML, CSS, JS, Bootstrap, Python, Flask Framework + MongoDB

## Strategy

### About:
- The Foodies App is an online cookbook where users can create an account and share their favourite recipes with other users.

### Wireframes

## Architecture details & Functional Specification:

### Navbar and Home Page:
- A Navbar with a burger style menu, a logo and a the following pages displayed for unregistered users: Home, Login, Register.
- The Home page will display all recipes in a blog style.
- Desktop:

	<img src="static\img\wireframes\desktop\homePage001.JPG" style="height: 500px; width:1000px;"/>
	
- Mobile:

	<img src="static\img\wireframes\mobile\mobileHomePage001.JPG" style="height: 500px; width:1000px;"/>
	
### Searching for a recipe:
- When the user enters a keyword and presses enter then a list of recipes with the searched term will be displayed.
- If there are no results then the page will display a flashing message indicating that No results were found.
- Desktop:

	<img src="static\img\wireframes\desktop\noResults.JPG" style="height: 500px; width:1000px;"/>
- Mobile:

	<img src="static\img\wireframes\mobile\mobileNoResults.JPG" style="height: 500px; width:1000px;"/>

### Individual recipe page:
- This page will display the full recipe with an image, Title, preparation time and recipe description.
- Desktop:

	<img src="static\img\wireframes\desktop\individualRecipe.JPG" style="height: 500px; width:1000px;"/>
- Mobile:

	<img src="static\img\wireframes\mobile\mobileIndividualRecipe.JPG" style="height: 500px; width:1000px;"/>


### Login page:
- Desktop:

	<img src="static\img\wireframes\desktop\loginPage001.JPG" style="height: 500px; width:1000px;"/>
- Mobile:

	<img src="static\img\wireframes\mobile\mobileLoginPage001.JPG" style="height: 500px; width:1000px;"/>

### Logout page:

- Desktop:

	<img src="static\img\wireframes\desktop\logout001.JPG" style="height: 500px; width:1000px;"/>
- Mobile:

	<img src="static\img\wireframes\mobile\mobileLogout001.JPG" style="height: 500px; width:1000px;"/>

### Register page:
- Desktop:

	<img src="static\img\wireframes\desktop\registerPage001.JPG" style="height: 500px; width:1000px;"/>
- Mobile:

	<img src="static\img\wireframes\mobile\mobileRegisterPage001.JPG" style="height: 500px; width:1000px;"/>

### Profile page:
- Desktop:

	<img src="static\img\wireframes\desktop\profilePage001.JPG" style="height: 500px; width:1000px;"/>

- Mobile:

	<img src="static\img\wireframes\mobile\mobileProfilePage001.JPG" style="height: 500px; width:1000px;"/>

	<img src="static\img\wireframes\mobile\mobileProfilePage002.JPG" style="height: 500px; width:1000px;"/>

### Main Pages/HTML:
Pages are organized as follows:
- Home: templates\home.html
- Login: templates\login.html
- Register: templates\register.html
- Logout: templates\logout.html
- Add Post: templates\add_post.html
- Update Post: templates\update_post.html
- User Profile: templates\profile.html
- Post: templates\post.html
- Base: templates\base.html

The core html elements are injected through different functions via the .py files.

### Styles/CSS:
Styles are organized under the "static\css\" directory:
- style.css: contains all styles

### Python:
Py Files are organized under the core directory::
- app.py: runs the app
- auth.py: contains the views for Login, Logout and Register pages
- mongo.py: contains all mongo db related functions
- views.py: contains the views for

### MongoDB structure

#### Database name: m3_db

#### Collections:
- users:
	- _id
	- email
	- username
	- password1
	- password2

- posts:
	- _id
	- post_title
	- post_description
	- user_id
	- image_url
	- prep_time

## Scope
### User Stories:

- As a user I want to:
  1. be able to navigate through the website content with fluidity
  2. be able to register and create an account
  3. be able to search for recipes by using a keyword
  
- As a registered user I want to:
  1. be able to login using my credentials
  2. be able to create my own recipes
  3. be able to update my own recipes
  4. be able to delete my own recipes

### Design Choices:

- I wanted to present a neat, minimalist approach in this page.

- The website should be fully responsive and follow a "mobile first" approach.

- The colors palette include the following colors:
    - primary color: #00ac96;
	- secondary color: #34495e;
	- light color: #fff;
    - red color for errors: #ee5253 
    - green color for links and happy interactions: #1abc9c
    - orange color for warnings: #e58e26

- Fonts used: Google Fonts - Raleway family


## Testing

- All existing features have been tested on the following: Android, iPhone, iPad, iPad Pro and PC.
- The following Test Plan was executed and all scenarios passed:

#### Pages and Links
Scenario | Test Result | Comments
:-----|:-----|:-----
Verify that the User can navigate to the Home Page.|Passed|N/A
Verify that the User can navigate to the Login Page.|Passed|N/A
Verify that the User can navigate to the Register Page.|Passed|N/A
Verify that the User can navigate to the Profile Page.|Passed|N/A
Verify that the User can navigate to the New Post Page.|Passed|N/A
Verify that when clicking the Foodie logo the user will be redirected to the Home Page.|Passed|N/A

#### Search bar
Scenario | Test Result | Comments
:-----|:-----|:-----
Using the search bar, enter a keyword, ie: "chicken" and verify that the page will display search results related to our search.|Passed|N/A
Using the search bar, enter a invalid keyword that will trigger no results, ie: asd!@#!@#252 and verify that the page will display a flashing error message.|Passed|N/A

#### Profile view
Scenario | Test Result | Comments
:-----|:-----|:-----
Verify that if the API doesn't return an image then the default image is displayed instead.|Passed|N/A

#### Creating a new recipe
Scenario | Test Result | Comments
:-----|:-----|:-----
Verify that the user can create a new recipe|Passed|N/A
Verify that the following fields will be present: Title, description, preparation time, image url.|Passed|N/A
Verify that all fields are mandatory|Passed|N/A

#### Updating a new recipe
Scenario | Test Result | Comments
:-----|:-----|:-----
Verify that the user can update a recipe|Passed|N/A
Verify that an updated recipe is displayed with all changes in the Profile page|Passed|N/A
Verify that an updated recipe is displayed with all changes in the Home page|Passed|N/A

#### Deleting a recipe
Scenario | Test Result | Comments
:-----|:-----|:-----
Verify that the user can delete a recipe|Passed|N/A
Verify that a deleted recipe is not displayed in the Profile page|Passed|N/A
Verify that a deleted recipe is not displayed in the Home page|Passed|N/A


## Deployment
### App deployment to Heroku

- Create a requirements.txt file using the terminal command pip freeze > requirements.txt
- Create a Procfile with the terminal command echo web: python app.py > Procfile
- git add and git commit the new requirements and Procfile and then git push the project to Github.
- Create a new app on the Heroku website by clicking the "New" button in the dashboard. Give it a name and set the region to Europe.
- From the Heroku dashboard of your newly created application, click on "Deploy" > "Deployment method" and select Github.
- Confirm the linking of the Heroku app to the correct Github repository.
- In the Heroku dashboard for the application, click on "Settings" > "Reveal Config Vars".
- Set the following config vars and save all changes:
KEY | VALUE
:-----|:-----
IP|0.0.0.0
MONGO_DBNAME|<your mongo db name here>
MONGO_URI|<your mongo db URI here>
PORT|5000
SECRET_KEY|<your secret key here>
COLLECTION_POSTS|posts
COLLECTION_USERS|users

- The website should be live and a url will be provided to access it.
- https://foodie-ci-m3.herokuapp.com/

### Local Deployment using Git

Steps on Github:

- Go to https://github.com/zippote/Milestone3_Foodie
- Click Code
- Select HTTPS and copy the following url https://github.com/zippote/Milestone3_Foodie.git

Steps on your local:

- Create a destination folder in your local >> ie: myFolderExample in the C drive
- Open the cmd and move to that folder >> cd C:\myFolderExample
- Type the following command: git clone https://github.com/zippote/Milestone3_Foodie.git
- Hit enter and wait until the process is completed
- Open the project using your favourite IDE

## Credits
- Media
  - Images were taken from Unplash.com and are royalty free images.
- Recipes content was taken form BBC recipes
  - https://www.bbcgoodfood.com/recipes
