# State-Level Information

The [file](policy_labor_market_data.csv) contains information on labor market and policy differences at the state-year level from 2006 to 2016. The `statename`, `state_fips`, and `year` columns identify the state (or District of Columbia) name and the year, and can be used to connect this data to the ACS data. This file also contains a `CensusRegion` variable indicating which of the four main Census regions the state belongs to.

## Policy Variables

These variables all refer to different laws and policies, enacted on the state level, that are likely to make it easier or more difficult for undocumented workers to find employment. Data comes from the [Urban Institute](https://www.urban.org/features/state-immigration-policy-resource). That link also contains more information about the specific policies.

### DRIVERSLICENSES
Is there a policy in place to allow undocumented immigrants to get state drivers’ licenses (either normal licenses or alternative versions)?
- **0** = No
- **1** = Yes

### INSTATETUITION
Can undocumented immigrants who meet certain requirements (usually, attending a certain number of years of an in-state high school system) receive in-state tuition at the state’s public colleges? In-state tuition is typically much lower than out-of-state tuition.
- **0** = No
- **1** = Yes

### STATEFINANCIALAID
Can undocumented immigrants who meet certain requirements (usually, attending a certain number of years of an in-state high school system) receive financial aid for college from the state?
- **0** = No
- **1** = Yes

### HIGHEREDBAN
Are undocumented immigrants banned from attending the state’s public colleges?
- **0** = No
- **1** = Yes

### EVERIFY
This refers to state-level E-Verify laws, which help or require that employers verify the work authorization of new hires. This policy constitutes a barrier to working for undocumented immigrants.
- **0** = No E-Verify Mandate
- **1** = Employers required to use E-Verify for some hires
- **2** = Employers required to use E-Verify for all hires

### LIMITEVERIFY
In addition to some states not having an E-Verify mandate, some states block local governments like cities or counties from implementing their own E-Verify mandates. This policy prevents local governments from imposing an E-Verify barrier to working for undocumented immigrants.
- **0** = No limit to local governments imposing E-Verify mandates
- **1** = Local governments in the state may not impose their own E-Verify mandates

### OMNIBUS
This refers to the State Omnibus Immigration Legislation and Legal Challenges described on [this website](https://www.ncsl.org/research/immigration/omnibus-immigration-legislation.aspx#State_Omnibus). These policies vary across states but in general increase enforcement of immigration law, by forcing immigrants to carry immigration registration documents, requiring law enforcement to verify immigration status during traffic stops, and creating penalties for harboring immigrants who were in violation of immigration law.
- **0** = No Omnibus policy
- **1** = Omnibus policy in place

### TASK287G
287(g) policies allow local law enforcement to perform certain functions of federal immigration law, increasing the number of law enforcement agencies that can enforce immigration laws. `TASK287G` indicates that either the state or most high-immigration counties in the state have a 287(g) task force arrangement in place allowing local law enforcement to do things like access federal immigration databases and detain individuals for immigration violations. The task force model was ended in 2012.
- **0** = None of the counties in the state with the most immigrants had a 287(g) task force agreement
- **1** = Some of the counties in the state with the most immigrants had a 287(g) task force agreement
- **2** = All of the counties in the state with the most immigrants had a 287(g) task force agreement

### JAIL287G
287(g) policies allow local law enforcement to perform certain functions of federal immigration law, increasing the number of law enforcement agencies that can enforce immigration laws. `JAIL287G` indicates that either the state or most high-immigration counties in the state have a 287(g) arrangement in place to perform immigration enforcement in jails.
- **0** = None of the counties in the state with the most immigrants had a 287(g) jail agreement
- **1** = Some of the counties in the state with the most immigrants had a 287(g) jail agreement
- **2** = All of the counties in the state with the most immigrants had a 287(g) jail agreement

### SECURECOMMUNITIES
Is Secure Communities active in this state in this year? Through Secure Communities, fingerprints submitted by local law enforcement agencies to the FBI are shared with immigration enforcement agencies for checks against immigration databases. Depending on the result, immigration officials decide whether to take enforcement action, such as issuing a detainer request. This program ran from 2008 to 2014, and was reinstated in 2017. From 2012 through 2014 the program was mandatory and was active in all states.
- **0** = No
- **1** = Yes

## Labor Market Data

These variables refer to certain labor market conditions in each state each year. Data comes from the [Bureau of Labor Statistics](https://download.bls.gov/pub/time.series/la/). These statistics are for the state as a whole, and are not specific to immigrants.

### UNEMP
This is the state unemployment rate, on a scale from 0 to 100. For example, a value of 6 indicates that the unemployment rate in the state in that year is 6%.

### LFPR
This is the labor force participation rate, on a scale from 0 to 100. For example, a value of 65 indicates that the labor force participation rate in that state in that year is 65%.
