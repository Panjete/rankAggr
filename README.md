## To Run

* `bash rrf.sh [collection-file] [output-file]` - to get RRF aggregation on results from `[collection-file]` written into `[result-file]`.
* `bash bordacount.sh [collection-file] [output-file]` - to get Borda Count aggregation on results from `[collection-file]` written into `[result-file]`.
* `bash condorcet.sh [collection-file] [output-file]` - to get Condorcet aggregation on results from `[collection-file]` written into `[result-file]`.
* `bash bayesfuse.sh [collection-file] [output-file]` - to get BayesFuse aggregation on results from `[collection-file]` written into `[result-file]`.
* `bash bordafuse.sh [collection-file] [output-file]` - to get Bordafuse aggregation on results from `[collection-file]` written into `[result-file]`.


* `bash getscores.sh` -> to get trec_eval results (read script for I/O compatibilty)
* `python getqrels.py` -> to obtain a qrels file to trec_eval computation from `[collection-file]`

## REFERENCES

[1] Javed A. Aslam and Mark H. Montague. Models for metasearch. In SIGIR, 2001. URL: https://www.khoury.northeastern.edu/home/jaa/CSG339.06F/resources/borda_metas.pdf.

[2] GordonV.Cormack, CharlesL.A.Clarke, andStefan Buttcher. Reciprocal rank fusion outperforms condorcet and individual rank learning methods. Proceedings of the 32nd international ACM SIGIR conference on Research and development in information retrieval, 2009. URL: https://api.semanticscholar.org/CorpusID:12408211.

[3] Mark H. Montague and Javed A. Aslam. Condorcet fusion for improved retrieval. In International Con- ference on Information and Knowledge Management, 2002. URL: https://api.semanticscholar.org/CorpusID:5201014.

## RESULTS 

As map, p@5 and p@10 values, 

* RRF on no-retrieve = 500 -> 0.4757, 0.3375, 0.2439
* RRF on no-retrieve = 100 -> 0.4502, 0.3194, 0.2304

* RRF on k = 10 -> 0.4707, 0.3332, 0.2408
* RRF on k = 60 -> 0.4772, 0.3413, 0.2450
* RRF on k = 60, including NULL docs with rank = 1000 -> 0.4768 , 0.3401, 0.2444
* RRF on k = 100 -> 0.4780, 0.3444, 0.2455
* RRF on k = 150 -> 0.4796, 0.3464, 0.2463
* RRF on k = 300 -> 0.4811, 0.3457, 0.2460
* RRF on k = 400 -> 0.4786, 0.3457, 0.2460


* Bordacount approach 1 -> 0.3981, 0.2911, 0.2250
* Bordacount approach 2 = 0.4773, 0.3454, 0.2457
* Without considering non-retrieved = 0.2416, 0.1497, 0.1589

* Condorcet -> 0.4786, 0.3449, 0.2485
* Condorcet ignoring non-retrieved -> 0.3942, 0.2888, 0.2249

* Bayesfuse with fine prob classes -> 0.4799, 0.3462, 0.2464
* Bayesfuse without considering irrelevant at all -> 0.4807, 0.3457, 0.2460

* Variants of Bordafuse maps -> 0.4855, 0.4835
* Final optimisations of Bordafuse -> 0.4862, 0.3485, 0.2489




