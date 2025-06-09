A data-driven framework for an efficient block-level coastal flood

risk assessment

Farnaz Yarveysia,b, Keighobad Jafarzadegana,b, Shrabani S. Tripathya,b,

Hamed Moftakharia,b, Hamid Moradkhania,b,*

aCenter for Complex Hydrosystems Research, University of Alabama, 1030 Cyber Hall, Tuscaloosa, 35487, AL, USA

bDepartment of Civil, Construction, and Environmental Engineering, 1030 Cyber Hall, Tuscaloosa, 35487, AL, USA

# ABSTRACT

The escalating global frequency and severity of disasters highlight the need for regional to national risk assessments, necessary for risk-informed

decision-making. The susceptibility of the Gulf Coast of the United States to flooding underscores the urgency of this need. Here, we introduce a

framework for fine-scale (i.e. block-level) flood risk assessment in low-lying coastal regions prone to compound hazards that systematically ad-

dresses limitations in existing approaches. Focused on reducing subjectivity and enhancing spatial resolution down to the block level, our proposed

framework integrates hydroclimatic, geomorphological, socio-economic, and infrastructure variables, and incorporates indicators including land

use, soil type, elevation, and demographic data to ensure a comprehensive evaluation of flood vulnerability. Additionally, we capture the multi -

dimensional nature of compounding hazards by accounting for both precipitation probability and storm surge height in our analysis. To minimize

subjectivity in determining the contribution of various risk indicators, a supervised machine-learning algorithm classifies flood risk levels based on

reported damages since 2006. The results highlight that 60 % of the studied Gulf Coast blocks face high to very high flood risk, necessitating

proactive risk management. Such high-resolution risk factorization could provide insights for informed decision-making in emergency responses,

land use planning, and resilience assessment.

1.Introduction

The rising occurrence of disasters and their adverse impacts necessitates a comprehensive examination of these effects and their

associated risks, ranging from regional to local scales [1,2]. Intergovernmental Panel on Climate Change Sixth Assessment Report

(IPCC AR6) 2021 defines risk as the potential of adverse consequences for human or ecological systems, recognizing the diversity of

values and objectives associated with such systems. In the context of climate change impacts, risk is quantified as the dynamic

interplay of climate-related hazards with the exposure and vulnerability of human or ecological systems [3,4]. These variables are

subject to various sources of uncertainty, including uncertainties stemming from data curation, parameterization, and model selection

[5–7].

Despite the multitude of studies addressing the spatiotemporal risk at local, regional, and global scales, some aspects of risk remain

inadequately understood and require further refinement[ 1,8–10]. Precise measurement of all elements at an appropriate spatial scale

is crucial for the effective assessment of risks associated with natural hazards [11]. By considering a comprehensive set of risk

components and implementing a high-resolution spatial scale indexing system, the provided information becomes more interpretable

for decision-makers such as floodplain managers, emergency planners, and policy makers [12]. This, in turn, streamlines the risk

assessment process and enhances communication among potential end users [13]. Decision-makers benefit from comprehensive and

*Corresponding author. Center for Complex Hydrosystems Research, University of Alabama, 1030 Cyber Hall, Tuscaloosa, 35487, AL, USA.

E-mail address: hmoradkhani@ua.edu (H. Moradkhani).

Contents lists available at ScienceDirect

International Journal of Disaster Risk Reduction

