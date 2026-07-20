# Sample MSBA Statistics Notes

These notes are an original demonstration knowledge base. Replace or supplement them with the instructor's official course materials.

## 1. Populations, Samples, Parameters, and Statistics

A population is the complete set of units relevant to a question. A sample is the subset actually observed. A parameter is a numerical characteristic of a population, such as the population mean mu or population proportion p. A statistic is calculated from sample data, such as the sample mean x-bar or sample proportion p-hat. Statistics are used to estimate unknown parameters.

A good sample should represent the target population. Convenience samples, voluntary-response samples, and nonresponse can create selection bias. Increasing sample size reduces random sampling variation, but it does not repair a systematically biased sampling process.

## 2. Descriptive Statistics

The mean uses every observation and is sensitive to extreme values. The median is the middle ordered value and is resistant to outliers. The mode is the most frequent value and can be used with categorical data.

Range equals maximum minus minimum. Sample variance is the average squared deviation from the sample mean using n minus 1 in the denominator. Sample standard deviation is the square root of sample variance and is expressed in the original measurement units.

The interquartile range is IQR = Q3 - Q1. A common rule flags observations below Q1 - 1.5 IQR or above Q3 + 1.5 IQR as potential outliers. A flagged point is not automatically an error; it should be investigated in context.

The coefficient of variation is standard deviation divided by the mean, often expressed as a percentage. It can compare relative variability across positive variables measured on different scales, but it is not meaningful when the mean is near zero.

## 3. Probability Foundations

For events A and B, the addition rule is P(A or B) = P(A) + P(B) - P(A and B). If the events are mutually exclusive, P(A and B) = 0.

Conditional probability is P(A given B) = P(A and B) / P(B), provided P(B) is positive. Events A and B are independent when P(A given B) = P(A), equivalently P(A and B) = P(A)P(B). Mutually exclusive events with positive probabilities are not independent because occurrence of one prevents occurrence of the other.

The complement rule is P(not A) = 1 - P(A). The phrase "at least one" is often easiest to calculate as one minus the probability of none.

## 4. Random Variables and Expected Value

A discrete random variable takes countable values. Its probability distribution assigns a probability to each value, with all probabilities nonnegative and summing to one.

The expected value is a long-run probability-weighted average: E(X) = sum of x times P(X = x). The variance is E[(X - mu)^2], and the standard deviation is its square root. Expected value is not necessarily a value that can occur in one trial.

For a binomial random variable, there is a fixed number n of independent trials, each trial has two outcomes, and the success probability p is constant. The mean is np and the variance is np(1-p).

## 5. Normal Distribution and z Scores

A normal distribution is symmetric and determined by its mean and standard deviation. A z score standardizes an observation: z = (x - mu) / sigma. It reports how many standard deviations x lies above or below the mean.

For an approximately normal distribution, about 68 percent of observations lie within one standard deviation of the mean, about 95 percent within two, and about 99.7 percent within three. This empirical rule is an approximation, not a replacement for exact normal probabilities.

A percentile describes the percentage of observations at or below a value. A z score and a percentile are related but not identical: the z score is a standardized distance, while the percentile is a cumulative proportion.

## 6. Sampling Distributions and the Central Limit Theorem

A sampling distribution describes how a statistic varies across repeated random samples of the same size. The mean of the sampling distribution of x-bar equals the population mean. Its standard deviation, called the standard error, is sigma divided by the square root of n when the population standard deviation is known.

The central limit theorem states that, under suitable conditions, the sampling distribution of the sample mean becomes approximately normal as sample size grows, even when the population is not normal. Strong skewness or extreme outliers may require a larger sample.

Larger samples reduce standard error by the square-root rule. Multiplying sample size by four cuts the standard error approximately in half.

## 7. Confidence Intervals

A confidence interval has the general form point estimate plus or minus critical value times standard error. A 95 percent confidence level refers to the long-run performance of the method: if the sampling process were repeated many times, about 95 percent of intervals constructed by that method would contain the fixed population parameter.

It is usually incorrect to say there is a 95 percent probability that the already-computed interval contains the fixed parameter in the classical frequentist framework. The interval either contains the parameter or it does not; the 95 percent describes the procedure before sampling.

For a population mean with unknown population standard deviation, a t interval is commonly used: x-bar plus or minus t-star times s divided by square root n. The t distribution has heavier tails than the standard normal distribution. As degrees of freedom increase, it approaches the normal distribution.

Margin of error decreases when sample size increases or when the confidence level decreases. Higher confidence requires a wider interval when all other quantities are fixed.

## 8. Hypothesis Testing

A null hypothesis represents a baseline claim. The alternative hypothesis represents the direction of evidence being investigated. The test statistic measures how far the sample result lies from the null value in standard-error units.

The p value is the probability, assuming the null hypothesis and model assumptions are true, of obtaining a result at least as extreme as the observed result in the direction specified by the alternative. It is not the probability that the null hypothesis is true.

If the p value is less than or equal to the significance level alpha, reject the null hypothesis. Otherwise, fail to reject it. Failing to reject is not the same as proving the null hypothesis true.

A Type I error rejects a true null hypothesis; its probability is controlled by alpha. A Type II error fails to reject a false null hypothesis. Power is one minus the Type II error probability and represents the ability to detect a real effect of a specified size.

Statistical significance does not imply practical significance. A very large sample can make a small, operationally unimportant difference statistically significant. Report effect size and a confidence interval in addition to the p value.

## 9. Correlation and Simple Linear Regression

Correlation r measures the direction and strength of a linear association between two quantitative variables. It is unitless and lies between -1 and 1. Correlation does not establish causation and can be distorted by outliers, nonlinear patterns, or confounding variables.

Simple linear regression models the mean response as E(Y|X=x) = beta0 + beta1 x. The estimated line is y-hat = b0 + b1 x. The slope b1 estimates the expected change in the mean response associated with a one-unit increase in x.

A residual is observed minus predicted: e = y - y-hat. Least squares selects the line minimizing the sum of squared residuals, SSE. SST measures total variability around the sample mean, and SSR measures variability explained by the regression. The identity is SST = SSR + SSE when the model includes an intercept.

R-squared is SSR/SST = 1 - SSE/SST. It is the proportion of sample variation in Y explained by the fitted linear model with X. A high R-squared does not prove causality, guarantee accurate future predictions, or confirm that model assumptions hold.

Common regression assumptions concern linearity of the mean relationship, independence of errors, approximately constant error variance, and normality of errors for small-sample inference. Residual plots help assess linearity and constant variance. Extrapolation beyond the observed range of X can be unreliable.

## 10. Business Interpretation Checklist

When reporting a result, identify the population and variable, state the estimate with units, quantify uncertainty, and translate the conclusion into the decision context. Avoid saying "accept the null" or "prove." Explain what the evidence supports and what limitations remain.

For a confidence interval, report both endpoints and interpret the plausible range for the population parameter. For a test, report the hypotheses, test statistic, p value, decision at the stated alpha, and a contextual conclusion. For regression, interpret slope and R-squared carefully and discuss whether prediction or causal explanation is the goal.
