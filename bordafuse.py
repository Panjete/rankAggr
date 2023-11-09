import argparse
from reader_file import reader
from math import sqrt


aparser = argparse.ArgumentParser(description="Process filenames")
aparser.add_argument("collection_file", nargs=1)
aparser.add_argument("output_file", nargs=1)
args = aparser.parse_args()

collection_file = args.collection_file[0]
output_file = args.output_file[0]

dictionary = reader(collection_file)
#print(dictionary[10002])

k = 60




# rel_docs_counted = dict([(i, 0) for i in range(1, 26)]) ## Contains the number of relevant documents retrieved by this system
# ## The more relevant nodes a system retrieves, the more reliable it is 
# for qid in dictionary.keys():
#     for _, rel_label, ranks in dictionary[qid]:
#         if rel_label>0:
#             for key in ranks.keys():
#                 if ranks[key]!=-1:
#                     rel_docs_counted[key] += 1

# weights_ranks = {}
# total_rel_documents = 0
# for rs in range(1, 26):
#     total_rel_documents += rel_docs_counted[rs]
# for rs in range(1, 26):
#     weights_ranks[rs] = rel_docs_counted[rs]/total_rel_documents


## For a file, returns dictionary ranker -> total relevant documents retrieved by the ranker
def get_stats_file(filename):
    dictionary_f = reader(filename)
    rel_docs_counted = dict([(i, 0) for i in range(1, 26)]) ## Contains the number of relevant documents retrieved by this system
    for qid in dictionary_f.keys():
        for _, rel_label, ranks in dictionary_f[qid]:
            if rel_label>0:
                for key in ranks.keys():
                    if ranks[key]!=-1:
                        rel_docs_counted[key] += rel_label * ranks[key] ## without multiplication -> 0.4855, now 0.4866
                    else:
                        rel_docs_counted[key] -= 0.1 * ranks[key]


                        # if ranks[key] < 500:  #### 4852
                        #     rel_docs_counted[key] += 5*(rel_label) ## Promote higher rel and lower rank
                        # else:
                        #     rel_docs_counted[key] += rel_label


                        #rel_docs_counted[key] += (rel_label/ranks[key]) #### 4835
                        #rel_docs_counted[key] += rel_label * ranks[key] #### 4862 ## Promote higher rel and lower rank
                        

    return rel_docs_counted

def get_weights(filenames):
    rel_docs_total = dict([(i, 0) for i in range(1, 26)])
    for file in filenames:
        local_stats = get_stats_file(file)
        for j in range(1, 26):
            rel_docs_total[j] += local_stats[j]

    total_rel_documents = sum(rel_docs_total)

    weights_ranks = {}
    for rs in range(1, 26):
        weights_ranks[rs] = rel_docs_total[rs]/total_rel_documents

    return weights_ranks

filenames = ["MQ2008-agg/agg.txt",
                         "MQ2008-agg/Fold1/test.txt", "MQ2008-agg/Fold1/train.txt", "MQ2008-agg/Fold1/vali.txt",
                         "MQ2008-agg/Fold2/test.txt", "MQ2008-agg/Fold2/train.txt", "MQ2008-agg/Fold2/vali.txt",
                         "MQ2008-agg/Fold3/test.txt", "MQ2008-agg/Fold3/train.txt", "MQ2008-agg/Fold3/vali.txt",
                         "MQ2008-agg/Fold4/test.txt", "MQ2008-agg/Fold4/train.txt", "MQ2008-agg/Fold4/vali.txt",
                         "MQ2008-agg/Fold5/test.txt", "MQ2008-agg/Fold5/train.txt", "MQ2008-agg/Fold5/vali.txt"
                        ]

global_weights = get_weights(filenames)
sorted_keys = sorted(dictionary.keys())

def weightedborda(listOfDocs):
    for docid, _, ranks in listOfDocs:
        doc_score = 0
        for ranking_mechanism in ranks.keys():
            if ranks[ranking_mechanism]!= -1:
                doc_score -= ranks[ranking_mechanism] * global_weights[ranking_mechanism] ## The bigger the absolute number, the worse 
            else :
                doc_score -= 1000 * global_weights[ranking_mechanism]
        scores[docid] = doc_score

    return sorted(scores.items(), key=lambda x: x[1], reverse=True) 

with open(output_file, 'w') as wf:
    for qid in sorted_keys:
        scores = {} # For all the documents in this qid, will contain scores
        ordered_scores = weightedborda(dictionary[qid])
        aggrank = 1
        for aggid, aggscore in ordered_scores:
            wf.write(str(qid) + " Q0 " + aggid + " " + str(aggrank) + " " + str(aggscore) + " gsp1\n")
            aggrank += 1

print("All done!")


    