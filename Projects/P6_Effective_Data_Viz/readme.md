# P6: Data Visualization using D3
Student: Andy Miller 
Udacity's [Data Analyst Nanodegree](https://www.udacity.com/course/nd002)

## Background
This project represented a substantial departure from what I am used to.  I currently work for a Fortune 500 company, where we use a variety of tools to prepare and visualization data, primarily being Alteryx and Tableau.  I have used Tableau extensively and therefore am very accustomed to the drag and drop, yet powerful, interface.  Learning D3 was a substantial departure from what I am used to or comfortable with, however, I was EXTREMLY excited about this course for several reasons:
 
 1. D3 - Learning a new tool to augment my current visualization skills is a fruitful endeavor, in my eyes.  The D3 language is very powerful and far less abstract than a tool such as Tableau.  While Tableau allows many types of visualizations, it does abstract some of the other elements away from the user.  With D3, a user has a totally blank canvas, allowing him / her to define their exact layout and interaction.  For instance, Tableau does not (truely) support much in terms of transformations.  However, your abilities are endless with D3 and a web browser.  Further, I should note that I had no experience with CSS or HTML, but after working through the courses and searching on my own, I was equiped enough to be dangerous.
 2. The Udacity course exceeded my expectations in terms of digging into the world of visualization.  I enjoyed the discussion on understanding visualization principles, such as: choosing the appropriate chart, augmenting charts with the right encodings, telling a story with data, and understanding pre-attentive attributes and Gestalt Principles of Perception.
 3. The cameos.  I was impressed to see Cole Nussbaumer Knaflic and other references and learnings from others, such as: Alberto Cairo, Stephen Few and Edward Tufte.  Not to mention other visualization mentions from people like Andy Kriebel (an avid Tableau user and blogger).

Overall this broadened and deepened my knowledge of the world of visualization, which is much more than just a chart.  While the greatest learning from this lesson and project was D3, I really enjoyed the focus on telling a story with your data and ensuring message comprehension by using the right charts, encodings and other elements (such as overall presentation, transformations / motion). 

Using these learnings, I dove into D3 and the Titanic dataset to create a story that is simple, yet uniquely tells a story.  

### Summary
My data visualization utilized the Titanic dataset, which lists and describes the attributes of all Titanic passengers, including information such as age of the passenger, cabin class, number of siblings onboard, and the fare paid to take the journey.  My visualization focuses on two key measures, age of the passenger and the fare that person paid to take the journey, which I wanted to investigate further to see the correlation and impact on survival.  Because I was focused on the correlation of two measures / features, I elected to utilize a scatter plot.  It should be noted that I purposefully excluded those passengers where their age was unknown.
## Design 
_(Note: Feedback discussed in "Feedback" Section)_

As mentioned in my summary, I elected to use a scatter plot, which does an excellent job of visualizing the correlation of two variables.  There were two key encodings on the data that I made, beyond position which is inherent to the scatterplot:

 1. Color of Circle - This encoding, from the survived feature, was the fill of every circle presented within the svg scatterplot.  I chose blue to indicate 'survived' and red to indicate 'died'.  Originally I was going to choose the high contrast colors of red-green, but choose blue as red-green is difficult for color blind persons (8% of males and .5% of females).
 2. Size of Circle - This encoding, from the sibsp feature (number of siblings / spouses onboard), was scaled for the min and max values of the dataset (0 and 8) between 3 and 8 pixels (zScale).  I choose this variable as it was complementary to message comprehension in the scatterplot, meaning that a user could review the correlation (the main purpose) between the age and fare features, while also getting an understanding for that passenger (e.g., did they only have to worry about themselves or did they have a spouse or sibling onboard that either slowed them down or increased the chance for survival as they may have had help surviving). 

