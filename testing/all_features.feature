Team Members: Jay Patel, Asad Noman, Stone Zheng, Prachi Yadav


Feature: List questions/posts

User Story: As a user, I want to be able to view a feed of posts.

Scenario: As a user I want to be able to sign in / register to see the feed

Given I am on the index page
When I click into Sign-In or Register
Then I should be on the registration validation pages (either one)
When I finish verifying my user details and sign in
Then I should be on the "Feed" page
And I should see the feed of posts



Feature: View a question/post

User Story: As a user, I want to be able to view an individual post.

Scenario: As a user I want to be able to navigate from the list of posts (feed) to a single post.

Given I am on the feeds page
When I click on one of the posts from the list
Then I should be on that individual post page
And I should be able to see the subject
And I should be able to see the text of the post
And I should be able to see the author of the post
And I should be able to see the comments made on the post
And I should be able to see the rating count of the post



Feature: Create a question/post

User Story: As a user, I want to be able to create a new post.

Scenario: As a user I want to be able to navigate from the homepage to the new post form

Given I am on the feed page
When I click on the big plus button
Then I should be on the "New Post" page
And I should see the Subject field
And I should see the Text field



Feature: Edit an question/post

User Story: As a user, I want to be able to edit individual posts.

Scenario: As a user, I want to be able to navigate from the feed to the edit a post form

Given I am on the feed page
When I click on a post that I made
Then I should be on the single post page for that post
When I click on the "Edit" button
Then I should be on the "Edit post" page
And I should see the text field



Feature: Reply to a question/post

User Story: As a user, I want to be able to reply to posts.

Scenario: As a user I want to be able to navigate from the feed page to writing a comment on a post. 

Given I am on the ‘feed’ page.
When I go to an individual post page.
Then I should be on the individual post page
When I click on the ‘Comment’ button on the individual post page
Then I should be on the commenting page
And I should see the text box to write your comment



Feature: Delete an question/post

User Story: As a user, I want to be able to delete a post.

Scenario:  As a user I want to be able to navigate from the feed page to an individual post to deleting a post.

Given I am on the ‘feed’ page
When I click on an individual post
Then I should be on the individual post that I clicked on
When I click on the delete button
Then it should delete the post 
And I should be taken back to the ‘feed’ page.


Feature: Register a user

User Story: As a user, I want to be able to register myself as a user.

Scenario:  As a user I want to be able to go on a register page and make a username and password.

Given I am on the ‘user registration’ page
When I click on  the sign up button
I should be able to create a user name
And I should  be able to create a password
And after making these, go back to the home page



Feature: User sign-in

User Story: As a user, I want to be able to sign in to use the app.

Scenario: As a user I want to sign in to my account 

Given I am on the user page
I am given two options to sign in
A username bar and a password bar
After typing in those two features
I should be able to login through the submit feature


Feature: Creating a user profile

User Story: As a user, I want to be able to update my profile

Scenario: 
Given I am signed into my account
I am on the feed page
When I click on the update profile link
I am redirected to an updated form
Where I should be able to type words 
And after clicking submit 
My user profile should be updated


Feature: Updating email and password

User Story: As a user, I want to be able to update my email and password

Scenario: 
Given I am on the feed page after being logged in
When I click update profile link
I am redirected to the update form 
Where I should click the update email & password link
After entering the new passwor/email 
I should be able to submit my new password/email
My password/email should be updated


Feature: Enforcing a regex to a field other than username/email

User Story: As a user, I want to be able to enter between 6-12 characters, and a minimum of 1 special character

Scenario: 
Given that I am registering for my account
When I am on the password field
I will be prompted to verify that my password is between 6-12 characters 
And at least 1 special character and 1 number
If all the conditions are met
Then I would be able to register my account


Feature: Rate (up vote)

User Story: As a user, I want to be able to rate posts.

Scenario: 
Given that I am on a post
I would be able to like a post
Each like being increased by one and decreased by one for each dislike



