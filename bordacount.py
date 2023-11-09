import argparse
from reader_file import reader

aparser = argparse.ArgumentParser(description="Process filenames")
aparser.add_argument("collection_file", nargs=1)
aparser.add_argument("output_file", nargs=1)
args = aparser.parse_args()

collection_file = args.collection_file[0]
output_file = args.output_file[0]

collection_file = "MQ2008-agg/agg.txt"
output_file = "trec_eval-9.0.7/bordacount.txt"

dictionary = reader(collection_file)
sorted_keys = sorted(dictionary.keys())

def borda(listOfDocs):
    ranks_per_ranker = dict([(rs,{}) for rs in range(1, 26)]) ## Approach 1

    for docid, _, ranks in listOfDocs:
        doc_score = 0
        for ranking_mechanism in ranks.keys():
            ### Approach 1
            if ranks[ranking_mechanism]!= -1:
                doc_score -= ranks[ranking_mechanism] ## The bigger the absolute number, the worse 
                ## Assuming every ranker has the same total retrieved documents (say 1000), scores will be 
                ## sum (1000 - rank_retrieved) -> we can simply ignore the 1000 for all, and assume that non-retrieved docs occur at 1000
                ranks_per_ranker[ranking_mechanism][ranks[ranking_mechanism]] = docid ## Approach 1
            else :
                doc_score -= 1000
        scores[docid] = doc_score
    
    bscores = {}
    for rs in range(1, 26):
        j = 1
        for key in sorted(ranks_per_ranker[rs], reverse=True):
            if key in bscores:
                bscores[ranks_per_ranker[rs][key]] += j
            else:
                bscores[ranks_per_ranker[rs][key]] = j
            j += 1
    return sorted(scores.items(), key=lambda x: x[1], reverse=True) ## use bscores for approach 1, scores for approach 2

with open(output_file, 'w') as wf:
    for qid in sorted_keys:
        scores = {} # For all the documents in this qid, will contain scores
        ordered_scores = borda(dictionary[qid])
        aggrank = 1
        for aggid, aggscore in ordered_scores:
            wf.write(str(qid) + " Q0 " + aggid + " " + str(aggrank) + " " + str(aggscore) + " gsp1\n")
            aggrank += 1

print("All done!")
