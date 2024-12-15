# event_detection/event_identification.py
def identify_events(data, outlier_flags, time_column, threshold=0.5, min_outlier_percentage=0.6):
    events = []
    event_id = 1
    n = len(data)

    i = 0
    while i < n:
        if outlier_flags[i]:
            start_time = data[time_column].iloc[i]
            end_time = start_time + threshold
            current_event = set()

            while i < n:
                interval_points = data.index[(data[time_column] > start_time) & (data[time_column] <= end_time)].tolist()
                outlier_count = sum(outlier_flags[interval_points])
                if len(interval_points) > 0 and outlier_count / len(interval_points) >= min_outlier_percentage:
                    current_event.update(interval_points)
                    i = i + 1
                    if i < n:
                        end_time = data[time_column].iloc[i] + threshold
                else:
                    i = i + max(1, len(interval_points)) # max to ensure loop terminates
                    break

            if len(current_event) > 0:
                current_event = sorted(current_event)
                event_duration = data[time_column].iloc[current_event[-1]] - data[time_column].iloc[current_event[0]]
                if event_duration >= threshold:
                    events.append({'event_id': event_id, 'indices': current_event})
                    event_id += 1
                i += 1
        else:
            i += 1

    return events
