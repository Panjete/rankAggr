import argparse
from reader_file import reader

aparser = argparse.ArgumentParser(description="Process filenames")
aparser.add_argument("collection_file", nargs=1)
aparser.add_argument("output_file", nargs=1)
args = aparser.parse_args()

collection_file = args.collection_file[0]
output_file = args.output_file[0]

# collection_file = "MQ2008-agg/agg.txt"
# output_file = "trec_eval-9.0.7/rrf.txt"

dictionary = reader(collection_file)
# dicttionary[queryID] -> list of (Document_id, relevance_label, rankings)
# where, rankings is a dictionary (RankingMechanism -> RankGiven) with RankGiven = -1
# if the RankingMechanism does not enlist this document

#print(dictionary[10002])

k = 60 ### Hyper-parameter
not_found_doc_rank = 100 ### Hyper-parameter, unused by experimental results

sorted_keys = sorted(dictionary.keys())

def rrf_rank_aggr(listOfDocs):
    scores = {} # document -> score map
    for docid, _, ranks in listOfDocs:
        doc_score = 0.0
        for ranking_mechanism in ranks.keys():
            if ranks[ranking_mechanism]!= -1:
                doc_score += (1/ (k + ranks[ranking_mechanism]))
            # else: ### After Analysis, found that best results when not included at all
            #     doc_score += (1/ (k + not_found_doc_rank))
        scores[docid] = doc_score
    new_sorted_list = sorted(scores.items(), key=lambda x: x[1], reverse=False)
    return new_sorted_list

with open(output_file, 'w') as wf:
    for qid in sorted_keys:
        scores = {} # For all the documents in this qid, will contain scores
        ordered_scores = rrf_rank_aggr(dictionary[qid])
        aggrank = 1
        for aggid, aggscore in ordered_scores:
            wf.write(str(qid) + " Q0 " + aggid + " " + str(aggrank) + " " + str(aggscore) + " gsp1\n")
            aggrank += 1

print("All done!")



