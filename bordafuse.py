import argparse
from reader_file import reader

aparser = argparse.ArgumentParser(description="Process filenames")
aparser.add_argument("collection_file", nargs=1)
aparser.add_argument("output_file", nargs=1)
args = aparser.parse_args()

collection_file = args.collection_file[0]
output_file = args.output_file[0]

dictionary = reader(collection_file)
#print(dictionary[10002])

k = 60

weights_rankers = dict([(i, 1) for i in range(1, 26)])



sorted_keys = sorted(dictionary.keys())

def borda(listOfDocs):
    for docid, rel_label, ranks in listOfDocs:
        doc_score = 0
        for ranking_mechanism in ranks.keys():
            if ranks[ranking_mechanism]!= -1:
                doc_score -= weights_rankers[ranking_mechanism] * ranks[ranking_mechanism] ## The bigger the absolute number, the worse -> Need to improve this!!
            else :
                doc_score -= weights_rankers[ranking_mechanism] * 1000
        scores[docid] = doc_score
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

with open(output_file, 'w') as wf:
    for qid in sorted_keys:
        scores = {} # For all the documents in this qid, will contain scores
        ordered_scores = borda(dictionary[qid])
        aggrank = 1
        for aggid, aggscore in ordered_scores:
            wf.write(str(qid) + " Q0 " + aggid + " " + str(aggrank) + " " + str(aggscore) + " gsp1\n")
            aggrank += 1

print("All done!")
