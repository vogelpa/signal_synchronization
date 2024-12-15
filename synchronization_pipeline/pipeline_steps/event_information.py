def extract_event_information(data, events, signal_column, normalization_window_duration, time_column='time'):
    event_stats = []
    for event in events:
        indices = event['indices']
        start_time = data[time_column].iloc[indices[0]]
        normalization_window_start = start_time - normalization_window_duration

        normalization_window_data = data[(data[time_column] >= normalization_window_start) & 
                                    (data[time_column] <= data[time_column].iloc[indices[-1]])][signal_column]

        if len(normalization_window_data) > 0:
            mean = normalization_window_data.mean()
            std = normalization_window_data.std()
        else:
            mean = data[signal_column].mean()
            std = data[signal_column].std()

        event_data = data[signal_column].iloc[indices]
        normalized_event_data = (event_data - mean) / std
        min_value_idx = event_data.idxmin()
        max_value_idx = event_data.idxmax()

        event_stats.append({
            'event_id': event['event_id'],
            'normalized_event_data': normalized_event_data,
            'start_index': indices[0],
            'start_time': start_time,
            'min_value_index': min_value_idx,
            'max_value_index': max_value_idx
        })
    return event_stats
