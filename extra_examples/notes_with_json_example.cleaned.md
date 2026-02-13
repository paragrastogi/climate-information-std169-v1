# README - v2 development

## Notes on committee discussions / decisions

1. Is Enthalpy a candidate for deletion?
1. Compound element names: convention for compounds like "Mean/standard deviation of extreme annual minimum/maximum dry-bulb temperature". Should mean come first, i.e., `mean_minimum`, or minimum first, i.e., `minimum_mean`?. **mean minimum selected**
For example, 
    1. `dry_bulb_temperature` --> `month` --> `mean_minimum` means the mean of the minimum monthly dry bulb temperature values over the period of record.
    1. `dry_bulb_temperature` --> `annual` --> `mean_maximum` means the mean of the maximum annual dry bulb temperature values over the period of record.
1. Should we use `fractional_exceedance` instead of `percent_exceedance`? **No**
1. There is no point to supporting daily values. Rather, we want to suppor "design day".

1. For optical depth, where should the word "pseudo" exist?
1. Confidence intervals: how do we support them for each number/quantity? Decide whether to support an arbitrary range and how to express confidence level (confidence level vs confidence interval vs "n-sigma").
1. Derived data handling: support/define variables but make them optional; guidelines/structure for extensibility/custom; or create an auxiliary data model.
1. Derived variables: include them in the base model vs only in a model for a specific use case?
    1. "ASHRAE flavour model": Some variables are excluded from the base data model so far because they are derivable. Examples: Hottest/Coldest Month (derivable); *WSF* (ASHRAE 62.2 specific?); Return periods (derivable, see Chpt. 14); Range (derivable).
    1. Return periods: decision is NO (as of 19 Dec 2025). Notes should include references to calculation method. Consider whether to rename to corresponding probability; whether to show that probabilities are calculated using a mixture of the empirical distribution (mean, std) and a nominal distribution (Gumbel); and whether to parameterize or explicitly support this.
1. Align name of precipitation to that decided in v1 of consensus doc. Review all variable names to ensure consistency.
1. Should source_data_type have a different enumeration than that for time series (DIRECT_MEASUREMENT, DERIVED_MEASUREMENT, MODELED, something else)?
1. Should climate_data_type use a different enumeration table: only historical and projected?

## Publication Rules

1. Climate zone object refers to list of climate zone classifications that are applicable to this location ONLY, not necessarily applicable to a "nearby" site.
1. List of monthly elements must be ordered.
1. Data providers are encouraged to include calculations for each statistic in schema notes and, preferably, reference original source.
1. 

## Application Rules


## Public review notes/questions

1. Are there any other specific variables, calculations, or use cases that you would like to see supported? For example, are specific variables required for designing district heating/cooling networks not covered here?
*1. Which use cases should be covered by this schema? We don't need to make everything explicit in the data model itself, individual data providers are encourage to provide more documentation and details for users.*
1. Which "products" are required to make this work usable, apart from the data model (schema) itself: "helpers", data output examples (e.g., ASHRAE data), etc.
1. The committee felt it was not essential to include support for trends in the data model (ref: ASHRAE design conditions table). Do you agree?
1. Is there a need to support design days? The committee didn't see a point to supporting "daily" values, i.e., 365 days. Do you agree?
1. The committee suggests that variables that are derived from one or more measured variables with a deterministic calculation should not be included in the base data model. Rather, the data model can provide guidelines on expandability, so data providers can pre-calculate the derived variables for specific "flavours" of output, e.g., to complete ASHRAE design data table you would need to add: 
    1. Enthalpy
    1. Ranges
    1. Return periods
    1. ...

# Next steps
1. Parag to clean up above list of questions / concerns / etc. Separate out pending committee decisions (e.g., source data type) from "public review questions"
1. Parag to clean up example file (up to a point). Decisions needed on "null" vs "omitted" - when if any should we enforce null.
1. Volunteers (Parag/Neal/Sagar) to write schema
1. Draft public review survey, share with IBPSA, CIBSE, ASHRAE 4.1, 4.7, JSHA, etc.
1. IBPSA newsletter draft by end of Feb. If missed, next opportunity October publication. Survey needs to be ready - actual model files ready by end of March.
1. 
