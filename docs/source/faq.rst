Frequently Asked Questions
==========================

Why are the *New* and *Open* buttons merged?
++++++++++++++++++++++++++++++++++++++++++++

Ok, let's run through what would happen in the code for the **New** button:

    1. Get the package folder from the user;

    2. Check if an installer exists in that folder;

    3. If it doesn't exist, create a new one;

    4. It it does exist, complain to the user.

Now for the **Open** button:

    1. Get the package folder from the user;

    2. Check if an installer exists in that folder;

    3. If it doesn't exist, complain to the user;

    4. It it does exist, open it up.

Do you see how similar these two are? It wouldn't really make sense to have
two completely separate actions that do pretty much the same thing. This way
everything is much simpler on our side and we never have to complain to you!
