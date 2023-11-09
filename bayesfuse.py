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
# dictionary[queryID] -> list of (Document_id, relevance_label, rankings)
# where, rankings is a dictionary (RankingMechanism -> RankGiven) with RankGiven = -1
# if the RankingMechanism does not enlist this document

## p(rank | relevance) computation is broken into it belonging to one of these buckets
## also, dividing by bucket size is not necesaary, gets cancelled in numerator/denominator computation anyways
#ranges = [(1, 5), (6, 10), (11, 15), (16, 20), (21, 30), (31, 100), (101, 200), (201, 500), (501, 1000), (1001, 1000_000)]
ranges = [(1, 5), (6, 10), (11, 15), (16, 20), (21, 30), (31, 50), (51, 75), (76, 100),
            (101, 125), (126, 150), (151, 175), (176, 200), (201, 225), (226, 250),
              (251, 275),(276, 300), (301, 325), (326, 350), (351, 375), (376, 400),
              (401, 425), (426, 450), (451, 475), (476, 500), (501, 525), (526, 550), (551, 600),
                (601, 650), (651, 700), (701, 750), (751, 800), (801, 900), (901, 1000), (1001, 1000_000)]
n_ranges = len(ranges)

# Computes which range the document rank lies in
def index_num(i):
    j = 0
    if i < 1 or i > ranges[-1][1]:
        return len(ranges) -1
    for left, right in ranges:
        if i >= left and i <= right:
            return j
        else:
            j += 1
        
## Returns p(rank = r| relevant) and p(rank = r| irrelevant)
def prob_distbn(dictionary):
    ranking_systems_rel = dict([(rs, []) for rs in range(1, 26)]) ## Contains all relevant documents' ranks retrieved by rs
    ranking_systems_irrel = dict([(rs, []) for rs in range(1, 26)]) ## Contains all irrelevant documents' ranks ranks retrieved by rs
    for qid in dictionary.keys():
        for _, rel_label, ranks in dictionary[qid]:
            if rel_label > 0: # consider only relevant ones
                for rs in ranks.keys(): ## For this document, append ranks to the relevant ranking system
                    if ranks[rs] != -1:
                        ranking_systems_rel[rs].append(ranks[rs])
                    else:
                        ranking_systems_rel[rs].append(1001)
                        
            else: ## considering irrelevant ones!
                for rs in ranks.keys(): ## For this document, append ranks to the irrelevant ranking system
                    if ranks[rs] == -1:
                        ranking_systems_irrel[rs].append(ranks[rs])
                    else:
                        ranking_systems_irrel[rs].append(1001)
                        
                        

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



