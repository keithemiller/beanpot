# beanpot

The Mongo Java project is an unfinished part of this project that was designed to work with a website.
The idea of this project was to take in images posted to the waiting REST endpoitn hosted by this application in SPRING. Then it would take those images and feed it to our python based machine learning system. That would then return a username based off of the images it was trained on then this would be used with the application and SPRING to pull the cabinets that the given user has access to. That would then be sent back to our hardware "unlocking" our cabinets. 

Unfortunately, we only got the MongoDB interaction to work. When trying to host the rest endpoint the application started generating comilation errors associated with the dependencies. We tried using Gradle Maven and even the spring IDE itself all to no avail. 
