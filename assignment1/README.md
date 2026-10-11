# AML 3303 — Assessment 1

## Delivery Delay Prediction & Slack Alerts

**Weight:** 20% of final grade

## Project overview

MapleFreight Logistics moves approximately 8,000 shipments each week across Ontario, Quebec, and the Prairies. Its on-time performance has fallen from 94% to 88%, and dispatch often learns about delays only after a delivery window has passed.

This project analyzes shipment data, predicts which in-transit shipments are at risk of arriving late, and sends high-risk alerts to a Slack dispatch channel.

## Objectives

- Explore shipment, route, and carrier data to identify factors associated with late deliveries.
- Build and evaluate a model that predicts late deliveries.
- Compare the final model against a baseline.
- Send useful, timely alerts to Slack for high-risk shipments.
- Recommend actions to help improve on-time performance.

## Dataset

The dataset, `maplefreight_delivery_delay_dataset.csv`, contains **6,035 shipments** and **23 columns**. The target is `delivered_late`:

- `1` — the shipment missed its promised delivery window.
- `0` — the shipment arrived on time.

Approximately 21% of shipments are late. A model that predicts every shipment will arrive on time would achieve about 79% accuracy, so accuracy alone is not a suitable measure of model performance.

The raw export may contain missing values, duplicate records, inconsistent category spellings, and unit errors.

### Data dictionary

| Column                      | Type     | Description                                                |
| --------------------------- | -------- | ---------------------------------------------------------- |
| `shipment_id`               | Text     | Unique shipment reference                                  |
| `origin_city`               | Category | Pickup city and province                                   |
| `destination_city`          | Category | Delivery city and province                                 |
| `carrier`                   | Category | Carrier handling the shipment, including owner-operators   |
| `service_level`             | Category | Express, Standard, or Economy                              |
| `goods_type`                | Category | General freight, refrigerated, fragile, hazardous, or bulk |
| `customer_priority_tier`    | Category | Gold, Silver, or Bronze account                            |
| `shipment_month`            | Integer  | Pickup month, from 1 to 12                                 |
| `distance_km`               | Numeric  | Route distance in kilometres                               |
| `weight_kg`                 | Numeric  | Shipment weight                                            |
| `num_stops`                 | Integer  | Intermediate stops on the route                            |
| `is_cross_border`           | Binary   | Whether the shipment crosses into the United States        |
| `scheduled_transit_hours`   | Numeric  | Transit time promised to the customer                      |
| `pickup_delay_minutes`      | Numeric  | Minutes late at pickup; negative values mean early         |
| `driver_experience_years`   | Numeric  | Assigned driver's years of experience                      |
| `vehicle_age_years`         | Numeric  | Age of the assigned vehicle                                |
| `weather_condition`         | Category | Dispatch forecast: clear, rain, fog, snow, or storm        |
| `traffic_index`             | Numeric  | Route traffic congestion at dispatch, from 0 to 100        |
| `route_congestion_score`    | Numeric  | Historical route congestion, from 0 to 1                   |
| `prior_late_deliveries_30d` | Integer  | Carrier's late deliveries in the previous 30 days          |
| `fuel_cost_cad`             | Numeric  | Estimated trip fuel cost                                   |
| `actual_transit_hours`      | Numeric  | Actual transit time, recorded on delivery                  |
| `delivered_late`            | Binary   | Target: 1 if the shipment missed its promised window       |

> **Prediction-time note:** `actual_transit_hours` is recorded after delivery and is not available when a prediction is made. Exclude it from model features to avoid target leakage.

## Project workflow

The notebook follows an end-to-end machine learning workflow:

1. Define the business problem and objectives.
2. Inspect and understand the data.
3. Explore patterns and potential delay drivers.
4. Clean and preprocess the data.
5. Engineer and prepare model features.
6. Train a baseline and compare candidate models.
7. Evaluate precision, recall, F1, and the confusion matrix.
8. Explain the model's results.
9. Select and justify an alert threshold.
10. Send Slack alerts and provide operational recommendations.

Each section should include relevant code, output, and a brief written finding.

## Running the project

1. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Make the dataset available at the path expected by the notebook.

3. Create a `.env` file in the project root and add your Slack Incoming Webhook URL:

   ```env
   SLACK_WEBHOOK_URL=your_webhook_url_here
   ```

4. Open the notebook and run it from a clean kernel, from top to bottom.

**Never commit `.env` or display the webhook URL in notebook output.** The repository should include `.env.example` with a placeholder value and `.gitignore` should exclude `.env`.

## Slack alerts

The notebook sends a message to the `#dispatch-alerts` Slack channel when shipments meet the selected risk threshold. Each alert should show the number of at-risk shipments and list the top shipments with their ID, destination, carrier, and risk score.

A screenshot of the Slack notification should be saved as `screenshots/slack_alert.png`.

## Model results

Complete this section after running the notebook.

| Model       |    Precision |       Recall |           F1 | Confusion matrix |
| ----------- | -----------: | -----------: | -----------: | ---------------- |
| Baseline    | [Add result] | [Add result] | [Add result] | [Add result]     |
| Final model | [Add result] | [Add result] | [Add result] | [Add result]     |

**Selected alert threshold:** [Add threshold]

**Why this threshold was selected:** [Explain the trade-off between catching late shipments and generating false alarms.]

## Key findings and recommendations

Add the most important findings from the notebook. For example, describe the strongest delay-related factors and how dispatch or carrier teams could respond.

- **Key finding:** [Add finding]
- **Key finding:** [Add finding]
- **Recommendation:** [Add actionable recommendation]

## AI usage

**AI assistant(s) used:** [Name the tools used, or write “None”.]

**One case where an AI suggestion was incorrect or needed correction:** [Describe the suggestion and how you verified or corrected it.]

## Repository contents

| File or folder                                           | Purpose                                               |
| -------------------------------------------------------- | ----------------------------------------------------- |
| `MapleFreight_Delivery_Delay_Prediction_<your_id>.ipynb` | Complete notebook with outputs                        |
| `README.md`                                              | Project overview, results, instructions, and AI usage |
| `screenshots/slack_alert.png`                            | Evidence of the Slack notification                    |
| `requirements.txt`                                       | Python dependencies                                   |
| `.gitignore`                                             | Excludes secrets such as `.env`                       |
| `.env.example`                                           | Webhook variable name with a placeholder value        |
| Dataset or dataset link                                  | Data used by the notebook                             |

## Submission

Submit the link to your **public GitHub repository**. This assessment is an individual assignment.
