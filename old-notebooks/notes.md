# todo

- td distributions - easier bc more bayesian?
- weights for recent performance - can i back into this?
- get all params that contribute to player perforamnce
- scrape fantasy sites for performance metrics - ADP etc for comparison
- lombardi.io - compare two players, one player at a time, etc
- how to break out attribution percentages? hypothesis is greater weight should be placed on yardage
- streaky players, consistent players, boom/bust players - k means? how to define?
- what is the mvp solution? what can i base my pre/post week 1 actions on?
- how to aggregate team performance to some cumulative probability distribution?
- what to do about proposing trades - determine what sounds reasonable but where i'm really gaining an advantage due to my model?
- obviously bayesian approach asap
- attempt at bayesian solution after clustering players


# how to continuously update a player's pdf

let's say we have player A, who usually ends up with 50 yards per game. Then we have player B, who gets like 150 yards per game on average. Each run for 200 yards. How does that data point affect each player's probability distribution afterwards?

At first blush I might assume my prior about player A was worse than it should have been - maybe he's recently gotten better, and I should adjust for that. On the other hand, while player B had an awesome game, he had a relatively less awesome game than player A. I don't foresee updating player B's distribution as much as I would for player A.

But this is because I know at least a bit of how football works and how distributions work across the board. I know that there's high variance, so consequently shouln't update any model *too* much given a single data point. Like, player A could still suck but could have had a fluke game.

So is the likelihood function simply the aggregate of all players? The case is clear when determining what bucket - elite, mid-level, or scrub - a player should fall in.

Well, actually I can code an example of that to have it more clear in my mind.

Okay, that was easy. One thing to consider is what are the other factors that contribute to the likelihood of the player getting a certain amount of yards in a given game. If player A doesn't have a great prior, but he comes out and gets 200 yards against the best defense in the league who are consistently excellent, there's a good chance we underrated player A.

Then again, we wouldn't update the distribution as much if the defense he was playing against was historically garbage.

So what I'm drawing from all this is that it's a serious task to create the likelihood distribution. What if I added opponent strength to this model of mine for informing a better likelihood model? That's at least one parameter that would adjust the likelihood distribution.

And I think it's gonna be some sort of mixture of frequentist and bayesian methods to get at those likelihoods.

Weird but entirely sensical issue - incorporating opponent distributions to inform likelihood calculations doesn't help, because for a given result (a), we get the likelihood that a player will do that against an opponent (0.7), and for each player type (alpha, beta, gamma, delta) we multiply their probability of getting that result by that scalar, which gets lost after normalization.














