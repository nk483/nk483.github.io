Hello! I see you've stumbled upon my final project! I know with all these folders you might be wondering where to even start, but
fear not, this document is a guide that will help you navigate my project.

So, first of all what is this project? This project is a website. More specifically, a basketball analytics website that will tell
users the greatest NBA player ever based on the specifications they input.

Where can I find the data you're using? All of my data is in a database called basketball.db . It can be opened by clicking the
database folder and then doubleclicking basketball.db . The original data is a .csv file that can be found in the datacleaning
folder. The python code and SQL queries I used to get from the raw data to the data I wanted are document in the .py files in
the datacleaning folder.

Ok, how do I run your website? Assuming you are in the /project folder in your terminal and using cs50 IDE, simply type in
"flask run" into your terminal. This will print a set of 5 lines, you're going to want to click on the link that is provided in
the penultimate line. This link takes you to a localhost server that is hosting my website.

What all can I do on your website? You will see that the link to you to the homepage of my website. On the homepage, you will see
7 dropdown menus, 3 checkboxes, and 3 input textboxes asking for a Number. Click the highest up dropdown menu, you will see
a bunch of basketball statistics drop down. If you think the best basketball player of all time is the highest point scorer,
click Points, if you think they are the best rebounder, click Rebounds... you get it. Now that you have done, hit the Go! button
on the bottom. You will have been redirected to a website displayer an NBA player's name, some statistic of theirs, and
their picture. This is the greatest basketball player of all-time based on the statistic you specified. To go back to the
homepage and input another statistic, simply click the button on the top left that says EightThirtyFive. That is the core
functionality of my website. There are however, more advanced searches you can do. You can add conditions to your queries by
checking any of the condition checkboxes. For example if you select Points in the highest up drop-down and then select the
Condition 1 checkbox and then select Assists in the drop-down just below it, and write 1000 in the number field, and hit Go!,
the page displayed will have the highest Point scorer in basketball history who also had more than 1000 assists. You can give up to
3 conditions. If your conditions are so picky that no such basketball player fits the bill, you will be displayed a page
saying there was no such player. One last piece of functionality I want to share with you is that once you type in a number you
do not have to click the Go! button, you can simply click Enter on your keyboard.