Further, I cycled through my visualization for different cohorts of passengers, specifically: Female Only, Male Only, Children Only (defined as <= 13), and finally All Passengers.  This enabled the users to not only see the differences in the makeup of passengers (range and count), but also the individual survival of these cohorts.  During this cycling, I used D3's transition() abilities of entering and exiting marks to make it more apparent to the users what was changing (instead of an abrupt  disappearance or entrance of circles).  During these cycles of cohorts, the axes dynamically adjust (and are minimalist styled - as I am not a support of chart junk).

Finally, I further enabled tooltips to enable the audience to do their own inspection of the passengers.  I included the information in the axes and encodings, as well as some addition information like cabin class. 

## Feedback
My process for developing this visualization was as follows: 1) sketched out my scatterplot idea, 2) circulated the visualization to the three people (my wife - no knowledge, my colleague (D3 experience), and my friend (works in Tableau quite a bit and understands design principles).  They had excellent findings that helped me refine my visualization.  This feedback and refinement is presented below (and can be reviewed by investigating index1.html (incorporating 1st feedback), index2.html (incorporating 1st feedback), index3.html (incorporating 1st feedback), and finally index_final.html includes my cleanup and revisions of my own.: 

 1. My Wife - "I noticed very clearly that people that paid more and were younger, as well as older (and didnt pay as much) survived more often.  This made sense as I would expect that passengers that paid more didnt have to travel far to the deck and lifeboats and were likely first in.  I am curious how the siblings play in this."  With this feedback, I realized that it would be nice to encode the circle size with the number of siblings. 
 2. My Colleague - "(mentioned similar takeaway as my wife)... I am more curious about investigating the circles.  Here you dont provide any way to find out who was the passenger or get an accurate value for the age and fare, without using a rule on the computer screen.  I would consider adding a tooltip."  That is exactly what I did, as adding tooltips was a great idea an allows the user to investigate the data on their own, as well as, get additional information about the passenger that wasnt included in either of the axes (age and fare). 
 3. My Friend - "I notice what you are going for here and you make it very apparent that people that paid more, survived more often.  One thing that I would mention is that you dont allow me to break it down by things such as sex, or what if I wanted to see how children fared?  Overall, I think I understand your story, but with this additional information, I would understand your story better."  This was the feedback that allowed me to enable some of D3's great transformation abilities.  Therefore, I took his advice and added in an interval that cycled through: "Female Only", "Male Only", "Children Only" (13 and younger), and finally settling on all the passengers. 
 4. Myself - Finally, I took a good look at my visualization after incorporating this feedback and set out to make some changes.  I cleaned up my code, added some comments where I thought necessary, and labeled and adjusted the aesthetics of the axes.  But I wanted more.  I wanted the user to be able to not only see this interval cycling through the cohorts, but I wanted them to be able to rewind and focus on one.  Therefore, I add some buttons that allowed the user to select this AFTER the cohort cycling was done.  You will see this in the upper-right hand corner.  

In general, with all that feedback, from three different perspectives, I had a visualization that allowed the user to see the data change in front of them, but also investigate the data on their own.  I discovered the story of the data, and that was the following key findings: 

 - People that paid more had a better chance of survival.
 - People that were 50 years or older had a better chance.  I suspect that they were helped to lifeboats and others gave up their chance at a lifeboat to allow them to board and survive.
 - Most children survived.  Likely for similar reasons as I mentioned for people 50 years and older.

I found a story in this data through visualization.

## Resources

 - Enter, Update, Exit - https://medium.com/@c_behrens/enter-update-exit-6cafc6014c36#.j6mcoko3a
 - Update Pattern Understanding: http://bl.ocks.org/mbostock/3808218
 - Arrays Help: https://github.com/d3/d3/wiki/Arrays
 - Reading in Data: http://learnjsdata.com/read_data.html
 - Color Principles - http://www.stonesc.com/pubs/Expert%20Color%20Choices.pdf
 - Gestalt Principles of Perception - http://www.slideshare.net/luisaepv/the-gestalt-laws-of-perception
 - Titanic Data and Feature Understanding - https://www.kaggle.com/c/titanic/data 