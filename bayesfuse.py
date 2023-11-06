import argparse
from reader_file import reader
from math import log

aparser = argparse.ArgumentParser(description="Process filenames")
aparser.add_argument("collection_file", nargs=1)
aparser.add_argument("output_file", nargs=1)
args = aparser.parse_args()

collection_file = args.collection_file[0]
output_file = args.output_file[0]

collection_file = "MQ2008-agg/agg.txt"
output_file = "trec_eval-9.0.7/bayesfuse.txt"

dictionary = reader(collection_file)
# dicttionary[queryID] -> list of (Document_id, relevance_label, rankings)
# where, rankings is a dictionary (RankingMechanism -> RankGiven) with RankGiven = -1
# if the RankingMechanism does not enlist this document

#print(dictionary[10002])

k = 60 ### Hyper-parameter

ranges = [(1, 5), (6, 10), (11, 15), (16, 20), (21, 30), (31, 100), (101, 200), (201, 500), (501, 1000), (1001, 100_000)]
n_ranges = len(ranges)
len_ranges = {0: 5, 1: 5, 2: 5, 3: 5, 4: 10, 5: 70, 6:100, 7:300, 8: 500, 9: 1000}

def index_num(i):
    if i >= 1 and i <= 5:
        return 0
    if i >= 6 and i <= 10:
        return 1
    if i >= 11 and i <= 15:
        return 2
    if i >= 16 and i <= 20:
        return 3
    if i >= 21 and i <= 30:
        return 4
    if i >= 31 and i <= 100:
        return 5
    if i >= 101 and i <= 200:
        return 6
    if i >= 201 and i <= 500:
        return 7
    if i >= 501 and i <= 1000:
        return 8
    else:
        return 9
        
def prob_distbn(dictionary):
    ranking_systems_rel = {}
    ranking_systems_irrel = {}
    for qid in dictionary.keys():
        for _, rel_label, ranks in dictionary[qid]:
            if rel_label > 0: # consider only relevant ones
                for rs in ranks.keys(): ## For this document, append ranks to the relevant ranking system
                    if ranks[rs] != -1:
                        if rs in ranking_systems_rel:
                            ranking_systems_rel[rs].append(ranks[rs])
                        else:
                            ranking_systems_rel[rs] = [ranks[rs]]
            else: ## considering irrelevant ones!
                for rs in ranks.keys(): ## For this document, append ranks to the irrelevant ranking system
                    if ranks[rs] != -1:
                        if rs in ranking_systems_irrel:
                            ranking_systems_irrel[rs].append(ranks[rs])
                        else:
                            ranking_systems_irrel[rs] = [ranks[rs]]

    for rs in ranking_systems_rel.keys():
        ranking_systems_rel[rs] = sorted(ranking_systems_rel[rs])
        ranking_systems_irrel[rs] = sorted(ranking_systems_irrel[rs])
        
    rs_distbn_rel = {}
    rs_distbn_irrel = {}
    for rs in ranking_systems_rel.keys():
        rs_distbn_rs = [1 for i in range(n_ranges)] # 1 to prevent log and division error
        for el in ranking_systems_rel[rs]:
            rs_distbn_rs[index_num(el)] += 1

        total_rel = sum(rs_distbn_rs) # Computing the probability
        for i in range(n_ranges):
            rs_distbn_rs[i] = rs_distbn_rs[i]/total_rel

        rs_distbn_rel[rs] = rs_distbn_rs

    for rs in ranking_systems_irrel.keys():
        rs_distbn_rs = [1 for i in range(n_ranges)] # 1 to prevent log and division error
        for el in ranking_systems_irrel[rs]:
            rs_distbn_rs[index_num(el)] += 1

        total_irrel = sum(rs_distbn_rs) # Computing the probability
        for i in range(n_ranges):
            rs_distbn_rs[i] = rs_distbn_rs[i]/total_irrel

        rs_distbn_irrel[rs] = rs_distbn_rs




    return rs_distbn_rel, rs_distbn_irrel

prob_dist_rel, prob_dist_irrel = prob_distbn(dictionary)
#print("relevance distbn for system 1 : ", prob_dist_rel[1])
#print("irrelevance distbn for system 2 : ", prob_dist_irrel[1])


sorted_keys = sorted(dictionary.keys())

def bayesfusescore(listOfDocs):
    for docid, rel_label, ranks in listOfDocs:
        doc_score = 0.0
        for ranking_mechanism in ranks.keys():
            if ranks[ranking_mechanism]!= -1:
                index_of_range = index_num(ranks[ranking_mechanism])
                prob_of_being_rel_in_this_range = prob_dist_rel[ranking_mechanism][index_of_range]
                prob_of_being_irrel_in_this_range = prob_dist_irrel[ranking_mechanism][index_of_range]
                doc_score += log(prob_of_being_rel_in_this_range/prob_of_being_irrel_in_this_range)
            else:
                prob_of_being_rel_in_this_range = prob_dist_rel[ranking_mechanism][n_ranges-1]
                prob_of_being_irrel_in_this_range = prob_dist_irrel[ranking_mechanism][n_ranges-1]
                doc_score += log(prob_of_being_rel_in_this_range/prob_of_being_irrel_in_this_range)
        scores[docid] = doc_score
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

with open(output_file, 'w') as wf:
    for qid in sorted_keys:
        scores = {} # For all the documents in this qid, will contain scores
        ordered_scores = bayesfusescore(dictionary[qid])
        aggrank = 1
        for aggid, aggscore in ordered_scores:
            wf.write(str(qid) + " Q0 " + aggid + " " + str(aggrank) + " " + str(aggscore) + " gsp1\n")
            aggrank += 1

print("All done!")



