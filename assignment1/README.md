# AML 3303 — Assessment 1

## Delivery Delay Prediction & Slack Alerts

**Weight:** 20% of final grade

## Project overview

MapleFreight Logistics moves approximately 8,000 shipments each week across Ontario, Quebec, and the Prairies. Its on-time performance has fallen from 94% to 88%, and dispatch often learns about delays only after a delivery window has passed.

This project analyzes shipment data, predicts which in-transit shipments are at risk of arriving late, and formats a Slack alert with the number of high-risk shipments and the top five shipment details.

## Objectives

- Explore shipment, route, and carrier data to identify factors associated with late deliveries.
- Build and evaluate a model that predicts late deliveries.
- Compare the final model against a baseline.
- Send a Slack alert for shipments whose predicted late risk meets the validation-selected pilot threshold.
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

> **Prediction-time note:** This notebook predicts after dispatch, once `pickup_delay_minutes` is available, to flag in-transit risk. `actual_transit_hours` is recorded after delivery and is excluded to avoid target leakage.

## Project workflow

The notebook follows an end-to-end machine learning workflow:

1. Define the business problem and objectives.
2. Inspect and understand the data.
3. Explore patterns and potential delay drivers.
4. Clean and preprocess the data.
5. Prepare model features and document feature-engineering hypotheses for future testing.
6. Train a baseline and compare candidate models.
7. Evaluate precision, recall, F1, and the confusion matrix.
8. Explain the model's results.
9. Select a pilot alert threshold from five-fold out-of-fold training predictions and evaluate it once on the held-out test set.
10. Format high-risk shipment details for a Slack alert and provide operational recommendations.

The analysis sections pair code and outputs with brief interpretation. Feature-engineering items are hypotheses for future validation, not experiments completed in this run.

## Running the project

1. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Place `maplefreight_delivery_delay_dataset.csv` in the `assignment1` folder, alongside the notebook, and run the notebook with `assignment1` as its working directory.

3. From the repository root, copy `assignment1/.env.example` to `assignment1/.env` and replace the placeholder with your Slack Incoming Webhook URL:

   ```env
   SLACK_WEBHOOK_URL=your_webhook_url_here
   ```

4. Open the notebook and run it from a clean kernel, from top to bottom.

**Never commit `.env` or share the webhook URL.** The repository's `.gitignore` excludes `.env`; `.env.example` is a safe placeholder.

## Slack alerts

The notebook formats a `HIGH-RISK SHIPMENT ALERT` for the `#dispatch-alerts` channel when one or more shipments meet the pilot cutoff. It includes the total number flagged and the five highest-risk shipment IDs, destinations, carriers, and estimated risk scores. Configure `SLACK_WEBHOOK_URL` in `.env` to send it; without a webhook, the notebook prints a preview. The current example scores the held-out test rows as a retrospective dispatch simulation, not a live shipment feed.

The required alert evidence is `screenshots/slack_alert.png`: it shows 259 test-set shipments over the 65% pilot cutoff and the five highest-risk shipment details. The older `Screenshot from 2026-10-10 20-07-43.png` shows a training-completed message, and `Screenshot from 2026-10-10 21-05-13.png` shows model metrics; those historical messages are not shipment-risk alerts.

## Model results

Results from the current stratified train/test run at the standard `0.50` classifier cutoff:

| Model                            | Weighted precision | Weighted recall | Weighted F1 | ROC AUC | Confusion matrix          |
| -------------------------------- | -----------------: | --------------: | ----------: | ------: | ------------------------- |
| Majority-class baseline          |              0.631 |           0.794 |       0.703 |   0.500 | `[[935, 0], [242, 0]]`    |
| Unweighted logistic regression   |              0.818 |           0.834 |       0.814 |   0.820 | `[[894, 41], [154, 88]]`  |
| Balanced logistic regression     |              0.822 |           0.748 |       0.768 |   0.822 | `[[697, 238], [59, 183]]` |
| Logistic regression with SMOTENC |              0.791 |           0.715 |       0.738 |   0.789 | `[[678, 257], [79, 163]]` |

Metrics are weighted averages; for balanced logistic regression, late-class precision is 0.435 and recall is 0.756. Confusion matrices use actual classes as rows and predictions as columns.

**Pilot alert threshold:** `0.65`, selected by maximizing late-class F2 ($\beta=2$, weighting recall more heavily) across five-fold out-of-fold training predictions, subject to a minimum late-class precision of `0.50`. The precision floor is an explicit pilot guardrail: at least half of alerts should be correct; it is not a measured dispatch-capacity or dollar-cost constraint. The standard `0.50` cutoff remains in the results for comparison.

At `0.65`, out-of-fold training precision is `0.530`, recall is `0.571`, and F2 is `0.562`. On the held-out test set, precision is `0.525`, recall is `0.562`, with 136 late shipments caught, 106 missed, and 123 false alerts (confusion matrix `[[812, 123], [106, 136]]`). The alert flags 259 test-set shipments. At the default `0.50`, test recall is higher (`0.756`) but precision is lower (`0.435`) and there are 238 false alerts.

The held-out test set was not used to choose the cutoff. Preprocessing is refit inside each CV fold. The threshold is still a provisional pilot choice from one random split, not a production setting; confirm it with dispatch capacity and later-period data before operational use.

## Key findings and recommendations

After excluding 150 shipments with missing weather, 5,885 rows remain, including 1,209 late shipments (20.5%). Distance and scheduled transit time show a positive association in the predictor-only correlation matrix. Weight has an extreme maximum of 2,999,300 kg against a median of 827.1 kg and needs source/unit verification. Balanced logistic regression had the highest late-class recall (0.756) and ROC AUC (0.822) among the valid candidates compared here; SMOTENC scored lower on both (0.674 recall, 0.789 ROC AUC). These are associations and one-split results, not evidence of causation or guaranteed savings.

