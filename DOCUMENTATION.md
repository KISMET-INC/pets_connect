# Project Documentation
### Problem:  MODAL 'CHAT' [ 12/10/2020 ]  
Trouble creating a smooth interface when comments are added inside of modal
### Solution:
- Added a number to the URL route 
- Checked if URL route is not zero implying an active image is available
- Targeted that modal in the dom using the url and loaded even before page load to bypass reload flash
***
### Problem: STRETCHING [ 12/21/20 ]  
Certain images are stretched instead of cropped using CSS styling only because there ratios are so different than the target ratio.
### Solution:
- Researched and found an pip environment library on github 'Django-resized' that crops images before uploading to the database. 
- This solved the stretching problem because all files are resized to the same aspect ratio.
***
### Problem: RESIZE [12/22/20]
Even when resized certain images are still stretched when changing the window size. It made me wonder if it a problem that lies within different types of jpg files.
### Solution:
-  In models.py I changed the force_format to PNG in the Image class and even though files still have the jpg extenstion they no longer stretch
***
### Problem: COMPLEXITY AND OVERLAP [12/31/20]
As project gets more complex and more data snippets begin to overlap. the include becomes a problem when using the snippet on different pages from where it gets different object paths to the same object.
### Solution
Used the With function on DJango template engine to set variables such as which user it represents before passing in if needed.
### Problem: ROUTING [12/31/20]
As project gets more complex and more data snippets begin to overlap. the include becomes a problem when using the snippet on different pages from where it gets different object paths to the same object.
### Solution
Used the With function on DJango template engine to set variables such as which user it represents before passing in if needed.

### Problem: WINDOW POSITION [1/1/2021]
Because of page rerendering, the area behind the modal always refreshes to the top
### Solution
Used the history.pushstate.url to set the url needed to load the modal
used window.reload to save the scroll location and reload in the same place

### Problem: COMPLEXITY AND OVERLAP [1/1/21]
As features were added that targeted reusable models, and because this application focuses around rerouting and page rendering I need a way to keep track of what page called the component. 
### Solution 
For every view I sent a 'location' variable through the context and made sure that all routes followed the same structure. Therefore 'location' could easily be added to the rout to get the user back where they came from after running a process. 

### Problem: FADE [1/1/21]
Because the page refreshes to load the modal with the correct image informatin i needed a way to tell the application when to have the modal fade in and when to have it pop on (in order to simulate a static chat within the modal)
### Solution
I sent a variable through the application that tells the application wheter it needs to load the modal with a fade or not. When returning from the the process of adding a comment it adds the no fade trigger into the url so that when the window opens the modal knows it is a nofade. When the user clicks off of the modal, the fade is turned back on for the next selection.
### Problem BULLETIN CHAT [1/1/21]
Once again the reloading breaking the flow of the UI when posting and deleting omments from the bulletin board
### Solution
Added the comments through an Iframe so that when a comment is added or removed it doesnt reload the person back to the top. The user stays put to add or delete more comments where they are. NOTE: Not the most memory efficient solution as it has to load and Iframe and the IFRAMEs css for every post on the bulletin board. I am looking into ways to solve this problem in a more efficient manner.
***
# What I Wish I Had Done Differently
- Mapped out the responsive wireframe design before building the project
- It proved difficult to make responsive after architeture is already built without responsiveness in mind
- Build the program in REACT. THere is alot of routing in my app that would have been better recieved as an SPA with no loading flashes

# What I've Learned So Far
- I learned the basics of responsive design, my first project where I kept multiple device sizes in mind.
- I learned how to effectively manipulate Bootstrap5 Modals
- I learned how to organize my CSS code and target DOM elements more through hierarchy than through multiple class names
- I learned to modularize my css for items that reoocurr across views.
- I learned the 'include' tag in Django Template which alowed me to modularize code snippets
- Although I didnt end up needing it, I learned how to make custom filter tags for template database queries using templatetags folder
  ## Problem 
- Because I did more targeting through heirarchy, as the project got more complex and elements began to interfere with each other and wrong elements began to be targeted when CSS files were shared across views. 
  ## Solution
- I realized the importance of planning the elements first so that overlapping CSS files do not interfere with each other. The targeting chain is extremely important for this. Classes and ID are needed and should be used strategically without being overused.


# TODO
## Features
- [x] Add loves to Model
- [x] Add Files Model and make one to many relationship (to allows for image filtering by user)
- [x] Add File Upload functionality using Pillow Technology Library
- [ ] Add an automated email to user when someone likes loves or comments their photo
- [ ] Create Pets Connect email for automated emails
- [ ] Add toggle for receiving emails
- [X] Deploy and maintain on AWS EC2 server
- [x] Add hover titles to the nav bar
- [x] When page reloads user is still in same location in the feed
- [ ] Integrate EDIT POST
- [ ] Integrate Share POST
- [x] Add UNFOLLOW
- [ ] Add cancel button to Edit user
- [ ] Add ability to change password
- [ ] only load X amount of posts, add more when user reaches  bottom of page
## Bug Fixes
- [X] Fix visual error in responsive design on landing page
- [ ] Work on Debug Nginx Media problem
- [x] Fix modal dialog size in dashboard
- [x] Signed in username not show up on posts
- [ ] Add favicon
- [x] Click out problem | Reload problem
- [x] fade problem
- [x] scroll problem
- [ ] Nav tooltip too long
- [x] Make Edit and Delete on Image look nice
- [x] Fix render routing after interactions
- [ ] reevalute breakpoints responsive design
- [ ] tweek modal visual
- [ ] tweek post visual
- [ ] add UNLOVE
## Efficiency
- [x] Learn how to make modular reusable code snippets
- [x] Optimize Modals, Stats, Nav
- [ ] Refactor
- [ ] Refactor so that it doesnt import CSS files for every post
## Changes
- [x] Change First name to Username and remove Last Name
- [ ] ADD DECENT DATA
- [ ] Make name in post centered by whatever means possible
## Security
- [ ] Data Validation for Comments and Images (Never Empty) 30chars
- [x] Investigate Char counts for strings and set validations accordingly to maintain visual appeal
- [ ] Dont allow routing without signin

# Outside Libraries
### Pillow
Makes the ImageField available to models:
This allows users to upload files directly to the server instead of having to link through a URL. The use of a file uploader adds conveinience to the user experience.

 https://pillow.readthedocs.io/en/stable/

    pip install pillow

### Django-Cleanup
Deletes image file from server if image is removed from database: Keeps the server clear of erroneous files and improves scalability and performance

 https://github.com/un1t/django-cleanup

    pip install django-cleanup


### Django-Resized
Resizes and crops image files before they are uploaded to the server :
Maintains the aesthetics of the application , uniform and easy to follow which facilitiates a pleasent user experience when 

  https://github.com/un1t/django-resized

    pip install django-resized