u{�~zkw! s{yo| kro>! ÐÐÐ1ow �o�to~1m{y2w {mk�o2tun~~

https://doi.org/10.1016/j.ijdrr.2025.105478

Received 9 May 2024; Received in revised form 4 April 2025; Accepted 8 April 2025  International  Journal  of Disaster  Risk Reduction  122 (2025)  105478

Available  online  9 April  2025

2212-4209/©  2025  The Authors.  Published  by Elsevier  Ltd. This is an open access  article  under  the CC BY-NC-ND  license

( http://creativecommons.org/licenses/by-nc-nd/4.0/  ).

high-resolution flood risk assessments as they provide more detailed and localized information, enabling precise identification of

vulnerable areas and more targeted interventions. This allows for better planning of mitigation measures, such as elevating structures

or targeted buyouts, and helps prioritize resources effectively.

High-resolution data can improve emergency response by identifying specific areas in need of immediate aid and support. Addi-

tionally, it enhances the accuracy of long-term recovery plans, such as land-use planning and infrastructure reconstruction, by offering

a more accurate understanding of the flood impacts at a finer scale. A crucial step in structuring a framework for risk analysis of natural

hazards is to determine the spatial resolution at which the analysis is conducted. The Census Bureau’s geographic boundaries are

primarily for data collection and analysis. These boundaries are well-known zoning systems among agencies and decision-makers, and

so the data generated from these boundaries play a crucial role in informing decisions across a wide range of stakeholders from

government agencies, researchers, and local beneficiaries [14,15].

Fine-scale coastal flood risk literature has predominantly focused on hazard characterization stemming from oceanic sources of

flooding, such as storm surge and tidal inundation, while often overlooking the contributions of other sources with hydroclimatic

nature [16–18 ]. While these studies provide valuable insights into the physical drivers of flooding, they frequently neglect the complex

interplay between hazards and the socio-economic vulnerabilities that exacerbate flood impacts. Among the limited efforts to integrate

vulnerability alongside hazard components, most assessments remain confined to localized scales, offering insights applicable only to

specific locations [19–22 ]. Those implemented at larger scales (regional to Global) provide information at resolutions not immediately

useable for community engagement or local risk management [23–25 ]. Furthermore, these studies are often constrained by meth -

odological subjectivity, particularly in the weighting of contributing factors, which can introduce biases and inconsistencies [26].

The contemporary risk assessment approaches with regional to national coverage in the United States, though, offer information at

the Census Bureau’s geographic boundaries at a much coarser scale than the actual occurrences of impacts. The Federal Emergency

Management Agency (FEMA), for example, provides the most precise geographical data on the spatial variability of the National Risk

Index (NRI) at the census tract scale over the Conterminous United States (CONUS) [27]. While offering finer details than other al-

ternatives, NRI helps assess risk at the scale of cities, towns, or other administrative areas, which is beneficial for funding allocations.

This coarse resolution though introduces notable uncertainty into the estimates and mitigation planning, while finer-resolution data

have demonstrated marked enhancements in overall risk evaluations. In the case of NRI, for instance, different neighborhoods or block

groups within a city, based on their different socioeconomic, infrastructure, and geomorphology characteristics, could demonstrate

different levels of vulnerability and exposure to natural hazards [28]. Another flood risk product with a national coverage and

relatively fine resolution (~30 m) by Wing et al., 2018 [29], while a significant step towards high-resolution estimates of risk over

larger domains, estimates potential flood risk over the conterminous United States due to fluvial and pluvial flooding mechanisms only.

Wing et al., 2022 [30] consider both terrestrial and coastal sources of flooding but is not based on familiar zoning boundaries, which

may hinder ease of use by decision-makers. Integrating the three components of hazard, exposure, and vulnerability is a significant

advancement in the national-scale assessment of U.S. flood risk. This approach incorporates property-level data for residential and

non-residential assets to represent exposure, while depth–damage functions are used to assess the vulnerability of these buildings to

flooding. By combining these elements with spatial hazard maps of varying frequencies, their method provides a more comprehensive

and accurate assessment of flood risk across the nation than what was available before.

The incorporation of both qualitative and quantitative risk indicators, along with the subjectivity involved in determining the

contribution of each factor to the overall risk, has proven to be a persistent challenge in risk assessment [26]. The NRI uses k-mean

clustering to assess the overall index for each census tract over the CONUS [27]. The k-mean clustering is a useful unsupervised

learning algorithm that is known for its simplicity and efficiency; however, it is subject to some significant limitations, i.e. sensitivity to

initial centroids, assumption of spherical clusters, and metric dependency. More importantly, an unsupervised algorithm is not

designed to learn from labeled data (i.e., reported damage or casualties), when available. Recently researchers developed a coastal

vulnerability index based on joint probability analysis using copula functions [31]. This methodology can be effective when ambient

data is available at the desired scale, and effective when there exists a statistically significant correlation between variables involved.

However, methodological complexities, e.g. marginal and joint probability function selection and parametrization, may burden its

broader implication at larger scales. Moreover, given its probabilistic nature, quantifying the contribution of each component to the

overall risk might not be a straightforward task.

In this study, we employ a supervised learning technique to reduce subjectivity and assign weights to each factor in assessing the

overall risk. Furthermore, our proposed machine learning (ML) algorithm offers a more computationally efficient alternative to

process-based modeling, such as the flood risk assessment by Wing et al., 2018 [29], Wing et al., 2022 [30], which requires significant

computational resources and extended processing times. By reducing computational costs, our approach enhances scalability and

accessibility, making large-scale flood risk predictions more feasible and efficient. Here, we develop a comprehensive flood risk index

that characterizes the spatial variation in various flood risk indicators (socio-economic, geomorphological, climatic) over the Gulf

Coast of the United States at the census block level.

The Gulf Coast of the United States, which borders the Gulf of Mexico spans from Texas to Florida, encompassing five states: Texas,

Louisiana, Mississippi, Alabama, and Florida. The Gulf Coast is home to over 64 million people and includes major cities such as

Houston, New Orleans, and Tampa. This area is highly vulnerable to coastal flooding, which refers to the inundation of typically dry

low-lying lands near the shoreline due to elevated sea level composed of mean sea levels, astronomical tides, and nontidal variations in

sea level (i.e. storm surge) [89,90]. These coastal flooding incidents have led to significant economic losses and disruptions in the past.

Notable events include Hurricane Katrina in 2005, Hurricane Harvey in 2017, and more recently Helene and Milton in 2024, all of

which caused widespread devastation and highlighted the need for effective coastal risk management. This study elevates the currently

used flood risk assessment by enhancing spatial resolution, expanding the scope of analysis, and minimizing subjectivity in F. Yarveysi et al.                                                                                                                                                                                                       International  Journal  of Disaster  Risk Reduction  122 (2025)  105478

2

determining the impact of various indicators on overall estimated flood risk. To ensure a comprehensive flood risk assessment, we

merge indicators across various categories, including hydroclimatic, geomorphological, socio-economical, and infrastructure. We

assess shoreline geomorphological vulnerability, which refers to a measure of shoreline susceptibility to damage from coastal hazards

(e.g., erosion). To do so, we consider influential indicators such as soil type, land use, land cover, elevation, and proximity to the

coastline [32–36 ]. These factors are integral to flood risk assessment as they influence both the intensity and extent of coastal flooding.

Soil type determines infiltration capacity, which modulates the overland flow regime and eventually could result in an increased

likelihood of flooding. Land use and land cover significantly affect water retention and drainage, with urbanized and impervious

surfaces exacerbating runoff and rural or vegetated areas aiding in water absorption. Elevation plays a crucial role in determining flood

exposure, as lower-lying regions are more susceptible to inundation during storm surges and extreme precipitation events [86–88 ].

Proximity to the coastline dictates the direct impact of tidal influences, storm surges, and wave action, with areas closer to the shore

experiencing higher risks. Understanding these interconnections enables a comprehensive evaluation of shoreline vulnerability,

helping to inform adaptive strategies for coastal flood mitigation.

We also assess socio-economic vulnerability, a measure of a community’s capacity to withstand hazards and its ability to adapt to or

cope with hazardous events [37], and infrastructure vulnerability, the likelihood of infrastructure failure to serve as expected due to

damage/disruption [38]. To conduct an exhaustive evaluation of these aspects of vulnerability, our analysis incorporates not just

demographic and housing data, but also indicators like building quantity and the proximity to the nearest emergency facilities for each

block. Moreover, to offer a comprehensive view of the various flood hazard drivers that endanger the targeted communities, we have

integrated the storm surge height and the probability of precipitation depth exceeding certain thresholds as hydroclimatic indicators in

this analysis. We employ a supervised ML technique to determine the weights of each factor, reducing subjectivity in assessing the

indicators contributing to overall risk. For this purpose, we have used a random forest algorithm, an ensemble learning technique that

improves model performance by combining the predictions of multiple decision trees during training. Random Forest (RF) is ad-

vantageous for its ability to handle mixed data types and its interpretability through feature importance scores. Its ensemble approach

reduces overfitting, making RF well-suited for cases where identifying key predictors and managing diverse data types are important.

The developed algorithm helps objectively classify the flood risk level for every census block in the Gulf Coast region based on the

documented damage resulting from the reported flood hazards dating back to 2006. This objective weighting scheme helps ensuring

that the generated results are universally applicable, making the tools and techniques developed in this study transferable to other

regions. A comparison between the comparable studies and our proposed methodology for flood risk assessment is provided in Table 1.

2.Methods

2.1. Data curation

The primary goal of this study is to provide the spatial distribution of block-level flood risk across the Gulf Coast of the United

States. Census blocks are the smallest geographic area for which the United States Bureau of the Census collects and tabulates decennial

data every 10 years [39,40]. Blocks are formed through the delineation of visible elements such as streets, roads, railroads, water

bodies, and other apparent physical and cultural features, as well as nonvisible boundaries such as property lines, city limits, school

districts, and county boundaries as depicted on Census Bureau maps [40]. Having risk information available at a fine-grained de-

mographic level, such as blocks, provides essential material for the planning and facilitates communication among various stake -

holders. The geographic coordinates of the blocks (latitude and longitude) required for distance calculations were obtained from the

Census’s Block-level Geographic Information [41].

To characterize the vulnerability component, we acquired social, economic, and infrastructure descriptors, including demographics

and building counts at the census block level, from the Hazus data inventory through the Comprehensive Data Management System

(CDMS). Hazus is a modeling application developed by the Federal Emergency Management Agency (FEMA), that offers information

on potential loss estimates for events such as floods, hurricanes, earthquakes, and tsunamis. CDMS is a complementary tool used for

searching and transferring data to and from a specific Hazus state inventory dataset. The data available in Hazus 5.0, which was

released on April 30, 2021, encompasses 59 demographic variables and 33 building count variables for a total of 501,636 studied

blocks across the Gulf Coast of the United States. The demographic features include household composition and socioeconomic status.

This dataset is based on the 2010 census data and has been modified using the National Structure Inventory (NSI) data developed by

the United States Army Corps of Engineers Hydrologic Engineering Center, Flood Impact Assessment (USACE HEC-FIA). We

Table 1

A comparison between methodological settings of various flood risk estimates.

Risk estimate project NRI Wing et al., 2022 This study

Approach Process-based modeling Process-based modeling Data-driven

Spatial resolution Census tract ~30 m Census Block

Relative computational

expensivenessmoderate high low

Risk calculation algorithm An unsupervised algorithm (k-mean

clustering)An ensemble-based method A supervised algorithm (Random Forest)

Impact assessment Regression-based depth-damage

curvesRegression-based depth-

damage curvesA machine learning algorithm trained using NOAA’s

Storm Events databaseF. Yarveysi et al.                                                                                                                                                                                                       International  Journal  of Disaster  Risk Reduction  122 (2025)  105478

3

acknowledge the uncertainty posed by utilizing a dataset collected back in 2010, but this is currently the latest available data at this

resolution. However, our proposed framework is flexible enough to allow updates and potential enhancement with the integration of a

more recent dataset, once becomes available.

To assess physical and shoreline vulnerability, we consider the distance to shoreline, and the average elevation of each block. The

latter is calculated based on the Digital Elevation Model (DEM) developed by the United States Geological Survey (USGS), specifically

the USGS 30 ARC-second Global Elevation Data, GTOPO30. The modification, carried out in coordination with FEMA involves

adjusting the data according to land cover patterns to include areas where structures are most likely to be located while excluding

undeveloped areas such as bodies of water, wetlands, or forests to prevent an overestimation of potential losses. Furthermore, the

General Building Stock (GBS) data in Hazus, which is utilized in this study, is based on RSMeans, a construction cost estimator ’s

toolbox, with a version from 2018 serving as reference [39].

The proximity of each block to the nearest emergency facilities such as fire stations, medical care facilities, shelters, and emergency

operation centers plays an important role in determining the infrastructural vulnerability of each block to natural hazards. The

geographic information regarding emergency resources is obtained from the Hazus database as well. This information was updated

using the 2019 Homeland Infrastructure Foundation-Level Data (HIFLD) [39]. We have also used the HIFLD database to acquire

geographic data about police stations (Local Law Enforcement Locations) and national shelter system facilities that have been

designated as shelters by either FEMA or the American Red Cross. Using the latitude and longitude of these facilities, we calculated

each block ’s proximity to them.

Exposure is quantified using the proportion of Land Use Land Cover (LULC) for five different categories of developed area, forest,

agriculture, water, and barren land and the proportion of soil groups classified into four hydrologic groups of soil (A, B, C, or D), within

each block. Hydrologic soil groups reflect infiltration capacity and flood risk. Group A (sand, loamy sand) has high infiltration and low

runoff, while Group B (sandy loam) is moderate. Group C (silty loam) has lower infiltration and higher runoff, and Group D (clay, clay

loam) has the lowest infiltration and highest flood risk. The National Land Cover Database (NLCD) product which provides nationwide

data on land cover and land cover change, is developed by USGS in partnership with several federal agencies and provides data [42].

The hydrologic groups of soil are acquired from the Gridded Soil Survey Geographic (gSSURGO) database developed by the United

States Department of Agriculture (USDA) [43]. For the variables LULC and soil group, which come at resolutions other than block

scale, with the help of spatial analysis tools in ArcGIS Pro we calculate the proportion of each category within each block area.

Flooding hazard is characterized by three key attributes: severity, duration, and intensity. Severity and intensity together define the

magnitude of the hazard driver, such as rainfall depth or storm surge height, at a given design threshold, including flood return periods

or hurricane categories. Duration, on the other hand, depends on basin characteristics and represents the time window during which

storm components remain impactful. For inland flooding, factors such as watershed steepness, connectivity, and size play a critical role

in determining design storm duration, while for offshore storms, the translation speed of tropical cyclones and wave propagation

dynamics are key considerations. In our study, we use hourly precipitation data, an appropriate temporal resolution for the relatively

small coastal watersheds in our region, and for coastal components, we account for duration implicitly through the storm forward

speed variable in the storm simulations. Here, we incorporate the analysis of two hydroclimatic-driven flood indicators: the ex-

ceedance probability of precipitation depth, representing the terrestrial driver of floods, and storm surge height, as representative of

oceanic flood drivers. Hourly total rainfall depth (mm/hr) from 2000 to 2021, at a spatial resolution of 1/8•, is obtained from the North

American Land Data Assimilation System (NLDAS). NLDAS, a core project supported by NOAA ’s Climate Prediction Program for the

Americas, integrates multiple datasets to create a comprehensive forcing dataset. This includes i) a daily gauge-based precipitation

analysis, which is further temporally disaggregated to hourly intervals using Stage II radar data, ii) bias-corrected shortwave radiation

data, and iii) surface meteorology reanalysis to drive different Land Surface Models [40]. Using this hourly dataset, we first calculated

the 90th percentile of precipitation across the entire study domain as an indicator of extreme rainfall severity, to set a regional

threshold. Then, at each block, the probability that this regional threshold be exceeded is calculated under two scenarios, conditioned

on the size of the block. For blocks smaller than the NLDAS grid cells, we simply use the data from the overlapping grid cell. For blocks

larger than a single NLDAS cell, we use the average of contributing cells.

We incorporate the contribution of oceanic hazard drivers to the overall flood risk at each block by considering the severity of storm

surge height associated with Category 5 hurricane scenarios. For this purpose, we use the data set available by Sea, Lake, and Overland

Surge from Hurricanes (SLOSH) which is a computerized model developed by the National Weather Service to predict storm surge

heights and wind patterns generated by past, theoretical, or forecasted hurricanes [44]. The SLOSH product used here is generated

based on synthetic hurricanes by computing the maximum storm surge, typically measured by feet, resulting from up to 100,000

hypothetical storms simulated through each SLOSH grid of varying forward speed, radius of maximum wind, intensity (Categories

1–5), landfall location, tide level, and storm direction [44]. For larger blocks overlapping with multiple SLOSH calculation points, we

took the maximum value of the estimated surge height.

Moreover, FEMA flood maps that delineate flood zones (areas with an annual flooding probability of 1 % or higher) are useful in

assessing socio-economic vulnerability. These maps guide homeowners and businesses in high-risk areas with mortgages from

federally regulated or insured lenders to purchase flood insurance [45]. This requirement highlights the vulnerability of coastal

communities to flooding and their capacity to recover from extreme events. FEMA ’s flood risk products are designed to guide a wide

range of stakeholders, including property owners, emergency management and floodplain officials, community planners, developers,

and real estate and insurance professionals. These products aim to enhance community resilience by providing valuable information

that deepens the understanding of specific flood risks within the floodplain [46]. Therefore, we calculate the proportion of a block area

that overlaps with the FEMA flood zone, as a metric for its potential of flood occurrence.

To train and validate the developed algorithm, we employ the NOAA Storm Events database. This database is a comprehensive F. Yarveysi et al.                                                                                                                                                                                                       International  Journal  of Disaster  Risk Reduction  122 (2025)  105478

4

repository that offers data on various types of disasters from the years 2006 –2023 [47]. We utilize this database to extract information

regarding the location and property damage for a total of 2040 flood events that occurred in the Gulf Coast region, with estimated

damages ranging from $500 million to $10 billion.

2.2. Framework development

Our objective is to develop a comprehensive block-level flood risk assessment framework for fine-scale flood risk assessment in low-

lying coastal regions that are prone to compound hazards which refers to the coincidence/concurrence of various flood drivers that

lead to significant impacts greater than what is expected from each in isolation [48–50].

This framework enables a risk assessment at the block level while reducing the subjectivity in determining the contribution of

various influential components. Fig. 1demonstrates the overall flow of tasks within this framework.

In order to ensure the consistency and reliability of the information for our analysis, we identified 34 key components deemed most

relevant, mostly based on existing literature [26,37,51–54].

There is a consensus within the scientific community about some of the major factors that influence social vulnerability. However,

some prior studies have approached this indicator selection more objectively. Social vulnerability index (SoVI) based on county-level

socioeconomic data for United States, for example, uses a reductionist technique such as factor analysis to find a robust and consistent

set of variables that capture vulnerability characteristics to be monitored over time [54]. They used principal component analysis to

reduce the initial set of 42 down to 11 independent factors that together explained approximately 76 percent of the variance in the

dataset [54]. More recently, Yarveysi et al. have developed a social-economic-infrastructure vulnerability (SEIV) index to characterize

the spatial variation in vulnerability across the CONUS at the census block level [26]. To conduct an exhaustive evaluation of these

aspects of vulnerability, their analysis incorporates not just demographic and housing data, but also indicators like building quantity

and the proximity to the nearest emergency facilities for each block. Using the variance inflation factor, they further detected the

multicollinear variables and removed them from the dataset to avoid redundant information and alleviate the complexity of the input

data [26]. Here, we build a complete list of risk components and sub-components along with their corresponding data sources, mainly

based on these existing studies, which can be found in Table 2. While all these subcategories are well-discussed in the Data Curation

section, the sub-category of SEIV which comprises 21 mixed variables is presented with the pertinent information in a previous

publication by our group [26].

To ensure that the range and unit variability do not overshadow the analysis of risk classification, we have normalized each of the

variables using a min-max feature scaling equation as follows:

xʹx minx

maxx minx(1)

Where x represents the original values of the variables, and xʹ represents the corresponding normalized values. This normalization is

valuable for handling varying measurement units, however, it might be subject to challenges when dealing with outliers [55,56]. After

normalization the range of each normalized variable will be between 0 and 1, ensuring that each variable retains its own distribution.

Then, normalized variables are ready for integration into a ML algorithm, which is used to categorize the blocks in the Gulf Coast

Fig. 1.Flowchart of estimating the flood risk index.F. Yarveysi et al.                                                                                                                                                                                                       International  Journal  of Disaster  Risk Reduction  122 (2025)  105478

5

Table 2

Sources of sub-components under each category.

Socioeconomic

StatusDemographics Total Population Hazus 5.0, that was released on April 30, 2021, is based on 2010

Census data. Modified by National Structure Inventory (NSI) data

developed by U.S. Army Corp of Engineers Hydrologic

Engineering Center, Flood Impact Assessment (USACE HEC-FIA)

in coordination with FEMATotal Units

Income Less then

10KLow-Income

Income between

10K and 20K

Income between

20K and 30K

Income between

75K and 100KHigh-Income

Income Over 100k

Renter Occupied

Multi-Family UnitsRenter Percent

Renter Occupied

Single-Family Units

Average Cash Rent

Average Home Value

Population Stating

AsianMinority Percent

Population Stating

Black​

Population Stating

Hispanic

Population Stating

Native American

Population Stating

Pacific Islander

Population Stating

Other Race Only

Population Over 65 years-old Percent

Flood Hazard Awareness FEMA Flood Map

Infrastructure General Building

StuckUnits Built Before

1940Old Build Units Percent Hazus 5.0, based on RSMeans (a construction cost estimators

toolbox) version 2018.

Units Built Between

1940 and 1949

Units Built Between

1950 and 1959

Units Built Between

1980 and 1989Recent Build Units

Percent

Units Built Between

1990 and 1998

Units Built After

1998

Multi-dwellings

(10–19 units)Multi dwelling Building

Count (more than 10

unis) Multi-dwellings

(20–49 units)

Multi-dwellings

(50units)

Manufactured Housing

Churches and Other Non-profit Org.

Nursing Home Building Counts

Essential

FacilitiesDistance of to the nearest Emergency Operation

CentersHazus 5.0, that has been updated by 2019 Homeland

Infrastructure Foundation-Level Data (HIFLD).

Distance to the nearest Medical Cares

Distance to the nearest Shelters

Distance to the nearest Fire Stations

Distance to the nearest Police Stations

Geomorphology Land Use Land

CoverDeveloped Area Percent The National Land Cover Database (NLCD) product developed by

USGS Agriculture Area Percent

Forest Area Percent

Water Area Percent

Barren Area Percent

Hydrologic Group

of SoilGroup A Percent Gridded Soil Survey Geographic (gSSURGO) database developed

by the United States Department of Agriculture (USDA) Group B Percent

Group C Percent

Group D Percent

(continued on next page)F. Yarveysi et al.                                                                                                                                                                                                       International  Journal  of Disaster  Risk Reduction  122 (2025)  105478

6

region into five different categories: very low, low, medium, high, and very high.

To determine the level of risk for each block on the Gulf Coast and the contribution of the selected variables to the flood risk index,

we have used a random forest (RF) algorithm. RF is an ensemble learning method that leverages multiple decision trees during the

training phase to enhance the model ’s performance [57]. This method is versatile and applicable to both classification and regression

problems. RF exhibits superiority over alternative regression and classification algorithms due to its ability to handle high-dimensional

data, mitigate overfitting, and provide robust predictions by aggregating the outputs of multiple decision trees. The ensemble nature of

RF enhances model stability, reduces variance, and often results in superior performance across diverse datasets [57].

Given that the damage estimates (explained earlier in the Data Curation section) are associated with specific latitude and longitude

coordinates, we established polygons to represent the area of influence around the reporting location, using the reported damage start

and endpoints (see Fig. 2). Within these polygons, we allocated a weighted distribution of the reported damage (Di) proportional to the

area contribution from each block (Ai) in such a way that the cumulative sum aligns with the total reported damage (D).

DiAi

⋃n

j1AjD (2)

where n is the total number of overlapping blocks with the weighting calculation polygon. The reported damage is classified into five

categories based on their estimated damage quantile (qD) to very low (qD D0.2), low (0.2DqD D0.4), medium (0.4DqD D0.6), high

(0.6DqD D0.8), and very high (0.8DqD).

Implementing a trial-and-error toning approach to maximize the performance of the algorithm, we used 120 decision trees for this

project. We allocated 80 % of the data for training and reserved the remaining 20 % for testing the model ’s performance. To assess the

algorithm ’s performance, we used 10-fold cross-validation. K-fold cross-validation is a method for estimating the performance of ML

models on unseen data [58]. In this process, the dataset is initially randomly divided into K subsets, each with equal sample sizes. One

of these subsets, known as a fold, is used as the test dataset, while the remaining K-1 folds are used as the training dataset. The model is

trained on the training data and then evaluated on the test data. This procedure is repeated for each of the K subsets. The overall Table 2 (continued )

Elevation Digital Elevation Model (DEM) developed by the United States

Geological Survey (USGS), specifically the USGS 30 ARC-second

Global Elevation Data, GTOPO30.

Distance to Shore Census ’ Block-level Geographic information

Hydroclimate Exceedance Probability of Precipitation Depth Hourly total precipitation, from 2000 to 2021, at a spatial

resolution of 1/8•, available by the North American Land Data

Assimilation System (NLDAS)

Storm Surge Height

The Sea, Lake, and Overland Surge from Hurricanes (SLOSH) model

developed by the National Weather Service

Fig. 2.Schematic of weight calculation polygon for redistribution of damage estimates.F. Yarveysi et al.                                                                                                                                                                                                       International  Journal  of Disaster  Risk Reduction  122 (2025)  105478

7

performance of the model is determined as the mean of the model skill scores obtained from each K-fold cross-validation run. This

approach is valuable because it helps reduce the variability of accuracy estimates [59] and provides a more robust assessment of the

model ’s performance.

Furthermore, to determine the contribution of the selected variables to the overall flood risk, we use a built-in feature importance in

the RF algorithm that quantifies the relevance of input features in the calculation of the target variable. The feature selection for

internal nodes of each tree is based on variance reduction for the regression task. Thus, for each feature, the algorithm can measure

how, on average, it reduces variance. The largest decrease is the most relevant and important [60]. The outcome of this trained RF

algorithm would be the estimated category of risk, ranging from very low to very high for each block within the study domain, to be

consistent with the categories drawn by damage quantiles.

3.Results

3.1. Model performance assessment

To determine the level of risk for each block on the Gulf Coast of the United States we have utilized a RF model that leverages

multiple decision trees during the training phase to enhance the model ’s performance (see the details in the Methods section). The

algorithm shows an overall accuracy of 62 % in estimating damage from validation events that were not used during model training.

However, the performance across different subcategories is different. Fig. 3shows the performance matrix of the algorithm, which

helps gauge how well the algorithm is performing in terms of predictive accuracy and generalization to new data at various sub-

categories. It performs best in the Very Low category, with an 89 % success rate, followed by a success rate of 66 % in the Very High

category. From a close look into this matrix, we found out that the numbers below the diagonal are generally larger than those reported

above the diagonal. For example, it is 15.44 % likely that a block with an actual risk level of Very Low will be categorized as medium

risk in prediction, while the likelihood for the opposite (a block with a medium level of risk be predicted as Very Low) is less than 1 %.

From the characteristics of this performance matrix, it can be concluded that the algorithm generally tends to underestimate the risk

category. In regional risk assessment, such an algorithm with a lower chance of false alarms would ensure to avoid raising false red

flags for High to Very High-risk categories. The proposed algorithm ’s conservative approach, which tends to underestimate risk, re-

duces false positives by avoiding over-classifying cases as high risk when they may not be. This can be beneficial in certain situations,

such as healthcare or infrastructure planning, where false positives could lead to unnecessary interventions or costs. However, this

comes with the trade-off of potentially missing true high-risk cases, leading to false negatives. For example, in flood risk management,

underestimating risks can have severe consequences. By failing to identify vulnerable areas, this approach may leave certain regions

unprepared for disasters, resulting in greater damage or loss. While minimizing false positives is valuable, the risk of overlooking areas

that genuinely require attention must be carefully managed to avoid greater harm.

3.2. Contribution of various components to overall flood risk

Conventional methods for risk assessment usually consider various components, including hazard, exposure, and vulnerability that

are equally important and so their contribution to the overall risk is assumed to be uniform. Our analysis, based on reported flood

property damage costs over the studied region, contrasts this assumption and uses a built-in feature importance in the ML algorithm to

assign weights to various variables that contribute to risk (see Methods section for details). The outcomes of our model show a

Fig. 3.Random Forest performance matrix.F. Yarveysi et al.                                                                                                                                                                                                       International  Journal  of Disaster  Risk Reduction  122 (2025)  105478

8

variation in the relative contribution of the components involved (Fig. 4). The input features precipitation probability 90th percentile,

distance to shore, average elevation, percent soil group D, percent developed area, average surge height for category 5 events, and

average home value are found to be the most important descriptors of flood risk that together describe more than 50 % of spatial

variability of risk. The weights obtained from this approach help reduce subjectivity in determining the relative contribution of risk

indicators and thus help provide a more objective depiction of risk drivers across the Gulf Coast.

Fig. 5, the correlation matrix, shows the Spearman correlation coefficients among the six most important key variables associated

with flood risk (or predicted damage) assessment, including average elevation, precipitation probability, average Category 5 surge,

percent developed area, percent soil group D, and distance to shore. Each cell in the heatmap represents the strength and direction of

the relationship between two variables, with darker colors indicating stronger correlations (positive or negative). Notably, there is a

strong negative correlation ( 0.85) between average elevation and average Category 5 surge, suggesting that areas with higher

elevation are less likely to experience extreme surge impacts, likely due to elevation providing natural protection from flood events.

Additionally, the positive correlation (0.15) between percent soil group D and predicted damage implies that areas with more soil

group D (often associated with low permeability) may be more prone to damage during floods, potentially because such soil types favor

increased generation of surface runoff. Most other correlations are weak, indicating a low degree of association between those variable

pairs, which may reflect diverse, complex influences on flood risk factors in coastal environments.

3.3. Block-level flood risk distribution

The summary statistics for the percentage of blocks across the Gulf Coast indicate that nearly 60 % of the region falls into the High

or Very High flood risk categories (Fig. 6). However, this is unequally distributed among coastal states. The state of Mississippi with

more than 93 % of blocks identified as High and Very High risk, and only 3 % of coastal blocks being subject to Low risk is the state with

the highest ratio of blocks subject to flood risk. The state of Texas with 43 % of blocks categorized as High and Very High, and 42 % of

blocks categorized as Low and Very Low demonstrates a more even distribution of flood risk at the block level. It should be noted that

this distribution of categories relies on the damage criteria that distinguish between risk levels (see Methods section for details of

classification).

Fig. 7presents the zoom-in snapshot of the block-level distribution of flood risk in Houston metro, Texas, which has experienced

various major floods over the past few years. As evident in this map, the spatial distribution is unequal between urban and suburban

blocks. This figure further highlights the value of fine-scale flood risk information, when compared with aggregate-level data. Within

the state of Texas which demonstrated a relatively fair distribution of risk between high and low categories, a zoom-in could help

recognize geographical patterns. Such pattern recognition, enabled by block-level risk assessment, can further provide an enhanced

understanding of various contributors when compared with various layers of the major contributing parameter. Fig. 8depicts the

spatial distribution of six of the most important indicators in flood risk based on feature importance analysis.

Figs. 7 and 8reveal specific spatial patterns linking the distribution of the six influential factors with the coastal flood risk cate-

gories in the Houston metropolitan area. A close look into these layers helps interpret the results of the RF algorithm. Areas in eastern

Houston, that show high flood risk, marked in dark red on the flood risk map (Fig. 7), correspond with regions that exhibit high storm

Fig. 4.Contribution of various indicators in flood risk index based on Random Forest (RF). This bar chart is derived from 804 independent flood and

flash flood events within the Gulf Coast of the United States.F. Yarveysi et al.                                                                                                                                                                                                       International  Journal  of Disaster  Risk Reduction  122 (2025)  105478

9

surge heights and low elevations (middle panels in Fig. 8). This combination of high surge potential and low elevation likely drives the

increased flood risk in these eastern zones. Further, regions classified as high-risk often coincide with soil type D in the hydrologic soil

groups map. Soil group D, with its low infiltration rate, increases surface runoff and exacerbates flood risks in heavy rainfall or surge

events, partially explaining why these areas are marked as high-risk on the flood map. Additionally, developed land areas, shown in red

Fig. 5.Spearman correlation coefficients matrix among the six most important key variables associated with flood risk. This matrix is derived from

804 independent flood and flash flood events within the Gulf Coast of the United States.

Fig. 6.Distribution of risk categories across the Gulf Coast and within different states.F. Yarveysi et al.                                                                                                                                                                                                       International  Journal  of Disaster  Risk Reduction  122 (2025)  105478

10

on the land use map, align with higher flood risk zones, reflecting how urbanization can lead to greater runoff and flood potential due

to impervious surfaces.

In the high-risk flood areas in southeastern and central Houston, the map shows relatively high average home values compared to

other parts of the region. This spatial overlap highlights the potential socioeconomic impacts of flooding, as more affluent neigh -

borhoods face increased exposure to coastal flooding. Interestingly, the high precipitation probability areas do not overlap signifi -

cantly with the moderate or high flood risk areas identified in the coastal flood risk map. This spatial separation suggests that while

these areas may frequently experience intense rainfall, other factors, such as less exposure to storm surge, higher elevations, permeable

soils, or distance from the coast, counteract and lead to lower flood risk. Therefore, while precipitation probability is an important

variable in general flood risk assessments, its lower overlap with high-risk zones, in this case, highlights the predominant influence of

coastal and urban factors in shaping flood vulnerability in Houston.

4.Discussions

Despite extensive research on spatiotemporal risk assessment, understanding and refining natural hazard risk factors remain

essential, especially at high spatial resolutions for local impact. A high-resolution, comprehensive flood risk index like the one pre-

sented here at the Gulf Coast census block level enables clearer insights for floodplain managers, emergency planners, and policy -

makers to prioritize resources, plan interventions, and enhance response and recovery efforts. This index encompasses crucial

information, including socio-economic, infrastructure, geomorphological, and hydroclimatic indicators. This study advances current

assessments by improving the precision and applicability of risk categorization down to the census block level and reducing subjec -

tivity through supervised ML algorithms to assign objective weights to indicators and classify flood risk levels based on reported

damages since 2006.

The block-level flood risk assessment enables targeted adaptation and mitigation strategies by providing precise spatial infor-

mation. By identifying high-risk blocks with specific vulnerability factors, local authorities can implement customized interventions

such as strategic buyout programs for properties in very high-risk blocks, prioritized infrastructure hardening in areas with critical

facilities, or targeted elevation requirements for new construction. The granular nature of this assessment allows emergency managers

to develop block-specific evacuation routes and sheltering plans rather than applying uniform approaches across larger census tracts.

Additionally, Communities can allocate limited resilience funding more effectively by targeting blocks with specific risk factor

combinations, like high storm surge potential paired with high-value properties, allowing for more accurate cost-benefit analyses and

effectiveness monitoring.

Maps provide a clear and intuitive visualization of the spatial distribution of flood risk, making them essential tools for assessing

local flood conditions, planning defenses, and informing disaster management strategies [61]. While much of the existing literature has

focused on flood hazard mapping and its associated uncertainties [62–64], a growing body of research has shifted focus toward flood

risk mapping [7,65–67]. Such an approach integrates vulnerability factors, offering a more comprehensive understanding of flood risk.

Fig. 7.Spatial distribution of coastal flood risk categories in Houston metropolitan area, Texas.F. Yarveysi et al.                                                                                                                                                                                                       International  Journal  of Disaster  Risk Reduction  122 (2025)  105478

11

However, most studies remain concentrated on local scales [68–70], with limited exploration of spatially distributed flood risk in-

dicators across larger domains at fine resolutions. Currently existing flood risk indices (e.g., NRI), available at aggregate levels (i.e.

tract to county level), often prioritize top-down flood risk management approaches mainly for resource allocation, thus do not

necessarily facilitate local risk assessment and communication. This potential for spatial misrepresentation and increased uncertainty

is associated with risk assessment at those scales. Consequently, this deficiency could lead to eroding public trust and even

compromising effective risk management. The limitations of the top-down risk management methodology become evident in its failure

to identify and prioritize communities requiring immediate attention for risk mitigation. The traditional methodology lacks the ca-

pacity to determine the relative urgency of action and allocate resources effectively, resulting in a one-size-fits-all governance

approach that eliminates fine-scale variability. This, in turn, obstructs the adoption of adaptive bottom-up flood risk management

approaches [71,72]. Risk information at the level of granularity like the one proposed here facilitates various processes underlying

bottom-up approaches, such as public participation, and inclusion of vulnerable groups [73,74]. This approach not only provides

crucial information to stakeholders but also facilitates communication among local leaders, NGOs, and governments. When made

publicly accessible, it fosters trust, aligns resources based on agreed-upon strategies, and mobilizes assets to enhance resilience against

upcoming hazards [75,76].

Quantifying flood risk involves the integration of indicators from different categories, including hydroclimatic, geomorphological,

socio-economic, and infrastructure variables. This analysis incorporates geomorphological data including land use land cover, soil

type, elevation, and shoreline proximity, as well as demographic data, building counts, and distance to emergency facilities, ensuring a

well-rounded evaluation of flood vulnerability. Worths noted that there are more exposure/vulnerability indicators, e.g. disability

rates, building materials, and precautionary measures that their inclusion could enhance the proposed risk index here. Disability, for

example has a direct relationship with vulnerability to flood risk. Individuals with limited mobility may struggle to evacuate quickly or

access higher ground, while those with sensory disabilities might find it harder to receive timely warnings or navigate flood-prone

areas safely. Cognitive impairments also could hinder decision-making in an emergency. However, due to data limitations, espe-

cially at the block-level resolution, it was not possible to incorporate these indicators in our current analysis. We believe that the

chosen indicators provide a robust foundation for assessing flood risk at the block level, and further refinements can be explored as

more detailed data becomes available at the block-level. Also, while compound flood risk assessment studies usually consider the

Fig. 8.Spatial distribution of six most important features in flood risk characterization.F. Yarveysi et al.                                                                                                                                                                                                       International  Journal  of Disaster  Risk Reduction  122 (2025)  105478

12

nonlinear interaction between hazard drivers (i.e. intense rainfall and storm surge in coastal areas [77–79]), compounding between

various exposure/vulnerability indicators may exacerbate the situation and lead in the level of impacts not expected from each in

isolation [80,81].

The coastal flood risk index proposed in this study stands as a valid risk measure meeting widely accepted criteria, including

practicality, transparency, interpretability, relevance, and theoretical, internal, and external consistency [82]. The transparency of our

approach is based on the publicly available data and methodology used in the analysis that enables reproducibility and usability by

scientists and practitioners. The interpretability of this risk categorization lies in its qualitative clustering, where the Low and Very Low

categories indicate lesser risk, and the High and Very High categories signify increased risk potential. This indexing system provides

conveniently accessible information at a more relevant scale to the flood risk that communities are experiencing, which facilitates risk

assessment and communication among potential end-users. Additionally, relevance is assured through an expert opinion-based var-

iable selection process in this flood risk index development. Leveraging existing hydroclimatic, geomorphologic, social, economic, and

infrastructure indicators from federally supported databases enhances the effectiveness of flood risk assessment. To address various

facets of flood risk, we integrate coastal vulnerability indicators spanning diverse categories such as geomorphological, hydroclimatic,

and socio-economic-infrastructure vulnerabilities. Hence, in the context of coastal flood risk assessment, each variable incorporated

into our index significantly contributes to quantifying the risk that limits an individual, a community, and their assets from the impacts

of flooding. Theoretical consistency is maintained in our coastal flood risk assessment, grounded in the classic theory of risk that views

risk as the combined effects of hazard, exposure, and vulnerability. While an explicit measure for risk is lacking, proxies like reported

damage are reasonably used to validate the risk measure. We acknowledge that alternative frameworks offer valuable insights, and

future research could certainly explore these models for complementary analysis in more complex systems. In network-based

frameworks, for example, the analysis typically centers on a specific type of network of interconnected infrastructure, such as

drainage systems and/or transportation infrastructure, with a key focus on understanding how failures within one component can

propagate and lead to additional stress or cascading failures in interconnected components. This approach highlights the critical need

to account for the systemic nature of infrastructure networks in risk assessments and disaster management strategies, as even a single

point of failure can have far-reaching consequences, undermining the functionality of the broader system. By identifying potential

weak points and their ripple effects, network-based frameworks provide valuable insights for designing resilient systems and priori -

tizing interventions that mitigate the risks of cascading failures during extreme events [83].

Our decision to utilize the classical risk theory stems from its broad applicability and proven effectiveness in addressing the specific

objectives of our study. Given the nature of the risk indicators we are assessing, this framework provides a clear and structured

approach to quantifying risk in a way that aligns with both the available data and the intended applications of our results. Furthermore,

to mitigate the inherent subjectivity in evaluating the impact of various indicators on overall risk, the RF algorithm, a widely employed

tool in various fields of science [57,84], is utilized to categorize the flood risk. The model ’s internal consistency and robustness are

evaluated through K-fold cross-validation (K 10), to ensure a reliable estimate of performance on unseen data and stabilize the

variability of accuracy estimates. The performance metrics, particularly in estimating damage from validation events not utilized in the

training, serve to properly evaluate the external consistency of the proposed indexing system. However, as previously noted, due to the

lack of a clear quantification of risk, conducting a thorough analysis of external consistency is not straightforward and requires

dependence on proxy measures.

The usability of the proposed block-level risk assessment database is, however, challenged by the inconsistency in data updates and

alterations resulting from anthropogenic or natural processes. For instance, the definition of census blocks relies on observable or

imperceptible features, and changes occur as urban features are gained or lost due to urbanization or in response to disasters. These

alterations, coupled with the relevant data updates are usually released within years after each decadal census revision [85]. In

addition, due to climate variations, the dynamic nature of geomorphologic and hydroclimatic indicators is subject to variability,

prompting a need for continuous monitoring and inclusion of new datasets to capture their evolving patterns. Such inconsistency in

data updates and alterations may pose an inherent challenge in maintaining the usability of this product. However, the methodology

presented here is adaptable and can be applied to updated data upon availability. By incorporating updated datasets, we can generate

more accurate and timely risk assessments to inform future planning and response efforts.

In this study, we utilized the most recent and accurate data available at the desired block-level resolution to ensure robust flood risk

assessment. However, it is important to acknowledge a potential source of uncertainty arising from temporal discrepancies across our

datasets (2010 Census data, NLDAS from 2000 to 2021, etc.), as not all input datasets were collected simultaneously. Demographic and

building characteristics from 2010 may not reflect the current community composition in rapidly developing coastal areas, while

hydroclimatic patterns may not fully capture evolving precipitation trends. Addressing this temporal misalignment could refine the

accuracy of the results but falls beyond the scope of this work. Notably, datasets such as those provided by the Census Bureau undergo

revisions within a few years of each decadal survey, minimizing the lag in updates for socio-economic and vulnerability indicators.

This relatively short revision cycle suggests that the temporal misalignment is unlikely to significantly affect the reliability of the final

outcomes. Moreover, the potential for more frequent and quality-controlled data reporting in the future offers a promising avenue to

overcome such uncertainties, further enhancing the precision and applicability of data-driven flood risk assessments.

The proposed algorithm ’s conservative approach, which tends to underestimate risk, reduces false positives by avoiding over-

classifying cases as high risk when they may not be. This can be beneficial in areas like healthcare, infrastructure planning, and

flood risk management, where false positives could lead to unnecessary interventions, costs, or loss of public trust in warning systems.

However, this conservative bias comes with the trade-off of potentially missing true high-risk cases, leading to false negatives that

could leave vulnerable areas unprepared for disasters, resulting in greater damage or loss. Risk managers should account for this

tendency when setting intervention thresholds, potentially lowering the risk category threshold to compensate for underestimation. F. Yarveysi et al.                                                                                                                                                                                                       International  Journal  of Disaster  Risk Reduction  122 (2025)  105478

13

Future iterations of the framework should explore calibration techniques to address this systematic bias while maintaining strong

performance in identifying very high-risk areas.

While our Random Forest model achieves 62 % overall accuracy, we recognize this performance could be enhanced through several

approaches. First, incorporating higher temporal resolution data and more recent demographic information could better align our

predictors with actual flood conditions. Second, expanding our feature set to include additional risk factors such as drainage infra-

structure capacity, impervious surface percentages, and detailed building architectural characteristics could capture more variance in

flood vulnerability. Third, employing ensemble methods that combine multiple machine learning algorithms might improve prediction

accuracy by leveraging the strengths of different modeling approaches.

Addressing the challenge of incompleteness and/or incomprehensiveness of data at the block level is essential for this risk indexing

system. To enhance the effectiveness of the risk index, obtaining additional information such as disability status, education, unem -

ployment, or language proficiency—currently unavailable at the block level—would prove invaluable. Similarly, block-level infor-

mation on LULC and design extreme precipitation substituting estimated information used here with more precise observed data is

imperative for ensuring the accuracy of the risk index.

5.Conclusions

In this study, we present a data-driven framework for fine-scale flood risk assessment tailored to the unique challenges of low-lying

coastal regions, particularly along the Gulf Coast of the United States. This framework integrates a wide range of hydroclimatic,

geomorphological, socio-economic, and infrastructure variables to assess flood risk at the census block level and uses a supervised ML

algorithm to minimize subjectivity in determining indicator contributions and objectively classify flood risk levels based on historical

flood damage reports.

By incorporating diverse indicators such as storm surge height, precipitation, land use, soil type, and infrastructure proximity, this

methodology offers a comprehensive and actionable tool for decision-makers. Our analysis reveals that 60 % of Gulf Coast blocks face

high to very high flood risk, emphasizing the urgent need for localized, proactive risk management strategies. A detailed examination

of Houston Metro, TX reveals that areas with high flood risk, particularly in eastern Houston, are subject to high storm surge potential,

low elevations, and soil group D, which exacerbates flood risks due to its inherent low infiltration rates. Additionally, urbanized re-

gions with impervious surfaces further elevate flood potential. Our findings emphasize the need to consider multiple hazard and

vulnerability indicators in assessing flood risk. Although high precipitation probability areas are important in general flood risk as-

sessments, they do not necessarily overlap with high-risk zones in coastal regions, where storm surge and other urban factors dominate.

The spatial overlap of high-risk flood areas with economically valuable and densely populated neighborhoods in southeastern and

central Houston also highlights the significance of socioeconomic factors in flood risk assessment, underscoring the urgent need for

targeted risk mitigation strategies in these areas. The transparency, interpretability, and practicality of this approach not only improve

risk communication among stakeholders but also help align resources effectively for resilience-building efforts. While challenges

remain—such as the need for continuous data updates and finer block-level information—this study marks a significant advancement

in flood risk assessment. The framework’s scalability and transparency enable its transferability to other regions and contexts, making

it a versatile tool beyond the immediate study area. Given the availability of data at such fine resolutions, this methodology is flexible

enough to be extended to other regions that suffer from compound coastal flooding, offering an adaptable approach to address varying

hydroclimatic and socio-economic conditions.

Future work could focus on refining data resolution, incorporating real-time monitoring, and further enhancing the framework’s

predictive capabilities to provide even more localized and dynamic flood risk assessments. Ultimately, this framework not only serves

as a vital tool for understanding and managing flood risk but also sets a precedent for integrating advanced data-driven approaches into

resilience planning and policy development.

CRediT authorship contribution statement

Farnaz Yarveysi: Writing – original draft, Visualization, Validation, Software, Methodology, Investigation, Formal analysis, Data

curation, Conceptualization. Keighobad Jafarzadegan: Writing – review & editing, Validation, Methodology. Shrabani S. Tripathy:

Writing – review & editing, Validation, Methodology. Hamed Moftakhari: Writing – review & editing, Project administration,

Funding acquisition, Conceptualization. Hamid Moradkhani: Writing – review & editing, Supervision, Project administration,

Funding acquisition, Conceptualization.

Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to

influence the work reported in this paper.

Acknowledgments

This study is funded by USACE contract #W912HZ2020055. Partial Funding for this project was also provided by the National

Oceanic and Atmospheric Administration (NOAA), awarded to the Cooperative Institute for Research on Hydrology (CIROH) through

the NOAA Cooperative Agreement with The University of Alabama, NA22NWS4320003.F. Yarveysi et al.                                                                                                                                                                                                       International  Journal  of Disaster  Risk Reduction  122 (2025)  105478

14

Data availability

Data will be made available on request.

References

[1]P.J. Ward, V. Blauhut, N. Bloemendaal, J.E. Daniell, M.C. de Ruiter, M.J. Duncan, R. Emberson, S.F. Jenkins, D. Kirschbaum, M. Kunz, S. Mohr, S. Muis, G.

A. Riddell, A. Schafer, T. Stanley, T.I.E. Veldkamp, H.C. Winsemius, Review article: natural hazard risk assessments at the global scale, Nat. Hazards Earth Syst.

Sci. 20 (2020) 1069 –1096, https://doi.org/10.5194/nhess-20-1069-2020 .

[2]A. Reisinger, M. Howden, C. Vera, Guidance for IPCC Authors, (n.d.).

[3]W. Kron, Flood risk hazard ≡values ≡vulnerability, Water Int. 30 (2005) 58–68, https://doi.org/10.1080/02508060508691837 .

[4]S.S. Tripathy, H. Vittal, S. Karmakar, S. Ghosh, Flood risk forecasting at weather to medium range incorporating weather model, topography, socio-economic

information and land use exposure, Adv. Water Resour. 146 (2020) 103785 .

[5]P. Abbaszadeh, D. Munoz, H. Moftakhari, K. Jafarzadegan, H. Moradkhani, Perspective on uncertainty quantification and reduction in compound flood

modeling and forecasting, special issue on compound events/connected events, iScience 25 (10) (2022) 105201, https://doi.org/10.1016/j.isci.2022.105201 .

[6]K.J. Beven, W.P. Aspinall, P.D. Bates, E. Borgomeo, K. Goda, J.W. Hall, T. Page, J.C. Phillips, M. Simpson, P.J. Smith, T. Wagener, M. Watson, Epistemic

uncertainties and natural hazard risk assessment – part 2: what should constitute good practice? Nat. Hazards Earth Syst. Sci. 18 (2018) 2769 –2783, https://doi.

org/10.5194/nhess-18-2769-2018 .

[7]K. Jafarzadegan, H. Moradkhani, F. Pappenberger, H. Moftakhari, P. Bates, P. Abbaszadeh, R. Marsooli, C. Ferreira, H.L. Cloke, F. Ogden, Q. Duan, Recent

advances and new frontiers in riverine and coastal flood modeling, Rev. Geophys. 61 (2023) e2022RG000788, https://doi.org/10.1029/2022RG000788 .

[8]V. Silva, S. Brzev, C. Scawthorn, C. Yepes, J. Dabbeek, H. Crowley, A building classification system for multi-hazard risk assessment, Int. J. DIsaster Risk Sci. 13

(2022) 161–177, https://doi.org/10.1007/s13753-022-00400-x .

[9]I. Karimi, E. Hüllermeier, Risk assessment system of natural hazards: a new approach based on fuzzy probability, Fuzzy Set Syst. 158 (2007) 987–999, https://

doi.org/10.1016/j.fss.2006.12.013 .

[10] B. Liu, Y.L. Siu, G. Mitchell, Hazard interaction analysis for multi-hazard risk assessment: a systematic classification based on hazard-forming environment, Nat.

Hazards Earth Syst. Sci. 16 (2016) 629–642, https://doi.org/10.5194/nhess-16-629-2016 .

[11] J.C. Gomez-Zapata, N. Brinckmann, S. Harig, R. Zafrir, M. Pittore, F. Cotton, A. Babeyko, Variable-resolution building exposure modelling for earthquake and

tsunami scenario-based risk assessment: an application case in Lima, Peru, Nat. Hazards Earth Syst. Sci. 21 (2021) 3599 –3628, https://doi.org/10.5194/nhess-

21-3599-2021 .

[12] A.H. Tanim, E. Goharian, H. Moradkhani, Integrated socio-environmental vulnerability assessment of coastal hazards using data-driven and multi-criteria

analysis approaches, Sci. Rep. 12 (2022) 11625, https://doi.org/10.1038/s41598-022-15237-z .

[13] S.S. Tripathy, K. Jafarzadegan, H. Moftakhari, H. Moradkhani, Dynamic bivariate hazard forecasting of hurricanes for improved disaster preparedness, Coun.

Earth Environ. 5 (2024) 12, https://doi.org/10.1038/s43247-023-01198-2 .

[14] Stakeholder toolkit, the census project. https://thecensusproject.org/toolkit/ , 2016. (Accessed 17 October 2023).

[15] U.C. Bureau, Evidence-based decision-making at the Census Bureau, Census.Gov (n.d.). https://www.census.gov/about/what/evidence-act.html (accessed

October 17, 2023).

[16] M.I. Vousdoukas, D. Bouziotas, A. Giardino, L.M. Bouwer, L. Mentaschi, E. Voukouvalas, L. Feyen, Understanding epistemic uncertainty in large-scale coastal

flood risk assessment for present and future climates, Nat. Hazards Earth Syst. Sci. 18 (2018) 2127 –2142, https://doi.org/10.5194/nhess-18-2127-2018 .

[17] M. Lorie, J.E. Neumann, M.C. Sarofim, R. Jones, R.M. Horton, R.E. Kopp, C. Fant, C. Wobus, J. Martinich, M. O’Grady, L.E. Gentile, Modeling coastal flood risk

and adaptation response under future climate conditions, Clim. Risk Manag. 29 (2020) 100233, https://doi.org/10.1016/j.crm.2020.100233 .

[18] D.L. Anderson, P. Ruggiero, F.J. Mendez, P.L. Barnard, L.H. Erikson, A.C. O’Neill, M. Merrifield, A. Rueda, L. Cagigal, J. Marra, Projecting climate dependent

coastal flood risk with a hybrid statistical dynamical model, Earths Future 9 (2021) e2021EF002285, https://doi.org/10.1029/2021EF002285 .

[19] M. Ghanbari, M. Arabi, J. Obeysekera, Chronic and acute coastal flood risks to assets and communities in Southeast Florida, J. Water Resour. Plann. Manag. 146

(2020) 04020049, https://doi.org/10.1061/(ASCE)WR.1943-5452.0001245 .

[20] S.F. Silva, M. Martinho, R. Capit ~ao, T. Reis, C.J. Fortes, J.C. Ferreira, An index-based method for coastal-flood risk assessment in low-lying areas (Costa de

Caparica, Portugal), Ocean Coast Manag. 144 (2017) 90–104, https://doi.org/10.1016/j.ocecoaman.2017.04.010 .

[21] S.-J. Park, D.-K. Lee, Prediction of coastal flooding risk under climate change impacts in South Korea using machine learning algorithms, Environ. Res. Lett. 15

(2020) 094052, https://doi.org/10.1088/1748-9326/aba5b3 .

[22] P. Herreros-Cantis, V. Olivotto, Z.J. Grabowski, T. McPhearson, Shifting landscapes of coastal flood risk: environmental (in)justice of urban change, sea level

rise, and differential vulnerability in New York City, Urban Trans. 2 (2020) 9, https://doi.org/10.1186/s42854-020-00014-w .

[23] M.I. Vousdoukas, L. Mentaschi, E. Voukouvalas, A. Bianchi, F. Dottori, L. Feyen, Climatic and socioeconomic controls of future coastal flood risk in Europe, Nat.

Clim. Change 8 (2018) 776–780, https://doi.org/10.1038/s41558-018-0260-4 .

[24] J. Hinkel, L. Feyen, M. Hemer, G. Le Cozannet, D. Lincke, M. Marcos, L. Mentaschi, J.L. Merkens, H. De Moel, S. Muis, R.J. Nicholls, A.T. Vafeidis, R.S.W. Van De

Wal, M.I. Vousdoukas, T. Wahl, P.J. Ward, C. Wolff, Uncertainty and bias in global to regional scale assessments of current and future coastal flood risk, Earths

Future 9 (2021) e2020EF001882, https://doi.org/10.1029/2020EF001882 .

[25] T. Tiggeloven, H. De Moel, H.C. Winsemius, D. Eilander, G. Erkens, E. Gebremedhin, A. Diaz Loaiza, S. Kuzma, T. Luo, C. Iceland, A. Bouwman, J. Van Huijstee,

W. Ligtvoet, P.J. Ward, Global-scale benefit –cost analysis of coastal flood adaptation to different flood risk drivers using structural measures, Nat. Hazards Earth

Syst. Sci. 20 (2020) 1025 –1044, https://doi.org/10.5194/nhess-20-1025-2020 .

[26] F. Yarveysi, A. Alipour, H. Moftakhari, K. Jafarzadegan, H. Moradkhani, Block-level vulnerability assessment reveals disproportionate impacts of natural

hazards across the conterminous United States, Nat. Commun. 14 (2023) 4222, https://doi.org/10.1038/s41467-023-39853-z .

[27] National Risk Index Technical Documentation, 2023 .

[28] S. Van Zandt, W.G. Peacock, D.W. Henry, H. Grover, W.E. Highfield, S.D. Brody, Mapping social vulnerability to enhance housing and neighborhood resilience,

Housing Policy Debate 22 (2012) 29–55, https://doi.org/10.1080/10511482.2011.624528 .

[29] O.E.J. Wing, P.D. Bates, A.M. Smith, C.C. Sampson, K.A. Johnson, J. Fargione, P. Morefield, Estimates of present and future flood risk in the conterminous

United States, Environ. Res. Lett. 13 (2018) 034023, https://doi.org/10.1088/1748-9326/aaac65 .

[30] O.E.J. Wing, W. Lehman, P.D. Bates, C.C. Sampson, N. Quinn, A.M. Smith, J.C. Neal, J.R. Porter, C. Kousky, Inequitable patterns of US flood risk in the

anthropocene, Nat. Clim. Change 12 (2022) 156–162, https://doi.org/10.1038/s41558-021-01265-6 .

[31] Toward an integrated probabilistic coastal vulnerability assessment: a novel copula-based vulnerability index - tanim - 2023 - water resources research - wiley

online library, (n.d.). https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2022WR033603 (accessed October 17, 2023).

[32] S. Janizadeh, S. Chandra Pal, A. Saha, I. Chowdhuri, K. Ahmadi, S. Mirzaei, A.H. Mosavi, J.P. Tiefenbacher, Mapping the spatial and temporal variability of

flood hazard affected by climate and land-use changes in the future, J. Environ. Manag. 298 (2021) 113551, https://doi.org/10.1016/j.jenvman.2021.113551 .

[33] K. Mishra, R. Sinha, Flood risk assessment in the Kosi megafan using multi-criteria decision analysis: a hydro-geomorphic approach, Geomorphology 350 (2020)

106861, https://doi.org/10.1016/j.geomorph.2019.106861 .

[34] S. Sugianto, A. Deli, E. Miswar, M. Rusdi, M. Irham, The effect of land use and land cover changes on flood occurrence in Teunom Watershed, Aceh jaya, Land 11

(2022) 1271, https://doi.org/10.3390/land11081271 .

[35] B. Van de Sande, J. Lansen, C. Hoyng, Sensitivity of coastal flood risk assessments to digital elevation models, Water 4 (2012) 568–579, https://doi.org/

10.3390/w4030568 .F. Yarveysi et al.                                                                                                                                                                                                       International  Journal  of Disaster  Risk Reduction  122 (2025)  105478

15

[36] R.U. Zzaman, S. Nowreen, M. Billah, A.S. Islam, Flood hazard mapping of Sangu River basin in Bangladesh using multi-criteria analysis of hydro-

geomorphological factors, J. Flood Risk Manag. 14 (2021) e12715, https://doi.org/10.1111/jfr3.12715 .

[37] CDC/ATSDR social vulnerability index (CDC/ATSDR SVI). https://www.atsdr.cdc.gov/placeandhealth/svi/index.html , 2024. (Accessed 21 October 2024).

[38] A. Silvast, R. Kongsager, T.-K. Lehtonen, M. Lundgren, M. Virtanen, Critical infrastructure vulnerability: a research note on adaptation to climate change in the

Nordic countries, Dan. J. Geogr. 121 (2021) 79–90, https://doi.org/10.1080/00167223.2020.1851609 .

[39] FEMA, Hazus inventory technical manual. file:///C:/Users/fyarveysi/Documents/Research/Vulnerability/Fema_hazus-inventory-technical-manual-4.2.3.pdf ,

2021. (Accessed 9 March 2022).

[40] K. Rossiter, What are census blocks? U. S. Census Bur. (2011). https://www.census.gov/newsroom/blogs/random-samplings/2011/07/what-are-census-blocks.

html. (Accessed 8 March 2022).

[41] U.S. Census Bureau, TIGER/line shapefiles technical documentation, 2021, https://www2.census.gov/geo/pdfs/maps-data/data/tiger/tgrshp2021/

TGRSHP2021_TechDoc.pdf , 2021.

[42] J. Dewitz, National land cover database (NLCD) 2021 products. https://doi.org/10.5066/P9JZ7AO3 , 2023.

[43] Gridded soil survey geographic (gSSURGO) database | natural resources conservation service, n.d. https://www.nrcs.usda.gov/resources/data-and-reports/

gridded-soil-survey-geographic-gssurgo-database . (Accessed 24 October 2023).

[44] Sea, Lake, and Overland surges from hurricanes (SLOSH), (n.d.). https://www.nhc.noaa.gov/surge/slosh.php (accessed October 25, 2023).

[45] FEMA flood maps and zones explained | FEMA.gov. https://www.fema.gov/blog/fema-flood-maps-and-zones-explained , 2018. (Accessed 21 October 2024).

[46] Flood maps | FEMA.gov. https://www.fema.gov/flood-maps , 2023. (Accessed 30 October 2023).

[47] NOAA, National centers for environmental information storm events database. https://www.ncdc.noaa.gov/stormevents/ , 2023.

[48] Climate extremes and compound hazards in a warming world | annual reviews, (n.d.). https://www.annualreviews.org/content/journals/10.1146/annurev-

earth-071719-055228 (accessed October 21, 2024).

[49] J. Green, I. Haigh, N. Quinn, J. Neal, T. Wahl, M. Wood, D. Eilander, M. de Ruiter, P. Ward, P. Camus, Review Article: a Comprehensive Review of Compound

Flooding Literature with a Focus on Coastal and Estuarine Regions, EGUsphere, 2024, pp. 1–108, https://doi.org/10.5194/egusphere-2024-2247 .

[50] J. Zscheischler, S. Westra, B.J.J.M. van den Hurk, S.I. Seneviratne, P.J. Ward, A. Pitman, A. AghaKouchak, D.N. Bresch, M. Leonard, T. Wahl, X. Zhang, Future

climate risk from compound events, Nat. Clim. Change 8 (2018) 469–477, https://doi.org/10.1038/s41558-018-0156-3 .

[51] S. Khajehei, A. Ahmadalipour, W. Shao, H. Moradkhani, A place-based assessment of flash flood hazard and vulnerability in the contiguous United States, Sci.

Rep. 10 (2020) 448, https://doi.org/10.1038/s41598-019-57349-z .

[52] B. Flanagan, E. Hallisey, E. Adams, A. Lavery, Measuring community vulnerability to natural and anthropogenic hazards: the centers for disease control and

prevention ’s social vulnerability index, J. Environ. Health 80 (2018) 34–36.

[53] K. Tierney, C. Bevc, E. Kuligowski, Metaphors matter: disaster myths, media frames, and their consequences in Hurricane Katrina, Ann. Am. Acad. Polit. Soc. Sci.

604 (2006) 57–81, https://doi.org/10.1177/0002716205285589 .

[54] S.L. Cutter, The origin and diffusion of the social vulnerability index (SoVI), Int. J. Disaster Risk Reduct. 109 (2024) 104576, https://doi.org/10.1016/j.

ijdrr.2024.104576 .

[55] L.L. Moreira, M.M. de Brito, M. Kobiyama, Review article: a systematic review and future prospects of flood vulnerability indices, Nat. Hazards Earth Syst. Sci.

21 (2021) 1513 –1530, https://doi.org/10.5194/nhess-21-1513-2021 .

[56] Jacobs, P. Smith, M. Goddard, Measuring Performance: an Examination of Composite Performance Indicators, 2004 .

[57] G. Biau, E. Scornet, A random forest guided tour, Test 25 (2016) 197–227, https://doi.org/10.1007/s11749-016-0481-7 .

[58] J.D. Rodriguez, A. Perez, J.A. Lozano, Sensitivity analysis of k-Fold cross validation in prediction error estimation, IEEE Trans. Pattern Anal. Mach. Intell. 32

(2010) 569–575, https://doi.org/10.1109/TPAMI.2009.187 .

[59] G. Vanwinckelen, H. Blockeel, On estimating model accuracy with repeated cross-validation, in: BeneLearn 2012: Proceedings of the 21st Belgian-Dutch

Conference on Machine Learning, 2012, pp. 39–44. https://lirias.kuleuven.be/1655861 . (Accessed 7 April 2022).

[60] P. Pło˘nski, Random Forest Feature Importance Computed in 3 Ways with Python, MLJAR, 2020. https://mljar.com/blog/feature-importance-in-random-forest/ .

(Accessed 9 March 2022).

[61] B. Merz, A.H. Thieken, M. Gocht, Flood risk mapping at the local scale: Concepts and challenges, in: S. Begum, M.J.F. Stive, J.W. Hall (Eds.), Flood Risk

Management in Europe, Springer Netherlands, Dordrecht, 2007, pp. 231–251, https://doi.org/10.1007/978-1-4020-4200-3_13 .

[62] R.B. Mudashiru, N. Sabtu, I. Abustan, W. Balogun, Flood hazard mapping methods: a review, J. Hydrol. 603 (2021) 126846, https://doi.org/10.1016/j.

jhydrol.2021.126846 .

[63] J. Neal, C. Keef, P. Bates, K. Beven, D. Leedal, Probabilistic flood risk mapping including spatial dependence, Hydrol. Process. 27 (2013) 1349 –1363, https://doi.

org/10.1002/hyp.9572 .

[64] P.D. Bates, N. Quinn, C. Sampson, A. Smith, O. Wing, J. Sosa, J. Savage, G. Olcese, J. Neal, G. Schumann, L. Giustarini, G. Coxon, J.R. Porter, M.F. Amodeo,

Z. Chu, S. Lewis-Gruss, N.B. Freeman, T. Houser, M. Delgado, A. Hamidi, I. Bolliger, K.E. McCusker, K. Emanuel, C.M. Ferreira, A. Khalid, I.D. Haigh,

A. Couasnon, R.E. Kopp, S. Hsiang, W.F. Krajewski, Combined modeling of US fluvial, pluvial, and coastal flood hazard under current and future climates, Water

Resour. Res. 57 (2021) e2020WR028673, https://doi.org/10.1029/2020WR028673 .

[65] J. Van Alphen, F. Martini, R. Loat, R. Slomp, R. Passchier, Flood risk mapping in Europe, experiences and best practices, J. Flood Risk Manag. 2 (2009) 285–292,

https://doi.org/10.1111/j.1753-318X.2009.01045.x .

[66] H. Kreibich, N. Sairam, Dynamic flood risk modelling in human –flood systems, in: C. Kondrup, P. Mercogliano, F. Bosello, J. Mysiak, E. Scoccimarro, A. Rizzo,

R. Ebrey, M. de Ruiter, A. Jeuken, P. Watkiss (Eds.), Climate Adaptation Modelling, Springer International Publishing, Cham, 2022, pp. 95–103, https://doi.org/

10.1007/978-3-030-86211-4_12 .

[67] B. Büchele, H. Kreibich, A. Kron, A. Thieken, J. Ihringer, P. Oberle, B. Merz, F. Nestmann, Flood-risk mapping: contributions towards an enhanced assessment of

extreme events and associated risks, Nat. Hazards Earth Syst. Sci. 6 (2006) 485–503, https://doi.org/10.5194/nhess-6-485-2006 .

[68] K. Oubennaceur, K. Chokmani, M. Nastev, R. Lhissou, A. El Alem, Flood risk mapping for direct damage to residential buildings in Quebec, Canada, Int. J.

Disaster Risk Reduct. 33 (2019) 44–54, https://doi.org/10.1016/j.ijdrr.2018.09.007 .

[69] C. Lu, J. Zhou, Z. He, S. Yuan, Evaluating typical flood risks in Yangtze River Economic Belt: application of a flood risk mapping framework, Nat. Hazards 94

(2018) 1187 –1210, https://doi.org/10.1007/s11069-018-3466-x .

[70] R. De Risi, F. Jalayer, F. De Paola, I. Iervolino, M. Giugni, M.E. Topa, E. Mbuya, A. Kyessi, G. Manfredi, P. Gasparini, Flood risk assessment for informal

settlements, Nat. Hazards 69 (2013) 1003 –1032, https://doi.org/10.1007/s11069-013-0749-0 .

[71] J.O. Knighton, O. Tsuda, R. Elliott, M.T. Walter, Challenges to implementing bottom-up flood risk decision analysis frameworks: how strong are social networks

of flooding professionals? Hydrol. Earth Syst. Sci. 22 (2018) 5657 –5673, https://doi.org/10.5194/hess-22-5657-2018 .

[72] A. Serra-Llobet, E. Conrad, K. Schaefer, Governing for integrated water and flood risk management: comparing top-down and Bottom-Up approaches in Spain

and California, Water 8 (2016) 445, https://doi.org/10.3390/w8100445 .

[73] J. Edelenbos, A. Van Buuren, D. Roth, M. Winnubst, Stakeholder initiatives in flood risk management: exploring the role and impact of bottom-up initiatives in

three ‘Room for the River ’ projects in the Netherlands, J. Environ. Plann. Manag. 60 (2017) 47–66, https://doi.org/10.1080/09640568.2016.1140025 .

[74] S. Seebauer, S. Ortner, P. Babcicky, T. Thaler, Bottom-up citizen initiatives as emergent actors in flood risk management: mapping roles, relations and

limitations, J. Flood Risk Manag. 12 (2019) e12468, https://doi.org/10.1111/jfr3.12468 .

[75] S. Bhagavathula, K. Brundiers, M. Stauffacher, B. Kay, Fostering collaboration in city governments ’ sustainability, emergency management and resilience work

through competency-based capacity building, Int. J. Disaster Risk Reduct. 63 (2021) 102408, https://doi.org/10.1016/j.ijdrr.2021.102408 .

[76] B.F. Sanders, J.E. Schubert, D.T. Kahl, K.J. Mach, D. Brady, A. AghaKouchak, F. Forman, R.A. Matthew, N. Ulibarri, S.J. Davis, Large and inequitable flood risks

in Los Angeles, California, Nat. Sustain. 6 (2022) 47–57, https://doi.org/10.1038/s41893-022-00977-7 .

[77] T. Wahl, S. Jain, J. Bender, S.D. Meyers, M.E. Luther, Increasing risk of compound flooding from storm surge and rainfall for major US cities, Nat. Clim. Change

5 (2015) 1093 –1097, https://doi.org/10.1038/nclimate2736 .F. Yarveysi et al.                                                                                                                                                                                                       International  Journal  of Disaster  Risk Reduction  122 (2025)  105478

16

[78] H. Xu, K. Xu, J. Lian, C. Ma, Compound effects of rainfall and storm tides on coastal flooding risk, Stoch. Environ. Res. Risk Assess. 33 (2019) 1249 –1261,

https://doi.org/10.1007/s00477-019-01695-x .

[79] E. Bevacqua, D. Maraun, M.I. Vousdoukas, E. Voukouvalas, M. Vrac, L. Mentaschi, M. Widmann, Higher probability of compound flooding from precipitation

and storm surge in Europe under anthropogenic climate change, Sci. Adv. 5 (2019) eaaw5531, https://doi.org/10.1126/sciadv.aaw5531 .

[80] N. van Maanen, M. de Ruiter, P.J. Ward, Workshop report: the role of Earth observation for multi-(hazard-)risk assessment and management, iScience 27 (2024),

https://doi.org/10.1016/j.isci.2024.110833 .

[81] R. ¯Saki˘c Trogrli ˘c, K. Reiter, R.L. Ciurean, S. Gottardo, S. Torresan, A.S. Daloz, L. Ma, N. Padr ˘on Fumero, S. Tatman, S. Hochrainer-Stigler, M.C. de Ruiter,

J. Schlumberger, R. Harris, S. Garcia-Gonzalez, M. García-Vaquero, T.L.F. Ar˘evalo, R. Hernandez-Martin, J. Mendoza-Jimenez, D.M. Ferrario, D. Geurts,

D. Stuparu, T. Tiggeloven, M.J. Duncan, P.J. Ward, Challenges in assessing and managing multi-hazard risks: a European stakeholders perspective, Environ. Sci.

Pol. 157 (2024) 103774, https://doi.org/10.1016/j.envsci.2024.103774 .

[82] S.E. Spielman, J. Tuccillo, D.C. Folch, A. Schweikert, R. Davies, N. Wood, E. Tate, Evaluating social vulnerability indicators: criteria and their application to the

social vulnerability index, Nat. Hazards 100 (2020) 417–436, https://doi.org/10.1007/s11069-019-03820-z .

[83] M.R. Najafi, Y. Zhang, N. Martyn, A flood risk assessment framework for interdependent infrastructure systems in coastal environments, Sustain. Cities Soc. 64

(2021) 102516, https://doi.org/10.1016/j.scs.2020.102516 .

[84] P. Abbaszadeh, H. Moradkhani, X. Zhan, Downscaling SMAP radiometer soil moisture over the CONUS using an ensemble learning method, Water Resour. Res.

55 (2019) 324–344, https://doi.org/10.1029/2018WR023354 .

[85] Bureau of the Census, Chapter 11: Census blocks and block groups, in: Geographic Areas Reference Manual, U.S. Department of Commerce, Washington, D.C.,

1994. https://www2.census.gov/geo/pdfs/reference/GARM/Ch11GARM.pdf .

[86] A. Samadi, K. Jafarzadegan, H. Moradkhani, DEM-based pluvial flood inundation modeling at a metropolitan scale, Environ. Model. Software (2025), https://

doi.org/10.1016/j.envsoft.2024.106226 .

[87] H. Dey, W. Shao, H. Moradkhani, B.D. Keim, B.G. Peter, Urban flood susceptibility mapping using frequency ratio and multiple decision tree-based machine

learning models, Nat. Hazards (2024), https://doi.org/10.1007/s11069-024-06609-x .

[88] F.R. Aderyani, K. Jafarzadegan, H. Moradkhani, A surrogate machine learning modeling approach for enhancing the efficiency of urban flood modeling at

metropolitan scales, Sustain. Cities Soc. (2025), https://doi.org/10.1016/j.scs.2025.106277 .

[89] H. Moftakhari, D.F. Mu~noz, A. Akbari Asanjan, A. Aghakouchak, H. Moradkhani, D.A. Jay, Nonlinear interactions of sea-level rise and storm tide alter extreme

coastal water levels: how and why? AGU Adv. (2024) https://doi.org/10.1029/2023AV000996 .

[90] S. Mahmoudi, H. Moftakhari, D.F. Mu~noz, W. Sweet, H. Moradkhani, Establishing flood thresholds for sea level rise impact communication, Nat. Commun.

(2024), https://doi.org/10.1038/s41467-024-48545-1 .F. Yarveysi et al.                                                                                                                                                                                                       International  Journal  of Disaster  Risk Reduction  122 (2025)  105478

17