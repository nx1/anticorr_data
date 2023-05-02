echo "==============================="
echo "Running table_closest_srcreg.py"
echo "==============================="
python3 table_closest_srcreg.py

echo "==============================="
echo "Running table_host_distances.py"
echo "==============================="
python3 table_host_distances.py

echo "==============================="
echo "Running table_obs_counts_XRT.py"
echo "==============================="
python3 table_obs_counts_XRT.py

echo "================================"
echo "Running table_obs_counts_UVOT.py"
echo "================================"
python3 table_obs_counts_UVOT.py
