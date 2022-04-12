# AppleSoft
AppleSoft is the version of MS-Basic provided for the Apple II computer. It is a very limited version of basic, which makes it difficult to work with. However, it is the first language I learned. Using that first Apple II computer, I was able to explore some of the math and computing concepts I learned in school. 

I find returning to this platform to be enlightening. Writing in this crippled language is like working through a complex puzzle. My ability to work through a problem reflects some of the new skills I have acquired over time. Overall, writing for this platform is like completing a difficult crossword puzzle. It’s a mental challenge that provides a sense of accomplishment through success.

Below are some of the challenges found with working with AppleSoft.

* Variable names are only recognized by the first two letters. That means "Test" and "Text" are the same variable. Due to this limitation, I have found it easier to only use two letters for all variables. While this is a detriment to readability, using longer names makes it too easy to accidentally overwrite variables.

* All variables are global. This is a common trait for early versions of MS-Basic. This means that all variables need to be closely accounted for. It also forces the use for certain naming strategies, such as L1, L2, etc, for loop variables. 

* The only loops provided are FOR – NEXT, and GOTO. The GOTO command was common in very early languages, but led to unreadable code. GOTO can be used to emulate a DO or WHILE loop using comments at both ends to provide readability.

* There is no support for ELSE. AppleSoft provides an IF command, but not an ELSE command. Two strategies for this are setting a default state prior to IF, or branching to a sub routine to work out the details of the two conditions. In some cases, multiple IF statements may be needed as well.

* Unlike most modern languages, MS-Basic only supported single line operations. Logic following an IF statement either needs to be stitched together on a single line with colons, or needs to branch to a sub routine to handle more complex steps. 

* Each line only supports 256 characters. While you can use colons to stitch together multiple steps, the entire line must be less than 256 characters.

* All lines must be numbered, which makes it near impossible to re-arrange sections of code after they have been written. When writing code, you need to number subroutines carefully to maintain readability. An Apple program named “RENUMBER” will automatically renumber code, but it is applied blindly which hinders code readability.

I am sure there are a lot more limitations that I am not considering, but these seem to be the largest ones.
