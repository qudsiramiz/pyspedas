import pandas as pd
import datetime
import numpy as np

jet_detection_times = pd.read_csv("/home/cephadrius/Desktop/git/rxn_location/data/study_data/mms_jet_reversal_times_list_20221027_beta_brst.csv", index_col=False)

jet_times = jet_detection_times["Date"].values
# Remove milliseconds
jet_times = [t[:-6] for t in jet_times]
jet_times_datetime = np.array([datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f") for t in jet_times])

# Set the time zone to UTC
jet_times_datetime = np.array([t.replace(tzinfo=datetime.timezone.utc) for t in jet_times_datetime])

brst_intervals = pd.read_csv("brst_intervals.csv", index_col=False)

brst_start_datetime = np.array([datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S%z") for t in brst_intervals["start_time"]])
brst_end_datetime = np.array([datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S%z") for t in brst_intervals["end_time"]])

# Set the time zone to UTC
brst_start_datetime = np.array([t.replace(tzinfo=datetime.timezone.utc) for t in brst_start_datetime])
brst_end_datetime = np.array([t.replace(tzinfo=datetime.timezone.utc) for t in brst_end_datetime])


brst_start_datetime_closest = []
brst_end_datetime_closest = []
# For each jet_times_datetime, find the closest brst_start_datetime
for jet_time in jet_times_datetime:
    brst_start_datetime_closest.append(brst_start_datetime[np.argmin(np.abs(brst_start_datetime - jet_time))])
    brst_end_datetime_closest.append(brst_end_datetime[np.argmin(np.abs(brst_end_datetime - jet_time))])

brst_start_datetime_closest = np.array(brst_start_datetime_closest)
brst_end_datetime_closest = np.array(brst_end_datetime_closest)

# Find the time interval between the jet_times_datetime and the closest brst_start_datetime
time_interval_start = jet_times_datetime - brst_start_datetime_closest
time_interval_end = jet_times_datetime - brst_end_datetime_closest

# Convert the time intervals to seconds
time_interval_start = np.array([t.total_seconds() for t in time_interval_start])
time_interval_end = np.array([t.total_seconds() for t in time_interval_end])

# Print the 5, 10, 15, 20, 25, 30, 35, 40, 45, and 50th percentiles of the time intervals
print(np.percentile(time_interval_start, [5, 10, 15, 25, 50, 75, 85, 90, 95]))
print(np.percentile(time_interval_end, [5, 10, 15, 25, 50, 75, 85, 90, 95]))
'''
    print(f"Jet time: {jet_time}")
    print(f"Closest start time: {brst_start_datetime_closest}")
    print(f"Closest end time: {brst_end_datetime_closest}")

brst_end_datetime_closest = brst_end_datetime[np.argmin(np.abs(brst_end_datetime - jet_times_datetime))]

# Find the time interval between the jet_times_datetime and the closest brst_start_datetime
time_interval_start = jet_times_datetime - brst_start_datetime_closest
time_interval_end = jet_times_datetime - brst_end_datetime_closest

# Convert the time intervals to seconds
time_interval_start = np.array([t.total_seconds() for t in time_interval_start])
time_interval_end = np.array([t.total_seconds() for t in time_interval_end])


# Save the closest start and end times to a csv file along with the jet times
df = pd.DataFrame({'jet_times': jet_times_datetime, 'brst_start_datetime_closest': brst_start_datetime_closest, 'brst_end_datetime_closest': brst_end_datetime_closest, 'time_interval_start': time_interval_start, 'time_interval_end': time_interval_end})

df.to_csv("brst_intervals_closest.csv", index=False)

'''