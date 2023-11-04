import argparse
from reader_file import reader

aparser = argparse.ArgumentParser(description="Process filenames")
aparser.add_argument("collection_file", nargs=1)
aparser.add_argument("output_file", nargs=1)
args = aparser.parse_args()

collection_file = args.collection_file[0]
output_file = args.output_file[0]

collection_file = "MQ2008-agg/agg.txt"
output_file = "trec_eval-9.0.7/rrf.txt"

dictionary = reader(collection_file)
#print(dictionary[10002])

k = 60 ### Hyper-parameter

sorted_keys = sorted(dictionary.keys())

def rrf_rank_aggr(listOfDocs):
    for docid, rel_label, ranks in listOfDocs:
        doc_score = 0.0
        for ranking_mechanism in ranks.keys():
            if ranks[ranking_mechanism]!= -1:
                doc_score += (1/ (k + ranks[ranking_mechanism]))
        scores[docid] = doc_score
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

with open(output_file, 'w') as wf:
    for qid in sorted_keys:
        scores = {} # For all the documents in this qid, will contain scores
        ordered_scores = rrf_rank_aggr(dictionary[qid])
        aggrank = 1
        for aggid, aggscore in ordered_scores:
            wf.write(str(qid) + " Q0 " + aggid + " " + str(aggrank) + " " + str(aggscore) + " gsp1\n")
            aggrank += 1

print("All done!")



