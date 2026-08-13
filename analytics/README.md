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

Why Stratify?

Maintains the same survival proportion in train and test datasets, preventing class imbalance from skewing model evaluation.

Interpretation

Random scatter indicates homoscedasticity.

A funnel shape indicates heteroscedasticity.

Recommendation :

Random Forest is typically the strongest performer because it captures non-linear relationships and interactions between features.
If it achieves the highest F1 score and AUC while maintaining balanced precision and recall, it is the preferred deployment model.
The complete preprocessing pipeline ensures consistent handling of raw input data during inference.
The saved pipeline can be directly reused without manually repeating preprocessing steps.