- **Data quality:** Service-level casing was normalized; investigate extreme weight values at the source and confirm their units rather than relying only on clipping.
- **Model trade-off:** Balanced logistic regression misses fewer late shipments than the unweighted version at the default cutoff, but it creates more false alerts.
- **Recommendation:** Pilot post-dispatch alerts at the validation-selected cutoff, monitor missed delays and alert volume, and revisit the precision floor with dispatch before production use. No financial savings are claimed.

## AI usage

**AI assistant used:** GitHub Copilot in VS Code.

**How I used it:** I used Copilot iteratively to understand class weighting, leakage, scaling, preprocessing, model evaluation, the correlation matrix, ROC AUC versus a decision threshold, and operational trade-offs. It also helped organize and explain the notebook. At my request, Copilot used a read-only subagent to cross-check the disclosure facts; it did not edit files.

**My work and AI-assisted additions:** I wrote the original data-loading, data-cleaning, preprocessing, and balanced logistic-regression code and made the original model adjustments. After I explicitly authorized additions, Copilot reconstructed a historical leakage demonstration from our conversation because the earlier work was uncommitted; this was a reconstruction, not a recovery of a committed version. Copilot also helped add the predictor-only correlation heatmap and numeric summaries, majority baseline, unweighted/balanced and SMOTENC comparisons, ROC/AUC plots, an 18-cutoff threshold sweep with false-negative/false-positive analysis, an optional cost chart gated on agreed inputs, the local scorecard, and an initial conditional Slack model-update cell that was later replaced by the per-shipment risk alert. It drafted explanatory text and recommendations as well. I reviewed the additions and remain responsible for the final analysis and conclusions; it would not be accurate to say that every cell in the submitted notebook was written solely by me.

**Mistakes and corrections:**

- **Edited code after a review-only request:** When I asked for review and explanation of scaling/clipping, Copilot changed the existing model cell and added ROC/AUC code without permission. The first edit also clipped weights after scaling and calculated separate clipping limits for train and test; its first run hit a pandas integer-dtype assignment error. I objected to the scope change. Those preprocessing problems were later corrected: bounds are learned on training data, reused on test data, and applied before scaling.
- **Inaccurate review findings:** Copilot said the missing-value count used `.count()`, although the notebook used `.isna().sum()`, which was correct. Its duplicate-count concern was valid: the filtered `.count()` returns per-column counts rather than one scalar. Later, despite my saying that training medians and training-derived clipping bounds were already reused for test data, Copilot incorrectly reported that the test set used its own median and quantiles. The final model uses training-derived statistics.
- **Wrong Python environment:** My shell was active in a different course project's environment. Copilot initially installed modeling dependencies there; after I told it to use this repository's `uv` environment, it removed the packages it had just added to the other environment and installed them in this repository's `.venv`.
- **Misread class notes:** Copilot initially treated my class notes as feature-engineering material. I clarified that the class notes should remain a separate section and feature-engineering ideas should be hypotheses to test; the notebook was reorganized accordingly.
- **Notebook-save and overwrite handling:** Copilot reported a notebook edit as saved while the old unconditional Slack training-message cell was still on disk, then had to verify and replace it with the conditional model-update cell. A later JSON serialization rewrite triggered VS Code's external-overwrite warning. Comparing the current notebook with the staged copy confirmed that no cells, source, outputs, execution counts, or ordering were lost; the difference was serialization/formatting only.
- **Incomplete earlier disclosure and README mismatch:** Earlier AI-use wording did not list these mistakes and blurred my original work with Copilot's additions. The README also briefly described individual shipment-risk Slack alerts and required an `.env.example` that was not present. I corrected the disclosure; the current submission now includes the per-shipment alert, the safe webhook template, and documentation of the actual behavior.

**Clarified project decision:** I first discussed a pre-dispatch prediction, then later chose post-dispatch/post-pickup prediction, where `pickup_delay_minutes` is available. The final notebook and README reflect that later decision and exclude post-delivery `actual_transit_hours`. Copilot also clarified that ROC AUC `0.822` is a ranking metric, not a probability threshold; the selected pilot cutoff comes from training-only cross-validation, while the threshold sweep reports held-out test trade-offs. No production threshold or unsupported CAD savings claim is made.

**Recommendations developed with AI:** Verify the extreme weight and category inconsistencies with their data sources; test proposed feature formulas using validation data; and choose any alert threshold using validation results plus dispatch capacity and defensible error-cost estimates. No dollar savings were estimated because the dataset supplies no agreed false-negative or false-positive costs.

**Where it appears:** The AI-assisted cells and related explanations are in the notebook's EDA, historical leakage demonstration, preprocessing/model comparison, threshold, scorecard, and conditional Slack sections. This README records the assistance and corrections in detail.

## Repository contents

| File or folder                                         | Purpose                                                                   |
| ------------------------------------------------------ | ------------------------------------------------------------------------- |
| `MapleFreight_Delivery_Delay_Prediction_0960408.ipynb` | Analysis notebook with outputs                                            |
| `README.md`                                            | Project overview, results, instructions, and AI usage                     |
| `screenshots/slack_alert.png`                          | Required high-risk shipment alert evidence                              |
| `screenshots/` timestamped PNGs                        | Historical training and model-metrics messages                          |
| `.env.example`                                         | Safe Slack webhook configuration template                                 |
| `requirements.txt`                                     | Python dependencies                                                       |
| `.gitignore`                                           | Excludes secrets such as `.env`                                           |
| `maplefreight_delivery_delay_dataset.csv`              | Shipment data used by the notebook                                        |

## Submission

Submit the link to your **public GitHub repository**. This assessment is an individual assignment.
