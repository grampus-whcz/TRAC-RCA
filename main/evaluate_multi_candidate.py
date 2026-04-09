import re
import itertools
from datetime import datetime

def time_difference(time1_str, time2_str):
    time_format = "%Y-%m-%d %H:%M:%S"
    try:
        time1 = datetime.strptime(time1_str, time_format)
        time2 = datetime.strptime(time2_str, time_format)
    except ValueError:
        return False
    diff = abs((time1 - time2).total_seconds())
    return diff <= 60

def evaluate_single_candidate(single_pred_dict, scoring_points):
    """
    Evaluate one candidate (dict) against scoring_points.
    Returns (passing_criteria, failing_criteria, bin_score)
    """
    # Extract from single prediction dict
    datetime_str = single_pred_dict.get("root cause occurrence datetime", "")
    component = single_pred_dict.get("root cause component", "")
    reason = single_pred_dict.get("root cause reason", "")

    # Build list of one prediction (as in original logic)
    predict_results = [{
        "root cause occurrence datetime": datetime_str,
        "root cause component": component,
        "root cause reason": reason
    }]

    # Parse scoring points
    component_pattern = r"The (?:\d+-th|only) predicted root cause component is ([^\n]+)"
    reason_pattern = r"The (?:\d+-th|only) predicted root cause reason is ([^\n]+)"
    time_pattern = r"The (?:\d+-th|only) root cause occurrence time is within 1 minutes \(i.e., <=1min\) of ([^\n]+)"

    components = re.findall(component_pattern, scoring_points)
    reasons = re.findall(reason_pattern, scoring_points)
    times = re.findall(time_pattern, scoring_points)

    scoringpoints_length = max(len(components), len(reasons), len(times))
    total_scores = len(components) + len(reasons) + len(times)

    if total_scores == 0:
        return [], [], 1.0  # No criteria → full score

    scores_get = 0
    passing_criteria = []
    failing_criteria = []

    # Only one prediction → no need for permutations
    if scoringpoints_length == 1:
        current_passing = []
        current_score = 0

        if components and component == components[0]:
            current_score += 1
            current_passing.append(components[0])
        if reasons and reason == reasons[0]:
            current_score += 1
            current_passing.append(reasons[0])
        if times and time_difference(times[0], datetime_str):
            current_score += 1
            current_passing.append(times[0])

        scores_get = current_score
        passing_criteria = current_passing

    else:
        # Fallback: if scoring expects >1 but we have only 1 pred → can't match order
        # So we try all permutations (though only one item, so trivial)
        best_score = -1
        best_passing = []
        for perm in itertools.permutations(predict_results):
            cur_score = 0
            cur_pass = []
            for i in range(min(scoringpoints_length, len(perm))):
                if i < len(components) and perm[i]['root cause component'] == components[i]:
                    cur_score += 1
                    cur_pass.append(components[i])
                if i < len(reasons) and perm[i]['root cause reason'] == reasons[i]:
                    cur_score += 1
                    cur_pass.append(reasons[i])
                if i < len(times) and time_difference(times[i], perm[i]['root cause occurrence datetime']):
                    cur_score += 1
                    cur_pass.append(times[i])
            if cur_score > best_score:
                best_score = cur_score
                best_passing = cur_pass
        scores_get = best_score
        passing_criteria = best_passing

    failing_criteria = list(set(components + reasons + times) - set(passing_criteria))
    final_score = scores_get / total_scores if total_scores > 0 else 1.0
    bin_score = round(final_score, 2)

    return passing_criteria, failing_criteria, bin_score


def evaluate_multi_candidate(prediction: str, scoring_points: str):
    import json

    try:
        pred_dict = json.loads(prediction)
    except json.JSONDecode迫Error as e:
        raise ValueError(f"Invalid JSON in prediction: {e}")

    results = {}

    # Pre-extract all scoring criteria for fallback failing list
    all_components = re.findall(r'The (?:\d+-th|only) predicted root cause component is ([^\n]+)', scoring_points)
    all_reasons = re.findall(r'The (?:\d+-th|only) predicted root cause reason is ([^\n]+)', scoring_points)
    all_times = re.findall(r'The (?:\d+-th|only) root cause occurrence time is within 1 minutes \(i.e., <=1min\) of ([^\n]+)', scoring_points)
    all_criteria = list(set(all_components + all_reasons + all_times))

    for key, value in pred_dict.items():
        required_keys = ["root cause occurrence datetime", "root cause component", "root cause reason"]
        if not all(k in value for k in required_keys):
            # Missing required fields → score 0, all criteria failed
            results[key] = ([], all_criteria, 0.0)
            continue

        res = evaluate_single_candidate(value, scoring_points)
        results[key] = res

    return results


# ===== Test =====
if __name__ == '__main__':
    # prediction = """{
    #   "1": {
    #     "Suspicious score": 0.95,
    #     "root cause occurrence datetime": "2021-03-04 13:30:00",
    #     "root cause component": "IG01",
    #     "root cause reason": "memory exhaustion (OOM) and garbage collection (GC) pressure observed, with log patterns indicating GC events at 13:39"
    #   },
    #   "2": {
    #     "Suspicious score": 0.95,
    #     "root cause occurrence datetime": "2021-03-04 13:54:00",
    #     "root cause component": "Redis01",
    #     "root cause reason": "Exhibited numerous container-level memory, CPU, and network anomalies along with rising MySQL query rates and cache updates, indicating it was under significant stress and likely contributed to the downstream impact on MySQL."
    #   },
    #   "3": {
    #     "Suspicious score": 0.95,
    #     "root cause occurrence datetime": "2021-03-04 13:58:00",
    #     "root cause component": "Redis01",
    #     "root cause reason": "Redis01 experienced evictions, rejected connections, and session rejections during the anomaly window, directly indicating high memory usage leading to service degradation."
    #   }
    # }"""

    prediction = """{
  "1": {
    "Suspicious score": 0.95,
    "root cause occurrence datetime": "2021-03-04 22:00:00",
    "root cause component": "IG01",
    "root cause reason": "high JVM CPU load and JVM Out of Memory (OOM) Heap due to excessive garbage collection activity causing system-level stress and cascading failures"
  }
}"""
    scoring_points = """The only predicted root cause component is Redis01"""

    results = evaluate_multi_candidate(prediction, scoring_points)

    for key, (passing, failing, score) in results.items():
        print(f"Candidate {key}: Passing={passing}, Failing={failing}, Score={score}")