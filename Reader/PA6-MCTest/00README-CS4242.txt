MCTest: Machine comprehension test
http://research.microsoft.com/mct


This is a subset of the original MCTest data as distributed by
Microsoft. The original dataset is described in 00README.txt.

The version for CS 4242 has been organized so that there is a
Dev, Train, and Test directory.  Please use Train and Dev to 
develop your system, and only use Test when your system is
finalized and you are nearly ready to submit your system with
results. 

tpederse@ukko:~/PA6-MCTest/Dev$ wc *
   50   200   450 mc500.dev.ans
   50 15608 88860 mc500.dev.tsv
  100 15808 89310 total

tpederse@ukko:~/PA6-MCTest/Test$ wc *
   150    600   1350 mc500.test.ans
   150  45036 258420 mc500.test.tsv
   300  45636 259770 total

tpederse@ukko:~/PA6-MCTest/Train$ wc *
   300   1200   2700 mc500.train.ans
   300  93705 537529 mc500.train.tsv
   600  94905 540229 total

00README.txt explains details of how the tsv files are formatted,
which is also copied below.

---- TSV/ANS Format ----

These consist of tab-delimited files, with one story set per line. 
The .tsv file contains the story, questions, and answers.
The .ans file contains the correct answer for each question

The format of a line in the TSV file is:
  Id <tab> properties <tab> story <tab> q1 <tab> q2 <tab> q3 <tab> q4 
    where
  qN = questionText <tab> answerA <tab> answerB <tab> answerC <tab> answerD
    and
  properties is a semicolon-delimited list of property:value pairs, including
    Author (anonymized author id, consistent across all files)
    Work Time(s): Seconds between author accepting and submitting the task
    Qual. score: The author's grammar qualification test score (% correct)
    Creativity Words: Words the author was given to encourage creativity
    (there are no creativity words or qual score for mc160, see paper)

The format of a line in the ANS file is:
  answer1 <tab> answer2 <tab> answer3 <tab> answer4
    where
  answerN is the correct answer (A, B, C, or D) for question N

Finally, because some authors used newlines and/or tabs to indicate
paragraph separation, and this would break the TSV format, we have
replaced any newline or tab with "\newline" or "\tab", respectively.
No questions or answers required this escaping.

