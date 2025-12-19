# Notes

1. Climate zone object refers to list of climate zone classifications that are applicable to this location ONLY, not necessarily applicable to a "nearby" site.
1. List of monthly elements must be ordered.
1. Enthalpy is a candidate for deletion.
1. Compound element names
    1. What should be the convention when dealing with compounds such as "Mean and standard deviation of extreme annual minimum and maximum dry-bulb tem-
perature". Should mean come first (`mean_minimum`) or minimum (`minimum_mean`).
    1. Monthly or annual mean-minimum means mean of monthly/annual minimums over the period of record. Maximum is analogous. Monthly and annual are analogous. [A.1.1.3.b]   
1. Put calculations for each statistic in schema notes and/or reference Std. 169 notes.
1. ~Should `percent_exceedance` be called `inverse_quantile` or `complementary_quantile`?~ Should we use `fractional_exceedance` instead of `percent_exceedance`?
1. Should we retain `return periods`? - NO (as of 19 Dec 2025) - Notes to include references to calculation method
    1. Rename them to their corresponding probability?
    1. Since the probabilities are calculated using a mixture of the empirical distribution (mean, std) and a nominal distribution (Gumbel), should we just show this in the notes?
    1. Can/should we parametrise this?
    1. Explicitly support?
1. What is your use case - we don't need to make everything explicit in the data model itself.
1. What are the products - data model itself, "helpers", data output examples, e.g., ASHRAE data, etc.
1. How do we support confidence intervals? FOR EACH NUMBER / QUANTITY.
    1. Should we support an arbitrary range?
    1. How should we support the confidence level? - Confidence level, confidence interval, "n-sigma" number
1. For optical depth - where should the word "pseudo" exist?
1. Derived data - how should they be handled?
    1. Support/define the variables but make them optional
    1. Guidelines or structure for extensibility / custom
    1. Make an auxiliary data model
