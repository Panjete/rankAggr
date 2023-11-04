## For generating qels file
## One time Run just

def generator(infile, outfile):
    with open(infile, 'r') as f:
        lines = f.readlines()

    dictionary = {}
    for line in lines:
        words = line.split()
        relevance_label = int(words[0])
        qid = int(words[1].split(":")[1])
        i = 2
        while True:
            if(words[i][:1] == "#"):
                docid = words[i+2]
                break
            else:
                i+=1
        if qid in dictionary:
            dictionary[qid].append((docid, relevance_label))
        else:
            dictionary[qid] = [(docid, relevance_label)]

    print("Input Parsed, Writing Qrels")
    sorted_keys = sorted(dictionary.keys())
    with open(outfile, "w") as wf:
        for qid in sorted_keys:
            for did, rlabel in dictionary[qid]:
                wf.write(str(qid) + " Q0 " + str(did) + " " + str(rlabel) + " \n")
    
        
    return 


    
generator("MQ2008-agg/agg.txt", "trec_eval-9.0.7/qrels.txt")
