import argparse
# from sklearn.metrics import confusion_matrix

def calculate_precision_multiclass(predictions, ground_truth, labels, ood_ratio):
    n = len(predictions)
    precision_per_classs_id = []
    precision_per_classs_ood = []
    k = len(labels)
    for i in range(k):
        score_id = 0
        score_ood = 0
        count_id = 0
        count_ood = 0
        for j in range(n):
            if predictions[j] == labels[i]:
                count_id += 1 - ood_ratio[j]
                count_ood += ood_ratio[j]
                if predictions[j] == ground_truth[j]:
                    score_id += 1 - ood_ratio[j]
                    score_ood += ood_ratio[j]
        precision_per_classs_id.append(score_id/count_id)
        precision_per_classs_ood.append(score_ood/count_ood)
    return precision_per_classs_id, precision_per_classs_ood

def calculate_recall_multiclass(predictions, ground_truth, labels, ood_ratio):
    n = len(predictions)
    recall_per_class_id = []
    recall_per_class_ood = []
    k = len(labels) 
    for i in range(k):
        score_id = 0
        score_ood = 0
        count_id = 0
        count_ood = 0
        for j in range(n):
            if ground_truth[j] == labels[i]:
                count_id += 1 - ood_ratio[j]
                count_ood += ood_ratio[j]
                if predictions[j] == ground_truth[j]:
                    score_id += 1 - ood_ratio[j]
                    score_ood += ood_ratio[j]
        recall_per_class_id.append(score_id/count_id)
        recall_per_class_ood.append(score_ood/count_ood)    
    return recall_per_class_id, recall_per_class_ood
    

def f1_score_multiclass(precision_value, recall_value):
    # n = len(precision_value)
    k = len(precision_value)
    f1_score_per_class = []
    for i in range(k):
        f1_score = (2*precision_value[i]*recall_value[i])/(precision_value[i] + recall_value[i])
        f1_score_per_class.append(f1_score)
    return f1_score_per_class


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prediction', type=str, required=True)
    parser.add_argument('--ground_truth', type=str, required=True)
    parser.add_argument('--ood_score_file', type=str, required=True)
    parser.add_argument('--labels', type=str, required=True)
    args = parser.parse_args()
    
    predicted_values = [] # ['chemical', 'disease', 'chemical', 'disease'] # load it from the file
    ground_values =  [] # ['chemical', 'chemical', 'chemical', 'disease'] # load it from the file
    labels = [] # ['chemical', 'disease']
    ood_score = [] # [0.2, 0.4, 0.7, 0.5]

    # Open the file and read each line
    with open(args.prediction, 'r') as file:
        for line in file:
            # Strip leading and trailing whitespaces and append to the list
            predicted_values.append(line.strip())
    
    # Open the file and read each line
    with open(args.ood_score_file, 'r') as file:
        for line in file:
            val = float(line.strip())
            ood_score.append(val)

    # Open the file and read each line
    with open(args.labels, 'r') as file:
        for line in file:
            # Strip leading and trailing whitespaces and append to the list
            labels.append(line.strip())

    # Open the file and read each line
    with open(args.ground_truth, 'r') as file:
        for line in file:
            # Strip leading and trailing whitespaces and append to the list
            ground_values.append(line.strip())

    print(predicted_values)
    print(ground_values)
    print(ood_score)
    print(labels)

    precision_id, precision_ood = calculate_precision_multiclass(predicted_values, ground_values, labels, ood_score)
    print(precision_id)
    print(precision_ood)
    recall_id, recall_ood = calculate_recall_multiclass(predicted_values, ground_values, labels, ood_score)
    print(recall_id)
    print(recall_ood)
    f1_score_id = f1_score_multiclass(precision_id, recall_id)
    f1_score_ood = f1_score_multiclass(precision_ood, recall_ood)
    print(f1_score_id)
    print(f1_score_ood)

    avg_precision_id = 0
    avg_precision_ood = 0
    avg_recall_id = 0
    avg_recall_ood = 0
    avg_f1_id = 0
    avg_f1_ood = 0
    k = len(precision_id)
    for i in range(k):
        avg_precision_id += precision_id[i]
        avg_precision_ood += precision_ood[i]
        avg_recall_id += recall_id[i]
        avg_recall_ood += recall_ood[i]
        avg_f1_id += f1_score_id[i]
        avg_f1_ood += f1_score_ood[i]
    
    avg_precision_id = avg_precision_id/k
    avg_precision_ood = avg_precision_ood/k
    avg_recall_id = avg_recall_id/k
    avg_recall_ood = avg_recall_ood/k
    avg_f1_id = avg_f1_id/k
    avg_f1_ood = avg_f1_ood/k

    print(f'average precision id : {avg_precision_id}')
    print(f'average precision ood : {avg_precision_ood}')
    print(f'average recall id : {avg_recall_id}')
    print(f'average recall ood : {avg_recall_ood}')
    print(f'average f1 score id : {avg_f1_id}')
    print(f'average f1 score ood : {avg_f1_ood}')

if __name__ == "__main__":
    main()