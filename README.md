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

> RRF on no-retrieve -> 0.4772, 0.3413, 0.2450
> RRF on no-retrieve = 1000 -> 0.4768 , 0.3401, 0.2444
> RRF on no-retrieve = 500 -> 0.4757, 0.3375, 0.2439
> RRF on no-retrieve = 100 -> 0.4502, 0.3194, 0.2304

> Bordacount apprach 2 -> for each query, find out all the documents ranking mechanism has ordered -> give points -> add points -> rank -> score = 0.3981, 0.2911, 0.2250
> Using total_ret - rank = 0.4773, 0.3454, 0.2457
> Without considering non-retrieved = 0.2416, 0.1497, 0.1589

> Condorcet with -> 0.4786, 0.3449, 0.2485
> Condorcet ignoring non-retrieved -> 0.3942, 0.2888, 0.2249