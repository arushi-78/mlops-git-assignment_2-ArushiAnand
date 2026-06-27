# MAI201 MLOps: Assignment 2 Report
# Data Validation & Testing
**Student:** Arushi Anand  

## 1. GE Validation Results
<img width="940" height="438" alt="image" src="https://github.com/user-attachments/assets/a9e279eb-ee3a-459c-9860-1b95a3631164" />
## 2. Data Quality Issues Found
<img width="940" height="402" alt="image" src="https://github.com/user-attachments/assets/89c617d2-50da-44cd-9025-5f946de0d585" />
| Issue | Count |
|-------|------:|
| Total rows (expected 500–1000) | **5,015** |
| Null `customer_id` | 150 |
| Duplicate `customer_id` | 452 |
| Fully duplicate rows | 15 |
| Age out of range (< 0 or > 120) | 384 |
| Missing `age` | 147 |
| Invalid email format | 346 |
| Missing `email` | 438 |
| Missing `salary` (fails 95% rule) | 425 |
| Negative `salary` | 159 |
| Invalid `country` value | 301 |
| Missing `country` | 41 |
| Missing `phone` | 319 |
| Missing `signup_date` | 14 |


## 3. pytest Execution - All Tests Passing

<img width="442" height="362" alt="image" src="https://github.com/user-attachments/assets/6b7c7724-6881-47c7-9611-9ab27c198b92" />

29 tests collected and passed in 1.66 seconds across three test classes.

## 4. Reflection: Which Data Quality Issue Would Most Impact ML Model Performance?

**Missing and invalid `salary` values would cause the greatest harm to ML model performance.**

With 425 missing values (~8.5%) and 159 negative entries (~3.2%), nearly 12% of salary records are either absent or physically impossible. This creates two compounding problems:

**Imputation bias**: Standard strategies such as mean or median fill introduce systematic bias when missingness is not at random. If higher earners disproportionately omit their salary, mean imputation underestimates the feature for that segment, corrupting any downstream salary-based segmentation or prediction.

**Distribution corruption**: Negative salary values that slip through cleaning distort the feature distribution, corrupt normalisation statistics (mean, standard deviation), and destabilise gradient-based optimisers during training by producing extreme scaled values after normalisation.

By contrast, inconsistent phone number formats carry no predictive signal in a typical ML model. Fully duplicate rows can be safely dropped without distorting the learned distribution. Invalid country values (301 rows) affect a categorical feature that can be handled cleanly with an "Unknown" category. Salary corruption is harder to recover from because any imputed value is a fabrication of a continuous signal that directly influences model weights.
