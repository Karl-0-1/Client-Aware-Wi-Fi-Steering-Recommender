# Client-Aware-Wi-Fi-Steering-Recommender

This project simulates a "client-aware" Wi-Fi steering mechanism, a core part of modern mesh Wi-Fi and enterprise wireless systems. It demonstrates the logic used for 802.11k/v-style client roaming.

The project consists of two main scripts:
1.  `generate_data.py`: A utility script to synthesize a fake dataset of client connection reports.
2.  `recommender.py`: The main analysis script that parses the data and suggests optimal AP roams to improve client quality of experience (QoE).

---

## How to Run

1.  **Generate the data:**
    First, run the data generator to create the `client_reports.csv` file.
    ```bash
    python generate_data.py
    ```

2.  **Run the recommender:**
    Once the data is generated, run the main analysis script.
    ```bash
    python recommender.py
    ```

---

## Example Output

Running the recommender will parse the CSV and print a list of suggested actions for clients with poor connections.
