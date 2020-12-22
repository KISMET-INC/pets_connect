# Project Documentation
### Problem:  [ 12/10/2020 ]  
Trouble creating a smooth interface when comments are added inside of modal
### Solution:
- Added a number to the URL route 
- Checked if URL route is not zero implying an active image is available
- Targeted that modal in the dom using the url and loaded even before page load to bypass reload flash
***
### Problem: [ 12/21/20 ]  
Certain images are stretched instead of cropped using CSS styling only because there ratios are so different than the target ratio.
### Solution:
- Researched and found an pip environment library on github 'Django-resized' that crops images before uploading to the database. 
- This solved the stretching problem because all files are resized to the same aspect ratio.


# What I Wish I Had Done Differently
- Mapped out the responsive wireframe design before building the project
  - It proved difficult to make responsive after architeture is already built without responsiveness in mind

# What I've Learned So Far
- I learned the basics of responsive design, my first project where I kept multiple device sizes in mind.
- I learned how to effectively manipulate Bootstrap5 Modals
- I learned how to organize my CSS code and target DOM elements more through hierarchy than through multiple class names
- I learned to modularize my css for items that reoocurr across views.
  ## Problem 
- Because I did more targeting through heirarchy, as the project got more complex and elements began to interfere with each other and wrong elements began to be targeted when CSS files were shared across views
  ## Solution
- I realized the importance of planning the elements first so that overlapping CSS files do not interfere with each other. The targeting chain is extremely important for this. Classes and ID are needed and should be used strategically without being overused.


# TODO

- [x] Add loves to Model
- [x] Change First name to Username and remove Last Name
- [x] Add Files Model and make one to many relationship (to allows for image filtering by user)
- [x] Add File Upload functionality using Pillow Technology Library
- [ ] Optimize Modals
- [ ] Add an automated email to user when someone likes loves or comments their photo
- [ ] Add toggle for receiving emails
- [ ] Data Validation for Comments and Images (Never Empty)
- [ ] Investigate Char counts for strings and set validations accordingly to maintain visual appeal
- [ ] Deploy and maintain on AWS EC2 server
- [ ] Fix visual error in responsive design on landing page
- [ ] Add hover titles to the nav bar


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