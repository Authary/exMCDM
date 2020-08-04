# EXPLAINING MULTICRITERIA DECISION MAKING

Python module with functions for explaining the presence of alternatives on a Pareto front with background knowledge on the criteria. Some additional preference aggregation functions are provided.

Functionalities:<br/>
-Rankings -> Pareto front<br/>
-Rankings x Alternative -> Minimal sets of criteria for which the alternative appears on the Pareto front<br/>
-Rankings x Knowledge -> Explanation of the reasons why alternatives appears on the Pareto front<br/>
-Rankings -> Aggregated ranking (Borda, Condorcet, Copeland, Majority, Bucklin)

# LEGAL STUFF

You are free to use this module.<br/>
If you do something interesting with it, please tell Alexandre Bazin: contact [at] alexandrebazin [dot] com.

# INPUT FORMAT

*Rankings*

The rankings of alternatives should contained in a file such that each line is an alternative and the rankings of the alternatives by the different criteria are separated by commas.<br/>
Example:<br/>
1,1,3<br/>
3,2,2<br/>
2,3,1<br/>
4,4,4<br/>
5,5,5<br/>
corresponds to the following rankings:<br/>
Criteria1 : a1 > a3 > a2 > a4 > a5<br/>
Criteria2 : a1 > a2 > a3 > a4 > a5<br/>
Criteria3 : a3 > a2 > a1 > a4 > a5


*Background knowledge*

The background knowledge takes the form of a set of rules of the form A -> B in which A and B are sets of terms. It should be contained in a file such that each line corresponds to a rule. The terms are separated by commas and the premise and conclusion are separated by semicolons.<br/>
Example:<br/>
Blue;Color<br/>
Green;Color<br/>
Green,Big,Triangle;Tree<br/>
Square;Shape<br/>
Triangle;Shape<br/>


*Giving meaning to criteria*

The assignment of meaning to the criteria should be contained in a file such that the ith line corresponds to the ith criterion. A line contains a set of terms separated by commas.<br/>
Example:<br/>
Blue,Square<br/>
Big,Green,Triangle<br/>
Shape<br/>
states that the first criterion is a blue square, the second criterion is a big green triangle and the third criterion is a shape.

# USEFUL FUNCTIONS

*loadRanking(f)*<br/>
INPUT: a file f containing the rankings<br/>
OUTPUT: the rankings


*loadKnowledgeBase(f)*<br/>
INPUT: a file f containing the background knowledge<br/>
OUTPUT: the background knowledge


*loadKnowledgeCriteria(f)*<br/>
INPUT: a file f containing the assignment of terms to criteria<br/>
OUTPUT: the knowledge about the criteria


*ParetoDepth(ranks,depth)*<br/>
INPUT: the rankings (ranks) and an integer (depth)<br/>
OUTPUT: the biggest elements in the set of alternatives ordered by the Pareto dominance relation, up to a given depth (use 1 for the Pareto front)


*minCritSets(alt, rankings, depth)*<br/>
INPUT: an alternative (alt), the rankings (rankings) and an integer (depth)<br/>
OUTPUT: a list of the minimal criterion sets for which the alternative appears in the output of ParetoDepth(rankings,depth)


*constructInterpretation(rankings, knowlCrit, knowledge, depth)*<br/>
INPUT: the rankings (rankings), knowledge about the criteria (knowlCrit), the background knowledge (knowledge) and an integer (depth)<br/>
OUTPUT: A list of lists of terms. The ith list explains the presence of the ith alternative in the output of ParetoDepth(rankings,depth).


*<aggregation function>(rankings)* [Borda, Condorcet, Copeland, Majority, Bucklin]<br/>
INPUT: the rankings
OUTPUT: a list of the scores of each alternative
  
  
*Rank(Scores)*
INPUT: a list of the scores of each alternative
OUTPUT: a ranking of the alternatives


# HOW TO USE

#load your data<br/>
ranks = loadRankings("rankings.txt")<br/>
knowl = loadKnowledgeBase("knowledge.txt")<br/>
knowlCrit = loadKnowledgeCriteria("criteria.txt")

#Explain the presence of alternatives on the Pareto front<br/>
Explanation = constructInterpretation(ranks, knowlCrit, knowl, 1)

#Rank the alternatives according the Condorcet method<br/>
newRanks = Ranks(Condorcet(ranks))
