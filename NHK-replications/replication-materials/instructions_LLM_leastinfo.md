# Research Task

## Research Question

Among ethnically Hispanic-Mexican Mexican-born people living in the United States, what was the causal impact of eligibility for the Deferred Action for Childhood Arrivals (DACA) program (treatment) on the probability that the eligible person is employed full-time (outcome), defined as usually working 35 hours per week or more?

DACA was implemented in 2012. Examine the effects on full-time employment in the years 2013-2016. 

## Background

DACA is a program enacted in the United States on June 15, 2012. The program, enacted by the US federal government, allowed a selected set of undocumented immigrants, who had arrived unlawfully in the US, to apply for and obtain authorization to work legally for two years without fear of deportation. Because the program offers legal work authorization, and also allows recipients to apply for drivers’ licenses or other identification in some states, we might expect that the program would increase employment rates among those eligible.

People were eligible for the program if they:

- Arrived unlawfully in the US before their 16th birthday
- Had not yet had their 31st birthday as of June 15, 2012
- Lived continuously in the US since June 15, 2007
- Were present in the US on June 15, 2012 and did not have lawful status (citizenship or legal residency) at that time

Additional background notes:
- Applications for the program started to be received on August 15, 2012, and in the [first four years](https://www.uscis.gov/sites/default/files/document/data/daca_performancedata_fy2016_qtr3.pdf) nearly 900,000 initial applications were received, about 90% of which were approved.
- After the initial two years of work authorization and deportation relief, people could reapply for an additional two years, which many did.
- While the program was not specific to immigrants from any origin country, because of the structure of undocumented immigration to the United States, the great majority of eligible people were from Mexico.

## Data

Data for analysis will come from the American Community Survey (ACS) as provided by [IPUMS USA](https://usa.ipums.org/usa/acs.shtml), in addition to a provided supplemental file of state demographic and policy information. Please do not retrieve any other data for analysis other than what's in [usa_00042.dat](usa_00042.dat) and [policy_labor_market_data.csv](policy_labor_market_data.csv) (the latter is described in [State-Level Data Documentation.md](State-Level Data Documentation.md)). You are not required to use any of the supplemental state-level information, but may do so.

The data were constructed as follows:
- Using “USA Samples”
- Using only the one-year ACS files (these just say “ACS” instead of “ACS 3yr” or “ACS 5yr” or the older census files that say “5% state” and so on)
- Not using any files newer than 2016. 
- Not using any files older than 2006. This is to avoid data definition inconsistencies, and to ensure that the variables necessary for identifying DACA eligibility are all present. You are not required to use all files back to 2006, but will not be using any older than that. 
- On the “Select Variables” page, only Harmonized Variables were selected
- See use_00042.cbk for a plain-text codebook of the data. usa_00042.do is the Stata do-file that can be used to read the raw usa_00042.dat file into Stata as well as understand the underlying data structure; usa_00042.xml provides an alternative xml-formatted codebook.

- DACA eligibility and whether someone was Hispanic and born in Mexico can be determined using:
    - Census year (included in data extract by default)
    - Birth year and quarter (Person -> Demographic)
    - Hispanic-Mexican ethnicity, birthplace, citizenship, and year of immigration (Person -> Race, Ethnicity, and Nativity)
    - We cannot distinguish in the data between documented and undocumented non-citizens. Assume that anyone who is not a citizen and who has not received immigration papers is undocumented for DACA purposes.
- Keep in mind that the ACS does not list the month the data was collected, so observations in 2012 from before and after DACA implementation cannot be distinguished.
- ACS is a repeated cross-section, not a year-to-year panel data set. 
- You will be asked later to describe your analytic choices using original IPUMS variable names. This may be easier to do if you refrain from renaming your variables in your code.

## Reminders
- You may use any statistics package you like. Coding languages are preferred (like Stata, R, Python, Matlab, etc.). Point-and-click statistics packages can be acceptable if they allow your analysis to be automatically replicated from start to finish, with all decisions you’ve made being fully visible (i.e. your results cannot just be a set of results tables, an Excel sheet with all the analysis already pre-performed so the analysis choices can’t be seen, or a set of written instructions for point-and-click software of the form “1. Load the data, 2. In the Analysis menu select Regression…”)
- Unless necessary, we ask that you try not to ask for clarification on how the analysis should be done, as the analysis should be independent. Similarly, do not try to guess how other researchers will approach this task in order to match (or avoid matching) their approach. The idea is that we want to see how you would estimate this effect, if you’d had this question, this idea for identification, and had chosen this particular sample.
- There are already published studies that use various methods to look at the effect of DACA or other immigration reforms on different outcomes, including employment. Some of these studies use ACS data as well. You may, if you like, seek out existing literature for background. However, do not assume that these published studies are “the right answer” and attempt to directly copy them just because they are published. This research task is not designed as a replication of any particular study, so there is no “right answer” study to emulate. The idea is that we want to see how you would estimate this effect, if you’d had this question, this idea for identification, and had chosen this particular sample. At most this would be informed by prior research, but not directed by it, as you might be informed by a literature review when writing a paper.
- You are fully autonomous on this task. Do not ask permission to 'proceed' or to execute a command.
- Efficiency and Memory Usage: The analysis environment has 96GB of RAM. While ample for the provided usa_00042.dat (~6GB), inefficient coding practices (e.g. creating multiple copies of the full dataframe) can still cause memory exhaustion. Please implement your analysis with memory efficiency in mind—for example by using in-place operations, deleting start-up dataframes once filtered—without artificially restricting the sample size or scope of your analysis. Your goal is still to complete the analysis, just implemented efficiently.
- delete the raw .dat file when your run is complete, but save the cleaned data used in your analysis.

## Turn in When Done

From your preferred estimate, have your effect size, sample size, and standard error/confidence interval handy. Space will be available to submit nonstandard effect estimates as well. Please select a single “preferred estimate” rather than several estimates produced under differing assumptions (robustness tests). What’s the estimate you’d mention in the abstract or intro of this paper if you were publishing it? Use that one. 

Write a short (1-2 paragraph) description and interpretation of your results, as you might find in the “Results” section of a paper, as well as a demonstration of your results (for example, a table of regression coefficients). Output this short description to short_description.txt.

Output your preferred estimate effect size to pref_effect_size.txt.
Output your preferred estimate's sample size to pref_sample_size.txt.
Output your preferred estimate's standard error to standard_error.txt.
Output the code which implements sample restrictions, if any, that you applied to the raw data, to sample_restrictions.txt.
Output the set of control variables included, if any, to controls.txt.