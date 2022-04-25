import numpy as np
import os
import matplotlib.pyplot as plt
import argparse
import sys


def readPCCURVE(file="PCCURVE.qdp", minExposure=0, minSigma=0, minSNR=0):
    """Read PCCURVE from Swift data pipeline.

        Parameters
        ----------
        file: str, optional
            The file to be read. Default is PCCURVE.qdp
        minExposure : float, optional
            Minimum exposure to consider
        minSigma : float, optional
            Minimum Sigma to consider.
        minSNR: float, optional
            Minimum SNR to consider.
        """
    print("Reading data from %s" % file)
    try:
        data = np.genfromtxt("%s" % file, names=True, delimiter="\t", skip_header=2, comments="!", dtype=("f8, f8, f8, f8, f8, f8, f8, f8, f8, f8, i8, f8, f8, f8, f8, U30"))
    except ValueError:
        data = np.genfromtxt("%s" % file, names=True, delimiter="\t", skip_header=2, comments="!", dtype=("f8, f8, f8, f8, f8, f8, f8, f8, f8, f8, i8, f8, f8, f8, f8"))
    filtered_data = data[(data["Exposure"] > minExposure) & (data["SNR"] > minSNR) & (data["Sigma"] > minSigma)]
    filtered_obs = len(data) - len(filtered_data)
    print("Filtered %d datapoints by minSNR = %d" % (filtered_obs, minSNR))
    return filtered_data


def readPCHR(file="PCHR.qdp", minSoftSig=0, minHardSig=0, reject_errors=True, minExposure=0):
    """Read PCHR from Swift data pipeline.

        Parameters
        ----------
        file: str, optional
            The file to be read. Default is PCHR.qdp
        minSoftSig : float, optional
            Minimum soft signal to filer. Default is 0.
        minHardSig : float, optional
            Minimum hard signal to filer. Default is 0.
        reject_errors : boolean, optional
            Whether to reject data points with errors higher than the data point value. Default is True.
        """
    print("Reading %s data" % file)
    try:
        data = np.genfromtxt("%s" % file, names=True, delimiter="\t", skip_header=2, comments="!", dtype=("f8, f8, f8, f8, f8, f8, f8, f8, f8, f8, f8, f8, f8, U30"))
    except ValueError:
        data = np.genfromtxt("%s" % file, names=True, delimiter="\t", skip_header=2, comments="!", dtype=("f8, f8, f8, f8, f8, f8, f8, f8, f8, f8, f8, f8, f8"))
    if reject_errors is True:
        filtered_data = data[(~np.isnan(data["HR"])) & (data["HR"] > 0) & (data["SoftSig"] > minSoftSig) & (data["HardSig"] > minHardSig) & (data["HRerr"] < data["HR"]) & (data["Exposure"] > minExposure)]
    else:
        filtered_data = data[(~np.isnan(data["HR"])) & (data["HR"] > 0) & (data["SoftSig"] > minSoftSig) & (data["HardSig"] > minHardSig) & (data["Exposure"] > minExposure)]
    print("Filtered %d datapoints" % (len(data) - len(filtered_data)))
    return filtered_data


ap = argparse.ArgumentParser(description='Cluster data points based on HR and count rate')
ap.add_argument("-hr", "--hr", nargs='+', help="List of HR ranges i.e. 0.5:2.0")
ap.add_argument("-c", "--countrate", nargs='+', help="List of count rate ranges i.e. 2.0:2.0 3.0:5.0", type=str)
ap.add_argument("-i", "--input_file", nargs='?', help="Input file with HR and count rates to split data", type=str, default="segregation.txt")
args = ap.parse_args()


if args.hr is None:
    if os.path.isfile(args.input_file):
        segregation_info = np.genfromtxt(args.input_file, names=True, dtype=("U22, U22"), delimiter="\t", deletechars="")
        print(segregation_info)
        hr_ranges = segregation_info["HR"]
        count_rate_ranges = segregation_info["countrates"]
else:
    hr_ranges = args.hr
    count_rate_ranges = args.countrate
    if len(hr_ranges) != len(count_rate_ranges):
        print("Error number of hr ranges has to be equal to countrate ranges")
        sys.exit()

count_rate_file = "PCCURVE.qdp"
hr_file = "PCHR.qdp"
if os.path.isfile(count_rate_file) and os.path.isfile(hr_file):

    data_count_rate = readPCCURVE(count_rate_file)
    data_hr = readPCHR(hr_file)
    print("Found %d swift observations in %s" % (len(data_count_rate), count_rate_file))
    print("Found %d swift observations in %s" % (len(data_hr), hr_file))
    fig, ax = plt.subplots(1, 1)
    # select only common obsid
    common_obs, common_1, common_2 = np.intersect1d(data_count_rate["Time"], data_hr["Time"], return_indices=True)
    print("Found %d common observations" % len(common_obs))
    data_count_rate = data_count_rate[common_1]
    data_hr = data_hr[common_2]
    chunk_counter = 1
    colors = ["orange", "green", "blue", "yellow", "olive", "purple"]
    #ax.errorbar(data_hr["HR"], data_count_rate["Rate"],
    #            xerr=data_hr["HRerr"], yerr=[-data_count_rate["Rateneg"],
    #            data_count_rate["Ratepos"]], ls="None", fmt="-", color="black", marker="+")

    string_out = "#HR\tcountrate\tobsids\n"
    for hr_range, count_range, color in zip(hr_ranges, count_rate_ranges, colors):
        print("Filtering by %s HR values and %s count rate values" % (hr_range, count_range))
        string_out += "%s\t%s\t" % (hr_range, count_range)
        hr_range = hr_range.split(":")
        count_rate_range = count_range.split(":")
        # filter by count rate
        count_rate_chunk = data_count_rate[(data_count_rate['Rate'] >= float(count_rate_range[0])) & (data_count_rate['Rate'] <= float(count_rate_range[1]))]
        # filter by hr
        hr_chunk = data_hr[(data_hr['HR'] >= float(hr_range[0])) & (data_hr['HR'] <= float(hr_range[1]))]
        common_chunk_obs, indexes_1, indexes_2 = np.intersect1d(hr_chunk["Time"], count_rate_chunk["Time"], return_indices=True)
        final_hr = hr_chunk[indexes_1]
        final_countrate = count_rate_chunk[indexes_2]
        print("Obsids for chunk 1 (total %d/%d)" % (len(common_chunk_obs), len(data_count_rate)))
        obsstring = ""
        for row in final_hr:
            obs = str(row["Obsid"])
            print(obs)
            obsstring += "%s," % obs.split("::ObsID=")[1]
            string_out += "%s," % obs.split("::ObsID=")[1]
        print(obsstring)
        ax.errorbar(final_hr["HR"], final_countrate["Rate"],
                    xerr=final_hr["HRerr"], yerr=[-final_countrate["Rateneg"],
                    final_countrate["Ratepos"]], ls="None", fmt="-", color=color, marker="+")
        chunk_counter += 1
        string_out += "\n"
    file = open("segregation_out.txt", "w")
    file.write(string_out)
    file.close()
