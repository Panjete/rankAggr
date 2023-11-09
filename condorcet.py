import argparse
from reader_file import reader

aparser = argparse.ArgumentParser(description="Process filenames")
aparser.add_argument("collection_file", nargs=1)
aparser.add_argument("output_file", nargs=1)
args = aparser.parse_args()

collection_file = args.collection_file[0]
output_file = args.output_file[0]

dictionary = reader(collection_file)
# dicttionary[queryID] -> list of (Document_id, relevance_label, rankings)
# where, rankings is a dictionary (RankingMechanism -> RankGiven) with RankGiven = -1
# if the RankingMechanism does not enlist this document

#print(dictionary[10002])

k = 60 ### Hyper-parameter

sorted_keys = sorted(dictionary.keys())


### Algorithm 1 in the paper
def simple_majority_runoff(ranks_d1, ranks_d2):
    count = 0
    for key in ranks_d1.keys():
        if key in ranks_d2:
            if ranks_d1[key]!= -1 and ranks_d2[key]!= -1:
                if ranks_d2[key] > ranks_d1[key]:
                    count += 1 #D1 is ranked higher
                else:
                    count -= 1
            elif ranks_d1[key]!= -1:
                count += 1 #D1 is ranked better
            elif ranks_d2[key] != -1:
                count -= 1 # D2 is ranked better

    if count > 0:
        return True ## D1 better than D2
    return False

### Basically a quicksort (descending order) over the list of documents
def condorcetfuse(listOfDocs):
    n = len(listOfDocs)
    if n < 2:
        return listOfDocs
    
    pivot_docid, pivot_rel_label, pivot_ranks = listOfDocs[n//2]
    left_list = []
    right_list = []


    for i in range(n):
        if i != n//2:
            docid, rel_label, ranks = listOfDocs[i]
            if simple_majority_runoff(ranks, pivot_ranks): ## i th is better than pivot
                left_list.append((docid, rel_label, ranks))
            else:
                right_list.append((docid, rel_label, ranks))

    return condorcetfuse(left_list) + [(pivot_docid, pivot_rel_label, pivot_ranks)] + condorcetfuse(right_list)


with open(output_file, 'w') as wf:
    for qid in sorted_keys:
        scores = {} # For all the documents in this qid, will contain scores
        ordered_scores = condorcetfuse(dictionary[qid])
        aggrank = 1
        aggscore = len(ordered_scores)
        for aggid, _, _ in ordered_scores:
            wf.write(str(qid) + " Q0 " + aggid + " " + str(aggrank) + " " + str(aggscore) + " gsp1\n")
            aggrank += 1
            aggscore -= 1

print("All done!")



