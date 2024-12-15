import numpy as np
from scipy.signal import correlate
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean


def compare_events_dtw(event_stats1, event_stats2, max_time_difference):
    comparison_results = []
    matched_event2_ids = {}

    for event1 in event_stats1:
        best_match = None
        best_distance = np.inf
        
        for event2 in event_stats2:
            if abs(event1['start_time'] - event2['start_time']) <= max_time_difference:
                data1 = event1['normalized_event_data'].values.reshape(-1, 1)
                data2 = event2['normalized_event_data'].values.reshape(-1, 1)
                distance, _ = fastdtw(data1, data2, dist=euclidean)

                if distance < best_distance:
                    best_distance = distance
                    best_match = event2

        if best_match:
            event2_id = best_match['event_id']

            # Check if the event2_id is already matched
            if event2_id not in matched_event2_ids or best_distance < matched_event2_ids[event2_id]['dtw_distance']:
                # Update the best match for this event2_id
                matched_event2_ids[event2_id] = {
                    'event1_id': event1['event_id'],
                    'dtw_distance': best_distance,
                    'event1_min_value_index': event1['min_value_index'],
                    'event1_max_value_index': event1['max_value_index'],
                    'event2_min_value_index': best_match['min_value_index'],
                    'event2_max_value_index': best_match['max_value_index']
                }

    # Prepare final results by iterating over the matched events
    for event2_id, result in matched_event2_ids.items():
        comparison_results.append({
            'event1_id': result['event1_id'],
            'best_match_event2_id': event2_id,
            'dtw_distance': result['dtw_distance'],
            'event1_min_value_index': result['event1_min_value_index'],
            'event1_max_value_index': result['event1_max_value_index'],
            'event2_min_value_index': result['event2_min_value_index'],
            'event2_max_value_index': result['event2_max_value_index']
        })
    return comparison_results


def compare_events_cca(event_stats1, event_stats2):
    # signals must be same frequency
    # resample must be done before event extraction already
    pass
