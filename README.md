## LeToR

1. Always 25 mechanisms that generate rankings? Or is it per query?
2. Are all 25(X) always mentioned?
3. Print in output file in increading order of query id?

4. RRF- Currently not counting un-occured results at all, counting as rank 1000 gives decreased perf
5. Ranks - Better Document when higher rank or lower?

6. Check Ranking for all models

7. For bayesfuse, probability of falling in a region == (probability rank = r) ? Wouldn't make a difference, gets cancelled!

8. Condorcet all perfect, except ranking desc or asc. Also adding if exists in D1 but not in D2, D1 better! Significantly imporved

9. Bordacount - gave a-ve reward even for documents not labelled at all






./getscores.sh -> to get eval results
./[algorithm].sh -> to generate relevant file (currently gets stored in trec_eval/)

> RRF on no-retrieve -> 0.4772
> RRF on no-retrieve = 1000 -> 0.4768
> RRF on no-retrieve = 500 -> 0.4757
> RRF on no-retrieve = 100 -> 0.4502