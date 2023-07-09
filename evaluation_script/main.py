import random
import json
import evaluate as eval
import sklearn



def evaluate(test_annotation_file, user_submission_file, phase_codename, **kwargs):
    print("Starting Evaluation.....")
    """
    Evaluates the submission for a particular challenge phase and returns score
    Arguments:

        `test_annotations_file`: Path to test_annotation_file on the server
        `user_submission_file`: Path to file submitted by the user
        `phase_codename`: Phase to which submission is made

        `**kwargs`: keyword arguments that contains additional submission
        metadata that challenge hosts can use to send slack notification.
        You can access the submission metadata
        with kwargs['submission_metadata']

        Example: A sample submission metadata can be accessed like this:
        >>> print(kwargs['submission_metadata'])
        {
            'status': u'running',
            'when_made_public': None,
            'participant_team': 5,
            'input_file': 'https://abc.xyz/path/to/submission/file.json',
            'execution_time': u'123',
            'publication_url': u'ABC',
            'challenge_phase': 1,
            'created_by': u'ABC',
            'stdout_file': 'https://abc.xyz/path/to/stdout/file.json',
            'method_name': u'Test',
            'stderr_file': 'https://abc.xyz/path/to/stderr/file.json',
            'participant_team_name': u'Test Team',
            'project_url': u'http://foo.bar',
            'method_description': u'ABC',
            'is_public': False,
            'submission_result_file': 'https://abc.xyz/path/result/file.json',
            'id': 123,
            'submitted_at': u'2017-03-20T19:22:03.880652Z'
        }
    """
    with open(user_submission_file, "r") as test_file_object:
        test_data = json.load(test_file_object)
    with open(test_annotation_file, "r") as ground_truth_file_object:
        ground_truth_data = json.load(ground_truth_file_object)
    test_dict = {item: test_data[item] for item in test_data}
    ground_truth_dict = {item: ground_truth_data[item] for item in ground_truth_data}
    tp = 0  # True positives
    fp = 0  # False positives
    fn = 0  # False negatives

    for id, test_emotion in test_dict.items():
        ground_truth_emotion = ground_truth_dict.get(id)
        if ground_truth_emotion is not None:
            if test_emotion == ground_truth_emotion:
                tp += 1
            else:
                fp += 1
        else:
            fn += 1
    
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * (precision * recall) / (precision + recall)
    acc = precision
    # print(precision, recall, f1, acc)

    output = {}
    if phase_codename == "dev":
        print("Evaluating for Dev Phase")
        output["result"] = [
            {
                "train_split": {
                    "F1": f1,
                    "Accuracy": acc,
                }
            }
        ]
        # To display the results in the result file
        output["submission_result"] = output["result"][0]["train_split"]
        print("Completed evaluation for Dev Phase")
    elif phase_codename == "test":
        print("Evaluating for Test Phase")
        output["result"] = [
            # {
            #     "train_split": {
            #         "F1": f1,
            #         "Accuracy": acc,                }
            # },
            {
                "test_split": {
                    "F1": f1,
                    "Accuracy": acc,
                }
            },
        ]
        # To display the results in the result file
        output["submission_result"] = output["result"][0]
        print("Completed evaluation for Test Phase")
    return output
