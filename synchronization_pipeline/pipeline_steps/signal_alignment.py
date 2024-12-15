# event_detection/signal_alignment.py
import pandas as pd

def align_signals(df1, df2, comparison_results, sensor1, sensor2, dtw_distance_threshold, time_column='time'):
    df1['sync_point'] = pd.NA
    df2['sync_point'] = pd.NA

    previous_match = None
    original_df2 = df2.copy()
    for result in comparison_results:
        if result['dtw_distance'] is not None and result['dtw_distance'] < dtw_distance_threshold:
            
            # for sensomative, if min index before max idx on accelereometer, match with max idx senso, with min idx accelero
            # else match with min idx from senso with max? idx from accelero
            # if sensor1 == 'accelerometer' and sensor2 == 'sensomative':
            if sensor2 == 'sensomative':
                if result['event1_min_value_index'] < result['event1_max_value_index']:
                    event1_synch_index = result['event1_min_value_index']
                    event2_synch_index = result['event2_max_value_index']
                else:
                    event1_synch_index = result['event1_max_value_index']
                    event2_synch_index = result['event2_min_value_index']

            # elif (sensor1 == 'sensomative' and sensor2 == 'accelerometer'):
            elif sensor1 == 'sensomative':
                if result['event2_min_value_index'] < result['event2_max_value_index']:
                    event1_synch_index = result['event1_max_value_index']
                    event2_synch_index = result['event2_min_value_index']
                else:
                    event1_synch_index = result['event1_min_value_index']
                    event2_synch_index = result['event2_max_value_index']
            else:
                event1_synch_index = result['event1_min_value_index']
                event2_synch_index = result['event2_min_value_index']
           
            df1.at[event1_synch_index, 'sync_point'] = 1
            df2.at[event2_synch_index, 'sync_point'] = 1

            event1_synch_time = df1[time_column].iloc[event1_synch_index]
            event2_synch_time = df2[time_column].iloc[event2_synch_index]
            
            if previous_match is None:
                time_shift = event1_synch_time - event2_synch_time
                df2[time_column] += time_shift
            else:
                prev_event1_index = previous_match['event1_synch_index']
                prev_event2_index = previous_match['event2_synch_index']
                prev_event1_time = df1[time_column].iloc[prev_event1_index] # fetch anew because df2 has been changed
                prev_event2_time = df2[time_column].iloc[prev_event2_index]
                curr_event1_time = event1_synch_time
                curr_event2_time = event2_synch_time

                stretch_factor = (curr_event1_time - prev_event1_time) / (curr_event2_time - prev_event2_time)
                
                df2.loc[(df2[time_column] > prev_event2_time), time_column] = \
                    prev_event2_time + (df2[time_column] - prev_event2_time) * stretch_factor
                
            previous_match = {
                'event1_synch_index': event1_synch_index,
                'event2_synch_index': event2_synch_index             
            }    
    return original_df2, df2
