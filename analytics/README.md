Task 2 Missing Value Handling

Column	      Approx Missing	 Action
Embarked	   0.22%	         Drop rows
Embark_town    0.22%	         Drop rows
Age	           19.86%	         Median Imputation
Deck	       77%	             Drop Column

Interpretation

Mean > Median > Mode
Therefore Fare is Right Skewed.

Task 5 Data Story

Example
1.Survival vs Gender
2.Survival vs Passenger Class
3.Age vs Survival
4.Fare vs Survival
5.Pairplot
6.Heatmap

Justification

Stratification is important because survived contains two classes: passengers who survived and passengers who did not. The split should preserve approximately the same class proportions in both training and testing sets. Without stratification, a random split could produce a noticeably different class distribution, making model evaluation less reliable.

Why Stratify?

Maintains the same survival proportion in train and test datasets, preventing class imbalance from skewing model evaluation.

Interpretation

If the residuals are randomly scattered around zero with approximately constant spread, there is little evidence of heteroscedasticity.

If the plot shows a funnel-shaped pattern, where residual spread increases or decreases as predicted fare increases, that is evidence of heteroscedasticity.

Use what your actual residual plot shows rather than automatically claiming one or the other.

Recommendation :

Random Forest is typically the strongest performer because it captures non-linear relationships and interactions between features.
If it achieves the highest F1 score and AUC while maintaining balanced precision and recall, it is the preferred deployment model.
The complete preprocessing pipeline ensures consistent handling of raw input data during inference.
The saved pipeline can be directly reused without manually repeating preprocessing steps.

Your final recommendation should reference the actual numbers produced by your run.

For example:

Based on the evaluation results, Random Forest is recommended for deployment because it achieved the strongest overall F1 score and AUC among the three classifiers. Its precision and recall provide a good balance between correctly identifying survivors and minimizing incorrect predictions. Logistic Regression provides a useful interpretable baseline, while the Decision Tree provides an easily visualized set of decision rules. Therefore, Random Forest is preferred because its overall predictive performance is strongest on the held-out test set.

Replace the model name and metric values with your actual results.
