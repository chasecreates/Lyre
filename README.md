## Inspiration
We both consider ourselves enamored with the therapeutic effects of music. Music can lift your spirits, facilitate your happiness, and push you upwards in life. At times when we're feeling low, music can catapult us back up—however, finding the right music to do that is challenge. That's where Lyre shines.

## What it does
What Lyre does is simple! Lyre takes a picture of your face and recommends ten songs, their previews, and the ability to stream it from Spotify. It's easy enough for the laymen, after all that's what we're aiming for.

## How we built it
Lyre was built using the Flask micro-framework for Python. Extensive use of HTML and CSS was utilized for the frontend. For recognizing your emotion merely from your face, we trained a deep convolutional neural network on the easily accessible Cohn-Kanade dataset. The data was trained for 200 epochs, for a total of two hours, before converging and reaching a fair accuracy of 81% (this could've been completed far quicker with more relative accuracy if we had our GPUs!). The Keras framework was used to define the model. The weights of the neural network were saved into an HD5  file and included in the Flask application. We then wrapped the Spotify API with Python and integrated it into our application.


## Challenges we ran into
A few obstructions hindered our progress, including integrating the network weights into the Flask application, creating the frontend without error, combing through the Spotify API JSON for the right output, and building a list comprehension to handle the aforementioned.


## Accomplishments that we're proud of
We're proud of having a finished project that accomplishes what we initially set out to do. We severely underestimated our skills, however after developing it in its entirety, we found it feasible. 

## What we learned
Christian learned how to build a frontend utilizing the Bootrstrap framework.
Chase learned how to wrap APIs into a Python application and implement neural network weights into the application.

## What's next for Lyre
Depending on its reception, we intend to debut it on the world wide web after further tinkering and perfecting.