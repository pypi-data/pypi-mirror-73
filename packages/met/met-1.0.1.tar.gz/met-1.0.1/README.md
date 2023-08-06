met.py
Multinomial Exact Tests

met.py is a Python module that allows you to define a pair of
multinomial distributions (conceptually 'control' and 'test'
distributions) and then compute one- and two-sided p values to test
whether the 'test' distribution is equivalent to the 'control'
distribution. The likelihood of all possible 'control' distributions can
be evaluated and the distribution of p values can be expressed in terms
of the likelihood of the observed 'control' distribution.


Installation
======================

You can install the module from [PyPi](https://pypi.org/) with the
command

    pip install met

or you can install in manually by downloading `met.py` and copying
the module to wherever you want to use it.  If you place it in a
location other than the standard library for your Python distribution,
you must add that location to your Python path prior to importing the
module.


Purpose
======================

Perform exact tests of a (site or test) distribution of multinomial
count data against a distribution of equivalent ordered multinomial
count data from another (reference or control) data set. Both two-sided
and one-sided tests can be performed. One-sided tests require that
categories be ordered.

A practical example of relevant data (and the motivation for writing
this module) arises from the use of Sediment Profile Imaging to evaluate
the benthic macroinvertebrate community at site and reference locations,
and characterization of each sample in terms of the benthic successional
stage presen. These categorical data are ordered, and so a one-sided
exact multinomial test can be applied.


Notes
======================

Exact Tests
--------------------

Whereas most statistical tests compute p values based on the parameters
of a continuous distribution, and those p value are therefore
estimates, calculation of exact p values is possible when every
possible rearrangement of the data can be enumerated. Each 
rearrangement of the data must have a specific probability of
occurrence, which is computed based on a theoretical or reference
distribution of probabilities.  Summing of the probabilities of
occurrence for the observed data and for all more extreme arrangments of
the data produces an exact p value--hence, the result of an exact test.

For two-sided tests, "more extreme" means that the probability of an alternative
arrangement of site data has a lower probability than the observed arrangement.

For one-sided tests, "more extreme" means a data arrangement in which
one or more observations is shifted from a 'better' category to a
'worse' one. Therefore, to carry out one-sided exact tests, the
categories must be ordered from 'better' to 'worse'.

Issues
--------------------

When reference area sample sizes are small relative to site sample
sizes, the accuracy of the probabilities calculated from the reference
area samples may be questionable.  In particular, some categories that
are represented in the site data may not be represented in the reference
data, and so have zero reference aera probabilities.  Whenever a
reference area probability for any category is zero, the probability of
any arrangement of site data with a non-zero count in that category is
also zero.  Small reference area sample sizes may therefore lead to
underestimation of true reference probabilities for some categories, and
consequently to an underestimation of p values in the exact tests.

The met module contains two features to help evaluate and account for
uncertainties related to relatively small reference area sample sizes. 
The first of these allows assignment of small non-zero probabilities to
categories with no reference area observations, and the second allows
evaluation of the likelihood of different p values based on possible
reference area probabilities that could have led to the observed
reference data.

Example
======================

This example illustrates the computation of one-sided and two-sided *p* values, with
and without zeroes in the reference distribution.
import met

    # Counts observed in the reference area, ordered from 'best' to 'worst'
    # category. For SPI data, the categories are Stage 3, Stage 2 on 3,
    #			Stage 1 on 3, Stage 2, and Stage 1.

    ref = [9, 6, 6, 0, 5]

    # Counts observed in the site.
    # These are skewed toward an impacted distribution.
    # Counts are low for speed of illustration.
    site = [10, 12, 14, 5, 6]


    # MET with zeroes in the reference distribution.

    t1 = met.Multinom(ref, site)

    t1_p1 = t1.onesided_exact_test(save_cases=True)
    print("Example 1 with no zero-fill; one-sided p = %s" % t1_p1)
    print("    Number of extreme cases = %s" % t1.n_extreme_cases)

The results are shown as:

    Example 1 with no zero-fill; one-sided p = 0.00634738889819
        Number of extreme cases = 63348

Although there are zero probabilities in the reference area distribution, a non-zero
one-sided probability is calculated because some of the more extreme distributions
(i.e., skewed further from the reference distribution than the actual size) have zeroes
in the same category.

Calculation of a two-sided p value:

    t1_p2 = t1.twosided_exact_test(save_cases=True)
    print("Example 1 with no zero-fill; two-sided p = %s" % t1_p2)
    print("    Number of cases = %s" % len(t1.cases))
    print("    Number of extreme_cases = %s" % t1.n_extreme_cases)

The result is:

    Example 1 with no zero-fill; two-sided p = 0.0
        Number of cases = 249900
        Number of extreme_cases = 0

The zero probabilities in the reference distribution prevent the calculation of a two-sided
*p* value. The multinomial probability for the site itself is zero, and the two-sided test sums
that with the multinomial probabilities of all of the (249,900) other possible results for the
site that are less probable than the observed site data.

Specifying a 'zero-fill' value results in a different p value for both the one-sided and
two-sided tests.

    # MET with zeros replaced with 1 and non-zeroes inflated by 10.

    t2 = met.Multinom(met.fillzeroes(ref, 10), site)

    t2_p1 = t2.onesided_exact_test()
    t2_p2 = t2.twosided_exact_test()

    print("Example 2 with a zero-fill factor of 10; one-sided p = %s, two-sided p = %s" % (t2_p1, t2_p2))

The result is:

    Example 2 with a zero-fill factor of 10; one-sided p = 0.0070346, two-sided p = 1.95908e-06

    A larger fill factor results in different calculated probabilities.
    # MET with zeros replaced with 1 and non-zeroes inflated by 100.

    t3 = met.Multinom(met.fillzeroes(ref, 100), site)

    t3_p1 = t3.onesided_exact_test()
    t3_p2 = t3.twosided_exact_test()

    print("Example 3 with a zero-fill factor of 100; one-sided p = %s, two-sided p = %s" % (t3_p1, t3_p2))

The result is:

    Example 3 with a zero-fill factor of 100; one-sided p = 0.0064139, two-sided p = 1.73424e-11



Copyright and License
======================

Copyright (c) 2009, 2019 R.Dreas Nielsen

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version. This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details. The GNU General Public License is available at
http://www.gnu.org/licenses/.
