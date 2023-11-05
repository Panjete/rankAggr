## For reading [collection-file]
# returns a dictionary with query ID as the key
# dict[queryID] -> list of (Document_id, relevance_label, rankings)
# where, rankings is a dictionary (RankingMechanism -> RankGiven) with RankGiven = -1
# if the RankingMechanism does not enlist this document

def reader(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    dictionary  = {}
    print("parsing numlines = ", len(lines))
    for line in lines:
        words = line.split()
        relevance_label = int(words[0])
        qid = int(words[1].split(":")[1])
        i = 2
        rankings_doc_query = {}
        while True:
            ind_rank_pair = words[i]
            if(ind_rank_pair[:1] == "#"):
                break
            i+=1
            ind, rank = ind_rank_pair.split(":")
            if rank != "NULL":
                rankings_doc_query[int(ind)] = int(rank)
            else:
                rankings_doc_query[int(ind)] = -1
        while True:
            if(words[i][:1] == "#"):
                docid = words[i+2]
                break
            else:
                i+=1
        if qid in dictionary:
            dictionary[qid].append((docid, relevance_label, rankings_doc_query))
        else:
            dictionary[qid] = [(docid, relevance_label, rankings_doc_query)]
    return dictionary

def prob_rank_r_given_relevant(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    dictionary  = {}
    print("parsing numlines = ", len(lines))
    for line in lines:
        words = line.split()
        relevance_label = int(words[0])
        qid = int(words[1].split(":")[1])
        i = 2
        rankings_doc_query = {}
        while True:
            ind_rank_pair = words[i]
            if(ind_rank_pair[:1] == "#"):
                break
            i+=1
            ind, rank = ind_rank_pair.split(":")
            if rank != "NULL":
                rankings_doc_query[int(ind)] = int(rank)
            else:
                rankings_doc_query[int(ind)] = -1
        while True:
            if(words[i][:1] == "#"):
                docid = words[i+2]
                break
            else:
                i+=1
        if qid in dictionary:
            dictionary[qid].append((docid, relevance_label, rankings_doc_query))
        else:
            dictionary[qid] = [(docid, relevance_label, rankings_doc_query)]
    return dictionary
    
#reader("MQ2008-agg/agg.txt")
