
import datetime

import numpy as np
import pandas as pd
import pickle as pkl
import pytplot as ptt
import matplotlib.pyplot as plt

import pyspedas as spd
from pyspedas.mms.mms_load_brst_segments import mms_load_brst_segments
brst_start, brst_end = mms_load_brst_segments(trange=['2015-01-16', '2023-09-01'])

# # Convert brst_start from unix time to datetime
brst_start_datetime = np.array([datetime.datetime.utcfromtimestamp(t) for t in brst_start])
brst_end_datetime = np.array([datetime.datetime.utcfromtimestamp(t) for t in brst_end])

# Set the time zone to UTC
brst_start_datetime = np.array([t.replace(tzinfo=datetime.timezone.utc) for t in brst_start_datetime])
brst_end_datetime = np.array([t.replace(tzinfo=datetime.timezone.utc) for t in brst_end_datetime])

# Compute the length of each interval in seconds
brst_interval_length = brst_end - brst_start

# Save the start and end times and the interval lengths to a csv file
df = pd.DataFrame({'start_time': brst_start_datetime, 'end_time': brst_end_datetime, 'interval_length': brst_interval_length})
df.to_csv("brst_intervals.csv", index=False)



mms_fpi_varnames = ['mms3_dis_bulkv_gse_brst']

trange = ['2017-09-01 09:58:30', '2017-09-01 09:59:30']
_ = spd.mms.fpi(trange=trange, probe=3, data_rate='brst', level='l2',
                datatype='dis-moms', varnames='mms3_dis_bulkv_gse_brst', time_clip=True,
                latest_version=True)
fpi_time_unix = ptt.get_data(mms_fpi_varnames[0])[0]
fpi_v_gse = ptt.get_data(mms_fpi_varnames[0])[1:][0]

fpi_time_utc = spd.time_datetime(fpi_time_unix)
# Set the time zone to UTC
fpi_time_utc = np.array([t.replace(tzinfo=datetime.timezone.utc) for t in fpi_time_utc])

print(f"Start time: {fpi_time_utc[0].strftime('%Y-%m-%d %H:%M:%S')}")
print(f"End time: {fpi_time_utc[-1].strftime('%Y-%m-%d %H:%M:%S')}")

# Find the closest time in the brst_start_datetime array to the start time of the FPI data
brst_start_datetime_closest = brst_start_datetime[np.argmin(np.abs(brst_start_datetime - fpi_time_utc[0]))]
brst_end_datetime_closest = brst_end_datetime[np.argmin(np.abs(brst_end_datetime - fpi_time_utc[-1]))]

print(f"Closest start time: {brst_start_datetime_closest.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Closest end time: {brst_end_datetime_closest.strftime('%Y-%m-%d %H:%M:%S')}")

# Read the pickle file
with open("pydata/mms_brst_intervals.pickle", "rb") as f:
    brst_intervals = pkl.load(f)

brst_start_datetime_pkl = np.array([datetime.datetime.utcfromtimestamp(t) for t in brst_intervals["start_times"]])
brst_end_datetime_pkl = np.array([datetime.datetime.utcfromtimestamp(t) for t in brst_intervals["end_times"]])

# Set the time zone to UTC
brst_start_datetime_pkl = np.array([t.replace(tzinfo=datetime.timezone.utc) for t in brst_start_datetime_pkl])
brst_end_datetime_pkl = np.array([t.replace(tzinfo=datetime.timezone.utc) for t in brst_end_datetime_pkl])

diff_start = brst_start_datetime[:] - brst_start_datetime_pkl
diff_end = brst_end_datetime[:] - brst_end_datetime_pkl

# Find the indices where the start and end times are different by more than 1 second
idx_start = np.where(np.abs(diff_start) > datetime.timedelta(seconds=1))[0]
idx_end = np.where(np.abs(diff_end) > datetime.timedelta(seconds=1))[0]

# Print the number of times the start and end times are different by more than 1 second
print(f"Number of start times different by more than 1 second: {np.sum(np.abs(diff_start) > datetime.timedelta(seconds=1))}")
print(f"Number of end times different by more than 1 second: {np.sum(np.abs(diff_end) > datetime.timedelta(seconds=1))}")

ttt = [str(ttt.strftime('%Y-%m-%d %H:%M:%S')) for ttt in brst_start_datetime_pkl[idx_start]]
# On a time series plot, plot the start and end times that are different by more than 1 second

plt.figure(figsize=(12, 8))
plt.plot(ttt, diff_start[idx_start], "b.", label="Start time")

#plt.plot(brst_end_datetime_pkl[idx_end], diff_end, "r.", label="End time")
plt.legend()
plt.ylabel("Difference (s)")
plt.title("Difference between start times in the pickle file and the start times from the SPDAS server")
plt.show()
"""

# Find the indices where the differences between brst_start_datetime and brst_end_datetime are
# greater than 10 minutes
idx = np.where(np.abs(brst_start_datetime - brst_end_datetime) > datetime.timedelta(minutes=3))[0]

# Print the brst_start_datetime and brst_end_datetime where the difference is greater than 10 minutes
# as a couplet
for i in idx:
    print(f"[{brst_start_datetime[i].strftime('%Y-%m-%d %H:%M:%S')}, {brst_end_datetime[i].strftime('%Y-%m-%d %H:%M:%S')}]")
