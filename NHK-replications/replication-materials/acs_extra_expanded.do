* NOTE: You need to set the Stata working directory to the path
* where the data file is located.

set more off

clear
quietly infix                    ///
  int     year        1-4        ///
  long    sample      5-10       ///
  double  serial      11-18      ///
  double  cbserial    19-31      ///
  double  hhwt        32-41      ///
  byte    hhtype      42-42      ///
  byte    repwt       43-43      ///
  double  cluster     44-56      ///
  double  cpi99       57-61      ///
  byte    region      62-63      ///
  byte    stateicp    64-65      ///
  byte    statefip    66-67      ///
  int     countyicp   68-71      ///
  int     countyfip   72-74      ///
  long    puma        75-79      ///
  int     cpuma0010   80-83      ///
  double  density     84-90      ///
  byte    metro       91-91      ///
  int     metarea     92-94      ///
  int     metaread    95-98      ///
  long    met2013     99-103     ///
  double  metpop10    104-111    ///
  int     city        112-115    ///
  long    citypop     116-122    ///
  byte    homeland    123-123    ///
  double  strata      124-135    ///
  int     cntry       136-138    ///
  byte    gq          139-139    ///
  byte    gqtype      140-140    ///
  int     gqtyped     141-143    ///
  byte    farm        144-144    ///
  byte    ownershp    145-145    ///
  byte    ownershpd   146-147    ///
  byte    mortgage    148-148    ///
  byte    mortgag2    149-149    ///
  long    mortamt1    150-154    ///
  byte    taxincl     155-155    ///
  byte    insincl     156-156    ///
  int     proptx99    157-159    ///
  long    rentgrs     160-164    ///
  byte    rentmeal    165-165    ///
  long    hhincome    166-172    ///
  byte    foodstmp    173-173    ///
  long    valueh      174-180    ///
  byte    lingisol    181-181    ///
  byte    vacancy     182-182    ///
  byte    bedrooms    183-184    ///
  byte    phone       185-185    ///
  byte    cinethh     186-186    ///
  byte    cilaptop    187-187    ///
  byte    cismrtphn   188-188    ///
  byte    citablet    189-189    ///
  byte    cihand      190-190    ///
  byte    ciothcomp   191-191    ///
  byte    cidatapln   192-192    ///
  byte    cihispeed   193-194    ///
  byte    cisat       195-195    ///
  byte    cidial      196-196    ///
  byte    ciothsvc    197-197    ///
  byte    vehicles    198-198    ///
  byte    nfams       199-200    ///
  byte    nsubfam     201-201    ///
  byte    ncouples    202-202    ///
  byte    nmothers    203-203    ///
  byte    nfathers    204-204    ///
  byte    multgen     205-205    ///
  byte    multgend    206-207    ///
  long    repwt1      208-213    ///
  long    repwt2      214-219    ///
  long    repwt3      220-225    ///
  long    repwt4      226-231    ///
  long    repwt5      232-237    ///
  long    repwt6      238-243    ///
  long    repwt7      244-249    ///
  long    repwt8      250-255    ///
  long    repwt9      256-261    ///
  long    repwt10     262-267    ///
  long    repwt11     268-273    ///
  long    repwt12     274-279    ///
  long    repwt13     280-285    ///
  long    repwt14     286-291    ///
  long    repwt15     292-297    ///
  long    repwt16     298-303    ///
  long    repwt17     304-309    ///
  long    repwt18     310-315    ///
  long    repwt19     316-321    ///
  long    repwt20     322-327    ///
  long    repwt21     328-333    ///
  long    repwt22     334-339    ///
  long    repwt23     340-345    ///
  long    repwt24     346-351    ///
  long    repwt25     352-357    ///
  long    repwt26     358-363    ///
  long    repwt27     364-369    ///
  long    repwt28     370-375    ///
  long    repwt29     376-381    ///
  long    repwt30     382-387    ///
  long    repwt31     388-393    ///
  long    repwt32     394-399    ///
  long    repwt33     400-405    ///
  long    repwt34     406-411    ///
  long    repwt35     412-417    ///
  long    repwt36     418-423    ///
  long    repwt37     424-429    ///
  long    repwt38     430-435    ///
  long    repwt39     436-441    ///
  long    repwt40     442-447    ///
  long    repwt41     448-453    ///
  long    repwt42     454-459    ///
  long    repwt43     460-465    ///
  long    repwt44     466-471    ///
  long    repwt45     472-477    ///
  long    repwt46     478-483    ///
  long    repwt47     484-489    ///
  long    repwt48     490-495    ///
  long    repwt49     496-501    ///
  long    repwt50     502-507    ///
  long    repwt51     508-513    ///
  long    repwt52     514-519    ///
  long    repwt53     520-525    ///
  long    repwt54     526-531    ///
  long    repwt55     532-537    ///
  long    repwt56     538-543    ///
  long    repwt57     544-549    ///
  long    repwt58     550-555    ///
  long    repwt59     556-561    ///
  long    repwt60     562-567    ///
  long    repwt61     568-573    ///
  long    repwt62     574-579    ///
  long    repwt63     580-585    ///
  long    repwt64     586-591    ///
  long    repwt65     592-597    ///
  long    repwt66     598-603    ///
  long    repwt67     604-609    ///
  long    repwt68     610-615    ///
  long    repwt69     616-621    ///
  long    repwt70     622-627    ///
  long    repwt71     628-633    ///
  long    repwt72     634-639    ///
  long    repwt73     640-645    ///
  long    repwt74     646-651    ///
  long    repwt75     652-657    ///
  long    repwt76     658-663    ///
  long    repwt77     664-669    ///
  long    repwt78     670-675    ///
  long    repwt79     676-681    ///
  long    repwt80     682-687    ///
  int     pernum      688-691    ///
  double  perwt       692-701    ///
  double  slwt        702-711    ///
  byte    repwtp      712-712    ///
  byte    famunit     713-714    ///
  byte    famsize     715-716    ///
  byte    subfam      717-717    ///
  byte    sftype      718-718    ///
  byte    momloc      719-720    ///
  byte    momrule     721-722    ///
  byte    poploc      723-724    ///
  byte    sploc       725-726    ///
  byte    nchild      727-727    ///
  byte    nchlt5      728-728    ///
  byte    nsibs       729-729    ///
  byte    eldch       730-731    ///
  byte    yngch       732-733    ///
  byte    relate      734-735    ///
  int     related     736-739    ///
  byte    sex         740-740    ///
  int     age         741-743    ///
  byte    ageorig     744-745    ///
  byte    birthqtr    746-746    ///
  byte    marst       747-747    ///
  int     birthyr     748-751    ///
  byte    marrinyr    752-752    ///
  int     yrmarr      753-756    ///
  byte    divinyr     757-757    ///
  byte    widinyr     758-758    ///
  byte    fertyr      759-759    ///
  byte    race        760-760    ///
  int     raced       761-763    ///
  byte    hispan      764-764    ///
  int     hispand     765-767    ///
  int     bpl         768-770    ///
  long    bpld        771-775    ///
  int     ancestr1    776-778    ///
  int     ancestr1d   779-782    ///
  int     ancestr2    783-785    ///
  int     ancestr2d   786-789    ///
  byte    citizen     790-790    ///
  int     yrnatur     791-794    ///
  int     yrimmig     795-798    ///
  byte    yrsusa1     799-800    ///
  byte    yrsusa2     801-801    ///
  byte    language    802-803    ///
  int     languaged   804-807    ///
  byte    speakeng    808-808    ///
  byte    rachsing    809-809    ///
  double  predai      810-817    ///
  double  predapi     818-825    ///
  double  predblk     826-833    ///
  double  predwht     834-841    ///
  byte    predhisp    842-842    ///
  byte    racamind    843-843    ///
  byte    racasian    844-844    ///
  byte    racblk      845-845    ///
  byte    racpacis    846-846    ///
  byte    racwht      847-847    ///
  byte    racother    848-848    ///
  byte    hcovany     849-849    ///
  byte    hcovpriv    850-850    ///
  byte    hinsemp     851-851    ///
  byte    hinspur     852-852    ///
  byte    hinstri     853-853    ///
  byte    hcovpub     854-854    ///
  byte    hinscaid    855-855    ///
  byte    hinscare    856-856    ///
  byte    hinsva      857-857    ///
  byte    hinsihs     858-858    ///
  byte    school      859-859    ///
  byte    educ        860-861    ///
  int     educd       862-864    ///
  byte    gradeatt    865-865    ///
  byte    gradeattd   866-867    ///
  byte    schltype    868-868    ///
  byte    degfield    869-870    ///
  int     degfieldd   871-874    ///
  byte    empstat     875-875    ///
  byte    empstatd    876-877    ///
  byte    labforce    878-878    ///
  byte    classwkr    879-879    ///
  byte    classwkrd   880-881    ///
  int     occ         882-885    ///
  int     occ2010     886-889    ///
  int     ind         890-893    ///
  str     indnaics    894-901    ///
  byte    wkswork1    902-903    ///
  byte    wkswork2    904-904    ///
  byte    uhrswork    905-906    ///
  byte    wrklstwk    907-907    ///
  byte    absent      908-908    ///
  byte    looking     909-909    ///
  byte    availble    910-910    ///
  byte    wrkrecal    911-911    ///
  byte    workedyr    912-912    ///
  long    inctot      913-919    ///
  long    ftotinc     920-926    ///
  long    incwage     927-932    ///
  long    incbus00    933-938    ///
  long    incss       939-943    ///
  long    incwelfr    944-948    ///
  long    incinvst    949-954    ///
  long    incretir    955-960    ///
  long    incsupp     961-965    ///
  long    incother    966-970    ///
  long    incearn     971-977    ///
  int     poverty     978-980    ///
  byte    occscore    981-982    ///
  byte    sei         983-984    ///
  double  hwsei       985-988    ///
  byte    migrate1    989-989    ///
  byte    migrate1d   990-991    ///
  int     migplac1    992-994    ///
  int     migcounty1  995-997    ///
  long    migpuma1    998-1002   ///
  long    migmet131   1003-1007  ///
  byte    movedin     1008-1008  ///
  byte    disabwrk    1009-1009  ///
  byte    vetdisab    1010-1010  ///
  byte    diffrem     1011-1011  ///
  byte    diffphys    1012-1012  ///
  byte    diffmob     1013-1013  ///
  byte    diffcare    1014-1014  ///
  byte    diffsens    1015-1015  ///
  byte    vetstat     1016-1016  ///
  byte    vetstatd    1017-1018  ///
  byte    pwstate2    1019-1020  ///
  int     pwcounty    1021-1023  ///
  byte    tranwork    1024-1025  ///
  byte    carpool     1026-1026  ///
  byte    riders      1027-1027  ///
  int     trantime    1028-1030  ///
  int     departs     1031-1034  ///
  int     arrives     1035-1038  ///
  byte    qage        1039-1039  ///
  byte    qmarst      1040-1040  ///
  byte    qrelate     1041-1041  ///
  byte    qsex        1042-1042  ///
  byte    qbpl        1043-1043  ///
  byte    qcitizen    1044-1044  ///
  byte    qhispan     1045-1045  ///
  byte    qlanguag    1046-1046  ///
  byte    qrace       1047-1047  ///
  byte    qspeaken    1048-1048  ///
  byte    qyrimm      1049-1049  ///
  byte    qyrnatur    1050-1050  ///
  byte    qeduc       1051-1051  ///
  byte    qschool     1052-1052  ///
  byte    qempstat    1053-1053  ///
  byte    qocc        1054-1054  ///
  byte    quhrswor    1055-1055  ///
  byte    qwkswork2   1056-1056  ///
  byte    qworkedy    1057-1057  ///
  byte    qmigrat1    1058-1058  ///
  long    repwtp1     1059-1064  ///
  long    repwtp2     1065-1070  ///
  long    repwtp3     1071-1076  ///
  long    repwtp4     1077-1082  ///
  long    repwtp5     1083-1088  ///
  long    repwtp6     1089-1094  ///
  long    repwtp7     1095-1100  ///
  long    repwtp8     1101-1106  ///
  long    repwtp9     1107-1112  ///
  long    repwtp10    1113-1118  ///
  long    repwtp11    1119-1124  ///
  long    repwtp12    1125-1130  ///
  long    repwtp13    1131-1136  ///
  long    repwtp14    1137-1142  ///
  long    repwtp15    1143-1148  ///
  long    repwtp16    1149-1154  ///
  long    repwtp17    1155-1160  ///
  long    repwtp18    1161-1166  ///
  long    repwtp19    1167-1172  ///
  long    repwtp20    1173-1178  ///
  long    repwtp21    1179-1184  ///
  long    repwtp22    1185-1190  ///
  long    repwtp23    1191-1196  ///
  long    repwtp24    1197-1202  ///
  long    repwtp25    1203-1208  ///
  long    repwtp26    1209-1214  ///
  long    repwtp27    1215-1220  ///
  long    repwtp28    1221-1226  ///
  long    repwtp29    1227-1232  ///
  long    repwtp30    1233-1238  ///
  long    repwtp31    1239-1244  ///
  long    repwtp32    1245-1250  ///
  long    repwtp33    1251-1256  ///
  long    repwtp34    1257-1262  ///
  long    repwtp35    1263-1268  ///
  long    repwtp36    1269-1274  ///
  long    repwtp37    1275-1280  ///
  long    repwtp38    1281-1286  ///
  long    repwtp39    1287-1292  ///
  long    repwtp40    1293-1298  ///
  long    repwtp41    1299-1304  ///
  long    repwtp42    1305-1310  ///
  long    repwtp43    1311-1316  ///
  long    repwtp44    1317-1322  ///
  long    repwtp45    1323-1328  ///
  long    repwtp46    1329-1334  ///
  long    repwtp47    1335-1340  ///
  long    repwtp48    1341-1346  ///
  long    repwtp49    1347-1352  ///
  long    repwtp50    1353-1358  ///
  long    repwtp51    1359-1364  ///
  long    repwtp52    1365-1370  ///
  long    repwtp53    1371-1376  ///
  long    repwtp54    1377-1382  ///
  long    repwtp55    1383-1388  ///
  long    repwtp56    1389-1394  ///
  long    repwtp57    1395-1400  ///
  long    repwtp58    1401-1406  ///
  long    repwtp59    1407-1412  ///
  long    repwtp60    1413-1418  ///
  long    repwtp61    1419-1424  ///
  long    repwtp62    1425-1430  ///
  long    repwtp63    1431-1436  ///
  long    repwtp64    1437-1442  ///
  long    repwtp65    1443-1448  ///
  long    repwtp66    1449-1454  ///
  long    repwtp67    1455-1460  ///
  long    repwtp68    1461-1466  ///
  long    repwtp69    1467-1472  ///
  long    repwtp70    1473-1478  ///
  long    repwtp71    1479-1484  ///
  long    repwtp72    1485-1490  ///
  long    repwtp73    1491-1496  ///
  long    repwtp74    1497-1502  ///
  long    repwtp75    1503-1508  ///
  long    repwtp76    1509-1514  ///
  long    repwtp77    1515-1520  ///
  long    repwtp78    1521-1526  ///
  long    repwtp79    1527-1532  ///
  long    repwtp80    1533-1538  ///
  byte    spmpov      1539-1539  ///
  byte    offpov      1540-1540  ///
  using `"ACS_extract_expanded.dat"'

replace hhwt       = hhwt       / 100
replace cpi99      = cpi99      / 1000
replace density    = density    / 10
replace perwt      = perwt      / 100
replace slwt       = slwt       / 100
replace predai     = predai     / 10000000
replace predapi    = predapi    / 10000000
replace predblk    = predblk    / 10000000
replace predwht    = predwht    / 10000000
replace hwsei      = hwsei      / 100

format serial     %8.0f
format cbserial   %13.0f
format hhwt       %10.2f
format cluster    %13.0f
format cpi99      %5.3f
format density    %7.1f
format metpop10   %8.0f
format strata     %12.0f
format perwt      %10.2f
format slwt       %10.2f
format predai     %8.7f
format predapi    %8.7f
format predblk    %8.7f
format predwht    %8.7f
format hwsei      %4.2f

label var year       `"Census year"'
label var sample     `"IPUMS sample identifier"'
label var serial     `"Household serial number"'
label var cbserial   `"Original Census Bureau household serial number"'
label var hhwt       `"Household weight"'
label var hhtype     `"Household Type"'
label var repwt      `"Household replicate weights [80 variables]"'
label var cluster    `"Household cluster for variance estimation"'
label var cpi99      `"CPI-U adjustment factor to 1999 dollars"'
label var region     `"Census region and division"'
label var stateicp   `"State (ICPSR code)"'
label var statefip   `"State (FIPS code)"'
label var countyicp  `"County (ICPSR code, identifiable counties only)"'
label var countyfip  `"County (FIPS code, identifiable counties only)"'
label var puma       `"Public Use Microdata Area"'
label var cpuma0010  `"Consistent PUMA, 2000-2010"'
label var density    `"Population-weighted density of PUMA"'
label var metro      `"Metropolitan status (where determinable)"'
label var metarea    `"Metropolitan area (pre-2013 delineations, identifiable areas only) [general vers"'
label var metaread   `"Metropolitan area (pre-2013 delineations, identifiable areas only) [detailed ver"'
label var met2013    `"Metropolitan area (2013 delineations, identifiable areas only)"'
label var metpop10   `"Average 2010 population of 2013 metro/micro areas in PUMA"'
label var city       `"City (identifiable cities only)"'
label var citypop    `"City population (identifiable cities only)"'
label var homeland   `"American Indian, Alaska Native, or Native Hawaiian homeland area"'
label var strata     `"Household strata for variance estimation"'
label var cntry      `"Country"'
label var gq         `"Group quarters status"'
label var gqtype     `"Group quarters type [general version]"'
label var gqtyped    `"Group quarters type [detailed version]"'
label var farm       `"Farm status"'
label var ownershp   `"Ownership of dwelling (tenure) [general version]"'
label var ownershpd  `"Ownership of dwelling (tenure) [detailed version]"'
label var mortgage   `"Mortgage status"'
label var mortgag2   `"Second mortgage status"'
label var mortamt1   `"First mortgage monthly payment"'
label var taxincl    `"Mortgage payment includes property taxes"'
label var insincl    `"Mortgage payment includes property insurance"'
label var proptx99   `"Annual property taxes, 1990"'
label var rentgrs    `"Monthly gross rent"'
label var rentmeal   `"Meals included in rent"'
label var hhincome   `"Total household income "'
label var foodstmp   `"Food stamp recipiency"'
label var valueh     `"House value"'
label var lingisol   `"Linguistic isolation"'
label var vacancy    `"Vacancy status"'
label var bedrooms   `"Number of bedrooms"'
label var phone      `"Telephone availability"'
label var cinethh    `"Access to internet"'
label var cilaptop   `"Laptop, desktop, or notebook computer"'
label var cismrtphn  `"Smartphone"'
label var citablet   `"Tablet or other portable wireless computer"'
label var cihand     `"Handheld computer"'
label var ciothcomp  `"Other computer equipment"'
label var cidatapln  `"Cellular data plan for a smartphone or other mobile device"'
label var cihispeed  `"Broadband (high speed) Internet service such as cable, fiber optic, or DSL servi"'
label var cisat      `"Satellite internet service"'
label var cidial     `"Dial-up service"'
label var ciothsvc   `"Other internet service"'
label var vehicles   `"Vehicles available"'
label var nfams      `"Number of families in household"'
label var nsubfam    `"Number of subfamilies in household"'
label var ncouples   `"Number of couples in household"'
label var nmothers   `"Number of mothers in household"'
label var nfathers   `"Number of fathers in household"'
label var multgen    `"Multigenerational household [general version]"'
label var multgend   `"Multigenerational household [detailed version]"'
label var repwt1     `"Household replicate weight 1"'
label var repwt2     `"Household replicate weight 2"'
label var repwt3     `"Household replicate weight 3"'
label var repwt4     `"Household replicate weight 4"'
label var repwt5     `"Household replicate weight 5"'
label var repwt6     `"Household replicate weight 6"'
label var repwt7     `"Household replicate weight 7"'
label var repwt8     `"Household replicate weight 8"'
label var repwt9     `"Household replicate weight 9"'
label var repwt10    `"Household replicate weight 10"'
label var repwt11    `"Household replicate weight 11"'
label var repwt12    `"Household replicate weight 12"'
label var repwt13    `"Household replicate weight 13"'
label var repwt14    `"Household replicate weight 14"'
label var repwt15    `"Household replicate weight 15"'
label var repwt16    `"Household replicate weight 16"'
label var repwt17    `"Household replicate weight 17"'
label var repwt18    `"Household replicate weight 18"'
label var repwt19    `"Household replicate weight 19"'
label var repwt20    `"Household replicate weight 20"'
label var repwt21    `"Household replicate weight 21"'
label var repwt22    `"Household replicate weight 22"'
label var repwt23    `"Household replicate weight 23"'
label var repwt24    `"Household replicate weight 24"'
label var repwt25    `"Household replicate weight 25"'
label var repwt26    `"Household replicate weight 26"'
label var repwt27    `"Household replicate weight 27"'
label var repwt28    `"Household replicate weight 28"'
label var repwt29    `"Household replicate weight 29"'
label var repwt30    `"Household replicate weight 30"'
label var repwt31    `"Household replicate weight 31"'
label var repwt32    `"Household replicate weight 32"'
label var repwt33    `"Household replicate weight 33"'
label var repwt34    `"Household replicate weight 34"'
label var repwt35    `"Household replicate weight 35"'
label var repwt36    `"Household replicate weight 36"'
label var repwt37    `"Household replicate weight 37"'
label var repwt38    `"Household replicate weight 38"'
label var repwt39    `"Household replicate weight 39"'
label var repwt40    `"Household replicate weight 40"'
label var repwt41    `"Household replicate weight 41"'
label var repwt42    `"Household replicate weight 42"'
label var repwt43    `"Household replicate weight 43"'
label var repwt44    `"Household replicate weight 44"'
label var repwt45    `"Household replicate weight 45"'
label var repwt46    `"Household replicate weight 46"'
label var repwt47    `"Household replicate weight 47"'
label var repwt48    `"Household replicate weight 48"'
label var repwt49    `"Household replicate weight 49"'
label var repwt50    `"Household replicate weight 50"'
label var repwt51    `"Household replicate weight 51"'
label var repwt52    `"Household replicate weight 52"'
label var repwt53    `"Household replicate weight 53"'
label var repwt54    `"Household replicate weight 54"'
label var repwt55    `"Household replicate weight 55"'
label var repwt56    `"Household replicate weight 56"'
label var repwt57    `"Household replicate weight 57"'
label var repwt58    `"Household replicate weight 58"'
label var repwt59    `"Household replicate weight 59"'
label var repwt60    `"Household replicate weight 60"'
label var repwt61    `"Household replicate weight 61"'
label var repwt62    `"Household replicate weight 62"'
label var repwt63    `"Household replicate weight 63"'
label var repwt64    `"Household replicate weight 64"'
label var repwt65    `"Household replicate weight 65"'
label var repwt66    `"Household replicate weight 66"'
label var repwt67    `"Household replicate weight 67"'
label var repwt68    `"Household replicate weight 68"'
label var repwt69    `"Household replicate weight 69"'
label var repwt70    `"Household replicate weight 70"'
label var repwt71    `"Household replicate weight 71"'
label var repwt72    `"Household replicate weight 72"'
label var repwt73    `"Household replicate weight 73"'
label var repwt74    `"Household replicate weight 74"'
label var repwt75    `"Household replicate weight 75"'
label var repwt76    `"Household replicate weight 76"'
label var repwt77    `"Household replicate weight 77"'
label var repwt78    `"Household replicate weight 78"'
label var repwt79    `"Household replicate weight 79"'
label var repwt80    `"Household replicate weight 80"'
label var pernum     `"Person number in sample unit"'
label var perwt      `"Person weight"'
label var slwt       `"Sample-line weight"'
label var repwtp     `"Person replicate weights [80 variables]"'
label var famunit    `"Family unit membership"'
label var famsize    `"Number of own family members in household"'
label var subfam     `"Subfamily membership"'
label var sftype     `"Subfamily type"'
label var momloc     `"Mother's location in the household"'
label var momrule    `"Rule for linking mother (new)"'
label var poploc     `"Father's location in the household"'
label var sploc      `"Spouse's location in household"'
label var nchild     `"Number of own children in the household"'
label var nchlt5     `"Number of own children under age 5 in household"'
label var nsibs      `"Number of own siblings in household"'
label var eldch      `"Age of eldest own child in household"'
label var yngch      `"Age of youngest own child in household"'
label var relate     `"Relationship to household head [general version]"'
label var related    `"Relationship to household head [detailed version]"'
label var sex        `"Sex"'
label var age        `"Age"'
label var ageorig    `"Age (original version)"'
label var birthqtr   `"Quarter of birth"'
label var marst      `"Marital status"'
label var birthyr    `"Year of birth"'
label var marrinyr   `"Married within the past year"'
label var yrmarr     `"Year married"'
label var divinyr    `"Divorced in the past year"'
label var widinyr    `"Widowed in the past year"'
label var fertyr     `"Children born within the last year"'
label var race       `"Race [general version]"'
label var raced      `"Race [detailed version]"'
label var hispan     `"Hispanic origin [general version]"'
label var hispand    `"Hispanic origin [detailed version]"'
label var bpl        `"Birthplace [general version]"'
label var bpld       `"Birthplace [detailed version]"'
label var ancestr1   `"Ancestry, first response [general version]"'
label var ancestr1d  `"Ancestry, first response [detailed version]"'
label var ancestr2   `"Ancestry, second response [general version]"'
label var ancestr2d  `"Ancestry, second response [detailed version]"'
label var citizen    `"Citizenship status"'
label var yrnatur    `"Year naturalized"'
label var yrimmig    `"Year of immigration"'
label var yrsusa1    `"Years in the United States"'
label var yrsusa2    `"Years in the United States, intervalled"'
label var language   `"Language spoken [general version]"'
label var languaged  `"Language spoken [detailed version]"'
label var speakeng   `"Speaks English"'
label var rachsing   `"Race: Simplified race/ethnicity identification"'
label var predai     `"American Indian/Alaska Native race response predicted value"'
label var predapi    `"Asian/Pacific Islander race response predicted value"'
label var predblk    `"Black/African American race response predicted value"'
label var predwht    `"White race response predicted value"'
label var predhisp   `"Hispanic/Latino response predicted value"'
label var racamind   `"Race: American Indian or Alaska Native"'
label var racasian   `"Race: Asian"'
label var racblk     `"Race: black or African American"'
label var racpacis   `"Race: Pacific Islander"'
label var racwht     `"Race: white"'
label var racother   `"Race: some other race"'
label var hcovany    `"Any health insurance coverage"'
label var hcovpriv   `"Private health insurance coverage"'
label var hinsemp    `"Health insurance through employer/union"'
label var hinspur    `"Health insurance purchased directly"'
label var hinstri    `"Health insurance through TRICARE"'
label var hcovpub    `"Public health insurance coverage"'
label var hinscaid   `"Health insurance through Medicaid"'
label var hinscare   `"Health insurance through Medicare"'
label var hinsva     `"Health insurance through VA"'
label var hinsihs    `"Health insurance through Indian Health Services"'
label var school     `"School attendance"'
label var educ       `"Educational attainment [general version]"'
label var educd      `"Educational attainment [detailed version]"'
label var gradeatt   `"Grade level attending [general version]"'
label var gradeattd  `"Grade level attending [detailed version]"'
label var schltype   `"Public or private school"'
label var degfield   `"Field of degree [general version]"'
label var degfieldd  `"Field of degree [detailed version]"'
label var empstat    `"Employment status [general version]"'
label var empstatd   `"Employment status [detailed version]"'
label var labforce   `"Labor force status"'
label var classwkr   `"Class of worker [general version]"'
label var classwkrd  `"Class of worker [detailed version]"'
label var occ        `"Occupation"'
label var occ2010    `"Occupation, 2010 basis"'
label var ind        `"Industry"'
label var indnaics   `"Industry, NAICS classification"'
label var wkswork1   `"Weeks worked last year"'
label var wkswork2   `"Weeks worked last year, intervalled"'
label var uhrswork   `"Usual hours worked per week"'
label var wrklstwk   `"Worked last week"'
label var absent     `"Absent from work last week"'
label var looking    `"Looking for work"'
label var availble   `"Available for work"'
label var wrkrecal   `"Informed of work recall"'
label var workedyr   `"Worked last year"'
label var inctot     `"Total personal income"'
label var ftotinc    `"Total family income"'
label var incwage    `"Wage and salary income"'
label var incbus00   `"Business and farm income, 2000"'
label var incss      `"Social Security income"'
label var incwelfr   `"Welfare (public assistance) income"'
label var incinvst   `"Interest, dividend, and rental income"'
label var incretir   `"Retirement income"'
label var incsupp    `"Supplementary Security Income"'
label var incother   `"Other income"'
label var incearn    `"Total personal earned income"'
label var poverty    `"Poverty status"'
label var occscore   `"Occupational income score"'
label var sei        `"Duncan Socioeconomic Index "'
label var hwsei      `"Socioeconomic Index, Hauser and Warren"'
label var migrate1   `"Migration status 1 year ago [general version]"'
label var migrate1d  `"Migration status 1 year ago [detailed version]"'
label var migplac1   `"State or country of residence 1 year ago"'
label var migcounty1 `"County of residence 1 year ago (FIPS code)"'
label var migpuma1   `"Migration PUMA of residence 1 year ago"'
label var migmet131  `"Metropolitan area of residence 1 year ago (2013 delineations)"'
label var movedin    `"When occupant moved into residence"'
label var disabwrk   `"Work disability"'
label var vetdisab   `"VA service-connected disability rating"'
label var diffrem    `"Cognitive difficulty"'
label var diffphys   `"Ambulatory difficulty"'
label var diffmob    `"Independent living difficulty"'
label var diffcare   `"Self-care difficulty"'
label var diffsens   `"Vision or hearing difficulty"'
label var vetstat    `"Veteran status [general version]"'
label var vetstatd   `"Veteran status [detailed version]"'
label var pwstate2   `"Place of work: state"'
label var pwcounty   `"Place of work: county"'
label var tranwork   `"Means of transportation to work"'
label var carpool    `"Carpooling"'
label var riders     `"Vehicle occupancy"'
label var trantime   `"Travel time to work"'
label var departs    `"Time of departure for work"'
label var arrives    `"Time of arrival at work"'
label var qage       `"Flag for Age"'
label var qmarst     `"Flag for Marst"'
label var qrelate    `"Flag for Relate"'
label var qsex       `"Flag for Sex"'
label var qbpl       `"Flag for Bpl, Nativity"'
label var qcitizen   `"Flag for Citizen"'
label var qhispan    `"Flag for Hispan"'
label var qlanguag   `"Flag for Language, Speakeng"'
label var qrace      `"Flag for Race, Racamind, Racasian, Racblk, Racpais, Racwht, Racoth, Racnum, Race"'
label var qspeaken   `"Flag for Speakeng"'
label var qyrimm     `"Flag for Yrimmig, Yrsusa1, Yrsusa2"'
label var qyrnatur   `"Flag for Yrnatur"'
label var qeduc      `"Flag for Educrec, Higrade, Educ99"'
label var qschool    `"Flag for School, Schltype"'
label var qempstat   `"Flag for Empstat, Labforce"'
label var qocc       `"Flag for Occ, Occ1950, SEI, Occscore, Occsoc, Labforce"'
label var quhrswor   `"Flag for Uhrswork"'
label var qwkswork2  `"Flag for Wkswork2"'
label var qworkedy   `"Flag for Workedyr"'
label var qmigrat1   `"Flag for Migrate1"'
label var repwtp1    `"Person replicate weight 1"'
label var repwtp2    `"Person replicate weight 2"'
label var repwtp3    `"Person replicate weight 3"'
label var repwtp4    `"Person replicate weight 4"'
label var repwtp5    `"Person replicate weight 5"'
label var repwtp6    `"Person replicate weight 6"'
label var repwtp7    `"Person replicate weight 7"'
label var repwtp8    `"Person replicate weight 8"'
label var repwtp9    `"Person replicate weight 9"'
label var repwtp10   `"Person replicate weight 10"'
label var repwtp11   `"Person replicate weight 11"'
label var repwtp12   `"Person replicate weight 12"'
label var repwtp13   `"Person replicate weight 13"'
label var repwtp14   `"Person replicate weight 14"'
label var repwtp15   `"Person replicate weight 15"'
label var repwtp16   `"Person replicate weight 16"'
label var repwtp17   `"Person replicate weight 17"'
label var repwtp18   `"Person replicate weight 18"'
label var repwtp19   `"Person replicate weight 19"'
label var repwtp20   `"Person replicate weight 20"'
label var repwtp21   `"Person replicate weight 21"'
label var repwtp22   `"Person replicate weight 22"'
label var repwtp23   `"Person replicate weight 23"'
label var repwtp24   `"Person replicate weight 24"'
label var repwtp25   `"Person replicate weight 25"'
label var repwtp26   `"Person replicate weight 26"'
label var repwtp27   `"Person replicate weight 27"'
label var repwtp28   `"Person replicate weight 28"'
label var repwtp29   `"Person replicate weight 29"'
label var repwtp30   `"Person replicate weight 30"'
label var repwtp31   `"Person replicate weight 31"'
label var repwtp32   `"Person replicate weight 32"'
label var repwtp33   `"Person replicate weight 33"'
label var repwtp34   `"Person replicate weight 34"'
label var repwtp35   `"Person replicate weight 35"'
label var repwtp36   `"Person replicate weight 36"'
label var repwtp37   `"Person replicate weight 37"'
label var repwtp38   `"Person replicate weight 38"'
label var repwtp39   `"Person replicate weight 39"'
label var repwtp40   `"Person replicate weight 40"'
label var repwtp41   `"Person replicate weight 41"'
label var repwtp42   `"Person replicate weight 42"'
label var repwtp43   `"Person replicate weight 43"'
label var repwtp44   `"Person replicate weight 44"'
label var repwtp45   `"Person replicate weight 45"'
label var repwtp46   `"Person replicate weight 46"'
label var repwtp47   `"Person replicate weight 47"'
label var repwtp48   `"Person replicate weight 48"'
label var repwtp49   `"Person replicate weight 49"'
label var repwtp50   `"Person replicate weight 50"'
label var repwtp51   `"Person replicate weight 51"'
label var repwtp52   `"Person replicate weight 52"'
label var repwtp53   `"Person replicate weight 53"'
label var repwtp54   `"Person replicate weight 54"'
label var repwtp55   `"Person replicate weight 55"'
label var repwtp56   `"Person replicate weight 56"'
label var repwtp57   `"Person replicate weight 57"'
label var repwtp58   `"Person replicate weight 58"'
label var repwtp59   `"Person replicate weight 59"'
label var repwtp60   `"Person replicate weight 60"'
label var repwtp61   `"Person replicate weight 61"'
label var repwtp62   `"Person replicate weight 62"'
label var repwtp63   `"Person replicate weight 63"'
label var repwtp64   `"Person replicate weight 64"'
label var repwtp65   `"Person replicate weight 65"'
label var repwtp66   `"Person replicate weight 66"'
label var repwtp67   `"Person replicate weight 67"'
label var repwtp68   `"Person replicate weight 68"'
label var repwtp69   `"Person replicate weight 69"'
label var repwtp70   `"Person replicate weight 70"'
label var repwtp71   `"Person replicate weight 71"'
label var repwtp72   `"Person replicate weight 72"'
label var repwtp73   `"Person replicate weight 73"'
label var repwtp74   `"Person replicate weight 74"'
label var repwtp75   `"Person replicate weight 75"'
label var repwtp76   `"Person replicate weight 76"'
label var repwtp77   `"Person replicate weight 77"'
label var repwtp78   `"Person replicate weight 78"'
label var repwtp79   `"Person replicate weight 79"'
label var repwtp80   `"Person replicate weight 80"'
label var spmpov     `"SPM poverty status"'
label var offpov     `"Official poverty status"'

label define year_lbl 1850 `"1850"'
label define year_lbl 1860 `"1860"', add
label define year_lbl 1870 `"1870"', add
label define year_lbl 1880 `"1880"', add
label define year_lbl 1900 `"1900"', add
label define year_lbl 1910 `"1910"', add
label define year_lbl 1920 `"1920"', add
label define year_lbl 1930 `"1930"', add
label define year_lbl 1940 `"1940"', add
label define year_lbl 1950 `"1950"', add
label define year_lbl 1960 `"1960"', add
label define year_lbl 1970 `"1970"', add
label define year_lbl 1980 `"1980"', add
label define year_lbl 1990 `"1990"', add
label define year_lbl 2000 `"2000"', add
label define year_lbl 2001 `"2001"', add
label define year_lbl 2002 `"2002"', add
label define year_lbl 2003 `"2003"', add
label define year_lbl 2004 `"2004"', add
label define year_lbl 2005 `"2005"', add
label define year_lbl 2006 `"2006"', add
label define year_lbl 2007 `"2007"', add
label define year_lbl 2008 `"2008"', add
label define year_lbl 2009 `"2009"', add
label define year_lbl 2010 `"2010"', add
label define year_lbl 2011 `"2011"', add
label define year_lbl 2012 `"2012"', add
label define year_lbl 2013 `"2013"', add
label define year_lbl 2014 `"2014"', add
label define year_lbl 2015 `"2015"', add
label define year_lbl 2016 `"2016"', add
label define year_lbl 2017 `"2017"', add
label define year_lbl 2018 `"2018"', add
label define year_lbl 2019 `"2019"', add
label define year_lbl 2020 `"2020"', add
label define year_lbl 2021 `"2021"', add
label define year_lbl 2022 `"2022"', add
label define year_lbl 2023 `"2023"', add
label define year_lbl 2024 `"2024"', add
label values year year_lbl

label define sample_lbl 202404 `"2020-2024, PRCS 5-year"'
label define sample_lbl 202403 `"2020-2024, ACS 5-year"', add
label define sample_lbl 202402 `"2024 PRCS"', add
label define sample_lbl 202401 `"2024 ACS"', add
label define sample_lbl 202304 `"2019-2023, PRCS 5-year"', add
label define sample_lbl 202303 `"2019-2023, ACS 5-year"', add
label define sample_lbl 202302 `"2023 PRCS"', add
label define sample_lbl 202301 `"2023 ACS"', add
label define sample_lbl 202204 `"2018-2022, PRCS 5-year"', add
label define sample_lbl 202203 `"2018-2022, ACS 5-year"', add
label define sample_lbl 202202 `"2022 PRCS"', add
label define sample_lbl 202201 `"2022 ACS"', add
label define sample_lbl 202104 `"2017-2021, PRCS 5-year"', add
label define sample_lbl 202103 `"2017-2021, ACS 5-year"', add
label define sample_lbl 202102 `"2021 PRCS"', add
label define sample_lbl 202101 `"2021 ACS"', add
label define sample_lbl 202004 `"2016-2020, PRCS 5-year"', add
label define sample_lbl 202003 `"2016-2020, ACS 5-year"', add
label define sample_lbl 202001 `"2020 ACS"', add
label define sample_lbl 201904 `"2015-2019, PRCS 5-year"', add
label define sample_lbl 201903 `"2015-2019, ACS 5-year"', add
label define sample_lbl 201902 `"2019 PRCS"', add
label define sample_lbl 201901 `"2019 ACS"', add
label define sample_lbl 201804 `"2014-2018, PRCS 5-year"', add
label define sample_lbl 201803 `"2014-2018, ACS 5-year"', add
label define sample_lbl 201802 `"2018 PRCS"', add
label define sample_lbl 201801 `"2018 ACS"', add
label define sample_lbl 201704 `"2013-2017, PRCS 5-year"', add
label define sample_lbl 201703 `"2013-2017, ACS 5-year"', add
label define sample_lbl 201702 `"2017 PRCS"', add
label define sample_lbl 201701 `"2017 ACS"', add
label define sample_lbl 201604 `"2012-2016, PRCS 5-year"', add
label define sample_lbl 201603 `"2012-2016, ACS 5-year"', add
label define sample_lbl 201602 `"2016 PRCS"', add
label define sample_lbl 201601 `"2016 ACS"', add
label define sample_lbl 201504 `"2011-2015, PRCS 5-year"', add
label define sample_lbl 201503 `"2011-2015, ACS 5-year"', add
label define sample_lbl 201502 `"2015 PRCS"', add
label define sample_lbl 201501 `"2015 ACS"', add
label define sample_lbl 201404 `"2010-2014, PRCS 5-year"', add
label define sample_lbl 201403 `"2010-2014, ACS 5-year"', add
label define sample_lbl 201402 `"2014 PRCS"', add
label define sample_lbl 201401 `"2014 ACS"', add
label define sample_lbl 201306 `"2009-2013, PRCS 5-year"', add
label define sample_lbl 201305 `"2009-2013, ACS 5-year"', add
label define sample_lbl 201304 `"2011-2013, PRCS 3-year"', add
label define sample_lbl 201303 `"2011-2013, ACS 3-year"', add
label define sample_lbl 201302 `"2013 PRCS"', add
label define sample_lbl 201301 `"2013 ACS"', add
label define sample_lbl 201206 `"2008-2012, PRCS 5-year"', add
label define sample_lbl 201205 `"2008-2012, ACS 5-year"', add
label define sample_lbl 201204 `"2010-2012, PRCS 3-year"', add
label define sample_lbl 201203 `"2010-2012, ACS 3-year"', add
label define sample_lbl 201202 `"2012 PRCS"', add
label define sample_lbl 201201 `"2012 ACS"', add
label define sample_lbl 201106 `"2007-2011, PRCS 5-year"', add
label define sample_lbl 201105 `"2007-2011, ACS 5-year"', add
label define sample_lbl 201104 `"2009-2011, PRCS 3-year"', add
label define sample_lbl 201103 `"2009-2011, ACS 3-year"', add
label define sample_lbl 201102 `"2011 PRCS"', add
label define sample_lbl 201101 `"2011 ACS"', add
label define sample_lbl 201008 `"2010 Puerto Rico 10%"', add
label define sample_lbl 201007 `"2010 10%"', add
label define sample_lbl 201006 `"2006-2010, PRCS 5-year"', add
label define sample_lbl 201005 `"2006-2010, ACS 5-year"', add
label define sample_lbl 201004 `"2008-2010, PRCS 3-year"', add
label define sample_lbl 201003 `"2008-2010, ACS 3-year"', add
label define sample_lbl 201002 `"2010 PRCS"', add
label define sample_lbl 201001 `"2010 ACS"', add
label define sample_lbl 200906 `"2005-2009, PRCS 5-year"', add
label define sample_lbl 200905 `"2005-2009, ACS 5-year"', add
label define sample_lbl 200904 `"2007-2009, PRCS 3-year"', add
label define sample_lbl 200903 `"2007-2009, ACS 3-year"', add
label define sample_lbl 200902 `"2009 PRCS"', add
label define sample_lbl 200901 `"2009 ACS"', add
label define sample_lbl 200804 `"2006-2008, PRCS 3-year"', add
label define sample_lbl 200803 `"2006-2008, ACS 3-year"', add
label define sample_lbl 200802 `"2008 PRCS"', add
label define sample_lbl 200801 `"2008 ACS"', add
label define sample_lbl 200704 `"2005-2007, PRCS 3-year"', add
label define sample_lbl 200703 `"2005-2007, ACS 3-year"', add
label define sample_lbl 200702 `"2007 PRCS"', add
label define sample_lbl 200701 `"2007 ACS"', add
label define sample_lbl 200602 `"2006 PRCS"', add
label define sample_lbl 200601 `"2006 ACS"', add
label define sample_lbl 200502 `"2005 PRCS"', add
label define sample_lbl 200501 `"2005 ACS"', add
label define sample_lbl 200401 `"2004 ACS"', add
label define sample_lbl 200301 `"2003 ACS"', add
label define sample_lbl 200201 `"2002 ACS"', add
label define sample_lbl 200101 `"2001 ACS"', add
label define sample_lbl 200008 `"2000 Puerto Rico 1%"', add
label define sample_lbl 200007 `"2000 1%"', add
label define sample_lbl 200006 `"2000 Puerto Rico 1% sample (old version)"', add
label define sample_lbl 200005 `"2000 Puerto Rico 5%"', add
label define sample_lbl 200004 `"2000 ACS"', add
label define sample_lbl 200003 `"2000 Unweighted 1%"', add
label define sample_lbl 200002 `"2000 1% sample (old version)"', add
label define sample_lbl 200001 `"2000 5%"', add
label define sample_lbl 199007 `"1990 Puerto Rico 1%"', add
label define sample_lbl 199006 `"1990 Puerto Rico 5%"', add
label define sample_lbl 199005 `"1990 Labor Market Area"', add
label define sample_lbl 199004 `"1990 Elderly"', add
label define sample_lbl 199003 `"1990 Unweighted 1%"', add
label define sample_lbl 199002 `"1990 1%"', add
label define sample_lbl 199001 `"1990 5%"', add
label define sample_lbl 198007 `"1980 Puerto Rico 1%"', add
label define sample_lbl 198006 `"1980 Puerto Rico 5%"', add
label define sample_lbl 198005 `"1980 Detailed metro/non-metro"', add
label define sample_lbl 198004 `"1980 Labor Market Area"', add
label define sample_lbl 198003 `"1980 Urban/Rural"', add
label define sample_lbl 198002 `"1980 1%"', add
label define sample_lbl 198001 `"1980 5%"', add
label define sample_lbl 197009 `"1970 Puerto Rico Neighborhood"', add
label define sample_lbl 197008 `"1970 Puerto Rico Municipio"', add
label define sample_lbl 197007 `"1970 Puerto Rico State"', add
label define sample_lbl 197006 `"1970 Form 2 Neighborhood"', add
label define sample_lbl 197005 `"1970 Form 1 Neighborhood"', add
label define sample_lbl 197004 `"1970 Form 2 Metro"', add
label define sample_lbl 197003 `"1970 Form 1 Metro"', add
label define sample_lbl 197002 `"1970 Form 2 State"', add
label define sample_lbl 197001 `"1970 Form 1 State"', add
label define sample_lbl 196002 `"1960 5%"', add
label define sample_lbl 196001 `"1960 1%"', add
label define sample_lbl 195002 `"1950 100% database"', add
label define sample_lbl 195001 `"1950 1%"', add
label define sample_lbl 194002 `"1940 100% database"', add
label define sample_lbl 194001 `"1940 1%"', add
label define sample_lbl 193004 `"1930 100% database"', add
label define sample_lbl 193003 `"1930 Puerto Rico"', add
label define sample_lbl 193002 `"1930 5%"', add
label define sample_lbl 193001 `"1930 1%"', add
label define sample_lbl 192003 `"1920 100% database"', add
label define sample_lbl 192002 `"1920 Puerto Rico sample"', add
label define sample_lbl 192001 `"1920 1%"', add
label define sample_lbl 191004 `"1910 100% database"', add
label define sample_lbl 191003 `"1910 1.4% sample with oversamples"', add
label define sample_lbl 191002 `"1910 1%"', add
label define sample_lbl 191001 `"1910 Puerto Rico"', add
label define sample_lbl 190004 `"1900 100% database"', add
label define sample_lbl 190003 `"1900 1% sample with oversamples"', add
label define sample_lbl 190002 `"1900 1%"', add
label define sample_lbl 190001 `"1900 5%"', add
label define sample_lbl 188003 `"1880 100% database"', add
label define sample_lbl 188002 `"1880 10%"', add
label define sample_lbl 188001 `"1880 1%"', add
label define sample_lbl 187003 `"1870 100% database"', add
label define sample_lbl 187002 `"1870 1% sample with black oversample"', add
label define sample_lbl 187001 `"1870 1%"', add
label define sample_lbl 186003 `"1860 100% database"', add
label define sample_lbl 186002 `"1860 1% sample with black oversample"', add
label define sample_lbl 186001 `"1860 1%"', add
label define sample_lbl 185002 `"1850 100% database"', add
label define sample_lbl 185001 `"1850 1%"', add
label values sample sample_lbl

label define hhtype_lbl 0 `"N/A"'
label define hhtype_lbl 1 `"Married-couple family household"', add
label define hhtype_lbl 2 `"Male householder, no wife present"', add
label define hhtype_lbl 3 `"Female householder, no husband present"', add
label define hhtype_lbl 4 `"Male householder, living alone"', add
label define hhtype_lbl 5 `"Male householder, not living alone"', add
label define hhtype_lbl 6 `"Female householder, living alone"', add
label define hhtype_lbl 7 `"Female householder, not living alone"', add
label define hhtype_lbl 9 `"HHTYPE could not be determined"', add
label values hhtype hhtype_lbl

label define repwt_lbl 0 `"Repwt not available"'
label define repwt_lbl 1 `"Repwt available"', add
label values repwt repwt_lbl

label define region_lbl 11 `"New England Division"'
label define region_lbl 12 `"Middle Atlantic Division"', add
label define region_lbl 13 `"Mixed Northeast Divisions (1970 Metro)"', add
label define region_lbl 21 `"East North Central Div."', add
label define region_lbl 22 `"West North Central Div."', add
label define region_lbl 23 `"Mixed Midwest Divisions (1970 Metro)"', add
label define region_lbl 31 `"South Atlantic Division"', add
label define region_lbl 32 `"East South Central Div."', add
label define region_lbl 33 `"West South Central Div."', add
label define region_lbl 34 `"Mixed Southern Divisions (1970 Metro)"', add
label define region_lbl 41 `"Mountain Division"', add
label define region_lbl 42 `"Pacific Division"', add
label define region_lbl 43 `"Mixed Western Divisions (1970 Metro)"', add
label define region_lbl 91 `"Military/Military reservations"', add
label define region_lbl 92 `"PUMA boundaries cross state lines-1% sample"', add
label define region_lbl 97 `"State not identified"', add
label define region_lbl 99 `"Not identified"', add
label values region region_lbl

label define stateicp_lbl 01 `"Connecticut"'
label define stateicp_lbl 02 `"Maine"', add
label define stateicp_lbl 03 `"Massachusetts"', add
label define stateicp_lbl 04 `"New Hampshire"', add
label define stateicp_lbl 05 `"Rhode Island"', add
label define stateicp_lbl 06 `"Vermont"', add
label define stateicp_lbl 11 `"Delaware"', add
label define stateicp_lbl 12 `"New Jersey"', add
label define stateicp_lbl 13 `"New York"', add
label define stateicp_lbl 14 `"Pennsylvania"', add
label define stateicp_lbl 21 `"Illinois"', add
label define stateicp_lbl 22 `"Indiana"', add
label define stateicp_lbl 23 `"Michigan"', add
label define stateicp_lbl 24 `"Ohio"', add
label define stateicp_lbl 25 `"Wisconsin"', add
label define stateicp_lbl 31 `"Iowa"', add
label define stateicp_lbl 32 `"Kansas"', add
label define stateicp_lbl 33 `"Minnesota"', add
label define stateicp_lbl 34 `"Missouri"', add
label define stateicp_lbl 35 `"Nebraska"', add
label define stateicp_lbl 36 `"North Dakota"', add
label define stateicp_lbl 37 `"South Dakota"', add
label define stateicp_lbl 40 `"Virginia"', add
label define stateicp_lbl 41 `"Alabama"', add
label define stateicp_lbl 42 `"Arkansas"', add
label define stateicp_lbl 43 `"Florida"', add
label define stateicp_lbl 44 `"Georgia"', add
label define stateicp_lbl 45 `"Louisiana"', add
label define stateicp_lbl 46 `"Mississippi"', add
label define stateicp_lbl 47 `"North Carolina"', add
label define stateicp_lbl 48 `"South Carolina"', add
label define stateicp_lbl 49 `"Texas"', add
label define stateicp_lbl 51 `"Kentucky"', add
label define stateicp_lbl 52 `"Maryland"', add
label define stateicp_lbl 53 `"Oklahoma"', add
label define stateicp_lbl 54 `"Tennessee"', add
label define stateicp_lbl 56 `"West Virginia"', add
label define stateicp_lbl 61 `"Arizona"', add
label define stateicp_lbl 62 `"Colorado"', add
label define stateicp_lbl 63 `"Idaho"', add
label define stateicp_lbl 64 `"Montana"', add
label define stateicp_lbl 65 `"Nevada"', add
label define stateicp_lbl 66 `"New Mexico"', add
label define stateicp_lbl 67 `"Utah"', add
label define stateicp_lbl 68 `"Wyoming"', add
label define stateicp_lbl 71 `"California"', add
label define stateicp_lbl 72 `"Oregon"', add
label define stateicp_lbl 73 `"Washington"', add
label define stateicp_lbl 81 `"Alaska"', add
label define stateicp_lbl 82 `"Hawaii"', add
label define stateicp_lbl 83 `"Puerto Rico"', add
label define stateicp_lbl 96 `"State groupings (1980 Urban/rural sample)"', add
label define stateicp_lbl 97 `"Military/Mil. Reservations"', add
label define stateicp_lbl 98 `"District of Columbia"', add
label define stateicp_lbl 99 `"State not identified"', add
label values stateicp stateicp_lbl

label define statefip_lbl 01 `"Alabama"'
label define statefip_lbl 02 `"Alaska"', add
label define statefip_lbl 04 `"Arizona"', add
label define statefip_lbl 05 `"Arkansas"', add
label define statefip_lbl 06 `"California"', add
label define statefip_lbl 08 `"Colorado"', add
label define statefip_lbl 09 `"Connecticut"', add
label define statefip_lbl 10 `"Delaware"', add
label define statefip_lbl 11 `"District of Columbia"', add
label define statefip_lbl 12 `"Florida"', add
label define statefip_lbl 13 `"Georgia"', add
label define statefip_lbl 15 `"Hawaii"', add
label define statefip_lbl 16 `"Idaho"', add
label define statefip_lbl 17 `"Illinois"', add
label define statefip_lbl 18 `"Indiana"', add
label define statefip_lbl 19 `"Iowa"', add
label define statefip_lbl 20 `"Kansas"', add
label define statefip_lbl 21 `"Kentucky"', add
label define statefip_lbl 22 `"Louisiana"', add
label define statefip_lbl 23 `"Maine"', add
label define statefip_lbl 24 `"Maryland"', add
label define statefip_lbl 25 `"Massachusetts"', add
label define statefip_lbl 26 `"Michigan"', add
label define statefip_lbl 27 `"Minnesota"', add
label define statefip_lbl 28 `"Mississippi"', add
label define statefip_lbl 29 `"Missouri"', add
label define statefip_lbl 30 `"Montana"', add
label define statefip_lbl 31 `"Nebraska"', add
label define statefip_lbl 32 `"Nevada"', add
label define statefip_lbl 33 `"New Hampshire"', add
label define statefip_lbl 34 `"New Jersey"', add
label define statefip_lbl 35 `"New Mexico"', add
label define statefip_lbl 36 `"New York"', add
label define statefip_lbl 37 `"North Carolina"', add
label define statefip_lbl 38 `"North Dakota"', add
label define statefip_lbl 39 `"Ohio"', add
label define statefip_lbl 40 `"Oklahoma"', add
label define statefip_lbl 41 `"Oregon"', add
label define statefip_lbl 42 `"Pennsylvania"', add
label define statefip_lbl 44 `"Rhode Island"', add
label define statefip_lbl 45 `"South Carolina"', add
label define statefip_lbl 46 `"South Dakota"', add
label define statefip_lbl 47 `"Tennessee"', add
label define statefip_lbl 48 `"Texas"', add
label define statefip_lbl 49 `"Utah"', add
label define statefip_lbl 50 `"Vermont"', add
label define statefip_lbl 51 `"Virginia"', add
label define statefip_lbl 53 `"Washington"', add
label define statefip_lbl 54 `"West Virginia"', add
label define statefip_lbl 55 `"Wisconsin"', add
label define statefip_lbl 56 `"Wyoming"', add
label define statefip_lbl 61 `"Maine-New Hampshire-Vermont"', add
label define statefip_lbl 62 `"Massachusetts-Rhode Island"', add
label define statefip_lbl 63 `"Minnesota-Iowa-Missouri-Kansas-Nebraska-S.Dakota-N.Dakota"', add
label define statefip_lbl 64 `"Maryland-Delaware"', add
label define statefip_lbl 65 `"Montana-Idaho-Wyoming"', add
label define statefip_lbl 66 `"Utah-Nevada"', add
label define statefip_lbl 67 `"Arizona-New Mexico"', add
label define statefip_lbl 68 `"Alaska-Hawaii"', add
label define statefip_lbl 72 `"Puerto Rico"', add
label define statefip_lbl 97 `"Military/Mil. Reservation"', add
label define statefip_lbl 99 `"State not identified"', add
label values statefip statefip_lbl

label define countyicp_lbl 0010 `"0010"'
label define countyicp_lbl 0030 `"0030"', add
label define countyicp_lbl 0050 `"0050"', add
label define countyicp_lbl 0070 `"0070"', add
label define countyicp_lbl 0090 `"0090"', add
label define countyicp_lbl 0110 `"0110"', add
label define countyicp_lbl 0130 `"0130"', add
label define countyicp_lbl 0150 `"0150"', add
label define countyicp_lbl 0170 `"0170"', add
label define countyicp_lbl 0190 `"0190"', add
label define countyicp_lbl 0200 `"0200"', add
label define countyicp_lbl 0205 `"0205"', add
label define countyicp_lbl 0210 `"0210"', add
label define countyicp_lbl 0230 `"0230"', add
label define countyicp_lbl 0250 `"0250"', add
label define countyicp_lbl 0270 `"0270"', add
label define countyicp_lbl 0290 `"0290"', add
label define countyicp_lbl 0310 `"0310"', add
label define countyicp_lbl 0330 `"0330"', add
label define countyicp_lbl 0350 `"0350"', add
label define countyicp_lbl 0360 `"0360"', add
label define countyicp_lbl 0370 `"0370"', add
label define countyicp_lbl 0390 `"0390"', add
label define countyicp_lbl 0410 `"0410"', add
label define countyicp_lbl 0430 `"0430"', add
label define countyicp_lbl 0450 `"0450"', add
label define countyicp_lbl 0455 `"0455"', add
label define countyicp_lbl 0470 `"0470"', add
label define countyicp_lbl 0490 `"0490"', add
label define countyicp_lbl 0510 `"0510"', add
label define countyicp_lbl 0530 `"0530"', add
label define countyicp_lbl 0550 `"0550"', add
label define countyicp_lbl 0570 `"0570"', add
label define countyicp_lbl 0590 `"0590"', add
label define countyicp_lbl 0605 `"0605"', add
label define countyicp_lbl 0610 `"0610"', add
label define countyicp_lbl 0630 `"0630"', add
label define countyicp_lbl 0650 `"0650"', add
label define countyicp_lbl 0670 `"0670"', add
label define countyicp_lbl 0690 `"0690"', add
label define countyicp_lbl 0710 `"0710"', add
label define countyicp_lbl 0730 `"0730"', add
label define countyicp_lbl 0750 `"0750"', add
label define countyicp_lbl 0770 `"0770"', add
label define countyicp_lbl 0790 `"0790"', add
label define countyicp_lbl 0810 `"0810"', add
label define countyicp_lbl 0830 `"0830"', add
label define countyicp_lbl 0850 `"0850"', add
label define countyicp_lbl 0870 `"0870"', add
label define countyicp_lbl 0890 `"0890"', add
label define countyicp_lbl 0910 `"0910"', add
label define countyicp_lbl 0930 `"0930"', add
label define countyicp_lbl 0950 `"0950"', add
label define countyicp_lbl 0970 `"0970"', add
label define countyicp_lbl 0990 `"0990"', add
label define countyicp_lbl 1010 `"1010"', add
label define countyicp_lbl 1030 `"1030"', add
label define countyicp_lbl 1050 `"1050"', add
label define countyicp_lbl 1070 `"1070"', add
label define countyicp_lbl 1090 `"1090"', add
label define countyicp_lbl 1110 `"1110"', add
label define countyicp_lbl 1130 `"1130"', add
label define countyicp_lbl 1150 `"1150"', add
label define countyicp_lbl 1170 `"1170"', add
label define countyicp_lbl 1190 `"1190"', add
label define countyicp_lbl 1210 `"1210"', add
label define countyicp_lbl 1230 `"1230"', add
label define countyicp_lbl 1250 `"1250"', add
label define countyicp_lbl 1270 `"1270"', add
label define countyicp_lbl 1290 `"1290"', add
label define countyicp_lbl 1310 `"1310"', add
label define countyicp_lbl 1330 `"1330"', add
label define countyicp_lbl 1350 `"1350"', add
label define countyicp_lbl 1370 `"1370"', add
label define countyicp_lbl 1390 `"1390"', add
label define countyicp_lbl 1410 `"1410"', add
label define countyicp_lbl 1430 `"1430"', add
label define countyicp_lbl 1450 `"1450"', add
label define countyicp_lbl 1470 `"1470"', add
label define countyicp_lbl 1490 `"1490"', add
label define countyicp_lbl 1510 `"1510"', add
label define countyicp_lbl 1530 `"1530"', add
label define countyicp_lbl 1550 `"1550"', add
label define countyicp_lbl 1570 `"1570"', add
label define countyicp_lbl 1590 `"1590"', add
label define countyicp_lbl 1610 `"1610"', add
label define countyicp_lbl 1630 `"1630"', add
label define countyicp_lbl 1650 `"1650"', add
label define countyicp_lbl 1670 `"1670"', add
label define countyicp_lbl 1690 `"1690"', add
label define countyicp_lbl 1710 `"1710"', add
label define countyicp_lbl 1730 `"1730"', add
label define countyicp_lbl 1750 `"1750"', add
label define countyicp_lbl 1770 `"1770"', add
label define countyicp_lbl 1790 `"1790"', add
label define countyicp_lbl 1810 `"1810"', add
label define countyicp_lbl 1830 `"1830"', add
label define countyicp_lbl 1850 `"1850"', add
label define countyicp_lbl 1870 `"1870"', add
label define countyicp_lbl 1875 `"1875"', add
label define countyicp_lbl 1890 `"1890"', add
label define countyicp_lbl 1910 `"1910"', add
label define countyicp_lbl 1930 `"1930"', add
label define countyicp_lbl 1950 `"1950"', add
label define countyicp_lbl 1970 `"1970"', add
label define countyicp_lbl 1990 `"1990"', add
label define countyicp_lbl 2010 `"2010"', add
label define countyicp_lbl 2030 `"2030"', add
label define countyicp_lbl 2050 `"2050"', add
label define countyicp_lbl 2070 `"2070"', add
label define countyicp_lbl 2090 `"2090"', add
label define countyicp_lbl 2110 `"2110"', add
label define countyicp_lbl 2130 `"2130"', add
label define countyicp_lbl 2150 `"2150"', add
label define countyicp_lbl 2170 `"2170"', add
label define countyicp_lbl 2190 `"2190"', add
label define countyicp_lbl 2210 `"2210"', add
label define countyicp_lbl 2230 `"2230"', add
label define countyicp_lbl 2250 `"2250"', add
label define countyicp_lbl 2270 `"2270"', add
label define countyicp_lbl 2290 `"2290"', add
label define countyicp_lbl 2310 `"2310"', add
label define countyicp_lbl 2330 `"2330"', add
label define countyicp_lbl 2350 `"2350"', add
label define countyicp_lbl 2370 `"2370"', add
label define countyicp_lbl 2390 `"2390"', add
label define countyicp_lbl 2410 `"2410"', add
label define countyicp_lbl 2430 `"2430"', add
label define countyicp_lbl 2450 `"2450"', add
label define countyicp_lbl 2470 `"2470"', add
label define countyicp_lbl 2490 `"2490"', add
label define countyicp_lbl 2510 `"2510"', add
label define countyicp_lbl 2530 `"2530"', add
label define countyicp_lbl 2550 `"2550"', add
label define countyicp_lbl 2570 `"2570"', add
label define countyicp_lbl 2590 `"2590"', add
label define countyicp_lbl 2610 `"2610"', add
label define countyicp_lbl 2630 `"2630"', add
label define countyicp_lbl 2650 `"2650"', add
label define countyicp_lbl 2670 `"2670"', add
label define countyicp_lbl 2690 `"2690"', add
label define countyicp_lbl 2710 `"2710"', add
label define countyicp_lbl 2730 `"2730"', add
label define countyicp_lbl 2750 `"2750"', add
label define countyicp_lbl 2770 `"2770"', add
label define countyicp_lbl 2790 `"2790"', add
label define countyicp_lbl 2810 `"2810"', add
label define countyicp_lbl 2830 `"2830"', add
label define countyicp_lbl 2850 `"2850"', add
label define countyicp_lbl 2870 `"2870"', add
label define countyicp_lbl 2890 `"2890"', add
label define countyicp_lbl 2910 `"2910"', add
label define countyicp_lbl 2930 `"2930"', add
label define countyicp_lbl 2950 `"2950"', add
label define countyicp_lbl 2970 `"2970"', add
label define countyicp_lbl 2990 `"2990"', add
label define countyicp_lbl 3010 `"3010"', add
label define countyicp_lbl 3030 `"3030"', add
label define countyicp_lbl 3050 `"3050"', add
label define countyicp_lbl 3070 `"3070"', add
label define countyicp_lbl 3090 `"3090"', add
label define countyicp_lbl 3110 `"3110"', add
label define countyicp_lbl 3130 `"3130"', add
label define countyicp_lbl 3150 `"3150"', add
label define countyicp_lbl 3170 `"3170"', add
label define countyicp_lbl 3190 `"3190"', add
label define countyicp_lbl 3210 `"3210"', add
label define countyicp_lbl 3230 `"3230"', add
label define countyicp_lbl 3250 `"3250"', add
label define countyicp_lbl 3270 `"3270"', add
label define countyicp_lbl 3290 `"3290"', add
label define countyicp_lbl 3310 `"3310"', add
label define countyicp_lbl 3330 `"3330"', add
label define countyicp_lbl 3350 `"3350"', add
label define countyicp_lbl 3370 `"3370"', add
label define countyicp_lbl 3390 `"3390"', add
label define countyicp_lbl 3410 `"3410"', add
label define countyicp_lbl 3430 `"3430"', add
label define countyicp_lbl 3450 `"3450"', add
label define countyicp_lbl 3470 `"3470"', add
label define countyicp_lbl 3490 `"3490"', add
label define countyicp_lbl 3510 `"3510"', add
label define countyicp_lbl 3530 `"3530"', add
label define countyicp_lbl 3550 `"3550"', add
label define countyicp_lbl 3570 `"3570"', add
label define countyicp_lbl 3590 `"3590"', add
label define countyicp_lbl 3610 `"3610"', add
label define countyicp_lbl 3630 `"3630"', add
label define countyicp_lbl 3650 `"3650"', add
label define countyicp_lbl 3670 `"3670"', add
label define countyicp_lbl 3690 `"3690"', add
label define countyicp_lbl 3710 `"3710"', add
label define countyicp_lbl 3730 `"3730"', add
label define countyicp_lbl 3750 `"3750"', add
label define countyicp_lbl 3770 `"3770"', add
label define countyicp_lbl 3790 `"3790"', add
label define countyicp_lbl 3810 `"3810"', add
label define countyicp_lbl 3830 `"3830"', add
label define countyicp_lbl 3850 `"3850"', add
label define countyicp_lbl 3870 `"3870"', add
label define countyicp_lbl 3890 `"3890"', add
label define countyicp_lbl 3910 `"3910"', add
label define countyicp_lbl 3930 `"3930"', add
label define countyicp_lbl 3950 `"3950"', add
label define countyicp_lbl 3970 `"3970"', add
label define countyicp_lbl 3990 `"3990"', add
label define countyicp_lbl 4010 `"4010"', add
label define countyicp_lbl 4030 `"4030"', add
label define countyicp_lbl 4050 `"4050"', add
label define countyicp_lbl 4070 `"4070"', add
label define countyicp_lbl 4090 `"4090"', add
label define countyicp_lbl 4110 `"4110"', add
label define countyicp_lbl 4130 `"4130"', add
label define countyicp_lbl 4150 `"4150"', add
label define countyicp_lbl 4170 `"4170"', add
label define countyicp_lbl 4190 `"4190"', add
label define countyicp_lbl 4210 `"4210"', add
label define countyicp_lbl 4230 `"4230"', add
label define countyicp_lbl 4250 `"4250"', add
label define countyicp_lbl 4270 `"4270"', add
label define countyicp_lbl 4290 `"4290"', add
label define countyicp_lbl 4310 `"4310"', add
label define countyicp_lbl 4330 `"4330"', add
label define countyicp_lbl 4350 `"4350"', add
label define countyicp_lbl 4370 `"4370"', add
label define countyicp_lbl 4390 `"4390"', add
label define countyicp_lbl 4410 `"4410"', add
label define countyicp_lbl 4430 `"4430"', add
label define countyicp_lbl 4450 `"4450"', add
label define countyicp_lbl 4470 `"4470"', add
label define countyicp_lbl 4490 `"4490"', add
label define countyicp_lbl 4510 `"4510"', add
label define countyicp_lbl 4530 `"4530"', add
label define countyicp_lbl 4550 `"4550"', add
label define countyicp_lbl 4570 `"4570"', add
label define countyicp_lbl 4590 `"4590"', add
label define countyicp_lbl 4610 `"4610"', add
label define countyicp_lbl 4630 `"4630"', add
label define countyicp_lbl 4650 `"4650"', add
label define countyicp_lbl 4670 `"4670"', add
label define countyicp_lbl 4690 `"4690"', add
label define countyicp_lbl 4710 `"4710"', add
label define countyicp_lbl 4730 `"4730"', add
label define countyicp_lbl 4750 `"4750"', add
label define countyicp_lbl 4770 `"4770"', add
label define countyicp_lbl 4790 `"4790"', add
label define countyicp_lbl 4810 `"4810"', add
label define countyicp_lbl 4830 `"4830"', add
label define countyicp_lbl 4850 `"4850"', add
label define countyicp_lbl 4870 `"4870"', add
label define countyicp_lbl 4890 `"4890"', add
label define countyicp_lbl 4910 `"4910"', add
label define countyicp_lbl 4930 `"4930"', add
label define countyicp_lbl 4950 `"4950"', add
label define countyicp_lbl 4970 `"4970"', add
label define countyicp_lbl 4990 `"4990"', add
label define countyicp_lbl 5010 `"5010"', add
label define countyicp_lbl 5030 `"5030"', add
label define countyicp_lbl 5050 `"5050"', add
label define countyicp_lbl 5070 `"5070"', add
label define countyicp_lbl 5100 `"5100"', add
label define countyicp_lbl 5200 `"5200"', add
label define countyicp_lbl 5300 `"5300"', add
label define countyicp_lbl 5400 `"5400"', add
label define countyicp_lbl 5500 `"5500"', add
label define countyicp_lbl 5600 `"5600"', add
label define countyicp_lbl 5700 `"5700"', add
label define countyicp_lbl 5800 `"5800"', add
label define countyicp_lbl 5900 `"5900"', add
label define countyicp_lbl 6100 `"6100"', add
label define countyicp_lbl 6300 `"6300"', add
label define countyicp_lbl 6400 `"6400"', add
label define countyicp_lbl 6500 `"6500"', add
label define countyicp_lbl 6600 `"6600"', add
label define countyicp_lbl 6700 `"6700"', add
label define countyicp_lbl 6800 `"6800"', add
label define countyicp_lbl 6900 `"6900"', add
label define countyicp_lbl 7000 `"7000"', add
label define countyicp_lbl 7100 `"7100"', add
label define countyicp_lbl 7200 `"7200"', add
label define countyicp_lbl 7300 `"7300"', add
label define countyicp_lbl 7400 `"7400"', add
label define countyicp_lbl 7500 `"7500"', add
label define countyicp_lbl 7600 `"7600"', add
label define countyicp_lbl 7700 `"7700"', add
label define countyicp_lbl 7800 `"7800"', add
label define countyicp_lbl 7850 `"7850"', add
label define countyicp_lbl 7900 `"7900"', add
label define countyicp_lbl 8000 `"8000"', add
label define countyicp_lbl 8100 `"8100"', add
label define countyicp_lbl 8200 `"8200"', add
label define countyicp_lbl 8300 `"8300"', add
label define countyicp_lbl 8400 `"8400"', add
label values countyicp countyicp_lbl

label define cpuma0010_lbl 0001 `"0001"'
label define cpuma0010_lbl 0002 `"0002"', add
label define cpuma0010_lbl 0003 `"0003"', add
label define cpuma0010_lbl 0004 `"0004"', add
label define cpuma0010_lbl 0005 `"0005"', add
label define cpuma0010_lbl 0006 `"0006"', add
label define cpuma0010_lbl 0007 `"0007"', add
label define cpuma0010_lbl 0008 `"0008"', add
label define cpuma0010_lbl 0009 `"0009"', add
label define cpuma0010_lbl 0010 `"0010"', add
label define cpuma0010_lbl 0011 `"0011"', add
label define cpuma0010_lbl 0012 `"0012"', add
label define cpuma0010_lbl 0013 `"0013"', add
label define cpuma0010_lbl 0014 `"0014"', add
label define cpuma0010_lbl 0015 `"0015"', add
label define cpuma0010_lbl 0016 `"0016"', add
label define cpuma0010_lbl 0017 `"0017"', add
label define cpuma0010_lbl 0018 `"0018"', add
label define cpuma0010_lbl 0019 `"0019"', add
label define cpuma0010_lbl 0020 `"0020"', add
label define cpuma0010_lbl 0021 `"0021"', add
label define cpuma0010_lbl 0022 `"0022"', add
label define cpuma0010_lbl 0023 `"0023"', add
label define cpuma0010_lbl 0024 `"0024"', add
label define cpuma0010_lbl 0025 `"0025"', add
label define cpuma0010_lbl 0026 `"0026"', add
label define cpuma0010_lbl 0027 `"0027"', add
label define cpuma0010_lbl 0028 `"0028"', add
label define cpuma0010_lbl 0029 `"0029"', add
label define cpuma0010_lbl 0030 `"0030"', add
label define cpuma0010_lbl 0031 `"0031"', add
label define cpuma0010_lbl 0032 `"0032"', add
label define cpuma0010_lbl 0033 `"0033"', add
label define cpuma0010_lbl 0034 `"0034"', add
label define cpuma0010_lbl 0035 `"0035"', add
label define cpuma0010_lbl 0036 `"0036"', add
label define cpuma0010_lbl 0037 `"0037"', add
label define cpuma0010_lbl 0038 `"0038"', add
label define cpuma0010_lbl 0039 `"0039"', add
label define cpuma0010_lbl 0040 `"0040"', add
label define cpuma0010_lbl 0041 `"0041"', add
label define cpuma0010_lbl 0042 `"0042"', add
label define cpuma0010_lbl 0043 `"0043"', add
label define cpuma0010_lbl 0044 `"0044"', add
label define cpuma0010_lbl 0045 `"0045"', add
label define cpuma0010_lbl 0046 `"0046"', add
label define cpuma0010_lbl 0047 `"0047"', add
label define cpuma0010_lbl 0048 `"0048"', add
label define cpuma0010_lbl 0049 `"0049"', add
label define cpuma0010_lbl 0050 `"0050"', add
label define cpuma0010_lbl 0051 `"0051"', add
label define cpuma0010_lbl 0052 `"0052"', add
label define cpuma0010_lbl 0053 `"0053"', add
label define cpuma0010_lbl 0054 `"0054"', add
label define cpuma0010_lbl 0055 `"0055"', add
label define cpuma0010_lbl 0056 `"0056"', add
label define cpuma0010_lbl 0057 `"0057"', add
label define cpuma0010_lbl 0058 `"0058"', add
label define cpuma0010_lbl 0059 `"0059"', add
label define cpuma0010_lbl 0060 `"0060"', add
label define cpuma0010_lbl 0061 `"0061"', add
label define cpuma0010_lbl 0062 `"0062"', add
label define cpuma0010_lbl 0063 `"0063"', add
label define cpuma0010_lbl 0064 `"0064"', add
label define cpuma0010_lbl 0065 `"0065"', add
label define cpuma0010_lbl 0066 `"0066"', add
label define cpuma0010_lbl 0067 `"0067"', add
label define cpuma0010_lbl 0068 `"0068"', add
label define cpuma0010_lbl 0069 `"0069"', add
label define cpuma0010_lbl 0070 `"0070"', add
label define cpuma0010_lbl 0071 `"0071"', add
label define cpuma0010_lbl 0072 `"0072"', add
label define cpuma0010_lbl 0073 `"0073"', add
label define cpuma0010_lbl 0074 `"0074"', add
label define cpuma0010_lbl 0075 `"0075"', add
label define cpuma0010_lbl 0076 `"0076"', add
label define cpuma0010_lbl 0077 `"0077"', add
label define cpuma0010_lbl 0078 `"0078"', add
label define cpuma0010_lbl 0079 `"0079"', add
label define cpuma0010_lbl 0080 `"0080"', add
label define cpuma0010_lbl 0081 `"0081"', add
label define cpuma0010_lbl 0082 `"0082"', add
label define cpuma0010_lbl 0083 `"0083"', add
label define cpuma0010_lbl 0084 `"0084"', add
label define cpuma0010_lbl 0085 `"0085"', add
label define cpuma0010_lbl 0086 `"0086"', add
label define cpuma0010_lbl 0087 `"0087"', add
label define cpuma0010_lbl 0088 `"0088"', add
label define cpuma0010_lbl 0089 `"0089"', add
label define cpuma0010_lbl 0090 `"0090"', add
label define cpuma0010_lbl 0091 `"0091"', add
label define cpuma0010_lbl 0092 `"0092"', add
label define cpuma0010_lbl 0093 `"0093"', add
label define cpuma0010_lbl 0094 `"0094"', add
label define cpuma0010_lbl 0095 `"0095"', add
label define cpuma0010_lbl 0096 `"0096"', add
label define cpuma0010_lbl 0097 `"0097"', add
label define cpuma0010_lbl 0098 `"0098"', add
label define cpuma0010_lbl 0099 `"0099"', add
label define cpuma0010_lbl 0100 `"0100"', add
label define cpuma0010_lbl 0101 `"0101"', add
label define cpuma0010_lbl 0102 `"0102"', add
label define cpuma0010_lbl 0103 `"0103"', add
label define cpuma0010_lbl 0104 `"0104"', add
label define cpuma0010_lbl 0105 `"0105"', add
label define cpuma0010_lbl 0106 `"0106"', add
label define cpuma0010_lbl 0107 `"0107"', add
label define cpuma0010_lbl 0108 `"0108"', add
label define cpuma0010_lbl 0109 `"0109"', add
label define cpuma0010_lbl 0110 `"0110"', add
label define cpuma0010_lbl 0111 `"0111"', add
label define cpuma0010_lbl 0112 `"0112"', add
label define cpuma0010_lbl 0113 `"0113"', add
label define cpuma0010_lbl 0114 `"0114"', add
label define cpuma0010_lbl 0115 `"0115"', add
label define cpuma0010_lbl 0116 `"0116"', add
label define cpuma0010_lbl 0117 `"0117"', add
label define cpuma0010_lbl 0118 `"0118"', add
label define cpuma0010_lbl 0119 `"0119"', add
label define cpuma0010_lbl 0120 `"0120"', add
label define cpuma0010_lbl 0121 `"0121"', add
label define cpuma0010_lbl 0122 `"0122"', add
label define cpuma0010_lbl 0123 `"0123"', add
label define cpuma0010_lbl 0124 `"0124"', add
label define cpuma0010_lbl 0125 `"0125"', add
label define cpuma0010_lbl 0126 `"0126"', add
label define cpuma0010_lbl 0127 `"0127"', add
label define cpuma0010_lbl 0128 `"0128"', add
label define cpuma0010_lbl 0129 `"0129"', add
label define cpuma0010_lbl 0130 `"0130"', add
label define cpuma0010_lbl 0131 `"0131"', add
label define cpuma0010_lbl 0132 `"0132"', add
label define cpuma0010_lbl 0133 `"0133"', add
label define cpuma0010_lbl 0134 `"0134"', add
label define cpuma0010_lbl 0135 `"0135"', add
label define cpuma0010_lbl 0136 `"0136"', add
label define cpuma0010_lbl 0137 `"0137"', add
label define cpuma0010_lbl 0138 `"0138"', add
label define cpuma0010_lbl 0139 `"0139"', add
label define cpuma0010_lbl 0140 `"0140"', add
label define cpuma0010_lbl 0141 `"0141"', add
label define cpuma0010_lbl 0142 `"0142"', add
label define cpuma0010_lbl 0143 `"0143"', add
label define cpuma0010_lbl 0144 `"0144"', add
label define cpuma0010_lbl 0145 `"0145"', add
label define cpuma0010_lbl 0146 `"0146"', add
label define cpuma0010_lbl 0147 `"0147"', add
label define cpuma0010_lbl 0148 `"0148"', add
label define cpuma0010_lbl 0149 `"0149"', add
label define cpuma0010_lbl 0150 `"0150"', add
label define cpuma0010_lbl 0151 `"0151"', add
label define cpuma0010_lbl 0152 `"0152"', add
label define cpuma0010_lbl 0153 `"0153"', add
label define cpuma0010_lbl 0154 `"0154"', add
label define cpuma0010_lbl 0155 `"0155"', add
label define cpuma0010_lbl 0156 `"0156"', add
label define cpuma0010_lbl 0157 `"0157"', add
label define cpuma0010_lbl 0158 `"0158"', add
label define cpuma0010_lbl 0159 `"0159"', add
label define cpuma0010_lbl 0160 `"0160"', add
label define cpuma0010_lbl 0161 `"0161"', add
label define cpuma0010_lbl 0162 `"0162"', add
label define cpuma0010_lbl 0163 `"0163"', add
label define cpuma0010_lbl 0164 `"0164"', add
label define cpuma0010_lbl 0165 `"0165"', add
label define cpuma0010_lbl 0166 `"0166"', add
label define cpuma0010_lbl 0167 `"0167"', add
label define cpuma0010_lbl 0168 `"0168"', add
label define cpuma0010_lbl 0169 `"0169"', add
label define cpuma0010_lbl 0170 `"0170"', add
label define cpuma0010_lbl 0171 `"0171"', add
label define cpuma0010_lbl 0172 `"0172"', add
label define cpuma0010_lbl 0173 `"0173"', add
label define cpuma0010_lbl 0174 `"0174"', add
label define cpuma0010_lbl 0175 `"0175"', add
label define cpuma0010_lbl 0176 `"0176"', add
label define cpuma0010_lbl 0177 `"0177"', add
label define cpuma0010_lbl 0178 `"0178"', add
label define cpuma0010_lbl 0179 `"0179"', add
label define cpuma0010_lbl 0180 `"0180"', add
label define cpuma0010_lbl 0181 `"0181"', add
label define cpuma0010_lbl 0182 `"0182"', add
label define cpuma0010_lbl 0183 `"0183"', add
label define cpuma0010_lbl 0184 `"0184"', add
label define cpuma0010_lbl 0185 `"0185"', add
label define cpuma0010_lbl 0186 `"0186"', add
label define cpuma0010_lbl 0187 `"0187"', add
label define cpuma0010_lbl 0188 `"0188"', add
label define cpuma0010_lbl 0189 `"0189"', add
label define cpuma0010_lbl 0190 `"0190"', add
label define cpuma0010_lbl 0191 `"0191"', add
label define cpuma0010_lbl 0192 `"0192"', add
label define cpuma0010_lbl 0193 `"0193"', add
label define cpuma0010_lbl 0194 `"0194"', add
label define cpuma0010_lbl 0195 `"0195"', add
label define cpuma0010_lbl 0196 `"0196"', add
label define cpuma0010_lbl 0197 `"0197"', add
label define cpuma0010_lbl 0198 `"0198"', add
label define cpuma0010_lbl 0199 `"0199"', add
label define cpuma0010_lbl 0200 `"0200"', add
label define cpuma0010_lbl 0201 `"0201"', add
label define cpuma0010_lbl 0202 `"0202"', add
label define cpuma0010_lbl 0203 `"0203"', add
label define cpuma0010_lbl 0204 `"0204"', add
label define cpuma0010_lbl 0205 `"0205"', add
label define cpuma0010_lbl 0206 `"0206"', add
label define cpuma0010_lbl 0207 `"0207"', add
label define cpuma0010_lbl 0208 `"0208"', add
label define cpuma0010_lbl 0209 `"0209"', add
label define cpuma0010_lbl 0210 `"0210"', add
label define cpuma0010_lbl 0211 `"0211"', add
label define cpuma0010_lbl 0212 `"0212"', add
label define cpuma0010_lbl 0213 `"0213"', add
label define cpuma0010_lbl 0214 `"0214"', add
label define cpuma0010_lbl 0215 `"0215"', add
label define cpuma0010_lbl 0216 `"0216"', add
label define cpuma0010_lbl 0217 `"0217"', add
label define cpuma0010_lbl 0218 `"0218"', add
label define cpuma0010_lbl 0219 `"0219"', add
label define cpuma0010_lbl 0220 `"0220"', add
label define cpuma0010_lbl 0221 `"0221"', add
label define cpuma0010_lbl 0222 `"0222"', add
label define cpuma0010_lbl 0223 `"0223"', add
label define cpuma0010_lbl 0224 `"0224"', add
label define cpuma0010_lbl 0225 `"0225"', add
label define cpuma0010_lbl 0226 `"0226"', add
label define cpuma0010_lbl 0227 `"0227"', add
label define cpuma0010_lbl 0228 `"0228"', add
label define cpuma0010_lbl 0229 `"0229"', add
label define cpuma0010_lbl 0230 `"0230"', add
label define cpuma0010_lbl 0231 `"0231"', add
label define cpuma0010_lbl 0232 `"0232"', add
label define cpuma0010_lbl 0233 `"0233"', add
label define cpuma0010_lbl 0234 `"0234"', add
label define cpuma0010_lbl 0235 `"0235"', add
label define cpuma0010_lbl 0236 `"0236"', add
label define cpuma0010_lbl 0237 `"0237"', add
label define cpuma0010_lbl 0238 `"0238"', add
label define cpuma0010_lbl 0239 `"0239"', add
label define cpuma0010_lbl 0240 `"0240"', add
label define cpuma0010_lbl 0241 `"0241"', add
label define cpuma0010_lbl 0242 `"0242"', add
label define cpuma0010_lbl 0243 `"0243"', add
label define cpuma0010_lbl 0244 `"0244"', add
label define cpuma0010_lbl 0245 `"0245"', add
label define cpuma0010_lbl 0246 `"0246"', add
label define cpuma0010_lbl 0247 `"0247"', add
label define cpuma0010_lbl 0248 `"0248"', add
label define cpuma0010_lbl 0249 `"0249"', add
label define cpuma0010_lbl 0250 `"0250"', add
label define cpuma0010_lbl 0251 `"0251"', add
label define cpuma0010_lbl 0252 `"0252"', add
label define cpuma0010_lbl 0253 `"0253"', add
label define cpuma0010_lbl 0254 `"0254"', add
label define cpuma0010_lbl 0255 `"0255"', add
label define cpuma0010_lbl 0256 `"0256"', add
label define cpuma0010_lbl 0257 `"0257"', add
label define cpuma0010_lbl 0258 `"0258"', add
label define cpuma0010_lbl 0259 `"0259"', add
label define cpuma0010_lbl 0260 `"0260"', add
label define cpuma0010_lbl 0261 `"0261"', add
label define cpuma0010_lbl 0262 `"0262"', add
label define cpuma0010_lbl 0263 `"0263"', add
label define cpuma0010_lbl 0264 `"0264"', add
label define cpuma0010_lbl 0265 `"0265"', add
label define cpuma0010_lbl 0266 `"0266"', add
label define cpuma0010_lbl 0267 `"0267"', add
label define cpuma0010_lbl 0268 `"0268"', add
label define cpuma0010_lbl 0269 `"0269"', add
label define cpuma0010_lbl 0270 `"0270"', add
label define cpuma0010_lbl 0271 `"0271"', add
label define cpuma0010_lbl 0272 `"0272"', add
label define cpuma0010_lbl 0273 `"0273"', add
label define cpuma0010_lbl 0274 `"0274"', add
label define cpuma0010_lbl 0275 `"0275"', add
label define cpuma0010_lbl 0276 `"0276"', add
label define cpuma0010_lbl 0277 `"0277"', add
label define cpuma0010_lbl 0278 `"0278"', add
label define cpuma0010_lbl 0279 `"0279"', add
label define cpuma0010_lbl 0280 `"0280"', add
label define cpuma0010_lbl 0281 `"0281"', add
label define cpuma0010_lbl 0282 `"0282"', add
label define cpuma0010_lbl 0283 `"0283"', add
label define cpuma0010_lbl 0284 `"0284"', add
label define cpuma0010_lbl 0285 `"0285"', add
label define cpuma0010_lbl 0286 `"0286"', add
label define cpuma0010_lbl 0287 `"0287"', add
label define cpuma0010_lbl 0288 `"0288"', add
label define cpuma0010_lbl 0289 `"0289"', add
label define cpuma0010_lbl 0290 `"0290"', add
label define cpuma0010_lbl 0291 `"0291"', add
label define cpuma0010_lbl 0292 `"0292"', add
label define cpuma0010_lbl 0293 `"0293"', add
label define cpuma0010_lbl 0294 `"0294"', add
label define cpuma0010_lbl 0295 `"0295"', add
label define cpuma0010_lbl 0296 `"0296"', add
label define cpuma0010_lbl 0297 `"0297"', add
label define cpuma0010_lbl 0298 `"0298"', add
label define cpuma0010_lbl 0299 `"0299"', add
label define cpuma0010_lbl 0300 `"0300"', add
label define cpuma0010_lbl 0301 `"0301"', add
label define cpuma0010_lbl 0302 `"0302"', add
label define cpuma0010_lbl 0303 `"0303"', add
label define cpuma0010_lbl 0304 `"0304"', add
label define cpuma0010_lbl 0305 `"0305"', add
label define cpuma0010_lbl 0306 `"0306"', add
label define cpuma0010_lbl 0307 `"0307"', add
label define cpuma0010_lbl 0308 `"0308"', add
label define cpuma0010_lbl 0309 `"0309"', add
label define cpuma0010_lbl 0310 `"0310"', add
label define cpuma0010_lbl 0311 `"0311"', add
label define cpuma0010_lbl 0312 `"0312"', add
label define cpuma0010_lbl 0313 `"0313"', add
label define cpuma0010_lbl 0314 `"0314"', add
label define cpuma0010_lbl 0315 `"0315"', add
label define cpuma0010_lbl 0316 `"0316"', add
label define cpuma0010_lbl 0317 `"0317"', add
label define cpuma0010_lbl 0318 `"0318"', add
label define cpuma0010_lbl 0319 `"0319"', add
label define cpuma0010_lbl 0320 `"0320"', add
label define cpuma0010_lbl 0321 `"0321"', add
label define cpuma0010_lbl 0322 `"0322"', add
label define cpuma0010_lbl 0323 `"0323"', add
label define cpuma0010_lbl 0324 `"0324"', add
label define cpuma0010_lbl 0325 `"0325"', add
label define cpuma0010_lbl 0326 `"0326"', add
label define cpuma0010_lbl 0327 `"0327"', add
label define cpuma0010_lbl 0328 `"0328"', add
label define cpuma0010_lbl 0329 `"0329"', add
label define cpuma0010_lbl 0330 `"0330"', add
label define cpuma0010_lbl 0331 `"0331"', add
label define cpuma0010_lbl 0332 `"0332"', add
label define cpuma0010_lbl 0333 `"0333"', add
label define cpuma0010_lbl 0334 `"0334"', add
label define cpuma0010_lbl 0335 `"0335"', add
label define cpuma0010_lbl 0336 `"0336"', add
label define cpuma0010_lbl 0337 `"0337"', add
label define cpuma0010_lbl 0338 `"0338"', add
label define cpuma0010_lbl 0339 `"0339"', add
label define cpuma0010_lbl 0340 `"0340"', add
label define cpuma0010_lbl 0341 `"0341"', add
label define cpuma0010_lbl 0342 `"0342"', add
label define cpuma0010_lbl 0343 `"0343"', add
label define cpuma0010_lbl 0344 `"0344"', add
label define cpuma0010_lbl 0345 `"0345"', add
label define cpuma0010_lbl 0346 `"0346"', add
label define cpuma0010_lbl 0347 `"0347"', add
label define cpuma0010_lbl 0348 `"0348"', add
label define cpuma0010_lbl 0349 `"0349"', add
label define cpuma0010_lbl 0350 `"0350"', add
label define cpuma0010_lbl 0351 `"0351"', add
label define cpuma0010_lbl 0352 `"0352"', add
label define cpuma0010_lbl 0353 `"0353"', add
label define cpuma0010_lbl 0354 `"0354"', add
label define cpuma0010_lbl 0355 `"0355"', add
label define cpuma0010_lbl 0356 `"0356"', add
label define cpuma0010_lbl 0357 `"0357"', add
label define cpuma0010_lbl 0358 `"0358"', add
label define cpuma0010_lbl 0359 `"0359"', add
label define cpuma0010_lbl 0360 `"0360"', add
label define cpuma0010_lbl 0361 `"0361"', add
label define cpuma0010_lbl 0362 `"0362"', add
label define cpuma0010_lbl 0363 `"0363"', add
label define cpuma0010_lbl 0364 `"0364"', add
label define cpuma0010_lbl 0365 `"0365"', add
label define cpuma0010_lbl 0366 `"0366"', add
label define cpuma0010_lbl 0367 `"0367"', add
label define cpuma0010_lbl 0368 `"0368"', add
label define cpuma0010_lbl 0369 `"0369"', add
label define cpuma0010_lbl 0370 `"0370"', add
label define cpuma0010_lbl 0371 `"0371"', add
label define cpuma0010_lbl 0372 `"0372"', add
label define cpuma0010_lbl 0373 `"0373"', add
label define cpuma0010_lbl 0374 `"0374"', add
label define cpuma0010_lbl 0375 `"0375"', add
label define cpuma0010_lbl 0376 `"0376"', add
label define cpuma0010_lbl 0377 `"0377"', add
label define cpuma0010_lbl 0378 `"0378"', add
label define cpuma0010_lbl 0379 `"0379"', add
label define cpuma0010_lbl 0380 `"0380"', add
label define cpuma0010_lbl 0381 `"0381"', add
label define cpuma0010_lbl 0382 `"0382"', add
label define cpuma0010_lbl 0383 `"0383"', add
label define cpuma0010_lbl 0384 `"0384"', add
label define cpuma0010_lbl 0385 `"0385"', add
label define cpuma0010_lbl 0386 `"0386"', add
label define cpuma0010_lbl 0387 `"0387"', add
label define cpuma0010_lbl 0388 `"0388"', add
label define cpuma0010_lbl 0389 `"0389"', add
label define cpuma0010_lbl 0390 `"0390"', add
label define cpuma0010_lbl 0391 `"0391"', add
label define cpuma0010_lbl 0392 `"0392"', add
label define cpuma0010_lbl 0393 `"0393"', add
label define cpuma0010_lbl 0394 `"0394"', add
label define cpuma0010_lbl 0395 `"0395"', add
label define cpuma0010_lbl 0396 `"0396"', add
label define cpuma0010_lbl 0397 `"0397"', add
label define cpuma0010_lbl 0398 `"0398"', add
label define cpuma0010_lbl 0399 `"0399"', add
label define cpuma0010_lbl 0400 `"0400"', add
label define cpuma0010_lbl 0401 `"0401"', add
label define cpuma0010_lbl 0402 `"0402"', add
label define cpuma0010_lbl 0403 `"0403"', add
label define cpuma0010_lbl 0404 `"0404"', add
label define cpuma0010_lbl 0405 `"0405"', add
label define cpuma0010_lbl 0406 `"0406"', add
label define cpuma0010_lbl 0407 `"0407"', add
label define cpuma0010_lbl 0408 `"0408"', add
label define cpuma0010_lbl 0409 `"0409"', add
label define cpuma0010_lbl 0410 `"0410"', add
label define cpuma0010_lbl 0411 `"0411"', add
label define cpuma0010_lbl 0412 `"0412"', add
label define cpuma0010_lbl 0413 `"0413"', add
label define cpuma0010_lbl 0414 `"0414"', add
label define cpuma0010_lbl 0415 `"0415"', add
label define cpuma0010_lbl 0416 `"0416"', add
label define cpuma0010_lbl 0417 `"0417"', add
label define cpuma0010_lbl 0418 `"0418"', add
label define cpuma0010_lbl 0419 `"0419"', add
label define cpuma0010_lbl 0420 `"0420"', add
label define cpuma0010_lbl 0421 `"0421"', add
label define cpuma0010_lbl 0422 `"0422"', add
label define cpuma0010_lbl 0423 `"0423"', add
label define cpuma0010_lbl 0424 `"0424"', add
label define cpuma0010_lbl 0425 `"0425"', add
label define cpuma0010_lbl 0426 `"0426"', add
label define cpuma0010_lbl 0427 `"0427"', add
label define cpuma0010_lbl 0428 `"0428"', add
label define cpuma0010_lbl 0429 `"0429"', add
label define cpuma0010_lbl 0430 `"0430"', add
label define cpuma0010_lbl 0431 `"0431"', add
label define cpuma0010_lbl 0432 `"0432"', add
label define cpuma0010_lbl 0433 `"0433"', add
label define cpuma0010_lbl 0434 `"0434"', add
label define cpuma0010_lbl 0435 `"0435"', add
label define cpuma0010_lbl 0436 `"0436"', add
label define cpuma0010_lbl 0437 `"0437"', add
label define cpuma0010_lbl 0438 `"0438"', add
label define cpuma0010_lbl 0439 `"0439"', add
label define cpuma0010_lbl 0440 `"0440"', add
label define cpuma0010_lbl 0441 `"0441"', add
label define cpuma0010_lbl 0442 `"0442"', add
label define cpuma0010_lbl 0443 `"0443"', add
label define cpuma0010_lbl 0444 `"0444"', add
label define cpuma0010_lbl 0445 `"0445"', add
label define cpuma0010_lbl 0446 `"0446"', add
label define cpuma0010_lbl 0447 `"0447"', add
label define cpuma0010_lbl 0448 `"0448"', add
label define cpuma0010_lbl 0449 `"0449"', add
label define cpuma0010_lbl 0450 `"0450"', add
label define cpuma0010_lbl 0451 `"0451"', add
label define cpuma0010_lbl 0452 `"0452"', add
label define cpuma0010_lbl 0453 `"0453"', add
label define cpuma0010_lbl 0454 `"0454"', add
label define cpuma0010_lbl 0455 `"0455"', add
label define cpuma0010_lbl 0456 `"0456"', add
label define cpuma0010_lbl 0457 `"0457"', add
label define cpuma0010_lbl 0458 `"0458"', add
label define cpuma0010_lbl 0459 `"0459"', add
label define cpuma0010_lbl 0460 `"0460"', add
label define cpuma0010_lbl 0461 `"0461"', add
label define cpuma0010_lbl 0462 `"0462"', add
label define cpuma0010_lbl 0463 `"0463"', add
label define cpuma0010_lbl 0464 `"0464"', add
label define cpuma0010_lbl 0465 `"0465"', add
label define cpuma0010_lbl 0466 `"0466"', add
label define cpuma0010_lbl 0467 `"0467"', add
label define cpuma0010_lbl 0468 `"0468"', add
label define cpuma0010_lbl 0469 `"0469"', add
label define cpuma0010_lbl 0470 `"0470"', add
label define cpuma0010_lbl 0471 `"0471"', add
label define cpuma0010_lbl 0472 `"0472"', add
label define cpuma0010_lbl 0473 `"0473"', add
label define cpuma0010_lbl 0474 `"0474"', add
label define cpuma0010_lbl 0475 `"0475"', add
label define cpuma0010_lbl 0476 `"0476"', add
label define cpuma0010_lbl 0477 `"0477"', add
label define cpuma0010_lbl 0478 `"0478"', add
label define cpuma0010_lbl 0479 `"0479"', add
label define cpuma0010_lbl 0480 `"0480"', add
label define cpuma0010_lbl 0481 `"0481"', add
label define cpuma0010_lbl 0482 `"0482"', add
label define cpuma0010_lbl 0483 `"0483"', add
label define cpuma0010_lbl 0484 `"0484"', add
label define cpuma0010_lbl 0485 `"0485"', add
label define cpuma0010_lbl 0486 `"0486"', add
label define cpuma0010_lbl 0487 `"0487"', add
label define cpuma0010_lbl 0488 `"0488"', add
label define cpuma0010_lbl 0489 `"0489"', add
label define cpuma0010_lbl 0490 `"0490"', add
label define cpuma0010_lbl 0491 `"0491"', add
label define cpuma0010_lbl 0492 `"0492"', add
label define cpuma0010_lbl 0493 `"0493"', add
label define cpuma0010_lbl 0494 `"0494"', add
label define cpuma0010_lbl 0495 `"0495"', add
label define cpuma0010_lbl 0496 `"0496"', add
label define cpuma0010_lbl 0497 `"0497"', add
label define cpuma0010_lbl 0498 `"0498"', add
label define cpuma0010_lbl 0499 `"0499"', add
label define cpuma0010_lbl 0500 `"0500"', add
label define cpuma0010_lbl 0501 `"0501"', add
label define cpuma0010_lbl 0502 `"0502"', add
label define cpuma0010_lbl 0503 `"0503"', add
label define cpuma0010_lbl 0504 `"0504"', add
label define cpuma0010_lbl 0505 `"0505"', add
label define cpuma0010_lbl 0506 `"0506"', add
label define cpuma0010_lbl 0507 `"0507"', add
label define cpuma0010_lbl 0508 `"0508"', add
label define cpuma0010_lbl 0509 `"0509"', add
label define cpuma0010_lbl 0510 `"0510"', add
label define cpuma0010_lbl 0511 `"0511"', add
label define cpuma0010_lbl 0512 `"0512"', add
label define cpuma0010_lbl 0513 `"0513"', add
label define cpuma0010_lbl 0514 `"0514"', add
label define cpuma0010_lbl 0515 `"0515"', add
label define cpuma0010_lbl 0516 `"0516"', add
label define cpuma0010_lbl 0517 `"0517"', add
label define cpuma0010_lbl 0518 `"0518"', add
label define cpuma0010_lbl 0519 `"0519"', add
label define cpuma0010_lbl 0520 `"0520"', add
label define cpuma0010_lbl 0521 `"0521"', add
label define cpuma0010_lbl 0522 `"0522"', add
label define cpuma0010_lbl 0523 `"0523"', add
label define cpuma0010_lbl 0524 `"0524"', add
label define cpuma0010_lbl 0525 `"0525"', add
label define cpuma0010_lbl 0526 `"0526"', add
label define cpuma0010_lbl 0527 `"0527"', add
label define cpuma0010_lbl 0528 `"0528"', add
label define cpuma0010_lbl 0529 `"0529"', add
label define cpuma0010_lbl 0530 `"0530"', add
label define cpuma0010_lbl 0531 `"0531"', add
label define cpuma0010_lbl 0532 `"0532"', add
label define cpuma0010_lbl 0533 `"0533"', add
label define cpuma0010_lbl 0534 `"0534"', add
label define cpuma0010_lbl 0535 `"0535"', add
label define cpuma0010_lbl 0536 `"0536"', add
label define cpuma0010_lbl 0537 `"0537"', add
label define cpuma0010_lbl 0538 `"0538"', add
label define cpuma0010_lbl 0539 `"0539"', add
label define cpuma0010_lbl 0540 `"0540"', add
label define cpuma0010_lbl 0541 `"0541"', add
label define cpuma0010_lbl 0542 `"0542"', add
label define cpuma0010_lbl 0543 `"0543"', add
label define cpuma0010_lbl 0544 `"0544"', add
label define cpuma0010_lbl 0545 `"0545"', add
label define cpuma0010_lbl 0546 `"0546"', add
label define cpuma0010_lbl 0547 `"0547"', add
label define cpuma0010_lbl 0548 `"0548"', add
label define cpuma0010_lbl 0549 `"0549"', add
label define cpuma0010_lbl 0550 `"0550"', add
label define cpuma0010_lbl 0551 `"0551"', add
label define cpuma0010_lbl 0552 `"0552"', add
label define cpuma0010_lbl 0553 `"0553"', add
label define cpuma0010_lbl 0554 `"0554"', add
label define cpuma0010_lbl 0555 `"0555"', add
label define cpuma0010_lbl 0556 `"0556"', add
label define cpuma0010_lbl 0557 `"0557"', add
label define cpuma0010_lbl 0558 `"0558"', add
label define cpuma0010_lbl 0559 `"0559"', add
label define cpuma0010_lbl 0560 `"0560"', add
label define cpuma0010_lbl 0561 `"0561"', add
label define cpuma0010_lbl 0562 `"0562"', add
label define cpuma0010_lbl 0563 `"0563"', add
label define cpuma0010_lbl 0564 `"0564"', add
label define cpuma0010_lbl 0565 `"0565"', add
label define cpuma0010_lbl 0566 `"0566"', add
label define cpuma0010_lbl 0567 `"0567"', add
label define cpuma0010_lbl 0568 `"0568"', add
label define cpuma0010_lbl 0569 `"0569"', add
label define cpuma0010_lbl 0570 `"0570"', add
label define cpuma0010_lbl 0571 `"0571"', add
label define cpuma0010_lbl 0572 `"0572"', add
label define cpuma0010_lbl 0573 `"0573"', add
label define cpuma0010_lbl 0574 `"0574"', add
label define cpuma0010_lbl 0575 `"0575"', add
label define cpuma0010_lbl 0576 `"0576"', add
label define cpuma0010_lbl 0577 `"0577"', add
label define cpuma0010_lbl 0578 `"0578"', add
label define cpuma0010_lbl 0579 `"0579"', add
label define cpuma0010_lbl 0580 `"0580"', add
label define cpuma0010_lbl 0581 `"0581"', add
label define cpuma0010_lbl 0582 `"0582"', add
label define cpuma0010_lbl 0583 `"0583"', add
label define cpuma0010_lbl 0584 `"0584"', add
label define cpuma0010_lbl 0585 `"0585"', add
label define cpuma0010_lbl 0586 `"0586"', add
label define cpuma0010_lbl 0587 `"0587"', add
label define cpuma0010_lbl 0588 `"0588"', add
label define cpuma0010_lbl 0589 `"0589"', add
label define cpuma0010_lbl 0590 `"0590"', add
label define cpuma0010_lbl 0591 `"0591"', add
label define cpuma0010_lbl 0592 `"0592"', add
label define cpuma0010_lbl 0593 `"0593"', add
label define cpuma0010_lbl 0594 `"0594"', add
label define cpuma0010_lbl 0595 `"0595"', add
label define cpuma0010_lbl 0596 `"0596"', add
label define cpuma0010_lbl 0597 `"0597"', add
label define cpuma0010_lbl 0598 `"0598"', add
label define cpuma0010_lbl 0599 `"0599"', add
label define cpuma0010_lbl 0600 `"0600"', add
label define cpuma0010_lbl 0601 `"0601"', add
label define cpuma0010_lbl 0602 `"0602"', add
label define cpuma0010_lbl 0603 `"0603"', add
label define cpuma0010_lbl 0604 `"0604"', add
label define cpuma0010_lbl 0605 `"0605"', add
label define cpuma0010_lbl 0606 `"0606"', add
label define cpuma0010_lbl 0607 `"0607"', add
label define cpuma0010_lbl 0608 `"0608"', add
label define cpuma0010_lbl 0609 `"0609"', add
label define cpuma0010_lbl 0610 `"0610"', add
label define cpuma0010_lbl 0611 `"0611"', add
label define cpuma0010_lbl 0612 `"0612"', add
label define cpuma0010_lbl 0613 `"0613"', add
label define cpuma0010_lbl 0614 `"0614"', add
label define cpuma0010_lbl 0615 `"0615"', add
label define cpuma0010_lbl 0616 `"0616"', add
label define cpuma0010_lbl 0617 `"0617"', add
label define cpuma0010_lbl 0618 `"0618"', add
label define cpuma0010_lbl 0619 `"0619"', add
label define cpuma0010_lbl 0620 `"0620"', add
label define cpuma0010_lbl 0621 `"0621"', add
label define cpuma0010_lbl 0622 `"0622"', add
label define cpuma0010_lbl 0623 `"0623"', add
label define cpuma0010_lbl 0624 `"0624"', add
label define cpuma0010_lbl 0625 `"0625"', add
label define cpuma0010_lbl 0626 `"0626"', add
label define cpuma0010_lbl 0627 `"0627"', add
label define cpuma0010_lbl 0628 `"0628"', add
label define cpuma0010_lbl 0629 `"0629"', add
label define cpuma0010_lbl 0630 `"0630"', add
label define cpuma0010_lbl 0631 `"0631"', add
label define cpuma0010_lbl 0632 `"0632"', add
label define cpuma0010_lbl 0633 `"0633"', add
label define cpuma0010_lbl 0634 `"0634"', add
label define cpuma0010_lbl 0635 `"0635"', add
label define cpuma0010_lbl 0636 `"0636"', add
label define cpuma0010_lbl 0637 `"0637"', add
label define cpuma0010_lbl 0638 `"0638"', add
label define cpuma0010_lbl 0639 `"0639"', add
label define cpuma0010_lbl 0640 `"0640"', add
label define cpuma0010_lbl 0641 `"0641"', add
label define cpuma0010_lbl 0642 `"0642"', add
label define cpuma0010_lbl 0643 `"0643"', add
label define cpuma0010_lbl 0644 `"0644"', add
label define cpuma0010_lbl 0645 `"0645"', add
label define cpuma0010_lbl 0646 `"0646"', add
label define cpuma0010_lbl 0647 `"0647"', add
label define cpuma0010_lbl 0648 `"0648"', add
label define cpuma0010_lbl 0649 `"0649"', add
label define cpuma0010_lbl 0650 `"0650"', add
label define cpuma0010_lbl 0651 `"0651"', add
label define cpuma0010_lbl 0652 `"0652"', add
label define cpuma0010_lbl 0653 `"0653"', add
label define cpuma0010_lbl 0654 `"0654"', add
label define cpuma0010_lbl 0655 `"0655"', add
label define cpuma0010_lbl 0656 `"0656"', add
label define cpuma0010_lbl 0657 `"0657"', add
label define cpuma0010_lbl 0658 `"0658"', add
label define cpuma0010_lbl 0659 `"0659"', add
label define cpuma0010_lbl 0660 `"0660"', add
label define cpuma0010_lbl 0661 `"0661"', add
label define cpuma0010_lbl 0662 `"0662"', add
label define cpuma0010_lbl 0663 `"0663"', add
label define cpuma0010_lbl 0664 `"0664"', add
label define cpuma0010_lbl 0665 `"0665"', add
label define cpuma0010_lbl 0666 `"0666"', add
label define cpuma0010_lbl 0667 `"0667"', add
label define cpuma0010_lbl 0668 `"0668"', add
label define cpuma0010_lbl 0669 `"0669"', add
label define cpuma0010_lbl 0670 `"0670"', add
label define cpuma0010_lbl 0671 `"0671"', add
label define cpuma0010_lbl 0672 `"0672"', add
label define cpuma0010_lbl 0673 `"0673"', add
label define cpuma0010_lbl 0674 `"0674"', add
label define cpuma0010_lbl 0675 `"0675"', add
label define cpuma0010_lbl 0676 `"0676"', add
label define cpuma0010_lbl 0677 `"0677"', add
label define cpuma0010_lbl 0678 `"0678"', add
label define cpuma0010_lbl 0679 `"0679"', add
label define cpuma0010_lbl 0680 `"0680"', add
label define cpuma0010_lbl 0681 `"0681"', add
label define cpuma0010_lbl 0682 `"0682"', add
label define cpuma0010_lbl 0683 `"0683"', add
label define cpuma0010_lbl 0684 `"0684"', add
label define cpuma0010_lbl 0685 `"0685"', add
label define cpuma0010_lbl 0686 `"0686"', add
label define cpuma0010_lbl 0687 `"0687"', add
label define cpuma0010_lbl 0688 `"0688"', add
label define cpuma0010_lbl 0689 `"0689"', add
label define cpuma0010_lbl 0690 `"0690"', add
label define cpuma0010_lbl 0691 `"0691"', add
label define cpuma0010_lbl 0692 `"0692"', add
label define cpuma0010_lbl 0693 `"0693"', add
label define cpuma0010_lbl 0694 `"0694"', add
label define cpuma0010_lbl 0695 `"0695"', add
label define cpuma0010_lbl 0696 `"0696"', add
label define cpuma0010_lbl 0697 `"0697"', add
label define cpuma0010_lbl 0698 `"0698"', add
label define cpuma0010_lbl 0699 `"0699"', add
label define cpuma0010_lbl 0700 `"0700"', add
label define cpuma0010_lbl 0701 `"0701"', add
label define cpuma0010_lbl 0702 `"0702"', add
label define cpuma0010_lbl 0703 `"0703"', add
label define cpuma0010_lbl 0704 `"0704"', add
label define cpuma0010_lbl 0705 `"0705"', add
label define cpuma0010_lbl 0706 `"0706"', add
label define cpuma0010_lbl 0707 `"0707"', add
label define cpuma0010_lbl 0708 `"0708"', add
label define cpuma0010_lbl 0709 `"0709"', add
label define cpuma0010_lbl 0710 `"0710"', add
label define cpuma0010_lbl 0711 `"0711"', add
label define cpuma0010_lbl 0712 `"0712"', add
label define cpuma0010_lbl 0713 `"0713"', add
label define cpuma0010_lbl 0714 `"0714"', add
label define cpuma0010_lbl 0715 `"0715"', add
label define cpuma0010_lbl 0716 `"0716"', add
label define cpuma0010_lbl 0717 `"0717"', add
label define cpuma0010_lbl 0718 `"0718"', add
label define cpuma0010_lbl 0719 `"0719"', add
label define cpuma0010_lbl 0720 `"0720"', add
label define cpuma0010_lbl 0721 `"0721"', add
label define cpuma0010_lbl 0722 `"0722"', add
label define cpuma0010_lbl 0723 `"0723"', add
label define cpuma0010_lbl 0724 `"0724"', add
label define cpuma0010_lbl 0725 `"0725"', add
label define cpuma0010_lbl 0726 `"0726"', add
label define cpuma0010_lbl 0727 `"0727"', add
label define cpuma0010_lbl 0728 `"0728"', add
label define cpuma0010_lbl 0729 `"0729"', add
label define cpuma0010_lbl 0730 `"0730"', add
label define cpuma0010_lbl 0731 `"0731"', add
label define cpuma0010_lbl 0732 `"0732"', add
label define cpuma0010_lbl 0733 `"0733"', add
label define cpuma0010_lbl 0734 `"0734"', add
label define cpuma0010_lbl 0735 `"0735"', add
label define cpuma0010_lbl 0736 `"0736"', add
label define cpuma0010_lbl 0737 `"0737"', add
label define cpuma0010_lbl 0738 `"0738"', add
label define cpuma0010_lbl 0739 `"0739"', add
label define cpuma0010_lbl 0740 `"0740"', add
label define cpuma0010_lbl 0741 `"0741"', add
label define cpuma0010_lbl 0742 `"0742"', add
label define cpuma0010_lbl 0743 `"0743"', add
label define cpuma0010_lbl 0744 `"0744"', add
label define cpuma0010_lbl 0745 `"0745"', add
label define cpuma0010_lbl 0746 `"0746"', add
label define cpuma0010_lbl 0747 `"0747"', add
label define cpuma0010_lbl 0748 `"0748"', add
label define cpuma0010_lbl 0749 `"0749"', add
label define cpuma0010_lbl 0750 `"0750"', add
label define cpuma0010_lbl 0751 `"0751"', add
label define cpuma0010_lbl 0752 `"0752"', add
label define cpuma0010_lbl 0753 `"0753"', add
label define cpuma0010_lbl 0754 `"0754"', add
label define cpuma0010_lbl 0755 `"0755"', add
label define cpuma0010_lbl 0756 `"0756"', add
label define cpuma0010_lbl 0757 `"0757"', add
label define cpuma0010_lbl 0758 `"0758"', add
label define cpuma0010_lbl 0759 `"0759"', add
label define cpuma0010_lbl 0760 `"0760"', add
label define cpuma0010_lbl 0761 `"0761"', add
label define cpuma0010_lbl 0762 `"0762"', add
label define cpuma0010_lbl 0763 `"0763"', add
label define cpuma0010_lbl 0764 `"0764"', add
label define cpuma0010_lbl 0765 `"0765"', add
label define cpuma0010_lbl 0766 `"0766"', add
label define cpuma0010_lbl 0767 `"0767"', add
label define cpuma0010_lbl 0768 `"0768"', add
label define cpuma0010_lbl 0769 `"0769"', add
label define cpuma0010_lbl 0770 `"0770"', add
label define cpuma0010_lbl 0771 `"0771"', add
label define cpuma0010_lbl 0772 `"0772"', add
label define cpuma0010_lbl 0773 `"0773"', add
label define cpuma0010_lbl 0774 `"0774"', add
label define cpuma0010_lbl 0775 `"0775"', add
label define cpuma0010_lbl 0776 `"0776"', add
label define cpuma0010_lbl 0777 `"0777"', add
label define cpuma0010_lbl 0778 `"0778"', add
label define cpuma0010_lbl 0779 `"0779"', add
label define cpuma0010_lbl 0780 `"0780"', add
label define cpuma0010_lbl 0781 `"0781"', add
label define cpuma0010_lbl 0782 `"0782"', add
label define cpuma0010_lbl 0783 `"0783"', add
label define cpuma0010_lbl 0784 `"0784"', add
label define cpuma0010_lbl 0785 `"0785"', add
label define cpuma0010_lbl 0786 `"0786"', add
label define cpuma0010_lbl 0787 `"0787"', add
label define cpuma0010_lbl 0788 `"0788"', add
label define cpuma0010_lbl 0789 `"0789"', add
label define cpuma0010_lbl 0790 `"0790"', add
label define cpuma0010_lbl 0791 `"0791"', add
label define cpuma0010_lbl 0792 `"0792"', add
label define cpuma0010_lbl 0793 `"0793"', add
label define cpuma0010_lbl 0794 `"0794"', add
label define cpuma0010_lbl 0795 `"0795"', add
label define cpuma0010_lbl 0796 `"0796"', add
label define cpuma0010_lbl 0797 `"0797"', add
label define cpuma0010_lbl 0798 `"0798"', add
label define cpuma0010_lbl 0799 `"0799"', add
label define cpuma0010_lbl 0800 `"0800"', add
label define cpuma0010_lbl 0801 `"0801"', add
label define cpuma0010_lbl 0802 `"0802"', add
label define cpuma0010_lbl 0803 `"0803"', add
label define cpuma0010_lbl 0804 `"0804"', add
label define cpuma0010_lbl 0805 `"0805"', add
label define cpuma0010_lbl 0806 `"0806"', add
label define cpuma0010_lbl 0807 `"0807"', add
label define cpuma0010_lbl 0808 `"0808"', add
label define cpuma0010_lbl 0809 `"0809"', add
label define cpuma0010_lbl 0810 `"0810"', add
label define cpuma0010_lbl 0811 `"0811"', add
label define cpuma0010_lbl 0812 `"0812"', add
label define cpuma0010_lbl 0813 `"0813"', add
label define cpuma0010_lbl 0814 `"0814"', add
label define cpuma0010_lbl 0815 `"0815"', add
label define cpuma0010_lbl 0816 `"0816"', add
label define cpuma0010_lbl 0817 `"0817"', add
label define cpuma0010_lbl 0818 `"0818"', add
label define cpuma0010_lbl 0819 `"0819"', add
label define cpuma0010_lbl 0820 `"0820"', add
label define cpuma0010_lbl 0821 `"0821"', add
label define cpuma0010_lbl 0822 `"0822"', add
label define cpuma0010_lbl 0823 `"0823"', add
label define cpuma0010_lbl 0824 `"0824"', add
label define cpuma0010_lbl 0825 `"0825"', add
label define cpuma0010_lbl 0826 `"0826"', add
label define cpuma0010_lbl 0827 `"0827"', add
label define cpuma0010_lbl 0828 `"0828"', add
label define cpuma0010_lbl 0829 `"0829"', add
label define cpuma0010_lbl 0830 `"0830"', add
label define cpuma0010_lbl 0831 `"0831"', add
label define cpuma0010_lbl 0832 `"0832"', add
label define cpuma0010_lbl 0833 `"0833"', add
label define cpuma0010_lbl 0834 `"0834"', add
label define cpuma0010_lbl 0835 `"0835"', add
label define cpuma0010_lbl 0836 `"0836"', add
label define cpuma0010_lbl 0837 `"0837"', add
label define cpuma0010_lbl 0838 `"0838"', add
label define cpuma0010_lbl 0839 `"0839"', add
label define cpuma0010_lbl 0840 `"0840"', add
label define cpuma0010_lbl 0841 `"0841"', add
label define cpuma0010_lbl 0842 `"0842"', add
label define cpuma0010_lbl 0843 `"0843"', add
label define cpuma0010_lbl 0844 `"0844"', add
label define cpuma0010_lbl 0845 `"0845"', add
label define cpuma0010_lbl 0846 `"0846"', add
label define cpuma0010_lbl 0847 `"0847"', add
label define cpuma0010_lbl 0848 `"0848"', add
label define cpuma0010_lbl 0849 `"0849"', add
label define cpuma0010_lbl 0850 `"0850"', add
label define cpuma0010_lbl 0851 `"0851"', add
label define cpuma0010_lbl 0852 `"0852"', add
label define cpuma0010_lbl 0853 `"0853"', add
label define cpuma0010_lbl 0854 `"0854"', add
label define cpuma0010_lbl 0855 `"0855"', add
label define cpuma0010_lbl 0856 `"0856"', add
label define cpuma0010_lbl 0857 `"0857"', add
label define cpuma0010_lbl 0858 `"0858"', add
label define cpuma0010_lbl 0859 `"0859"', add
label define cpuma0010_lbl 0860 `"0860"', add
label define cpuma0010_lbl 0861 `"0861"', add
label define cpuma0010_lbl 0862 `"0862"', add
label define cpuma0010_lbl 0863 `"0863"', add
label define cpuma0010_lbl 0864 `"0864"', add
label define cpuma0010_lbl 0865 `"0865"', add
label define cpuma0010_lbl 0866 `"0866"', add
label define cpuma0010_lbl 0867 `"0867"', add
label define cpuma0010_lbl 0868 `"0868"', add
label define cpuma0010_lbl 0869 `"0869"', add
label define cpuma0010_lbl 0870 `"0870"', add
label define cpuma0010_lbl 0871 `"0871"', add
label define cpuma0010_lbl 0872 `"0872"', add
label define cpuma0010_lbl 0873 `"0873"', add
label define cpuma0010_lbl 0874 `"0874"', add
label define cpuma0010_lbl 0875 `"0875"', add
label define cpuma0010_lbl 0876 `"0876"', add
label define cpuma0010_lbl 0877 `"0877"', add
label define cpuma0010_lbl 0878 `"0878"', add
label define cpuma0010_lbl 0879 `"0879"', add
label define cpuma0010_lbl 0880 `"0880"', add
label define cpuma0010_lbl 0881 `"0881"', add
label define cpuma0010_lbl 0882 `"0882"', add
label define cpuma0010_lbl 0883 `"0883"', add
label define cpuma0010_lbl 0884 `"0884"', add
label define cpuma0010_lbl 0885 `"0885"', add
label define cpuma0010_lbl 0886 `"0886"', add
label define cpuma0010_lbl 0887 `"0887"', add
label define cpuma0010_lbl 0888 `"0888"', add
label define cpuma0010_lbl 0889 `"0889"', add
label define cpuma0010_lbl 0890 `"0890"', add
label define cpuma0010_lbl 0891 `"0891"', add
label define cpuma0010_lbl 0892 `"0892"', add
label define cpuma0010_lbl 0893 `"0893"', add
label define cpuma0010_lbl 0894 `"0894"', add
label define cpuma0010_lbl 0895 `"0895"', add
label define cpuma0010_lbl 0896 `"0896"', add
label define cpuma0010_lbl 0897 `"0897"', add
label define cpuma0010_lbl 0898 `"0898"', add
label define cpuma0010_lbl 0899 `"0899"', add
label define cpuma0010_lbl 0900 `"0900"', add
label define cpuma0010_lbl 0901 `"0901"', add
label define cpuma0010_lbl 0902 `"0902"', add
label define cpuma0010_lbl 0903 `"0903"', add
label define cpuma0010_lbl 0904 `"0904"', add
label define cpuma0010_lbl 0905 `"0905"', add
label define cpuma0010_lbl 0906 `"0906"', add
label define cpuma0010_lbl 0907 `"0907"', add
label define cpuma0010_lbl 0908 `"0908"', add
label define cpuma0010_lbl 0909 `"0909"', add
label define cpuma0010_lbl 0910 `"0910"', add
label define cpuma0010_lbl 0911 `"0911"', add
label define cpuma0010_lbl 0912 `"0912"', add
label define cpuma0010_lbl 0913 `"0913"', add
label define cpuma0010_lbl 0914 `"0914"', add
label define cpuma0010_lbl 0915 `"0915"', add
label define cpuma0010_lbl 0916 `"0916"', add
label define cpuma0010_lbl 0917 `"0917"', add
label define cpuma0010_lbl 0918 `"0918"', add
label define cpuma0010_lbl 0919 `"0919"', add
label define cpuma0010_lbl 0920 `"0920"', add
label define cpuma0010_lbl 0921 `"0921"', add
label define cpuma0010_lbl 0922 `"0922"', add
label define cpuma0010_lbl 0923 `"0923"', add
label define cpuma0010_lbl 0924 `"0924"', add
label define cpuma0010_lbl 0925 `"0925"', add
label define cpuma0010_lbl 0926 `"0926"', add
label define cpuma0010_lbl 0927 `"0927"', add
label define cpuma0010_lbl 0928 `"0928"', add
label define cpuma0010_lbl 0929 `"0929"', add
label define cpuma0010_lbl 0930 `"0930"', add
label define cpuma0010_lbl 0931 `"0931"', add
label define cpuma0010_lbl 0932 `"0932"', add
label define cpuma0010_lbl 0933 `"0933"', add
label define cpuma0010_lbl 0934 `"0934"', add
label define cpuma0010_lbl 0935 `"0935"', add
label define cpuma0010_lbl 0936 `"0936"', add
label define cpuma0010_lbl 0937 `"0937"', add
label define cpuma0010_lbl 0938 `"0938"', add
label define cpuma0010_lbl 0939 `"0939"', add
label define cpuma0010_lbl 0940 `"0940"', add
label define cpuma0010_lbl 0941 `"0941"', add
label define cpuma0010_lbl 0942 `"0942"', add
label define cpuma0010_lbl 0943 `"0943"', add
label define cpuma0010_lbl 0944 `"0944"', add
label define cpuma0010_lbl 0945 `"0945"', add
label define cpuma0010_lbl 0946 `"0946"', add
label define cpuma0010_lbl 0947 `"0947"', add
label define cpuma0010_lbl 0948 `"0948"', add
label define cpuma0010_lbl 0949 `"0949"', add
label define cpuma0010_lbl 0950 `"0950"', add
label define cpuma0010_lbl 0951 `"0951"', add
label define cpuma0010_lbl 0952 `"0952"', add
label define cpuma0010_lbl 0953 `"0953"', add
label define cpuma0010_lbl 0954 `"0954"', add
label define cpuma0010_lbl 0955 `"0955"', add
label define cpuma0010_lbl 0956 `"0956"', add
label define cpuma0010_lbl 0957 `"0957"', add
label define cpuma0010_lbl 0958 `"0958"', add
label define cpuma0010_lbl 0959 `"0959"', add
label define cpuma0010_lbl 0960 `"0960"', add
label define cpuma0010_lbl 0961 `"0961"', add
label define cpuma0010_lbl 0962 `"0962"', add
label define cpuma0010_lbl 0963 `"0963"', add
label define cpuma0010_lbl 0964 `"0964"', add
label define cpuma0010_lbl 0965 `"0965"', add
label define cpuma0010_lbl 0966 `"0966"', add
label define cpuma0010_lbl 0967 `"0967"', add
label define cpuma0010_lbl 0968 `"0968"', add
label define cpuma0010_lbl 0969 `"0969"', add
label define cpuma0010_lbl 0970 `"0970"', add
label define cpuma0010_lbl 0971 `"0971"', add
label define cpuma0010_lbl 0972 `"0972"', add
label define cpuma0010_lbl 0973 `"0973"', add
label define cpuma0010_lbl 0974 `"0974"', add
label define cpuma0010_lbl 0975 `"0975"', add
label define cpuma0010_lbl 0976 `"0976"', add
label define cpuma0010_lbl 0977 `"0977"', add
label define cpuma0010_lbl 0978 `"0978"', add
label define cpuma0010_lbl 0979 `"0979"', add
label define cpuma0010_lbl 0980 `"0980"', add
label define cpuma0010_lbl 0981 `"0981"', add
label define cpuma0010_lbl 0982 `"0982"', add
label define cpuma0010_lbl 0983 `"0983"', add
label define cpuma0010_lbl 0984 `"0984"', add
label define cpuma0010_lbl 0985 `"0985"', add
label define cpuma0010_lbl 0986 `"0986"', add
label define cpuma0010_lbl 0987 `"0987"', add
label define cpuma0010_lbl 0988 `"0988"', add
label define cpuma0010_lbl 0989 `"0989"', add
label define cpuma0010_lbl 0990 `"0990"', add
label define cpuma0010_lbl 0991 `"0991"', add
label define cpuma0010_lbl 0992 `"0992"', add
label define cpuma0010_lbl 0993 `"0993"', add
label define cpuma0010_lbl 0994 `"0994"', add
label define cpuma0010_lbl 0995 `"0995"', add
label define cpuma0010_lbl 0996 `"0996"', add
label define cpuma0010_lbl 0997 `"0997"', add
label define cpuma0010_lbl 0998 `"0998"', add
label define cpuma0010_lbl 0999 `"0999"', add
label define cpuma0010_lbl 1000 `"1000"', add
label define cpuma0010_lbl 1001 `"1001"', add
label define cpuma0010_lbl 1002 `"1002"', add
label define cpuma0010_lbl 1003 `"1003"', add
label define cpuma0010_lbl 1004 `"1004"', add
label define cpuma0010_lbl 1005 `"1005"', add
label define cpuma0010_lbl 1006 `"1006"', add
label define cpuma0010_lbl 1007 `"1007"', add
label define cpuma0010_lbl 1008 `"1008"', add
label define cpuma0010_lbl 1009 `"1009"', add
label define cpuma0010_lbl 1010 `"1010"', add
label define cpuma0010_lbl 1011 `"1011"', add
label define cpuma0010_lbl 1012 `"1012"', add
label define cpuma0010_lbl 1013 `"1013"', add
label define cpuma0010_lbl 1014 `"1014"', add
label define cpuma0010_lbl 1015 `"1015"', add
label define cpuma0010_lbl 1016 `"1016"', add
label define cpuma0010_lbl 1017 `"1017"', add
label define cpuma0010_lbl 1018 `"1018"', add
label define cpuma0010_lbl 1019 `"1019"', add
label define cpuma0010_lbl 1020 `"1020"', add
label define cpuma0010_lbl 1021 `"1021"', add
label define cpuma0010_lbl 1022 `"1022"', add
label define cpuma0010_lbl 1023 `"1023"', add
label define cpuma0010_lbl 1024 `"1024"', add
label define cpuma0010_lbl 1025 `"1025"', add
label define cpuma0010_lbl 1026 `"1026"', add
label define cpuma0010_lbl 1027 `"1027"', add
label define cpuma0010_lbl 1028 `"1028"', add
label define cpuma0010_lbl 1029 `"1029"', add
label define cpuma0010_lbl 1030 `"1030"', add
label define cpuma0010_lbl 1031 `"1031"', add
label define cpuma0010_lbl 1032 `"1032"', add
label define cpuma0010_lbl 1033 `"1033"', add
label define cpuma0010_lbl 1034 `"1034"', add
label define cpuma0010_lbl 1035 `"1035"', add
label define cpuma0010_lbl 1036 `"1036"', add
label define cpuma0010_lbl 1037 `"1037"', add
label define cpuma0010_lbl 1038 `"1038"', add
label define cpuma0010_lbl 1039 `"1039"', add
label define cpuma0010_lbl 1040 `"1040"', add
label define cpuma0010_lbl 1041 `"1041"', add
label define cpuma0010_lbl 1042 `"1042"', add
label define cpuma0010_lbl 1043 `"1043"', add
label define cpuma0010_lbl 1044 `"1044"', add
label define cpuma0010_lbl 1045 `"1045"', add
label define cpuma0010_lbl 1046 `"1046"', add
label define cpuma0010_lbl 1047 `"1047"', add
label define cpuma0010_lbl 1048 `"1048"', add
label define cpuma0010_lbl 1049 `"1049"', add
label define cpuma0010_lbl 1050 `"1050"', add
label define cpuma0010_lbl 1051 `"1051"', add
label define cpuma0010_lbl 1052 `"1052"', add
label define cpuma0010_lbl 1053 `"1053"', add
label define cpuma0010_lbl 1054 `"1054"', add
label define cpuma0010_lbl 1055 `"1055"', add
label define cpuma0010_lbl 1056 `"1056"', add
label define cpuma0010_lbl 1057 `"1057"', add
label define cpuma0010_lbl 1058 `"1058"', add
label define cpuma0010_lbl 1059 `"1059"', add
label define cpuma0010_lbl 1060 `"1060"', add
label define cpuma0010_lbl 1061 `"1061"', add
label define cpuma0010_lbl 1062 `"1062"', add
label define cpuma0010_lbl 1063 `"1063"', add
label define cpuma0010_lbl 1064 `"1064"', add
label define cpuma0010_lbl 1065 `"1065"', add
label define cpuma0010_lbl 1066 `"1066"', add
label define cpuma0010_lbl 1067 `"1067"', add
label define cpuma0010_lbl 1068 `"1068"', add
label define cpuma0010_lbl 1069 `"1069"', add
label define cpuma0010_lbl 1070 `"1070"', add
label define cpuma0010_lbl 1071 `"1071"', add
label define cpuma0010_lbl 1072 `"1072"', add
label define cpuma0010_lbl 1073 `"1073"', add
label define cpuma0010_lbl 1074 `"1074"', add
label define cpuma0010_lbl 1075 `"1075"', add
label define cpuma0010_lbl 1076 `"1076"', add
label define cpuma0010_lbl 1077 `"1077"', add
label define cpuma0010_lbl 1078 `"1078"', add
label define cpuma0010_lbl 1079 `"1079"', add
label define cpuma0010_lbl 1080 `"1080"', add
label define cpuma0010_lbl 1081 `"1081"', add
label define cpuma0010_lbl 1082 `"1082"', add
label define cpuma0010_lbl 1083 `"1083"', add
label define cpuma0010_lbl 1084 `"1084"', add
label define cpuma0010_lbl 1085 `"1085"', add
label values cpuma0010 cpuma0010_lbl

label define metro_lbl 1 `"Not in metropolitan area"'
label define metro_lbl 2 `"Metropolitan status indeterminable (mixed)"', add
label define metro_lbl 3 `"In metropolitan area: Not in central/principal city"', add
label define metro_lbl 4 `"In metropolitan area: Central/principal city status indeterminable (mixed)"', add
label define metro_lbl 5 `"In metropolitan area: In central/principal city"', add
label values metro metro_lbl

label define metarea_lbl 000 `"Not identifiable or not in an MSA"'
label define metarea_lbl 004 `"Abilene, TX"', add
label define metarea_lbl 006 `"Aguadilla, PR"', add
label define metarea_lbl 008 `"Akron, OH"', add
label define metarea_lbl 012 `"Albany, GA"', add
label define metarea_lbl 016 `"Albany-Schenectady-Troy, NY"', add
label define metarea_lbl 020 `"Albuquerque, NM"', add
label define metarea_lbl 022 `"Alexandria, LA"', add
label define metarea_lbl 024 `"Allentown-Bethlehem-Easton, PA/NJ"', add
label define metarea_lbl 028 `"Altoona, PA"', add
label define metarea_lbl 032 `"Amarillo, TX"', add
label define metarea_lbl 038 `"Anchorage, AK"', add
label define metarea_lbl 040 `"Anderson, IN"', add
label define metarea_lbl 044 `"Ann Arbor, MI"', add
label define metarea_lbl 045 `"Anniston, AL"', add
label define metarea_lbl 046 `"Appleton-Oshkosh-Neenah, WI"', add
label define metarea_lbl 047 `"Arecibo, PR"', add
label define metarea_lbl 048 `"Asheville, NC"', add
label define metarea_lbl 050 `"Athens, GA"', add
label define metarea_lbl 052 `"Atlanta, GA"', add
label define metarea_lbl 056 `"Atlantic City, NJ"', add
label define metarea_lbl 058 `"Auburn-Opekika, AL"', add
label define metarea_lbl 060 `"Augusta-Aiken, GA/SC"', add
label define metarea_lbl 064 `"Austin, TX"', add
label define metarea_lbl 068 `"Bakersfield, CA"', add
label define metarea_lbl 072 `"Baltimore, MD"', add
label define metarea_lbl 073 `"Bangor, ME"', add
label define metarea_lbl 074 `"Barnstable-Yarmouth, MA"', add
label define metarea_lbl 076 `"Baton Rouge, LA"', add
label define metarea_lbl 078 `"Battle Creek, MI"', add
label define metarea_lbl 084 `"Beaumont-Port Arthur-Orange, TX"', add
label define metarea_lbl 086 `"Bellingham, WA"', add
label define metarea_lbl 087 `"Benton Harbor, MI"', add
label define metarea_lbl 088 `"Billings, MT"', add
label define metarea_lbl 092 `"Biloxi-Gulfport, MS"', add
label define metarea_lbl 096 `"Binghamton, NY"', add
label define metarea_lbl 100 `"Birmingham, AL"', add
label define metarea_lbl 102 `"Bloomington, IN"', add
label define metarea_lbl 104 `"Bloomington-Normal, IL"', add
label define metarea_lbl 108 `"Boise City, ID"', add
label define metarea_lbl 112 `"Boston, MA/NH"', add
label define metarea_lbl 114 `"Bradenton, FL"', add
label define metarea_lbl 115 `"Bremerton, WA"', add
label define metarea_lbl 116 `"Bridgeport, CT"', add
label define metarea_lbl 120 `"Brockton, MA"', add
label define metarea_lbl 124 `"Brownsville-Harlingen-San Benito, TX"', add
label define metarea_lbl 126 `"Bryan-College Station, TX"', add
label define metarea_lbl 128 `"Buffalo-Niagara Falls, NY"', add
label define metarea_lbl 130 `"Burlington, NC"', add
label define metarea_lbl 131 `"Burlington, VT"', add
label define metarea_lbl 132 `"Canton, OH"', add
label define metarea_lbl 133 `"Caguas, PR"', add
label define metarea_lbl 135 `"Casper, WY"', add
label define metarea_lbl 136 `"Cedar Rapids, IA"', add
label define metarea_lbl 140 `"Champaign-Urbana-Rantoul, IL"', add
label define metarea_lbl 144 `"Charleston-N. Charleston, SC"', add
label define metarea_lbl 148 `"Charleston, WV"', add
label define metarea_lbl 152 `"Charlotte-Gastonia-Rock Hill, NC/SC"', add
label define metarea_lbl 154 `"Charlottesville, VA"', add
label define metarea_lbl 156 `"Chattanooga, TN/GA"', add
label define metarea_lbl 158 `"Cheyenne, WY"', add
label define metarea_lbl 160 `"Chicago, IL"', add
label define metarea_lbl 162 `"Chico, CA"', add
label define metarea_lbl 164 `"Cincinnati-Hamilton, OH/KY/IN"', add
label define metarea_lbl 166 `"Clarksville- Hopkinsville, TN/KY"', add
label define metarea_lbl 168 `"Cleveland, OH"', add
label define metarea_lbl 172 `"Colorado Springs, CO"', add
label define metarea_lbl 174 `"Columbia, MO"', add
label define metarea_lbl 176 `"Columbia, SC"', add
label define metarea_lbl 180 `"Columbus, GA/AL"', add
label define metarea_lbl 184 `"Columbus, OH"', add
label define metarea_lbl 188 `"Corpus Christi, TX"', add
label define metarea_lbl 190 `"Cumberland, MD/WV"', add
label define metarea_lbl 192 `"Dallas-Fort Worth, TX"', add
label define metarea_lbl 193 `"Danbury, CT"', add
label define metarea_lbl 195 `"Danville, VA"', add
label define metarea_lbl 196 `"Davenport, IA - Rock Island-Moline, IL"', add
label define metarea_lbl 200 `"Dayton-Springfield, OH"', add
label define metarea_lbl 202 `"Daytona Beach, FL"', add
label define metarea_lbl 203 `"Decatur, AL"', add
label define metarea_lbl 204 `"Decatur, IL"', add
label define metarea_lbl 208 `"Denver-Boulder, CO"', add
label define metarea_lbl 212 `"Des Moines, IA"', add
label define metarea_lbl 216 `"Detroit, MI"', add
label define metarea_lbl 218 `"Dothan, AL"', add
label define metarea_lbl 219 `"Dover, DE"', add
label define metarea_lbl 220 `"Dubuque, IA"', add
label define metarea_lbl 224 `"Duluth-Superior, MN/WI"', add
label define metarea_lbl 228 `"Dutchess Co., NY"', add
label define metarea_lbl 229 `"Eau Claire, WI"', add
label define metarea_lbl 231 `"El Paso, TX"', add
label define metarea_lbl 232 `"Elkhart-Goshen, IN"', add
label define metarea_lbl 233 `"Elmira, NY"', add
label define metarea_lbl 234 `"Enid, OK"', add
label define metarea_lbl 236 `"Erie, PA"', add
label define metarea_lbl 240 `"Eugene-Springfield, OR"', add
label define metarea_lbl 244 `"Evansville, IN/KY"', add
label define metarea_lbl 252 `"Fargo-Morehead, ND/MN"', add
label define metarea_lbl 256 `"Fayetteville, NC"', add
label define metarea_lbl 258 `"Fayetteville-Springdale, AR"', add
label define metarea_lbl 260 `"Fitchburg-Leominster, MA"', add
label define metarea_lbl 262 `"Flagstaff, AZ/UT"', add
label define metarea_lbl 264 `"Flint, MI"', add
label define metarea_lbl 265 `"Florence, AL"', add
label define metarea_lbl 266 `"Florence, SC"', add
label define metarea_lbl 267 `"Fort Collins-Loveland, CO"', add
label define metarea_lbl 268 `"Fort Lauderdale-Hollywood-Pompano Beach, FL"', add
label define metarea_lbl 270 `"Fort Myers-Cape Coral, FL"', add
label define metarea_lbl 271 `"Fort Pierce, FL"', add
label define metarea_lbl 272 `"Fort Smith, AR/OK"', add
label define metarea_lbl 275 `"Fort Walton Beach, FL"', add
label define metarea_lbl 276 `"Fort Wayne, IN"', add
label define metarea_lbl 284 `"Fresno, CA"', add
label define metarea_lbl 288 `"Gadsden, AL"', add
label define metarea_lbl 290 `"Gainesville, FL"', add
label define metarea_lbl 292 `"Galveston-Texas City, TX"', add
label define metarea_lbl 297 `"Glens Falls, NY"', add
label define metarea_lbl 298 `"Goldsboro, NC"', add
label define metarea_lbl 299 `"Grand Forks, ND"', add
label define metarea_lbl 300 `"Grand Rapids, MI"', add
label define metarea_lbl 301 `"Grand Junction, CO"', add
label define metarea_lbl 304 `"Great Falls, MT"', add
label define metarea_lbl 306 `"Greeley, CO"', add
label define metarea_lbl 308 `"Green Bay, WI"', add
label define metarea_lbl 312 `"Greensboro-Winston Salem-High Point, NC"', add
label define metarea_lbl 315 `"Greenville, NC"', add
label define metarea_lbl 316 `"Greenville-Spartenburg-Anderson, SC"', add
label define metarea_lbl 318 `"Hagerstown, MD"', add
label define metarea_lbl 320 `"Hamilton-Middleton, OH"', add
label define metarea_lbl 324 `"Harrisburg-Lebanon--Carlisle, PA"', add
label define metarea_lbl 328 `"Hartford-Bristol-Middleton- New Britain, CT"', add
label define metarea_lbl 329 `"Hickory-Morganton, NC"', add
label define metarea_lbl 330 `"Hattiesburg, MS"', add
label define metarea_lbl 332 `"Honolulu, HI"', add
label define metarea_lbl 335 `"Houma-Thibodoux, LA"', add
label define metarea_lbl 336 `"Houston-Brazoria, TX"', add
label define metarea_lbl 340 `"Huntington-Ashland, WV/KY/OH"', add
label define metarea_lbl 344 `"Huntsville, AL"', add
label define metarea_lbl 348 `"Indianapolis, IN"', add
label define metarea_lbl 350 `"Iowa City, IA"', add
label define metarea_lbl 352 `"Jackson, MI"', add
label define metarea_lbl 356 `"Jackson, MS"', add
label define metarea_lbl 358 `"Jackson, TN"', add
label define metarea_lbl 359 `"Jacksonville, FL"', add
label define metarea_lbl 360 `"Jacksonville, NC"', add
label define metarea_lbl 361 `"Jamestown-Dunkirk, NY"', add
label define metarea_lbl 362 `"Janesville-Beloit, WI"', add
label define metarea_lbl 366 `"Johnson City-Kingsport--Bristol, TN/VA"', add
label define metarea_lbl 368 `"Johnstown, PA"', add
label define metarea_lbl 371 `"Joplin, MO"', add
label define metarea_lbl 372 `"Kalamazoo-Portage, MI"', add
label define metarea_lbl 374 `"Kankakee, IL"', add
label define metarea_lbl 376 `"Kansas City, MO/KS"', add
label define metarea_lbl 380 `"Kenosha, WI"', add
label define metarea_lbl 381 `"Kileen-Temple, TX"', add
label define metarea_lbl 384 `"Knoxville, TN"', add
label define metarea_lbl 385 `"Kokomo, IN"', add
label define metarea_lbl 387 `"LaCrosse, WI"', add
label define metarea_lbl 388 `"Lafayette, LA"', add
label define metarea_lbl 392 `"Lafayette-W. Lafayette, IN"', add
label define metarea_lbl 396 `"Lake Charles, LA"', add
label define metarea_lbl 398 `"Lakeland-Winterhaven, FL"', add
label define metarea_lbl 400 `"Lancaster, PA"', add
label define metarea_lbl 404 `"Lansing-E. Lansing, MI"', add
label define metarea_lbl 408 `"Laredo, TX"', add
label define metarea_lbl 410 `"Las Cruces, NM"', add
label define metarea_lbl 412 `"Las Vegas, NV"', add
label define metarea_lbl 415 `"Lawrence, KS"', add
label define metarea_lbl 420 `"Lawton, OK"', add
label define metarea_lbl 424 `"Lewiston-Auburn, ME"', add
label define metarea_lbl 428 `"Lexington-Fayette, KY"', add
label define metarea_lbl 432 `"Lima, OH"', add
label define metarea_lbl 436 `"Lincoln, NE"', add
label define metarea_lbl 440 `"Little Rock-N. Little Rock, AR"', add
label define metarea_lbl 441 `"Long Branch-Asbury Park, NJ"', add
label define metarea_lbl 442 `"Longview-Marshall, TX"', add
label define metarea_lbl 444 `"Lorain-Elyria, OH"', add
label define metarea_lbl 448 `"Los Angeles-Long Beach, CA"', add
label define metarea_lbl 452 `"Louisville, KY/IN"', add
label define metarea_lbl 460 `"Lubbock, TX"', add
label define metarea_lbl 464 `"Lynchburg, VA"', add
label define metarea_lbl 468 `"Macon-Warner Robins, GA"', add
label define metarea_lbl 472 `"Madison, WI"', add
label define metarea_lbl 476 `"Manchester, NH"', add
label define metarea_lbl 480 `"Mansfield, OH"', add
label define metarea_lbl 484 `"Mayaguez, PR"', add
label define metarea_lbl 488 `"McAllen-Edinburg-Pharr-Mission, TX"', add
label define metarea_lbl 489 `"Medford, OR"', add
label define metarea_lbl 490 `"Melbourne-Titusville-Cocoa-Palm Bay, FL"', add
label define metarea_lbl 492 `"Memphis, TN/AR/MS"', add
label define metarea_lbl 494 `"Merced, CA"', add
label define metarea_lbl 500 `"Miami-Hialeah, FL"', add
label define metarea_lbl 504 `"Midland, TX"', add
label define metarea_lbl 508 `"Milwaukee, WI"', add
label define metarea_lbl 512 `"Minneapolis-St. Paul, MN"', add
label define metarea_lbl 514 `"Missoula, MT"', add
label define metarea_lbl 516 `"Mobile, AL"', add
label define metarea_lbl 517 `"Modesto, CA"', add
label define metarea_lbl 519 `"Monmouth-Ocean, NJ"', add
label define metarea_lbl 520 `"Monroe, LA"', add
label define metarea_lbl 524 `"Montgomery, AL"', add
label define metarea_lbl 528 `"Muncie, IN"', add
label define metarea_lbl 532 `"Muskegon-Norton Shores-Muskegon Heights, MI"', add
label define metarea_lbl 533 `"Myrtle Beach, SC"', add
label define metarea_lbl 534 `"Naples, FL"', add
label define metarea_lbl 535 `"Nashua, NH"', add
label define metarea_lbl 536 `"Nashville, TN"', add
label define metarea_lbl 540 `"New Bedford, MA"', add
label define metarea_lbl 546 `"New Brunswick-Perth Amboy-Sayreville, NJ"', add
label define metarea_lbl 548 `"New Haven-Meriden, CT"', add
label define metarea_lbl 552 `"New London-Norwich, CT/RI"', add
label define metarea_lbl 556 `"New Orleans, LA"', add
label define metarea_lbl 560 `"New York, NY-Northeastern NJ"', add
label define metarea_lbl 564 `"Newark, OH"', add
label define metarea_lbl 566 `"Newburgh-Middletown, NY"', add
label define metarea_lbl 572 `"Norfolk-VA Beach--Newport News, VA"', add
label define metarea_lbl 576 `"Norwalk, CT"', add
label define metarea_lbl 579 `"Ocala, FL"', add
label define metarea_lbl 580 `"Odessa, TX"', add
label define metarea_lbl 588 `"Oklahoma City, OK"', add
label define metarea_lbl 591 `"Olympia, WA"', add
label define metarea_lbl 592 `"Omaha, NE/IA"', add
label define metarea_lbl 595 `"Orange, NY"', add
label define metarea_lbl 596 `"Orlando, FL"', add
label define metarea_lbl 599 `"Owensboro, KY"', add
label define metarea_lbl 601 `"Panama City, FL"', add
label define metarea_lbl 602 `"Parkersburg-Marietta,WV/OH"', add
label define metarea_lbl 603 `"Pascagoula-Moss Point, MS"', add
label define metarea_lbl 608 `"Pensacola, FL"', add
label define metarea_lbl 612 `"Peoria, IL"', add
label define metarea_lbl 616 `"Philadelphia, PA/NJ"', add
label define metarea_lbl 620 `"Phoenix, AZ"', add
label define metarea_lbl 628 `"Pittsburgh, PA"', add
label define metarea_lbl 632 `"Pittsfield, MA"', add
label define metarea_lbl 636 `"Ponce, PR"', add
label define metarea_lbl 640 `"Portland, ME"', add
label define metarea_lbl 644 `"Portland, OR/WA"', add
label define metarea_lbl 645 `"Portsmouth-Dover--Rochester, NH/ME"', add
label define metarea_lbl 646 `"Poughkeepsie, NY"', add
label define metarea_lbl 648 `"Providence-Fall River-Pawtucket, MA/RI"', add
label define metarea_lbl 652 `"Provo-Orem, UT"', add
label define metarea_lbl 656 `"Pueblo, CO"', add
label define metarea_lbl 658 `"Punta Gorda, FL"', add
label define metarea_lbl 660 `"Racine, WI"', add
label define metarea_lbl 664 `"Raleigh-Durham, NC"', add
label define metarea_lbl 666 `"Rapid City, SD"', add
label define metarea_lbl 668 `"Reading, PA"', add
label define metarea_lbl 669 `"Redding, CA"', add
label define metarea_lbl 672 `"Reno, NV"', add
label define metarea_lbl 674 `"Richland-Kennewick-Pasco, WA"', add
label define metarea_lbl 676 `"Richmond-Petersburg, VA"', add
label define metarea_lbl 678 `"Riverside-San Bernardino, CA"', add
label define metarea_lbl 680 `"Roanoke, VA"', add
label define metarea_lbl 682 `"Rochester, MN"', add
label define metarea_lbl 684 `"Rochester, NY"', add
label define metarea_lbl 688 `"Rockford, IL"', add
label define metarea_lbl 689 `"Rocky Mount, NC"', add
label define metarea_lbl 692 `"Sacramento, CA"', add
label define metarea_lbl 696 `"Saginaw-Bay City-Midland, MI"', add
label define metarea_lbl 698 `"St. Cloud, MN"', add
label define metarea_lbl 700 `"St. Joseph, MO"', add
label define metarea_lbl 704 `"St. Louis, MO/IL"', add
label define metarea_lbl 708 `"Salem, OR"', add
label define metarea_lbl 712 `"Salinas-Sea Side-Monterey, CA"', add
label define metarea_lbl 714 `"Salisbury-Concord, NC"', add
label define metarea_lbl 716 `"Salt Lake City-Ogden, UT"', add
label define metarea_lbl 720 `"San Angelo, TX"', add
label define metarea_lbl 724 `"San Antonio, TX"', add
label define metarea_lbl 732 `"San Diego, CA"', add
label define metarea_lbl 736 `"San Francisco-Oakland-Vallejo, CA"', add
label define metarea_lbl 740 `"San Jose, CA"', add
label define metarea_lbl 744 `"San Juan-Bayamon, PR"', add
label define metarea_lbl 746 `"San Luis Obispo-Atascad-P Robles, CA"', add
label define metarea_lbl 747 `"Santa Barbara-Santa Maria-Lompoc, CA"', add
label define metarea_lbl 748 `"Santa Cruz, CA"', add
label define metarea_lbl 749 `"Santa Fe, NM"', add
label define metarea_lbl 750 `"Santa Rosa-Petaluma, CA"', add
label define metarea_lbl 751 `"Sarasota, FL"', add
label define metarea_lbl 752 `"Savannah, GA"', add
label define metarea_lbl 756 `"Scranton-Wilkes-Barre, PA"', add
label define metarea_lbl 760 `"Seattle-Everett, WA"', add
label define metarea_lbl 761 `"Sharon, PA"', add
label define metarea_lbl 762 `"Sheboygan, WI"', add
label define metarea_lbl 764 `"Sherman-Davidson, TX"', add
label define metarea_lbl 768 `"Shreveport, LA"', add
label define metarea_lbl 772 `"Sioux City, IA/NE"', add
label define metarea_lbl 776 `"Sioux Falls, SD"', add
label define metarea_lbl 780 `"South Bend-Mishawaka, IN"', add
label define metarea_lbl 784 `"Spokane, WA"', add
label define metarea_lbl 788 `"Springfield, IL"', add
label define metarea_lbl 792 `"Springfield, MO"', add
label define metarea_lbl 800 `"Springfield-Holyoke-Chicopee, MA"', add
label define metarea_lbl 804 `"Stamford, CT"', add
label define metarea_lbl 805 `"State College, PA"', add
label define metarea_lbl 808 `"Steubenville-Weirton,OH/WV"', add
label define metarea_lbl 812 `"Stockton, CA"', add
label define metarea_lbl 814 `"Sumter, SC"', add
label define metarea_lbl 816 `"Syracuse, NY"', add
label define metarea_lbl 820 `"Tacoma, WA"', add
label define metarea_lbl 824 `"Tallahassee, FL"', add
label define metarea_lbl 828 `"Tampa-St. Petersburg-Clearwater, FL"', add
label define metarea_lbl 832 `"Terre Haute, IN"', add
label define metarea_lbl 836 `"Texarkana, TX/AR"', add
label define metarea_lbl 840 `"Toledo, OH/MI"', add
label define metarea_lbl 844 `"Topeka, KS"', add
label define metarea_lbl 848 `"Trenton, NJ"', add
label define metarea_lbl 852 `"Tucson, AZ"', add
label define metarea_lbl 856 `"Tulsa, OK"', add
label define metarea_lbl 860 `"Tuscaloosa, AL"', add
label define metarea_lbl 864 `"Tyler, TX"', add
label define metarea_lbl 868 `"Utica-Rome, NY"', add
label define metarea_lbl 873 `"Ventura-Oxnard-Simi Valley, CA"', add
label define metarea_lbl 875 `"Victoria, TX"', add
label define metarea_lbl 876 `"Vineland-Milville-Bridgetown, NJ"', add
label define metarea_lbl 878 `"Visalia-Tulare-Porterville, CA"', add
label define metarea_lbl 880 `"Waco, TX"', add
label define metarea_lbl 884 `"Washington, DC/MD/VA"', add
label define metarea_lbl 888 `"Waterbury, CT"', add
label define metarea_lbl 892 `"Waterloo-Cedar Falls, IA"', add
label define metarea_lbl 894 `"Wausau, WI"', add
label define metarea_lbl 896 `"West Palm Beach-Boca Raton-Delray Beach, FL"', add
label define metarea_lbl 900 `"Wheeling, WV/OH"', add
label define metarea_lbl 904 `"Wichita, KS"', add
label define metarea_lbl 908 `"Wichita Falls, TX"', add
label define metarea_lbl 914 `"Williamsport, PA"', add
label define metarea_lbl 916 `"Wilmington, DE/NJ/MD"', add
label define metarea_lbl 920 `"Wilmington, NC"', add
label define metarea_lbl 924 `"Worcester, MA"', add
label define metarea_lbl 926 `"Yakima, WA"', add
label define metarea_lbl 927 `"Yolo, CA"', add
label define metarea_lbl 928 `"York, PA"', add
label define metarea_lbl 932 `"Youngstown-Warren, OH/PA"', add
label define metarea_lbl 934 `"Yuba City, CA"', add
label define metarea_lbl 936 `"Yuma, AZ"', add
label values metarea metarea_lbl

label define metaread_lbl 0000 `"Not identifiable or not in an MSA"'
label define metaread_lbl 0040 `"Abilene, TX"', add
label define metaread_lbl 0060 `"Aguadilla, PR"', add
label define metaread_lbl 0080 `"Akron, OH"', add
label define metaread_lbl 0120 `"Albany, GA"', add
label define metaread_lbl 0160 `"Albany-Schenectady-Troy, NY"', add
label define metaread_lbl 0200 `"Albuquerque, NM"', add
label define metaread_lbl 0220 `"Alexandria, LA"', add
label define metaread_lbl 0240 `"Allentown-Bethlehem-Easton, PA/NJ"', add
label define metaread_lbl 0280 `"Altoona, PA"', add
label define metaread_lbl 0320 `"Amarillo, TX"', add
label define metaread_lbl 0380 `"Anchorage, AK"', add
label define metaread_lbl 0400 `"Anderson, IN"', add
label define metaread_lbl 0440 `"Ann Arbor, MI"', add
label define metaread_lbl 0450 `"Anniston, AL"', add
label define metaread_lbl 0460 `"Appleton-Oshkosh-Neenah, WI"', add
label define metaread_lbl 0470 `"Arecibo, PR"', add
label define metaread_lbl 0480 `"Asheville, NC"', add
label define metaread_lbl 0500 `"Athens, GA"', add
label define metaread_lbl 0520 `"Atlanta, GA"', add
label define metaread_lbl 0560 `"Atlantic City, NJ"', add
label define metaread_lbl 0580 `"Auburn-Opelika, AL"', add
label define metaread_lbl 0600 `"Augusta-Aiken, GA/SC"', add
label define metaread_lbl 0640 `"Austin, TX"', add
label define metaread_lbl 0680 `"Bakersfield, CA"', add
label define metaread_lbl 0720 `"Baltimore, MD"', add
label define metaread_lbl 0730 `"Bangor, ME"', add
label define metaread_lbl 0740 `"Barnstable-Yarmouth, MA"', add
label define metaread_lbl 0760 `"Baton Rouge, LA"', add
label define metaread_lbl 0780 `"Battle Creek, MI"', add
label define metaread_lbl 0840 `"Beaumont-Port Arthur-Orange, TX"', add
label define metaread_lbl 0860 `"Bellingham, WA"', add
label define metaread_lbl 0870 `"Benton Harbor, MI"', add
label define metaread_lbl 0880 `"Billings, MT"', add
label define metaread_lbl 0920 `"Biloxi-Gulfport, MS"', add
label define metaread_lbl 0960 `"Binghamton, NY"', add
label define metaread_lbl 1000 `"Birmingham, AL"', add
label define metaread_lbl 1010 `"Bismarck, ND"', add
label define metaread_lbl 1020 `"Bloomington, IN"', add
label define metaread_lbl 1040 `"Bloomington-Normal, IL"', add
label define metaread_lbl 1080 `"Boise City, ID"', add
label define metaread_lbl 1120 `"Boston, MA"', add
label define metaread_lbl 1121 `"Lawrence-Haverhill, MA/NH"', add
label define metaread_lbl 1122 `"Lowell, MA/NH"', add
label define metaread_lbl 1123 `"Salem-Gloucester, MA"', add
label define metaread_lbl 1140 `"Bradenton, FL"', add
label define metaread_lbl 1150 `"Bremerton, WA"', add
label define metaread_lbl 1160 `"Bridgeport, CT"', add
label define metaread_lbl 1200 `"Brockton, MA"', add
label define metaread_lbl 1240 `"Brownsville-Harlingen-San Benito, TX"', add
label define metaread_lbl 1260 `"Bryan-College Station, TX"', add
label define metaread_lbl 1280 `"Buffalo-Niagara Falls, NY"', add
label define metaread_lbl 1281 `"Niagara Falls, NY"', add
label define metaread_lbl 1300 `"Burlington, NC"', add
label define metaread_lbl 1310 `"Burlington, VT"', add
label define metaread_lbl 1320 `"Canton, OH"', add
label define metaread_lbl 1330 `"Caguas, PR"', add
label define metaread_lbl 1350 `"Casper, WY"', add
label define metaread_lbl 1360 `"Cedar Rapids, IA"', add
label define metaread_lbl 1400 `"Champaign-Urbana-Rantoul, IL"', add
label define metaread_lbl 1440 `"Charleston-N. Charleston, SC"', add
label define metaread_lbl 1480 `"Charleston, WV"', add
label define metaread_lbl 1520 `"Charlotte-Gastonia-Rock Hill, SC"', add
label define metaread_lbl 1521 `"Rock Hill, SC"', add
label define metaread_lbl 1540 `"Charlottesville, VA"', add
label define metaread_lbl 1560 `"Chattanooga, TN/GA"', add
label define metaread_lbl 1580 `"Cheyenne, WY"', add
label define metaread_lbl 1600 `"Chicago-Gary-Lake, IL"', add
label define metaread_lbl 1601 `"Aurora-Elgin, IL"', add
label define metaread_lbl 1602 `"Gary-Hammond-East Chicago, IN"', add
label define metaread_lbl 1603 `"Joliet, IL"', add
label define metaread_lbl 1604 `"Lake County, IL"', add
label define metaread_lbl 1620 `"Chico, CA"', add
label define metaread_lbl 1640 `"Cincinnati, OH/KY/IN"', add
label define metaread_lbl 1660 `"Clarksville-Hopkinsville, TN/KY"', add
label define metaread_lbl 1680 `"Cleveland, OH"', add
label define metaread_lbl 1720 `"Colorado Springs, CO"', add
label define metaread_lbl 1740 `"Columbia, MO"', add
label define metaread_lbl 1760 `"Columbia, SC"', add
label define metaread_lbl 1800 `"Columbus, GA/AL"', add
label define metaread_lbl 1840 `"Columbus, OH"', add
label define metaread_lbl 1880 `"Corpus Christi, TX"', add
label define metaread_lbl 1900 `"Cumberland, MD/WV"', add
label define metaread_lbl 1920 `"Dallas-Fort Worth, TX"', add
label define metaread_lbl 1921 `"Fort Worth-Arlington, TX"', add
label define metaread_lbl 1930 `"Danbury, CT"', add
label define metaread_lbl 1950 `"Danville, VA"', add
label define metaread_lbl 1960 `"Davenport, IA - Rock Island-Moline, IL"', add
label define metaread_lbl 2000 `"Dayton-Springfield, OH"', add
label define metaread_lbl 2001 `"Springfield, OH"', add
label define metaread_lbl 2020 `"Daytona Beach, FL"', add
label define metaread_lbl 2030 `"Decatur, AL"', add
label define metaread_lbl 2040 `"Decatur, IL"', add
label define metaread_lbl 2080 `"Denver-Boulder-Longmont, CO"', add
label define metaread_lbl 2081 `"Boulder-Longmont, CO"', add
label define metaread_lbl 2120 `"Des Moines, IA"', add
label define metaread_lbl 2121 `"Polk, IA"', add
label define metaread_lbl 2160 `"Detroit, MI"', add
label define metaread_lbl 2180 `"Dothan, AL"', add
label define metaread_lbl 2190 `"Dover, DE"', add
label define metaread_lbl 2200 `"Dubuque, IA"', add
label define metaread_lbl 2240 `"Duluth-Superior, MN/WI"', add
label define metaread_lbl 2281 `"Dutchess Co., NY"', add
label define metaread_lbl 2290 `"Eau Claire, WI"', add
label define metaread_lbl 2310 `"El Paso, TX"', add
label define metaread_lbl 2320 `"Elkhart-Goshen, IN"', add
label define metaread_lbl 2330 `"Elmira, NY"', add
label define metaread_lbl 2340 `"Enid, OK"', add
label define metaread_lbl 2360 `"Erie, PA"', add
label define metaread_lbl 2400 `"Eugene-Springfield, OR"', add
label define metaread_lbl 2440 `"Evansville, IN/KY"', add
label define metaread_lbl 2520 `"Fargo-Morehead, ND/MN"', add
label define metaread_lbl 2560 `"Fayetteville, NC"', add
label define metaread_lbl 2580 `"Fayetteville-Springdale, AR"', add
label define metaread_lbl 2600 `"Fitchburg-Leominster, MA"', add
label define metaread_lbl 2620 `"Flagstaff, AZ/UT"', add
label define metaread_lbl 2640 `"Flint, MI"', add
label define metaread_lbl 2650 `"Florence, AL"', add
label define metaread_lbl 2660 `"Florence, SC"', add
label define metaread_lbl 2670 `"Fort Collins-Loveland, CO"', add
label define metaread_lbl 2680 `"Fort Lauderdale-Hollywood-Pompano Beach, FL"', add
label define metaread_lbl 2700 `"Fort Myers-Cape Coral, FL"', add
label define metaread_lbl 2710 `"Fort Pierce, FL"', add
label define metaread_lbl 2720 `"Fort Smith, AR/OK"', add
label define metaread_lbl 2750 `"Fort Walton Beach, FL"', add
label define metaread_lbl 2760 `"Fort Wayne, IN"', add
label define metaread_lbl 2840 `"Fresno, CA"', add
label define metaread_lbl 2880 `"Gadsden, AL"', add
label define metaread_lbl 2900 `"Gainesville, FL"', add
label define metaread_lbl 2920 `"Galveston-Texas City, TX"', add
label define metaread_lbl 2970 `"Glens Falls, NY"', add
label define metaread_lbl 2980 `"Goldsboro, NC"', add
label define metaread_lbl 2990 `"Grand Forks, ND/MN"', add
label define metaread_lbl 3000 `"Grand Rapids, MI"', add
label define metaread_lbl 3010 `"Grand Junction, CO"', add
label define metaread_lbl 3040 `"Great Falls, MT"', add
label define metaread_lbl 3060 `"Greeley, CO"', add
label define metaread_lbl 3080 `"Green Bay, WI"', add
label define metaread_lbl 3120 `"Greensboro-Winston Salem-High Point, NC"', add
label define metaread_lbl 3121 `"Winston-Salem, NC"', add
label define metaread_lbl 3150 `"Greenville, NC"', add
label define metaread_lbl 3160 `"Greenville-Spartenburg-Anderson, SC"', add
label define metaread_lbl 3161 `"Anderson, SC"', add
label define metaread_lbl 3180 `"Hagerstown, MD"', add
label define metaread_lbl 3200 `"Hamilton-Middleton, OH"', add
label define metaread_lbl 3240 `"Harrisburg-Lebanon-Carlisle, PA"', add
label define metaread_lbl 3280 `"Hartford-Bristol-Middleton-New Britain, CT"', add
label define metaread_lbl 3281 `"Bristol, CT"', add
label define metaread_lbl 3282 `"Middletown, CT"', add
label define metaread_lbl 3283 `"New Britain, CT"', add
label define metaread_lbl 3290 `"Hickory-Morganton, NC"', add
label define metaread_lbl 3300 `"Hattiesburg, MS"', add
label define metaread_lbl 3320 `"Honolulu, HI"', add
label define metaread_lbl 3350 `"Houma-Thibodoux, LA"', add
label define metaread_lbl 3360 `"Houston-Brazoria, TX"', add
label define metaread_lbl 3361 `"Brazoria, TX"', add
label define metaread_lbl 3400 `"Huntington-Ashland, WV/KY/OH"', add
label define metaread_lbl 3440 `"Huntsville, AL"', add
label define metaread_lbl 3480 `"Indianapolis, IN"', add
label define metaread_lbl 3500 `"Iowa City, IA"', add
label define metaread_lbl 3520 `"Jackson, MI"', add
label define metaread_lbl 3560 `"Jackson, MS"', add
label define metaread_lbl 3580 `"Jackson, TN"', add
label define metaread_lbl 3590 `"Jacksonville, FL"', add
label define metaread_lbl 3600 `"Jacksonville, NC"', add
label define metaread_lbl 3610 `"Jamestown-Dunkirk, NY"', add
label define metaread_lbl 3620 `"Janesville-Beloit, WI"', add
label define metaread_lbl 3660 `"Johnson City-Kingsport-Bristol, TN/VA"', add
label define metaread_lbl 3680 `"Johnstown, PA"', add
label define metaread_lbl 3710 `"Joplin, MO"', add
label define metaread_lbl 3720 `"Kalamazoo-Portage, MI"', add
label define metaread_lbl 3740 `"Kankakee, IL"', add
label define metaread_lbl 3760 `"Kansas City, MO/KS"', add
label define metaread_lbl 3800 `"Kenosha, WI"', add
label define metaread_lbl 3810 `"Kileen-Temple, TX"', add
label define metaread_lbl 3840 `"Knoxville, TN"', add
label define metaread_lbl 3850 `"Kokomo, IN"', add
label define metaread_lbl 3870 `"LaCrosse, WI"', add
label define metaread_lbl 3880 `"Lafayette, LA"', add
label define metaread_lbl 3920 `"Lafayette-W. Lafayette, IN"', add
label define metaread_lbl 3960 `"Lake Charles, LA"', add
label define metaread_lbl 3980 `"Lakeland-Winterhaven, FL"', add
label define metaread_lbl 4000 `"Lancaster, PA"', add
label define metaread_lbl 4040 `"Lansing-E. Lansing, MI"', add
label define metaread_lbl 4080 `"Laredo, TX"', add
label define metaread_lbl 4100 `"Las Cruces, NM"', add
label define metaread_lbl 4120 `"Las Vegas, NV"', add
label define metaread_lbl 4150 `"Lawrence, KS"', add
label define metaread_lbl 4200 `"Lawton, OK"', add
label define metaread_lbl 4240 `"Lewiston-Auburn, ME"', add
label define metaread_lbl 4280 `"Lexington-Fayette, KY"', add
label define metaread_lbl 4320 `"Lima, OH"', add
label define metaread_lbl 4360 `"Lincoln, NE"', add
label define metaread_lbl 4400 `"Little Rock-N. Little Rock, AR"', add
label define metaread_lbl 4410 `"Long Branch-Asbury Park, NJ"', add
label define metaread_lbl 4420 `"Longview-Marshall, TX"', add
label define metaread_lbl 4440 `"Lorain-Elyria, OH"', add
label define metaread_lbl 4480 `"Los Angeles-Long Beach, CA"', add
label define metaread_lbl 4481 `"Anaheim-Santa Ana-Garden Grove, CA"', add
label define metaread_lbl 4482 `"Orange County, CA"', add
label define metaread_lbl 4520 `"Louisville, KY/IN"', add
label define metaread_lbl 4600 `"Lubbock, TX"', add
label define metaread_lbl 4640 `"Lynchburg, VA"', add
label define metaread_lbl 4680 `"Macon-Warner Robins, GA"', add
label define metaread_lbl 4720 `"Madison, WI"', add
label define metaread_lbl 4760 `"Manchester, NH"', add
label define metaread_lbl 4800 `"Mansfield, OH"', add
label define metaread_lbl 4840 `"Mayaguez, PR"', add
label define metaread_lbl 4880 `"McAllen-Edinburg-Pharr-Mission, TX"', add
label define metaread_lbl 4890 `"Medford, OR"', add
label define metaread_lbl 4900 `"Melbourne-Titusville-Cocoa-Palm Bay, FL"', add
label define metaread_lbl 4920 `"Memphis, TN/AR/MS"', add
label define metaread_lbl 4940 `"Merced, CA"', add
label define metaread_lbl 5000 `"Miami-Hialeah, FL"', add
label define metaread_lbl 5040 `"Midland, TX"', add
label define metaread_lbl 5080 `"Milwaukee, WI"', add
label define metaread_lbl 5120 `"Minneapolis-St. Paul, MN"', add
label define metaread_lbl 5140 `"Missoula, MT"', add
label define metaread_lbl 5160 `"Mobile, AL"', add
label define metaread_lbl 5170 `"Modesto, CA"', add
label define metaread_lbl 5190 `"Monmouth-Ocean, NJ"', add
label define metaread_lbl 5200 `"Monroe, LA"', add
label define metaread_lbl 5240 `"Montgomery, AL"', add
label define metaread_lbl 5280 `"Muncie, IN"', add
label define metaread_lbl 5320 `"Muskegon-Norton Shores-Muskegon Heights, MI"', add
label define metaread_lbl 5330 `"Myrtle Beach, SC"', add
label define metaread_lbl 5340 `"Naples, FL"', add
label define metaread_lbl 5350 `"Nashua, NH"', add
label define metaread_lbl 5360 `"Nashville, TN"', add
label define metaread_lbl 5400 `"New Bedford, MA"', add
label define metaread_lbl 5460 `"New Brunswick-Perth Amboy-Sayreville, NJ"', add
label define metaread_lbl 5480 `"New Haven-Meriden, CT"', add
label define metaread_lbl 5481 `"Meriden"', add
label define metaread_lbl 5482 `"New Haven, CT"', add
label define metaread_lbl 5520 `"New London-Norwich, CT/RI"', add
label define metaread_lbl 5560 `"New Orleans, LA"', add
label define metaread_lbl 5600 `"New York, NY-Northeastern NJ"', add
label define metaread_lbl 5601 `"Nassau Co, NY"', add
label define metaread_lbl 5602 `"Bergen-Passaic, NJ"', add
label define metaread_lbl 5603 `"Jersey City, NJ"', add
label define metaread_lbl 5604 `"Middlesex-Somerset-Hunterdon, NJ"', add
label define metaread_lbl 5605 `"Newark, NJ"', add
label define metaread_lbl 5640 `"Newark, OH"', add
label define metaread_lbl 5660 `"Newburgh-Middletown, NY"', add
label define metaread_lbl 5720 `"Norfolk-VA Beach-Newport News, VA"', add
label define metaread_lbl 5721 `"Newport News-Hampton"', add
label define metaread_lbl 5722 `"Norfolk- VA Beach-Portsmouth"', add
label define metaread_lbl 5760 `"Norwalk, CT"', add
label define metaread_lbl 5790 `"Ocala, FL"', add
label define metaread_lbl 5800 `"Odessa, TX"', add
label define metaread_lbl 5880 `"Oklahoma City, OK"', add
label define metaread_lbl 5910 `"Olympia, WA"', add
label define metaread_lbl 5920 `"Omaha, NE/IA"', add
label define metaread_lbl 5950 `"Orange, NY"', add
label define metaread_lbl 5960 `"Orlando, FL"', add
label define metaread_lbl 5990 `"Owensboro, KY"', add
label define metaread_lbl 6010 `"Panama City, FL"', add
label define metaread_lbl 6020 `"Parkersburg-Marietta,WV/OH"', add
label define metaread_lbl 6030 `"Pascagoula-Moss Point, MS"', add
label define metaread_lbl 6080 `"Pensacola, FL"', add
label define metaread_lbl 6120 `"Peoria, IL"', add
label define metaread_lbl 6160 `"Philadelphia, PA/NJ"', add
label define metaread_lbl 6200 `"Phoenix, AZ"', add
label define metaread_lbl 6240 `"Pine Bluff, AR"', add
label define metaread_lbl 6280 `"Pittsburgh-Beaver Valley, PA"', add
label define metaread_lbl 6281 `"Beaver County, PA"', add
label define metaread_lbl 6320 `"Pittsfield, MA"', add
label define metaread_lbl 6360 `"Ponce, PR"', add
label define metaread_lbl 6400 `"Portland, ME"', add
label define metaread_lbl 6440 `"Portland-Vancouver, OR"', add
label define metaread_lbl 6441 `"Vancouver, WA"', add
label define metaread_lbl 6450 `"Portsmouth-Dover-Rochester, NH/ME"', add
label define metaread_lbl 6460 `"Poughkeepsie, NY"', add
label define metaread_lbl 6480 `"Providence-Fall River-Pawtucket, MA/RI"', add
label define metaread_lbl 6481 `"Fall River, MA/RI"', add
label define metaread_lbl 6482 `"Pawtuckett-Woonsocket-Attleboro, RI/MA"', add
label define metaread_lbl 6520 `"Provo-Orem, UT"', add
label define metaread_lbl 6560 `"Pueblo, CO"', add
label define metaread_lbl 6580 `"Punta Gorda, FL"', add
label define metaread_lbl 6600 `"Racine, WI"', add
label define metaread_lbl 6640 `"Raleigh-Durham, NC"', add
label define metaread_lbl 6641 `"Durham, NC"', add
label define metaread_lbl 6660 `"Rapid City, SD"', add
label define metaread_lbl 6680 `"Reading, PA"', add
label define metaread_lbl 6690 `"Redding, CA"', add
label define metaread_lbl 6720 `"Reno, NV"', add
label define metaread_lbl 6740 `"Richland-Kennewick-Pasco, WA"', add
label define metaread_lbl 6760 `"Richmond-Petersburg, VA"', add
label define metaread_lbl 6761 `"Petersburg-Colonial Heights, VA"', add
label define metaread_lbl 6780 `"Riverside-San Bernardino, CA"', add
label define metaread_lbl 6781 `"San Bernardino, CA"', add
label define metaread_lbl 6800 `"Roanoke, VA"', add
label define metaread_lbl 6820 `"Rochester, MN"', add
label define metaread_lbl 6840 `"Rochester, NY"', add
label define metaread_lbl 6880 `"Rockford, IL"', add
label define metaread_lbl 6895 `"Rocky Mount, NC"', add
label define metaread_lbl 6920 `"Sacramento, CA"', add
label define metaread_lbl 6960 `"Saginaw-Bay City-Midland, MI"', add
label define metaread_lbl 6961 `"Bay City, MI"', add
label define metaread_lbl 6980 `"St. Cloud, MN"', add
label define metaread_lbl 7000 `"St. Joseph, MO"', add
label define metaread_lbl 7040 `"St. Louis, MO/IL"', add
label define metaread_lbl 7080 `"Salem, OR"', add
label define metaread_lbl 7120 `"Salinas-Sea Side-Monterey, CA"', add
label define metaread_lbl 7140 `"Salisbury-Concord, NC"', add
label define metaread_lbl 7160 `"Salt Lake City-Ogden, UT"', add
label define metaread_lbl 7161 `"Ogden"', add
label define metaread_lbl 7200 `"San Angelo, TX"', add
label define metaread_lbl 7240 `"San Antonio, TX"', add
label define metaread_lbl 7320 `"San Diego, CA"', add
label define metaread_lbl 7360 `"San Francisco-Oakland-Vallejo, CA"', add
label define metaread_lbl 7361 `"Oakland, CA"', add
label define metaread_lbl 7362 `"Vallejo-Fairfield-Napa, CA"', add
label define metaread_lbl 7400 `"San Jose, CA"', add
label define metaread_lbl 7440 `"San Juan-Bayamon, PR"', add
label define metaread_lbl 7460 `"San Luis Obispo-Atascad-P Robles, CA"', add
label define metaread_lbl 7470 `"Santa Barbara-Santa Maria-Lompoc, CA"', add
label define metaread_lbl 7480 `"Santa Cruz, CA"', add
label define metaread_lbl 7490 `"Santa Fe, NM"', add
label define metaread_lbl 7500 `"Santa Rosa-Petaluma, CA"', add
label define metaread_lbl 7510 `"Sarasota, FL"', add
label define metaread_lbl 7520 `"Savannah, GA"', add
label define metaread_lbl 7560 `"Scranton-Wilkes-Barre, PA"', add
label define metaread_lbl 7561 `"Wilkes-Barre-Hazelton, PA"', add
label define metaread_lbl 7600 `"Seattle-Everett, WA"', add
label define metaread_lbl 7610 `"Sharon, PA"', add
label define metaread_lbl 7620 `"Sheboygan, WI"', add
label define metaread_lbl 7640 `"Sherman-Denison, TX"', add
label define metaread_lbl 7680 `"Shreveport, LA"', add
label define metaread_lbl 7720 `"Sioux City, IA/NE"', add
label define metaread_lbl 7760 `"Sioux Falls, SD"', add
label define metaread_lbl 7800 `"South Bend-Mishawaka, IN"', add
label define metaread_lbl 7840 `"Spokane, WA"', add
label define metaread_lbl 7880 `"Springfield, IL"', add
label define metaread_lbl 7920 `"Springfield, MO"', add
label define metaread_lbl 8000 `"Springfield-Holyoke-Chicopee, MA"', add
label define metaread_lbl 8040 `"Stamford, CT"', add
label define metaread_lbl 8050 `"State College, PA"', add
label define metaread_lbl 8080 `"Steubenville-Weirton,OH/WV"', add
label define metaread_lbl 8120 `"Stockton, CA"', add
label define metaread_lbl 8140 `"Sumter, SC"', add
label define metaread_lbl 8160 `"Syracuse, NY"', add
label define metaread_lbl 8200 `"Tacoma, WA"', add
label define metaread_lbl 8240 `"Tallahassee, FL"', add
label define metaread_lbl 8280 `"Tampa-St. Petersburg-Clearwater, FL"', add
label define metaread_lbl 8320 `"Terre Haute, IN"', add
label define metaread_lbl 8360 `"Texarkana, TX/AR"', add
label define metaread_lbl 8400 `"Toledo, OH/MI"', add
label define metaread_lbl 8440 `"Topeka, KS"', add
label define metaread_lbl 8480 `"Trenton, NJ"', add
label define metaread_lbl 8520 `"Tucson, AZ"', add
label define metaread_lbl 8560 `"Tulsa, OK"', add
label define metaread_lbl 8600 `"Tuscaloosa, AL"', add
label define metaread_lbl 8640 `"Tyler, TX"', add
label define metaread_lbl 8680 `"Utica-Rome, NY"', add
label define metaread_lbl 8730 `"Ventura-Oxnard-Simi Valley, CA"', add
label define metaread_lbl 8750 `"Victoria, TX"', add
label define metaread_lbl 8760 `"Vineland-Milville-Bridgetown, NJ"', add
label define metaread_lbl 8780 `"Visalia-Tulare-Porterville, CA"', add
label define metaread_lbl 8800 `"Waco, TX"', add
label define metaread_lbl 8840 `"Washington, DC/MD/VA"', add
label define metaread_lbl 8880 `"Waterbury, CT"', add
label define metaread_lbl 8920 `"Waterloo-Cedar Falls, IA"', add
label define metaread_lbl 8940 `"Wausau, WI"', add
label define metaread_lbl 8960 `"West Palm Beach-Boca Raton-Delray Beach, FL"', add
label define metaread_lbl 9000 `"Wheeling, WV/OH"', add
label define metaread_lbl 9040 `"Wichita, KS"', add
label define metaread_lbl 9080 `"Wichita Falls, TX"', add
label define metaread_lbl 9140 `"Williamsport, PA"', add
label define metaread_lbl 9160 `"Wilmington, DE/NJ/MD"', add
label define metaread_lbl 9200 `"Wilmington, NC"', add
label define metaread_lbl 9240 `"Worcester, MA"', add
label define metaread_lbl 9260 `"Yakima, WA"', add
label define metaread_lbl 9270 `"Yolo, CA"', add
label define metaread_lbl 9280 `"York, PA"', add
label define metaread_lbl 9320 `"Youngstown-Warren, OH/PA"', add
label define metaread_lbl 9340 `"Yuba City, CA"', add
label define metaread_lbl 9360 `"Yuma, AZ"', add
label values metaread metaread_lbl

label define met2013_lbl 00000 `"Not in identifiable area"'
label define met2013_lbl 10420 `"Akron, OH"', add
label define met2013_lbl 10540 `"Albany, OR"', add
label define met2013_lbl 10580 `"Albany-Schenectady-Troy, NY"', add
label define met2013_lbl 10740 `"Albuquerque, NM"', add
label define met2013_lbl 10780 `"Alexandria, LA"', add
label define met2013_lbl 10900 `"Allentown-Bethlehem-Easton, PA-NJ"', add
label define met2013_lbl 11020 `"Altoona, PA"', add
label define met2013_lbl 11100 `"Amarillo, TX"', add
label define met2013_lbl 11260 `"Anchorage, AK"', add
label define met2013_lbl 11460 `"Ann Arbor, MI"', add
label define met2013_lbl 11500 `"Anniston-Oxford-Jacksonville, AL"', add
label define met2013_lbl 11700 `"Asheville, NC"', add
label define met2013_lbl 12020 `"Athens-Clarke County, GA"', add
label define met2013_lbl 12060 `"Atlanta-Sandy Springs-Roswell, GA"', add
label define met2013_lbl 12100 `"Atlantic City-Hammonton, NJ"', add
label define met2013_lbl 12220 `"Auburn-Opelika, AL"', add
label define met2013_lbl 12260 `"Augusta-Richmond County, GA-SC"', add
label define met2013_lbl 12420 `"Austin-Round Rock, TX"', add
label define met2013_lbl 12540 `"Bakersfield, CA"', add
label define met2013_lbl 12580 `"Baltimore-Columbia-Towson, MD"', add
label define met2013_lbl 12620 `"Bangor, ME"', add
label define met2013_lbl 12700 `"Barnstable Town, MA"', add
label define met2013_lbl 12940 `"Baton Rouge, LA"', add
label define met2013_lbl 12980 `"Battle Creek, MI"', add
label define met2013_lbl 13140 `"Beaumont-Port Arthur, TX"', add
label define met2013_lbl 13220 `"Beckley, WV"', add
label define met2013_lbl 13380 `"Bellingham, WA"', add
label define met2013_lbl 13460 `"Bend-Redmond, OR"', add
label define met2013_lbl 13740 `"Billings, MT"', add
label define met2013_lbl 13780 `"Binghamton, NY"', add
label define met2013_lbl 13820 `"Birmingham-Hoover, AL"', add
label define met2013_lbl 13900 `"Bismarck, ND"', add
label define met2013_lbl 13980 `"Blacksburg-Christiansburg-Radford, VA"', add
label define met2013_lbl 14010 `"Bloomington, IL"', add
label define met2013_lbl 14020 `"Bloomington, IN"', add
label define met2013_lbl 14260 `"Boise City, ID"', add
label define met2013_lbl 14460 `"Boston-Cambridge-Newton, MA-NH"', add
label define met2013_lbl 14740 `"Bremerton-Silverdale, WA"', add
label define met2013_lbl 14860 `"Bridgeport-Stamford-Norwalk, CT"', add
label define met2013_lbl 15180 `"Brownsville-Harlingen, TX"', add
label define met2013_lbl 15380 `"Buffalo-Cheektowaga-Niagara Falls, NY"', add
label define met2013_lbl 15500 `"Burlington, NC"', add
label define met2013_lbl 15540 `"Burlington-South Burlington, VT"', add
label define met2013_lbl 15680 `"California-Lexington Park, MD"', add
label define met2013_lbl 15940 `"Canton-Massillon, OH"', add
label define met2013_lbl 15980 `"Cape Coral-Fort Myers, FL"', add
label define met2013_lbl 16580 `"Champaign-Urbana, IL"', add
label define met2013_lbl 16620 `"Charleston, WV"', add
label define met2013_lbl 16700 `"Charleston-North Charleston, SC"', add
label define met2013_lbl 16740 `"Charlotte-Concord-Gastonia, NC-SC"', add
label define met2013_lbl 16820 `"Charlottesville, VA"', add
label define met2013_lbl 16860 `"Chattanooga, TN-GA"', add
label define met2013_lbl 16940 `"Cheyenne, WY"', add
label define met2013_lbl 16980 `"Chicago-Naperville-Elgin, IL-IN-WI"', add
label define met2013_lbl 17020 `"Chico, CA"', add
label define met2013_lbl 17140 `"Cincinnati, OH-KY-IN"', add
label define met2013_lbl 17300 `"Clarksville, TN-KY"', add
label define met2013_lbl 17420 `"Cleveland, TN"', add
label define met2013_lbl 17460 `"Cleveland-Elyria, OH"', add
label define met2013_lbl 17660 `"Coeur d'Alene, ID"', add
label define met2013_lbl 17780 `"College Station-Bryan, TX"', add
label define met2013_lbl 17820 `"Colorado Springs, CO"', add
label define met2013_lbl 17860 `"Columbia, MO"', add
label define met2013_lbl 17900 `"Columbia, SC"', add
label define met2013_lbl 18140 `"Columbus, OH"', add
label define met2013_lbl 18580 `"Corpus Christi, TX"', add
label define met2013_lbl 18700 `"Corvallis, OR"', add
label define met2013_lbl 18880 `"Crestview-Fort Walton Beach-Destin, FL"', add
label define met2013_lbl 19100 `"Dallas-Fort Worth-Arlington, TX"', add
label define met2013_lbl 19300 `"Daphne-Fairhope-Foley, AL"', add
label define met2013_lbl 19340 `"Davenport-Moline-Rock Island, IA-IL"', add
label define met2013_lbl 19380 `"Dayton, OH"', add
label define met2013_lbl 19460 `"Decatur, AL"', add
label define met2013_lbl 19500 `"Decatur, IL"', add
label define met2013_lbl 19660 `"Deltona-Daytona Beach-Ormond Beach, FL"', add
label define met2013_lbl 19740 `"Denver-Aurora-Lakewood, CO"', add
label define met2013_lbl 19780 `"Des Moines-West Des Moines, IA"', add
label define met2013_lbl 19820 `"Detroit-Warren-Dearborn, MI"', add
label define met2013_lbl 20020 `"Dothan, AL"', add
label define met2013_lbl 20100 `"Dover, DE"', add
label define met2013_lbl 20500 `"Durham-Chapel Hill, NC"', add
label define met2013_lbl 20700 `"East Stroudsburg, PA"', add
label define met2013_lbl 20740 `"Eau Claire, WI"', add
label define met2013_lbl 20940 `"El Centro, CA"', add
label define met2013_lbl 21060 `"Elizabethtown-Fort Knox, KY"', add
label define met2013_lbl 21140 `"Elkhart-Goshen, IN"', add
label define met2013_lbl 21340 `"El Paso, TX"', add
label define met2013_lbl 21500 `"Erie, PA"', add
label define met2013_lbl 21660 `"Eugene, OR"', add
label define met2013_lbl 21780 `"Evansville, IN-KY"', add
label define met2013_lbl 22140 `"Farmington, NM"', add
label define met2013_lbl 22180 `"Fayetteville, NC"', add
label define met2013_lbl 22220 `"Fayetteville-Springdale-Rogers, AR-MO"', add
label define met2013_lbl 22380 `"Flagstaff, AZ"', add
label define met2013_lbl 22420 `"Flint, MI"', add
label define met2013_lbl 22500 `"Florence, SC"', add
label define met2013_lbl 22520 `"Florence-Muscle Shoals, AL"', add
label define met2013_lbl 22660 `"Fort Collins, CO"', add
label define met2013_lbl 23060 `"Fort Wayne, IN"', add
label define met2013_lbl 23420 `"Fresno, CA"', add
label define met2013_lbl 23460 `"Gadsden, AL"', add
label define met2013_lbl 23540 `"Gainesville, FL"', add
label define met2013_lbl 23580 `"Gainesville, GA"', add
label define met2013_lbl 24020 `"Glens Falls, NY"', add
label define met2013_lbl 24140 `"Goldsboro, NC"', add
label define met2013_lbl 24300 `"Grand Junction, CO"', add
label define met2013_lbl 24340 `"Grand Rapids-Wyoming, MI"', add
label define met2013_lbl 24540 `"Greeley, CO"', add
label define met2013_lbl 24660 `"Greensboro-High Point, NC"', add
label define met2013_lbl 24780 `"Greenville, NC"', add
label define met2013_lbl 24860 `"Greenville-Anderson-Mauldin, SC"', add
label define met2013_lbl 25060 `"Gulfport-Biloxi-Pascagoula, MS"', add
label define met2013_lbl 25220 `"Hammond, LA"', add
label define met2013_lbl 25260 `"Hanford-Corcoran, CA"', add
label define met2013_lbl 25420 `"Harrisburg-Carlisle, PA"', add
label define met2013_lbl 25500 `"Harrisonburg, VA"', add
label define met2013_lbl 25540 `"Hartford-West Hartford-East Hartford, CT"', add
label define met2013_lbl 25620 `"Hattiesburg, MS"', add
label define met2013_lbl 25860 `"Hickory-Lenoir-Morganton, NC"', add
label define met2013_lbl 25940 `"Hilton Head Island-Bluffton-Beaufort, SC"', add
label define met2013_lbl 26140 `"Homosassa Springs, FL"', add
label define met2013_lbl 26380 `"Houma-Thibodaux, LA"', add
label define met2013_lbl 26420 `"Houston-The Woodlands-Sugar Land, TX"', add
label define met2013_lbl 26620 `"Huntsville, AL"', add
label define met2013_lbl 26900 `"Indianapolis-Carmel-Anderson, IN"', add
label define met2013_lbl 26980 `"Iowa City, IA"', add
label define met2013_lbl 27060 `"Ithaca, NY"', add
label define met2013_lbl 27100 `"Jackson, MI"', add
label define met2013_lbl 27140 `"Jackson, MS"', add
label define met2013_lbl 27180 `"Jackson, TN"', add
label define met2013_lbl 27260 `"Jacksonville, FL"', add
label define met2013_lbl 27340 `"Jacksonville, NC"', add
label define met2013_lbl 27500 `"Janesville-Beloit, WI"', add
label define met2013_lbl 27620 `"Jefferson City, MO"', add
label define met2013_lbl 27740 `"Johnson City, TN"', add
label define met2013_lbl 27780 `"Johnstown, PA"', add
label define met2013_lbl 27860 `"Jonesboro, AR"', add
label define met2013_lbl 27900 `"Joplin, MO"', add
label define met2013_lbl 28020 `"Kalamazoo-Portage, MI"', add
label define met2013_lbl 28100 `"Kankakee, IL"', add
label define met2013_lbl 28140 `"Kansas City, MO-KS"', add
label define met2013_lbl 28420 `"Kennewick-Richland, WA"', add
label define met2013_lbl 28660 `"Killeen-Temple, TX"', add
label define met2013_lbl 28700 `"Kingsport-Bristol-Bristol, TN-VA"', add
label define met2013_lbl 28940 `"Knoxville, TN"', add
label define met2013_lbl 29100 `"La Crosse-Onalaska, WI-MN"', add
label define met2013_lbl 29180 `"Lafayette, LA"', add
label define met2013_lbl 29200 `"Lafayette-West Lafayette, IN"', add
label define met2013_lbl 29340 `"Lake Charles, LA"', add
label define met2013_lbl 29420 `"Lake Havasu City-Kingman, AZ"', add
label define met2013_lbl 29460 `"Lakeland-Winter Haven, FL"', add
label define met2013_lbl 29540 `"Lancaster, PA"', add
label define met2013_lbl 29620 `"Lansing-East Lansing, MI"', add
label define met2013_lbl 29700 `"Laredo, TX"', add
label define met2013_lbl 29740 `"Las Cruces, NM"', add
label define met2013_lbl 29820 `"Las Vegas-Henderson-Paradise, NV"', add
label define met2013_lbl 29940 `"Lawrence, KS"', add
label define met2013_lbl 30020 `"Lawton, OK"', add
label define met2013_lbl 30140 `"Lebanon, PA"', add
label define met2013_lbl 30340 `"Lewiston-Auburn, ME"', add
label define met2013_lbl 30620 `"Lima, OH"', add
label define met2013_lbl 30700 `"Lincoln, NE"', add
label define met2013_lbl 30780 `"Little Rock-North Little Rock-Conway, AR"', add
label define met2013_lbl 31080 `"Los Angeles-Long Beach-Anaheim, CA"', add
label define met2013_lbl 31140 `"Louisville/Jefferson County, KY-IN"', add
label define met2013_lbl 31180 `"Lubbock, TX"', add
label define met2013_lbl 31340 `"Lynchburg, VA"', add
label define met2013_lbl 31460 `"Madera, CA"', add
label define met2013_lbl 31700 `"Manchester-Nashua, NH"', add
label define met2013_lbl 31860 `"Mankato-North Mankato, MN"', add
label define met2013_lbl 31900 `"Mansfield, OH"', add
label define met2013_lbl 32420 `"Mayagüez, PR"', add
label define met2013_lbl 32580 `"McAllen-Edinburg-Mission, TX"', add
label define met2013_lbl 32780 `"Medford, OR"', add
label define met2013_lbl 32820 `"Memphis, TN-MS-AR"', add
label define met2013_lbl 32900 `"Merced, CA"', add
label define met2013_lbl 33100 `"Miami-Fort Lauderdale-West Palm Beach, FL"', add
label define met2013_lbl 33140 `"Michigan City-La Porte, IN"', add
label define met2013_lbl 33260 `"Midland, TX"', add
label define met2013_lbl 33340 `"Milwaukee-Waukesha-West Allis, WI"', add
label define met2013_lbl 33460 `"Minneapolis-St. Paul-Bloomington, MN-WI"', add
label define met2013_lbl 33660 `"Mobile, AL"', add
label define met2013_lbl 33700 `"Modesto, CA"', add
label define met2013_lbl 33740 `"Monroe, LA"', add
label define met2013_lbl 33780 `"Monroe, MI"', add
label define met2013_lbl 33860 `"Montgomery, AL"', add
label define met2013_lbl 34060 `"Morgantown, WV"', add
label define met2013_lbl 34580 `"Mount Vernon-Anacortes, WA"', add
label define met2013_lbl 34620 `"Muncie, IN"', add
label define met2013_lbl 34740 `"Muskegon, MI"', add
label define met2013_lbl 34820 `"Myrtle Beach-Conway-North Myrtle Beach, SC-NC"', add
label define met2013_lbl 34900 `"Napa, CA"', add
label define met2013_lbl 34940 `"Naples-Immokalee-Marco Island, FL"', add
label define met2013_lbl 34980 `"Nashville-Davidson--Murfreesboro--Franklin, TN"', add
label define met2013_lbl 35300 `"New Haven-Milford, CT"', add
label define met2013_lbl 35380 `"New Orleans-Metairie, LA"', add
label define met2013_lbl 35620 `"New York-Newark-Jersey City, NY-NJ-PA"', add
label define met2013_lbl 35660 `"Niles-Benton Harbor, MI"', add
label define met2013_lbl 35840 `"North Port-Sarasota-Bradenton, FL"', add
label define met2013_lbl 35980 `"Norwich-New London, CT"', add
label define met2013_lbl 36100 `"Ocala, FL"', add
label define met2013_lbl 36140 `"Ocean City, NJ"', add
label define met2013_lbl 36220 `"Odessa, TX"', add
label define met2013_lbl 36260 `"Ogden-Clearfield, UT"', add
label define met2013_lbl 36420 `"Oklahoma City, OK"', add
label define met2013_lbl 36500 `"Olympia-Tumwater, WA"', add
label define met2013_lbl 36540 `"Omaha-Council Bluffs, NE-IA"', add
label define met2013_lbl 36740 `"Orlando-Kissimmee-Sanford, FL"', add
label define met2013_lbl 36780 `"Oshkosh-Neenah, WI"', add
label define met2013_lbl 36980 `"Owensboro, KY"', add
label define met2013_lbl 37100 `"Oxnard-Thousand Oaks-Ventura, CA"', add
label define met2013_lbl 37340 `"Palm Bay-Melbourne-Titusville, FL"', add
label define met2013_lbl 37460 `"Panama City, FL"', add
label define met2013_lbl 37620 `"Parkersburg-Vienna, WV"', add
label define met2013_lbl 37860 `"Pensacola-Ferry Pass-Brent, FL"', add
label define met2013_lbl 37900 `"Peoria, IL"', add
label define met2013_lbl 37980 `"Philadelphia-Camden-Wilmington, PA-NJ-DE-MD"', add
label define met2013_lbl 38060 `"Phoenix-Mesa-Scottsdale, AZ"', add
label define met2013_lbl 38300 `"Pittsburgh, PA"', add
label define met2013_lbl 38340 `"Pittsfield, MA"', add
label define met2013_lbl 38660 `"Ponce, PR"', add
label define met2013_lbl 38860 `"Portland-South Portland, ME"', add
label define met2013_lbl 38900 `"Portland-Vancouver-Hillsboro, OR-WA"', add
label define met2013_lbl 38940 `"Port St. Lucie, FL"', add
label define met2013_lbl 39140 `"Prescott, AZ"', add
label define met2013_lbl 39300 `"Providence-Warwick, RI-MA"', add
label define met2013_lbl 39340 `"Provo-Orem, UT"', add
label define met2013_lbl 39380 `"Pueblo, CO"', add
label define met2013_lbl 39460 `"Punta Gorda, FL"', add
label define met2013_lbl 39540 `"Racine, WI"', add
label define met2013_lbl 39580 `"Raleigh, NC"', add
label define met2013_lbl 39740 `"Reading, PA"', add
label define met2013_lbl 39820 `"Redding, CA"', add
label define met2013_lbl 39900 `"Reno, NV"', add
label define met2013_lbl 40060 `"Richmond, VA"', add
label define met2013_lbl 40140 `"Riverside-San Bernardino-Ontario, CA"', add
label define met2013_lbl 40220 `"Roanoke, VA"', add
label define met2013_lbl 40380 `"Rochester, NY"', add
label define met2013_lbl 40420 `"Rockford, IL"', add
label define met2013_lbl 40580 `"Rocky Mount, NC"', add
label define met2013_lbl 40900 `"Sacramento--Roseville--Arden-Arcade, CA"', add
label define met2013_lbl 40980 `"Saginaw, MI"', add
label define met2013_lbl 41060 `"St. Cloud, MN"', add
label define met2013_lbl 41100 `"St. George, UT"', add
label define met2013_lbl 41140 `"St. Joseph, MO-KS"', add
label define met2013_lbl 41180 `"St. Louis, MO-IL"', add
label define met2013_lbl 41420 `"Salem, OR"', add
label define met2013_lbl 41500 `"Salinas, CA"', add
label define met2013_lbl 41540 `"Salisbury, MD-DE"', add
label define met2013_lbl 41620 `"Salt Lake City, UT"', add
label define met2013_lbl 41660 `"San Angelo, TX"', add
label define met2013_lbl 41700 `"San Antonio-New Braunfels, TX"', add
label define met2013_lbl 41740 `"San Diego-Carlsbad, CA"', add
label define met2013_lbl 41860 `"San Francisco-Oakland-Hayward, CA"', add
label define met2013_lbl 41900 `"San Germán, PR"', add
label define met2013_lbl 41940 `"San Jose-Sunnyvale-Santa Clara, CA"', add
label define met2013_lbl 41980 `"San Juan-Carolina-Caguas, PR"', add
label define met2013_lbl 42020 `"San Luis Obispo-Paso Robles-Arroyo Grande, CA"', add
label define met2013_lbl 42100 `"Santa Cruz-Watsonville, CA"', add
label define met2013_lbl 42140 `"Santa Fe, NM"', add
label define met2013_lbl 42200 `"Santa Maria-Santa Barbara, CA"', add
label define met2013_lbl 42220 `"Santa Rosa, CA"', add
label define met2013_lbl 42540 `"Scranton--Wilkes-Barre--Hazleton, PA"', add
label define met2013_lbl 42660 `"Seattle-Tacoma-Bellevue, WA"', add
label define met2013_lbl 42680 `"Sebastian-Vero Beach, FL"', add
label define met2013_lbl 43100 `"Sheboygan, WI"', add
label define met2013_lbl 43340 `"Shreveport-Bossier City, LA"', add
label define met2013_lbl 43900 `"Spartanburg, SC"', add
label define met2013_lbl 44060 `"Spokane-Spokane Valley, WA"', add
label define met2013_lbl 44100 `"Springfield, IL"', add
label define met2013_lbl 44140 `"Springfield, MA"', add
label define met2013_lbl 44180 `"Springfield, MO"', add
label define met2013_lbl 44220 `"Springfield, OH"', add
label define met2013_lbl 44300 `"State College, PA"', add
label define met2013_lbl 44700 `"Stockton-Lodi, CA"', add
label define met2013_lbl 44940 `"Sumter, SC"', add
label define met2013_lbl 45060 `"Syracuse, NY"', add
label define met2013_lbl 45220 `"Tallahassee, FL"', add
label define met2013_lbl 45300 `"Tampa-St. Petersburg-Clearwater, FL"', add
label define met2013_lbl 45460 `"Terre Haute, IN"', add
label define met2013_lbl 45540 `"The Villages, FL"', add
label define met2013_lbl 45780 `"Toledo, OH"', add
label define met2013_lbl 45820 `"Topeka, KS"', add
label define met2013_lbl 45940 `"Trenton, NJ"', add
label define met2013_lbl 46060 `"Tucson, AZ"', add
label define met2013_lbl 46140 `"Tulsa, OK"', add
label define met2013_lbl 46220 `"Tuscaloosa, AL"', add
label define met2013_lbl 46340 `"Tyler, TX"', add
label define met2013_lbl 46520 `"Urban Honolulu, HI"', add
label define met2013_lbl 46540 `"Utica-Rome, NY"', add
label define met2013_lbl 46660 `"Valdosta, GA"', add
label define met2013_lbl 46700 `"Vallejo-Fairfield, CA"', add
label define met2013_lbl 47220 `"Vineland-Bridgeton, NJ"', add
label define met2013_lbl 47260 `"Virginia Beach-Norfolk-Newport News, VA-NC"', add
label define met2013_lbl 47300 `"Visalia-Porterville, CA"', add
label define met2013_lbl 47380 `"Waco, TX"', add
label define met2013_lbl 47580 `"Warner Robins, GA"', add
label define met2013_lbl 47900 `"Washington-Arlington-Alexandria, DC-VA-MD-WV"', add
label define met2013_lbl 48140 `"Wausau, WI"', add
label define met2013_lbl 48300 `"Wenatchee, WA"', add
label define met2013_lbl 48620 `"Wichita, KS"', add
label define met2013_lbl 48660 `"Wichita Falls, TX"', add
label define met2013_lbl 48700 `"Williamsport, PA"', add
label define met2013_lbl 48900 `"Wilmington, NC"', add
label define met2013_lbl 49180 `"Winston-Salem, NC"', add
label define met2013_lbl 49340 `"Worcester, MA-CT"', add
label define met2013_lbl 49420 `"Yakima, WA"', add
label define met2013_lbl 49620 `"York-Hanover, PA"', add
label define met2013_lbl 49660 `"Youngstown-Warren-Boardman, OH-PA"', add
label define met2013_lbl 49700 `"Yuba City, CA"', add
label define met2013_lbl 49740 `"Yuma, AZ"', add
label values met2013 met2013_lbl

label define city_lbl 0000 `"Not in identifiable city (or size group)"'
label define city_lbl 0001 `"Aberdeen, SD"', add
label define city_lbl 0002 `"Aberdeen, WA"', add
label define city_lbl 0003 `"Abilene, TX"', add
label define city_lbl 0004 `"Ada, OK"', add
label define city_lbl 0005 `"Adams, MA"', add
label define city_lbl 0006 `"Adrian, MI"', add
label define city_lbl 0007 `"Abington, PA"', add
label define city_lbl 0010 `"Akron, OH"', add
label define city_lbl 0030 `"Alameda, CA"', add
label define city_lbl 0050 `"Albany, NY"', add
label define city_lbl 0051 `"Albany, GA"', add
label define city_lbl 0052 `"Albert Lea, MN"', add
label define city_lbl 0070 `"Albuquerque, NM"', add
label define city_lbl 0090 `"Alexandria, VA"', add
label define city_lbl 0091 `"Alexandria, LA"', add
label define city_lbl 0100 `"Alhambra, CA"', add
label define city_lbl 0110 `"Allegheny, PA"', add
label define city_lbl 0120 `"Aliquippa, PA"', add
label define city_lbl 0130 `"Allentown, PA"', add
label define city_lbl 0131 `"Alliance, OH"', add
label define city_lbl 0132 `"Alpena, MI"', add
label define city_lbl 0140 `"Alton, IL"', add
label define city_lbl 0150 `"Altoona, PA"', add
label define city_lbl 0160 `"Amarillo, TX"', add
label define city_lbl 0161 `"Ambridge, PA"', add
label define city_lbl 0162 `"Ames, IA"', add
label define city_lbl 0163 `"Amesbury, MA"', add
label define city_lbl 0170 `"Amsterdam, NY"', add
label define city_lbl 0171 `"Anaconda, MT"', add
label define city_lbl 0190 `"Anaheim, CA"', add
label define city_lbl 0210 `"Anchorage, AK"', add
label define city_lbl 0230 `"Anderson, IN"', add
label define city_lbl 0231 `"Anderson, SC"', add
label define city_lbl 0250 `"Andover, MA"', add
label define city_lbl 0270 `"Ann Arbor, MI"', add
label define city_lbl 0271 `"Annapolis, MD"', add
label define city_lbl 0272 `"Anniston, AL"', add
label define city_lbl 0273 `"Ansonia, CT"', add
label define city_lbl 0275 `"Antioch, CA"', add
label define city_lbl 0280 `"Appleton, WI"', add
label define city_lbl 0281 `"Ardmore, OK"', add
label define city_lbl 0282 `"Argenta, AR"', add
label define city_lbl 0283 `"Arkansas, KS"', add
label define city_lbl 0284 `"Arden-Arcade, CA"', add
label define city_lbl 0290 `"Arlington, TX"', add
label define city_lbl 0310 `"Arlington, VA"', add
label define city_lbl 0311 `"Arlington, MA"', add
label define city_lbl 0312 `"Arnold, PA"', add
label define city_lbl 0313 `"Asbury Park, NJ"', add
label define city_lbl 0330 `"Asheville, NC"', add
label define city_lbl 0331 `"Ashland, OH"', add
label define city_lbl 0340 `"Ashland, KY"', add
label define city_lbl 0341 `"Ashland, WI"', add
label define city_lbl 0342 `"Ashtabula, OH"', add
label define city_lbl 0343 `"Astoria, OR"', add
label define city_lbl 0344 `"Atchison, KS"', add
label define city_lbl 0345 `"Athens, GA"', add
label define city_lbl 0346 `"Athol, MA"', add
label define city_lbl 0347 `"Athens-Clarke County, GA"', add
label define city_lbl 0350 `"Atlanta, GA"', add
label define city_lbl 0370 `"Atlantic City, NJ"', add
label define city_lbl 0371 `"Attleboro, MA"', add
label define city_lbl 0390 `"Auburn, NY"', add
label define city_lbl 0391 `"Auburn, ME"', add
label define city_lbl 0410 `"Augusta, GA"', add
label define city_lbl 0411 `"Augusta-Richmond County, GA"', add
label define city_lbl 0430 `"Augusta, ME"', add
label define city_lbl 0450 `"Aurora, CO"', add
label define city_lbl 0470 `"Aurora, IL"', add
label define city_lbl 0490 `"Austin, TX"', add
label define city_lbl 0491 `"Austin, MN"', add
label define city_lbl 0510 `"Bakersfield, CA"', add
label define city_lbl 0530 `"Baltimore, MD"', add
label define city_lbl 0550 `"Bangor, ME"', add
label define city_lbl 0551 `"Barberton, OH"', add
label define city_lbl 0552 `"Barre, VT"', add
label define city_lbl 0553 `"Bartlesville, OK"', add
label define city_lbl 0554 `"Batavia, NY"', add
label define city_lbl 0570 `"Bath, ME"', add
label define city_lbl 0590 `"Baton Rouge, LA"', add
label define city_lbl 0610 `"Battle Creek, MI"', add
label define city_lbl 0630 `"Bay City, MI"', add
label define city_lbl 0640 `"Bayamon, PR"', add
label define city_lbl 0650 `"Bayonne, NJ"', add
label define city_lbl 0651 `"Beacon, NY"', add
label define city_lbl 0652 `"Beatrice, NE"', add
label define city_lbl 0660 `"Belleville, IL"', add
label define city_lbl 0670 `"Beaumont, TX"', add
label define city_lbl 0671 `"Beaver Falls, PA"', add
label define city_lbl 0672 `"Bedford, IN"', add
label define city_lbl 0673 `"Bellaire, OH"', add
label define city_lbl 0680 `"Bellevue, WA"', add
label define city_lbl 0690 `"Bellingham, WA"', add
label define city_lbl 0695 `"Belvedere, CA"', add
label define city_lbl 0700 `"Belleville, NJ"', add
label define city_lbl 0701 `"Bellevue, PA"', add
label define city_lbl 0702 `"Belmont, OH"', add
label define city_lbl 0703 `"Belmont, MA"', add
label define city_lbl 0704 `"Beloit, WI"', add
label define city_lbl 0705 `"Bennington, VT"', add
label define city_lbl 0706 `"Benton Harbor, MI"', add
label define city_lbl 0710 `"Berkeley, CA"', add
label define city_lbl 0711 `"Berlin, NH"', add
label define city_lbl 0712 `"Berwick, PA"', add
label define city_lbl 0720 `"Berwyn, IL"', add
label define city_lbl 0721 `"Bessemer, AL"', add
label define city_lbl 0730 `"Bethlehem, PA"', add
label define city_lbl 0740 `"Biddeford, ME"', add
label define city_lbl 0741 `"Big Spring, TX"', add
label define city_lbl 0742 `"Billings, MT"', add
label define city_lbl 0743 `"Biloxi, MS"', add
label define city_lbl 0750 `"Binghamton, NY"', add
label define city_lbl 0760 `"Beverly, MA"', add
label define city_lbl 0761 `"Beverly Hills, CA"', add
label define city_lbl 0770 `"Birmingham, AL"', add
label define city_lbl 0771 `"Birmingham, CT"', add
label define city_lbl 0772 `"Bismarck, ND"', add
label define city_lbl 0780 `"Bloomfield, NJ"', add
label define city_lbl 0790 `"Bloomington, IL"', add
label define city_lbl 0791 `"Bloomington, IN"', add
label define city_lbl 0792 `"Blue Island, IL"', add
label define city_lbl 0793 `"Bluefield, WV"', add
label define city_lbl 0794 `"Blytheville, AR"', add
label define city_lbl 0795 `"Bogalusa, LA"', add
label define city_lbl 0800 `"Boise, ID"', add
label define city_lbl 0801 `"Boone, IA"', add
label define city_lbl 0810 `"Boston, MA"', add
label define city_lbl 0811 `"Boulder, CO"', add
label define city_lbl 0812 `"Bowling Green, KY"', add
label define city_lbl 0813 `"Braddock, PA"', add
label define city_lbl 0814 `"Braden, WA"', add
label define city_lbl 0815 `"Bradford, PA"', add
label define city_lbl 0816 `"Brainerd, MN"', add
label define city_lbl 0817 `"Braintree, MA"', add
label define city_lbl 0818 `"Brawley, CA"', add
label define city_lbl 0819 `"Bremerton, WA"', add
label define city_lbl 0830 `"Bridgeport, CT"', add
label define city_lbl 0831 `"Bridgeton, NJ"', add
label define city_lbl 0832 `"Bristol, CT"', add
label define city_lbl 0833 `"Bristol, PA"', add
label define city_lbl 0834 `"Bristol, VA"', add
label define city_lbl 0835 `"Bristol, TN"', add
label define city_lbl 0837 `"Bristol, RI"', add
label define city_lbl 0850 `"Brockton, MA"', add
label define city_lbl 0851 `"Brookfield, IL"', add
label define city_lbl 0870 `"Brookline, MA"', add
label define city_lbl 0880 `"Brownsville, TX"', add
label define city_lbl 0881 `"Brownwood, TX"', add
label define city_lbl 0882 `"Brunswick, GA"', add
label define city_lbl 0883 `"Bucyrus, OH"', add
label define city_lbl 0890 `"Buffalo, NY"', add
label define city_lbl 0900 `"Burlington, IA"', add
label define city_lbl 0905 `"Burlington, VT"', add
label define city_lbl 0906 `"Burlington, NJ"', add
label define city_lbl 0907 `"Bushkill, PA"', add
label define city_lbl 0910 `"Butte, MT"', add
label define city_lbl 0911 `"Butler, PA"', add
label define city_lbl 0920 `"Burbank, CA"', add
label define city_lbl 0921 `"Burlingame, CA"', add
label define city_lbl 0926 `"Cairo, IL"', add
label define city_lbl 0927 `"Calumet City, IL"', add
label define city_lbl 0930 `"Cambridge, MA"', add
label define city_lbl 0931 `"Cambridge, OH"', add
label define city_lbl 0950 `"Camden, NJ"', add
label define city_lbl 0951 `"Campbell, OH"', add
label define city_lbl 0952 `"Canonsburg, PA"', add
label define city_lbl 0970 `"Camden, NY"', add
label define city_lbl 0990 `"Canton, OH"', add
label define city_lbl 0991 `"Canton, IL"', add
label define city_lbl 0992 `"Cape Girardeau, MO"', add
label define city_lbl 0993 `"Carbondale, PA"', add
label define city_lbl 0994 `"Carlisle, PA"', add
label define city_lbl 0995 `"Carnegie, PA"', add
label define city_lbl 0996 `"Carrick, PA"', add
label define city_lbl 0997 `"Carteret, NJ"', add
label define city_lbl 0998 `"Carthage, MO"', add
label define city_lbl 0999 `"Casper, WY"', add
label define city_lbl 1000 `"Cape Coral, FL"', add
label define city_lbl 1010 `"Cedar Rapids, IA"', add
label define city_lbl 1020 `"Central Falls, RI"', add
label define city_lbl 1021 `"Centralia, IL"', add
label define city_lbl 1023 `"Chambersburg, PA"', add
label define city_lbl 1024 `"Champaign, IL"', add
label define city_lbl 1025 `"Chanute, KS"', add
label define city_lbl 1026 `"Charleroi, PA"', add
label define city_lbl 1027 `"Chandler, AZ"', add
label define city_lbl 1030 `"Charlestown, MA"', add
label define city_lbl 1050 `"Charleston, SC"', add
label define city_lbl 1060 `"Carolina, PR"', add
label define city_lbl 1070 `"Charleston, WV"', add
label define city_lbl 1090 `"Charlotte, NC"', add
label define city_lbl 1091 `"Charlottesville, VA"', add
label define city_lbl 1110 `"Chattanooga, TN"', add
label define city_lbl 1130 `"Chelsea, MA"', add
label define city_lbl 1140 `"Cheltenham, PA"', add
label define city_lbl 1150 `"Chesapeake, VA"', add
label define city_lbl 1170 `"Chester, PA"', add
label define city_lbl 1171 `"Cheyenne, WY"', add
label define city_lbl 1190 `"Chicago, IL"', add
label define city_lbl 1191 `"Chicago Heights, IL"', add
label define city_lbl 1192 `"Chickasha, OK"', add
label define city_lbl 1210 `"Chicopee, MA"', add
label define city_lbl 1230 `"Chillicothe, OH"', add
label define city_lbl 1250 `"Chula Vista, CA"', add
label define city_lbl 1270 `"Cicero, IL"', add
label define city_lbl 1290 `"Cincinnati, OH"', add
label define city_lbl 1291 `"Clairton, PA"', add
label define city_lbl 1292 `"Claremont, NH"', add
label define city_lbl 1310 `"Clarksburg, WV"', add
label define city_lbl 1311 `"Clarksdale, MS"', add
label define city_lbl 1312 `"Cleburne, TX"', add
label define city_lbl 1330 `"Cleveland, OH"', add
label define city_lbl 1340 `"Cleveland Heights, OH"', add
label define city_lbl 1341 `"Cliffside Park, NJ"', add
label define city_lbl 1350 `"Clifton, NJ"', add
label define city_lbl 1351 `"Clinton, IN"', add
label define city_lbl 1370 `"Clinton, IA"', add
label define city_lbl 1371 `"Clinton, MA"', add
label define city_lbl 1372 `"Coatesville, PA"', add
label define city_lbl 1373 `"Coffeyville, KS"', add
label define city_lbl 1374 `"Cohoes, NY"', add
label define city_lbl 1375 `"Collingswood, NJ"', add
label define city_lbl 1390 `"Colorado Springs, CO"', add
label define city_lbl 1410 `"Columbia, SC"', add
label define city_lbl 1411 `"Columbia, PA"', add
label define city_lbl 1412 `"Columbia, MO"', add
label define city_lbl 1414 `"Columbia CDP, MD"', add
label define city_lbl 1420 `"Columbia City, IN"', add
label define city_lbl 1430 `"Columbus, GA"', add
label define city_lbl 1450 `"Columbus, OH"', add
label define city_lbl 1451 `"Columbus, MS"', add
label define city_lbl 1452 `"Compton, CA"', add
label define city_lbl 1470 `"Concord, CA"', add
label define city_lbl 1490 `"Concord, NH"', add
label define city_lbl 1491 `"Concord, NC"', add
label define city_lbl 1492 `"Connellsville, PA"', add
label define city_lbl 1493 `"Connersville, IN"', add
label define city_lbl 1494 `"Conshohocken, PA"', add
label define city_lbl 1495 `"Coraopolis, PA"', add
label define city_lbl 1496 `"Corning, NY"', add
label define city_lbl 1500 `"Corona, CA"', add
label define city_lbl 1510 `"Council Bluffs, IA"', add
label define city_lbl 1520 `"Corpus Christi, TX"', add
label define city_lbl 1521 `"Corsicana, TX"', add
label define city_lbl 1522 `"Cortland, NY"', add
label define city_lbl 1523 `"Coshocton, OH"', add
label define city_lbl 1530 `"Covington, KY"', add
label define city_lbl 1540 `"Costa Mesa, CA"', add
label define city_lbl 1545 `"Cranford, NJ"', add
label define city_lbl 1550 `"Cranston, RI"', add
label define city_lbl 1551 `"Crawfordsville, IN"', add
label define city_lbl 1552 `"Cripple Creek, CO"', add
label define city_lbl 1553 `"Cudahy, WI"', add
label define city_lbl 1570 `"Cumberland, MD"', add
label define city_lbl 1571 `"Cumberland, RI"', add
label define city_lbl 1572 `"Cuyahoga Falls, OH"', add
label define city_lbl 1590 `"Dallas, TX"', add
label define city_lbl 1591 `"Danbury, CT"', add
label define city_lbl 1592 `"Daly City, CA"', add
label define city_lbl 1610 `"Danvers, MA"', add
label define city_lbl 1630 `"Danville, IL"', add
label define city_lbl 1631 `"Danville, VA"', add
label define city_lbl 1650 `"Davenport, IA"', add
label define city_lbl 1670 `"Dayton, OH"', add
label define city_lbl 1671 `"Daytona Beach, FL"', add
label define city_lbl 1680 `"Dearborn, MI"', add
label define city_lbl 1690 `"Decatur, IL"', add
label define city_lbl 1691 `"Decatur, AL"', add
label define city_lbl 1692 `"Decatur, GA"', add
label define city_lbl 1693 `"Dedham, MA"', add
label define city_lbl 1694 `"Del Rio, TX"', add
label define city_lbl 1695 `"Denison, TX"', add
label define city_lbl 1710 `"Denver, CO"', add
label define city_lbl 1711 `"Derby, CT"', add
label define city_lbl 1713 `"Derry, PA"', add
label define city_lbl 1730 `"Des Moines, IA"', add
label define city_lbl 1750 `"Detroit, MI"', add
label define city_lbl 1751 `"Dickson City, PA"', add
label define city_lbl 1752 `"Dodge, KS"', add
label define city_lbl 1753 `"Donora, PA"', add
label define city_lbl 1754 `"Dormont, PA"', add
label define city_lbl 1755 `"Dothan, AL"', add
label define city_lbl 1770 `"Dorchester, MA"', add
label define city_lbl 1790 `"Dover, NH"', add
label define city_lbl 1791 `"Dover, NJ"', add
label define city_lbl 1792 `"Du Bois, PA"', add
label define city_lbl 1800 `"Downey, CA"', add
label define city_lbl 1810 `"Dubuque, IA"', add
label define city_lbl 1830 `"Duluth, MN"', add
label define city_lbl 1831 `"Dunkirk, NY"', add
label define city_lbl 1832 `"Dunmore, PA"', add
label define city_lbl 1833 `"Duquesne, PA"', add
label define city_lbl 1834 `"Dundalk, MD"', add
label define city_lbl 1850 `"Durham, NC"', add
label define city_lbl 1860 `"1860"', add
label define city_lbl 1870 `"East Chicago, IN"', add
label define city_lbl 1890 `"East Cleveland, OH"', add
label define city_lbl 1891 `"East Hartford, CT"', add
label define city_lbl 1892 `"East Liverpool, OH"', add
label define city_lbl 1893 `"East Moline, IL"', add
label define city_lbl 1910 `"East Los Angeles, CA"', add
label define city_lbl 1930 `"East Orange, NJ"', add
label define city_lbl 1931 `"East Providence, RI"', add
label define city_lbl 1940 `"East Saginaw, MI"', add
label define city_lbl 1950 `"East St. Louis, IL"', add
label define city_lbl 1951 `"East Youngstown, OH"', add
label define city_lbl 1952 `"Easthampton, MA"', add
label define city_lbl 1970 `"Easton, PA"', add
label define city_lbl 1971 `"Eau Claire, WI"', add
label define city_lbl 1972 `"Ecorse, MI"', add
label define city_lbl 1973 `"El Dorado, KS"', add
label define city_lbl 1974 `"El Dorado, AR"', add
label define city_lbl 1990 `"El Monte, CA"', add
label define city_lbl 2010 `"El Paso, TX"', add
label define city_lbl 2030 `"Elgin, IL"', add
label define city_lbl 2040 `"Elyria, OH"', add
label define city_lbl 2050 `"Elizabeth, NJ"', add
label define city_lbl 2051 `"Elizabeth City, NC"', add
label define city_lbl 2055 `"Elk Grove, CA"', add
label define city_lbl 2060 `"Elkhart, IN"', add
label define city_lbl 2061 `"Ellwood City, PA"', add
label define city_lbl 2062 `"Elmhurst, IL"', add
label define city_lbl 2070 `"Elmira, NY"', add
label define city_lbl 2071 `"Elmwood Park, IL"', add
label define city_lbl 2072 `"Elwood, IN"', add
label define city_lbl 2073 `"Emporia, KS"', add
label define city_lbl 2074 `"Endicott, NY"', add
label define city_lbl 2075 `"Enfield, CT"', add
label define city_lbl 2076 `"Englewood, NJ"', add
label define city_lbl 2080 `"Enid, OK"', add
label define city_lbl 2090 `"Erie, PA"', add
label define city_lbl 2091 `"Escanaba, MI"', add
label define city_lbl 2092 `"Euclid, OH"', add
label define city_lbl 2110 `"Escondido, CA"', add
label define city_lbl 2130 `"Eugene, OR"', add
label define city_lbl 2131 `"Eureka, CA"', add
label define city_lbl 2150 `"Evanston, IL"', add
label define city_lbl 2170 `"Evansville, IN"', add
label define city_lbl 2190 `"Everett, MA"', add
label define city_lbl 2210 `"Everett, WA"', add
label define city_lbl 2211 `"Fairfield, AL"', add
label define city_lbl 2212 `"Fairfield, CT"', add
label define city_lbl 2213 `"Fairhaven, MA"', add
label define city_lbl 2214 `"Fairmont, WV"', add
label define city_lbl 2220 `"Fargo, ND"', add
label define city_lbl 2221 `"Faribault, MN"', add
label define city_lbl 2222 `"Farrell, PA"', add
label define city_lbl 2230 `"Fall River, MA"', add
label define city_lbl 2240 `"Fayetteville, NC"', add
label define city_lbl 2241 `"Ferndale, MI"', add
label define city_lbl 2242 `"Findlay, OH"', add
label define city_lbl 2250 `"Fitchburg, MA"', add
label define city_lbl 2260 `"Fontana, CA"', add
label define city_lbl 2270 `"Flint, MI"', add
label define city_lbl 2271 `"Floral Park, NY"', add
label define city_lbl 2273 `"Florence, AL"', add
label define city_lbl 2274 `"Florence, SC"', add
label define city_lbl 2275 `"Flushing, NY"', add
label define city_lbl 2280 `"Fond du Lac, WI"', add
label define city_lbl 2281 `"Forest Park, IL"', add
label define city_lbl 2290 `"Fort Lauderdale, FL"', add
label define city_lbl 2300 `"Fort Collins, CO"', add
label define city_lbl 2301 `"Fort Dodge, IA"', add
label define city_lbl 2302 `"Fort Madison, IA"', add
label define city_lbl 2303 `"Fort Scott, KS"', add
label define city_lbl 2310 `"Fort Smith, AR"', add
label define city_lbl 2311 `"Fort Thomas, KY"', add
label define city_lbl 2330 `"Fort Wayne, IN"', add
label define city_lbl 2350 `"Fort Worth, TX"', add
label define city_lbl 2351 `"Fostoria, OH"', add
label define city_lbl 2352 `"Framingham, MA"', add
label define city_lbl 2353 `"Frankfort, IN"', add
label define city_lbl 2354 `"Frankfort, KY"', add
label define city_lbl 2355 `"Franklin, PA"', add
label define city_lbl 2356 `"Frederick, MD"', add
label define city_lbl 2357 `"Freeport, NY"', add
label define city_lbl 2358 `"Freeport, IL"', add
label define city_lbl 2359 `"Fremont, OH"', add
label define city_lbl 2360 `"Fremont, NE"', add
label define city_lbl 2370 `"Fresno, CA"', add
label define city_lbl 2390 `"Fullerton, CA"', add
label define city_lbl 2391 `"Fulton, NY"', add
label define city_lbl 2392 `"Gadsden, AL"', add
label define city_lbl 2393 `"Galena, KS"', add
label define city_lbl 2394 `"Gainesville, FL"', add
label define city_lbl 2400 `"Galesburg, IL"', add
label define city_lbl 2410 `"Galveston, TX"', add
label define city_lbl 2411 `"Gardner, MA"', add
label define city_lbl 2430 `"Garden Grove, CA"', add
label define city_lbl 2435 `"Gardena, CA"', add
label define city_lbl 2440 `"Garfield, NJ"', add
label define city_lbl 2441 `"Garfield Heights, OH"', add
label define city_lbl 2450 `"Garland, TX"', add
label define city_lbl 2470 `"Gary, IN"', add
label define city_lbl 2471 `"Gastonia, NC"', add
label define city_lbl 2472 `"Geneva, NY"', add
label define city_lbl 2473 `"Glen Cove, NY"', add
label define city_lbl 2489 `"Glendale, AZ"', add
label define city_lbl 2490 `"Glendale, CA"', add
label define city_lbl 2491 `"Glens Falls, NY"', add
label define city_lbl 2510 `"Gloucester, MA"', add
label define city_lbl 2511 `"Gloucester, NJ"', add
label define city_lbl 2512 `"Gloversville, NY"', add
label define city_lbl 2513 `"Goldsboro, NC"', add
label define city_lbl 2514 `"Goshen, IN"', add
label define city_lbl 2515 `"Grand Forks, ND"', add
label define city_lbl 2516 `"Grand Island, NE"', add
label define city_lbl 2517 `"Grand Junction, CO"', add
label define city_lbl 2520 `"Granite City, IL"', add
label define city_lbl 2530 `"Grand Rapids, MI"', add
label define city_lbl 2531 `"Grandville, MI"', add
label define city_lbl 2540 `"Great Falls, MT"', add
label define city_lbl 2541 `"Greeley, CO"', add
label define city_lbl 2550 `"Green Bay, WI"', add
label define city_lbl 2551 `"Greenfield, MA"', add
label define city_lbl 2570 `"Greensboro, NC"', add
label define city_lbl 2571 `"Greensburg, PA"', add
label define city_lbl 2572 `"Greenville, MS"', add
label define city_lbl 2573 `"Greenville, SC"', add
label define city_lbl 2574 `"Greenville, TX"', add
label define city_lbl 2575 `"Greenwich, CT"', add
label define city_lbl 2576 `"Greenwood, MS"', add
label define city_lbl 2577 `"Greenwood, SC"', add
label define city_lbl 2578 `"Griffin, GA"', add
label define city_lbl 2579 `"Grosse Pointe Park, MI"', add
label define city_lbl 2580 `"Guynabo, PR"', add
label define city_lbl 2581 `"Groton, CT"', add
label define city_lbl 2582 `"Gulfport, MS"', add
label define city_lbl 2583 `"Guthrie, OK"', add
label define city_lbl 2584 `"Hackensack, NJ"', add
label define city_lbl 2590 `"Hagerstown, MD"', add
label define city_lbl 2591 `"Hamden, CT"', add
label define city_lbl 2610 `"Hamilton, OH"', add
label define city_lbl 2630 `"Hammond, IN"', add
label define city_lbl 2650 `"Hampton, VA"', add
label define city_lbl 2670 `"Hamtramck Village, MI"', add
label define city_lbl 2680 `"Hannibal, MO"', add
label define city_lbl 2681 `"Hanover, PA"', add
label define city_lbl 2682 `"Harlingen, TX"', add
label define city_lbl 2683 `"Hanover township, Luzerne county, PA"', add
label define city_lbl 2690 `"Harrisburg, PA"', add
label define city_lbl 2691 `"Harrisburg, IL"', add
label define city_lbl 2692 `"Harrison, NJ"', add
label define city_lbl 2693 `"Harrison, PA"', add
label define city_lbl 2710 `"Hartford, CT"', add
label define city_lbl 2711 `"Harvey, IL"', add
label define city_lbl 2712 `"Hastings, NE"', add
label define city_lbl 2713 `"Hattiesburg, MS"', add
label define city_lbl 2725 `"Haverford, PA"', add
label define city_lbl 2730 `"Haverhill, MA"', add
label define city_lbl 2731 `"Hawthorne, NJ"', add
label define city_lbl 2740 `"Hayward, CA"', add
label define city_lbl 2750 `"Hazleton, PA"', add
label define city_lbl 2751 `"Helena, MT"', add
label define city_lbl 2752 `"Hempstead, NY"', add
label define city_lbl 2753 `"Henderson, KY"', add
label define city_lbl 2754 `"Herkimer, NY"', add
label define city_lbl 2755 `"Herrin, IL"', add
label define city_lbl 2756 `"Hibbing, MN"', add
label define city_lbl 2757 `"Henderson, NV"', add
label define city_lbl 2770 `"Hialeah, FL"', add
label define city_lbl 2780 `"High Point, NC"', add
label define city_lbl 2781 `"Highland Park, IL"', add
label define city_lbl 2790 `"Highland Park, MI"', add
label define city_lbl 2791 `"Hilo, HI"', add
label define city_lbl 2792 `"Hillside, NJ"', add
label define city_lbl 2810 `"Hoboken, NJ"', add
label define city_lbl 2811 `"Holland, MI"', add
label define city_lbl 2830 `"Hollywood, FL"', add
label define city_lbl 2850 `"Holyoke, MA"', add
label define city_lbl 2851 `"Homestead, PA"', add
label define city_lbl 2870 `"Honolulu, HI"', add
label define city_lbl 2871 `"Hopewell, VA"', add
label define city_lbl 2872 `"Hopkinsville, KY"', add
label define city_lbl 2873 `"Hoquiam, WA"', add
label define city_lbl 2874 `"Hornell, NY"', add
label define city_lbl 2875 `"Hot Springs, AR"', add
label define city_lbl 2890 `"Houston, TX"', add
label define city_lbl 2891 `"Hudson, NY"', add
label define city_lbl 2892 `"Huntington, IN"', add
label define city_lbl 2910 `"Huntington, WV"', add
label define city_lbl 2930 `"Huntington Beach, CA"', add
label define city_lbl 2950 `"Huntsville, AL"', add
label define city_lbl 2951 `"Huron, SD"', add
label define city_lbl 2960 `"Hutchinson, KS"', add
label define city_lbl 2961 `"Hyde Park, MA"', add
label define city_lbl 2962 `"Ilion, NY"', add
label define city_lbl 2963 `"Independence, KS"', add
label define city_lbl 2970 `"Independence, MO"', add
label define city_lbl 2990 `"Indianapolis, IN"', add
label define city_lbl 3010 `"Inglewood, CA"', add
label define city_lbl 3011 `"Iowa City, IA"', add
label define city_lbl 3012 `"Iron Mountain, MI"', add
label define city_lbl 3013 `"Ironton, OH"', add
label define city_lbl 3014 `"Ironwood, MI"', add
label define city_lbl 3015 `"Irondequoit, NY"', add
label define city_lbl 3020 `"Irvine, CA"', add
label define city_lbl 3030 `"Irving, TX"', add
label define city_lbl 3050 `"Irvington, NJ"', add
label define city_lbl 3051 `"Ishpeming, MI"', add
label define city_lbl 3052 `"Ithaca, NY"', add
label define city_lbl 3070 `"Jackson, MI"', add
label define city_lbl 3071 `"Jackson, MN"', add
label define city_lbl 3090 `"Jackson, MS"', add
label define city_lbl 3091 `"Jackson, TN"', add
label define city_lbl 3110 `"Jacksonville, FL"', add
label define city_lbl 3111 `"Jacksonville, IL"', add
label define city_lbl 3130 `"Jamestown, NY"', add
label define city_lbl 3131 `"Janesville, WI"', add
label define city_lbl 3132 `"Jeannette, PA"', add
label define city_lbl 3133 `"Jefferson City, MO"', add
label define city_lbl 3134 `"Jeffersonville, IN"', add
label define city_lbl 3150 `"Jersey City, NJ"', add
label define city_lbl 3151 `"Johnson City, NY"', add
label define city_lbl 3160 `"Johnson City, TN"', add
label define city_lbl 3161 `"Johnstown, NY"', add
label define city_lbl 3170 `"Johnstown, PA"', add
label define city_lbl 3190 `"Joliet, IL"', add
label define city_lbl 3191 `"Jonesboro, AR"', add
label define city_lbl 3210 `"Joplin, MO"', add
label define city_lbl 3230 `"Kalamazoo, MI"', add
label define city_lbl 3231 `"Kankakee, IL"', add
label define city_lbl 3250 `"Kansas City, KS"', add
label define city_lbl 3260 `"Kansas City, MO"', add
label define city_lbl 3270 `"Kearny, NJ"', add
label define city_lbl 3271 `"Keene, NH"', add
label define city_lbl 3272 `"Kenmore, NY"', add
label define city_lbl 3273 `"Kenmore, OH"', add
label define city_lbl 3290 `"Kenosha, WI"', add
label define city_lbl 3291 `"Keokuk, IA"', add
label define city_lbl 3292 `"Kewanee, IL"', add
label define city_lbl 3293 `"Key West, FL"', add
label define city_lbl 3294 `"Kingsport, TN"', add
label define city_lbl 3300 `"Kent, WA"', add
label define city_lbl 3310 `"Kingston, NY"', add
label define city_lbl 3311 `"Kingston, PA"', add
label define city_lbl 3312 `"Kinston, NC"', add
label define city_lbl 3313 `"Klamath Falls, OR"', add
label define city_lbl 3330 `"Knoxville, TN"', add
label define city_lbl 3350 `"Kokomo, IN"', add
label define city_lbl 3370 `"La Crosse, WI"', add
label define city_lbl 3380 `"Lafayette, IN"', add
label define city_lbl 3390 `"Lafayette, LA"', add
label define city_lbl 3391 `"La Grange, IL"', add
label define city_lbl 3392 `"La Grange, GA"', add
label define city_lbl 3393 `"La Porte, IN"', add
label define city_lbl 3394 `"La Salle, IL"', add
label define city_lbl 3395 `"Lackawanna, NY"', add
label define city_lbl 3396 `"Laconia, NH"', add
label define city_lbl 3397 `"Historical Lafayette, LA"', add
label define city_lbl 3400 `"Lake Charles, LA"', add
label define city_lbl 3405 `"Lakeland, FL"', add
label define city_lbl 3410 `"Lakewood, CO"', add
label define city_lbl 3430 `"Lakewood, OH"', add
label define city_lbl 3440 `"Lancaster, CA"', add
label define city_lbl 3450 `"Lancaster, PA"', add
label define city_lbl 3451 `"Lancaster, OH"', add
label define city_lbl 3470 `"Lansing, MI"', add
label define city_lbl 3471 `"Lansingburgh, NY"', add
label define city_lbl 3480 `"Laredo, TX"', add
label define city_lbl 3481 `"Latrobe, PA"', add
label define city_lbl 3482 `"Laurel, MS"', add
label define city_lbl 3490 `"Las Vegas, NV"', add
label define city_lbl 3510 `"Lawrence, MA"', add
label define city_lbl 3511 `"Lawrence, KS"', add
label define city_lbl 3512 `"Lawton, OK"', add
label define city_lbl 3513 `"Leadville, CO"', add
label define city_lbl 3520 `"Leavenworth, KS"', add
label define city_lbl 3521 `"Lebanon, PA"', add
label define city_lbl 3522 `"Leominster, MA"', add
label define city_lbl 3530 `"Lehigh, PA"', add
label define city_lbl 3550 `"Lewiston, ME"', add
label define city_lbl 3551 `"Lewistown, PA"', add
label define city_lbl 3560 `"Lewisville, TX"', add
label define city_lbl 3570 `"Lexington, KY"', add
label define city_lbl 3590 `"Lexington-Fayette, KY"', add
label define city_lbl 3610 `"Lima, OH"', add
label define city_lbl 3630 `"Lincoln, NE"', add
label define city_lbl 3631 `"Lincoln, IL"', add
label define city_lbl 3632 `"Lincoln Park, MI"', add
label define city_lbl 3633 `"Lincoln, RI"', add
label define city_lbl 3634 `"Linden, NJ"', add
label define city_lbl 3635 `"Little Falls, NY"', add
label define city_lbl 3638 `"Lodi, NJ"', add
label define city_lbl 3639 `"Logansport, IN"', add
label define city_lbl 3650 `"Little Rock, AR"', add
label define city_lbl 3670 `"Livonia, MI"', add
label define city_lbl 3680 `"Lockport, NY"', add
label define city_lbl 3690 `"Long Beach, CA"', add
label define city_lbl 3691 `"Long Branch, NJ"', add
label define city_lbl 3692 `"Long Island City, NY"', add
label define city_lbl 3693 `"Longview, WA"', add
label define city_lbl 3710 `"Lorain, OH"', add
label define city_lbl 3730 `"Los Angeles, CA"', add
label define city_lbl 3750 `"Louisville, KY"', add
label define city_lbl 3765 `"Lower Merion, PA"', add
label define city_lbl 3770 `"Lowell, MA"', add
label define city_lbl 3771 `"Lubbock, TX"', add
label define city_lbl 3772 `"Lynbrook, NY"', add
label define city_lbl 3790 `"Lynchburg, VA"', add
label define city_lbl 3800 `"Lyndhurst, NJ"', add
label define city_lbl 3810 `"Lynn, MA"', add
label define city_lbl 3830 `"Macon, GA"', add
label define city_lbl 3850 `"Madison, IN"', add
label define city_lbl 3870 `"Madison, WI"', add
label define city_lbl 3871 `"Mahanoy City, PA"', add
label define city_lbl 3890 `"Malden, MA"', add
label define city_lbl 3891 `"Mamaroneck, NY"', add
label define city_lbl 3910 `"Manchester, NH"', add
label define city_lbl 3911 `"Manchester, CT"', add
label define city_lbl 3912 `"Manhattan, KS"', add
label define city_lbl 3913 `"Manistee, MI"', add
label define city_lbl 3914 `"Manitowoc, WI"', add
label define city_lbl 3915 `"Mankato, MN"', add
label define city_lbl 3929 `"Maplewood, NJ"', add
label define city_lbl 3930 `"Mansfield, OH"', add
label define city_lbl 3931 `"Maplewood, MO"', add
label define city_lbl 3932 `"Marietta, OH"', add
label define city_lbl 3933 `"Marinette, WI"', add
label define city_lbl 3934 `"Marion, IN"', add
label define city_lbl 3940 `"Maywood, IL"', add
label define city_lbl 3950 `"Marion, OH"', add
label define city_lbl 3951 `"Marlborough, MA"', add
label define city_lbl 3952 `"Marquette, MI"', add
label define city_lbl 3953 `"Marshall, TX"', add
label define city_lbl 3954 `"Marshalltown, IA"', add
label define city_lbl 3955 `"Martins Ferry, OH"', add
label define city_lbl 3956 `"Martinsburg, WV"', add
label define city_lbl 3957 `"Mason City, IA"', add
label define city_lbl 3958 `"Massena, NY"', add
label define city_lbl 3959 `"Massillon, OH"', add
label define city_lbl 3960 `"McAllen, TX"', add
label define city_lbl 3961 `"Mattoon, IL"', add
label define city_lbl 3962 `"Mcalester, OK"', add
label define city_lbl 3963 `"Mccomb, MS"', add
label define city_lbl 3964 `"Mckees Rocks, PA"', add
label define city_lbl 3970 `"McKeesport, PA"', add
label define city_lbl 3971 `"Meadville, PA"', add
label define city_lbl 3990 `"Medford, MA"', add
label define city_lbl 3991 `"Medford, OR"', add
label define city_lbl 3992 `"Melrose, MA"', add
label define city_lbl 3993 `"Melrose Park, IL"', add
label define city_lbl 4010 `"Memphis, TN"', add
label define city_lbl 4011 `"Menominee, MI"', add
label define city_lbl 4030 `"Meriden, CT"', add
label define city_lbl 4040 `"Meridian, MS"', add
label define city_lbl 4041 `"Methuen, MA"', add
label define city_lbl 4050 `"Mesa, AZ"', add
label define city_lbl 4070 `"Mesquite, TX"', add
label define city_lbl 4090 `"Metairie, LA"', add
label define city_lbl 4110 `"Miami, FL"', add
label define city_lbl 4120 `"Michigan City, IN"', add
label define city_lbl 4121 `"Middlesboro, KY"', add
label define city_lbl 4122 `"Middletown, CT"', add
label define city_lbl 4123 `"Middletown, NY"', add
label define city_lbl 4124 `"Middletown, OH"', add
label define city_lbl 4125 `"Milford, CT"', add
label define city_lbl 4126 `"Milford, MA"', add
label define city_lbl 4127 `"Millville, NJ"', add
label define city_lbl 4128 `"Milton, MA"', add
label define city_lbl 4130 `"Milwaukee, WI"', add
label define city_lbl 4150 `"Minneapolis, MN"', add
label define city_lbl 4151 `"Minot, ND"', add
label define city_lbl 4160 `"Mishawaka, IN"', add
label define city_lbl 4161 `"Missoula, MT"', add
label define city_lbl 4162 `"Mitchell, SD"', add
label define city_lbl 4163 `"Moberly, MO"', add
label define city_lbl 4170 `"Mobile, AL"', add
label define city_lbl 4190 `"Modesto, CA"', add
label define city_lbl 4210 `"Moline, IL"', add
label define city_lbl 4211 `"Monessen, PA"', add
label define city_lbl 4212 `"Monroe, MI"', add
label define city_lbl 4213 `"Monroe, LA"', add
label define city_lbl 4214 `"Monrovia, CA"', add
label define city_lbl 4230 `"Montclair, NJ"', add
label define city_lbl 4250 `"Montgomery, AL"', add
label define city_lbl 4251 `"Morgantown, WV"', add
label define city_lbl 4252 `"Morristown, NJ"', add
label define city_lbl 4253 `"Moundsville, WV"', add
label define city_lbl 4254 `"Mount Arlington, NJ"', add
label define city_lbl 4255 `"Mount Carmel, PA"', add
label define city_lbl 4256 `"Mount Clemens, MI"', add
label define city_lbl 4260 `"Mount Lebanon, PA"', add
label define city_lbl 4270 `"Moreno Valley, CA"', add
label define city_lbl 4290 `"Mount Vernon, NY"', add
label define city_lbl 4291 `"Mount Vernon, IL"', add
label define city_lbl 4310 `"Muncie, IN"', add
label define city_lbl 4311 `"Munhall, PA"', add
label define city_lbl 4312 `"Murphysboro, IL"', add
label define city_lbl 4313 `"Muscatine, IA"', add
label define city_lbl 4330 `"Muskegon, MI"', add
label define city_lbl 4331 `"Muskegon Heights, MI"', add
label define city_lbl 4350 `"Muskogee, OK"', add
label define city_lbl 4351 `"Nanticoke, PA"', add
label define city_lbl 4370 `"Nantucket, MA"', add
label define city_lbl 4390 `"Nashua, NH"', add
label define city_lbl 4410 `"Nashville-Davidson, TN"', add
label define city_lbl 4411 `"Nashville, TN"', add
label define city_lbl 4413 `"Natchez, MS"', add
label define city_lbl 4414 `"Natick, MA"', add
label define city_lbl 4415 `"Naugatuck, CT"', add
label define city_lbl 4416 `"Needham, MA"', add
label define city_lbl 4420 `"Neptune, NJ"', add
label define city_lbl 4430 `"New Albany, IN"', add
label define city_lbl 4450 `"New Bedford, MA"', add
label define city_lbl 4451 `"New Bern, NC"', add
label define city_lbl 4452 `"New Brighton, NY"', add
label define city_lbl 4470 `"New Britain, CT"', add
label define city_lbl 4490 `"New Brunswick, NJ"', add
label define city_lbl 4510 `"New Castle, PA"', add
label define city_lbl 4511 `"New Castle, IN"', add
label define city_lbl 4530 `"New Haven, CT"', add
label define city_lbl 4550 `"New London, CT"', add
label define city_lbl 4570 `"New Orleans, LA"', add
label define city_lbl 4571 `"New Philadelphia, OH"', add
label define city_lbl 4590 `"New Rochelle, NY"', add
label define city_lbl 4610 `"New York, NY"', add
label define city_lbl 4611 `"Brooklyn (only in census years before 1900)"', add
label define city_lbl 4612 `"Williamsburgh, NY"', add
label define city_lbl 4630 `"Newark, NJ"', add
label define city_lbl 4650 `"Newark, OH"', add
label define city_lbl 4670 `"Newburgh, NY"', add
label define city_lbl 4690 `"Newburyport, MA"', add
label define city_lbl 4710 `"Newport, KY"', add
label define city_lbl 4730 `"Newport, RI"', add
label define city_lbl 4750 `"Newport News, VA"', add
label define city_lbl 4770 `"Newton, MA"', add
label define city_lbl 4771 `"Newton, IA"', add
label define city_lbl 4772 `"Newton, KS"', add
label define city_lbl 4790 `"Niagara Falls, NY"', add
label define city_lbl 4791 `"Niles, MI"', add
label define city_lbl 4792 `"Niles, OH"', add
label define city_lbl 4810 `"Norfolk, VA"', add
label define city_lbl 4811 `"Norfolk, NE"', add
label define city_lbl 4820 `"North Las Vegas, NV"', add
label define city_lbl 4830 `"Norristown Borough, PA"', add
label define city_lbl 4831 `"North Adams, MA"', add
label define city_lbl 4832 `"North Attleborough, MA"', add
label define city_lbl 4833 `"North Bennington, VT"', add
label define city_lbl 4834 `"North Braddock, PA"', add
label define city_lbl 4835 `"North Branford, CT"', add
label define city_lbl 4836 `"North Haven, CT"', add
label define city_lbl 4837 `"North Little Rock, AR"', add
label define city_lbl 4838 `"North Platte, NE"', add
label define city_lbl 4839 `"North Providence, RI"', add
label define city_lbl 4840 `"Northampton, MA"', add
label define city_lbl 4841 `"North Tonawanda, NY"', add
label define city_lbl 4842 `"North Yakima, WA"', add
label define city_lbl 4843 `"Northbridge, MA"', add
label define city_lbl 4845 `"North Bergen, NJ"', add
label define city_lbl 4860 `"Norwalk, CA"', add
label define city_lbl 4870 `"Norwalk, CT"', add
label define city_lbl 4890 `"Norwich, CT"', add
label define city_lbl 4900 `"Norwood, OH"', add
label define city_lbl 4901 `"Norwood, MA"', add
label define city_lbl 4902 `"Nutley, NJ"', add
label define city_lbl 4905 `"Oak Park, IL"', add
label define city_lbl 4910 `"Oak Park Village, IL"', add
label define city_lbl 4930 `"Oakland, CA"', add
label define city_lbl 4950 `"Oceanside, CA"', add
label define city_lbl 4970 `"Ogden, UT"', add
label define city_lbl 4971 `"Ogdensburg, NY"', add
label define city_lbl 4972 `"Oil City, PA"', add
label define city_lbl 4990 `"Oklahoma City, OK"', add
label define city_lbl 4991 `"Okmulgee, OK"', add
label define city_lbl 4992 `"Old Bennington, VT"', add
label define city_lbl 4993 `"Old Forge, PA"', add
label define city_lbl 4994 `"Olean, NY"', add
label define city_lbl 4995 `"Olympia, WA"', add
label define city_lbl 4996 `"Olyphant, PA"', add
label define city_lbl 5010 `"Omaha, NE"', add
label define city_lbl 5011 `"Oneida, NY"', add
label define city_lbl 5012 `"Oneonta, NY"', add
label define city_lbl 5030 `"Ontario, CA"', add
label define city_lbl 5040 `"Orange, CA"', add
label define city_lbl 5050 `"Orange, NJ"', add
label define city_lbl 5051 `"Orange, CT"', add
label define city_lbl 5070 `"Orlando, FL"', add
label define city_lbl 5090 `"Oshkosh, WI"', add
label define city_lbl 5091 `"Oskaloosa, IA"', add
label define city_lbl 5092 `"Ossining, NY"', add
label define city_lbl 5110 `"Oswego, NY"', add
label define city_lbl 5111 `"Ottawa, IL"', add
label define city_lbl 5112 `"Ottumwa, IA"', add
label define city_lbl 5113 `"Owensboro, KY"', add
label define city_lbl 5114 `"Owosso, MI"', add
label define city_lbl 5116 `"Painesville, OH"', add
label define city_lbl 5117 `"Palestine, TX"', add
label define city_lbl 5118 `"Palo Alto, CA"', add
label define city_lbl 5119 `"Pampa, TX"', add
label define city_lbl 5121 `"Paris, TX"', add
label define city_lbl 5122 `"Park Ridge, IL"', add
label define city_lbl 5123 `"Parkersburg, WV"', add
label define city_lbl 5124 `"Parma, OH"', add
label define city_lbl 5125 `"Parsons, KS"', add
label define city_lbl 5130 `"Oxnard, CA"', add
label define city_lbl 5140 `"Palmdale, CA"', add
label define city_lbl 5150 `"Pasadena, CA"', add
label define city_lbl 5170 `"Pasadena, TX"', add
label define city_lbl 5180 `"Paducah, KY"', add
label define city_lbl 5190 `"Passaic, NJ"', add
label define city_lbl 5210 `"Paterson, NJ"', add
label define city_lbl 5230 `"Pawtucket, RI"', add
label define city_lbl 5231 `"Peabody, MA"', add
label define city_lbl 5232 `"Peekskill, NY"', add
label define city_lbl 5233 `"Pekin, IL"', add
label define city_lbl 5240 `"Pembroke Pines, FL"', add
label define city_lbl 5250 `"Pensacola, FL"', add
label define city_lbl 5255 `"Pensauken, NJ"', add
label define city_lbl 5269 `"Peoria, AZ"', add
label define city_lbl 5270 `"Peoria, IL"', add
label define city_lbl 5271 `"Peoria Heights, IL"', add
label define city_lbl 5290 `"Perth Amboy, NJ"', add
label define city_lbl 5291 `"Peru, IN"', add
label define city_lbl 5310 `"Petersburg, VA"', add
label define city_lbl 5311 `"Phenix City, AL"', add
label define city_lbl 5330 `"Philadelphia, PA"', add
label define city_lbl 5331 `"Kensington"', add
label define city_lbl 5332 `"Moyamensing"', add
label define city_lbl 5333 `"Northern Liberties"', add
label define city_lbl 5334 `"Southwark"', add
label define city_lbl 5335 `"Spring Garden"', add
label define city_lbl 5341 `"Phillipsburg, NJ"', add
label define city_lbl 5350 `"Phoenix, AZ"', add
label define city_lbl 5351 `"Phoenixville, PA"', add
label define city_lbl 5352 `"Pine Bluff, AR"', add
label define city_lbl 5353 `"Piqua, OH"', add
label define city_lbl 5354 `"Pittsburg, KS"', add
label define city_lbl 5370 `"Pittsburgh, PA"', add
label define city_lbl 5390 `"Pittsfield, MA"', add
label define city_lbl 5391 `"Pittston, PA"', add
label define city_lbl 5409 `"Plains, PA"', add
label define city_lbl 5410 `"Plainfield, NJ"', add
label define city_lbl 5411 `"Plattsburg, NY"', add
label define city_lbl 5412 `"Pleasantville, NJ"', add
label define city_lbl 5413 `"Plymouth, PA"', add
label define city_lbl 5414 `"Plymouth, MA"', add
label define city_lbl 5415 `"Pocatello, ID"', add
label define city_lbl 5430 `"Plano, TX"', add
label define city_lbl 5450 `"Pomona, CA"', add
label define city_lbl 5451 `"Ponca City, OK"', add
label define city_lbl 5460 `"Ponce, PR"', add
label define city_lbl 5470 `"Pontiac, MI"', add
label define city_lbl 5471 `"Port Angeles, WA"', add
label define city_lbl 5480 `"Port Arthur, TX"', add
label define city_lbl 5481 `"Port Chester, NY"', add
label define city_lbl 5490 `"Port Huron, MI"', add
label define city_lbl 5491 `"Port Jervis, NY"', add
label define city_lbl 5500 `"Port St. Lucie, FL"', add
label define city_lbl 5510 `"Portland, ME"', add
label define city_lbl 5511 `"Portland, IL"', add
label define city_lbl 5530 `"Portland, OR"', add
label define city_lbl 5550 `"Portsmouth, NH"', add
label define city_lbl 5570 `"Portsmouth, OH"', add
label define city_lbl 5590 `"Portsmouth, VA"', add
label define city_lbl 5591 `"Pottstown, PA"', add
label define city_lbl 5610 `"Pottsville, PA"', add
label define city_lbl 5630 `"Poughkeepsie, NY"', add
label define city_lbl 5650 `"Providence, RI"', add
label define city_lbl 5660 `"Provo, UT"', add
label define city_lbl 5670 `"Pueblo, CO"', add
label define city_lbl 5671 `"Punxsutawney, PA"', add
label define city_lbl 5690 `"Quincy, IL"', add
label define city_lbl 5710 `"Quincy, MA"', add
label define city_lbl 5730 `"Racine, WI"', add
label define city_lbl 5731 `"Rahway, NJ"', add
label define city_lbl 5750 `"Raleigh, NC"', add
label define city_lbl 5751 `"Ranger, TX"', add
label define city_lbl 5752 `"Rapid City, SD"', add
label define city_lbl 5770 `"Rancho Cucamonga, CA"', add
label define city_lbl 5790 `"Reading, PA"', add
label define city_lbl 5791 `"Red Bank, NJ"', add
label define city_lbl 5792 `"Redlands, CA"', add
label define city_lbl 5810 `"Reno, NV"', add
label define city_lbl 5811 `"Rensselaer, NY"', add
label define city_lbl 5830 `"Revere, MA"', add
label define city_lbl 5850 `"Richmond, IN"', add
label define city_lbl 5870 `"Richmond, VA"', add
label define city_lbl 5871 `"Richmond, CA"', add
label define city_lbl 5872 `"Ridgefield Park, NJ"', add
label define city_lbl 5873 `"Ridgewood, NJ"', add
label define city_lbl 5874 `"River Rouge, MI"', add
label define city_lbl 5890 `"Riverside, CA"', add
label define city_lbl 5910 `"Roanoke, VA"', add
label define city_lbl 5930 `"Rochester, NY"', add
label define city_lbl 5931 `"Rochester, NH"', add
label define city_lbl 5932 `"Rochester, MN"', add
label define city_lbl 5933 `"Rock Hill, SC"', add
label define city_lbl 5950 `"Rock Island, IL"', add
label define city_lbl 5970 `"Rockford, IL"', add
label define city_lbl 5971 `"Rockland, ME"', add
label define city_lbl 5972 `"Rockton, IL"', add
label define city_lbl 5973 `"Rockville Centre, NY"', add
label define city_lbl 5974 `"Rocky Mount, NC"', add
label define city_lbl 5990 `"Rome, NY"', add
label define city_lbl 5991 `"Rome, GA"', add
label define city_lbl 5992 `"Roosevelt, NJ"', add
label define city_lbl 5993 `"Roselle, NJ"', add
label define city_lbl 5994 `"Roswell, NM"', add
label define city_lbl 5995 `"Roseville, CA"', add
label define city_lbl 5996 `"Rondout, NY"', add
label define city_lbl 6010 `"Roxbury, MA"', add
label define city_lbl 6011 `"Royal Oak, MI"', add
label define city_lbl 6012 `"Rumford Falls, ME"', add
label define city_lbl 6013 `"Rutherford, NJ"', add
label define city_lbl 6014 `"Rutland, VT"', add
label define city_lbl 6030 `"Sacramento, CA"', add
label define city_lbl 6050 `"Saginaw, MI"', add
label define city_lbl 6070 `"Saint Joseph, MO"', add
label define city_lbl 6090 `"Saint Louis, MO"', add
label define city_lbl 6110 `"Saint Paul, MN"', add
label define city_lbl 6130 `"Saint Petersburg, FL"', add
label define city_lbl 6150 `"Salem, MA"', add
label define city_lbl 6170 `"Salem, OR"', add
label define city_lbl 6171 `"Salem, OH"', add
label define city_lbl 6172 `"Salina, KS"', add
label define city_lbl 6190 `"Salinas, CA"', add
label define city_lbl 6191 `"Salisbury, NC"', add
label define city_lbl 6192 `"Salisbury, MD"', add
label define city_lbl 6210 `"Salt Lake City, UT"', add
label define city_lbl 6211 `"San Angelo, TX"', add
label define city_lbl 6230 `"San Antonio, TX"', add
label define city_lbl 6231 `"San Benito, TX"', add
label define city_lbl 6250 `"San Bernardino, CA"', add
label define city_lbl 6260 `"San Buenaventura (Ventura), CA"', add
label define city_lbl 6270 `"San Diego, CA"', add
label define city_lbl 6280 `"Sandusky, OH"', add
label define city_lbl 6281 `"Sanford, FL"', add
label define city_lbl 6282 `"Sanford, ME"', add
label define city_lbl 6290 `"San Francisco, CA"', add
label define city_lbl 6300 `"San Juan, PR"', add
label define city_lbl 6310 `"San Jose, CA"', add
label define city_lbl 6311 `"San Leandro, CA"', add
label define city_lbl 6312 `"San Mateo, CA"', add
label define city_lbl 6320 `"Santa Barbara, CA"', add
label define city_lbl 6321 `"Santa Cruz, CA"', add
label define city_lbl 6322 `"Santa Fe, NM"', add
label define city_lbl 6326 `"Sandy Springs, GA"', add
label define city_lbl 6330 `"Santa Ana, CA"', add
label define city_lbl 6335 `"Santa Clara, CA"', add
label define city_lbl 6340 `"Santa Clarita, CA"', add
label define city_lbl 6350 `"Santa Rosa, CA"', add
label define city_lbl 6351 `"Sapulpa, OK"', add
label define city_lbl 6352 `"Saratoga Springs, NY"', add
label define city_lbl 6353 `"Saugus, MA"', add
label define city_lbl 6354 `"Sault Ste. Marie, MI"', add
label define city_lbl 6360 `"Santa Monica, CA"', add
label define city_lbl 6370 `"Savannah, GA"', add
label define city_lbl 6390 `"Schenectedy, NY"', add
label define city_lbl 6410 `"Scranton, PA"', add
label define city_lbl 6430 `"Seattle, WA"', add
label define city_lbl 6431 `"Sedalia, MO"', add
label define city_lbl 6432 `"Selma, AL"', add
label define city_lbl 6433 `"Seminole, OK"', add
label define city_lbl 6434 `"Shaker Heights, OH"', add
label define city_lbl 6435 `"Shamokin, PA"', add
label define city_lbl 6437 `"Sharpsville, PA"', add
label define city_lbl 6438 `"Shawnee, OK"', add
label define city_lbl 6440 `"Sharon, PA"', add
label define city_lbl 6450 `"Sheboygan, WI"', add
label define city_lbl 6451 `"Shelby, NC"', add
label define city_lbl 6452 `"Shelbyville, IN"', add
label define city_lbl 6453 `"Shelton, CT"', add
label define city_lbl 6470 `"Shenandoah Borough, PA"', add
label define city_lbl 6471 `"Sherman, TX"', add
label define city_lbl 6472 `"Shorewood, WI"', add
label define city_lbl 6490 `"Shreveport, LA"', add
label define city_lbl 6500 `"Simi Valley, CA"', add
label define city_lbl 6510 `"Sioux City, IA"', add
label define city_lbl 6530 `"Sioux Falls, SD"', add
label define city_lbl 6550 `"Smithfield, RI (1850)"', add
label define city_lbl 6570 `"Somerville, MA"', add
label define city_lbl 6590 `"South Bend, IN"', add
label define city_lbl 6591 `"South Bethlehem, PA"', add
label define city_lbl 6592 `"South Boise, ID"', add
label define city_lbl 6593 `"South Gate, CA"', add
label define city_lbl 6594 `"South Milwaukee, WI"', add
label define city_lbl 6595 `"South Norwalk, CT"', add
label define city_lbl 6610 `"South Omaha, NE"', add
label define city_lbl 6611 `"South Orange, NJ"', add
label define city_lbl 6612 `"South Pasadena, CA"', add
label define city_lbl 6613 `"South Pittsburgh, PA"', add
label define city_lbl 6614 `"South Portland, ME"', add
label define city_lbl 6615 `"South River, NJ"', add
label define city_lbl 6616 `"South St. Paul, MN"', add
label define city_lbl 6617 `"Southbridge, MA"', add
label define city_lbl 6620 `"Spartanburg, SC"', add
label define city_lbl 6630 `"Spokane, WA"', add
label define city_lbl 6640 `"Spring Valley, NV"', add
label define city_lbl 6650 `"Springfield, IL"', add
label define city_lbl 6670 `"Springfield, MA"', add
label define city_lbl 6690 `"Springfield, MO"', add
label define city_lbl 6691 `"St. Augustine, FL"', add
label define city_lbl 6692 `"St. Charles, MO"', add
label define city_lbl 6693 `"St. Cloud, MN"', add
label define city_lbl 6710 `"Springfield, OH"', add
label define city_lbl 6730 `"Stamford, CT"', add
label define city_lbl 6731 `"Statesville, NC"', add
label define city_lbl 6732 `"Staunton, VA"', add
label define city_lbl 6733 `"Steelton, PA"', add
label define city_lbl 6734 `"Sterling, IL"', add
label define city_lbl 6750 `"Sterling Heights, MI"', add
label define city_lbl 6770 `"Steubenville, OH"', add
label define city_lbl 6771 `"Stevens Point, WI"', add
label define city_lbl 6772 `"Stillwater, MN"', add
label define city_lbl 6789 `"Stowe, PA"', add
label define city_lbl 6790 `"Stockton, CA"', add
label define city_lbl 6791 `"Stoneham, MA"', add
label define city_lbl 6792 `"Stonington, CT"', add
label define city_lbl 6793 `"Stratford, CT"', add
label define city_lbl 6794 `"Streator, IL"', add
label define city_lbl 6795 `"Struthers, OH"', add
label define city_lbl 6796 `"Suffolk, VA"', add
label define city_lbl 6797 `"Summit, NJ"', add
label define city_lbl 6798 `"Sumter, SC"', add
label define city_lbl 6799 `"Sunbury, PA"', add
label define city_lbl 6810 `"Sunnyvale, CA"', add
label define city_lbl 6830 `"Superior, WI"', add
label define city_lbl 6831 `"Swampscott, MA"', add
label define city_lbl 6832 `"Sweetwater, TX"', add
label define city_lbl 6833 `"Swissvale, PA"', add
label define city_lbl 6850 `"Syracuse, NY"', add
label define city_lbl 6870 `"Tacoma, WA"', add
label define city_lbl 6871 `"Tallahassee, FL"', add
label define city_lbl 6872 `"Tamaqua, PA"', add
label define city_lbl 6890 `"Tampa, FL"', add
label define city_lbl 6910 `"Taunton, MA"', add
label define city_lbl 6911 `"Taylor, PA"', add
label define city_lbl 6912 `"Temple, TX"', add
label define city_lbl 6913 `"Teaneck, NJ"', add
label define city_lbl 6930 `"Tempe, AZ"', add
label define city_lbl 6950 `"Terre Haute, IN"', add
label define city_lbl 6951 `"Texarkana, TX/AR"', add
label define city_lbl 6952 `"Thomasville, GA"', add
label define city_lbl 6953 `"Thomasville, NC"', add
label define city_lbl 6954 `"Tiffin, OH"', add
label define city_lbl 6960 `"Thousand Oaks, CA"', add
label define city_lbl 6970 `"Toledo, OH"', add
label define city_lbl 6971 `"Tonawanda, NY"', add
label define city_lbl 6990 `"Topeka, KS"', add
label define city_lbl 6991 `"Torrington, CT"', add
label define city_lbl 6992 `"Traverse City, MI"', add
label define city_lbl 7000 `"Torrance, CA"', add
label define city_lbl 7010 `"Trenton, NJ"', add
label define city_lbl 7011 `"Trinidad, CO"', add
label define city_lbl 7030 `"Troy, NY"', add
label define city_lbl 7050 `"Tucson, AZ"', add
label define city_lbl 7070 `"Tulsa, OK"', add
label define city_lbl 7071 `"Turtle Creek, PA"', add
label define city_lbl 7072 `"Tuscaloosa, AL"', add
label define city_lbl 7073 `"Two Rivers, WI"', add
label define city_lbl 7074 `"Tyler, TX"', add
label define city_lbl 7079 `"Union, NJ"', add
label define city_lbl 7080 `"Union City, NJ"', add
label define city_lbl 7081 `"Uniontown, PA"', add
label define city_lbl 7082 `"University City, MO"', add
label define city_lbl 7083 `"Urbana, IL"', add
label define city_lbl 7084 `"Upper Darby, PA"', add
label define city_lbl 7090 `"Utica, NY"', add
label define city_lbl 7091 `"Valdosta, GA"', add
label define city_lbl 7093 `"Valley Stream, NY"', add
label define city_lbl 7100 `"Vancouver, WA"', add
label define city_lbl 7110 `"Vallejo, CA"', add
label define city_lbl 7111 `"Vandergrift, PA"', add
label define city_lbl 7112 `"Venice, CA"', add
label define city_lbl 7120 `"Vicksburg, MS"', add
label define city_lbl 7121 `"Vincennes, IN"', add
label define city_lbl 7122 `"Virginia, MN"', add
label define city_lbl 7123 `"Virginia City, NV"', add
label define city_lbl 7130 `"Virginia Beach, VA"', add
label define city_lbl 7140 `"Visalia, CA"', add
label define city_lbl 7150 `"Waco, TX"', add
label define city_lbl 7151 `"Wakefield, MA"', add
label define city_lbl 7152 `"Walla Walla, WA"', add
label define city_lbl 7153 `"Wallingford, CT"', add
label define city_lbl 7170 `"Waltham, MA"', add
label define city_lbl 7180 `"Warren, MI"', add
label define city_lbl 7190 `"Warren, OH"', add
label define city_lbl 7191 `"Warren, PA"', add
label define city_lbl 7210 `"Warwick Town, RI"', add
label define city_lbl 7230 `"Washington, DC"', add
label define city_lbl 7231 `"Georgetown, DC"', add
label define city_lbl 7241 `"Washington, PA"', add
label define city_lbl 7242 `"Washington, VA"', add
label define city_lbl 7250 `"Waterbury, CT"', add
label define city_lbl 7270 `"Waterloo, IA"', add
label define city_lbl 7290 `"Waterloo, NY"', add
label define city_lbl 7310 `"Watertown, NY"', add
label define city_lbl 7311 `"Watertown, WI"', add
label define city_lbl 7312 `"Watertown, SD"', add
label define city_lbl 7313 `"Watertown, MA"', add
label define city_lbl 7314 `"Waterville, ME"', add
label define city_lbl 7315 `"Watervliet, NY"', add
label define city_lbl 7316 `"Waukegan, IL"', add
label define city_lbl 7317 `"Waukesha, WI"', add
label define city_lbl 7318 `"Wausau, WI"', add
label define city_lbl 7319 `"Wauwatosa, WI"', add
label define city_lbl 7320 `"West Covina, CA"', add
label define city_lbl 7321 `"Waycross, GA"', add
label define city_lbl 7322 `"Waynesboro, PA"', add
label define city_lbl 7323 `"Webb City, MO"', add
label define city_lbl 7324 `"Webster Groves, MO"', add
label define city_lbl 7325 `"Webster, MA"', add
label define city_lbl 7326 `"Wellesley, MA"', add
label define city_lbl 7327 `"Wenatchee, WA"', add
label define city_lbl 7328 `"Weehawken, NJ"', add
label define city_lbl 7329 `"West Bay City, MI"', add
label define city_lbl 7330 `"West Hoboken, NJ"', add
label define city_lbl 7331 `"West Bethlehem, PA"', add
label define city_lbl 7332 `"West Chester, PA"', add
label define city_lbl 7333 `"West Frankfort, IL"', add
label define city_lbl 7334 `"West Hartford, CT"', add
label define city_lbl 7335 `"West Haven, CT"', add
label define city_lbl 7340 `"West Allis, WI"', add
label define city_lbl 7350 `"West New York, NJ"', add
label define city_lbl 7351 `"West Orange, NJ"', add
label define city_lbl 7352 `"West Palm Beach, FL"', add
label define city_lbl 7353 `"West Springfield, MA"', add
label define city_lbl 7360 `"West Valley City, UT"', add
label define city_lbl 7370 `"West Troy, NY"', add
label define city_lbl 7371 `"West Warwick, RI"', add
label define city_lbl 7372 `"Westbrook, ME"', add
label define city_lbl 7373 `"Westerly, RI"', add
label define city_lbl 7374 `"Westfield, MA"', add
label define city_lbl 7375 `"Westfield, NJ"', add
label define city_lbl 7376 `"Wewoka, OK"', add
label define city_lbl 7377 `"Weymouth, MA"', add
label define city_lbl 7390 `"Wheeling, WV"', add
label define city_lbl 7400 `"White Plains, NY"', add
label define city_lbl 7401 `"Whiting, IN"', add
label define city_lbl 7402 `"Whittier, CA"', add
label define city_lbl 7410 `"Wichita, KS"', add
label define city_lbl 7430 `"Wichita Falls, TX"', add
label define city_lbl 7450 `"Wilkes-Barre, PA"', add
label define city_lbl 7460 `"Wilkinsburg, PA"', add
label define city_lbl 7470 `"Williamsport, PA"', add
label define city_lbl 7471 `"Willimantic, CT"', add
label define city_lbl 7472 `"Wilmette, IL"', add
label define city_lbl 7490 `"Wilmington, DE"', add
label define city_lbl 7510 `"Wilmington, NC"', add
label define city_lbl 7511 `"Wilson, NC"', add
label define city_lbl 7512 `"Winchester, VA"', add
label define city_lbl 7513 `"Winchester, MA"', add
label define city_lbl 7514 `"Windham, CT"', add
label define city_lbl 7515 `"Winnetka, IL"', add
label define city_lbl 7516 `"Winona, MN"', add
label define city_lbl 7530 `"Winston-Salem, NC"', add
label define city_lbl 7531 `"Winthrop, MA"', add
label define city_lbl 7532 `"Woburn, MA"', add
label define city_lbl 7533 `"Woodlawn, PA"', add
label define city_lbl 7534 `"Woodmont, CT"', add
label define city_lbl 7535 `"Woodbridge, NJ"', add
label define city_lbl 7550 `"Woonsocket, RI"', add
label define city_lbl 7551 `"Wooster, OH"', add
label define city_lbl 7570 `"Worcester, MA"', add
label define city_lbl 7571 `"Wyandotte, MI"', add
label define city_lbl 7572 `"Xenia, OH"', add
label define city_lbl 7573 `"Yakima, WA"', add
label define city_lbl 7590 `"Yonkers, NY"', add
label define city_lbl 7610 `"York, PA"', add
label define city_lbl 7630 `"Youngstown, OH"', add
label define city_lbl 7631 `"Ypsilanti, MI"', add
label define city_lbl 7650 `"Zanesville, OH"', add
label values city city_lbl

label define homeland_lbl 1 `"PUMA does not include a Homeland area"'
label define homeland_lbl 2 `"PUMA includes a Homeland area"', add
label values homeland homeland_lbl

label define cntry_lbl 630 `"Puerto Rico"'
label define cntry_lbl 840 `"United States"', add
label values cntry cntry_lbl

label define gq_lbl 0 `"Vacant unit"'
label define gq_lbl 1 `"Households under 1970 definition"', add
label define gq_lbl 2 `"Additional households under 1990 definition"', add
label define gq_lbl 3 `"Group quarters--Institutions"', add
label define gq_lbl 4 `"Other group quarters"', add
label define gq_lbl 5 `"Additional households under 2000 definition"', add
label define gq_lbl 6 `"Fragment"', add
label values gq gq_lbl

label define gqtype_lbl 0 `"NA (non-group quarters households)"'
label define gqtype_lbl 1 `"Institution (1990, 2000, ACS/PRCS)"', add
label define gqtype_lbl 2 `"Correctional institutions"', add
label define gqtype_lbl 3 `"Mental institutions"', add
label define gqtype_lbl 4 `"Institutions for the elderly, handicapped, and poor"', add
label define gqtype_lbl 5 `"Non-institutional GQ"', add
label define gqtype_lbl 6 `"Military"', add
label define gqtype_lbl 7 `"College dormitory"', add
label define gqtype_lbl 8 `"Rooming house"', add
label define gqtype_lbl 9 `"Other non-institutional GQ and unknown"', add
label values gqtype gqtype_lbl

label define gqtyped_lbl 000 `"NA (non-group quarters households)"'
label define gqtyped_lbl 010 `"Family group, someone related to head"', add
label define gqtyped_lbl 020 `"Unrelated individuals, no one related to head"', add
label define gqtyped_lbl 100 `"Institution (1990, 2000, ACS/PRCS)"', add
label define gqtyped_lbl 200 `"Correctional institution"', add
label define gqtyped_lbl 210 `"Federal/state correctional"', add
label define gqtyped_lbl 211 `"Prison"', add
label define gqtyped_lbl 212 `"Penitentiary"', add
label define gqtyped_lbl 213 `"Military prison"', add
label define gqtyped_lbl 220 `"Local correctional"', add
label define gqtyped_lbl 221 `"Jail"', add
label define gqtyped_lbl 230 `"School juvenile delinquents"', add
label define gqtyped_lbl 240 `"Reformatory"', add
label define gqtyped_lbl 250 `"Camp or chain gang"', add
label define gqtyped_lbl 260 `"House of correction"', add
label define gqtyped_lbl 300 `"Mental institutions"', add
label define gqtyped_lbl 400 `"Institutions for the elderly, handicapped, and poor"', add
label define gqtyped_lbl 410 `"Homes for elderly"', add
label define gqtyped_lbl 411 `"Aged, dependent home"', add
label define gqtyped_lbl 412 `"Nursing/convalescent home"', add
label define gqtyped_lbl 413 `"Old soldiers' home"', add
label define gqtyped_lbl 420 `"Other Instits (Not Aged)"', add
label define gqtyped_lbl 421 `"Other Institution nec"', add
label define gqtyped_lbl 430 `"Homes neglected/depend children"', add
label define gqtyped_lbl 431 `"Orphan school"', add
label define gqtyped_lbl 432 `"Orphans' home, asylum"', add
label define gqtyped_lbl 440 `"Other instits for children"', add
label define gqtyped_lbl 441 `"Children's home, asylum"', add
label define gqtyped_lbl 450 `"Homes physically handicapped"', add
label define gqtyped_lbl 451 `"Deaf, blind school"', add
label define gqtyped_lbl 452 `"Deaf, blind, epilepsy"', add
label define gqtyped_lbl 460 `"Mentally handicapped home"', add
label define gqtyped_lbl 461 `"School for feeblemind"', add
label define gqtyped_lbl 470 `"TB and chronic disease hospital"', add
label define gqtyped_lbl 471 `"Chronic hospitals"', add
label define gqtyped_lbl 472 `"Sanatoria"', add
label define gqtyped_lbl 480 `"Poor houses and farms"', add
label define gqtyped_lbl 481 `"Poor house, almshouse"', add
label define gqtyped_lbl 482 `"Poor farm, workhouse"', add
label define gqtyped_lbl 491 `"Maternity homes for unmarried mothers"', add
label define gqtyped_lbl 492 `"Homes for widows, single, fallen women"', add
label define gqtyped_lbl 493 `"Detention homes"', add
label define gqtyped_lbl 494 `"Misc asylums"', add
label define gqtyped_lbl 495 `"Home, other dependent"', add
label define gqtyped_lbl 496 `"Institution combination or unknown"', add
label define gqtyped_lbl 500 `"Non-institutional group quarters"', add
label define gqtyped_lbl 501 `"Family formerly in institutional group quarters"', add
label define gqtyped_lbl 502 `"Unrelated individual residing with family formerly in institutional group quarters"', add
label define gqtyped_lbl 600 `"Military"', add
label define gqtyped_lbl 601 `"U.S. army installation"', add
label define gqtyped_lbl 602 `"Navy, marine installation"', add
label define gqtyped_lbl 603 `"Navy ships"', add
label define gqtyped_lbl 604 `"Air service"', add
label define gqtyped_lbl 700 `"College dormitory"', add
label define gqtyped_lbl 701 `"Military service academies"', add
label define gqtyped_lbl 800 `"Rooming house"', add
label define gqtyped_lbl 801 `"Hotel"', add
label define gqtyped_lbl 802 `"House, lodging apartments"', add
label define gqtyped_lbl 803 `"YMCA, YWCA"', add
label define gqtyped_lbl 804 `"Club"', add
label define gqtyped_lbl 900 `"Other Non-Instit GQ"', add
label define gqtyped_lbl 901 `"Other Non-Instit GQ"', add
label define gqtyped_lbl 910 `"Schools"', add
label define gqtyped_lbl 911 `"Boarding schools"', add
label define gqtyped_lbl 912 `"Academy, institute"', add
label define gqtyped_lbl 913 `"Industrial training"', add
label define gqtyped_lbl 914 `"Indian school"', add
label define gqtyped_lbl 920 `"Hospitals"', add
label define gqtyped_lbl 921 `"Hospital, charity"', add
label define gqtyped_lbl 922 `"Infirmary"', add
label define gqtyped_lbl 923 `"Maternity hospital"', add
label define gqtyped_lbl 924 `"Children's hospital"', add
label define gqtyped_lbl 931 `"Church, Abbey"', add
label define gqtyped_lbl 932 `"Convent"', add
label define gqtyped_lbl 933 `"Monastery"', add
label define gqtyped_lbl 934 `"Mission"', add
label define gqtyped_lbl 935 `"Seminary"', add
label define gqtyped_lbl 936 `"Religious commune"', add
label define gqtyped_lbl 937 `"Other religious"', add
label define gqtyped_lbl 940 `"Work sites"', add
label define gqtyped_lbl 941 `"Construction, except rr"', add
label define gqtyped_lbl 942 `"Lumber"', add
label define gqtyped_lbl 943 `"Mining"', add
label define gqtyped_lbl 944 `"Railroad"', add
label define gqtyped_lbl 945 `"Farms, ranches"', add
label define gqtyped_lbl 946 `"Ships, boats"', add
label define gqtyped_lbl 947 `"Other industrial"', add
label define gqtyped_lbl 948 `"Other worksites"', add
label define gqtyped_lbl 950 `"Nurses home, dorm"', add
label define gqtyped_lbl 955 `"Passenger ships"', add
label define gqtyped_lbl 960 `"Other group quarters"', add
label define gqtyped_lbl 997 `"Unknown"', add
label define gqtyped_lbl 999 `"Fragment (boarders and lodgers, 1900)"', add
label values gqtyped gqtyped_lbl

label define farm_lbl 0 `"N/A"'
label define farm_lbl 1 `"Non-Farm"', add
label define farm_lbl 2 `"Farm"', add
label define farm_lbl 9 `"Blank/missing"', add
label values farm farm_lbl

label define ownershp_lbl 0 `"N/A"'
label define ownershp_lbl 1 `"Owned or being bought (loan)"', add
label define ownershp_lbl 2 `"Rented"', add
label values ownershp ownershp_lbl

label define ownershpd_lbl 00 `"N/A"'
label define ownershpd_lbl 10 `"Owned or being bought"', add
label define ownershpd_lbl 11 `"Check mark (owns?)"', add
label define ownershpd_lbl 12 `"Owned free and clear"', add
label define ownershpd_lbl 13 `"Owned with mortgage or loan"', add
label define ownershpd_lbl 20 `"Rented"', add
label define ownershpd_lbl 21 `"No cash rent"', add
label define ownershpd_lbl 22 `"With cash rent"', add
label values ownershpd ownershpd_lbl

label define mortgage_lbl 0 `"N/A"'
label define mortgage_lbl 1 `"No, owned free and clear"', add
label define mortgage_lbl 2 `"Check mark on manuscript (probably yes)"', add
label define mortgage_lbl 3 `"Yes, mortgaged/ deed of trust or similar debt"', add
label define mortgage_lbl 4 `"Yes, contract to purchase"', add
label values mortgage mortgage_lbl

label define mortgag2_lbl 0 `"N/A"'
label define mortgag2_lbl 1 `"No"', add
label define mortgag2_lbl 2 `"Yes"', add
label define mortgag2_lbl 3 `"Yes, 2nd mortgage"', add
label define mortgag2_lbl 4 `"Yes, home equity loan"', add
label define mortgag2_lbl 5 `"Yes, 2nd mortgage and home equity loan"', add
label values mortgag2 mortgag2_lbl

label define mortamt1_lbl 00000 `"N/A"'
label define mortamt1_lbl 00001 `"00001"', add
label values mortamt1 mortamt1_lbl

label define taxincl_lbl 0 `"N/A"'
label define taxincl_lbl 1 `"No"', add
label define taxincl_lbl 2 `"Yes"', add
label values taxincl taxincl_lbl

label define insincl_lbl 0 `"N/A"'
label define insincl_lbl 1 `"No"', add
label define insincl_lbl 2 `"Yes, payment includes insurance premiums"', add
label values insincl insincl_lbl

label define proptx99_lbl 000 `"N/A (GQ/vacant/not owned  or being bought/not a one-family h"'
label define proptx99_lbl 001 `"None"', add
label define proptx99_lbl 002 `"$1-49  ($2-49 in 1990 PR Samples)"', add
label define proptx99_lbl 003 `"$ 50 - 99"', add
label define proptx99_lbl 004 `"$ 100 - 149"', add
label define proptx99_lbl 005 `"$ 150 - 199"', add
label define proptx99_lbl 006 `"$ 200 - 249"', add
label define proptx99_lbl 007 `"$ 250 - 299"', add
label define proptx99_lbl 008 `"$ 300 - 349"', add
label define proptx99_lbl 009 `"$ 350 - 399"', add
label define proptx99_lbl 010 `"$ 400 - 449"', add
label define proptx99_lbl 011 `"$ 450 - 499"', add
label define proptx99_lbl 012 `"$ 500 - 549"', add
label define proptx99_lbl 013 `"$ 550 - 599"', add
label define proptx99_lbl 014 `"$ 600 - 649"', add
label define proptx99_lbl 015 `"$ 650 - 699"', add
label define proptx99_lbl 016 `"$ 700 - 749"', add
label define proptx99_lbl 017 `"$ 750 - 799"', add
label define proptx99_lbl 018 `"$ 800 - 849"', add
label define proptx99_lbl 019 `"$ 850 - 899"', add
label define proptx99_lbl 020 `"$ 900 - 949"', add
label define proptx99_lbl 021 `"$ 950 - 999"', add
label define proptx99_lbl 022 `"$ 1,000 - 1,099"', add
label define proptx99_lbl 023 `"$ 1,100 - 1,199"', add
label define proptx99_lbl 024 `"$ 1,200 - 1,299"', add
label define proptx99_lbl 025 `"$ 1,300 - 1,399"', add
label define proptx99_lbl 026 `"$ 1,400 - 1,499"', add
label define proptx99_lbl 027 `"$ 1,500 - 1,599"', add
label define proptx99_lbl 028 `"$ 1,600 - 1,699"', add
label define proptx99_lbl 029 `"$ 1,700 - 1,799"', add
label define proptx99_lbl 030 `"$ 1,800 - 1,899"', add
label define proptx99_lbl 031 `"$ 1,900 - 1,999"', add
label define proptx99_lbl 032 `"$ 2,000 - 2,099"', add
label define proptx99_lbl 033 `"$2100-2199  ($2199+ 1990 PR Samples)"', add
label define proptx99_lbl 034 `"$ 2,200 - 2,299"', add
label define proptx99_lbl 035 `"$ 2,300 - 2,399"', add
label define proptx99_lbl 036 `"$ 2,400 - 2,499"', add
label define proptx99_lbl 037 `"$ 2,500 - 2,599"', add
label define proptx99_lbl 038 `"$ 2,600 - 2,699"', add
label define proptx99_lbl 039 `"$ 2,700 - 2,799"', add
label define proptx99_lbl 040 `"$ 2,800 - 2,899"', add
label define proptx99_lbl 041 `"$ 2,900 - 2,999"', add
label define proptx99_lbl 042 `"$ 3,000 - 3,099"', add
label define proptx99_lbl 043 `"$ 3,100 - 3,199"', add
label define proptx99_lbl 044 `"$ 3,200 - 3,299"', add
label define proptx99_lbl 045 `"$ 3,300 - 3,399"', add
label define proptx99_lbl 046 `"$ 3,400 - 3,499"', add
label define proptx99_lbl 047 `"$ 3,500 - 3,599"', add
label define proptx99_lbl 048 `"$ 3,600 - 3,699"', add
label define proptx99_lbl 049 `"$ 3,700 - 3,799"', add
label define proptx99_lbl 050 `"$ 3,800 - 3,899"', add
label define proptx99_lbl 051 `"$ 3,900 - 3,999"', add
label define proptx99_lbl 052 `"$ 4,000 - 4,099"', add
label define proptx99_lbl 053 `"$ 4,100 - 4,199"', add
label define proptx99_lbl 054 `"$ 4,200 - 4,299"', add
label define proptx99_lbl 055 `"$ 4,300 - 4,399"', add
label define proptx99_lbl 056 `"$ 4,400 - 4,499"', add
label define proptx99_lbl 057 `"$4500 (1990 U.S. Samples)"', add
label define proptx99_lbl 058 `"$4500-4599 ($4501+ 1990 U.S. Samples)"', add
label define proptx99_lbl 059 `"$4600 - 4699"', add
label define proptx99_lbl 060 `"$4700 - 4799"', add
label define proptx99_lbl 061 `"$4800 - 4899"', add
label define proptx99_lbl 062 `"$4900 - 4999"', add
label define proptx99_lbl 063 `"$5000 - 5499"', add
label define proptx99_lbl 064 `"$5500 - 5999"', add
label define proptx99_lbl 065 `"$6000 - 6999"', add
label define proptx99_lbl 066 `"$7000 - 7999"', add
label define proptx99_lbl 067 `"$8000-8999 ($8000-9099 in 2000)"', add
label define proptx99_lbl 068 `"$9000-9999 ($9100+ in 2000)"', add
label define proptx99_lbl 069 `"$10000-10999 ($10,000+ in 2000-2017 ACS/PRCS Samples)"', add
label define proptx99_lbl 070 `"$11000-11999"', add
label define proptx99_lbl 071 `"$12000-12999"', add
label define proptx99_lbl 072 `"$13000-13999"', add
label define proptx99_lbl 073 `"$14000-14999"', add
label define proptx99_lbl 074 `"$15000-15999"', add
label define proptx99_lbl 075 `"$16000-16999"', add
label define proptx99_lbl 076 `"$17000-17999"', add
label define proptx99_lbl 077 `"$18000-18999"', add
label define proptx99_lbl 078 `"$19000-19999"', add
label define proptx99_lbl 079 `"$20000-20999"', add
label define proptx99_lbl 080 `"$21000-21999"', add
label define proptx99_lbl 081 `"$22000-22999"', add
label define proptx99_lbl 082 `"$23000-23999"', add
label define proptx99_lbl 083 `"$24000-24999"', add
label define proptx99_lbl 084 `"$25000-25999"', add
label define proptx99_lbl 085 `"$26000-26999"', add
label define proptx99_lbl 086 `"$27000-27999"', add
label define proptx99_lbl 087 `"$28000-28999"', add
label define proptx99_lbl 088 `"$29000-29999"', add
label define proptx99_lbl 089 `"$30000-39999"', add
label define proptx99_lbl 090 `"$31000-31999"', add
label define proptx99_lbl 091 `"$32000-32999"', add
label define proptx99_lbl 092 `"$33000-33999"', add
label define proptx99_lbl 093 `"$34000-34999"', add
label define proptx99_lbl 094 `"$35000-35999"', add
label define proptx99_lbl 095 `"$36000-36999"', add
label define proptx99_lbl 096 `"$37000-37999"', add
label define proptx99_lbl 097 `"$38000-38999"', add
label define proptx99_lbl 098 `"$39000-39999"', add
label define proptx99_lbl 099 `"$40000-40999"', add
label define proptx99_lbl 100 `"$41000-41999"', add
label define proptx99_lbl 101 `"$42000-42999"', add
label define proptx99_lbl 102 `"$43000-43999"', add
label define proptx99_lbl 103 `"$44000-44999"', add
label define proptx99_lbl 104 `"$45000-45999"', add
label define proptx99_lbl 105 `"$46000-46999"', add
label define proptx99_lbl 106 `"$47000-47999"', add
label define proptx99_lbl 107 `"$48000-48999"', add
label define proptx99_lbl 108 `"$49000-49999"', add
label define proptx99_lbl 109 `"$50000-50999"', add
label define proptx99_lbl 110 `"$51000-51999"', add
label define proptx99_lbl 111 `"$52000-52999"', add
label define proptx99_lbl 112 `"$53000-53999"', add
label define proptx99_lbl 113 `"$54000-54999"', add
label define proptx99_lbl 114 `"$55000-55999"', add
label define proptx99_lbl 115 `"$56000-56999"', add
label define proptx99_lbl 116 `"$57000-57999"', add
label define proptx99_lbl 117 `"$58000-58999"', add
label define proptx99_lbl 118 `"$59000-59999"', add
label define proptx99_lbl 119 `"$60000-60999"', add
label define proptx99_lbl 120 `"$61000-61999"', add
label define proptx99_lbl 121 `"$62000-62999"', add
label define proptx99_lbl 122 `"$63000-63999"', add
label define proptx99_lbl 123 `"$64000-64999"', add
label define proptx99_lbl 124 `"$65000-65999"', add
label define proptx99_lbl 125 `"$66000-66999"', add
label define proptx99_lbl 126 `"$67000-67999"', add
label define proptx99_lbl 127 `"$68000-68999"', add
label define proptx99_lbl 128 `"$69000-69999"', add
label define proptx99_lbl 129 `"$70000-70999"', add
label define proptx99_lbl 130 `"$71000-71999"', add
label define proptx99_lbl 131 `"$72000-72999"', add
label define proptx99_lbl 132 `"$73000-73999"', add
label define proptx99_lbl 133 `"$74000-74999"', add
label define proptx99_lbl 134 `"$75000-75999"', add
label define proptx99_lbl 135 `"$76000-76999"', add
label define proptx99_lbl 136 `"$77000-77999"', add
label define proptx99_lbl 137 `"$78000-78999"', add
label define proptx99_lbl 138 `"$79000-79999"', add
label define proptx99_lbl 139 `"$80000-80999"', add
label define proptx99_lbl 140 `"$81000-81999"', add
label define proptx99_lbl 141 `"$82000-82999"', add
label define proptx99_lbl 142 `"$83000-83999"', add
label define proptx99_lbl 143 `"$84000-84999"', add
label define proptx99_lbl 144 `"$85000-85999"', add
label define proptx99_lbl 145 `"$86000-86999"', add
label define proptx99_lbl 146 `"$87000-87999"', add
label define proptx99_lbl 147 `"$88000-88999"', add
label define proptx99_lbl 148 `"$89000-89999"', add
label define proptx99_lbl 149 `"$90000-90999"', add
label define proptx99_lbl 150 `"$91000-91999"', add
label define proptx99_lbl 151 `"$92000-92999"', add
label define proptx99_lbl 152 `"$93000-93999"', add
label define proptx99_lbl 153 `"$94000-94999"', add
label define proptx99_lbl 154 `"$95000-95999"', add
label define proptx99_lbl 155 `"$96000-96999"', add
label define proptx99_lbl 156 `"$97000-97999"', add
label define proptx99_lbl 157 `"$98000-98999"', add
label define proptx99_lbl 158 `"$99000-99999"', add
label define proptx99_lbl 159 `"$100,000+ (2018-Onward Samples)"', add
label values proptx99 proptx99_lbl

label define rentgrs_lbl 00000 `"N/A"'
label define rentgrs_lbl 00010 `"$1-19"', add
label define rentgrs_lbl 00025 `"$20-29"', add
label define rentgrs_lbl 00035 `"$30-39"', add
label define rentgrs_lbl 00045 `"$40-49"', add
label define rentgrs_lbl 00055 `"$50-59"', add
label define rentgrs_lbl 00065 `"$60-69"', add
label define rentgrs_lbl 00075 `"$70-79"', add
label define rentgrs_lbl 00090 `"$80-99"', add
label define rentgrs_lbl 00110 `"$100-119"', add
label define rentgrs_lbl 00135 `"$120-149"', add
label define rentgrs_lbl 00175 `"$150-199"', add
label define rentgrs_lbl 00200 `"$200+"', add
label values rentgrs rentgrs_lbl

label define rentmeal_lbl 0 `"N/A"'
label define rentmeal_lbl 1 `"No, meals not included"', add
label define rentmeal_lbl 2 `"Yes"', add
label values rentmeal rentmeal_lbl

label define hhincome_lbl 9999998 `"9999998"'
label define hhincome_lbl 9999999 `"9999999"', add
label values hhincome hhincome_lbl

label define foodstmp_lbl 0 `"N/A"'
label define foodstmp_lbl 1 `"No"', add
label define foodstmp_lbl 2 `"Yes"', add
label values foodstmp foodstmp_lbl

label define valueh_lbl 0000000 `"$0 (1940)"'
label define valueh_lbl 0000250 `"Less than $500"', add
label define valueh_lbl 0000500 `"Less than $999"', add
label define valueh_lbl 0001000 `"Less than $2,000"', add
label define valueh_lbl 0001500 `"$2,000-$1,999"', add
label define valueh_lbl 0002500 `"Less than $5,000"', add
label define valueh_lbl 0003500 `"$3,000-$3,999"', add
label define valueh_lbl 0004000 `"$3,000-$4,999"', add
label define valueh_lbl 0004500 `"$4,000-$4,999"', add
label define valueh_lbl 0005000 `"Less than $10,000"', add
label define valueh_lbl 0006250 `"$5,000 - 7,499"', add
label define valueh_lbl 0008750 `"$7,500 - 9,999"', add
label define valueh_lbl 0012500 `"$10,000 - 14,999"', add
label define valueh_lbl 0011250 `"$10,000 - 12,499"', add
label define valueh_lbl 0013750 `"$12,500 - 14,999"', add
label define valueh_lbl 0017500 `"$15,000 - 19,999"', add
label define valueh_lbl 0016250 `"$15,000 - 17,499"', add
label define valueh_lbl 0018750 `"$17,500 - 19,999"', add
label define valueh_lbl 0025000 `"$20,000-$29,999"', add
label define valueh_lbl 0022500 `"$20,000 - 24,999"', add
label define valueh_lbl 0021250 `"$20,000 - 22,499"', add
label define valueh_lbl 0023750 `"$22,500 - 24,999"', add
label define valueh_lbl 0030000 `"$25,000 - 34,999"', add
label define valueh_lbl 0026250 `"$25,000 - 27,499"', add
label define valueh_lbl 0027500 `"$25,000 - 29,999"', add
label define valueh_lbl 0028750 `"$27,500 - 29,999"', add
label define valueh_lbl 0032500 `"$30,000 - 34,999"', add
label define valueh_lbl 0031250 `"$30,000-$32,499"', add
label define valueh_lbl 0033750 `"$32,500-$34,999"', add
label define valueh_lbl 0035000 `"$35,000+"', add
label define valueh_lbl 0042500 `"$35,000 - 49,999"', add
label define valueh_lbl 0037500 `"$35,000 - 39,999"', add
label define valueh_lbl 0036250 `"$35,000-$37,499"', add
label define valueh_lbl 0038750 `"$37,500-$39,999"', add
label define valueh_lbl 0045000 `"$40,000 - 49,999"', add
label define valueh_lbl 0042499 `"$40,000 - 44,999"', add
label define valueh_lbl 0047500 `"$45,000 - 49,999"', add
label define valueh_lbl 0050000 `"$50,000+"', add
label define valueh_lbl 0055000 `"$50,000 - 59,999"', add
label define valueh_lbl 0052500 `"$50,000 - 54,999"', add
label define valueh_lbl 0057500 `"$55,000 - 59,999"', add
label define valueh_lbl 0065000 `"$60,000 - 69,999"', add
label define valueh_lbl 0062500 `"$60,000 - 64,999"', add
label define valueh_lbl 0067500 `"$65,000 - 69,999"', add
label define valueh_lbl 0075000 `"$70,000 - 79,999"', add
label define valueh_lbl 0072500 `"$70,000 - 74,999"', add
label define valueh_lbl 0077500 `"$75,000 - 79,999"', add
label define valueh_lbl 0087500 `"$75,000-$99,999"', add
label define valueh_lbl 0085000 `"$80,000 - 89,999"', add
label define valueh_lbl 0095000 `"$90,000 - 99,999"', add
label define valueh_lbl 0100000 `"$100,000+"', add
label define valueh_lbl 0112500 `"$100,000 - 124,999"', add
label define valueh_lbl 0137500 `"$125,000 - 149,999"', add
label define valueh_lbl 0175000 `"$150,000 - 199,999"', add
label define valueh_lbl 0162500 `"$150,000 - 174,999"', add
label define valueh_lbl 0187500 `"$175,000 - 199,999"', add
label define valueh_lbl 0200000 `"$200,000+"', add
label define valueh_lbl 0225000 `"$200,000 - 249,999"', add
label define valueh_lbl 0275000 `"$250,000 - 299,999"', add
label define valueh_lbl 0350000 `"$300,000 - 399,999"', add
label define valueh_lbl 0400000 `"$400,000+"', add
label define valueh_lbl 0450000 `"$400,000 - 499,999"', add
label define valueh_lbl 0625000 `"$500,000 - 749,999"', add
label define valueh_lbl 0875000 `"$750,000 - 999,999"', add
label define valueh_lbl 1000000 `"$1,000,000+"', add
label define valueh_lbl 9999998 `"Missing"', add
label define valueh_lbl 9999999 `"N/A"', add
label values valueh valueh_lbl

label define lingisol_lbl 0 `"N/A (group quarters/vacant)"'
label define lingisol_lbl 1 `"Not linguistically isolated"', add
label define lingisol_lbl 2 `"Linguistically isolated"', add
label values lingisol lingisol_lbl

label define vacancy_lbl 0 `"N/A"'
label define vacancy_lbl 1 `"For rent or sale"', add
label define vacancy_lbl 2 `"For sale only"', add
label define vacancy_lbl 3 `"Rented or sold but not (yet) occupied"', add
label define vacancy_lbl 4 `"For seasonal, recreational or other occasional use"', add
label define vacancy_lbl 5 `"For occasional use"', add
label define vacancy_lbl 6 `"For seasonal use"', add
label define vacancy_lbl 7 `"For migrant farm workers"', add
label define vacancy_lbl 8 `"For seasonal use or migratory"', add
label define vacancy_lbl 9 `"Other vacant"', add
label values vacancy vacancy_lbl

label define bedrooms_lbl 00 `"N/A"'
label define bedrooms_lbl 01 `"No bedrooms"', add
label define bedrooms_lbl 02 `"1"', add
label define bedrooms_lbl 03 `"2"', add
label define bedrooms_lbl 04 `"3"', add
label define bedrooms_lbl 05 `"4 (1970-2000, 2000-2007 ACS/PRCS)"', add
label define bedrooms_lbl 06 `"5+ (1970-2000, 2000-2007 ACS/PRCS)"', add
label define bedrooms_lbl 07 `"6"', add
label define bedrooms_lbl 08 `"7"', add
label define bedrooms_lbl 09 `"8"', add
label define bedrooms_lbl 10 `"9"', add
label define bedrooms_lbl 11 `"10"', add
label define bedrooms_lbl 12 `"11"', add
label define bedrooms_lbl 13 `"12"', add
label define bedrooms_lbl 14 `"13"', add
label define bedrooms_lbl 15 `"14"', add
label define bedrooms_lbl 16 `"15"', add
label define bedrooms_lbl 17 `"16"', add
label define bedrooms_lbl 18 `"17"', add
label define bedrooms_lbl 19 `"18"', add
label define bedrooms_lbl 20 `"19"', add
label define bedrooms_lbl 21 `"20"', add
label define bedrooms_lbl 22 `"21"', add
label values bedrooms bedrooms_lbl

label define phone_lbl 0 `"N/A"'
label define phone_lbl 1 `"No, no phone available"', add
label define phone_lbl 2 `"Yes, phone available"', add
label define phone_lbl 8 `"Suppressed (see comparability tab)"', add
label values phone phone_lbl

label define cinethh_lbl 0 `"N/A (GQ)"'
label define cinethh_lbl 1 `"Yes, with a subscription to an Internet Service"', add
label define cinethh_lbl 2 `"Yes, without a subscription to an Internet Service"', add
label define cinethh_lbl 3 `"No Internet access at this house, apartment, or mobile home"', add
label define cinethh_lbl 8 `"Suppressed for data year 2024 for select PUMAs"', add
label values cinethh cinethh_lbl

label define cilaptop_lbl 0 `"N/A (GQ)"'
label define cilaptop_lbl 1 `"Yes"', add
label define cilaptop_lbl 2 `"No"', add
label values cilaptop cilaptop_lbl

label define cismrtphn_lbl 0 `"N/A (GQ)"'
label define cismrtphn_lbl 1 `"Yes"', add
label define cismrtphn_lbl 2 `"No"', add
label values cismrtphn cismrtphn_lbl

label define citablet_lbl 0 `"N/A (GQ)"'
label define citablet_lbl 1 `"Yes"', add
label define citablet_lbl 2 `"No"', add
label values citablet citablet_lbl

label define cihand_lbl 0 `"N/A (GQ)"'
label define cihand_lbl 1 `"Yes"', add
label define cihand_lbl 2 `"No"', add
label values cihand cihand_lbl

label define ciothcomp_lbl 0 `"N/A (GQ)"'
label define ciothcomp_lbl 1 `"Yes"', add
label define ciothcomp_lbl 2 `"No"', add
label values ciothcomp ciothcomp_lbl

label define cidatapln_lbl 0 `"N/A (GQ)"'
label define cidatapln_lbl 1 `"Yes"', add
label define cidatapln_lbl 2 `"No"', add
label define cidatapln_lbl 8 `"Suppressed for data years 2023 and 2024 for select PUMAs"', add
label values cidatapln cidatapln_lbl

label define cihispeed_lbl 00 `"N/A (GQ)"'
label define cihispeed_lbl 10 `"Yes (Cable modem, fiber optic or DSL service)"', add
label define cihispeed_lbl 11 `"Cable modem only"', add
label define cihispeed_lbl 12 `"Fiber optic only"', add
label define cihispeed_lbl 13 `"DSL service only"', add
label define cihispeed_lbl 14 `"Cable modem + Fiber optic"', add
label define cihispeed_lbl 15 `"Cable modem + DSL service"', add
label define cihispeed_lbl 16 `"Fiber optic + DSL service"', add
label define cihispeed_lbl 17 `"Cable modem, Fiber optic and DSL service"', add
label define cihispeed_lbl 20 `"No"', add
label define cihispeed_lbl 88 `"Suppressed for data years 2023 and 2024 for select PUMAs"', add
label values cihispeed cihispeed_lbl

label define cisat_lbl 0 `"N/A (GQ)"'
label define cisat_lbl 1 `"Yes"', add
label define cisat_lbl 2 `"No"', add
label define cisat_lbl 8 `"Suppressed for data year 2023 for select PUMAs"', add
label values cisat cisat_lbl

label define cidial_lbl 0 `"N/A (GQ)"'
label define cidial_lbl 1 `"Yes"', add
label define cidial_lbl 2 `"No"', add
label define cidial_lbl 8 `"Suppressed for data years 2023 and 2024 for select PUMAs"', add
label values cidial cidial_lbl

label define ciothsvc_lbl 0 `"N/A (GQ)"'
label define ciothsvc_lbl 1 `"Yes"', add
label define ciothsvc_lbl 2 `"No"', add
label define ciothsvc_lbl 8 `"Suppressed for data years 2023 and 2024 for select PUMAs"', add
label values ciothsvc ciothsvc_lbl

label define vehicles_lbl 0 `"N/A"'
label define vehicles_lbl 1 `"1 available"', add
label define vehicles_lbl 2 `"2"', add
label define vehicles_lbl 3 `"3"', add
label define vehicles_lbl 4 `"4"', add
label define vehicles_lbl 5 `"5"', add
label define vehicles_lbl 6 `"6 (6+, 2000, ACS and PRCS)"', add
label define vehicles_lbl 7 `"7+"', add
label define vehicles_lbl 9 `"No vehicles available"', add
label values vehicles vehicles_lbl

label define nfams_lbl 00 `"0 families (vacant unit)"'
label define nfams_lbl 01 `"1 family or N/A"', add
label define nfams_lbl 02 `"2 families"', add
label define nfams_lbl 03 `"3"', add
label define nfams_lbl 04 `"4"', add
label define nfams_lbl 05 `"5"', add
label define nfams_lbl 06 `"6"', add
label define nfams_lbl 07 `"7"', add
label define nfams_lbl 08 `"8"', add
label define nfams_lbl 09 `"9"', add
label define nfams_lbl 10 `"10"', add
label define nfams_lbl 11 `"11"', add
label define nfams_lbl 12 `"12"', add
label define nfams_lbl 13 `"13"', add
label define nfams_lbl 14 `"14"', add
label define nfams_lbl 15 `"15"', add
label define nfams_lbl 16 `"16"', add
label define nfams_lbl 17 `"17"', add
label define nfams_lbl 18 `"18"', add
label define nfams_lbl 19 `"19"', add
label define nfams_lbl 20 `"20"', add
label define nfams_lbl 21 `"21"', add
label define nfams_lbl 22 `"22"', add
label define nfams_lbl 23 `"23"', add
label define nfams_lbl 24 `"24"', add
label define nfams_lbl 25 `"25"', add
label define nfams_lbl 26 `"26"', add
label define nfams_lbl 27 `"27"', add
label define nfams_lbl 28 `"28"', add
label define nfams_lbl 29 `"29"', add
label define nfams_lbl 30 `"30"', add
label define nfams_lbl 31 `"31"', add
label define nfams_lbl 32 `"32"', add
label define nfams_lbl 33 `"33"', add
label define nfams_lbl 34 `"34"', add
label define nfams_lbl 35 `"35"', add
label define nfams_lbl 36 `"36"', add
label define nfams_lbl 37 `"37"', add
label define nfams_lbl 38 `"38"', add
label define nfams_lbl 39 `"39"', add
label define nfams_lbl 40 `"40"', add
label define nfams_lbl 41 `"41"', add
label define nfams_lbl 42 `"42"', add
label define nfams_lbl 43 `"43"', add
label define nfams_lbl 44 `"44"', add
label define nfams_lbl 45 `"45"', add
label define nfams_lbl 46 `"46"', add
label define nfams_lbl 47 `"47"', add
label define nfams_lbl 48 `"48"', add
label define nfams_lbl 49 `"49"', add
label define nfams_lbl 50 `"50"', add
label define nfams_lbl 51 `"51"', add
label define nfams_lbl 52 `"52"', add
label define nfams_lbl 53 `"53"', add
label define nfams_lbl 54 `"54"', add
label define nfams_lbl 55 `"55"', add
label define nfams_lbl 56 `"56"', add
label define nfams_lbl 57 `"57"', add
label define nfams_lbl 58 `"58"', add
label define nfams_lbl 59 `"59"', add
label define nfams_lbl 60 `"60"', add
label values nfams nfams_lbl

label define nsubfam_lbl 0 `"No subfamilies or N/A (GQ/vacant unit)"'
label define nsubfam_lbl 1 `"1 subfamily"', add
label define nsubfam_lbl 2 `"2 subfamilies"', add
label define nsubfam_lbl 3 `"3"', add
label define nsubfam_lbl 4 `"4"', add
label define nsubfam_lbl 5 `"5"', add
label define nsubfam_lbl 6 `"6"', add
label define nsubfam_lbl 7 `"7"', add
label define nsubfam_lbl 8 `"8"', add
label define nsubfam_lbl 9 `"9"', add
label values nsubfam nsubfam_lbl

label define ncouples_lbl 0 `"0 couples or N/A"'
label define ncouples_lbl 1 `"1"', add
label define ncouples_lbl 2 `"2"', add
label define ncouples_lbl 3 `"3"', add
label define ncouples_lbl 4 `"4"', add
label define ncouples_lbl 5 `"5"', add
label define ncouples_lbl 6 `"6"', add
label define ncouples_lbl 7 `"7"', add
label define ncouples_lbl 8 `"8"', add
label define ncouples_lbl 9 `"9"', add
label values ncouples ncouples_lbl

label define nmothers_lbl 0 `"0 mothers or N/A"'
label define nmothers_lbl 1 `"1"', add
label define nmothers_lbl 2 `"2"', add
label define nmothers_lbl 3 `"3"', add
label define nmothers_lbl 4 `"4"', add
label define nmothers_lbl 5 `"5"', add
label define nmothers_lbl 6 `"6"', add
label define nmothers_lbl 7 `"7"', add
label define nmothers_lbl 8 `"8"', add
label define nmothers_lbl 9 `"9"', add
label values nmothers nmothers_lbl

label define nfathers_lbl 0 `"0 fathers or N/A"'
label define nfathers_lbl 1 `"1"', add
label define nfathers_lbl 2 `"2"', add
label define nfathers_lbl 3 `"3"', add
label define nfathers_lbl 4 `"4"', add
label define nfathers_lbl 5 `"5"', add
label define nfathers_lbl 6 `"6"', add
label define nfathers_lbl 7 `"7"', add
label define nfathers_lbl 8 `"8"', add
label define nfathers_lbl 9 `"9"', add
label values nfathers nfathers_lbl

label define multgen_lbl 0 `"N/A"'
label define multgen_lbl 1 `"1 generation"', add
label define multgen_lbl 2 `"2 generations"', add
label define multgen_lbl 3 `"3+ generations"', add
label values multgen multgen_lbl

label define multgend_lbl 00 `"N/A"'
label define multgend_lbl 10 `"1 generation"', add
label define multgend_lbl 20 `"1-2 generations (Census 2008 definition)"', add
label define multgend_lbl 21 `"2 adjacent generations, adult-children"', add
label define multgend_lbl 22 `"2 adjacent generations, adult-adult"', add
label define multgend_lbl 23 `"2 nonadjacent generations"', add
label define multgend_lbl 24 `"2 adjacent generations, no linking spouse"', add
label define multgend_lbl 31 `"3+ generations (Census 2008 definition)"', add
label define multgend_lbl 32 `"3+ generations (Additional IPUMS definition)"', add
label values multgend multgend_lbl

label define repwtp_lbl 0 `"Repwtp not available"'
label define repwtp_lbl 1 `"Repwtp available"', add
label values repwtp repwtp_lbl

label define famunit_lbl 01 `"1st family in household or group quarters"'
label define famunit_lbl 02 `"2nd family in household or group quarters"', add
label define famunit_lbl 03 `"3rd"', add
label define famunit_lbl 04 `"4th"', add
label define famunit_lbl 05 `"5th"', add
label define famunit_lbl 06 `"6th"', add
label define famunit_lbl 07 `"7th"', add
label define famunit_lbl 08 `"8th"', add
label define famunit_lbl 09 `"9th"', add
label define famunit_lbl 10 `"10th"', add
label define famunit_lbl 11 `"11th"', add
label define famunit_lbl 12 `"12th"', add
label define famunit_lbl 13 `"13th"', add
label define famunit_lbl 14 `"14th"', add
label define famunit_lbl 15 `"15th"', add
label define famunit_lbl 16 `"16th"', add
label define famunit_lbl 17 `"17th"', add
label define famunit_lbl 18 `"18th"', add
label define famunit_lbl 19 `"19th"', add
label define famunit_lbl 20 `"20th"', add
label define famunit_lbl 21 `"21th"', add
label define famunit_lbl 22 `"22th"', add
label define famunit_lbl 23 `"23th"', add
label define famunit_lbl 24 `"24th"', add
label define famunit_lbl 25 `"25th"', add
label define famunit_lbl 26 `"26th"', add
label define famunit_lbl 27 `"27th"', add
label define famunit_lbl 28 `"28th"', add
label define famunit_lbl 29 `"29th"', add
label define famunit_lbl 30 `"30th"', add
label define famunit_lbl 31 `"31st"', add
label define famunit_lbl 32 `"32nd"', add
label define famunit_lbl 33 `"33rd"', add
label define famunit_lbl 34 `"34th"', add
label define famunit_lbl 35 `"35th"', add
label define famunit_lbl 36 `"36th"', add
label define famunit_lbl 37 `"37th"', add
label define famunit_lbl 38 `"38th"', add
label define famunit_lbl 39 `"39th"', add
label define famunit_lbl 40 `"40th"', add
label define famunit_lbl 41 `"41st"', add
label define famunit_lbl 42 `"42nd"', add
label define famunit_lbl 43 `"43rd"', add
label define famunit_lbl 44 `"44th"', add
label define famunit_lbl 45 `"45th"', add
label define famunit_lbl 46 `"46th"', add
label define famunit_lbl 47 `"47th"', add
label define famunit_lbl 48 `"48th"', add
label define famunit_lbl 49 `"49th"', add
label define famunit_lbl 50 `"50th"', add
label define famunit_lbl 51 `"51st"', add
label define famunit_lbl 52 `"52nd"', add
label define famunit_lbl 53 `"53rd"', add
label define famunit_lbl 54 `"54th"', add
label define famunit_lbl 55 `"55th"', add
label define famunit_lbl 56 `"56th"', add
label define famunit_lbl 57 `"57th"', add
label define famunit_lbl 58 `"58th"', add
label define famunit_lbl 59 `"59th"', add
label define famunit_lbl 60 `"60th"', add
label values famunit famunit_lbl

label define famsize_lbl 01 `"1 family member present"'
label define famsize_lbl 02 `"2 family members present"', add
label define famsize_lbl 03 `"3"', add
label define famsize_lbl 04 `"4"', add
label define famsize_lbl 05 `"5"', add
label define famsize_lbl 06 `"6"', add
label define famsize_lbl 07 `"7"', add
label define famsize_lbl 08 `"8"', add
label define famsize_lbl 09 `"9"', add
label define famsize_lbl 10 `"10"', add
label define famsize_lbl 11 `"11"', add
label define famsize_lbl 12 `"12"', add
label define famsize_lbl 13 `"13"', add
label define famsize_lbl 14 `"14"', add
label define famsize_lbl 15 `"15"', add
label define famsize_lbl 16 `"16"', add
label define famsize_lbl 17 `"17"', add
label define famsize_lbl 18 `"18"', add
label define famsize_lbl 19 `"19"', add
label define famsize_lbl 20 `"20"', add
label define famsize_lbl 21 `"21"', add
label define famsize_lbl 22 `"22"', add
label define famsize_lbl 23 `"23"', add
label define famsize_lbl 24 `"24"', add
label define famsize_lbl 25 `"25"', add
label define famsize_lbl 26 `"26"', add
label define famsize_lbl 27 `"27"', add
label define famsize_lbl 28 `"28"', add
label define famsize_lbl 29 `"29"', add
label define famsize_lbl 30 `"30"', add
label define famsize_lbl 31 `"31"', add
label define famsize_lbl 32 `"32"', add
label define famsize_lbl 33 `"33"', add
label define famsize_lbl 34 `"34"', add
label define famsize_lbl 35 `"35"', add
label define famsize_lbl 36 `"36"', add
label define famsize_lbl 37 `"37"', add
label define famsize_lbl 38 `"38"', add
label define famsize_lbl 39 `"39"', add
label define famsize_lbl 40 `"40"', add
label define famsize_lbl 41 `"41"', add
label define famsize_lbl 42 `"42"', add
label define famsize_lbl 43 `"43"', add
label define famsize_lbl 44 `"44"', add
label define famsize_lbl 45 `"45"', add
label define famsize_lbl 46 `"46"', add
label define famsize_lbl 47 `"47"', add
label define famsize_lbl 48 `"48"', add
label define famsize_lbl 49 `"49"', add
label define famsize_lbl 50 `"50"', add
label define famsize_lbl 51 `"51"', add
label define famsize_lbl 52 `"52"', add
label define famsize_lbl 53 `"53"', add
label define famsize_lbl 54 `"54"', add
label define famsize_lbl 55 `"55"', add
label define famsize_lbl 56 `"56"', add
label define famsize_lbl 57 `"57"', add
label define famsize_lbl 58 `"58"', add
label values famsize famsize_lbl

label define subfam_lbl 0 `"Group quarters or not in subfamily"'
label define subfam_lbl 1 `"1st subfamily in household"', add
label define subfam_lbl 2 `"2nd subfamily in household"', add
label define subfam_lbl 3 `"3rd"', add
label define subfam_lbl 4 `"4th"', add
label define subfam_lbl 5 `"5th"', add
label define subfam_lbl 6 `"6th"', add
label define subfam_lbl 7 `"7th"', add
label define subfam_lbl 8 `"8th"', add
label define subfam_lbl 9 `"9th"', add
label values subfam subfam_lbl

label define sftype_lbl 0 `"Group quarters or not in subfamily"'
label define sftype_lbl 1 `"Married-couple related subfamily with children"', add
label define sftype_lbl 2 `"Married-couple related subfamily without children"', add
label define sftype_lbl 3 `"Father-child related subfamily"', add
label define sftype_lbl 4 `"Mother-child related subfamily"', add
label define sftype_lbl 5 `"Married-couple unrelated subfamily with children"', add
label define sftype_lbl 6 `"Married-couple unrelated subfamily without children"', add
label define sftype_lbl 7 `"Father-child unrelated subfamily"', add
label define sftype_lbl 8 `"Mother-child unrelated subfamily"', add
label values sftype sftype_lbl

label define momrule_lbl 00 `"No mother link"'
label define momrule_lbl 11 `"Direct link, clarity level 1"', add
label define momrule_lbl 12 `"Direct link, clarity level 2"', add
label define momrule_lbl 13 `"Direct link, clarity level 3"', add
label define momrule_lbl 14 `"Direct link, clarity level 4"', add
label define momrule_lbl 15 `"Direct link, clarity level 5"', add
label define momrule_lbl 16 `"Direct link, clarity level 6"', add
label define momrule_lbl 17 `"Direct link, clarity level 7"', add
label define momrule_lbl 18 `"Direct link, clarity level 8"', add
label define momrule_lbl 21 `"Second level link, clarity level 1"', add
label define momrule_lbl 22 `"Second level link, clarity level 2"', add
label define momrule_lbl 23 `"Second level link, clarity level 3"', add
label define momrule_lbl 24 `"Second level link, clarity level 4"', add
label define momrule_lbl 25 `"Second level link, clarity level 5"', add
label define momrule_lbl 26 `"Second level link, clarity level 6"', add
label define momrule_lbl 27 `"Second level link, clarity level 7"', add
label define momrule_lbl 28 `"Second level link, clarity level 8"', add
label define momrule_lbl 31 `"Third level link, clarity level 1"', add
label define momrule_lbl 32 `"Third level link, clarity level 2"', add
label define momrule_lbl 33 `"Third level link, clarity level 3"', add
label define momrule_lbl 34 `"Third level link, clarity level 4"', add
label define momrule_lbl 35 `"Third level link, clarity level 5"', add
label define momrule_lbl 36 `"Third level link, clarity level 6"', add
label define momrule_lbl 37 `"Third level link, clarity level 7"', add
label define momrule_lbl 38 `"Third level link, clarity level 8"', add
label values momrule momrule_lbl

label define nchild_lbl 0 `"0 children present"'
label define nchild_lbl 1 `"1 child present"', add
label define nchild_lbl 2 `"2"', add
label define nchild_lbl 3 `"3"', add
label define nchild_lbl 4 `"4"', add
label define nchild_lbl 5 `"5"', add
label define nchild_lbl 6 `"6"', add
label define nchild_lbl 7 `"7"', add
label define nchild_lbl 8 `"8"', add
label define nchild_lbl 9 `"9+"', add
label values nchild nchild_lbl

label define nchlt5_lbl 0 `"No children under age 5"'
label define nchlt5_lbl 1 `"1 child under age 5"', add
label define nchlt5_lbl 2 `"2"', add
label define nchlt5_lbl 3 `"3"', add
label define nchlt5_lbl 4 `"4"', add
label define nchlt5_lbl 5 `"5"', add
label define nchlt5_lbl 6 `"6"', add
label define nchlt5_lbl 7 `"7"', add
label define nchlt5_lbl 8 `"8"', add
label define nchlt5_lbl 9 `"9+"', add
label values nchlt5 nchlt5_lbl

label define nsibs_lbl 0 `"0 siblings"'
label define nsibs_lbl 1 `"1 sibling"', add
label define nsibs_lbl 2 `"2 siblings"', add
label define nsibs_lbl 3 `"3 siblings"', add
label define nsibs_lbl 4 `"4 siblings"', add
label define nsibs_lbl 5 `"5 siblings"', add
label define nsibs_lbl 6 `"6 siblings"', add
label define nsibs_lbl 7 `"7 siblings"', add
label define nsibs_lbl 8 `"8 siblings"', add
label define nsibs_lbl 9 `"9 or more siblings"', add
label values nsibs nsibs_lbl

label define eldch_lbl 00 `"Less than 1 year old"'
label define eldch_lbl 01 `"1"', add
label define eldch_lbl 02 `"2"', add
label define eldch_lbl 03 `"3"', add
label define eldch_lbl 04 `"4"', add
label define eldch_lbl 05 `"5"', add
label define eldch_lbl 06 `"6"', add
label define eldch_lbl 07 `"7"', add
label define eldch_lbl 08 `"8"', add
label define eldch_lbl 09 `"9"', add
label define eldch_lbl 10 `"10"', add
label define eldch_lbl 11 `"11"', add
label define eldch_lbl 12 `"12"', add
label define eldch_lbl 13 `"13"', add
label define eldch_lbl 14 `"14"', add
label define eldch_lbl 15 `"15"', add
label define eldch_lbl 16 `"16"', add
label define eldch_lbl 17 `"17"', add
label define eldch_lbl 18 `"18"', add
label define eldch_lbl 19 `"19"', add
label define eldch_lbl 20 `"20"', add
label define eldch_lbl 21 `"21"', add
label define eldch_lbl 22 `"22"', add
label define eldch_lbl 23 `"23"', add
label define eldch_lbl 24 `"24"', add
label define eldch_lbl 25 `"25"', add
label define eldch_lbl 26 `"26"', add
label define eldch_lbl 27 `"27"', add
label define eldch_lbl 28 `"28"', add
label define eldch_lbl 29 `"29"', add
label define eldch_lbl 30 `"30"', add
label define eldch_lbl 31 `"31"', add
label define eldch_lbl 32 `"32"', add
label define eldch_lbl 33 `"33"', add
label define eldch_lbl 34 `"34"', add
label define eldch_lbl 35 `"35"', add
label define eldch_lbl 36 `"36"', add
label define eldch_lbl 37 `"37"', add
label define eldch_lbl 38 `"38"', add
label define eldch_lbl 39 `"39"', add
label define eldch_lbl 40 `"40"', add
label define eldch_lbl 41 `"41"', add
label define eldch_lbl 42 `"42"', add
label define eldch_lbl 43 `"43"', add
label define eldch_lbl 44 `"44"', add
label define eldch_lbl 45 `"45"', add
label define eldch_lbl 46 `"46"', add
label define eldch_lbl 47 `"47"', add
label define eldch_lbl 48 `"48"', add
label define eldch_lbl 49 `"49"', add
label define eldch_lbl 50 `"50"', add
label define eldch_lbl 51 `"51"', add
label define eldch_lbl 52 `"52"', add
label define eldch_lbl 53 `"53"', add
label define eldch_lbl 54 `"54"', add
label define eldch_lbl 55 `"55"', add
label define eldch_lbl 56 `"56"', add
label define eldch_lbl 57 `"57"', add
label define eldch_lbl 58 `"58"', add
label define eldch_lbl 59 `"59"', add
label define eldch_lbl 60 `"60"', add
label define eldch_lbl 61 `"61"', add
label define eldch_lbl 62 `"62"', add
label define eldch_lbl 63 `"63"', add
label define eldch_lbl 64 `"64"', add
label define eldch_lbl 65 `"65"', add
label define eldch_lbl 66 `"66"', add
label define eldch_lbl 67 `"67"', add
label define eldch_lbl 68 `"68"', add
label define eldch_lbl 69 `"69"', add
label define eldch_lbl 70 `"70"', add
label define eldch_lbl 71 `"71"', add
label define eldch_lbl 72 `"72"', add
label define eldch_lbl 73 `"73"', add
label define eldch_lbl 74 `"74"', add
label define eldch_lbl 75 `"75"', add
label define eldch_lbl 76 `"76"', add
label define eldch_lbl 77 `"77"', add
label define eldch_lbl 78 `"78"', add
label define eldch_lbl 79 `"79"', add
label define eldch_lbl 80 `"80"', add
label define eldch_lbl 81 `"81"', add
label define eldch_lbl 82 `"82"', add
label define eldch_lbl 83 `"83"', add
label define eldch_lbl 84 `"84"', add
label define eldch_lbl 85 `"85"', add
label define eldch_lbl 86 `"86"', add
label define eldch_lbl 87 `"87"', add
label define eldch_lbl 88 `"88"', add
label define eldch_lbl 89 `"89"', add
label define eldch_lbl 90 `"90"', add
label define eldch_lbl 91 `"91"', add
label define eldch_lbl 92 `"92"', add
label define eldch_lbl 93 `"93"', add
label define eldch_lbl 94 `"94"', add
label define eldch_lbl 95 `"95"', add
label define eldch_lbl 96 `"96"', add
label define eldch_lbl 97 `"97"', add
label define eldch_lbl 98 `"98"', add
label define eldch_lbl 99 `"N/A"', add
label values eldch eldch_lbl

label define yngch_lbl 00 `"Less than 1 year old"'
label define yngch_lbl 01 `"1"', add
label define yngch_lbl 02 `"2"', add
label define yngch_lbl 03 `"3"', add
label define yngch_lbl 04 `"4"', add
label define yngch_lbl 05 `"5"', add
label define yngch_lbl 06 `"6"', add
label define yngch_lbl 07 `"7"', add
label define yngch_lbl 08 `"8"', add
label define yngch_lbl 09 `"9"', add
label define yngch_lbl 10 `"10"', add
label define yngch_lbl 11 `"11"', add
label define yngch_lbl 12 `"12"', add
label define yngch_lbl 13 `"13"', add
label define yngch_lbl 14 `"14"', add
label define yngch_lbl 15 `"15"', add
label define yngch_lbl 16 `"16"', add
label define yngch_lbl 17 `"17"', add
label define yngch_lbl 18 `"18"', add
label define yngch_lbl 19 `"19"', add
label define yngch_lbl 20 `"20"', add
label define yngch_lbl 21 `"21"', add
label define yngch_lbl 22 `"22"', add
label define yngch_lbl 23 `"23"', add
label define yngch_lbl 24 `"24"', add
label define yngch_lbl 25 `"25"', add
label define yngch_lbl 26 `"26"', add
label define yngch_lbl 27 `"27"', add
label define yngch_lbl 28 `"28"', add
label define yngch_lbl 29 `"29"', add
label define yngch_lbl 30 `"30"', add
label define yngch_lbl 31 `"31"', add
label define yngch_lbl 32 `"32"', add
label define yngch_lbl 33 `"33"', add
label define yngch_lbl 34 `"34"', add
label define yngch_lbl 35 `"35"', add
label define yngch_lbl 36 `"36"', add
label define yngch_lbl 37 `"37"', add
label define yngch_lbl 38 `"38"', add
label define yngch_lbl 39 `"39"', add
label define yngch_lbl 40 `"40"', add
label define yngch_lbl 41 `"41"', add
label define yngch_lbl 42 `"42"', add
label define yngch_lbl 43 `"43"', add
label define yngch_lbl 44 `"44"', add
label define yngch_lbl 45 `"45"', add
label define yngch_lbl 46 `"46"', add
label define yngch_lbl 47 `"47"', add
label define yngch_lbl 48 `"48"', add
label define yngch_lbl 49 `"49"', add
label define yngch_lbl 50 `"50"', add
label define yngch_lbl 51 `"51"', add
label define yngch_lbl 52 `"52"', add
label define yngch_lbl 53 `"53"', add
label define yngch_lbl 54 `"54"', add
label define yngch_lbl 55 `"55"', add
label define yngch_lbl 56 `"56"', add
label define yngch_lbl 57 `"57"', add
label define yngch_lbl 58 `"58"', add
label define yngch_lbl 59 `"59"', add
label define yngch_lbl 60 `"60"', add
label define yngch_lbl 61 `"61"', add
label define yngch_lbl 62 `"62"', add
label define yngch_lbl 63 `"63"', add
label define yngch_lbl 64 `"64"', add
label define yngch_lbl 65 `"65"', add
label define yngch_lbl 66 `"66"', add
label define yngch_lbl 67 `"67"', add
label define yngch_lbl 68 `"68"', add
label define yngch_lbl 69 `"69"', add
label define yngch_lbl 70 `"70"', add
label define yngch_lbl 71 `"71"', add
label define yngch_lbl 72 `"72"', add
label define yngch_lbl 73 `"73"', add
label define yngch_lbl 74 `"74"', add
label define yngch_lbl 75 `"75"', add
label define yngch_lbl 76 `"76"', add
label define yngch_lbl 77 `"77"', add
label define yngch_lbl 78 `"78"', add
label define yngch_lbl 79 `"79"', add
label define yngch_lbl 80 `"80"', add
label define yngch_lbl 81 `"81"', add
label define yngch_lbl 82 `"82"', add
label define yngch_lbl 83 `"83"', add
label define yngch_lbl 84 `"84"', add
label define yngch_lbl 85 `"85"', add
label define yngch_lbl 86 `"86"', add
label define yngch_lbl 87 `"87"', add
label define yngch_lbl 88 `"88"', add
label define yngch_lbl 89 `"89"', add
label define yngch_lbl 90 `"90"', add
label define yngch_lbl 91 `"91"', add
label define yngch_lbl 92 `"92"', add
label define yngch_lbl 93 `"93"', add
label define yngch_lbl 94 `"94"', add
label define yngch_lbl 95 `"95"', add
label define yngch_lbl 96 `"96"', add
label define yngch_lbl 97 `"97"', add
label define yngch_lbl 98 `"98"', add
label define yngch_lbl 99 `"N/A"', add
label values yngch yngch_lbl

label define relate_lbl 01 `"Head/Householder"'
label define relate_lbl 02 `"Spouse"', add
label define relate_lbl 03 `"Child"', add
label define relate_lbl 04 `"Child-in-law"', add
label define relate_lbl 05 `"Parent"', add
label define relate_lbl 06 `"Parent-in-Law"', add
label define relate_lbl 07 `"Sibling"', add
label define relate_lbl 08 `"Sibling-in-Law"', add
label define relate_lbl 09 `"Grandchild"', add
label define relate_lbl 10 `"Other relatives"', add
label define relate_lbl 11 `"Partner, friend, visitor"', add
label define relate_lbl 12 `"Other non-relatives"', add
label define relate_lbl 13 `"Institutional inmates"', add
label values relate relate_lbl

label define related_lbl 0101 `"Head/Householder"'
label define related_lbl 0201 `"Spouse"', add
label define related_lbl 0202 `"2nd/3rd Wife (Polygamous)"', add
label define related_lbl 0301 `"Child"', add
label define related_lbl 0302 `"Adopted Child"', add
label define related_lbl 0303 `"Stepchild"', add
label define related_lbl 0304 `"Adopted, n.s."', add
label define related_lbl 0401 `"Child-in-law"', add
label define related_lbl 0402 `"Step Child-in-law"', add
label define related_lbl 0501 `"Parent"', add
label define related_lbl 0502 `"Stepparent"', add
label define related_lbl 0601 `"Parent-in-Law"', add
label define related_lbl 0602 `"Stepparent-in-law"', add
label define related_lbl 0701 `"Sibling"', add
label define related_lbl 0702 `"Step/Half/Adopted Sibling"', add
label define related_lbl 0801 `"Sibling-in-Law"', add
label define related_lbl 0802 `"Step/Half Sibling-in-law"', add
label define related_lbl 0901 `"Grandchild"', add
label define related_lbl 0902 `"Adopted Grandchild"', add
label define related_lbl 0903 `"Step Grandchild"', add
label define related_lbl 0904 `"Grandchild-in-law"', add
label define related_lbl 1000 `"Other relatives:"', add
label define related_lbl 1001 `"Other Relatives"', add
label define related_lbl 1011 `"Grandparent"', add
label define related_lbl 1012 `"Step Grandparent"', add
label define related_lbl 1013 `"Grandparent-in-law"', add
label define related_lbl 1021 `"Aunt or Uncle"', add
label define related_lbl 1022 `"Aunt,Uncle-in-law"', add
label define related_lbl 1031 `"Nephew, Niece"', add
label define related_lbl 1032 `"Neph/Niece-in-law"', add
label define related_lbl 1033 `"Step/Adopted Nephew/Niece"', add
label define related_lbl 1034 `"Grand Niece/Nephew"', add
label define related_lbl 1041 `"Cousin"', add
label define related_lbl 1042 `"Cousin-in-law"', add
label define related_lbl 1051 `"Great Grandchild"', add
label define related_lbl 1061 `"Other relatives, nec"', add
label define related_lbl 1100 `"Partner, Friend, Visitor"', add
label define related_lbl 1110 `"Partner/friend"', add
label define related_lbl 1111 `"Friend"', add
label define related_lbl 1112 `"Partner"', add
label define related_lbl 1113 `"Partner/roommate"', add
label define related_lbl 1114 `"Unmarried Partner"', add
label define related_lbl 1115 `"Housemate/Roomate"', add
label define related_lbl 1120 `"Relative of partner"', add
label define related_lbl 1130 `"Concubine/Mistress"', add
label define related_lbl 1131 `"Visitor"', add
label define related_lbl 1132 `"Companion and family of companion"', add
label define related_lbl 1139 `"Allocated partner/friend/visitor"', add
label define related_lbl 1200 `"Other non-relatives"', add
label define related_lbl 1201 `"Roomers/boarders/lodgers"', add
label define related_lbl 1202 `"Boarders"', add
label define related_lbl 1203 `"Lodgers"', add
label define related_lbl 1204 `"Roomer"', add
label define related_lbl 1205 `"Tenant"', add
label define related_lbl 1206 `"Foster child"', add
label define related_lbl 1210 `"Employees:"', add
label define related_lbl 1211 `"Servant"', add
label define related_lbl 1212 `"Housekeeper"', add
label define related_lbl 1213 `"Maid"', add
label define related_lbl 1214 `"Cook"', add
label define related_lbl 1215 `"Nurse"', add
label define related_lbl 1216 `"Other probable domestic employee"', add
label define related_lbl 1217 `"Other employee"', add
label define related_lbl 1219 `"Relative of employee"', add
label define related_lbl 1221 `"Military"', add
label define related_lbl 1222 `"Students"', add
label define related_lbl 1223 `"Members of religious orders"', add
label define related_lbl 1230 `"Other non-relatives"', add
label define related_lbl 1239 `"Allocated other non-relative"', add
label define related_lbl 1240 `"Roomers/boarders/lodgers and foster children"', add
label define related_lbl 1241 `"Roomers/boarders/lodgers"', add
label define related_lbl 1242 `"Foster children"', add
label define related_lbl 1250 `"Employees"', add
label define related_lbl 1251 `"Domestic employees"', add
label define related_lbl 1252 `"Non-domestic employees"', add
label define related_lbl 1253 `"Relative of employee"', add
label define related_lbl 1260 `"Other non-relatives (1990 includes employees)"', add
label define related_lbl 1270 `"Non-inmate 1990"', add
label define related_lbl 1281 `"Head of group quarters"', add
label define related_lbl 1282 `"Employees of group quarters"', add
label define related_lbl 1283 `"Relative of head, staff, or employee group quarters"', add
label define related_lbl 1284 `"Other non-inmate 1940-1959"', add
label define related_lbl 1291 `"Military"', add
label define related_lbl 1292 `"College dormitories"', add
label define related_lbl 1293 `"Residents of rooming houses"', add
label define related_lbl 1294 `"Other non-inmate 1980 (includes employees and non-inmates in"', add
label define related_lbl 1295 `"Other non-inmates 1960-1970 (includes employees)"', add
label define related_lbl 1296 `"Non-inmates in institutions"', add
label define related_lbl 1301 `"Institutional inmates"', add
label define related_lbl 9996 `"Unclassifiable"', add
label define related_lbl 9997 `"Unknown"', add
label define related_lbl 9998 `"Illegible"', add
label define related_lbl 9999 `"Missing"', add
label values related related_lbl

label define sex_lbl 1 `"Male"'
label define sex_lbl 2 `"Female"', add
label define sex_lbl 9 `"Missing/blank"', add
label values sex sex_lbl

label define age_lbl 000 `"Less than 1 year old"'
label define age_lbl 001 `"1"', add
label define age_lbl 002 `"2"', add
label define age_lbl 003 `"3"', add
label define age_lbl 004 `"4"', add
label define age_lbl 005 `"5"', add
label define age_lbl 006 `"6"', add
label define age_lbl 007 `"7"', add
label define age_lbl 008 `"8"', add
label define age_lbl 009 `"9"', add
label define age_lbl 010 `"10"', add
label define age_lbl 011 `"11"', add
label define age_lbl 012 `"12"', add
label define age_lbl 013 `"13"', add
label define age_lbl 014 `"14"', add
label define age_lbl 015 `"15"', add
label define age_lbl 016 `"16"', add
label define age_lbl 017 `"17"', add
label define age_lbl 018 `"18"', add
label define age_lbl 019 `"19"', add
label define age_lbl 020 `"20"', add
label define age_lbl 021 `"21"', add
label define age_lbl 022 `"22"', add
label define age_lbl 023 `"23"', add
label define age_lbl 024 `"24"', add
label define age_lbl 025 `"25"', add
label define age_lbl 026 `"26"', add
label define age_lbl 027 `"27"', add
label define age_lbl 028 `"28"', add
label define age_lbl 029 `"29"', add
label define age_lbl 030 `"30"', add
label define age_lbl 031 `"31"', add
label define age_lbl 032 `"32"', add
label define age_lbl 033 `"33"', add
label define age_lbl 034 `"34"', add
label define age_lbl 035 `"35"', add
label define age_lbl 036 `"36"', add
label define age_lbl 037 `"37"', add
label define age_lbl 038 `"38"', add
label define age_lbl 039 `"39"', add
label define age_lbl 040 `"40"', add
label define age_lbl 041 `"41"', add
label define age_lbl 042 `"42"', add
label define age_lbl 043 `"43"', add
label define age_lbl 044 `"44"', add
label define age_lbl 045 `"45"', add
label define age_lbl 046 `"46"', add
label define age_lbl 047 `"47"', add
label define age_lbl 048 `"48"', add
label define age_lbl 049 `"49"', add
label define age_lbl 050 `"50"', add
label define age_lbl 051 `"51"', add
label define age_lbl 052 `"52"', add
label define age_lbl 053 `"53"', add
label define age_lbl 054 `"54"', add
label define age_lbl 055 `"55"', add
label define age_lbl 056 `"56"', add
label define age_lbl 057 `"57"', add
label define age_lbl 058 `"58"', add
label define age_lbl 059 `"59"', add
label define age_lbl 060 `"60"', add
label define age_lbl 061 `"61"', add
label define age_lbl 062 `"62"', add
label define age_lbl 063 `"63"', add
label define age_lbl 064 `"64"', add
label define age_lbl 065 `"65"', add
label define age_lbl 066 `"66"', add
label define age_lbl 067 `"67"', add
label define age_lbl 068 `"68"', add
label define age_lbl 069 `"69"', add
label define age_lbl 070 `"70"', add
label define age_lbl 071 `"71"', add
label define age_lbl 072 `"72"', add
label define age_lbl 073 `"73"', add
label define age_lbl 074 `"74"', add
label define age_lbl 075 `"75"', add
label define age_lbl 076 `"76"', add
label define age_lbl 077 `"77"', add
label define age_lbl 078 `"78"', add
label define age_lbl 079 `"79"', add
label define age_lbl 080 `"80"', add
label define age_lbl 081 `"81"', add
label define age_lbl 082 `"82"', add
label define age_lbl 083 `"83"', add
label define age_lbl 084 `"84"', add
label define age_lbl 085 `"85"', add
label define age_lbl 086 `"86"', add
label define age_lbl 087 `"87"', add
label define age_lbl 088 `"88"', add
label define age_lbl 089 `"89"', add
label define age_lbl 090 `"90 (90+ in 1980 and 1990)"', add
label define age_lbl 091 `"91"', add
label define age_lbl 092 `"92"', add
label define age_lbl 093 `"93"', add
label define age_lbl 094 `"94"', add
label define age_lbl 095 `"95"', add
label define age_lbl 096 `"96"', add
label define age_lbl 097 `"97"', add
label define age_lbl 098 `"98"', add
label define age_lbl 099 `"99"', add
label define age_lbl 100 `"100 (100+ in 1960-1970)"', add
label define age_lbl 101 `"101"', add
label define age_lbl 102 `"102"', add
label define age_lbl 103 `"103"', add
label define age_lbl 104 `"104"', add
label define age_lbl 105 `"105"', add
label define age_lbl 106 `"106"', add
label define age_lbl 107 `"107"', add
label define age_lbl 108 `"108"', add
label define age_lbl 109 `"109"', add
label define age_lbl 110 `"110"', add
label define age_lbl 111 `"111"', add
label define age_lbl 112 `"112 (112+ in the 1980 internal data)"', add
label define age_lbl 113 `"113"', add
label define age_lbl 114 `"114"', add
label define age_lbl 115 `"115 (115+ in the 1990 internal data)"', add
label define age_lbl 116 `"116"', add
label define age_lbl 117 `"117"', add
label define age_lbl 118 `"118"', add
label define age_lbl 119 `"119"', add
label define age_lbl 120 `"120"', add
label define age_lbl 121 `"121"', add
label define age_lbl 122 `"122"', add
label define age_lbl 123 `"123"', add
label define age_lbl 124 `"124"', add
label define age_lbl 125 `"125"', add
label define age_lbl 126 `"126"', add
label define age_lbl 127 `"127"', add
label define age_lbl 128 `"128"', add
label define age_lbl 129 `"129"', add
label define age_lbl 130 `"130"', add
label define age_lbl 131 `"131"', add
label define age_lbl 132 `"132"', add
label define age_lbl 133 `"133"', add
label define age_lbl 134 `"134"', add
label define age_lbl 135 `"135"', add
label define age_lbl 140 `"140"', add
label define age_lbl 999 `"Missing"', add
label values age age_lbl

label define ageorig_lbl 00 `"Less than 1 year old"'
label define ageorig_lbl 01 `"1"', add
label define ageorig_lbl 02 `"2"', add
label define ageorig_lbl 03 `"3"', add
label define ageorig_lbl 04 `"4"', add
label define ageorig_lbl 05 `"5"', add
label define ageorig_lbl 06 `"6"', add
label define ageorig_lbl 07 `"7"', add
label define ageorig_lbl 08 `"8"', add
label define ageorig_lbl 09 `"9"', add
label define ageorig_lbl 10 `"10"', add
label define ageorig_lbl 11 `"11"', add
label define ageorig_lbl 12 `"12"', add
label define ageorig_lbl 13 `"13"', add
label define ageorig_lbl 14 `"14"', add
label define ageorig_lbl 15 `"15"', add
label define ageorig_lbl 16 `"16"', add
label define ageorig_lbl 17 `"17"', add
label define ageorig_lbl 18 `"18"', add
label define ageorig_lbl 19 `"19"', add
label define ageorig_lbl 20 `"20"', add
label define ageorig_lbl 21 `"21"', add
label define ageorig_lbl 22 `"22"', add
label define ageorig_lbl 23 `"23"', add
label define ageorig_lbl 24 `"24"', add
label define ageorig_lbl 25 `"25"', add
label define ageorig_lbl 26 `"26"', add
label define ageorig_lbl 27 `"27"', add
label define ageorig_lbl 28 `"28"', add
label define ageorig_lbl 29 `"29"', add
label define ageorig_lbl 30 `"30"', add
label define ageorig_lbl 31 `"31"', add
label define ageorig_lbl 32 `"32"', add
label define ageorig_lbl 33 `"33"', add
label define ageorig_lbl 34 `"34"', add
label define ageorig_lbl 35 `"35"', add
label define ageorig_lbl 36 `"36"', add
label define ageorig_lbl 37 `"37"', add
label define ageorig_lbl 38 `"38"', add
label define ageorig_lbl 39 `"39"', add
label define ageorig_lbl 40 `"40"', add
label define ageorig_lbl 41 `"41"', add
label define ageorig_lbl 42 `"42"', add
label define ageorig_lbl 43 `"43"', add
label define ageorig_lbl 44 `"44"', add
label define ageorig_lbl 45 `"45"', add
label define ageorig_lbl 46 `"46"', add
label define ageorig_lbl 47 `"47"', add
label define ageorig_lbl 48 `"48"', add
label define ageorig_lbl 49 `"49"', add
label define ageorig_lbl 50 `"50"', add
label define ageorig_lbl 51 `"51"', add
label define ageorig_lbl 52 `"52"', add
label define ageorig_lbl 53 `"53"', add
label define ageorig_lbl 54 `"54"', add
label define ageorig_lbl 55 `"55"', add
label define ageorig_lbl 56 `"56"', add
label define ageorig_lbl 57 `"57"', add
label define ageorig_lbl 58 `"58"', add
label define ageorig_lbl 59 `"59"', add
label define ageorig_lbl 60 `"60"', add
label define ageorig_lbl 61 `"61"', add
label define ageorig_lbl 62 `"62"', add
label define ageorig_lbl 63 `"63"', add
label define ageorig_lbl 64 `"64"', add
label define ageorig_lbl 65 `"65"', add
label define ageorig_lbl 66 `"66"', add
label define ageorig_lbl 67 `"67"', add
label define ageorig_lbl 68 `"68"', add
label define ageorig_lbl 69 `"69"', add
label define ageorig_lbl 70 `"70"', add
label define ageorig_lbl 71 `"71"', add
label define ageorig_lbl 72 `"72"', add
label define ageorig_lbl 73 `"73"', add
label define ageorig_lbl 74 `"74"', add
label define ageorig_lbl 75 `"75"', add
label define ageorig_lbl 76 `"76"', add
label define ageorig_lbl 77 `"77"', add
label define ageorig_lbl 78 `"78"', add
label define ageorig_lbl 79 `"79"', add
label define ageorig_lbl 80 `"80"', add
label define ageorig_lbl 81 `"81"', add
label define ageorig_lbl 82 `"82"', add
label define ageorig_lbl 83 `"83"', add
label define ageorig_lbl 84 `"84"', add
label define ageorig_lbl 85 `"85"', add
label define ageorig_lbl 86 `"86"', add
label define ageorig_lbl 87 `"87"', add
label define ageorig_lbl 88 `"88"', add
label define ageorig_lbl 89 `"89"', add
label define ageorig_lbl 90 `"90 (90+ in 1980 and 1990)"', add
label define ageorig_lbl 91 `"91"', add
label define ageorig_lbl 92 `"92"', add
label define ageorig_lbl 93 `"93"', add
label define ageorig_lbl 94 `"94"', add
label define ageorig_lbl 95 `"95"', add
label define ageorig_lbl 96 `"96"', add
label define ageorig_lbl 97 `"97"', add
label define ageorig_lbl 98 `"98"', add
label define ageorig_lbl 99 `"99"', add
label values ageorig ageorig_lbl

label define birthqtr_lbl 0 `"N/A"'
label define birthqtr_lbl 1 `"Jan-Feb-March"', add
label define birthqtr_lbl 2 `"April-May-June"', add
label define birthqtr_lbl 3 `"July-Aug-Sept"', add
label define birthqtr_lbl 4 `"Oct-Nov-Dec"', add
label define birthqtr_lbl 9 `"Missing"', add
label values birthqtr birthqtr_lbl

label define marst_lbl 1 `"Married, spouse present"'
label define marst_lbl 2 `"Married, spouse absent"', add
label define marst_lbl 3 `"Separated"', add
label define marst_lbl 4 `"Divorced"', add
label define marst_lbl 5 `"Widowed"', add
label define marst_lbl 6 `"Never married/single"', add
label define marst_lbl 9 `"Blank, missing"', add
label values marst marst_lbl

label define marrinyr_lbl 0 `"N/A"'
label define marrinyr_lbl 1 `"Blank (No)"', add
label define marrinyr_lbl 2 `"Yes"', add
label values marrinyr marrinyr_lbl

label define yrmarr_lbl 0000 `"N/A"'
label values yrmarr yrmarr_lbl

label define divinyr_lbl 0 `"N/A"'
label define divinyr_lbl 1 `"Blank (No)"', add
label define divinyr_lbl 2 `"Yes"', add
label define divinyr_lbl 8 `"Suppressed"', add
label values divinyr divinyr_lbl

label define widinyr_lbl 0 `"N/A"'
label define widinyr_lbl 1 `"Blank (No)"', add
label define widinyr_lbl 2 `"Yes"', add
label values widinyr widinyr_lbl

label define fertyr_lbl 0 `"N/A"'
label define fertyr_lbl 1 `"No"', add
label define fertyr_lbl 2 `"Yes"', add
label define fertyr_lbl 8 `"Suppressed"', add
label values fertyr fertyr_lbl

label define race_lbl 1 `"White"'
label define race_lbl 2 `"Black/African American"', add
label define race_lbl 3 `"American Indian or Alaska Native"', add
label define race_lbl 4 `"Chinese"', add
label define race_lbl 5 `"Japanese"', add
label define race_lbl 6 `"Other Asian or Pacific Islander"', add
label define race_lbl 7 `"Other race, nec"', add
label define race_lbl 8 `"Two major races"', add
label define race_lbl 9 `"Three or more major races"', add
label values race race_lbl

label define raced_lbl 100 `"White"'
label define raced_lbl 101 `"Albanian alone"', add
label define raced_lbl 102 `"Armenian alone"', add
label define raced_lbl 103 `"Austrian alone"', add
label define raced_lbl 104 `"Basque alone"', add
label define raced_lbl 105 `"Belarusian alone"', add
label define raced_lbl 106 `"Belgian alone"', add
label define raced_lbl 107 `"Bosnian and Herzegovinian alone"', add
label define raced_lbl 108 `"British alone"', add
label define raced_lbl 109 `"British Islander alone"', add
label define raced_lbl 110 `"Spanish write_in"', add
label define raced_lbl 111 `"Bulgarian alone"', add
label define raced_lbl 112 `"Celtic alone"', add
label define raced_lbl 113 `"Croatian alone"', add
label define raced_lbl 114 `"Czech alone"', add
label define raced_lbl 115 `"Danish alone"', add
label define raced_lbl 116 `"Dutch alone"', add
label define raced_lbl 117 `"English alone"', add
label define raced_lbl 118 `"Estonian alone"', add
label define raced_lbl 119 `"Finnish alone"', add
label define raced_lbl 120 `"Blank (white)"', add
label define raced_lbl 121 `"French alone"', add
label define raced_lbl 122 `"Georgian alone"', add
label define raced_lbl 123 `"German alone"', add
label define raced_lbl 124 `"Greek alone"', add
label define raced_lbl 125 `"Hungarian alone"', add
label define raced_lbl 126 `"Icelandic alone"', add
label define raced_lbl 127 `"Irish alone"', add
label define raced_lbl 128 `"Italian alone"', add
label define raced_lbl 129 `"Latvian alone"', add
label define raced_lbl 130 `"Portuguese"', add
label define raced_lbl 131 `"Lithuanian alone"', add
label define raced_lbl 132 `"Luxembourger alone"', add
label define raced_lbl 133 `"Macedonian alone"', add
label define raced_lbl 134 `"Maltese alone"', add
label define raced_lbl 135 `"Moldovan alone"', add
label define raced_lbl 136 `"Montenegrin alone"', add
label define raced_lbl 137 `"Norwegian alone"', add
label define raced_lbl 138 `"Polish alone"', add
label define raced_lbl 139 `"Romanian alone"', add
label define raced_lbl 140 `"Mexican (1930)"', add
label define raced_lbl 141 `"Russian alone"', add
label define raced_lbl 142 `"Scandinavian alone"', add
label define raced_lbl 143 `"Scots-Irish alone"', add
label define raced_lbl 144 `"Scottish alone"', add
label define raced_lbl 145 `"Serbian alone"', add
label define raced_lbl 146 `"Slavic alone"', add
label define raced_lbl 147 `"Slovak alone"', add
label define raced_lbl 148 `"Slovenian alone"', add
label define raced_lbl 149 `"Swedish alone"', add
label define raced_lbl 150 `"Puerto Rican"', add
label define raced_lbl 151 `"Swiss alone"', add
label define raced_lbl 152 `"Turkish alone"', add
label define raced_lbl 153 `"Ukrainian alone"', add
label define raced_lbl 154 `"Welsh alone"', add
label define raced_lbl 155 `"Algerian alone"', add
label define raced_lbl 156 `"Arab alone"', add
label define raced_lbl 157 `"Assyrian alone"', add
label define raced_lbl 158 `"Chaldean alone"', add
label define raced_lbl 159 `"Egyptian alone"', add
label define raced_lbl 160 `"Iranian alone"', add
label define raced_lbl 161 `"Iraqi alone"', add
label define raced_lbl 162 `"Israeli alone"', add
label define raced_lbl 163 `"Jordanian alone"', add
label define raced_lbl 164 `"Kurdish alone"', add
label define raced_lbl 165 `"Lebanese alone"', add
label define raced_lbl 166 `"Moroccan alone"', add
label define raced_lbl 167 `"Palestinian alone"', add
label define raced_lbl 168 `"Saudi alone"', add
label define raced_lbl 169 `"Syrian alone"', add
label define raced_lbl 170 `"Tunisian alone"', add
label define raced_lbl 171 `"Yemeni alone"', add
label define raced_lbl 172 `"Australian alone"', add
label define raced_lbl 173 `"Cajun alone"', add
label define raced_lbl 174 `"Canadian alone"', add
label define raced_lbl 175 `"French Canadian alone"', add
label define raced_lbl 176 `"Pennsylvania German alone"', add
label define raced_lbl 177 `"Other White alone"', add
label define raced_lbl 200 `"Black/African American"', add
label define raced_lbl 201 `"African American alone"', add
label define raced_lbl 202 `"Burundian alone"', add
label define raced_lbl 203 `"Cameroonian alone"', add
label define raced_lbl 204 `"Congolese alone"', add
label define raced_lbl 205 `"Eritrean alone"', add
label define raced_lbl 206 `"Ethiopian alone"', add
label define raced_lbl 207 `"Gambian alone"', add
label define raced_lbl 208 `"Ghanaian alone"', add
label define raced_lbl 209 `"Guinean alone"', add
label define raced_lbl 210 `"Mulatto"', add
label define raced_lbl 211 `"Ivoirian alone"', add
label define raced_lbl 212 `"Kenyan alone"', add
label define raced_lbl 213 `"Liberian alone"', add
label define raced_lbl 214 `"Nigerian (Nigeria) alone"', add
label define raced_lbl 215 `"Rwandan alone"', add
label define raced_lbl 216 `"Senegalese alone"', add
label define raced_lbl 217 `"Sierra Leonean alone"', add
label define raced_lbl 218 `"Somali alone"', add
label define raced_lbl 219 `"South African alone"', add
label define raced_lbl 220 `"South Sudanese alone"', add
label define raced_lbl 221 `"Sudanese alone"', add
label define raced_lbl 222 `"Tanzanian alone"', add
label define raced_lbl 223 `"Togolese alone"', add
label define raced_lbl 224 `"Ugandan alone"', add
label define raced_lbl 225 `"Zimbabwean alone"', add
label define raced_lbl 226 `"Bahamian alone"', add
label define raced_lbl 227 `"Barbadian alone"', add
label define raced_lbl 228 `"Grenadian alone"', add
label define raced_lbl 229 `"Haitian alone"', add
label define raced_lbl 230 `"Jamaican alone"', add
label define raced_lbl 231 `"St. Lucian alone"', add
label define raced_lbl 232 `"Trinidadian and Tobagonian alone"', add
label define raced_lbl 233 `"West Indian alone"', add
label define raced_lbl 234 `"Other Black or African American alone"', add
label define raced_lbl 300 `"American Indian/Alaska Native"', add
label define raced_lbl 302 `"Apache"', add
label define raced_lbl 303 `"Blackfoot"', add
label define raced_lbl 304 `"Cherokee"', add
label define raced_lbl 305 `"Cheyenne"', add
label define raced_lbl 306 `"Chickasaw"', add
label define raced_lbl 307 `"Chippewa"', add
label define raced_lbl 308 `"Choctaw"', add
label define raced_lbl 309 `"Comanche"', add
label define raced_lbl 310 `"Creek"', add
label define raced_lbl 311 `"Crow"', add
label define raced_lbl 312 `"Iroquois"', add
label define raced_lbl 313 `"Kiowa"', add
label define raced_lbl 314 `"Lumbee"', add
label define raced_lbl 315 `"Navajo"', add
label define raced_lbl 316 `"Osage"', add
label define raced_lbl 317 `"Paiute"', add
label define raced_lbl 318 `"Pima"', add
label define raced_lbl 319 `"Potawatomi"', add
label define raced_lbl 320 `"Pueblo"', add
label define raced_lbl 321 `"Seminole"', add
label define raced_lbl 322 `"Shoshone"', add
label define raced_lbl 323 `"Sioux"', add
label define raced_lbl 324 `"Tlingit (Tlingit_Haida, 2000/ACS)"', add
label define raced_lbl 325 `"Tohono O Odham"', add
label define raced_lbl 326 `"All other tribes (1990)"', add
label define raced_lbl 328 `"Hopi"', add
label define raced_lbl 329 `"Central American Indian"', add
label define raced_lbl 330 `"Spanish American Indian"', add
label define raced_lbl 340 `"Aztec"', add
label define raced_lbl 341 `"Inca"', add
label define raced_lbl 342 `"Maya"', add
label define raced_lbl 343 `"Mixtec"', add
label define raced_lbl 344 `"Taino"', add
label define raced_lbl 345 `"Tarasco (Purepecha)"', add
label define raced_lbl 350 `"Delaware"', add
label define raced_lbl 351 `"Latin American Indian"', add
label define raced_lbl 352 `"Puget Sound Salish"', add
label define raced_lbl 353 `"Yakama"', add
label define raced_lbl 354 `"Yaqui"', add
label define raced_lbl 355 `"Colville"', add
label define raced_lbl 356 `"Houma"', add
label define raced_lbl 357 `"Menominee"', add
label define raced_lbl 358 `"Yuman"', add
label define raced_lbl 359 `"South American Indian"', add
label define raced_lbl 360 `"Mexican American Indian"', add
label define raced_lbl 361 `"Other Amer. Indian tribe (2000,ACS)"', add
label define raced_lbl 362 `"2+ Amer. Indian tribes (2000,ACS)"', add
label define raced_lbl 363 `"American Indian alone, not specified"', add
label define raced_lbl 364 `"All other Latin American Indian alone"', add
label define raced_lbl 370 `"Alaskan Athabaskan"', add
label define raced_lbl 371 `"Aleut"', add
label define raced_lbl 372 `"Eskimo"', add
label define raced_lbl 373 `"Alaskan mixed"', add
label define raced_lbl 374 `"Inupiat"', add
label define raced_lbl 375 `"Yup'ik"', add
label define raced_lbl 379 `"Other Alaska Native tribe(s) (2000,ACS)"', add
label define raced_lbl 380 `"Alaska Native alone, not specified"', add
label define raced_lbl 381 `"Alaska Native tribes and villages alone"', add
label define raced_lbl 398 `"Both Am. Ind. and Alaska Native (2000,ACS)"', add
label define raced_lbl 399 `"Tribe not specified"', add
label define raced_lbl 400 `"Chinese"', add
label define raced_lbl 410 `"Taiwanese"', add
label define raced_lbl 420 `"Chinese and Taiwanese"', add
label define raced_lbl 500 `"Japanese"', add
label define raced_lbl 600 `"Filipino"', add
label define raced_lbl 610 `"Asian Indian (Hindu 1920_1940)"', add
label define raced_lbl 620 `"Korean"', add
label define raced_lbl 630 `"Hawaiian"', add
label define raced_lbl 631 `"Hawaiian and Asian (1900,1920)"', add
label define raced_lbl 632 `"Hawaiian and European (1900,1920)"', add
label define raced_lbl 634 `"Hawaiian mixed"', add
label define raced_lbl 640 `"Vietnamese"', add
label define raced_lbl 641 `"Bhutanese"', add
label define raced_lbl 642 `"Mongolian"', add
label define raced_lbl 643 `"Nepalese"', add
label define raced_lbl 650 `"Other Asian or Pacific Islander (1920,1980)"', add
label define raced_lbl 651 `"Asian only (CPS)"', add
label define raced_lbl 652 `"Pacific Islander only (CPS)"', add
label define raced_lbl 653 `"Asian or Pacific Islander, n.s. (1990 Internal Census files)"', add
label define raced_lbl 655 `"Afghan"', add
label define raced_lbl 656 `"Mien"', add
label define raced_lbl 657 `"Sikh"', add
label define raced_lbl 658 `"Kazakh"', add
label define raced_lbl 659 `"Uzbek"', add
label define raced_lbl 660 `"Cambodian"', add
label define raced_lbl 661 `"Hmong"', add
label define raced_lbl 662 `"Laotian"', add
label define raced_lbl 663 `"Thai"', add
label define raced_lbl 664 `"Bangladeshi"', add
label define raced_lbl 665 `"Burmese"', add
label define raced_lbl 666 `"Indonesian"', add
label define raced_lbl 667 `"Malaysian"', add
label define raced_lbl 668 `"Okinawan"', add
label define raced_lbl 669 `"Pakistani"', add
label define raced_lbl 670 `"Sri Lankan"', add
label define raced_lbl 671 `"Other Asian, n.e.c."', add
label define raced_lbl 672 `"Asian, not specified"', add
label define raced_lbl 673 `"Chinese and Japanese"', add
label define raced_lbl 674 `"Chinese and Filipino"', add
label define raced_lbl 675 `"Chinese and Vietnamese"', add
label define raced_lbl 676 `"Chinese and Asian write_in"', add
label define raced_lbl 677 `"Japanese and Filipino"', add
label define raced_lbl 678 `"Asian Indian and Asian write_in"', add
label define raced_lbl 679 `"Other Asian race combinations"', add
label define raced_lbl 680 `"Samoan"', add
label define raced_lbl 681 `"Tahitian"', add
label define raced_lbl 682 `"Tongan"', add
label define raced_lbl 683 `"Other Polynesian (1990)"', add
label define raced_lbl 684 `"1+ other Polynesian races (2000,ACS)"', add
label define raced_lbl 685 `"Chamorro"', add
label define raced_lbl 686 `"Northern Mariana Islander"', add
label define raced_lbl 687 `"Palauan"', add
label define raced_lbl 688 `"Other Micronesian (1990)"', add
label define raced_lbl 689 `"1+ other Micronesian races (2000,ACS)"', add
label define raced_lbl 690 `"Chuukese"', add
label define raced_lbl 691 `"Guamanian"', add
label define raced_lbl 692 `"Marshallese"', add
label define raced_lbl 695 `"Fijian"', add
label define raced_lbl 696 `"Other Melanesian (1990)"', add
label define raced_lbl 697 `"1+ other Melanesian races (2000,ACS)"', add
label define raced_lbl 698 `"2+ PI races from 2+ PI regions"', add
label define raced_lbl 699 `"Pacific Islander, n.s."', add
label define raced_lbl 700 `"Other race, n.e.c."', add
label define raced_lbl 710 `"Brazilian"', add
label define raced_lbl 720 `"Cabo Verdean"', add
label define raced_lbl 730 `"Guyanese"', add
label define raced_lbl 801 `"White and Black"', add
label define raced_lbl 802 `"White and AIAN"', add
label define raced_lbl 810 `"White and Asian"', add
label define raced_lbl 811 `"White and Chinese"', add
label define raced_lbl 812 `"White and Japanese"', add
label define raced_lbl 813 `"White and Filipino"', add
label define raced_lbl 814 `"White and Asian Indian"', add
label define raced_lbl 815 `"White and Korean"', add
label define raced_lbl 816 `"White and Vietnamese"', add
label define raced_lbl 817 `"White and Asian write_in"', add
label define raced_lbl 818 `"White and other Asian race(s)"', add
label define raced_lbl 819 `"White and two or more Asian groups"', add
label define raced_lbl 820 `"White and PI"', add
label define raced_lbl 821 `"White and Native Hawaiian"', add
label define raced_lbl 822 `"White and Samoan"', add
label define raced_lbl 823 `"White and Chamorro"', add
label define raced_lbl 824 `"White and PI write_in"', add
label define raced_lbl 825 `"White and other PI race(s)"', add
label define raced_lbl 826 `"White and other race write_in"', add
label define raced_lbl 827 `"White and other race, n.e.c."', add
label define raced_lbl 830 `"Black and AIAN"', add
label define raced_lbl 831 `"Black and Asian"', add
label define raced_lbl 832 `"Black and Chinese"', add
label define raced_lbl 833 `"Black and Japanese"', add
label define raced_lbl 834 `"Black and Filipino"', add
label define raced_lbl 835 `"Black and Asian Indian"', add
label define raced_lbl 836 `"Black and Korean"', add
label define raced_lbl 837 `"Black and Asian write_in"', add
label define raced_lbl 838 `"Black and other Asian race(s)"', add
label define raced_lbl 840 `"Black and PI"', add
label define raced_lbl 841 `"Black and PI write_in"', add
label define raced_lbl 842 `"Black and other PI race(s)"', add
label define raced_lbl 845 `"Black and other race write_in"', add
label define raced_lbl 850 `"AIAN and Asian"', add
label define raced_lbl 851 `"AIAN and Filipino (2000 1%)"', add
label define raced_lbl 852 `"AIAN and Asian Indian"', add
label define raced_lbl 853 `"AIAN and Asian write_in (2000 1%)"', add
label define raced_lbl 854 `"AIAN and other Asian race(s)"', add
label define raced_lbl 855 `"AIAN and PI"', add
label define raced_lbl 856 `"AIAN and other race write_in"', add
label define raced_lbl 860 `"Asian and PI"', add
label define raced_lbl 861 `"Chinese and Hawaiian"', add
label define raced_lbl 862 `"Chinese, Filipino, Hawaiian (2000 1%)"', add
label define raced_lbl 863 `"Japanese and Hawaiian (2000 1%)"', add
label define raced_lbl 864 `"Filipino and Hawaiian"', add
label define raced_lbl 865 `"Filipino and PI write_in"', add
label define raced_lbl 866 `"Asian Indian and PI write_in (2000 1%)"', add
label define raced_lbl 867 `"Asian write_in and PI write_in"', add
label define raced_lbl 868 `"Other Asian race(s) and PI race(s)"', add
label define raced_lbl 869 `"Japanese and Korean (ACS)"', add
label define raced_lbl 880 `"Asian and other race write_in"', add
label define raced_lbl 881 `"Chinese and other race write_in"', add
label define raced_lbl 882 `"Japanese and other race write_in"', add
label define raced_lbl 883 `"Filipino and other race write_in"', add
label define raced_lbl 884 `"Asian Indian and other race write_in"', add
label define raced_lbl 885 `"Asian write_in and other race write_in"', add
label define raced_lbl 886 `"Other Asian race(s) and other race write_in"', add
label define raced_lbl 887 `"Chinese and Korean"', add
label define raced_lbl 890 `"PI and other race write_in:"', add
label define raced_lbl 891 `"PI write_in and other race write_in"', add
label define raced_lbl 892 `"Other PI race(s) and other race write_in"', add
label define raced_lbl 893 `"Native Hawaiian or PI other race(s)"', add
label define raced_lbl 899 `"API and other race write_in"', add
label define raced_lbl 901 `"White, Black, AIAN"', add
label define raced_lbl 902 `"White, Black, Asian"', add
label define raced_lbl 903 `"White, Black, PI"', add
label define raced_lbl 904 `"White, Black, other race write_in"', add
label define raced_lbl 905 `"White, AIAN, Asian"', add
label define raced_lbl 906 `"White, AIAN, PI"', add
label define raced_lbl 907 `"White, AIAN, other race write_in"', add
label define raced_lbl 910 `"White, Asian, PI"', add
label define raced_lbl 911 `"White, Chinese, Hawaiian"', add
label define raced_lbl 912 `"White, Chinese, Filipino, Hawaiian (2000 1%)"', add
label define raced_lbl 913 `"White, Japanese, Hawaiian (2000 1%)"', add
label define raced_lbl 914 `"White, Filipino, Hawaiian"', add
label define raced_lbl 915 `"Other White, Asian race(s), PI race(s)"', add
label define raced_lbl 916 `"White, AIAN and Filipino"', add
label define raced_lbl 917 `"White, Black, and Filipino"', add
label define raced_lbl 920 `"White, Asian, other race write_in"', add
label define raced_lbl 921 `"White, Filipino, other race write_in (2000 1%)"', add
label define raced_lbl 922 `"White, Asian write_in, other race write_in (2000 1%)"', add
label define raced_lbl 923 `"Other White, Asian race(s), other race write_in (2000 1%)"', add
label define raced_lbl 925 `"White, PI, other race write_in"', add
label define raced_lbl 926 `"White and Japanese and Native Hawaiian and Pacific Islander"', add
label define raced_lbl 927 `"White and Asian and Native Hawaiian and Pacific Islander"', add
label define raced_lbl 930 `"Black, AIAN, Asian"', add
label define raced_lbl 931 `"Black, AIAN, PI"', add
label define raced_lbl 932 `"Black, AIAN, other race write_in"', add
label define raced_lbl 933 `"Black, Asian, PI"', add
label define raced_lbl 934 `"Black, Asian, other race write_in"', add
label define raced_lbl 935 `"Black, PI, other race write_in"', add
label define raced_lbl 936 `"Black and Native Hawaiian and Other Pacific Islander"', add
label define raced_lbl 940 `"AIAN, Asian, PI"', add
label define raced_lbl 941 `"AIAN, Asian, other race write_in"', add
label define raced_lbl 942 `"AIAN, PI, other race write_in"', add
label define raced_lbl 943 `"Asian, PI, other race write_in"', add
label define raced_lbl 944 `"Asian (Chinese, Japanese, Korean, Vietnamese); and Native Hawaiian or PI; and Other"', add
label define raced_lbl 949 `"2 or 3 races (CPS)"', add
label define raced_lbl 950 `"White, Black, AIAN, Asian"', add
label define raced_lbl 951 `"White, Black, AIAN, PI"', add
label define raced_lbl 952 `"White, Black, AIAN, other race write_in"', add
label define raced_lbl 953 `"White, Black, Asian, PI"', add
label define raced_lbl 954 `"White, Black, Asian, other race write_in"', add
label define raced_lbl 955 `"White, Black, PI, other race write_in"', add
label define raced_lbl 960 `"White, AIAN, Asian, PI"', add
label define raced_lbl 961 `"White, AIAN, Asian, other race write_in"', add
label define raced_lbl 962 `"White, AIAN, PI, other race write_in"', add
label define raced_lbl 963 `"White, Asian, PI, other race write_in"', add
label define raced_lbl 964 `"White, Chinese, Japanese, Native Hawaiian"', add
label define raced_lbl 970 `"Black, AIAN, Asian, PI"', add
label define raced_lbl 971 `"Black, AIAN, Asian, other race write_in"', add
label define raced_lbl 972 `"Black, AIAN, PI, other race write_in"', add
label define raced_lbl 973 `"Black, Asian, PI, other race write_in"', add
label define raced_lbl 974 `"AIAN, Asian, PI, other race write_in"', add
label define raced_lbl 975 `"AIAN, Asian, PI, Hawaiian other race write_in"', add
label define raced_lbl 976 `"Two specified Asian  (Chinese and other Asian, Chinese and Japanese, Japanese and other Asian, Korean and other Asian); Native Hawaiian/PI; and Other Race"', add
label define raced_lbl 980 `"White, Black, AIAN, Asian, PI"', add
label define raced_lbl 981 `"White, Black, AIAN, Asian, other race write_in"', add
label define raced_lbl 982 `"White, Black, AIAN, PI, other race write_in"', add
label define raced_lbl 983 `"White, Black, Asian, PI, other race write_in"', add
label define raced_lbl 984 `"White, AIAN, Asian, PI, other race write_in"', add
label define raced_lbl 985 `"Black, AIAN, Asian, PI, other race write_in"', add
label define raced_lbl 986 `"Black, AIAN, Asian, PI, Hawaiian, other race write_in"', add
label define raced_lbl 989 `"4 or 5 races (CPS)"', add
label define raced_lbl 990 `"White, Black, AIAN, Asian, PI, other race write_in"', add
label define raced_lbl 991 `"White race; Some other race; Black or African American race and/or American Indian and Alaska Native race and/or Asian groups and/or Native Hawaiian and Other Pacific Islander groups"', add
label define raced_lbl 996 `"2+ races, n.e.c. (CPS)"', add
label define raced_lbl 997 `"Unknown"', add
label values raced raced_lbl

label define hispan_lbl 0 `"Not Hispanic"'
label define hispan_lbl 1 `"Mexican"', add
label define hispan_lbl 2 `"Puerto Rican"', add
label define hispan_lbl 3 `"Cuban"', add
label define hispan_lbl 4 `"Other"', add
label define hispan_lbl 9 `"Not Reported"', add
label values hispan hispan_lbl

label define hispand_lbl 000 `"Not Hispanic"'
label define hispand_lbl 100 `"Mexican"', add
label define hispand_lbl 102 `"Mexican American"', add
label define hispand_lbl 103 `"Mexicano/Mexicana"', add
label define hispand_lbl 104 `"Chicano/Chicana"', add
label define hispand_lbl 105 `"La Raza"', add
label define hispand_lbl 106 `"Mexican American Indian"', add
label define hispand_lbl 107 `"Mexico"', add
label define hispand_lbl 200 `"Puerto Rican"', add
label define hispand_lbl 300 `"Cuban"', add
label define hispand_lbl 401 `"Central American Indian"', add
label define hispand_lbl 402 `"Canal Zone"', add
label define hispand_lbl 411 `"Costa Rican"', add
label define hispand_lbl 412 `"Guatemalan"', add
label define hispand_lbl 413 `"Honduran"', add
label define hispand_lbl 414 `"Nicaraguan"', add
label define hispand_lbl 415 `"Panamanian"', add
label define hispand_lbl 416 `"Salvadoran"', add
label define hispand_lbl 417 `"Central American, n.e.c."', add
label define hispand_lbl 420 `"Argentinean"', add
label define hispand_lbl 421 `"Bolivian"', add
label define hispand_lbl 422 `"Chilean"', add
label define hispand_lbl 423 `"Colombian"', add
label define hispand_lbl 424 `"Ecuadorian"', add
label define hispand_lbl 425 `"Paraguayan"', add
label define hispand_lbl 426 `"Peruvian"', add
label define hispand_lbl 427 `"Uruguayan"', add
label define hispand_lbl 428 `"Venezuelan"', add
label define hispand_lbl 429 `"South American Indian"', add
label define hispand_lbl 430 `"Criollo"', add
label define hispand_lbl 431 `"South American, n.e.c."', add
label define hispand_lbl 450 `"Spaniard"', add
label define hispand_lbl 451 `"Andalusian"', add
label define hispand_lbl 452 `"Asturian"', add
label define hispand_lbl 453 `"Castillian"', add
label define hispand_lbl 454 `"Catalonian"', add
label define hispand_lbl 455 `"Balearic Islander"', add
label define hispand_lbl 456 `"Gallego"', add
label define hispand_lbl 457 `"Valencian"', add
label define hispand_lbl 458 `"Canarian"', add
label define hispand_lbl 459 `"Spanish Basque"', add
label define hispand_lbl 460 `"Dominican"', add
label define hispand_lbl 465 `"Latin American"', add
label define hispand_lbl 470 `"Hispanic"', add
label define hispand_lbl 480 `"Spanish"', add
label define hispand_lbl 490 `"Californio"', add
label define hispand_lbl 491 `"Tejano"', add
label define hispand_lbl 492 `"Nuevo Mexicano"', add
label define hispand_lbl 493 `"Spanish American"', add
label define hispand_lbl 494 `"Spanish American Indian"', add
label define hispand_lbl 495 `"Meso American Indian"', add
label define hispand_lbl 496 `"Mestizo"', add
label define hispand_lbl 498 `"Other, n.s."', add
label define hispand_lbl 499 `"Other, n.e.c."', add
label define hispand_lbl 900 `"Not Reported"', add
label values hispand hispand_lbl

label define bpl_lbl 001 `"Alabama"'
label define bpl_lbl 002 `"Alaska"', add
label define bpl_lbl 004 `"Arizona"', add
label define bpl_lbl 005 `"Arkansas"', add
label define bpl_lbl 006 `"California"', add
label define bpl_lbl 008 `"Colorado"', add
label define bpl_lbl 009 `"Connecticut"', add
label define bpl_lbl 010 `"Delaware"', add
label define bpl_lbl 011 `"District of Columbia"', add
label define bpl_lbl 012 `"Florida"', add
label define bpl_lbl 013 `"Georgia"', add
label define bpl_lbl 015 `"Hawaii"', add
label define bpl_lbl 016 `"Idaho"', add
label define bpl_lbl 017 `"Illinois"', add
label define bpl_lbl 018 `"Indiana"', add
label define bpl_lbl 019 `"Iowa"', add
label define bpl_lbl 020 `"Kansas"', add
label define bpl_lbl 021 `"Kentucky"', add
label define bpl_lbl 022 `"Louisiana"', add
label define bpl_lbl 023 `"Maine"', add
label define bpl_lbl 024 `"Maryland"', add
label define bpl_lbl 025 `"Massachusetts"', add
label define bpl_lbl 026 `"Michigan"', add
label define bpl_lbl 027 `"Minnesota"', add
label define bpl_lbl 028 `"Mississippi"', add
label define bpl_lbl 029 `"Missouri"', add
label define bpl_lbl 030 `"Montana"', add
label define bpl_lbl 031 `"Nebraska"', add
label define bpl_lbl 032 `"Nevada"', add
label define bpl_lbl 033 `"New Hampshire"', add
label define bpl_lbl 034 `"New Jersey"', add
label define bpl_lbl 035 `"New Mexico"', add
label define bpl_lbl 036 `"New York"', add
label define bpl_lbl 037 `"North Carolina"', add
label define bpl_lbl 038 `"North Dakota"', add
label define bpl_lbl 039 `"Ohio"', add
label define bpl_lbl 040 `"Oklahoma"', add
label define bpl_lbl 041 `"Oregon"', add
label define bpl_lbl 042 `"Pennsylvania"', add
label define bpl_lbl 044 `"Rhode Island"', add
label define bpl_lbl 045 `"South Carolina"', add
label define bpl_lbl 046 `"South Dakota"', add
label define bpl_lbl 047 `"Tennessee"', add
label define bpl_lbl 048 `"Texas"', add
label define bpl_lbl 049 `"Utah"', add
label define bpl_lbl 050 `"Vermont"', add
label define bpl_lbl 051 `"Virginia"', add
label define bpl_lbl 053 `"Washington"', add
label define bpl_lbl 054 `"West Virginia"', add
label define bpl_lbl 055 `"Wisconsin"', add
label define bpl_lbl 056 `"Wyoming"', add
label define bpl_lbl 090 `"Native American"', add
label define bpl_lbl 099 `"United States, ns"', add
label define bpl_lbl 100 `"American Samoa"', add
label define bpl_lbl 105 `"Guam"', add
label define bpl_lbl 110 `"Puerto Rico"', add
label define bpl_lbl 115 `"U.S. Virgin Islands"', add
label define bpl_lbl 120 `"Other US Possessions"', add
label define bpl_lbl 150 `"Canada"', add
label define bpl_lbl 155 `"St. Pierre and Miquelon"', add
label define bpl_lbl 160 `"Atlantic Islands"', add
label define bpl_lbl 199 `"North America, ns"', add
label define bpl_lbl 200 `"Mexico"', add
label define bpl_lbl 210 `"Central America"', add
label define bpl_lbl 250 `"Cuba"', add
label define bpl_lbl 260 `"West Indies"', add
label define bpl_lbl 299 `"Americas, n.s."', add
label define bpl_lbl 300 `"SOUTH AMERICA"', add
label define bpl_lbl 400 `"Denmark"', add
label define bpl_lbl 401 `"Finland"', add
label define bpl_lbl 402 `"Iceland"', add
label define bpl_lbl 403 `"Lapland, n.s."', add
label define bpl_lbl 404 `"Norway"', add
label define bpl_lbl 405 `"Sweden"', add
label define bpl_lbl 410 `"England"', add
label define bpl_lbl 411 `"Scotland"', add
label define bpl_lbl 412 `"Wales"', add
label define bpl_lbl 413 `"United Kingdom, ns"', add
label define bpl_lbl 414 `"Ireland"', add
label define bpl_lbl 419 `"Northern Europe, ns"', add
label define bpl_lbl 420 `"Belgium"', add
label define bpl_lbl 421 `"France"', add
label define bpl_lbl 422 `"Liechtenstein"', add
label define bpl_lbl 423 `"Luxembourg"', add
label define bpl_lbl 424 `"Monaco"', add
label define bpl_lbl 425 `"Netherlands"', add
label define bpl_lbl 426 `"Switzerland"', add
label define bpl_lbl 429 `"Western Europe, ns"', add
label define bpl_lbl 430 `"Albania"', add
label define bpl_lbl 431 `"Andorra"', add
label define bpl_lbl 432 `"Gibraltar"', add
label define bpl_lbl 433 `"Greece"', add
label define bpl_lbl 434 `"Italy"', add
label define bpl_lbl 435 `"Malta"', add
label define bpl_lbl 436 `"Portugal"', add
label define bpl_lbl 437 `"San Marino"', add
label define bpl_lbl 438 `"Spain"', add
label define bpl_lbl 439 `"Vatican City"', add
label define bpl_lbl 440 `"Southern Europe, ns"', add
label define bpl_lbl 450 `"Austria"', add
label define bpl_lbl 451 `"Bulgaria"', add
label define bpl_lbl 452 `"Czechoslovakia"', add
label define bpl_lbl 453 `"Germany"', add
label define bpl_lbl 454 `"Hungary"', add
label define bpl_lbl 455 `"Poland"', add
label define bpl_lbl 456 `"Romania"', add
label define bpl_lbl 457 `"Yugoslavia"', add
label define bpl_lbl 458 `"Central Europe, ns"', add
label define bpl_lbl 459 `"Eastern Europe, ns"', add
label define bpl_lbl 460 `"Estonia"', add
label define bpl_lbl 461 `"Latvia"', add
label define bpl_lbl 462 `"Lithuania"', add
label define bpl_lbl 463 `"Baltic States, ns"', add
label define bpl_lbl 465 `"Other USSR/Russia"', add
label define bpl_lbl 499 `"Europe, ns"', add
label define bpl_lbl 500 `"China"', add
label define bpl_lbl 501 `"Japan"', add
label define bpl_lbl 502 `"Korea"', add
label define bpl_lbl 509 `"East Asia, ns"', add
label define bpl_lbl 510 `"Brunei"', add
label define bpl_lbl 511 `"Cambodia (Kampuchea)"', add
label define bpl_lbl 512 `"Indonesia"', add
label define bpl_lbl 513 `"Laos"', add
label define bpl_lbl 514 `"Malaysia"', add
label define bpl_lbl 515 `"Philippines"', add
label define bpl_lbl 516 `"Singapore"', add
label define bpl_lbl 517 `"Thailand"', add
label define bpl_lbl 518 `"Vietnam"', add
label define bpl_lbl 519 `"Southeast Asia, ns"', add
label define bpl_lbl 520 `"Afghanistan"', add
label define bpl_lbl 521 `"India"', add
label define bpl_lbl 522 `"Iran"', add
label define bpl_lbl 523 `"Maldives"', add
label define bpl_lbl 524 `"Nepal"', add
label define bpl_lbl 530 `"Bahrain"', add
label define bpl_lbl 531 `"Cyprus"', add
label define bpl_lbl 532 `"Iraq"', add
label define bpl_lbl 533 `"Iraq/Saudi Arabia"', add
label define bpl_lbl 534 `"Israel/Palestine"', add
label define bpl_lbl 535 `"Jordan"', add
label define bpl_lbl 536 `"Kuwait"', add
label define bpl_lbl 537 `"Lebanon"', add
label define bpl_lbl 538 `"Oman"', add
label define bpl_lbl 539 `"Qatar"', add
label define bpl_lbl 540 `"Saudi Arabia"', add
label define bpl_lbl 541 `"Syria"', add
label define bpl_lbl 542 `"Turkey"', add
label define bpl_lbl 543 `"United Arab Emirates"', add
label define bpl_lbl 544 `"Yemen Arab Republic (North)"', add
label define bpl_lbl 545 `"Yemen, PDR (South)"', add
label define bpl_lbl 546 `"Persian Gulf States, n.s."', add
label define bpl_lbl 547 `"Middle East, ns"', add
label define bpl_lbl 548 `"Southwest Asia, nec/ns"', add
label define bpl_lbl 549 `"Asia Minor, ns"', add
label define bpl_lbl 550 `"South Asia, nec"', add
label define bpl_lbl 599 `"Asia, nec/ns"', add
label define bpl_lbl 600 `"AFRICA"', add
label define bpl_lbl 700 `"Australia and New Zealand"', add
label define bpl_lbl 710 `"Pacific Islands"', add
label define bpl_lbl 800 `"Antarctica, ns/nec"', add
label define bpl_lbl 900 `"Abroad (unknown) or at sea"', add
label define bpl_lbl 950 `"Other n.e.c."', add
label define bpl_lbl 997 `"Unknown"', add
label define bpl_lbl 999 `"Missing/blank"', add
label values bpl bpl_lbl

label define bpld_lbl 00100 `"Alabama"'
label define bpld_lbl 00200 `"Alaska"', add
label define bpld_lbl 00400 `"Arizona"', add
label define bpld_lbl 00500 `"Arkansas"', add
label define bpld_lbl 00600 `"California"', add
label define bpld_lbl 00800 `"Colorado"', add
label define bpld_lbl 00810 `"Colorado Territory"', add
label define bpld_lbl 00900 `"Connecticut"', add
label define bpld_lbl 01000 `"Delaware"', add
label define bpld_lbl 01100 `"District of Columbia"', add
label define bpld_lbl 01200 `"Florida"', add
label define bpld_lbl 01300 `"Georgia"', add
label define bpld_lbl 01500 `"Hawaii"', add
label define bpld_lbl 01600 `"Idaho"', add
label define bpld_lbl 01610 `"Idaho Territory"', add
label define bpld_lbl 01700 `"Illinois"', add
label define bpld_lbl 01800 `"Indiana"', add
label define bpld_lbl 01900 `"Iowa"', add
label define bpld_lbl 02000 `"Kansas"', add
label define bpld_lbl 02100 `"Kentucky"', add
label define bpld_lbl 02200 `"Louisiana"', add
label define bpld_lbl 02300 `"Maine"', add
label define bpld_lbl 02400 `"Maryland"', add
label define bpld_lbl 02500 `"Massachusetts"', add
label define bpld_lbl 02600 `"Michigan"', add
label define bpld_lbl 02700 `"Minnesota"', add
label define bpld_lbl 02710 `"Minnesota Territory"', add
label define bpld_lbl 02800 `"Mississippi"', add
label define bpld_lbl 02900 `"Missouri"', add
label define bpld_lbl 03000 `"Montana"', add
label define bpld_lbl 03010 `"Montana Territory"', add
label define bpld_lbl 03100 `"Nebraska"', add
label define bpld_lbl 03110 `"Nebraska Territory"', add
label define bpld_lbl 03200 `"Nevada"', add
label define bpld_lbl 03210 `"Nevada Territory"', add
label define bpld_lbl 03300 `"New Hampshire"', add
label define bpld_lbl 03400 `"New Jersey"', add
label define bpld_lbl 03500 `"New Mexico"', add
label define bpld_lbl 03510 `"New Mexico Territory"', add
label define bpld_lbl 03600 `"New York"', add
label define bpld_lbl 03700 `"North Carolina"', add
label define bpld_lbl 03800 `"North Dakota"', add
label define bpld_lbl 03900 `"Ohio"', add
label define bpld_lbl 04000 `"Oklahoma"', add
label define bpld_lbl 04010 `"Indian Territory"', add
label define bpld_lbl 04100 `"Oregon"', add
label define bpld_lbl 04200 `"Pennsylvania"', add
label define bpld_lbl 04400 `"Rhode Island"', add
label define bpld_lbl 04500 `"South Carolina"', add
label define bpld_lbl 04600 `"South Dakota"', add
label define bpld_lbl 04610 `"Dakota Territory"', add
label define bpld_lbl 04700 `"Tennessee"', add
label define bpld_lbl 04800 `"Texas"', add
label define bpld_lbl 04900 `"Utah"', add
label define bpld_lbl 04910 `"Utah Territory"', add
label define bpld_lbl 05000 `"Vermont"', add
label define bpld_lbl 05100 `"Virginia"', add
label define bpld_lbl 05300 `"Washington"', add
label define bpld_lbl 05310 `"Washington Territory"', add
label define bpld_lbl 05400 `"West Virginia"', add
label define bpld_lbl 05500 `"Wisconsin"', add
label define bpld_lbl 05600 `"Wyoming"', add
label define bpld_lbl 05610 `"Wyoming Territory"', add
label define bpld_lbl 09000 `"Native American"', add
label define bpld_lbl 09900 `"United States, ns"', add
label define bpld_lbl 10000 `"American Samoa"', add
label define bpld_lbl 10010 `"Samoa, 1940-1950"', add
label define bpld_lbl 10500 `"Guam"', add
label define bpld_lbl 11000 `"Puerto Rico"', add
label define bpld_lbl 11500 `"U.S. Virgin Islands"', add
label define bpld_lbl 11510 `"St. Croix"', add
label define bpld_lbl 11520 `"St. John"', add
label define bpld_lbl 11530 `"St. Thomas"', add
label define bpld_lbl 12000 `"Other US Possessions:"', add
label define bpld_lbl 12010 `"Johnston Atoll"', add
label define bpld_lbl 12020 `"Midway Islands"', add
label define bpld_lbl 12030 `"Wake Island"', add
label define bpld_lbl 12040 `"Other US Caribbean Islands"', add
label define bpld_lbl 12041 `"Navassa Island"', add
label define bpld_lbl 12050 `"Other US Pacific Islands"', add
label define bpld_lbl 12051 `"Baker Island"', add
label define bpld_lbl 12052 `"Howland Island"', add
label define bpld_lbl 12053 `"Jarvis Island"', add
label define bpld_lbl 12054 `"Kingman Reef"', add
label define bpld_lbl 12055 `"Palmyra Atoll"', add
label define bpld_lbl 12056 `"Canton and Enderbury Island"', add
label define bpld_lbl 12090 `"US outlying areas, ns"', add
label define bpld_lbl 12091 `"US possessions, ns"', add
label define bpld_lbl 12092 `"US territory, ns"', add
label define bpld_lbl 15000 `"Canada"', add
label define bpld_lbl 15010 `"English Canada"', add
label define bpld_lbl 15011 `"British Columbia"', add
label define bpld_lbl 15013 `"Alberta"', add
label define bpld_lbl 15015 `"Saskatchewan"', add
label define bpld_lbl 15017 `"Northwest"', add
label define bpld_lbl 15019 `"Ruperts Land"', add
label define bpld_lbl 15020 `"Manitoba"', add
label define bpld_lbl 15021 `"Red River"', add
label define bpld_lbl 15030 `"Ontario/Upper Canada"', add
label define bpld_lbl 15031 `"Upper Canada"', add
label define bpld_lbl 15032 `"Canada West"', add
label define bpld_lbl 15040 `"New Brunswick"', add
label define bpld_lbl 15050 `"Nova Scotia"', add
label define bpld_lbl 15051 `"Cape Breton"', add
label define bpld_lbl 15052 `"Halifax"', add
label define bpld_lbl 15060 `"Prince Edward Island"', add
label define bpld_lbl 15070 `"Newfoundland"', add
label define bpld_lbl 15080 `"French Canada"', add
label define bpld_lbl 15081 `"Quebec"', add
label define bpld_lbl 15082 `"Lower Canada"', add
label define bpld_lbl 15083 `"Canada East"', add
label define bpld_lbl 15500 `"St. Pierre and Miquelon"', add
label define bpld_lbl 16000 `"Atlantic Islands"', add
label define bpld_lbl 16010 `"Bermuda"', add
label define bpld_lbl 16020 `"Cape Verde"', add
label define bpld_lbl 16030 `"Falkland Islands"', add
label define bpld_lbl 16040 `"Greenland"', add
label define bpld_lbl 16050 `"St. Helena and Ascension"', add
label define bpld_lbl 16060 `"Canary Islands"', add
label define bpld_lbl 19900 `"North America, ns"', add
label define bpld_lbl 20000 `"Mexico"', add
label define bpld_lbl 21000 `"Central America"', add
label define bpld_lbl 21010 `"Belize/British Honduras"', add
label define bpld_lbl 21020 `"Costa Rica"', add
label define bpld_lbl 21030 `"El Salvador"', add
label define bpld_lbl 21040 `"Guatemala"', add
label define bpld_lbl 21050 `"Honduras"', add
label define bpld_lbl 21060 `"Nicaragua"', add
label define bpld_lbl 21070 `"Panama"', add
label define bpld_lbl 21071 `"Canal Zone"', add
label define bpld_lbl 21090 `"Central America, ns"', add
label define bpld_lbl 25000 `"Cuba"', add
label define bpld_lbl 26000 `"West Indies"', add
label define bpld_lbl 26010 `"Dominican Republic"', add
label define bpld_lbl 26020 `"Haiti"', add
label define bpld_lbl 26030 `"Jamaica"', add
label define bpld_lbl 26040 `"British West Indies"', add
label define bpld_lbl 26041 `"Anguilla"', add
label define bpld_lbl 26042 `"Antigua-Barbuda"', add
label define bpld_lbl 26043 `"Bahamas"', add
label define bpld_lbl 26044 `"Barbados"', add
label define bpld_lbl 26045 `"British Virgin Islands"', add
label define bpld_lbl 26046 `"Anegada"', add
label define bpld_lbl 26047 `"Cooper"', add
label define bpld_lbl 26048 `"Jost Van Dyke"', add
label define bpld_lbl 26049 `"Peter"', add
label define bpld_lbl 26050 `"Tortola"', add
label define bpld_lbl 26051 `"Virgin Gorda"', add
label define bpld_lbl 26052 `"Br. Virgin Islands, ns"', add
label define bpld_lbl 26053 `"Cayman Islands"', add
label define bpld_lbl 26054 `"Dominica"', add
label define bpld_lbl 26055 `"Grenada"', add
label define bpld_lbl 26056 `"Montserrat"', add
label define bpld_lbl 26057 `"St. Kitts-Nevis"', add
label define bpld_lbl 26058 `"St. Lucia"', add
label define bpld_lbl 26059 `"St. Vincent"', add
label define bpld_lbl 26060 `"Trinidad and Tobago"', add
label define bpld_lbl 26061 `"Turks and Caicos"', add
label define bpld_lbl 26069 `"Br. Virgin Islands, ns"', add
label define bpld_lbl 26070 `"Other West Indies"', add
label define bpld_lbl 26071 `"Aruba"', add
label define bpld_lbl 26072 `"Netherlands Antilles"', add
label define bpld_lbl 26073 `"Bonaire"', add
label define bpld_lbl 26074 `"Curacao"', add
label define bpld_lbl 26075 `"Dutch St. Maarten"', add
label define bpld_lbl 26076 `"Saba"', add
label define bpld_lbl 26077 `"St. Eustatius"', add
label define bpld_lbl 26079 `"Dutch Caribbean, ns"', add
label define bpld_lbl 26080 `"French St. Maarten"', add
label define bpld_lbl 26081 `"Guadeloupe"', add
label define bpld_lbl 26082 `"Martinique"', add
label define bpld_lbl 26083 `"St. Barthelemy"', add
label define bpld_lbl 26089 `"French Caribbean, ns"', add
label define bpld_lbl 26090 `"Antilles, ns"', add
label define bpld_lbl 26091 `"Caribbean, ns"', add
label define bpld_lbl 26092 `"Latin America, ns"', add
label define bpld_lbl 26093 `"Leeward Islands, ns"', add
label define bpld_lbl 26094 `"West Indies, ns"', add
label define bpld_lbl 26095 `"Windward Islands, ns"', add
label define bpld_lbl 29900 `"Americas, ns"', add
label define bpld_lbl 30000 `"South America"', add
label define bpld_lbl 30005 `"Argentina"', add
label define bpld_lbl 30010 `"Bolivia"', add
label define bpld_lbl 30015 `"Brazil"', add
label define bpld_lbl 30020 `"Chile"', add
label define bpld_lbl 30025 `"Colombia"', add
label define bpld_lbl 30030 `"Ecuador"', add
label define bpld_lbl 30035 `"French Guiana"', add
label define bpld_lbl 30040 `"Guyana/British Guiana"', add
label define bpld_lbl 30045 `"Paraguay"', add
label define bpld_lbl 30050 `"Peru"', add
label define bpld_lbl 30055 `"Suriname"', add
label define bpld_lbl 30060 `"Uruguay"', add
label define bpld_lbl 30065 `"Venezuela"', add
label define bpld_lbl 30090 `"South America, ns"', add
label define bpld_lbl 30091 `"South and Central America, n.s."', add
label define bpld_lbl 40000 `"Denmark"', add
label define bpld_lbl 40010 `"Faeroe Islands"', add
label define bpld_lbl 40100 `"Finland"', add
label define bpld_lbl 40200 `"Iceland"', add
label define bpld_lbl 40300 `"Lapland, ns"', add
label define bpld_lbl 40400 `"Norway"', add
label define bpld_lbl 40410 `"Svalbard and Jan Meyen"', add
label define bpld_lbl 40411 `"Svalbard"', add
label define bpld_lbl 40412 `"Jan Meyen"', add
label define bpld_lbl 40500 `"Sweden"', add
label define bpld_lbl 41000 `"England"', add
label define bpld_lbl 41010 `"Channel Islands"', add
label define bpld_lbl 41011 `"Guernsey"', add
label define bpld_lbl 41012 `"Jersey"', add
label define bpld_lbl 41020 `"Isle of Man"', add
label define bpld_lbl 41100 `"Scotland"', add
label define bpld_lbl 41200 `"Wales"', add
label define bpld_lbl 41300 `"United Kingdom, ns"', add
label define bpld_lbl 41400 `"Ireland"', add
label define bpld_lbl 41410 `"Northern Ireland"', add
label define bpld_lbl 41900 `"Northern Europe, ns"', add
label define bpld_lbl 42000 `"Belgium"', add
label define bpld_lbl 42100 `"France"', add
label define bpld_lbl 42110 `"Alsace-Lorraine"', add
label define bpld_lbl 42111 `"Alsace"', add
label define bpld_lbl 42112 `"Lorraine"', add
label define bpld_lbl 42200 `"Liechtenstein"', add
label define bpld_lbl 42300 `"Luxembourg"', add
label define bpld_lbl 42400 `"Monaco"', add
label define bpld_lbl 42500 `"Netherlands"', add
label define bpld_lbl 42600 `"Switzerland"', add
label define bpld_lbl 42900 `"Western Europe, ns"', add
label define bpld_lbl 43000 `"Albania"', add
label define bpld_lbl 43100 `"Andorra"', add
label define bpld_lbl 43200 `"Gibraltar"', add
label define bpld_lbl 43300 `"Greece"', add
label define bpld_lbl 43310 `"Dodecanese Islands"', add
label define bpld_lbl 43320 `"Turkey Greece"', add
label define bpld_lbl 43330 `"Macedonia"', add
label define bpld_lbl 43400 `"Italy"', add
label define bpld_lbl 43500 `"Malta"', add
label define bpld_lbl 43600 `"Portugal"', add
label define bpld_lbl 43610 `"Azores"', add
label define bpld_lbl 43620 `"Madeira Islands"', add
label define bpld_lbl 43630 `"Cape Verde Islands"', add
label define bpld_lbl 43640 `"St. Miguel"', add
label define bpld_lbl 43700 `"San Marino"', add
label define bpld_lbl 43800 `"Spain"', add
label define bpld_lbl 43900 `"Vatican City"', add
label define bpld_lbl 44000 `"Southern Europe, ns"', add
label define bpld_lbl 45000 `"Austria"', add
label define bpld_lbl 45010 `"Austria-Hungary"', add
label define bpld_lbl 45020 `"Austria-Graz"', add
label define bpld_lbl 45030 `"Austria-Linz"', add
label define bpld_lbl 45040 `"Austria-Salzburg"', add
label define bpld_lbl 45050 `"Austria-Tyrol"', add
label define bpld_lbl 45060 `"Austria-Vienna"', add
label define bpld_lbl 45070 `"Austria-Kaernsten"', add
label define bpld_lbl 45080 `"Austria-Neustadt"', add
label define bpld_lbl 45100 `"Bulgaria"', add
label define bpld_lbl 45200 `"Czechoslovakia"', add
label define bpld_lbl 45210 `"Bohemia"', add
label define bpld_lbl 45211 `"Bohemia-Moravia"', add
label define bpld_lbl 45212 `"Slovakia"', add
label define bpld_lbl 45213 `"Czech Republic"', add
label define bpld_lbl 45300 `"Germany"', add
label define bpld_lbl 45301 `"Berlin"', add
label define bpld_lbl 45302 `"West Berlin"', add
label define bpld_lbl 45303 `"East Berlin"', add
label define bpld_lbl 45310 `"West Germany"', add
label define bpld_lbl 45311 `"Baden"', add
label define bpld_lbl 45312 `"Bavaria"', add
label define bpld_lbl 45313 `"Braunschweig"', add
label define bpld_lbl 45314 `"Bremen"', add
label define bpld_lbl 45315 `"Hamburg"', add
label define bpld_lbl 45316 `"Hanover"', add
label define bpld_lbl 45317 `"Hessen"', add
label define bpld_lbl 45318 `"Hesse-Nassau"', add
label define bpld_lbl 45319 `"Lippe"', add
label define bpld_lbl 45320 `"Lubeck"', add
label define bpld_lbl 45321 `"Oldenburg"', add
label define bpld_lbl 45322 `"Rheinland"', add
label define bpld_lbl 45323 `"Schaumburg-Lippe"', add
label define bpld_lbl 45324 `"Schleswig"', add
label define bpld_lbl 45325 `"Sigmaringen"', add
label define bpld_lbl 45326 `"Schwarzburg"', add
label define bpld_lbl 45327 `"Westphalia"', add
label define bpld_lbl 45328 `"Wurttemberg"', add
label define bpld_lbl 45329 `"Waldeck"', add
label define bpld_lbl 45330 `"Wittenberg"', add
label define bpld_lbl 45331 `"Frankfurt"', add
label define bpld_lbl 45332 `"Saarland"', add
label define bpld_lbl 45333 `"Nordrhein-Westfalen"', add
label define bpld_lbl 45340 `"East Germany"', add
label define bpld_lbl 45341 `"Anhalt"', add
label define bpld_lbl 45342 `"Brandenburg"', add
label define bpld_lbl 45344 `"Kingdom of Saxony"', add
label define bpld_lbl 45345 `"Mecklenburg"', add
label define bpld_lbl 45346 `"Saxony"', add
label define bpld_lbl 45347 `"Thuringian States"', add
label define bpld_lbl 45348 `"Sachsen-Meiningen"', add
label define bpld_lbl 45349 `"Sachsen-Weimar-Eisenach"', add
label define bpld_lbl 45350 `"Probable Saxony"', add
label define bpld_lbl 45351 `"Schwerin"', add
label define bpld_lbl 45352 `"Strelitz"', add
label define bpld_lbl 45353 `"Probably Thuringian States"', add
label define bpld_lbl 45360 `"Prussia, nec"', add
label define bpld_lbl 45361 `"Hohenzollern"', add
label define bpld_lbl 45362 `"Niedersachsen"', add
label define bpld_lbl 45400 `"Hungary"', add
label define bpld_lbl 45500 `"Poland"', add
label define bpld_lbl 45510 `"Austrian Poland"', add
label define bpld_lbl 45511 `"Galicia"', add
label define bpld_lbl 45520 `"German Poland"', add
label define bpld_lbl 45521 `"East Prussia"', add
label define bpld_lbl 45522 `"Pomerania"', add
label define bpld_lbl 45523 `"Posen"', add
label define bpld_lbl 45524 `"Prussian Poland"', add
label define bpld_lbl 45525 `"Silesia"', add
label define bpld_lbl 45526 `"West Prussia"', add
label define bpld_lbl 45530 `"Russian Poland"', add
label define bpld_lbl 45600 `"Romania"', add
label define bpld_lbl 45610 `"Transylvania"', add
label define bpld_lbl 45700 `"Yugoslavia"', add
label define bpld_lbl 45710 `"Croatia"', add
label define bpld_lbl 45720 `"Montenegro"', add
label define bpld_lbl 45730 `"Serbia"', add
label define bpld_lbl 45740 `"Bosnia"', add
label define bpld_lbl 45750 `"Dalmatia"', add
label define bpld_lbl 45760 `"Slovonia"', add
label define bpld_lbl 45770 `"Carniola"', add
label define bpld_lbl 45780 `"Slovenia"', add
label define bpld_lbl 45790 `"Kosovo"', add
label define bpld_lbl 45800 `"Central Europe, ns"', add
label define bpld_lbl 45900 `"Eastern Europe, ns"', add
label define bpld_lbl 46000 `"Estonia"', add
label define bpld_lbl 46100 `"Latvia"', add
label define bpld_lbl 46200 `"Lithuania"', add
label define bpld_lbl 46300 `"Baltic States, ns"', add
label define bpld_lbl 46500 `"Other USSR/Russia"', add
label define bpld_lbl 46510 `"Byelorussia"', add
label define bpld_lbl 46520 `"Moldavia"', add
label define bpld_lbl 46521 `"Bessarabia"', add
label define bpld_lbl 46530 `"Ukraine"', add
label define bpld_lbl 46540 `"Armenia"', add
label define bpld_lbl 46541 `"Azerbaijan"', add
label define bpld_lbl 46542 `"Republic of Georgia"', add
label define bpld_lbl 46543 `"Kazakhstan"', add
label define bpld_lbl 46544 `"Kirghizia"', add
label define bpld_lbl 46545 `"Tadzhik"', add
label define bpld_lbl 46546 `"Turkmenistan"', add
label define bpld_lbl 46547 `"Uzbekistan"', add
label define bpld_lbl 46548 `"Siberia"', add
label define bpld_lbl 46590 `"USSR, ns"', add
label define bpld_lbl 49900 `"Europe, ns."', add
label define bpld_lbl 50000 `"China"', add
label define bpld_lbl 50010 `"Hong Kong"', add
label define bpld_lbl 50020 `"Macau"', add
label define bpld_lbl 50030 `"Mongolia"', add
label define bpld_lbl 50040 `"Taiwan"', add
label define bpld_lbl 50100 `"Japan"', add
label define bpld_lbl 50200 `"Korea"', add
label define bpld_lbl 50210 `"North Korea"', add
label define bpld_lbl 50220 `"South Korea"', add
label define bpld_lbl 50900 `"East Asia, ns"', add
label define bpld_lbl 51000 `"Brunei"', add
label define bpld_lbl 51100 `"Cambodia (Kampuchea)"', add
label define bpld_lbl 51200 `"Indonesia"', add
label define bpld_lbl 51210 `"East Indies"', add
label define bpld_lbl 51220 `"East Timor"', add
label define bpld_lbl 51300 `"Laos"', add
label define bpld_lbl 51400 `"Malaysia"', add
label define bpld_lbl 51500 `"Philippines"', add
label define bpld_lbl 51600 `"Singapore"', add
label define bpld_lbl 51700 `"Thailand"', add
label define bpld_lbl 51800 `"Vietnam"', add
label define bpld_lbl 51900 `"Southeast Asia, ns"', add
label define bpld_lbl 51910 `"Indochina, ns"', add
label define bpld_lbl 52000 `"Afghanistan"', add
label define bpld_lbl 52100 `"India"', add
label define bpld_lbl 52110 `"Bangladesh"', add
label define bpld_lbl 52120 `"Bhutan"', add
label define bpld_lbl 52130 `"Burma (Myanmar)"', add
label define bpld_lbl 52140 `"Pakistan"', add
label define bpld_lbl 52150 `"Sri Lanka (Ceylon)"', add
label define bpld_lbl 52200 `"Iran"', add
label define bpld_lbl 52300 `"Maldives"', add
label define bpld_lbl 52400 `"Nepal"', add
label define bpld_lbl 53000 `"Bahrain"', add
label define bpld_lbl 53100 `"Cyprus"', add
label define bpld_lbl 53200 `"Iraq"', add
label define bpld_lbl 53210 `"Mesopotamia"', add
label define bpld_lbl 53300 `"Iraq/Saudi Arabia"', add
label define bpld_lbl 53400 `"Israel/Palestine"', add
label define bpld_lbl 53410 `"Gaza Strip"', add
label define bpld_lbl 53420 `"Palestine"', add
label define bpld_lbl 53430 `"West Bank"', add
label define bpld_lbl 53440 `"Israel"', add
label define bpld_lbl 53500 `"Jordan"', add
label define bpld_lbl 53600 `"Kuwait"', add
label define bpld_lbl 53700 `"Lebanon"', add
label define bpld_lbl 53800 `"Oman"', add
label define bpld_lbl 53900 `"Qatar"', add
label define bpld_lbl 54000 `"Saudi Arabia"', add
label define bpld_lbl 54100 `"Syria"', add
label define bpld_lbl 54200 `"Turkey"', add
label define bpld_lbl 54210 `"European Turkey"', add
label define bpld_lbl 54220 `"Asian Turkey"', add
label define bpld_lbl 54300 `"United Arab Emirates"', add
label define bpld_lbl 54400 `"Yemen Arab Republic (North)"', add
label define bpld_lbl 54500 `"Yemen, PDR (South)"', add
label define bpld_lbl 54600 `"Persian Gulf States, ns"', add
label define bpld_lbl 54700 `"Middle East, ns"', add
label define bpld_lbl 54800 `"Southwest Asia, nec/ns"', add
label define bpld_lbl 54900 `"Asia Minor, ns"', add
label define bpld_lbl 55000 `"South Asia, nec"', add
label define bpld_lbl 59900 `"Asia, nec/ns"', add
label define bpld_lbl 60000 `"Africa"', add
label define bpld_lbl 60010 `"Northern Africa"', add
label define bpld_lbl 60011 `"Algeria"', add
label define bpld_lbl 60012 `"Egypt/United Arab Rep."', add
label define bpld_lbl 60013 `"Libya"', add
label define bpld_lbl 60014 `"Morocco"', add
label define bpld_lbl 60015 `"Sudan"', add
label define bpld_lbl 60016 `"Tunisia"', add
label define bpld_lbl 60017 `"Western Sahara"', add
label define bpld_lbl 60019 `"North Africa, ns"', add
label define bpld_lbl 60020 `"Benin"', add
label define bpld_lbl 60021 `"Burkina Faso"', add
label define bpld_lbl 60022 `"Gambia"', add
label define bpld_lbl 60023 `"Ghana"', add
label define bpld_lbl 60024 `"Guinea"', add
label define bpld_lbl 60025 `"Guinea-Bissau"', add
label define bpld_lbl 60026 `"Ivory Coast"', add
label define bpld_lbl 60027 `"Liberia"', add
label define bpld_lbl 60028 `"Mali"', add
label define bpld_lbl 60029 `"Mauritania"', add
label define bpld_lbl 60030 `"Niger"', add
label define bpld_lbl 60031 `"Nigeria"', add
label define bpld_lbl 60032 `"Senegal"', add
label define bpld_lbl 60033 `"Sierra Leone"', add
label define bpld_lbl 60034 `"Togo"', add
label define bpld_lbl 60038 `"Western Africa, ns"', add
label define bpld_lbl 60039 `"French West Africa, ns"', add
label define bpld_lbl 60040 `"British Indian Ocean Territory"', add
label define bpld_lbl 60041 `"Burundi"', add
label define bpld_lbl 60042 `"Comoros"', add
label define bpld_lbl 60043 `"Djibouti"', add
label define bpld_lbl 60044 `"Ethiopia"', add
label define bpld_lbl 60045 `"Kenya"', add
label define bpld_lbl 60046 `"Madagascar"', add
label define bpld_lbl 60047 `"Malawi"', add
label define bpld_lbl 60048 `"Mauritius"', add
label define bpld_lbl 60049 `"Mozambique"', add
label define bpld_lbl 60050 `"Reunion"', add
label define bpld_lbl 60051 `"Rwanda"', add
label define bpld_lbl 60052 `"Seychelles"', add
label define bpld_lbl 60053 `"Somalia"', add
label define bpld_lbl 60054 `"Tanzania"', add
label define bpld_lbl 60055 `"Uganda"', add
label define bpld_lbl 60056 `"Zambia"', add
label define bpld_lbl 60057 `"Zimbabwe"', add
label define bpld_lbl 60058 `"Bassas de India"', add
label define bpld_lbl 60059 `"Europa"', add
label define bpld_lbl 60060 `"Gloriosos"', add
label define bpld_lbl 60061 `"Juan de Nova"', add
label define bpld_lbl 60062 `"Mayotte"', add
label define bpld_lbl 60063 `"Tromelin"', add
label define bpld_lbl 60064 `"Eastern Africa, nec/ns"', add
label define bpld_lbl 60065 `"Eritrea"', add
label define bpld_lbl 60066 `"South Sudan"', add
label define bpld_lbl 60070 `"Central Africa"', add
label define bpld_lbl 60071 `"Angola"', add
label define bpld_lbl 60072 `"Cameroon"', add
label define bpld_lbl 60073 `"Central African Republic"', add
label define bpld_lbl 60074 `"Chad"', add
label define bpld_lbl 60075 `"Congo"', add
label define bpld_lbl 60076 `"Equatorial Guinea"', add
label define bpld_lbl 60077 `"Gabon"', add
label define bpld_lbl 60078 `"Sao Tome and Principe"', add
label define bpld_lbl 60079 `"Zaire"', add
label define bpld_lbl 60080 `"Central Africa, ns"', add
label define bpld_lbl 60081 `"Equatorial Africa, ns"', add
label define bpld_lbl 60082 `"French Equatorial Africa, ns"', add
label define bpld_lbl 60090 `"Southern Africa"', add
label define bpld_lbl 60091 `"Botswana"', add
label define bpld_lbl 60092 `"Lesotho"', add
label define bpld_lbl 60093 `"Namibia"', add
label define bpld_lbl 60094 `"South Africa (Union of)"', add
label define bpld_lbl 60095 `"Swaziland"', add
label define bpld_lbl 60096 `"Southern Africa, ns"', add
label define bpld_lbl 60099 `"Africa, ns/nec"', add
label define bpld_lbl 70000 `"Australia and New Zealand"', add
label define bpld_lbl 70010 `"Australia"', add
label define bpld_lbl 70011 `"Ashmore and Cartier Islands"', add
label define bpld_lbl 70012 `"Coral Sea Islands Territory"', add
label define bpld_lbl 70013 `"Christmas Island"', add
label define bpld_lbl 70014 `"Cocos Islands"', add
label define bpld_lbl 70020 `"New Zealand"', add
label define bpld_lbl 71000 `"Pacific Islands"', add
label define bpld_lbl 71010 `"New Caledonia"', add
label define bpld_lbl 71012 `"Papua New Guinea"', add
label define bpld_lbl 71013 `"Solomon Islands"', add
label define bpld_lbl 71014 `"Vanuatu (New Hebrides)"', add
label define bpld_lbl 71015 `"Fiji"', add
label define bpld_lbl 71016 `"Melanesia, ns"', add
label define bpld_lbl 71017 `"Norfolk Islands"', add
label define bpld_lbl 71018 `"Niue"', add
label define bpld_lbl 71020 `"Cook Islands"', add
label define bpld_lbl 71022 `"French Polynesia"', add
label define bpld_lbl 71023 `"Tonga"', add
label define bpld_lbl 71024 `"Wallis and Futuna Islands"', add
label define bpld_lbl 71025 `"Western Samoa"', add
label define bpld_lbl 71026 `"Pitcairn Island"', add
label define bpld_lbl 71027 `"Tokelau"', add
label define bpld_lbl 71028 `"Tuvalu"', add
label define bpld_lbl 71029 `"Polynesia, ns"', add
label define bpld_lbl 71032 `"Kiribati"', add
label define bpld_lbl 71033 `"Canton and Enderbury"', add
label define bpld_lbl 71034 `"Nauru"', add
label define bpld_lbl 71039 `"Micronesia, ns"', add
label define bpld_lbl 71040 `"US Pacific Trust Territories"', add
label define bpld_lbl 71041 `"Marshall Islands"', add
label define bpld_lbl 71042 `"Micronesia"', add
label define bpld_lbl 71043 `"Kosrae"', add
label define bpld_lbl 71044 `"Pohnpei"', add
label define bpld_lbl 71045 `"Truk"', add
label define bpld_lbl 71046 `"Yap"', add
label define bpld_lbl 71047 `"Northern Mariana Islands"', add
label define bpld_lbl 71048 `"Palau"', add
label define bpld_lbl 71049 `"Pacific Trust Terr, ns"', add
label define bpld_lbl 71050 `"Clipperton Island"', add
label define bpld_lbl 71090 `"Oceania, ns/nec"', add
label define bpld_lbl 80000 `"Antarctica, ns/nec"', add
label define bpld_lbl 80010 `"Bouvet Islands"', add
label define bpld_lbl 80020 `"British Antarctic Terr."', add
label define bpld_lbl 80030 `"Dronning Maud Land"', add
label define bpld_lbl 80040 `"French Southern and Antarctic Lands"', add
label define bpld_lbl 80050 `"Heard and McDonald Islands"', add
label define bpld_lbl 90000 `"Abroad (unknown) or at sea"', add
label define bpld_lbl 90010 `"Abroad, ns"', add
label define bpld_lbl 90011 `"Abroad (US citizen)"', add
label define bpld_lbl 90020 `"At sea"', add
label define bpld_lbl 90021 `"At sea (US citizen)"', add
label define bpld_lbl 90022 `"At sea or abroad (U.S. citizen)"', add
label define bpld_lbl 95000 `"Other n.e.c."', add
label define bpld_lbl 99700 `"Unknown"', add
label define bpld_lbl 99900 `"Missing/blank"', add
label values bpld bpld_lbl

label define ancestr1_lbl 001 `"Alsatian, Alsace-Lorraine"'
label define ancestr1_lbl 002 `"Andorran"', add
label define ancestr1_lbl 003 `"Austrian"', add
label define ancestr1_lbl 004 `"Tirolean"', add
label define ancestr1_lbl 005 `"Basque"', add
label define ancestr1_lbl 006 `"French Basque"', add
label define ancestr1_lbl 008 `"Belgian"', add
label define ancestr1_lbl 009 `"Flemish"', add
label define ancestr1_lbl 010 `"Walloon"', add
label define ancestr1_lbl 011 `"British"', add
label define ancestr1_lbl 012 `"British Isles"', add
label define ancestr1_lbl 013 `"Channel Islander"', add
label define ancestr1_lbl 014 `"Gibraltan"', add
label define ancestr1_lbl 015 `"Cornish"', add
label define ancestr1_lbl 016 `"Corsican"', add
label define ancestr1_lbl 017 `"Cypriot"', add
label define ancestr1_lbl 018 `"Greek Cypriote"', add
label define ancestr1_lbl 019 `"Turkish Cypriote"', add
label define ancestr1_lbl 020 `"Danish"', add
label define ancestr1_lbl 021 `"Dutch"', add
label define ancestr1_lbl 022 `"English"', add
label define ancestr1_lbl 023 `"Faeroe Islander"', add
label define ancestr1_lbl 024 `"Finnish"', add
label define ancestr1_lbl 025 `"Karelian"', add
label define ancestr1_lbl 026 `"French"', add
label define ancestr1_lbl 027 `"Lorrainian"', add
label define ancestr1_lbl 028 `"Breton"', add
label define ancestr1_lbl 029 `"Frisian"', add
label define ancestr1_lbl 030 `"Friulian"', add
label define ancestr1_lbl 032 `"German"', add
label define ancestr1_lbl 033 `"Bavarian"', add
label define ancestr1_lbl 034 `"Berliner"', add
label define ancestr1_lbl 035 `"Hamburger"', add
label define ancestr1_lbl 036 `"Hanoverian"', add
label define ancestr1_lbl 037 `"Hessian"', add
label define ancestr1_lbl 038 `"Lubecker"', add
label define ancestr1_lbl 039 `"Pomeranian"', add
label define ancestr1_lbl 040 `"Prussian"', add
label define ancestr1_lbl 041 `"Saxon"', add
label define ancestr1_lbl 042 `"Sudetenlander"', add
label define ancestr1_lbl 043 `"Westphalian"', add
label define ancestr1_lbl 046 `"Greek"', add
label define ancestr1_lbl 047 `"Cretan"', add
label define ancestr1_lbl 048 `"Cycladic Islander, Dodecanese Islander, Peloponnesian"', add
label define ancestr1_lbl 049 `"Icelander"', add
label define ancestr1_lbl 050 `"Irish, various subheads,"', add
label define ancestr1_lbl 051 `"Italian"', add
label define ancestr1_lbl 053 `"Abruzzi"', add
label define ancestr1_lbl 054 `"Apulian"', add
label define ancestr1_lbl 055 `"Basilicata"', add
label define ancestr1_lbl 056 `"Calabrian"', add
label define ancestr1_lbl 057 `"Amalfin"', add
label define ancestr1_lbl 058 `"Emilia Romagna"', add
label define ancestr1_lbl 059 `"Rome"', add
label define ancestr1_lbl 060 `"Ligurian"', add
label define ancestr1_lbl 061 `"Lombardian"', add
label define ancestr1_lbl 062 `"Marches"', add
label define ancestr1_lbl 063 `"Molise"', add
label define ancestr1_lbl 064 `"Neapolitan"', add
label define ancestr1_lbl 065 `"Piedmontese"', add
label define ancestr1_lbl 066 `"Puglia"', add
label define ancestr1_lbl 067 `"Sardinian"', add
label define ancestr1_lbl 068 `"Sicilian"', add
label define ancestr1_lbl 069 `"Tuscan"', add
label define ancestr1_lbl 070 `"Trentino"', add
label define ancestr1_lbl 071 `"Umbrian"', add
label define ancestr1_lbl 072 `"Valle dAosta"', add
label define ancestr1_lbl 073 `"Venetian"', add
label define ancestr1_lbl 075 `"Lapp"', add
label define ancestr1_lbl 076 `"Liechtensteiner"', add
label define ancestr1_lbl 077 `"Luxemburger"', add
label define ancestr1_lbl 078 `"Maltese"', add
label define ancestr1_lbl 079 `"Manx"', add
label define ancestr1_lbl 080 `"Monegasque"', add
label define ancestr1_lbl 081 `"Northern Irelander"', add
label define ancestr1_lbl 082 `"Norwegian"', add
label define ancestr1_lbl 084 `"Portuguese"', add
label define ancestr1_lbl 085 `"Azorean"', add
label define ancestr1_lbl 086 `"Madeiran"', add
label define ancestr1_lbl 087 `"Scotch Irish"', add
label define ancestr1_lbl 088 `"Scottish"', add
label define ancestr1_lbl 089 `"Swedish"', add
label define ancestr1_lbl 090 `"Aland Islander"', add
label define ancestr1_lbl 091 `"Swiss"', add
label define ancestr1_lbl 092 `"Suisse"', add
label define ancestr1_lbl 095 `"Romansch"', add
label define ancestr1_lbl 096 `"Suisse Romane"', add
label define ancestr1_lbl 097 `"Welsh"', add
label define ancestr1_lbl 098 `"Scandinavian, Nordic"', add
label define ancestr1_lbl 100 `"Albanian"', add
label define ancestr1_lbl 101 `"Azerbaijani"', add
label define ancestr1_lbl 102 `"Belorussian"', add
label define ancestr1_lbl 103 `"Bulgarian"', add
label define ancestr1_lbl 105 `"Carpathian"', add
label define ancestr1_lbl 108 `"Cossack"', add
label define ancestr1_lbl 109 `"Croatian"', add
label define ancestr1_lbl 111 `"Czechoslovakian"', add
label define ancestr1_lbl 112 `"Bohemian"', add
label define ancestr1_lbl 115 `"Estonian"', add
label define ancestr1_lbl 116 `"Livonian"', add
label define ancestr1_lbl 117 `"Finno Ugrian"', add
label define ancestr1_lbl 118 `"Mordovian"', add
label define ancestr1_lbl 119 `"Voytak"', add
label define ancestr1_lbl 120 `"Georgian"', add
label define ancestr1_lbl 122 `"Germans from Russia"', add
label define ancestr1_lbl 123 `"Gruziia"', add
label define ancestr1_lbl 124 `"Rom"', add
label define ancestr1_lbl 125 `"Hungarian"', add
label define ancestr1_lbl 126 `"Magyar"', add
label define ancestr1_lbl 128 `"Latvian"', add
label define ancestr1_lbl 129 `"Lithuanian"', add
label define ancestr1_lbl 130 `"Macedonian"', add
label define ancestr1_lbl 132 `"North Caucasian"', add
label define ancestr1_lbl 133 `"North Caucasian Turkic"', add
label define ancestr1_lbl 140 `"Ossetian"', add
label define ancestr1_lbl 142 `"Polish"', add
label define ancestr1_lbl 143 `"Kashubian"', add
label define ancestr1_lbl 144 `"Romanian"', add
label define ancestr1_lbl 145 `"Bessarabian"', add
label define ancestr1_lbl 146 `"Moldavian"', add
label define ancestr1_lbl 147 `"Wallachian"', add
label define ancestr1_lbl 148 `"Russian"', add
label define ancestr1_lbl 150 `"Muscovite"', add
label define ancestr1_lbl 152 `"Serbian"', add
label define ancestr1_lbl 153 `"Slovak"', add
label define ancestr1_lbl 154 `"Slovene"', add
label define ancestr1_lbl 155 `"Sorb/Wend"', add
label define ancestr1_lbl 156 `"Soviet Turkic"', add
label define ancestr1_lbl 157 `"Bashkir"', add
label define ancestr1_lbl 158 `"Chevash"', add
label define ancestr1_lbl 159 `"Gagauz"', add
label define ancestr1_lbl 160 `"Mesknetian"', add
label define ancestr1_lbl 163 `"Yakut"', add
label define ancestr1_lbl 164 `"Soviet Union, nec"', add
label define ancestr1_lbl 165 `"Tatar"', add
label define ancestr1_lbl 169 `"Uzbek"', add
label define ancestr1_lbl 171 `"Ukrainian"', add
label define ancestr1_lbl 176 `"Yugoslavian"', add
label define ancestr1_lbl 178 `"Slav"', add
label define ancestr1_lbl 179 `"Slavonian"', add
label define ancestr1_lbl 181 `"Central European, nec"', add
label define ancestr1_lbl 183 `"Northern European, nec"', add
label define ancestr1_lbl 185 `"Southern European, nec"', add
label define ancestr1_lbl 187 `"Western European, nec"', add
label define ancestr1_lbl 190 `"Eastern European, nec"', add
label define ancestr1_lbl 195 `"European, nec"', add
label define ancestr1_lbl 200 `"Spaniard"', add
label define ancestr1_lbl 201 `"Andalusian"', add
label define ancestr1_lbl 202 `"Astorian"', add
label define ancestr1_lbl 204 `"Catalonian"', add
label define ancestr1_lbl 205 `"Balearic Islander"', add
label define ancestr1_lbl 206 `"Galician"', add
label define ancestr1_lbl 210 `"Mexican"', add
label define ancestr1_lbl 211 `"Mexican American"', add
label define ancestr1_lbl 213 `"Chicano/Chicana"', add
label define ancestr1_lbl 218 `"Nuevo Mexicano"', add
label define ancestr1_lbl 219 `"Californio"', add
label define ancestr1_lbl 221 `"Costa Rican"', add
label define ancestr1_lbl 222 `"Guatemalan"', add
label define ancestr1_lbl 223 `"Honduran"', add
label define ancestr1_lbl 224 `"Nicaraguan"', add
label define ancestr1_lbl 225 `"Panamanian"', add
label define ancestr1_lbl 226 `"Salvadoran"', add
label define ancestr1_lbl 227 `"Latin American"', add
label define ancestr1_lbl 231 `"Argentinean"', add
label define ancestr1_lbl 232 `"Bolivian"', add
label define ancestr1_lbl 233 `"Chilean"', add
label define ancestr1_lbl 234 `"Colombian"', add
label define ancestr1_lbl 235 `"Ecuadorian"', add
label define ancestr1_lbl 236 `"Paraguayan"', add
label define ancestr1_lbl 237 `"Peruvian"', add
label define ancestr1_lbl 238 `"Uruguayan"', add
label define ancestr1_lbl 239 `"Venezuelan"', add
label define ancestr1_lbl 248 `"South American"', add
label define ancestr1_lbl 261 `"Puerto Rican"', add
label define ancestr1_lbl 271 `"Cuban"', add
label define ancestr1_lbl 275 `"Dominican"', add
label define ancestr1_lbl 290 `"Hispanic"', add
label define ancestr1_lbl 291 `"Spanish"', add
label define ancestr1_lbl 295 `"Spanish American"', add
label define ancestr1_lbl 296 `"Other Spanish/Hispanic"', add
label define ancestr1_lbl 300 `"Bahamian"', add
label define ancestr1_lbl 301 `"Barbadian"', add
label define ancestr1_lbl 302 `"Belizean"', add
label define ancestr1_lbl 303 `"Bermudan"', add
label define ancestr1_lbl 304 `"Cayman Islander"', add
label define ancestr1_lbl 308 `"Jamaican"', add
label define ancestr1_lbl 310 `"Dutch West Indies"', add
label define ancestr1_lbl 311 `"Aruba Islander"', add
label define ancestr1_lbl 312 `"St Maarten Islander"', add
label define ancestr1_lbl 314 `"Trinidadian/Tobagonian"', add
label define ancestr1_lbl 315 `"Trinidadian"', add
label define ancestr1_lbl 316 `"Tobagonian"', add
label define ancestr1_lbl 317 `"U.S. Virgin Islander"', add
label define ancestr1_lbl 321 `"British Virgin Islander"', add
label define ancestr1_lbl 322 `"British West Indian"', add
label define ancestr1_lbl 323 `"Turks and Caicos Islander"', add
label define ancestr1_lbl 324 `"Anguilla Islander"', add
label define ancestr1_lbl 328 `"Dominica Islander"', add
label define ancestr1_lbl 329 `"Grenadian"', add
label define ancestr1_lbl 331 `"St Lucia Islander"', add
label define ancestr1_lbl 332 `"French West Indies"', add
label define ancestr1_lbl 333 `"Guadeloupe Islander"', add
label define ancestr1_lbl 334 `"Cayenne"', add
label define ancestr1_lbl 335 `"West Indian"', add
label define ancestr1_lbl 336 `"Haitian"', add
label define ancestr1_lbl 337 `"Other West Indian"', add
label define ancestr1_lbl 360 `"Brazilian"', add
label define ancestr1_lbl 365 `"San Andres"', add
label define ancestr1_lbl 370 `"Guyanese/British Guiana"', add
label define ancestr1_lbl 375 `"Providencia"', add
label define ancestr1_lbl 380 `"Surinam/Dutch Guiana"', add
label define ancestr1_lbl 400 `"Algerian"', add
label define ancestr1_lbl 402 `"Egyptian"', add
label define ancestr1_lbl 404 `"Libyan"', add
label define ancestr1_lbl 406 `"Moroccan"', add
label define ancestr1_lbl 407 `"Ifni"', add
label define ancestr1_lbl 408 `"Tunisian"', add
label define ancestr1_lbl 411 `"North African"', add
label define ancestr1_lbl 412 `"Alhucemas"', add
label define ancestr1_lbl 413 `"Berber"', add
label define ancestr1_lbl 414 `"Rio de Oro"', add
label define ancestr1_lbl 415 `"Bahraini"', add
label define ancestr1_lbl 416 `"Iranian"', add
label define ancestr1_lbl 417 `"Iraqi"', add
label define ancestr1_lbl 419 `"Israeli"', add
label define ancestr1_lbl 421 `"Jordanian"', add
label define ancestr1_lbl 423 `"Kuwaiti"', add
label define ancestr1_lbl 425 `"Lebanese"', add
label define ancestr1_lbl 427 `"Saudi Arabian"', add
label define ancestr1_lbl 429 `"Syrian"', add
label define ancestr1_lbl 431 `"Armenian"', add
label define ancestr1_lbl 434 `"Turkish"', add
label define ancestr1_lbl 435 `"Yemeni"', add
label define ancestr1_lbl 436 `"Omani"', add
label define ancestr1_lbl 437 `"Muscat"', add
label define ancestr1_lbl 438 `"Trucial Oman"', add
label define ancestr1_lbl 439 `"Qatar"', add
label define ancestr1_lbl 442 `"Kurdish"', add
label define ancestr1_lbl 444 `"Kuria Muria Islander"', add
label define ancestr1_lbl 465 `"Palestinian"', add
label define ancestr1_lbl 466 `"Gazan"', add
label define ancestr1_lbl 467 `"West Bank"', add
label define ancestr1_lbl 470 `"South Yemeni"', add
label define ancestr1_lbl 471 `"Aden"', add
label define ancestr1_lbl 480 `"United Arab Emirates"', add
label define ancestr1_lbl 482 `"Assyrian/Chaldean/Syriac"', add
label define ancestr1_lbl 490 `"Middle Eastern"', add
label define ancestr1_lbl 495 `"Arab"', add
label define ancestr1_lbl 496 `"Other Arab"', add
label define ancestr1_lbl 500 `"Angolan"', add
label define ancestr1_lbl 502 `"Benin"', add
label define ancestr1_lbl 504 `"Botswana"', add
label define ancestr1_lbl 506 `"Burundian"', add
label define ancestr1_lbl 508 `"Cameroonian"', add
label define ancestr1_lbl 510 `"Cape Verdean"', add
label define ancestr1_lbl 513 `"Chadian"', add
label define ancestr1_lbl 515 `"Congolese"', add
label define ancestr1_lbl 516 `"Congo-Brazzaville"', add
label define ancestr1_lbl 519 `"Djibouti"', add
label define ancestr1_lbl 520 `"Equatorial Guinea"', add
label define ancestr1_lbl 522 `"Ethiopian"', add
label define ancestr1_lbl 523 `"Eritrean"', add
label define ancestr1_lbl 525 `"Gabonese"', add
label define ancestr1_lbl 527 `"Gambian"', add
label define ancestr1_lbl 529 `"Ghanian"', add
label define ancestr1_lbl 530 `"Guinean"', add
label define ancestr1_lbl 531 `"Guinea Bissau"', add
label define ancestr1_lbl 532 `"Ivory Coast"', add
label define ancestr1_lbl 534 `"Kenyan"', add
label define ancestr1_lbl 538 `"Lesotho"', add
label define ancestr1_lbl 541 `"Liberian"', add
label define ancestr1_lbl 543 `"Madagascan"', add
label define ancestr1_lbl 545 `"Malawian"', add
label define ancestr1_lbl 546 `"Malian"', add
label define ancestr1_lbl 549 `"Mozambican"', add
label define ancestr1_lbl 550 `"Namibian"', add
label define ancestr1_lbl 551 `"Niger"', add
label define ancestr1_lbl 553 `"Nigerian"', add
label define ancestr1_lbl 554 `"Fulani"', add
label define ancestr1_lbl 555 `"Hausa"', add
label define ancestr1_lbl 556 `"Ibo"', add
label define ancestr1_lbl 557 `"Tiv"', add
label define ancestr1_lbl 561 `"Rwandan"', add
label define ancestr1_lbl 564 `"Senegalese"', add
label define ancestr1_lbl 566 `"Sierra Leonean"', add
label define ancestr1_lbl 568 `"Somalian"', add
label define ancestr1_lbl 569 `"Swaziland"', add
label define ancestr1_lbl 570 `"South African"', add
label define ancestr1_lbl 571 `"Union of South Africa"', add
label define ancestr1_lbl 572 `"Afrikaner"', add
label define ancestr1_lbl 573 `"Natalian"', add
label define ancestr1_lbl 574 `"Zulu"', add
label define ancestr1_lbl 576 `"Sudanese"', add
label define ancestr1_lbl 577 `"Dinka"', add
label define ancestr1_lbl 578 `"Nuer"', add
label define ancestr1_lbl 579 `"Fur"', add
label define ancestr1_lbl 582 `"Tanzanian"', add
label define ancestr1_lbl 583 `"Tanganyikan"', add
label define ancestr1_lbl 584 `"Zanzibar Islander"', add
label define ancestr1_lbl 586 `"Togo"', add
label define ancestr1_lbl 588 `"Ugandan"', add
label define ancestr1_lbl 589 `"Upper Voltan"', add
label define ancestr1_lbl 591 `"Zairian"', add
label define ancestr1_lbl 592 `"Zambian"', add
label define ancestr1_lbl 593 `"Zimbabwean"', add
label define ancestr1_lbl 594 `"African Islands"', add
label define ancestr1_lbl 595 `"Other Subsaharan Africa"', add
label define ancestr1_lbl 596 `"Central African"', add
label define ancestr1_lbl 597 `"East African"', add
label define ancestr1_lbl 598 `"West African"', add
label define ancestr1_lbl 599 `"African"', add
label define ancestr1_lbl 600 `"Afghan"', add
label define ancestr1_lbl 601 `"Baluchi"', add
label define ancestr1_lbl 602 `"Pathan"', add
label define ancestr1_lbl 603 `"Bengali"', add
label define ancestr1_lbl 607 `"Bhutanese"', add
label define ancestr1_lbl 609 `"Nepali"', add
label define ancestr1_lbl 615 `"Asian Indian"', add
label define ancestr1_lbl 622 `"Andaman Islander"', add
label define ancestr1_lbl 624 `"Andhra Pradesh"', add
label define ancestr1_lbl 626 `"Assamese"', add
label define ancestr1_lbl 628 `"Goanese"', add
label define ancestr1_lbl 630 `"Gujarati"', add
label define ancestr1_lbl 632 `"Karnatakan"', add
label define ancestr1_lbl 634 `"Keralan"', add
label define ancestr1_lbl 638 `"Maharashtran"', add
label define ancestr1_lbl 640 `"Madrasi"', add
label define ancestr1_lbl 642 `"Mysore"', add
label define ancestr1_lbl 644 `"Naga"', add
label define ancestr1_lbl 648 `"Pondicherry"', add
label define ancestr1_lbl 650 `"Punjabi"', add
label define ancestr1_lbl 656 `"Tamil"', add
label define ancestr1_lbl 675 `"East Indies"', add
label define ancestr1_lbl 680 `"Pakistani"', add
label define ancestr1_lbl 690 `"Sri Lankan"', add
label define ancestr1_lbl 691 `"Singhalese"', add
label define ancestr1_lbl 692 `"Veddah"', add
label define ancestr1_lbl 695 `"Maldivian"', add
label define ancestr1_lbl 700 `"Burmese"', add
label define ancestr1_lbl 702 `"Shan"', add
label define ancestr1_lbl 703 `"Cambodian"', add
label define ancestr1_lbl 704 `"Khmer"', add
label define ancestr1_lbl 706 `"Chinese"', add
label define ancestr1_lbl 707 `"Cantonese"', add
label define ancestr1_lbl 708 `"Manchurian"', add
label define ancestr1_lbl 709 `"Mandarin"', add
label define ancestr1_lbl 712 `"Mongolian"', add
label define ancestr1_lbl 714 `"Tibetan"', add
label define ancestr1_lbl 716 `"Hong Kong"', add
label define ancestr1_lbl 718 `"Macao"', add
label define ancestr1_lbl 720 `"Filipino"', add
label define ancestr1_lbl 730 `"Indonesian"', add
label define ancestr1_lbl 740 `"Japanese"', add
label define ancestr1_lbl 746 `"Ryukyu Islander"', add
label define ancestr1_lbl 748 `"Okinawan"', add
label define ancestr1_lbl 750 `"Korean"', add
label define ancestr1_lbl 765 `"Laotian"', add
label define ancestr1_lbl 766 `"Meo"', add
label define ancestr1_lbl 768 `"Hmong"', add
label define ancestr1_lbl 770 `"Malaysian"', add
label define ancestr1_lbl 774 `"Singaporean"', add
label define ancestr1_lbl 776 `"Thai"', add
label define ancestr1_lbl 777 `"Black Thai"', add
label define ancestr1_lbl 778 `"Western Lao"', add
label define ancestr1_lbl 782 `"Taiwanese"', add
label define ancestr1_lbl 785 `"Vietnamese"', add
label define ancestr1_lbl 786 `"Katu"', add
label define ancestr1_lbl 787 `"Ma"', add
label define ancestr1_lbl 788 `"Mnong"', add
label define ancestr1_lbl 790 `"Montagnard"', add
label define ancestr1_lbl 792 `"Indochinese"', add
label define ancestr1_lbl 793 `"Eurasian"', add
label define ancestr1_lbl 795 `"Asian"', add
label define ancestr1_lbl 796 `"Other Asian"', add
label define ancestr1_lbl 800 `"Australian"', add
label define ancestr1_lbl 801 `"Tasmanian"', add
label define ancestr1_lbl 802 `"Australian Aborigine"', add
label define ancestr1_lbl 803 `"New Zealander"', add
label define ancestr1_lbl 808 `"Polynesian"', add
label define ancestr1_lbl 810 `"Maori"', add
label define ancestr1_lbl 811 `"Hawaiian"', add
label define ancestr1_lbl 813 `"Part Hawaiian"', add
label define ancestr1_lbl 814 `"Samoan"', add
label define ancestr1_lbl 815 `"Tongan"', add
label define ancestr1_lbl 816 `"Tokelauan"', add
label define ancestr1_lbl 817 `"Cook Islander"', add
label define ancestr1_lbl 818 `"Tahitian"', add
label define ancestr1_lbl 819 `"Niuean"', add
label define ancestr1_lbl 820 `"Micronesian"', add
label define ancestr1_lbl 821 `"Guamanian"', add
label define ancestr1_lbl 822 `"Chamorro Islander"', add
label define ancestr1_lbl 823 `"Saipanese"', add
label define ancestr1_lbl 824 `"Palauan"', add
label define ancestr1_lbl 825 `"Marshall Islander"', add
label define ancestr1_lbl 826 `"Kosraean"', add
label define ancestr1_lbl 827 `"Ponapean"', add
label define ancestr1_lbl 828 `"Chuukese"', add
label define ancestr1_lbl 829 `"Yap Islander"', add
label define ancestr1_lbl 830 `"Caroline Islander"', add
label define ancestr1_lbl 831 `"Kiribatese"', add
label define ancestr1_lbl 832 `"Nauruan"', add
label define ancestr1_lbl 833 `"Tarawa Islander"', add
label define ancestr1_lbl 834 `"Tinian Islander"', add
label define ancestr1_lbl 840 `"Melanesian Islander"', add
label define ancestr1_lbl 841 `"Fijian"', add
label define ancestr1_lbl 843 `"New Guinean"', add
label define ancestr1_lbl 844 `"Papuan"', add
label define ancestr1_lbl 845 `"Solomon Islander"', add
label define ancestr1_lbl 846 `"New Caledonian Islander"', add
label define ancestr1_lbl 847 `"Vanuatuan"', add
label define ancestr1_lbl 850 `"Pacific Islander"', add
label define ancestr1_lbl 860 `"Oceania"', add
label define ancestr1_lbl 862 `"Chamolinian"', add
label define ancestr1_lbl 863 `"Reserved Codes"', add
label define ancestr1_lbl 870 `"Other Pacific"', add
label define ancestr1_lbl 900 `"Afro-American"', add
label define ancestr1_lbl 902 `"African-American"', add
label define ancestr1_lbl 913 `"Central American Indian"', add
label define ancestr1_lbl 914 `"South American Indian"', add
label define ancestr1_lbl 920 `"American Indian  (all tribes)"', add
label define ancestr1_lbl 921 `"Aleut"', add
label define ancestr1_lbl 922 `"Eskimo"', add
label define ancestr1_lbl 923 `"Inuit"', add
label define ancestr1_lbl 924 `"White/Caucasian"', add
label define ancestr1_lbl 930 `"Greenlander"', add
label define ancestr1_lbl 931 `"Canadian"', add
label define ancestr1_lbl 933 `"Newfoundland"', add
label define ancestr1_lbl 934 `"Nova Scotian"', add
label define ancestr1_lbl 935 `"French Canadian"', add
label define ancestr1_lbl 936 `"Acadian"', add
label define ancestr1_lbl 939 `"American"', add
label define ancestr1_lbl 940 `"United States"', add
label define ancestr1_lbl 941 `"Alabama"', add
label define ancestr1_lbl 942 `"Alaska"', add
label define ancestr1_lbl 943 `"Arizona"', add
label define ancestr1_lbl 944 `"Arkansas"', add
label define ancestr1_lbl 945 `"California"', add
label define ancestr1_lbl 946 `"Colorado"', add
label define ancestr1_lbl 947 `"Connecticut"', add
label define ancestr1_lbl 948 `"District of Columbia"', add
label define ancestr1_lbl 949 `"Delaware"', add
label define ancestr1_lbl 950 `"Florida"', add
label define ancestr1_lbl 951 `"Georgia"', add
label define ancestr1_lbl 952 `"Idaho"', add
label define ancestr1_lbl 953 `"Illinois"', add
label define ancestr1_lbl 954 `"Indiana"', add
label define ancestr1_lbl 955 `"Iowa"', add
label define ancestr1_lbl 956 `"Kansas"', add
label define ancestr1_lbl 957 `"Kentucky"', add
label define ancestr1_lbl 958 `"Louisiana"', add
label define ancestr1_lbl 959 `"Maine"', add
label define ancestr1_lbl 960 `"Maryland"', add
label define ancestr1_lbl 961 `"Massachusetts"', add
label define ancestr1_lbl 962 `"Michigan"', add
label define ancestr1_lbl 963 `"Minnesota"', add
label define ancestr1_lbl 964 `"Mississippi"', add
label define ancestr1_lbl 965 `"Missouri"', add
label define ancestr1_lbl 966 `"Montana"', add
label define ancestr1_lbl 967 `"Nebraska"', add
label define ancestr1_lbl 968 `"Nevada"', add
label define ancestr1_lbl 969 `"New Hampshire"', add
label define ancestr1_lbl 970 `"New Jersey"', add
label define ancestr1_lbl 971 `"New Mexico"', add
label define ancestr1_lbl 972 `"New York"', add
label define ancestr1_lbl 973 `"North Carolina"', add
label define ancestr1_lbl 974 `"North Dakota"', add
label define ancestr1_lbl 975 `"Ohio"', add
label define ancestr1_lbl 976 `"Oklahoma"', add
label define ancestr1_lbl 977 `"Oregon"', add
label define ancestr1_lbl 978 `"Pennsylvania"', add
label define ancestr1_lbl 979 `"Rhode Island"', add
label define ancestr1_lbl 980 `"South Carolina"', add
label define ancestr1_lbl 981 `"South Dakota"', add
label define ancestr1_lbl 982 `"Tennessee"', add
label define ancestr1_lbl 983 `"Texas"', add
label define ancestr1_lbl 984 `"Utah"', add
label define ancestr1_lbl 985 `"Vermont"', add
label define ancestr1_lbl 986 `"Virginia"', add
label define ancestr1_lbl 987 `"Washington"', add
label define ancestr1_lbl 988 `"West Virginia"', add
label define ancestr1_lbl 989 `"Wisconsin"', add
label define ancestr1_lbl 990 `"Wyoming"', add
label define ancestr1_lbl 993 `"Southerner"', add
label define ancestr1_lbl 994 `"North American"', add
label define ancestr1_lbl 995 `"Mixture"', add
label define ancestr1_lbl 996 `"Uncodable"', add
label define ancestr1_lbl 998 `"Other"', add
label define ancestr1_lbl 999 `"Not Reported"', add
label values ancestr1 ancestr1_lbl

label define ancestr1d_lbl 0010 `"Alsatian"'
label define ancestr1d_lbl 0020 `"Andorran"', add
label define ancestr1d_lbl 0030 `"Austrian"', add
label define ancestr1d_lbl 0040 `"Tirolean"', add
label define ancestr1d_lbl 0051 `"Basque (1980)"', add
label define ancestr1d_lbl 0052 `"Spanish Basque (1980)"', add
label define ancestr1d_lbl 0053 `"Basque (1990-2000)"', add
label define ancestr1d_lbl 0054 `"Spanish Basque (1990-2000, 2001-2004 ACS)"', add
label define ancestr1d_lbl 0060 `"French Basque"', add
label define ancestr1d_lbl 0080 `"Belgian"', add
label define ancestr1d_lbl 0090 `"Flemish"', add
label define ancestr1d_lbl 0100 `"Walloon"', add
label define ancestr1d_lbl 0110 `"British"', add
label define ancestr1d_lbl 0120 `"British Isles"', add
label define ancestr1d_lbl 0130 `"Channel Islander"', add
label define ancestr1d_lbl 0140 `"Gibraltan"', add
label define ancestr1d_lbl 0150 `"Cornish"', add
label define ancestr1d_lbl 0160 `"Corsican"', add
label define ancestr1d_lbl 0170 `"Cypriot"', add
label define ancestr1d_lbl 0180 `"Greek Cypriote"', add
label define ancestr1d_lbl 0190 `"Turkish Cypriote"', add
label define ancestr1d_lbl 0200 `"Danish"', add
label define ancestr1d_lbl 0210 `"Dutch"', add
label define ancestr1d_lbl 0211 `"Dutch-French-Irish"', add
label define ancestr1d_lbl 0212 `"Dutch-German-Irish"', add
label define ancestr1d_lbl 0213 `"Dutch-Irish-Scotch"', add
label define ancestr1d_lbl 0220 `"English"', add
label define ancestr1d_lbl 0221 `"English-French-German"', add
label define ancestr1d_lbl 0222 `"English-French-Irish"', add
label define ancestr1d_lbl 0223 `"English-German-Irish"', add
label define ancestr1d_lbl 0224 `"English-German-Swedish"', add
label define ancestr1d_lbl 0225 `"English-Irish-Scotch"', add
label define ancestr1d_lbl 0226 `"English-Scotch-Welsh"', add
label define ancestr1d_lbl 0230 `"Faeroe Islander"', add
label define ancestr1d_lbl 0240 `"Finnish"', add
label define ancestr1d_lbl 0250 `"Karelian"', add
label define ancestr1d_lbl 0260 `"French (1980)"', add
label define ancestr1d_lbl 0261 `"French (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 0262 `"Occitan (1990-2000)"', add
label define ancestr1d_lbl 0270 `"Lorrainian"', add
label define ancestr1d_lbl 0280 `"Breton"', add
label define ancestr1d_lbl 0290 `"Frisian"', add
label define ancestr1d_lbl 0300 `"Friulian"', add
label define ancestr1d_lbl 0320 `"German (1980)"', add
label define ancestr1d_lbl 0321 `"German (1990-2000, ACS/PRCS)"', add
label define ancestr1d_lbl 0322 `"Pennsylvania German (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 0323 `"East German (1990-2000)"', add
label define ancestr1d_lbl 0324 `"West German (2000)"', add
label define ancestr1d_lbl 0325 `"German-French-Irish"', add
label define ancestr1d_lbl 0326 `"German-Irish-Italian"', add
label define ancestr1d_lbl 0327 `"German-Irish-Scotch"', add
label define ancestr1d_lbl 0328 `"German-Irish-Swedish"', add
label define ancestr1d_lbl 0329 `"Germanic"', add
label define ancestr1d_lbl 0330 `"Bavarian"', add
label define ancestr1d_lbl 0340 `"Berliner"', add
label define ancestr1d_lbl 0350 `"Hamburger"', add
label define ancestr1d_lbl 0360 `"Hanoverian"', add
label define ancestr1d_lbl 0370 `"Hessian"', add
label define ancestr1d_lbl 0380 `"Lubecker"', add
label define ancestr1d_lbl 0390 `"Pomeranian (1980)"', add
label define ancestr1d_lbl 0391 `"Pomeranian (1990-2000)"', add
label define ancestr1d_lbl 0392 `"Silesian (1990-2000)"', add
label define ancestr1d_lbl 0400 `"Prussian"', add
label define ancestr1d_lbl 0410 `"Saxon"', add
label define ancestr1d_lbl 0420 `"Sudetenlander"', add
label define ancestr1d_lbl 0430 `"Westphalian"', add
label define ancestr1d_lbl 0460 `"Greek"', add
label define ancestr1d_lbl 0470 `"Cretan"', add
label define ancestr1d_lbl 0480 `"Cycladic Islander"', add
label define ancestr1d_lbl 0490 `"Icelander"', add
label define ancestr1d_lbl 0500 `"Irish"', add
label define ancestr1d_lbl 0501 `"Celtic"', add
label define ancestr1d_lbl 0502 `"Irish Scotch"', add
label define ancestr1d_lbl 0510 `"Italian (1980)"', add
label define ancestr1d_lbl 0511 `"Italian (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 0512 `"Trieste (1990-2000)"', add
label define ancestr1d_lbl 0513 `"San Marino (1990-2000)"', add
label define ancestr1d_lbl 0530 `"Abruzzi"', add
label define ancestr1d_lbl 0540 `"Apulian"', add
label define ancestr1d_lbl 0550 `"Basilicata"', add
label define ancestr1d_lbl 0560 `"Calabrian"', add
label define ancestr1d_lbl 0570 `"Amalfi"', add
label define ancestr1d_lbl 0580 `"Emilia Romagna"', add
label define ancestr1d_lbl 0590 `"Rome"', add
label define ancestr1d_lbl 0600 `"Ligurian"', add
label define ancestr1d_lbl 0610 `"Lombardian"', add
label define ancestr1d_lbl 0620 `"Marches"', add
label define ancestr1d_lbl 0630 `"Molise"', add
label define ancestr1d_lbl 0640 `"Neapolitan"', add
label define ancestr1d_lbl 0650 `"Piedmontese"', add
label define ancestr1d_lbl 0660 `"Puglia"', add
label define ancestr1d_lbl 0670 `"Sardinian"', add
label define ancestr1d_lbl 0680 `"Sicilian"', add
label define ancestr1d_lbl 0690 `"Tuscan"', add
label define ancestr1d_lbl 0700 `"Trentino"', add
label define ancestr1d_lbl 0710 `"Umbrian"', add
label define ancestr1d_lbl 0720 `"Valle dAosta"', add
label define ancestr1d_lbl 0730 `"Venetian"', add
label define ancestr1d_lbl 0750 `"Lapp"', add
label define ancestr1d_lbl 0760 `"Liechtensteiner"', add
label define ancestr1d_lbl 0770 `"Luxemburger"', add
label define ancestr1d_lbl 0780 `"Maltese"', add
label define ancestr1d_lbl 0790 `"Manx"', add
label define ancestr1d_lbl 0800 `"Monegasque"', add
label define ancestr1d_lbl 0810 `"Northern Irelander"', add
label define ancestr1d_lbl 0820 `"Norwegian"', add
label define ancestr1d_lbl 0840 `"Portuguese"', add
label define ancestr1d_lbl 0850 `"Azorean"', add
label define ancestr1d_lbl 0860 `"Madeiran"', add
label define ancestr1d_lbl 0870 `"Scotch Irish"', add
label define ancestr1d_lbl 0880 `"Scottish"', add
label define ancestr1d_lbl 0890 `"Swedish"', add
label define ancestr1d_lbl 0900 `"Aland Islander"', add
label define ancestr1d_lbl 0910 `"Swiss"', add
label define ancestr1d_lbl 0920 `"Suisse (1980)"', add
label define ancestr1d_lbl 0921 `"Suisse (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 0922 `"Switzer (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 0950 `"Romansch (1980, ACS)"', add
label define ancestr1d_lbl 0951 `"Romanscho (1990-2000)"', add
label define ancestr1d_lbl 0952 `"Ladin (1990-2000)"', add
label define ancestr1d_lbl 0960 `"Suisse Romane (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 0961 `"Suisse Romane (1980)"', add
label define ancestr1d_lbl 0962 `"Ticino"', add
label define ancestr1d_lbl 0970 `"Welsh"', add
label define ancestr1d_lbl 0980 `"Scandinavian, Nordic"', add
label define ancestr1d_lbl 1000 `"Albanian"', add
label define ancestr1d_lbl 1010 `"Azerbaijani"', add
label define ancestr1d_lbl 1020 `"Belorussian"', add
label define ancestr1d_lbl 1030 `"Bulgarian"', add
label define ancestr1d_lbl 1050 `"Carpathian"', add
label define ancestr1d_lbl 1051 `"Carpatho Rusyn"', add
label define ancestr1d_lbl 1052 `"Rusyn"', add
label define ancestr1d_lbl 1080 `"Cossack (1990-2000)"', add
label define ancestr1d_lbl 1081 `"Cossack (1980)"', add
label define ancestr1d_lbl 1082 `"Turkestani (1990-2000, 2012 ACS)"', add
label define ancestr1d_lbl 1083 `"Kirghiz (1980)"', add
label define ancestr1d_lbl 1084 `"Turcoman (1980)"', add
label define ancestr1d_lbl 1090 `"Croatian"', add
label define ancestr1d_lbl 1110 `"Czechoslovakian"', add
label define ancestr1d_lbl 1111 `"Czech"', add
label define ancestr1d_lbl 1120 `"Bohemian"', add
label define ancestr1d_lbl 1121 `"Bohemian (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 1122 `"Moravian (1990-2000)"', add
label define ancestr1d_lbl 1150 `"Estonian"', add
label define ancestr1d_lbl 1160 `"Livonian"', add
label define ancestr1d_lbl 1170 `"Finno Ugrian (1990-2000)"', add
label define ancestr1d_lbl 1171 `"Udmert"', add
label define ancestr1d_lbl 1180 `"Mordovian"', add
label define ancestr1d_lbl 1190 `"Voytak"', add
label define ancestr1d_lbl 1200 `"Georgian"', add
label define ancestr1d_lbl 1220 `"Germans from Russia"', add
label define ancestr1d_lbl 1221 `"Volga"', add
label define ancestr1d_lbl 1222 `"German from Russia (1990-2000); German Russian (ACS, PRCS)"', add
label define ancestr1d_lbl 1230 `"Gruziia (1990-2000)"', add
label define ancestr1d_lbl 1240 `"Rom"', add
label define ancestr1d_lbl 1250 `"Hungarian"', add
label define ancestr1d_lbl 1260 `"Magyar"', add
label define ancestr1d_lbl 1280 `"Latvian"', add
label define ancestr1d_lbl 1290 `"Lithuanian"', add
label define ancestr1d_lbl 1300 `"Macedonian"', add
label define ancestr1d_lbl 1320 `"North Caucasian"', add
label define ancestr1d_lbl 1330 `"North Caucasian Turkic (1990-2000)"', add
label define ancestr1d_lbl 1400 `"Ossetian"', add
label define ancestr1d_lbl 1420 `"Polish"', add
label define ancestr1d_lbl 1430 `"Kashubian"', add
label define ancestr1d_lbl 1440 `"Romanian (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 1441 `"Rumanian (1980)"', add
label define ancestr1d_lbl 1442 `"Transylvanian"', add
label define ancestr1d_lbl 1450 `"Bessarabian (1980)"', add
label define ancestr1d_lbl 1451 `"Bessarabian (1990-2000)"', add
label define ancestr1d_lbl 1452 `"Bucovina"', add
label define ancestr1d_lbl 1460 `"Moldavian"', add
label define ancestr1d_lbl 1470 `"Wallachian"', add
label define ancestr1d_lbl 1480 `"Russian"', add
label define ancestr1d_lbl 1500 `"Muscovite"', add
label define ancestr1d_lbl 1520 `"Serbian (1980)"', add
label define ancestr1d_lbl 1521 `"Serbian (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 1522 `"Bosnian (1990) Herzegovinian (2000, ACS, PRCS)"', add
label define ancestr1d_lbl 1523 `"Montenegrin (1990-2000, 2012 ACS)"', add
label define ancestr1d_lbl 1530 `"Slovak"', add
label define ancestr1d_lbl 1540 `"Slovene"', add
label define ancestr1d_lbl 1550 `"Sorb/Wend"', add
label define ancestr1d_lbl 1560 `"Soviet Turkic (1990-2000)"', add
label define ancestr1d_lbl 1570 `"Bashkir"', add
label define ancestr1d_lbl 1580 `"Chevash"', add
label define ancestr1d_lbl 1590 `"Gagauz (1990-2000)"', add
label define ancestr1d_lbl 1600 `"Mesknetian (1990-2000)"', add
label define ancestr1d_lbl 1630 `"Yakut"', add
label define ancestr1d_lbl 1640 `"Soviet Union, nec"', add
label define ancestr1d_lbl 1650 `"Tatar (1990-2000)"', add
label define ancestr1d_lbl 1651 `"Tartar (1980)"', add
label define ancestr1d_lbl 1652 `"Crimean (1980)"', add
label define ancestr1d_lbl 1653 `"Tuvinian (1990-2000)"', add
label define ancestr1d_lbl 1654 `"Soviet Central Asia (1990-2000)"', add
label define ancestr1d_lbl 1655 `"Tadzhik (1980, 2000)"', add
label define ancestr1d_lbl 1690 `"Uzbek"', add
label define ancestr1d_lbl 1710 `"Ukrainian (1980)"', add
label define ancestr1d_lbl 1711 `"Ukrainian (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 1712 `"Ruthenian (1980)"', add
label define ancestr1d_lbl 1713 `"Ruthenian (1990-2000)"', add
label define ancestr1d_lbl 1714 `"Lemko"', add
label define ancestr1d_lbl 1715 `"Bioko"', add
label define ancestr1d_lbl 1716 `"Husel"', add
label define ancestr1d_lbl 1717 `"Windish"', add
label define ancestr1d_lbl 1760 `"Yugoslavian"', add
label define ancestr1d_lbl 1780 `"Slav"', add
label define ancestr1d_lbl 1790 `"Slavonian"', add
label define ancestr1d_lbl 1810 `"Central European, nec"', add
label define ancestr1d_lbl 1830 `"Northern European, nec"', add
label define ancestr1d_lbl 1850 `"Southern European, nec"', add
label define ancestr1d_lbl 1870 `"Western European, nec"', add
label define ancestr1d_lbl 1900 `"Eastern European, nec"', add
label define ancestr1d_lbl 1950 `"European, nec"', add
label define ancestr1d_lbl 2000 `"Spaniard (1980)"', add
label define ancestr1d_lbl 2001 `"Spaniard (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 2002 `"Castillian (1990-2000)"', add
label define ancestr1d_lbl 2003 `"Valencian (1990-2000)"', add
label define ancestr1d_lbl 2010 `"Andalusian (1990-2000)"', add
label define ancestr1d_lbl 2020 `"Asturian (1990-2000)"', add
label define ancestr1d_lbl 2040 `"Catalonian"', add
label define ancestr1d_lbl 2050 `"Balearic Islander (1980)"', add
label define ancestr1d_lbl 2051 `"Balearic Islander (1990-2000)"', add
label define ancestr1d_lbl 2052 `"Canary Islander (1990-2000)"', add
label define ancestr1d_lbl 2060 `"Galician (1980)"', add
label define ancestr1d_lbl 2061 `"Gallego (1990-2000)"', add
label define ancestr1d_lbl 2062 `"Galician (1990-2000)"', add
label define ancestr1d_lbl 2100 `"Mexican"', add
label define ancestr1d_lbl 2101 `"Mexican (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 2102 `"Mexicano/Mexicana (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 2103 `"Mexican Indian"', add
label define ancestr1d_lbl 2110 `"Mexican American"', add
label define ancestr1d_lbl 2111 `"Mexican American Indian"', add
label define ancestr1d_lbl 2130 `"Chicano/Chicana"', add
label define ancestr1d_lbl 2180 `"Nuevo Mexicano"', add
label define ancestr1d_lbl 2181 `"Nuevo Mexicano (1990-2000)"', add
label define ancestr1d_lbl 2182 `"La Raza (1990-2000)"', add
label define ancestr1d_lbl 2183 `"Mexican state (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 2184 `"Tejano/Tejana (1990-2000)"', add
label define ancestr1d_lbl 2190 `"Californio"', add
label define ancestr1d_lbl 2210 `"Costa Rican"', add
label define ancestr1d_lbl 2220 `"Guatemalan"', add
label define ancestr1d_lbl 2230 `"Honduran"', add
label define ancestr1d_lbl 2240 `"Nicaraguan"', add
label define ancestr1d_lbl 2250 `"Panamanian (1980)"', add
label define ancestr1d_lbl 2251 `"Panamanian (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 2252 `"Canal Zone (1990-2000)"', add
label define ancestr1d_lbl 2260 `"Salvadoran"', add
label define ancestr1d_lbl 2270 `"Latin American (1980)"', add
label define ancestr1d_lbl 2271 `"Central American (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 2272 `"Latin American (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 2273 `"Latino/Latina (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 2274 `"Latin (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 2310 `"Argentinean"', add
label define ancestr1d_lbl 2320 `"Bolivian"', add
label define ancestr1d_lbl 2330 `"Chilean"', add
label define ancestr1d_lbl 2340 `"Colombian"', add
label define ancestr1d_lbl 2350 `"Ecuadorian"', add
label define ancestr1d_lbl 2360 `"Paraguayan"', add
label define ancestr1d_lbl 2370 `"Peruvian"', add
label define ancestr1d_lbl 2380 `"Uruguayan"', add
label define ancestr1d_lbl 2390 `"Venezuelan"', add
label define ancestr1d_lbl 2480 `"South American (1980)"', add
label define ancestr1d_lbl 2481 `"South American (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 2482 `"Criollo/Criolla (1990-2000)"', add
label define ancestr1d_lbl 2610 `"Puerto Rican"', add
label define ancestr1d_lbl 2710 `"Cuban"', add
label define ancestr1d_lbl 2750 `"Dominican"', add
label define ancestr1d_lbl 2900 `"Hispanic"', add
label define ancestr1d_lbl 2910 `"Spanish"', add
label define ancestr1d_lbl 2950 `"Spanish American"', add
label define ancestr1d_lbl 2960 `"Other Spanish/Hispanic"', add
label define ancestr1d_lbl 3000 `"Bahamian"', add
label define ancestr1d_lbl 3010 `"Barbadian"', add
label define ancestr1d_lbl 3020 `"Belizean"', add
label define ancestr1d_lbl 3030 `"Bermudan"', add
label define ancestr1d_lbl 3040 `"Cayman Islander"', add
label define ancestr1d_lbl 3080 `"Jamaican"', add
label define ancestr1d_lbl 3100 `"Dutch West Indies"', add
label define ancestr1d_lbl 3110 `"Aruba Islander"', add
label define ancestr1d_lbl 3120 `"St Maarten Islander"', add
label define ancestr1d_lbl 3140 `"Trinidadian/Tobagonian"', add
label define ancestr1d_lbl 3150 `"Trinidadian"', add
label define ancestr1d_lbl 3160 `"Tobagonian"', add
label define ancestr1d_lbl 3170 `"U.S. Virgin Islander (1980)"', add
label define ancestr1d_lbl 3171 `"U.S. Virgin Islander (1990-2000)"', add
label define ancestr1d_lbl 3172 `"St. Croix Islander (1990-2000)"', add
label define ancestr1d_lbl 3173 `"St. John Islander (1990-2000)"', add
label define ancestr1d_lbl 3174 `"St. Thomas Islander (1990-2000)"', add
label define ancestr1d_lbl 3210 `"British Virgin Islander (1980)"', add
label define ancestr1d_lbl 3211 `"British Virgin Islander (1990-2000)"', add
label define ancestr1d_lbl 3212 `"Antigua (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 3220 `"British West Indian"', add
label define ancestr1d_lbl 3230 `"Turks and Caicos Islander"', add
label define ancestr1d_lbl 3240 `"Anguilla Islander (1980)"', add
label define ancestr1d_lbl 3241 `"Anguilla Islander (1990-2000)"', add
label define ancestr1d_lbl 3242 `"Montserrat Islander (1990-2000)"', add
label define ancestr1d_lbl 3243 `"Kitts/Nevis Islander (1990-2000)"', add
label define ancestr1d_lbl 3244 `"St. Christopher (1980)"', add
label define ancestr1d_lbl 3245 `"St Vincent Islander (1990); Vincent-Grenadine Islander (2000 Census, 2005 ACS, 2005 PRCS)"', add
label define ancestr1d_lbl 3280 `"Dominica Islander"', add
label define ancestr1d_lbl 3290 `"Grenadian"', add
label define ancestr1d_lbl 3310 `"St Lucia Islander"', add
label define ancestr1d_lbl 3320 `"French West Indies"', add
label define ancestr1d_lbl 3330 `"Guadeloupe Islander"', add
label define ancestr1d_lbl 3340 `"Cayenne"', add
label define ancestr1d_lbl 3350 `"West Indian (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 3351 `"West Indian (1980)"', add
label define ancestr1d_lbl 3352 `"Caribbean (1980)"', add
label define ancestr1d_lbl 3353 `"Arawak (1980)"', add
label define ancestr1d_lbl 3360 `"Haitian"', add
label define ancestr1d_lbl 3370 `"Other West Indian"', add
label define ancestr1d_lbl 3600 `"Brazilian"', add
label define ancestr1d_lbl 3650 `"San Andres"', add
label define ancestr1d_lbl 3700 `"Guyanese/British Guiana"', add
label define ancestr1d_lbl 3750 `"Providencia"', add
label define ancestr1d_lbl 3800 `"Surinam/Dutch Guiana"', add
label define ancestr1d_lbl 4000 `"Algerian"', add
label define ancestr1d_lbl 4020 `"Egyptian"', add
label define ancestr1d_lbl 4040 `"Libyan"', add
label define ancestr1d_lbl 4060 `"Moroccan (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 4061 `"Moroccan (1980)"', add
label define ancestr1d_lbl 4062 `"Moor (1980)"', add
label define ancestr1d_lbl 4070 `"Ifni"', add
label define ancestr1d_lbl 4080 `"Tunisian"', add
label define ancestr1d_lbl 4110 `"North African"', add
label define ancestr1d_lbl 4120 `"Alhucemas"', add
label define ancestr1d_lbl 4130 `"Berber"', add
label define ancestr1d_lbl 4140 `"Rio de Oro"', add
label define ancestr1d_lbl 4150 `"Bahraini"', add
label define ancestr1d_lbl 4160 `"Iranian"', add
label define ancestr1d_lbl 4170 `"Iraqi"', add
label define ancestr1d_lbl 4190 `"Israeli"', add
label define ancestr1d_lbl 4210 `"Jordanian"', add
label define ancestr1d_lbl 4220 `"Transjordan"', add
label define ancestr1d_lbl 4230 `"Kuwaiti"', add
label define ancestr1d_lbl 4250 `"Lebanese"', add
label define ancestr1d_lbl 4270 `"Saudi Arabian"', add
label define ancestr1d_lbl 4290 `"Syrian (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 4291 `"Syrian (1980)"', add
label define ancestr1d_lbl 4292 `"Latakian (1980)"', add
label define ancestr1d_lbl 4293 `"Jebel Druse (1980)"', add
label define ancestr1d_lbl 4310 `"Armenian"', add
label define ancestr1d_lbl 4340 `"Turkish"', add
label define ancestr1d_lbl 4350 `"Yemeni"', add
label define ancestr1d_lbl 4360 `"Omani"', add
label define ancestr1d_lbl 4370 `"Muscat"', add
label define ancestr1d_lbl 4380 `"Trucial Oman"', add
label define ancestr1d_lbl 4390 `"Qatar"', add
label define ancestr1d_lbl 4410 `"Bedouin"', add
label define ancestr1d_lbl 4420 `"Kurdish"', add
label define ancestr1d_lbl 4440 `"Kuria Muria Islander"', add
label define ancestr1d_lbl 4650 `"Palestinian"', add
label define ancestr1d_lbl 4660 `"Gazan"', add
label define ancestr1d_lbl 4670 `"West Bank"', add
label define ancestr1d_lbl 4700 `"South Yemeni"', add
label define ancestr1d_lbl 4710 `"Aden"', add
label define ancestr1d_lbl 4800 `"United Arab Emirates"', add
label define ancestr1d_lbl 4820 `"Assyrian/Chaldean/Syriac (1990-2000)"', add
label define ancestr1d_lbl 4821 `"Assyrian"', add
label define ancestr1d_lbl 4822 `"Syriac (1980, 2000)"', add
label define ancestr1d_lbl 4823 `"Chaldean (2000, ACS, PRCS)"', add
label define ancestr1d_lbl 4900 `"Middle Eastern"', add
label define ancestr1d_lbl 4950 `"Arab"', add
label define ancestr1d_lbl 4951 `"Arabic (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 4960 `"Other Arab"', add
label define ancestr1d_lbl 5000 `"Angolan"', add
label define ancestr1d_lbl 5020 `"Benin"', add
label define ancestr1d_lbl 5040 `"Botswana"', add
label define ancestr1d_lbl 5060 `"Burundian"', add
label define ancestr1d_lbl 5080 `"Cameroonian"', add
label define ancestr1d_lbl 5100 `"Cape Verdean"', add
label define ancestr1d_lbl 5120 `"Central African Republic"', add
label define ancestr1d_lbl 5130 `"Chadian"', add
label define ancestr1d_lbl 5150 `"Congolese"', add
label define ancestr1d_lbl 5160 `"Congo-Brazzaville"', add
label define ancestr1d_lbl 5190 `"Djibouti"', add
label define ancestr1d_lbl 5200 `"Equatorial Guinea"', add
label define ancestr1d_lbl 5210 `"Corsico Islander"', add
label define ancestr1d_lbl 5220 `"Ethiopian"', add
label define ancestr1d_lbl 5230 `"Eritrean"', add
label define ancestr1d_lbl 5250 `"Gabonese"', add
label define ancestr1d_lbl 5270 `"Gambian"', add
label define ancestr1d_lbl 5290 `"Ghanian"', add
label define ancestr1d_lbl 5300 `"Guinean"', add
label define ancestr1d_lbl 5310 `"Guinea Bissau"', add
label define ancestr1d_lbl 5320 `"Ivory Coast"', add
label define ancestr1d_lbl 5340 `"Kenyan"', add
label define ancestr1d_lbl 5380 `"Lesotho"', add
label define ancestr1d_lbl 5410 `"Liberian"', add
label define ancestr1d_lbl 5430 `"Madagascan"', add
label define ancestr1d_lbl 5450 `"Malawian"', add
label define ancestr1d_lbl 5460 `"Malian"', add
label define ancestr1d_lbl 5470 `"Mauritanian"', add
label define ancestr1d_lbl 5490 `"Mozambican"', add
label define ancestr1d_lbl 5500 `"Namibian"', add
label define ancestr1d_lbl 5510 `"Niger"', add
label define ancestr1d_lbl 5530 `"Nigerian"', add
label define ancestr1d_lbl 5540 `"Fulani"', add
label define ancestr1d_lbl 5550 `"Hausa"', add
label define ancestr1d_lbl 5560 `"Ibo"', add
label define ancestr1d_lbl 5570 `"Tiv (1980)"', add
label define ancestr1d_lbl 5571 `"Tiv (1990-2000)"', add
label define ancestr1d_lbl 5572 `"Yoruba (1990-2000)"', add
label define ancestr1d_lbl 5610 `"Rwandan"', add
label define ancestr1d_lbl 5640 `"Senegalese"', add
label define ancestr1d_lbl 5660 `"Sierra Leonean"', add
label define ancestr1d_lbl 5680 `"Somalian"', add
label define ancestr1d_lbl 5690 `"Swaziland"', add
label define ancestr1d_lbl 5700 `"South African"', add
label define ancestr1d_lbl 5710 `"Union of South Africa"', add
label define ancestr1d_lbl 5720 `"Afrikaner"', add
label define ancestr1d_lbl 5730 `"Natalian"', add
label define ancestr1d_lbl 5740 `"Zulu"', add
label define ancestr1d_lbl 5760 `"Sudanese"', add
label define ancestr1d_lbl 5770 `"Dinka"', add
label define ancestr1d_lbl 5780 `"Nuer"', add
label define ancestr1d_lbl 5790 `"Fur"', add
label define ancestr1d_lbl 5800 `"Baggara"', add
label define ancestr1d_lbl 5820 `"Tanzanian"', add
label define ancestr1d_lbl 5830 `"Tanganyikan"', add
label define ancestr1d_lbl 5840 `"Zanzibar"', add
label define ancestr1d_lbl 5860 `"Togo"', add
label define ancestr1d_lbl 5880 `"Ugandan"', add
label define ancestr1d_lbl 5890 `"Upper Voltan"', add
label define ancestr1d_lbl 5900 `"Volta"', add
label define ancestr1d_lbl 5910 `"Zairian"', add
label define ancestr1d_lbl 5920 `"Zambian"', add
label define ancestr1d_lbl 5930 `"Zimbabwean"', add
label define ancestr1d_lbl 5940 `"African Islands (1980)"', add
label define ancestr1d_lbl 5941 `"African Islands (1990-2000)"', add
label define ancestr1d_lbl 5942 `"Mauritius (1990-2000)"', add
label define ancestr1d_lbl 5950 `"Other Subsaharan Africa"', add
label define ancestr1d_lbl 5960 `"Central African"', add
label define ancestr1d_lbl 5970 `"East African"', add
label define ancestr1d_lbl 5980 `"West African"', add
label define ancestr1d_lbl 5990 `"African"', add
label define ancestr1d_lbl 6000 `"Afghan"', add
label define ancestr1d_lbl 6010 `"Baluchi"', add
label define ancestr1d_lbl 6020 `"Pathan"', add
label define ancestr1d_lbl 6030 `"Bengali (1980)"', add
label define ancestr1d_lbl 6031 `"Bangladeshi (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 6032 `"Bengali (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 6070 `"Bhutanese"', add
label define ancestr1d_lbl 6090 `"Nepali"', add
label define ancestr1d_lbl 6150 `"Asian Indian (1980)"', add
label define ancestr1d_lbl 6151 `"India (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 6152 `"East Indian (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 6153 `"Madhya Pradesh (1990-2000)"', add
label define ancestr1d_lbl 6154 `"Orissa (1990-2000)"', add
label define ancestr1d_lbl 6155 `"Rajasthani (1990-2000)"', add
label define ancestr1d_lbl 6156 `"Sikkim (1990-2000)"', add
label define ancestr1d_lbl 6157 `"Uttar Pradesh (1990-2000)"', add
label define ancestr1d_lbl 6220 `"Andaman Islander"', add
label define ancestr1d_lbl 6240 `"Andhra Pradesh"', add
label define ancestr1d_lbl 6260 `"Assamese"', add
label define ancestr1d_lbl 6280 `"Goanese"', add
label define ancestr1d_lbl 6300 `"Gujarati"', add
label define ancestr1d_lbl 6320 `"Karnatakan"', add
label define ancestr1d_lbl 6340 `"Keralan"', add
label define ancestr1d_lbl 6380 `"Maharashtran"', add
label define ancestr1d_lbl 6400 `"Madrasi"', add
label define ancestr1d_lbl 6420 `"Mysore"', add
label define ancestr1d_lbl 6440 `"Naga"', add
label define ancestr1d_lbl 6480 `"Pondicherry"', add
label define ancestr1d_lbl 6500 `"Punjabi"', add
label define ancestr1d_lbl 6560 `"Tamil"', add
label define ancestr1d_lbl 6750 `"East Indies (1990-2000)"', add
label define ancestr1d_lbl 6800 `"Pakistani (1980)"', add
label define ancestr1d_lbl 6801 `"Pakistani (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 6802 `"Kashmiri (1990-2000)"', add
label define ancestr1d_lbl 6900 `"Sri Lankan"', add
label define ancestr1d_lbl 6910 `"Singhalese"', add
label define ancestr1d_lbl 6920 `"Veddah"', add
label define ancestr1d_lbl 6950 `"Maldivian"', add
label define ancestr1d_lbl 7000 `"Burmese (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 7001 `"Burmese (1980)"', add
label define ancestr1d_lbl 7002 `"Burman (1980)"', add
label define ancestr1d_lbl 7020 `"Shan"', add
label define ancestr1d_lbl 7030 `"Cambodian"', add
label define ancestr1d_lbl 7040 `"Khmer"', add
label define ancestr1d_lbl 7060 `"Chinese"', add
label define ancestr1d_lbl 7070 `"Cantonese (1980)"', add
label define ancestr1d_lbl 7071 `"Cantonese (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 7072 `"Formosan (1990-2000)"', add
label define ancestr1d_lbl 7080 `"Manchurian"', add
label define ancestr1d_lbl 7090 `"Mandarin (1990-2000)"', add
label define ancestr1d_lbl 7120 `"Mongolian (1980)"', add
label define ancestr1d_lbl 7121 `"Mongolian (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 7122 `"Kalmyk (1990-2000)"', add
label define ancestr1d_lbl 7140 `"Tibetan"', add
label define ancestr1d_lbl 7160 `"Hong Kong (1990-2000)"', add
label define ancestr1d_lbl 7161 `"Hong Kong (1980)"', add
label define ancestr1d_lbl 7162 `"Eastern Archipelago (1980)"', add
label define ancestr1d_lbl 7180 `"Macao"', add
label define ancestr1d_lbl 7200 `"Filipino"', add
label define ancestr1d_lbl 7300 `"Indonesian (1980)"', add
label define ancestr1d_lbl 7301 `"Indonesian (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 7302 `"Borneo (1990-2000)"', add
label define ancestr1d_lbl 7303 `"Java (1990-2000)"', add
label define ancestr1d_lbl 7304 `"Sumatran (1990-2000)"', add
label define ancestr1d_lbl 7400 `"Japanese (1980)"', add
label define ancestr1d_lbl 7401 `"Japanese (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 7402 `"Issei (1990-2000)"', add
label define ancestr1d_lbl 7403 `"Nisei (1990-2000)"', add
label define ancestr1d_lbl 7404 `"Sansei (1990-2000)"', add
label define ancestr1d_lbl 7405 `"Yonsei (1990-2000)"', add
label define ancestr1d_lbl 7406 `"Gosei (1990-2000)"', add
label define ancestr1d_lbl 7460 `"Ryukyu Islander"', add
label define ancestr1d_lbl 7480 `"Okinawan"', add
label define ancestr1d_lbl 7500 `"Korean"', add
label define ancestr1d_lbl 7650 `"Laotian"', add
label define ancestr1d_lbl 7660 `"Meo"', add
label define ancestr1d_lbl 7680 `"Hmong"', add
label define ancestr1d_lbl 7700 `"Malaysian (1980)"', add
label define ancestr1d_lbl 7701 `"Malaysian (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 7702 `"North Borneo (1990-2000)"', add
label define ancestr1d_lbl 7740 `"Singaporean"', add
label define ancestr1d_lbl 7760 `"Thai"', add
label define ancestr1d_lbl 7770 `"Black Thai"', add
label define ancestr1d_lbl 7780 `"Western Lao"', add
label define ancestr1d_lbl 7820 `"Taiwanese"', add
label define ancestr1d_lbl 7850 `"Vietnamese"', add
label define ancestr1d_lbl 7860 `"Katu"', add
label define ancestr1d_lbl 7870 `"Ma"', add
label define ancestr1d_lbl 7880 `"Mnong"', add
label define ancestr1d_lbl 7900 `"Montagnard"', add
label define ancestr1d_lbl 7920 `"Indochinese"', add
label define ancestr1d_lbl 7930 `"Eurasian"', add
label define ancestr1d_lbl 7931 `"Amerasian (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 7950 `"Asian"', add
label define ancestr1d_lbl 7960 `"Other Asian"', add
label define ancestr1d_lbl 8000 `"Australian"', add
label define ancestr1d_lbl 8010 `"Tasmanian"', add
label define ancestr1d_lbl 8020 `"Australian Aborigine (1990-2000)"', add
label define ancestr1d_lbl 8030 `"New Zealander"', add
label define ancestr1d_lbl 8080 `"Polynesian (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 8081 `"Polynesian (1980)"', add
label define ancestr1d_lbl 8082 `"Norfolk Islander (1980)"', add
label define ancestr1d_lbl 8090 `"Kapinagamarangan (1990-2000)"', add
label define ancestr1d_lbl 8091 `"Kapinagamarangan (1980)"', add
label define ancestr1d_lbl 8092 `"Nukuoroan (1980)"', add
label define ancestr1d_lbl 8100 `"Maori"', add
label define ancestr1d_lbl 8110 `"Hawaiian"', add
label define ancestr1d_lbl 8130 `"Part Hawaiian"', add
label define ancestr1d_lbl 8140 `"Samoan (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 8141 `"Samoan (1980)"', add
label define ancestr1d_lbl 8142 `"American Samoan (1980)"', add
label define ancestr1d_lbl 8143 `"French Samoan"', add
label define ancestr1d_lbl 8144 `"Part Samoan (1990-2000)"', add
label define ancestr1d_lbl 8150 `"Tongan"', add
label define ancestr1d_lbl 8160 `"Tokelauan"', add
label define ancestr1d_lbl 8170 `"Cook Islander"', add
label define ancestr1d_lbl 8180 `"Tahitian"', add
label define ancestr1d_lbl 8190 `"Niuean"', add
label define ancestr1d_lbl 8200 `"Micronesian (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 8201 `"Micronesian (1980)"', add
label define ancestr1d_lbl 8202 `"U.S. Trust Terr of the Pacific (1980)"', add
label define ancestr1d_lbl 8210 `"Guamanian"', add
label define ancestr1d_lbl 8220 `"Chamorro Islander"', add
label define ancestr1d_lbl 8230 `"Saipanese (1990-2000)"', add
label define ancestr1d_lbl 8231 `"Saipanese (1980)"', add
label define ancestr1d_lbl 8232 `"Northern Marianas (1980)"', add
label define ancestr1d_lbl 8240 `"Palauan"', add
label define ancestr1d_lbl 8250 `"Marshall Islander"', add
label define ancestr1d_lbl 8260 `"Kosraean"', add
label define ancestr1d_lbl 8270 `"Ponapean (1990-2000)"', add
label define ancestr1d_lbl 8271 `"Ponapean (1980)"', add
label define ancestr1d_lbl 8272 `"Mokilese (1980)"', add
label define ancestr1d_lbl 8273 `"Ngatikese (1980)"', add
label define ancestr1d_lbl 8274 `"Pingelapese (1980)"', add
label define ancestr1d_lbl 8280 `"Chuukese (1990-2000)"', add
label define ancestr1d_lbl 8281 `"Hall Islander (1980)"', add
label define ancestr1d_lbl 8282 `"Mortlockese (1980)"', add
label define ancestr1d_lbl 8283 `"Namanouito (1980)"', add
label define ancestr1d_lbl 8284 `"Pulawatese (1980)"', add
label define ancestr1d_lbl 8285 `"Truk Islander"', add
label define ancestr1d_lbl 8290 `"Yap Islander"', add
label define ancestr1d_lbl 8300 `"Caroline Islander (1990-2000)"', add
label define ancestr1d_lbl 8301 `"Caroline Islander (1980)"', add
label define ancestr1d_lbl 8302 `"Lamotrekese (1980)"', add
label define ancestr1d_lbl 8303 `"Ulithian (1980)"', add
label define ancestr1d_lbl 8304 `"Woleaian (1980)"', add
label define ancestr1d_lbl 8310 `"Kiribatese"', add
label define ancestr1d_lbl 8320 `"Nauruan"', add
label define ancestr1d_lbl 8330 `"Tarawa Islander (1990-2000)"', add
label define ancestr1d_lbl 8340 `"Tinian Islander (1990-2000)"', add
label define ancestr1d_lbl 8400 `"Melanesian Islander"', add
label define ancestr1d_lbl 8410 `"Fijian"', add
label define ancestr1d_lbl 8430 `"New Guinean"', add
label define ancestr1d_lbl 8440 `"Papuan"', add
label define ancestr1d_lbl 8450 `"Solomon Islander"', add
label define ancestr1d_lbl 8460 `"New Caledonian Islander"', add
label define ancestr1d_lbl 8470 `"Vanuatuan"', add
label define ancestr1d_lbl 8500 `"Pacific Islander (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 8501 `"Campbell Islander (1980)"', add
label define ancestr1d_lbl 8502 `"Christmas Islander (1980)"', add
label define ancestr1d_lbl 8503 `"Kermadec Islander (1980)"', add
label define ancestr1d_lbl 8504 `"Midway Islander (1980)"', add
label define ancestr1d_lbl 8505 `"Phoenix Islander (1980)"', add
label define ancestr1d_lbl 8506 `"Wake Islander (1980)"', add
label define ancestr1d_lbl 8600 `"Oceania"', add
label define ancestr1d_lbl 8620 `"Chamolinian (1990-2000)"', add
label define ancestr1d_lbl 8630 `"Reserved Codes"', add
label define ancestr1d_lbl 8700 `"Other Pacific"', add
label define ancestr1d_lbl 9000 `"Afro-American"', add
label define ancestr1d_lbl 9001 `"Afro-American (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 9002 `"Black (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 9003 `"Negro (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 9004 `"Nonwhite (1990-2000)"', add
label define ancestr1d_lbl 9005 `"Colored (1990-2000)"', add
label define ancestr1d_lbl 9006 `"Creole (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 9007 `"Mulatto (1990-2000)"', add
label define ancestr1d_lbl 9008 `"Afro"', add
label define ancestr1d_lbl 9020 `"African-American (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 9130 `"Central American Indian (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 9140 `"South American Indian (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 9200 `"American Indian (all tribes)"', add
label define ancestr1d_lbl 9201 `"American Indian-English-French"', add
label define ancestr1d_lbl 9202 `"American Indian-English-German"', add
label define ancestr1d_lbl 9203 `"American Indian-English-Irish"', add
label define ancestr1d_lbl 9204 `"American Indian-German-Irish"', add
label define ancestr1d_lbl 9205 `"Cherokee"', add
label define ancestr1d_lbl 9206 `"Native American"', add
label define ancestr1d_lbl 9207 `"Indian"', add
label define ancestr1d_lbl 9210 `"Aleut"', add
label define ancestr1d_lbl 9220 `"Eskimo"', add
label define ancestr1d_lbl 9230 `"Inuit"', add
label define ancestr1d_lbl 9240 `"White/Caucasian"', add
label define ancestr1d_lbl 9241 `"White/Caucasian (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 9242 `"Anglo (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 9243 `"Appalachian (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 9244 `"Aryan (1990-2000)"', add
label define ancestr1d_lbl 9300 `"Greenlander"', add
label define ancestr1d_lbl 9310 `"Canadian"', add
label define ancestr1d_lbl 9330 `"Newfoundland"', add
label define ancestr1d_lbl 9340 `"Nova Scotian"', add
label define ancestr1d_lbl 9350 `"French Canadian"', add
label define ancestr1d_lbl 9360 `"Acadian"', add
label define ancestr1d_lbl 9361 `"Acadian (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 9362 `"Cajun (1990-2000, ACS, PRCS)"', add
label define ancestr1d_lbl 9390 `"American"', add
label define ancestr1d_lbl 9391 `"American/United States"', add
label define ancestr1d_lbl 9400 `"United States"', add
label define ancestr1d_lbl 9410 `"Alabama"', add
label define ancestr1d_lbl 9420 `"Alaska"', add
label define ancestr1d_lbl 9430 `"Arizona"', add
label define ancestr1d_lbl 9440 `"Arkansas"', add
label define ancestr1d_lbl 9450 `"California"', add
label define ancestr1d_lbl 9460 `"Colorado"', add
label define ancestr1d_lbl 9470 `"Connecticut"', add
label define ancestr1d_lbl 9480 `"District of Columbia"', add
label define ancestr1d_lbl 9490 `"Delaware"', add
label define ancestr1d_lbl 9500 `"Florida"', add
label define ancestr1d_lbl 9510 `"Georgia"', add
label define ancestr1d_lbl 9520 `"Idaho"', add
label define ancestr1d_lbl 9530 `"Illinois"', add
label define ancestr1d_lbl 9540 `"Indiana"', add
label define ancestr1d_lbl 9550 `"Iowa"', add
label define ancestr1d_lbl 9560 `"Kansas"', add
label define ancestr1d_lbl 9570 `"Kentucky"', add
label define ancestr1d_lbl 9580 `"Louisiana"', add
label define ancestr1d_lbl 9590 `"Maine"', add
label define ancestr1d_lbl 9600 `"Maryland"', add
label define ancestr1d_lbl 9610 `"Massachusetts"', add
label define ancestr1d_lbl 9620 `"Michigan"', add
label define ancestr1d_lbl 9630 `"Minnesota"', add
label define ancestr1d_lbl 9640 `"Mississippi"', add
label define ancestr1d_lbl 9650 `"Missouri"', add
label define ancestr1d_lbl 9660 `"Montana"', add
label define ancestr1d_lbl 9670 `"Nebraska"', add
label define ancestr1d_lbl 9680 `"Nevada"', add
label define ancestr1d_lbl 9690 `"New Hampshire"', add
label define ancestr1d_lbl 9700 `"New Jersey"', add
label define ancestr1d_lbl 9710 `"New Mexico"', add
label define ancestr1d_lbl 9720 `"New York"', add
label define ancestr1d_lbl 9730 `"North Carolina"', add
label define ancestr1d_lbl 9740 `"North Dakota"', add
label define ancestr1d_lbl 9750 `"Ohio"', add
label define ancestr1d_lbl 9760 `"Oklahoma"', add
label define ancestr1d_lbl 9770 `"Oregon"', add
label define ancestr1d_lbl 9780 `"Pennsylvania"', add
label define ancestr1d_lbl 9790 `"Rhode Island"', add
label define ancestr1d_lbl 9800 `"South Carolina"', add
label define ancestr1d_lbl 9810 `"South Dakota"', add
label define ancestr1d_lbl 9820 `"Tennessee"', add
label define ancestr1d_lbl 9830 `"Texas"', add
label define ancestr1d_lbl 9840 `"Utah"', add
label define ancestr1d_lbl 9850 `"Vermont"', add
label define ancestr1d_lbl 9860 `"Virginia"', add
label define ancestr1d_lbl 9870 `"Washington"', add
label define ancestr1d_lbl 9880 `"West Virginia"', add
label define ancestr1d_lbl 9890 `"Wisconsin"', add
label define ancestr1d_lbl 9900 `"Wyoming"', add
label define ancestr1d_lbl 9930 `"Southerner"', add
label define ancestr1d_lbl 9940 `"North American"', add
label define ancestr1d_lbl 9950 `"Mixture"', add
label define ancestr1d_lbl 9960 `"Uncodable"', add
label define ancestr1d_lbl 9961 `"Not Classified"', add
label define ancestr1d_lbl 9962 `"Suppressed"', add
label define ancestr1d_lbl 9980 `"Other"', add
label define ancestr1d_lbl 9990 `"Not Reported"', add
label values ancestr1d ancestr1d_lbl

label define ancestr2_lbl 001 `"Alsatian, Alsace-Lorraine"'
label define ancestr2_lbl 002 `"Andorran"', add
label define ancestr2_lbl 003 `"Austrian"', add
label define ancestr2_lbl 004 `"Tirolean"', add
label define ancestr2_lbl 005 `"Basque"', add
label define ancestr2_lbl 006 `"French Basque"', add
label define ancestr2_lbl 008 `"Belgian"', add
label define ancestr2_lbl 009 `"Flemish"', add
label define ancestr2_lbl 010 `"Walloon"', add
label define ancestr2_lbl 011 `"British"', add
label define ancestr2_lbl 012 `"British Isles"', add
label define ancestr2_lbl 013 `"Channel Islander"', add
label define ancestr2_lbl 014 `"Gibraltan"', add
label define ancestr2_lbl 015 `"Cornish"', add
label define ancestr2_lbl 016 `"Corsican"', add
label define ancestr2_lbl 017 `"Cypriot"', add
label define ancestr2_lbl 018 `"Greek Cypriote"', add
label define ancestr2_lbl 019 `"Turkish Cypriote"', add
label define ancestr2_lbl 020 `"Danish"', add
label define ancestr2_lbl 021 `"Dutch"', add
label define ancestr2_lbl 022 `"English"', add
label define ancestr2_lbl 023 `"Faeroe Islander"', add
label define ancestr2_lbl 024 `"Finnish"', add
label define ancestr2_lbl 025 `"Karelian"', add
label define ancestr2_lbl 026 `"French"', add
label define ancestr2_lbl 027 `"Lorrainian"', add
label define ancestr2_lbl 028 `"Breton"', add
label define ancestr2_lbl 029 `"Frisian"', add
label define ancestr2_lbl 030 `"Friulian"', add
label define ancestr2_lbl 032 `"German"', add
label define ancestr2_lbl 033 `"Bavarian"', add
label define ancestr2_lbl 034 `"Berliner"', add
label define ancestr2_lbl 035 `"Hamburger"', add
label define ancestr2_lbl 036 `"Hanoverian"', add
label define ancestr2_lbl 037 `"Hessian"', add
label define ancestr2_lbl 038 `"Lubecker"', add
label define ancestr2_lbl 039 `"Pomeranian"', add
label define ancestr2_lbl 040 `"Prussian"', add
label define ancestr2_lbl 041 `"Saxon"', add
label define ancestr2_lbl 042 `"Sudetenlander"', add
label define ancestr2_lbl 043 `"Westphalian"', add
label define ancestr2_lbl 046 `"Greek"', add
label define ancestr2_lbl 047 `"Cretan"', add
label define ancestr2_lbl 048 `"Cycladic Islander"', add
label define ancestr2_lbl 049 `"Icelander"', add
label define ancestr2_lbl 050 `"Irish"', add
label define ancestr2_lbl 051 `"Italian"', add
label define ancestr2_lbl 053 `"Abruzzi"', add
label define ancestr2_lbl 054 `"Apulian"', add
label define ancestr2_lbl 055 `"Basilicata"', add
label define ancestr2_lbl 056 `"Calabrian"', add
label define ancestr2_lbl 057 `"Amalfin"', add
label define ancestr2_lbl 058 `"Emilia Romagna"', add
label define ancestr2_lbl 059 `"Rome"', add
label define ancestr2_lbl 060 `"Ligurian"', add
label define ancestr2_lbl 061 `"Lombardian"', add
label define ancestr2_lbl 062 `"Marches"', add
label define ancestr2_lbl 063 `"Molise"', add
label define ancestr2_lbl 064 `"Neapolitan"', add
label define ancestr2_lbl 065 `"Piedmontese"', add
label define ancestr2_lbl 066 `"Puglia"', add
label define ancestr2_lbl 067 `"Sardinian"', add
label define ancestr2_lbl 068 `"Sicilian"', add
label define ancestr2_lbl 069 `"Toscana"', add
label define ancestr2_lbl 070 `"Trentino"', add
label define ancestr2_lbl 071 `"Umbrian"', add
label define ancestr2_lbl 072 `"Valle dAosta"', add
label define ancestr2_lbl 073 `"Venetian"', add
label define ancestr2_lbl 075 `"Lapp"', add
label define ancestr2_lbl 076 `"Liechtensteiner"', add
label define ancestr2_lbl 077 `"Luxemburger"', add
label define ancestr2_lbl 078 `"Maltese"', add
label define ancestr2_lbl 079 `"Manx"', add
label define ancestr2_lbl 080 `"Monegasque"', add
label define ancestr2_lbl 081 `"Northern Irelander"', add
label define ancestr2_lbl 082 `"Norwegian"', add
label define ancestr2_lbl 084 `"Portuguese"', add
label define ancestr2_lbl 085 `"Azorean"', add
label define ancestr2_lbl 086 `"Madeiran"', add
label define ancestr2_lbl 087 `"Scotch Irish"', add
label define ancestr2_lbl 088 `"Scottish"', add
label define ancestr2_lbl 089 `"Swedish"', add
label define ancestr2_lbl 090 `"Aland Islander"', add
label define ancestr2_lbl 091 `"Swiss"', add
label define ancestr2_lbl 092 `"Suisse"', add
label define ancestr2_lbl 095 `"Romansch"', add
label define ancestr2_lbl 096 `"Suisse Romane"', add
label define ancestr2_lbl 097 `"Welsh"', add
label define ancestr2_lbl 098 `"Scandinavian, Nordic"', add
label define ancestr2_lbl 100 `"Albanian"', add
label define ancestr2_lbl 101 `"Azerbaijani"', add
label define ancestr2_lbl 102 `"Belourussian"', add
label define ancestr2_lbl 103 `"Bulgarian"', add
label define ancestr2_lbl 105 `"Carpathian"', add
label define ancestr2_lbl 108 `"Cossack"', add
label define ancestr2_lbl 109 `"Croatian"', add
label define ancestr2_lbl 111 `"Czechoslovakian"', add
label define ancestr2_lbl 112 `"Bohemian"', add
label define ancestr2_lbl 115 `"Estonian"', add
label define ancestr2_lbl 116 `"Livonian"', add
label define ancestr2_lbl 117 `"Finno Ugrian"', add
label define ancestr2_lbl 118 `"Mordovian"', add
label define ancestr2_lbl 119 `"Voytak"', add
label define ancestr2_lbl 120 `"Georgian"', add
label define ancestr2_lbl 122 `"Germans from Russia"', add
label define ancestr2_lbl 123 `"Gruziia"', add
label define ancestr2_lbl 124 `"Rom"', add
label define ancestr2_lbl 125 `"Hungarian"', add
label define ancestr2_lbl 126 `"Magyar"', add
label define ancestr2_lbl 128 `"Latvian"', add
label define ancestr2_lbl 129 `"Lithuanian"', add
label define ancestr2_lbl 130 `"Macedonian"', add
label define ancestr2_lbl 132 `"North Caucasian"', add
label define ancestr2_lbl 133 `"North Caucasian Turkic"', add
label define ancestr2_lbl 140 `"Ossetian"', add
label define ancestr2_lbl 142 `"Polish"', add
label define ancestr2_lbl 143 `"Kashubian"', add
label define ancestr2_lbl 144 `"Romanian"', add
label define ancestr2_lbl 145 `"Bessarabian"', add
label define ancestr2_lbl 146 `"Moldavian"', add
label define ancestr2_lbl 147 `"Wallachian"', add
label define ancestr2_lbl 148 `"Russian"', add
label define ancestr2_lbl 150 `"Muscovite"', add
label define ancestr2_lbl 152 `"Serbian"', add
label define ancestr2_lbl 153 `"Slovak"', add
label define ancestr2_lbl 154 `"Slovene"', add
label define ancestr2_lbl 155 `"Sorb/Wend"', add
label define ancestr2_lbl 156 `"Soviet Turkic"', add
label define ancestr2_lbl 157 `"Bashkir"', add
label define ancestr2_lbl 158 `"Chevash"', add
label define ancestr2_lbl 159 `"Gagauz"', add
label define ancestr2_lbl 160 `"Mesknetian"', add
label define ancestr2_lbl 163 `"Yakut"', add
label define ancestr2_lbl 164 `"Soviet Union, nec"', add
label define ancestr2_lbl 165 `"Tatar"', add
label define ancestr2_lbl 169 `"Uzbek"', add
label define ancestr2_lbl 171 `"Ukrainian"', add
label define ancestr2_lbl 176 `"Yugoslavian"', add
label define ancestr2_lbl 178 `"Slav"', add
label define ancestr2_lbl 179 `"Slavonian"', add
label define ancestr2_lbl 181 `"Central European, nec"', add
label define ancestr2_lbl 183 `"Northern European, nec"', add
label define ancestr2_lbl 185 `"Southern European, nec"', add
label define ancestr2_lbl 187 `"Western European, nec"', add
label define ancestr2_lbl 190 `"Eastern European, nec"', add
label define ancestr2_lbl 195 `"European, nec"', add
label define ancestr2_lbl 200 `"Spaniard"', add
label define ancestr2_lbl 201 `"Andalusian"', add
label define ancestr2_lbl 202 `"Astorian"', add
label define ancestr2_lbl 204 `"Catalonian"', add
label define ancestr2_lbl 205 `"Balearic Islander"', add
label define ancestr2_lbl 206 `"Galician"', add
label define ancestr2_lbl 210 `"Mexican"', add
label define ancestr2_lbl 211 `"Mexican American"', add
label define ancestr2_lbl 213 `"Chicano/Chicana"', add
label define ancestr2_lbl 218 `"Nuevo Mexicano"', add
label define ancestr2_lbl 219 `"Californio"', add
label define ancestr2_lbl 221 `"Costa Rican"', add
label define ancestr2_lbl 222 `"Guatemalan"', add
label define ancestr2_lbl 223 `"Honduran"', add
label define ancestr2_lbl 224 `"Nicaraguan"', add
label define ancestr2_lbl 225 `"Panamanian"', add
label define ancestr2_lbl 226 `"Salvadoran"', add
label define ancestr2_lbl 227 `"Latin American"', add
label define ancestr2_lbl 231 `"Argentinean"', add
label define ancestr2_lbl 232 `"Bolivian"', add
label define ancestr2_lbl 233 `"Chilean"', add
label define ancestr2_lbl 234 `"Colombian"', add
label define ancestr2_lbl 235 `"Ecuadorian"', add
label define ancestr2_lbl 236 `"Paraguayan"', add
label define ancestr2_lbl 237 `"Peruvian"', add
label define ancestr2_lbl 238 `"Uruguayan"', add
label define ancestr2_lbl 239 `"Venezuelan"', add
label define ancestr2_lbl 248 `"South American"', add
label define ancestr2_lbl 261 `"Puerto Rican"', add
label define ancestr2_lbl 271 `"Cuban"', add
label define ancestr2_lbl 275 `"Dominican"', add
label define ancestr2_lbl 290 `"Hispanic"', add
label define ancestr2_lbl 291 `"Spanish"', add
label define ancestr2_lbl 295 `"Spanish American"', add
label define ancestr2_lbl 296 `"Other Spanish/Hispanic"', add
label define ancestr2_lbl 300 `"Bahamian"', add
label define ancestr2_lbl 301 `"Barbadian"', add
label define ancestr2_lbl 302 `"Belizean"', add
label define ancestr2_lbl 303 `"Bermudan"', add
label define ancestr2_lbl 304 `"Cayman Islander"', add
label define ancestr2_lbl 308 `"Jamaican"', add
label define ancestr2_lbl 310 `"Dutch West Indies"', add
label define ancestr2_lbl 311 `"Aruba Islander"', add
label define ancestr2_lbl 312 `"St Maarten Islander"', add
label define ancestr2_lbl 314 `"Trinidadian/Tobagonian"', add
label define ancestr2_lbl 315 `"Trinidadian"', add
label define ancestr2_lbl 316 `"Tobagonian"', add
label define ancestr2_lbl 317 `"U.S. Virgin Islander"', add
label define ancestr2_lbl 321 `"British Virgin Islander"', add
label define ancestr2_lbl 322 `"British West Indian"', add
label define ancestr2_lbl 323 `"Turks and Caicos Islander"', add
label define ancestr2_lbl 324 `"Anguilla Islander"', add
label define ancestr2_lbl 328 `"Dominica Islander"', add
label define ancestr2_lbl 329 `"Grenadian"', add
label define ancestr2_lbl 331 `"St Lucia Islander"', add
label define ancestr2_lbl 332 `"French West Indies"', add
label define ancestr2_lbl 333 `"Guadeloupe Islander"', add
label define ancestr2_lbl 334 `"Cayenne"', add
label define ancestr2_lbl 335 `"West Indian"', add
label define ancestr2_lbl 336 `"Haitian"', add
label define ancestr2_lbl 337 `"Other West Indian"', add
label define ancestr2_lbl 360 `"Brazilian"', add
label define ancestr2_lbl 365 `"San Andres"', add
label define ancestr2_lbl 370 `"Guyanese/British Guiana"', add
label define ancestr2_lbl 375 `"Providencia"', add
label define ancestr2_lbl 380 `"Surinam/Dutch Guiana"', add
label define ancestr2_lbl 400 `"Algerian"', add
label define ancestr2_lbl 402 `"Egyptian"', add
label define ancestr2_lbl 404 `"Libyan"', add
label define ancestr2_lbl 406 `"Moroccan"', add
label define ancestr2_lbl 407 `"Ifni"', add
label define ancestr2_lbl 408 `"Tunisian"', add
label define ancestr2_lbl 411 `"North African"', add
label define ancestr2_lbl 412 `"Alhucemas"', add
label define ancestr2_lbl 413 `"Berber"', add
label define ancestr2_lbl 414 `"Rio de Oro"', add
label define ancestr2_lbl 415 `"Bahraini"', add
label define ancestr2_lbl 416 `"Iranian"', add
label define ancestr2_lbl 417 `"Iraqi"', add
label define ancestr2_lbl 419 `"Israeli"', add
label define ancestr2_lbl 421 `"Jordanian"', add
label define ancestr2_lbl 422 `"Transjordan"', add
label define ancestr2_lbl 423 `"Kuwaiti"', add
label define ancestr2_lbl 425 `"Lebanese"', add
label define ancestr2_lbl 427 `"Saudi Arabian"', add
label define ancestr2_lbl 429 `"Syrian"', add
label define ancestr2_lbl 431 `"Armenian"', add
label define ancestr2_lbl 434 `"Turkish"', add
label define ancestr2_lbl 435 `"Yemeni"', add
label define ancestr2_lbl 436 `"Omani"', add
label define ancestr2_lbl 437 `"Muscat"', add
label define ancestr2_lbl 438 `"Trucial Oman"', add
label define ancestr2_lbl 439 `"Qatar"', add
label define ancestr2_lbl 441 `"Bedouin"', add
label define ancestr2_lbl 442 `"Kurdish"', add
label define ancestr2_lbl 444 `"Kuria Muria Islander"', add
label define ancestr2_lbl 465 `"Palestinian"', add
label define ancestr2_lbl 466 `"Gazan"', add
label define ancestr2_lbl 467 `"West Bank"', add
label define ancestr2_lbl 470 `"South Yemeni"', add
label define ancestr2_lbl 471 `"Aden"', add
label define ancestr2_lbl 480 `"United Arab Emirates"', add
label define ancestr2_lbl 482 `"Assyrian/Chaldean/Syriac"', add
label define ancestr2_lbl 490 `"Middle Eastern"', add
label define ancestr2_lbl 495 `"Arab"', add
label define ancestr2_lbl 496 `"Other Arab"', add
label define ancestr2_lbl 500 `"Angolan"', add
label define ancestr2_lbl 502 `"Benin"', add
label define ancestr2_lbl 504 `"Botswana"', add
label define ancestr2_lbl 506 `"Burundian"', add
label define ancestr2_lbl 508 `"Cameroonian"', add
label define ancestr2_lbl 510 `"Cape Verdean"', add
label define ancestr2_lbl 513 `"Chadian"', add
label define ancestr2_lbl 515 `"Congolese"', add
label define ancestr2_lbl 516 `"Congo-Brazzaville"', add
label define ancestr2_lbl 519 `"Djibouti"', add
label define ancestr2_lbl 520 `"Equatorial Guinea"', add
label define ancestr2_lbl 521 `"Corsico Islander"', add
label define ancestr2_lbl 522 `"Ethiopian"', add
label define ancestr2_lbl 523 `"Eritrean"', add
label define ancestr2_lbl 525 `"Gabonese"', add
label define ancestr2_lbl 527 `"Gambian"', add
label define ancestr2_lbl 529 `"Ghanian"', add
label define ancestr2_lbl 530 `"Guinean"', add
label define ancestr2_lbl 531 `"Guinea Bissau"', add
label define ancestr2_lbl 532 `"Ivory Coast"', add
label define ancestr2_lbl 534 `"Kenyan"', add
label define ancestr2_lbl 538 `"Lesotho"', add
label define ancestr2_lbl 541 `"Liberian"', add
label define ancestr2_lbl 543 `"Madagascan"', add
label define ancestr2_lbl 545 `"Malawian"', add
label define ancestr2_lbl 546 `"Malian"', add
label define ancestr2_lbl 547 `"Mauritanian"', add
label define ancestr2_lbl 549 `"Mozambican"', add
label define ancestr2_lbl 550 `"Namibian"', add
label define ancestr2_lbl 551 `"Niger"', add
label define ancestr2_lbl 553 `"Nigerian"', add
label define ancestr2_lbl 554 `"Fulani"', add
label define ancestr2_lbl 555 `"Hausa"', add
label define ancestr2_lbl 556 `"Ibo"', add
label define ancestr2_lbl 557 `"Tiv"', add
label define ancestr2_lbl 561 `"Rwandan"', add
label define ancestr2_lbl 564 `"Senegalese"', add
label define ancestr2_lbl 566 `"Sierra Leonean"', add
label define ancestr2_lbl 568 `"Somalian"', add
label define ancestr2_lbl 569 `"Swaziland"', add
label define ancestr2_lbl 570 `"South African"', add
label define ancestr2_lbl 571 `"Union of South Africa"', add
label define ancestr2_lbl 572 `"Afrikaner"', add
label define ancestr2_lbl 573 `"Natalian"', add
label define ancestr2_lbl 574 `"Zulu"', add
label define ancestr2_lbl 576 `"Sudanese"', add
label define ancestr2_lbl 577 `"Dinka"', add
label define ancestr2_lbl 578 `"Nuer"', add
label define ancestr2_lbl 579 `"Fur"', add
label define ancestr2_lbl 580 `"Baggara"', add
label define ancestr2_lbl 582 `"Tanzanian"', add
label define ancestr2_lbl 583 `"Tanganyikan"', add
label define ancestr2_lbl 584 `"Zanzibar Islande"', add
label define ancestr2_lbl 586 `"Togo"', add
label define ancestr2_lbl 588 `"Ugandan"', add
label define ancestr2_lbl 589 `"Upper Voltan"', add
label define ancestr2_lbl 590 `"Voltan"', add
label define ancestr2_lbl 591 `"Zairian"', add
label define ancestr2_lbl 592 `"Zambian"', add
label define ancestr2_lbl 593 `"Zimbabwean"', add
label define ancestr2_lbl 594 `"African Islands"', add
label define ancestr2_lbl 595 `"Other Subsaharan Africa"', add
label define ancestr2_lbl 596 `"Central African"', add
label define ancestr2_lbl 597 `"East African"', add
label define ancestr2_lbl 598 `"West African"', add
label define ancestr2_lbl 599 `"African"', add
label define ancestr2_lbl 600 `"Afghan"', add
label define ancestr2_lbl 601 `"Baluchi"', add
label define ancestr2_lbl 602 `"Pathan"', add
label define ancestr2_lbl 603 `"Bengali"', add
label define ancestr2_lbl 607 `"Bhutanese"', add
label define ancestr2_lbl 609 `"Nepali"', add
label define ancestr2_lbl 615 `"Asian Indian"', add
label define ancestr2_lbl 622 `"Andaman Islander"', add
label define ancestr2_lbl 624 `"Andhra Pradesh"', add
label define ancestr2_lbl 626 `"Assamese"', add
label define ancestr2_lbl 628 `"Goanese"', add
label define ancestr2_lbl 630 `"Gujarati"', add
label define ancestr2_lbl 632 `"Karnatakan"', add
label define ancestr2_lbl 634 `"Keralan"', add
label define ancestr2_lbl 638 `"Maharashtran"', add
label define ancestr2_lbl 640 `"Madrasi"', add
label define ancestr2_lbl 642 `"Mysore"', add
label define ancestr2_lbl 644 `"Naga"', add
label define ancestr2_lbl 648 `"Pondicherry"', add
label define ancestr2_lbl 650 `"Punjabi"', add
label define ancestr2_lbl 656 `"Tamil"', add
label define ancestr2_lbl 675 `"East Indies"', add
label define ancestr2_lbl 680 `"Pakistani"', add
label define ancestr2_lbl 690 `"Sri Lankan"', add
label define ancestr2_lbl 691 `"Singhalese"', add
label define ancestr2_lbl 692 `"Veddah"', add
label define ancestr2_lbl 695 `"Maldivian"', add
label define ancestr2_lbl 700 `"Burmese"', add
label define ancestr2_lbl 702 `"Shan"', add
label define ancestr2_lbl 703 `"Cambodian"', add
label define ancestr2_lbl 704 `"Khmer"', add
label define ancestr2_lbl 706 `"Chinese"', add
label define ancestr2_lbl 707 `"Cantonese"', add
label define ancestr2_lbl 708 `"Manchurian"', add
label define ancestr2_lbl 709 `"Mandarin"', add
label define ancestr2_lbl 712 `"Mongolian"', add
label define ancestr2_lbl 714 `"Tibetan"', add
label define ancestr2_lbl 716 `"Hong Kong"', add
label define ancestr2_lbl 718 `"Macao"', add
label define ancestr2_lbl 720 `"Filipino"', add
label define ancestr2_lbl 730 `"Indonesian"', add
label define ancestr2_lbl 740 `"Japanese"', add
label define ancestr2_lbl 746 `"Ryukyu Islander"', add
label define ancestr2_lbl 748 `"Okinawan"', add
label define ancestr2_lbl 750 `"Korean"', add
label define ancestr2_lbl 765 `"Laotian"', add
label define ancestr2_lbl 766 `"Meo"', add
label define ancestr2_lbl 768 `"Hmong"', add
label define ancestr2_lbl 770 `"Malaysian"', add
label define ancestr2_lbl 774 `"Singaporean"', add
label define ancestr2_lbl 776 `"Thai"', add
label define ancestr2_lbl 777 `"Black Thai"', add
label define ancestr2_lbl 778 `"Western Lao"', add
label define ancestr2_lbl 782 `"Taiwanese"', add
label define ancestr2_lbl 785 `"Vietnamese"', add
label define ancestr2_lbl 786 `"Katu"', add
label define ancestr2_lbl 787 `"Ma"', add
label define ancestr2_lbl 788 `"Mnong"', add
label define ancestr2_lbl 790 `"Montagnard"', add
label define ancestr2_lbl 792 `"Indochinese"', add
label define ancestr2_lbl 793 `"Eurasian"', add
label define ancestr2_lbl 795 `"Asian"', add
label define ancestr2_lbl 796 `"Other Asian"', add
label define ancestr2_lbl 800 `"Australian"', add
label define ancestr2_lbl 801 `"Tasmanian"', add
label define ancestr2_lbl 802 `"Australian Aborigine"', add
label define ancestr2_lbl 803 `"New Zealander"', add
label define ancestr2_lbl 808 `"Polynesian"', add
label define ancestr2_lbl 809 `"Kapinagamarangan"', add
label define ancestr2_lbl 810 `"Maori"', add
label define ancestr2_lbl 811 `"Hawaiian"', add
label define ancestr2_lbl 813 `"Part Hawaiian"', add
label define ancestr2_lbl 814 `"Samoan"', add
label define ancestr2_lbl 815 `"Tongan"', add
label define ancestr2_lbl 816 `"Tokelauan"', add
label define ancestr2_lbl 817 `"Cook Islander"', add
label define ancestr2_lbl 818 `"Tahitian"', add
label define ancestr2_lbl 819 `"Niuean"', add
label define ancestr2_lbl 820 `"Micronesian"', add
label define ancestr2_lbl 821 `"Guamanian"', add
label define ancestr2_lbl 822 `"Chamorro Islander"', add
label define ancestr2_lbl 823 `"Saipanese"', add
label define ancestr2_lbl 824 `"Palauan"', add
label define ancestr2_lbl 825 `"Marshall Islander"', add
label define ancestr2_lbl 826 `"Kosraean"', add
label define ancestr2_lbl 827 `"Ponapean"', add
label define ancestr2_lbl 828 `"Chuukese"', add
label define ancestr2_lbl 829 `"Yap Islander"', add
label define ancestr2_lbl 830 `"Caroline Islander"', add
label define ancestr2_lbl 831 `"Kiribatese"', add
label define ancestr2_lbl 832 `"Nauruan"', add
label define ancestr2_lbl 833 `"Tarawa Islander"', add
label define ancestr2_lbl 834 `"Tinian Islander"', add
label define ancestr2_lbl 840 `"Melanesian Islander"', add
label define ancestr2_lbl 841 `"Fijian"', add
label define ancestr2_lbl 843 `"New Guinean"', add
label define ancestr2_lbl 844 `"Papuan"', add
label define ancestr2_lbl 845 `"Solomon Islander"', add
label define ancestr2_lbl 846 `"New Caledonian Islander"', add
label define ancestr2_lbl 847 `"Vanuatuan"', add
label define ancestr2_lbl 850 `"Pacific Islander"', add
label define ancestr2_lbl 860 `"Oceania"', add
label define ancestr2_lbl 862 `"Chamolinian"', add
label define ancestr2_lbl 863 `"Reserved Codes"', add
label define ancestr2_lbl 870 `"Other Pacific"', add
label define ancestr2_lbl 900 `"Afro-American"', add
label define ancestr2_lbl 902 `"African-American"', add
label define ancestr2_lbl 913 `"Central American Indian"', add
label define ancestr2_lbl 914 `"South American Indian"', add
label define ancestr2_lbl 920 `"American Indian  (all tribes)"', add
label define ancestr2_lbl 921 `"Aleut"', add
label define ancestr2_lbl 922 `"Eskimo"', add
label define ancestr2_lbl 923 `"Inuit"', add
label define ancestr2_lbl 924 `"White/Caucasian"', add
label define ancestr2_lbl 930 `"Greenlander"', add
label define ancestr2_lbl 931 `"Canadian (most provinces)"', add
label define ancestr2_lbl 933 `"Newfoundland"', add
label define ancestr2_lbl 934 `"Nova Scotian"', add
label define ancestr2_lbl 935 `"French Canadian"', add
label define ancestr2_lbl 936 `"Acadian"', add
label define ancestr2_lbl 939 `"American"', add
label define ancestr2_lbl 940 `"United States"', add
label define ancestr2_lbl 941 `"Alabama"', add
label define ancestr2_lbl 942 `"Alaska"', add
label define ancestr2_lbl 943 `"Arizona"', add
label define ancestr2_lbl 944 `"Arkansas"', add
label define ancestr2_lbl 945 `"California"', add
label define ancestr2_lbl 946 `"Colorado"', add
label define ancestr2_lbl 947 `"Connecticut"', add
label define ancestr2_lbl 948 `"District of Columbia"', add
label define ancestr2_lbl 949 `"Delaware"', add
label define ancestr2_lbl 950 `"Florida"', add
label define ancestr2_lbl 951 `"Georgia"', add
label define ancestr2_lbl 952 `"Idaho"', add
label define ancestr2_lbl 953 `"Illinois"', add
label define ancestr2_lbl 954 `"Indiana"', add
label define ancestr2_lbl 955 `"Iowa"', add
label define ancestr2_lbl 956 `"Kansas"', add
label define ancestr2_lbl 957 `"Kentucky"', add
label define ancestr2_lbl 958 `"Louisiana"', add
label define ancestr2_lbl 959 `"Maine"', add
label define ancestr2_lbl 960 `"Maryland"', add
label define ancestr2_lbl 961 `"Massachusetts"', add
label define ancestr2_lbl 962 `"Michigan"', add
label define ancestr2_lbl 963 `"Minnesota"', add
label define ancestr2_lbl 964 `"Mississippi"', add
label define ancestr2_lbl 965 `"Missouri"', add
label define ancestr2_lbl 966 `"Montana"', add
label define ancestr2_lbl 967 `"Nebraska"', add
label define ancestr2_lbl 968 `"Nevada"', add
label define ancestr2_lbl 969 `"New Hampshire"', add
label define ancestr2_lbl 970 `"New Jersey"', add
label define ancestr2_lbl 971 `"New Mexico"', add
label define ancestr2_lbl 972 `"New York"', add
label define ancestr2_lbl 973 `"North Carolina"', add
label define ancestr2_lbl 974 `"North Dakota"', add
label define ancestr2_lbl 975 `"Ohio"', add
label define ancestr2_lbl 976 `"Oklahoma"', add
label define ancestr2_lbl 977 `"Oregon"', add
label define ancestr2_lbl 978 `"Pennsylvania"', add
label define ancestr2_lbl 979 `"Rhode Island"', add
label define ancestr2_lbl 980 `"South Carolina"', add
label define ancestr2_lbl 981 `"South Dakota"', add
label define ancestr2_lbl 982 `"Tennessee"', add
label define ancestr2_lbl 983 `"Texas"', add
label define ancestr2_lbl 984 `"Utah"', add
label define ancestr2_lbl 985 `"Vermont"', add
label define ancestr2_lbl 986 `"Virginia"', add
label define ancestr2_lbl 987 `"Washington"', add
label define ancestr2_lbl 988 `"West Virginia"', add
label define ancestr2_lbl 989 `"Wisconsin"', add
label define ancestr2_lbl 990 `"Wyoming"', add
label define ancestr2_lbl 993 `"Southerner"', add
label define ancestr2_lbl 994 `"North American"', add
label define ancestr2_lbl 995 `"Mixture"', add
label define ancestr2_lbl 996 `"Uncodable"', add
label define ancestr2_lbl 997 `"Deferred Cases"', add
label define ancestr2_lbl 998 `"Other (Usually a Religion)"', add
label define ancestr2_lbl 999 `"Not Reported"', add
label values ancestr2 ancestr2_lbl

label define ancestr2d_lbl 0010 `"Alsatian"'
label define ancestr2d_lbl 0020 `"Andorran"', add
label define ancestr2d_lbl 0030 `"Austrian"', add
label define ancestr2d_lbl 0040 `"Tirolean"', add
label define ancestr2d_lbl 0051 `"Basque (1980)"', add
label define ancestr2d_lbl 0052 `"Spanish Basque (1980)"', add
label define ancestr2d_lbl 0053 `"Basque (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 0054 `"Spanish Basque (1990-2000, 2001-2004 ACS)"', add
label define ancestr2d_lbl 0060 `"French Basque"', add
label define ancestr2d_lbl 0080 `"Belgian"', add
label define ancestr2d_lbl 0090 `"Flemish"', add
label define ancestr2d_lbl 0100 `"Walloon"', add
label define ancestr2d_lbl 0110 `"British"', add
label define ancestr2d_lbl 0120 `"British Isles"', add
label define ancestr2d_lbl 0130 `"Channel Islander"', add
label define ancestr2d_lbl 0140 `"Gibraltan"', add
label define ancestr2d_lbl 0150 `"Cornish"', add
label define ancestr2d_lbl 0160 `"Corsican"', add
label define ancestr2d_lbl 0170 `"Cypriot"', add
label define ancestr2d_lbl 0180 `"Greek Cypriote"', add
label define ancestr2d_lbl 0190 `"Turkish Cypriote"', add
label define ancestr2d_lbl 0200 `"Danish"', add
label define ancestr2d_lbl 0210 `"Dutch"', add
label define ancestr2d_lbl 0211 `"Dutch-French-Irish"', add
label define ancestr2d_lbl 0212 `"Dutch-German-Irish"', add
label define ancestr2d_lbl 0213 `"Dutch-Irish-Scotch"', add
label define ancestr2d_lbl 0220 `"English"', add
label define ancestr2d_lbl 0221 `"English-French-German (1980)"', add
label define ancestr2d_lbl 0222 `"English-French-Irish (1980)"', add
label define ancestr2d_lbl 0223 `"English-German-Irish (1980)"', add
label define ancestr2d_lbl 0224 `"English-German-Swedish (1980)"', add
label define ancestr2d_lbl 0225 `"English-Irish-Scotch (1980)"', add
label define ancestr2d_lbl 0226 `"English-Scotch-Welsh (1980)"', add
label define ancestr2d_lbl 0230 `"Faeroe Islander"', add
label define ancestr2d_lbl 0240 `"Finnish"', add
label define ancestr2d_lbl 0250 `"Karelian"', add
label define ancestr2d_lbl 0260 `"French (1980)"', add
label define ancestr2d_lbl 0261 `"French (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 0262 `"Occitan (1990-2000)"', add
label define ancestr2d_lbl 0270 `"Lorrainian"', add
label define ancestr2d_lbl 0280 `"Breton"', add
label define ancestr2d_lbl 0290 `"Frisian"', add
label define ancestr2d_lbl 0300 `"Friulian"', add
label define ancestr2d_lbl 0320 `"German (1980)"', add
label define ancestr2d_lbl 0321 `"German (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 0322 `"Pennsylvania German (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 0323 `"East German (1990-2000)"', add
label define ancestr2d_lbl 0324 `"West German (2000)"', add
label define ancestr2d_lbl 0325 `"German-French-Irish (1980)"', add
label define ancestr2d_lbl 0326 `"German-Irish-Italian (1980)"', add
label define ancestr2d_lbl 0327 `"German-Irish-Scotch (1980)"', add
label define ancestr2d_lbl 0328 `"German-Irish-Swedish (1980)"', add
label define ancestr2d_lbl 0329 `"Germanic"', add
label define ancestr2d_lbl 0330 `"Bavarian"', add
label define ancestr2d_lbl 0340 `"Berliner"', add
label define ancestr2d_lbl 0350 `"Hamburger"', add
label define ancestr2d_lbl 0360 `"Hanoverian"', add
label define ancestr2d_lbl 0370 `"Hessian"', add
label define ancestr2d_lbl 0380 `"Lubecker"', add
label define ancestr2d_lbl 0390 `"Pomeranian (1980)"', add
label define ancestr2d_lbl 0391 `"Pomeranian (1990-2000)"', add
label define ancestr2d_lbl 0392 `"Silesian (1990-2000)"', add
label define ancestr2d_lbl 0400 `"Prussian"', add
label define ancestr2d_lbl 0410 `"Saxon"', add
label define ancestr2d_lbl 0420 `"Sudetenlander"', add
label define ancestr2d_lbl 0430 `"Westphalian"', add
label define ancestr2d_lbl 0460 `"Greek"', add
label define ancestr2d_lbl 0470 `"Cretan"', add
label define ancestr2d_lbl 0480 `"Cycladic Islander"', add
label define ancestr2d_lbl 0490 `"Icelander"', add
label define ancestr2d_lbl 0500 `"Irish"', add
label define ancestr2d_lbl 0501 `"Celtic"', add
label define ancestr2d_lbl 0502 `"Irish Scotch"', add
label define ancestr2d_lbl 0510 `"Italian (1980)"', add
label define ancestr2d_lbl 0511 `"Italian (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 0512 `"Trieste (1990-2000)"', add
label define ancestr2d_lbl 0513 `"San Marino (1990-2000)"', add
label define ancestr2d_lbl 0530 `"Abruzzi"', add
label define ancestr2d_lbl 0540 `"Apulian"', add
label define ancestr2d_lbl 0550 `"Basilicata"', add
label define ancestr2d_lbl 0560 `"Calabrian"', add
label define ancestr2d_lbl 0570 `"Amalfi"', add
label define ancestr2d_lbl 0580 `"Emilia Romagna"', add
label define ancestr2d_lbl 0590 `"Rome"', add
label define ancestr2d_lbl 0600 `"Ligurian"', add
label define ancestr2d_lbl 0610 `"Lombardian"', add
label define ancestr2d_lbl 0620 `"Marches"', add
label define ancestr2d_lbl 0630 `"Molise"', add
label define ancestr2d_lbl 0640 `"Neapolitan"', add
label define ancestr2d_lbl 0650 `"Piedmontese"', add
label define ancestr2d_lbl 0660 `"Puglia"', add
label define ancestr2d_lbl 0670 `"Sardinian"', add
label define ancestr2d_lbl 0680 `"Sicilian"', add
label define ancestr2d_lbl 0690 `"Toscana"', add
label define ancestr2d_lbl 0700 `"Trentino"', add
label define ancestr2d_lbl 0710 `"Umbrian"', add
label define ancestr2d_lbl 0720 `"Valle dAosta"', add
label define ancestr2d_lbl 0730 `"Venetian"', add
label define ancestr2d_lbl 0750 `"Lapp"', add
label define ancestr2d_lbl 0760 `"Liechtensteiner"', add
label define ancestr2d_lbl 0770 `"Luxemburger"', add
label define ancestr2d_lbl 0780 `"Maltese"', add
label define ancestr2d_lbl 0790 `"Manx"', add
label define ancestr2d_lbl 0800 `"Monegasque"', add
label define ancestr2d_lbl 0810 `"Northern Irelander"', add
label define ancestr2d_lbl 0820 `"Norwegian"', add
label define ancestr2d_lbl 0840 `"Portuguese"', add
label define ancestr2d_lbl 0850 `"Azorean"', add
label define ancestr2d_lbl 0860 `"Madeiran"', add
label define ancestr2d_lbl 0870 `"Scotch Irish"', add
label define ancestr2d_lbl 0880 `"Scottish"', add
label define ancestr2d_lbl 0890 `"Swedish"', add
label define ancestr2d_lbl 0900 `"Aland Islander"', add
label define ancestr2d_lbl 0910 `"Swiss"', add
label define ancestr2d_lbl 0920 `"Suisse (1980)"', add
label define ancestr2d_lbl 0921 `"Suisse (1990-2000)"', add
label define ancestr2d_lbl 0922 `"Switzer (1990-2000)"', add
label define ancestr2d_lbl 0950 `"Romansch (1980)"', add
label define ancestr2d_lbl 0951 `"Romanscho (1990-2000)"', add
label define ancestr2d_lbl 0952 `"Ladin (1990-2000)"', add
label define ancestr2d_lbl 0960 `"Suisse Romane (1990-2000)"', add
label define ancestr2d_lbl 0961 `"Suisse Romane (1980)"', add
label define ancestr2d_lbl 0962 `"Ticino"', add
label define ancestr2d_lbl 0970 `"Welsh"', add
label define ancestr2d_lbl 0980 `"Scandinavian, Nordic"', add
label define ancestr2d_lbl 1000 `"Albanian"', add
label define ancestr2d_lbl 1010 `"Azerbaijani"', add
label define ancestr2d_lbl 1020 `"Belorussian"', add
label define ancestr2d_lbl 1030 `"Bulgarian"', add
label define ancestr2d_lbl 1050 `"Carpathian"', add
label define ancestr2d_lbl 1051 `"Carpatho Rusyn"', add
label define ancestr2d_lbl 1052 `"Rusyn"', add
label define ancestr2d_lbl 1080 `"Cossack (1990-2000)"', add
label define ancestr2d_lbl 1081 `"Cossack (1980)"', add
label define ancestr2d_lbl 1082 `"Turkestani (1990-2000, 2012 ACS)"', add
label define ancestr2d_lbl 1083 `"Kirghiz (1980)"', add
label define ancestr2d_lbl 1084 `"Turcoman (1980)"', add
label define ancestr2d_lbl 1090 `"Croatian"', add
label define ancestr2d_lbl 1110 `"Czechoslovakian"', add
label define ancestr2d_lbl 1111 `"Czech"', add
label define ancestr2d_lbl 1120 `"Bohemian (1980)"', add
label define ancestr2d_lbl 1121 `"Bohemian (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 1122 `"Moravian (1990-2000)"', add
label define ancestr2d_lbl 1150 `"Estonian"', add
label define ancestr2d_lbl 1160 `"Livonian"', add
label define ancestr2d_lbl 1170 `"Finno Ugrian (1990-2000)"', add
label define ancestr2d_lbl 1171 `"Udmert"', add
label define ancestr2d_lbl 1180 `"Mordovian"', add
label define ancestr2d_lbl 1190 `"Voytak"', add
label define ancestr2d_lbl 1200 `"Georgian"', add
label define ancestr2d_lbl 1220 `"Germans from Russia"', add
label define ancestr2d_lbl 1221 `"Volga"', add
label define ancestr2d_lbl 1222 `"German from Russia (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 1230 `"Gruziia (1990-2000)"', add
label define ancestr2d_lbl 1240 `"Rom"', add
label define ancestr2d_lbl 1250 `"Hungarian"', add
label define ancestr2d_lbl 1260 `"Magyar"', add
label define ancestr2d_lbl 1280 `"Latvian"', add
label define ancestr2d_lbl 1290 `"Lithuanian"', add
label define ancestr2d_lbl 1300 `"Macedonian"', add
label define ancestr2d_lbl 1320 `"North Caucasian (1990-2000)"', add
label define ancestr2d_lbl 1330 `"North Caucasian Turkic (1990-2000)"', add
label define ancestr2d_lbl 1400 `"Ossetian"', add
label define ancestr2d_lbl 1420 `"Polish"', add
label define ancestr2d_lbl 1430 `"Kashubian"', add
label define ancestr2d_lbl 1440 `"Romanian (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 1441 `"Romanian (1980)"', add
label define ancestr2d_lbl 1442 `"Transylvanian"', add
label define ancestr2d_lbl 1450 `"Bessarabian (1980)"', add
label define ancestr2d_lbl 1451 `"Bessarabian (1990-2000)"', add
label define ancestr2d_lbl 1452 `"Bucovina"', add
label define ancestr2d_lbl 1460 `"Moldavian"', add
label define ancestr2d_lbl 1470 `"Wallachian"', add
label define ancestr2d_lbl 1480 `"Russian"', add
label define ancestr2d_lbl 1500 `"Muscovite"', add
label define ancestr2d_lbl 1520 `"Serbian (1980)"', add
label define ancestr2d_lbl 1521 `"Serbian (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 1522 `"Bosnian (1990) Herzegovinian (2000, ACS, PRCS)"', add
label define ancestr2d_lbl 1523 `"Montenegrin (1990-2000, 2012 ACS)"', add
label define ancestr2d_lbl 1530 `"Slovak"', add
label define ancestr2d_lbl 1540 `"Slovene"', add
label define ancestr2d_lbl 1550 `"Sorb/Wend"', add
label define ancestr2d_lbl 1560 `"Soviet Turkic (1990-2000)"', add
label define ancestr2d_lbl 1570 `"Bashkir"', add
label define ancestr2d_lbl 1580 `"Chevash"', add
label define ancestr2d_lbl 1590 `"Gagauz (1990-2000)"', add
label define ancestr2d_lbl 1600 `"Mesknetian (1990-2000)"', add
label define ancestr2d_lbl 1630 `"Yakut"', add
label define ancestr2d_lbl 1640 `"Soviet Union, nec"', add
label define ancestr2d_lbl 1650 `"Tatar (1990-2000)"', add
label define ancestr2d_lbl 1651 `"Tatar (1980)"', add
label define ancestr2d_lbl 1652 `"Crimean (1980)"', add
label define ancestr2d_lbl 1653 `"Tuvinian (1990-2000)"', add
label define ancestr2d_lbl 1654 `"Soviet Central Asian (1990-2000)"', add
label define ancestr2d_lbl 1655 `"Tadzhik (1980, 2000)"', add
label define ancestr2d_lbl 1690 `"Uzbek"', add
label define ancestr2d_lbl 1710 `"Ukrainian (1980)"', add
label define ancestr2d_lbl 1711 `"Ukrainian (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 1712 `"Ruthenian (1980)"', add
label define ancestr2d_lbl 1713 `"Ruthenian (1990-2000)"', add
label define ancestr2d_lbl 1714 `"Lemko"', add
label define ancestr2d_lbl 1715 `"Bioko"', add
label define ancestr2d_lbl 1716 `"Hesel"', add
label define ancestr2d_lbl 1717 `"Windish"', add
label define ancestr2d_lbl 1760 `"Yugoslavian"', add
label define ancestr2d_lbl 1780 `"Slav"', add
label define ancestr2d_lbl 1790 `"Slavonian"', add
label define ancestr2d_lbl 1810 `"Central European, nec"', add
label define ancestr2d_lbl 1830 `"Northern European, nec"', add
label define ancestr2d_lbl 1850 `"Southern European, nec"', add
label define ancestr2d_lbl 1870 `"Western European, nec"', add
label define ancestr2d_lbl 1900 `"Eastern European, nec"', add
label define ancestr2d_lbl 1950 `"European, nec"', add
label define ancestr2d_lbl 2000 `"Spaniard (1980)"', add
label define ancestr2d_lbl 2001 `"Spaniard (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 2002 `"Castillian (1990-2000)"', add
label define ancestr2d_lbl 2003 `"Valencian (1990-2000)"', add
label define ancestr2d_lbl 2010 `"Andalusian (1990-2000)"', add
label define ancestr2d_lbl 2020 `"Asturian (1990-2000)"', add
label define ancestr2d_lbl 2040 `"Catalonian"', add
label define ancestr2d_lbl 2050 `"Balearic Islander (1980)"', add
label define ancestr2d_lbl 2051 `"Balearic Islander (1990-2000)"', add
label define ancestr2d_lbl 2052 `"Canary Islander (1990-2000)"', add
label define ancestr2d_lbl 2060 `"Galician (1980)"', add
label define ancestr2d_lbl 2061 `"Gallego (1990-2000)"', add
label define ancestr2d_lbl 2062 `"Galician (1990-2000)"', add
label define ancestr2d_lbl 2100 `"Mexican"', add
label define ancestr2d_lbl 2101 `"Mexican (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 2102 `"Mexicano/Mexicana (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 2103 `"Mexican Indian"', add
label define ancestr2d_lbl 2110 `"Mexican American"', add
label define ancestr2d_lbl 2111 `"Mexican American Indian"', add
label define ancestr2d_lbl 2130 `"Chicano/Chicana"', add
label define ancestr2d_lbl 2180 `"Nuevo Mexicano"', add
label define ancestr2d_lbl 2181 `"Nuevo Mexicano (1990-2000)"', add
label define ancestr2d_lbl 2182 `"La Raza (1990-2000)"', add
label define ancestr2d_lbl 2183 `"Mexican state (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 2184 `"Tejano/Tejana (1990-2000)"', add
label define ancestr2d_lbl 2190 `"Californio"', add
label define ancestr2d_lbl 2210 `"Costa Rican"', add
label define ancestr2d_lbl 2220 `"Guatemalan"', add
label define ancestr2d_lbl 2230 `"Honduran"', add
label define ancestr2d_lbl 2240 `"Nicaraguan"', add
label define ancestr2d_lbl 2250 `"Panamanian (1980)"', add
label define ancestr2d_lbl 2251 `"Panamanian (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 2252 `"Canal Zone (1990-2000)"', add
label define ancestr2d_lbl 2260 `"Salvadoran"', add
label define ancestr2d_lbl 2270 `"Latin American (1980)"', add
label define ancestr2d_lbl 2271 `"Central American (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 2272 `"Latin American (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 2273 `"Latino/Latina (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 2274 `"Latin (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 2310 `"Argentinean"', add
label define ancestr2d_lbl 2320 `"Bolivian"', add
label define ancestr2d_lbl 2330 `"Chilean"', add
label define ancestr2d_lbl 2340 `"Colombian"', add
label define ancestr2d_lbl 2350 `"Ecuadorian"', add
label define ancestr2d_lbl 2360 `"Paraguayan"', add
label define ancestr2d_lbl 2370 `"Peruvian"', add
label define ancestr2d_lbl 2380 `"Uruguayan"', add
label define ancestr2d_lbl 2390 `"Venezuelan"', add
label define ancestr2d_lbl 2480 `"South American (1980)"', add
label define ancestr2d_lbl 2481 `"South American (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 2482 `"Criollo/Criolla (1990-2000)"', add
label define ancestr2d_lbl 2610 `"Puerto Rican"', add
label define ancestr2d_lbl 2710 `"Cuban"', add
label define ancestr2d_lbl 2750 `"Dominican"', add
label define ancestr2d_lbl 2900 `"Hispanic"', add
label define ancestr2d_lbl 2910 `"Spanish"', add
label define ancestr2d_lbl 2950 `"Spanish American"', add
label define ancestr2d_lbl 2960 `"Other Spanish/Hispanic"', add
label define ancestr2d_lbl 3000 `"Bahamian"', add
label define ancestr2d_lbl 3010 `"Barbadian"', add
label define ancestr2d_lbl 3020 `"Belizean"', add
label define ancestr2d_lbl 3030 `"Bermudan"', add
label define ancestr2d_lbl 3040 `"Cayman Islander"', add
label define ancestr2d_lbl 3080 `"Jamaican"', add
label define ancestr2d_lbl 3100 `"Dutch West Indies"', add
label define ancestr2d_lbl 3110 `"Aruba Islander"', add
label define ancestr2d_lbl 3120 `"St Maarten Islander"', add
label define ancestr2d_lbl 3140 `"Trinidadian/Tobagonian"', add
label define ancestr2d_lbl 3150 `"Trinidadian"', add
label define ancestr2d_lbl 3160 `"Tobagonian"', add
label define ancestr2d_lbl 3170 `"U.S. Virgin Islander (1980)"', add
label define ancestr2d_lbl 3171 `"U.S. Virgin Islander (1990-2000)"', add
label define ancestr2d_lbl 3172 `"St. Croix Islander (1990-2000)"', add
label define ancestr2d_lbl 3173 `"St. John Islander (1990-2000)"', add
label define ancestr2d_lbl 3174 `"St. Thomas Islander (1990-2000)"', add
label define ancestr2d_lbl 3210 `"British Virgin Islander (1980)"', add
label define ancestr2d_lbl 3211 `"British Virgin Islander (1990-2000)"', add
label define ancestr2d_lbl 3212 `"Antigua (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 3220 `"British West Indian"', add
label define ancestr2d_lbl 3230 `"Turks and Caicos Islander"', add
label define ancestr2d_lbl 3240 `"Anguilla Islander (1980)"', add
label define ancestr2d_lbl 3241 `"Anguilla Islander (1990-2000)"', add
label define ancestr2d_lbl 3242 `"Montserrat Islander (1990-2000)"', add
label define ancestr2d_lbl 3243 `"Kitts/Nevis Islander (1990-2000)"', add
label define ancestr2d_lbl 3244 `"St. Christopher (1980)"', add
label define ancestr2d_lbl 3245 `"St Vincent Islander"', add
label define ancestr2d_lbl 3280 `"Dominica Islander"', add
label define ancestr2d_lbl 3290 `"Grenadian"', add
label define ancestr2d_lbl 3310 `"St Lucia Islander"', add
label define ancestr2d_lbl 3320 `"French West Indies"', add
label define ancestr2d_lbl 3330 `"Guadeloupe Islander"', add
label define ancestr2d_lbl 3340 `"Cayenne"', add
label define ancestr2d_lbl 3350 `"West Indian (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 3351 `"West Indian (1980)"', add
label define ancestr2d_lbl 3352 `"Caribbean (1980)"', add
label define ancestr2d_lbl 3353 `"Arawak (1980)"', add
label define ancestr2d_lbl 3360 `"Haitian"', add
label define ancestr2d_lbl 3370 `"Other West Indian"', add
label define ancestr2d_lbl 3600 `"Brazilian"', add
label define ancestr2d_lbl 3650 `"San Andres"', add
label define ancestr2d_lbl 3700 `"Guyanese/British Guiana"', add
label define ancestr2d_lbl 3750 `"Providencia"', add
label define ancestr2d_lbl 3800 `"Surinam/Dutch Guiana"', add
label define ancestr2d_lbl 4000 `"Algerian"', add
label define ancestr2d_lbl 4020 `"Egyptian"', add
label define ancestr2d_lbl 4040 `"Libyan"', add
label define ancestr2d_lbl 4060 `"Moroccan (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 4061 `"Moroccan (1980)"', add
label define ancestr2d_lbl 4062 `"Moor (1980)"', add
label define ancestr2d_lbl 4070 `"Ifni"', add
label define ancestr2d_lbl 4080 `"Tunisian"', add
label define ancestr2d_lbl 4110 `"North African"', add
label define ancestr2d_lbl 4120 `"Alhucemas"', add
label define ancestr2d_lbl 4130 `"Berber"', add
label define ancestr2d_lbl 4140 `"Rio de Oro"', add
label define ancestr2d_lbl 4150 `"Bahraini"', add
label define ancestr2d_lbl 4160 `"Iranian"', add
label define ancestr2d_lbl 4170 `"Iraqi"', add
label define ancestr2d_lbl 4190 `"Israeli"', add
label define ancestr2d_lbl 4210 `"Jordanian"', add
label define ancestr2d_lbl 4220 `"Transjordan"', add
label define ancestr2d_lbl 4230 `"Kuwaiti"', add
label define ancestr2d_lbl 4250 `"Lebanese"', add
label define ancestr2d_lbl 4270 `"Saudi Arabian"', add
label define ancestr2d_lbl 4290 `"Syrian (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 4291 `"Syrian (1980)"', add
label define ancestr2d_lbl 4292 `"Latakian (1980)"', add
label define ancestr2d_lbl 4293 `"Jebel Druse (1980)"', add
label define ancestr2d_lbl 4310 `"Armenian"', add
label define ancestr2d_lbl 4340 `"Turkish"', add
label define ancestr2d_lbl 4350 `"Yemeni"', add
label define ancestr2d_lbl 4360 `"Omani"', add
label define ancestr2d_lbl 4370 `"Muscat"', add
label define ancestr2d_lbl 4380 `"Trucial Oman"', add
label define ancestr2d_lbl 4390 `"Qatar"', add
label define ancestr2d_lbl 4410 `"Bedouin"', add
label define ancestr2d_lbl 4420 `"Kurdish"', add
label define ancestr2d_lbl 4440 `"Kuria Muria Islander"', add
label define ancestr2d_lbl 4650 `"Palestinian"', add
label define ancestr2d_lbl 4660 `"Gazan"', add
label define ancestr2d_lbl 4670 `"West Bank"', add
label define ancestr2d_lbl 4700 `"South Yemeni"', add
label define ancestr2d_lbl 4710 `"Aden"', add
label define ancestr2d_lbl 4800 `"United Arab Emirates"', add
label define ancestr2d_lbl 4820 `"Assyrian/Chaldean/Syriac (1990-2000)"', add
label define ancestr2d_lbl 4821 `"Assyrian"', add
label define ancestr2d_lbl 4822 `"Syriac (1980, 2000)"', add
label define ancestr2d_lbl 4823 `"Chaldean (2000, ACS, PRCS)"', add
label define ancestr2d_lbl 4900 `"Middle Eastern"', add
label define ancestr2d_lbl 4950 `"Arab"', add
label define ancestr2d_lbl 4951 `"Arabic (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 4960 `"Other Arab"', add
label define ancestr2d_lbl 5000 `"Angolan"', add
label define ancestr2d_lbl 5020 `"Benin"', add
label define ancestr2d_lbl 5040 `"Botswana"', add
label define ancestr2d_lbl 5060 `"Burundian"', add
label define ancestr2d_lbl 5080 `"Cameroonian"', add
label define ancestr2d_lbl 5100 `"Cape Verdean"', add
label define ancestr2d_lbl 5120 `"Central African Republic"', add
label define ancestr2d_lbl 5130 `"Chadian"', add
label define ancestr2d_lbl 5150 `"Congolese"', add
label define ancestr2d_lbl 5160 `"Congo-Brazzaville"', add
label define ancestr2d_lbl 5190 `"Djibouti"', add
label define ancestr2d_lbl 5200 `"Equatorial Guinea"', add
label define ancestr2d_lbl 5210 `"Corsico Islander"', add
label define ancestr2d_lbl 5220 `"Ethiopian"', add
label define ancestr2d_lbl 5230 `"Eritrean"', add
label define ancestr2d_lbl 5250 `"Gabonese"', add
label define ancestr2d_lbl 5270 `"Gambian"', add
label define ancestr2d_lbl 5290 `"Ghanian"', add
label define ancestr2d_lbl 5300 `"Guinean"', add
label define ancestr2d_lbl 5310 `"Guinea Bissau"', add
label define ancestr2d_lbl 5320 `"Ivory Coast"', add
label define ancestr2d_lbl 5340 `"Kenyan"', add
label define ancestr2d_lbl 5380 `"Lesotho"', add
label define ancestr2d_lbl 5410 `"Liberian"', add
label define ancestr2d_lbl 5430 `"Madagascan"', add
label define ancestr2d_lbl 5450 `"Malawian"', add
label define ancestr2d_lbl 5460 `"Malian"', add
label define ancestr2d_lbl 5470 `"Mauritanian"', add
label define ancestr2d_lbl 5490 `"Mozambican"', add
label define ancestr2d_lbl 5500 `"Namibian"', add
label define ancestr2d_lbl 5510 `"Niger"', add
label define ancestr2d_lbl 5530 `"Nigerian"', add
label define ancestr2d_lbl 5540 `"Fulani"', add
label define ancestr2d_lbl 5550 `"Hausa"', add
label define ancestr2d_lbl 5560 `"Ibo"', add
label define ancestr2d_lbl 5570 `"Tiv (1980)"', add
label define ancestr2d_lbl 5571 `"Tiv (1990-2000)"', add
label define ancestr2d_lbl 5572 `"Yoruba (1990-2000)"', add
label define ancestr2d_lbl 5610 `"Rwandan"', add
label define ancestr2d_lbl 5640 `"Senegalese"', add
label define ancestr2d_lbl 5660 `"Sierra Leonean"', add
label define ancestr2d_lbl 5680 `"Somalian"', add
label define ancestr2d_lbl 5690 `"Swaziland"', add
label define ancestr2d_lbl 5700 `"South African"', add
label define ancestr2d_lbl 5710 `"Union of South Africa"', add
label define ancestr2d_lbl 5720 `"Afrikaner"', add
label define ancestr2d_lbl 5730 `"Natalian"', add
label define ancestr2d_lbl 5740 `"Zulu"', add
label define ancestr2d_lbl 5760 `"Sudanese"', add
label define ancestr2d_lbl 5770 `"Dinka"', add
label define ancestr2d_lbl 5780 `"Nuer"', add
label define ancestr2d_lbl 5790 `"Fur"', add
label define ancestr2d_lbl 5800 `"Baggara"', add
label define ancestr2d_lbl 5820 `"Tanzanian"', add
label define ancestr2d_lbl 5830 `"Tanganyikan"', add
label define ancestr2d_lbl 5840 `"Zanzibar"', add
label define ancestr2d_lbl 5860 `"Togo"', add
label define ancestr2d_lbl 5880 `"Ugandan"', add
label define ancestr2d_lbl 5890 `"Upper Voltan"', add
label define ancestr2d_lbl 5900 `"Voltan"', add
label define ancestr2d_lbl 5910 `"Zairian"', add
label define ancestr2d_lbl 5920 `"Zambian"', add
label define ancestr2d_lbl 5930 `"Zimbabwean"', add
label define ancestr2d_lbl 5940 `"African Islands (1980)"', add
label define ancestr2d_lbl 5941 `"African Islands (1990-2000)"', add
label define ancestr2d_lbl 5942 `"Mauritius (1990-2000)"', add
label define ancestr2d_lbl 5950 `"Other Subsaharan Africa"', add
label define ancestr2d_lbl 5960 `"Central African"', add
label define ancestr2d_lbl 5970 `"East African"', add
label define ancestr2d_lbl 5980 `"West African"', add
label define ancestr2d_lbl 5990 `"African"', add
label define ancestr2d_lbl 6000 `"Afghan"', add
label define ancestr2d_lbl 6010 `"Baluchi"', add
label define ancestr2d_lbl 6020 `"Pathan"', add
label define ancestr2d_lbl 6030 `"Bengali (1980)"', add
label define ancestr2d_lbl 6031 `"Bangladeshi (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 6032 `"Bengali (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 6070 `"Bhutanese"', add
label define ancestr2d_lbl 6090 `"Nepali"', add
label define ancestr2d_lbl 6150 `"Asian Indian (1980)"', add
label define ancestr2d_lbl 6151 `"India (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 6152 `"East Indian (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 6153 `"Madhya Pradesh (1990-2000)"', add
label define ancestr2d_lbl 6154 `"Orissa (1990-2000)"', add
label define ancestr2d_lbl 6155 `"Rajasthani (1990-2000)"', add
label define ancestr2d_lbl 6156 `"Sikkim (1990-2000)"', add
label define ancestr2d_lbl 6157 `"Uttar Pradesh (1990-2000)"', add
label define ancestr2d_lbl 6220 `"Andaman Islander"', add
label define ancestr2d_lbl 6240 `"Andhra Pradesh"', add
label define ancestr2d_lbl 6260 `"Assamese"', add
label define ancestr2d_lbl 6280 `"Goanese"', add
label define ancestr2d_lbl 6300 `"Gujarati"', add
label define ancestr2d_lbl 6320 `"Karnatakan"', add
label define ancestr2d_lbl 6340 `"Keralan"', add
label define ancestr2d_lbl 6380 `"Maharashtran"', add
label define ancestr2d_lbl 6400 `"Madrasi"', add
label define ancestr2d_lbl 6420 `"Mysore"', add
label define ancestr2d_lbl 6440 `"Naga"', add
label define ancestr2d_lbl 6480 `"Pondicherry"', add
label define ancestr2d_lbl 6500 `"Punjabi"', add
label define ancestr2d_lbl 6560 `"Tamil"', add
label define ancestr2d_lbl 6750 `"East Indies (1990-2000)"', add
label define ancestr2d_lbl 6800 `"Pakistani (1980)"', add
label define ancestr2d_lbl 6801 `"Pakistani (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 6802 `"Kashmiri (1990-2000)"', add
label define ancestr2d_lbl 6900 `"Sri Lankan"', add
label define ancestr2d_lbl 6910 `"Singhalese"', add
label define ancestr2d_lbl 6920 `"Veddah"', add
label define ancestr2d_lbl 6950 `"Maldivian"', add
label define ancestr2d_lbl 7000 `"Burmese (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 7001 `"Burmese (1980)"', add
label define ancestr2d_lbl 7002 `"Burman (1980)"', add
label define ancestr2d_lbl 7020 `"Shan"', add
label define ancestr2d_lbl 7030 `"Cambodian"', add
label define ancestr2d_lbl 7040 `"Khmer"', add
label define ancestr2d_lbl 7060 `"Chinese"', add
label define ancestr2d_lbl 7070 `"Cantonese (1980)"', add
label define ancestr2d_lbl 7071 `"Cantonese (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 7072 `"Formosan (1990-2000)"', add
label define ancestr2d_lbl 7080 `"Manchurian"', add
label define ancestr2d_lbl 7090 `"Mandarin (1990-2000)"', add
label define ancestr2d_lbl 7120 `"Mongolian (1980)"', add
label define ancestr2d_lbl 7121 `"Mongolian (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 7122 `"Kalmyk (1990-2000)"', add
label define ancestr2d_lbl 7140 `"Tibetan"', add
label define ancestr2d_lbl 7160 `"Hong Kong (1990-2000)"', add
label define ancestr2d_lbl 7161 `"Hong Kong (1980)"', add
label define ancestr2d_lbl 7162 `"Eastern Archipelago (1980)"', add
label define ancestr2d_lbl 7180 `"Macao"', add
label define ancestr2d_lbl 7200 `"Filipino"', add
label define ancestr2d_lbl 7300 `"Indonesian (1980)"', add
label define ancestr2d_lbl 7301 `"Indonesian (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 7302 `"Borneo (1990-2000)"', add
label define ancestr2d_lbl 7303 `"Java (1990-2000)"', add
label define ancestr2d_lbl 7304 `"Sumatran (1990-2000)"', add
label define ancestr2d_lbl 7400 `"Japanese (1980)"', add
label define ancestr2d_lbl 7401 `"Japanese (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 7402 `"Issei (1990-2000)"', add
label define ancestr2d_lbl 7403 `"Nisei (1990-2000)"', add
label define ancestr2d_lbl 7404 `"Sansei (1990-2000)"', add
label define ancestr2d_lbl 7405 `"Yonsei (1990-2000)"', add
label define ancestr2d_lbl 7406 `"Gosei (1990-2000)"', add
label define ancestr2d_lbl 7460 `"Ryukyu Islander"', add
label define ancestr2d_lbl 7480 `"Okinawan"', add
label define ancestr2d_lbl 7500 `"Korean"', add
label define ancestr2d_lbl 7650 `"Laotian"', add
label define ancestr2d_lbl 7660 `"Meo"', add
label define ancestr2d_lbl 7680 `"Hmong"', add
label define ancestr2d_lbl 7700 `"Malaysian (1980)"', add
label define ancestr2d_lbl 7701 `"Malaysian (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 7702 `"North Borneo (1990-2000)"', add
label define ancestr2d_lbl 7740 `"Singaporean"', add
label define ancestr2d_lbl 7760 `"Thai"', add
label define ancestr2d_lbl 7770 `"Black Thai"', add
label define ancestr2d_lbl 7780 `"Western Lao"', add
label define ancestr2d_lbl 7820 `"Taiwanese"', add
label define ancestr2d_lbl 7850 `"Vietnamese"', add
label define ancestr2d_lbl 7860 `"Katu"', add
label define ancestr2d_lbl 7870 `"Ma"', add
label define ancestr2d_lbl 7880 `"Mnong"', add
label define ancestr2d_lbl 7900 `"Montagnard"', add
label define ancestr2d_lbl 7920 `"Indochinese"', add
label define ancestr2d_lbl 7930 `"Eurasian"', add
label define ancestr2d_lbl 7931 `"Amerasian"', add
label define ancestr2d_lbl 7950 `"Asian"', add
label define ancestr2d_lbl 7960 `"Other Asian"', add
label define ancestr2d_lbl 8000 `"Australian"', add
label define ancestr2d_lbl 8010 `"Tasmanian"', add
label define ancestr2d_lbl 8020 `"Australian Aborigine (1990-2000)"', add
label define ancestr2d_lbl 8030 `"New Zealander"', add
label define ancestr2d_lbl 8080 `"Polynesian (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 8081 `"Polynesian (1980)"', add
label define ancestr2d_lbl 8082 `"Norfolk Islander (1980)"', add
label define ancestr2d_lbl 8090 `"Kapinagamarangan (1990-2000)"', add
label define ancestr2d_lbl 8091 `"Kapinagamarangan (1980)"', add
label define ancestr2d_lbl 8092 `"Nukuoroan (1980)"', add
label define ancestr2d_lbl 8100 `"Maori"', add
label define ancestr2d_lbl 8110 `"Hawaiian"', add
label define ancestr2d_lbl 8130 `"Part Hawaiian"', add
label define ancestr2d_lbl 8140 `"Samoan (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 8141 `"Samoan (1980)"', add
label define ancestr2d_lbl 8142 `"American Samoan (1980)"', add
label define ancestr2d_lbl 8143 `"French Samoan"', add
label define ancestr2d_lbl 8144 `"Part Samoan (1990-2000)"', add
label define ancestr2d_lbl 8150 `"Tongan"', add
label define ancestr2d_lbl 8160 `"Tokelauan"', add
label define ancestr2d_lbl 8170 `"Cook Islander"', add
label define ancestr2d_lbl 8180 `"Tahitian"', add
label define ancestr2d_lbl 8190 `"Niuean"', add
label define ancestr2d_lbl 8200 `"Micronesian (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 8201 `"Micronesian (1980)"', add
label define ancestr2d_lbl 8202 `"U.S. Trust Terr of the Pacific"', add
label define ancestr2d_lbl 8210 `"Guamanian"', add
label define ancestr2d_lbl 8220 `"Chamorro Islander"', add
label define ancestr2d_lbl 8230 `"Saipanese (1990-2000)"', add
label define ancestr2d_lbl 8231 `"Saipanese (1980)"', add
label define ancestr2d_lbl 8232 `"Northern Marianas (1980)"', add
label define ancestr2d_lbl 8240 `"Palauan"', add
label define ancestr2d_lbl 8250 `"Marshall Islander"', add
label define ancestr2d_lbl 8260 `"Kosraean"', add
label define ancestr2d_lbl 8270 `"Ponapean (1990-2000)"', add
label define ancestr2d_lbl 8271 `"Ponapean (1980)"', add
label define ancestr2d_lbl 8272 `"Mokilese (1980)"', add
label define ancestr2d_lbl 8273 `"Ngatikese (1980)"', add
label define ancestr2d_lbl 8274 `"Pingelapese (1980)"', add
label define ancestr2d_lbl 8280 `"Chuukese"', add
label define ancestr2d_lbl 8281 `"Hall Islander (1980)"', add
label define ancestr2d_lbl 8282 `"Mortlockese (1980)"', add
label define ancestr2d_lbl 8283 `"Namanouito (1980)"', add
label define ancestr2d_lbl 8284 `"Pulawatese (1980)"', add
label define ancestr2d_lbl 8285 `"Truk Islander"', add
label define ancestr2d_lbl 8290 `"Yap Islander"', add
label define ancestr2d_lbl 8300 `"Caroline Islander (1990-2000)"', add
label define ancestr2d_lbl 8301 `"Caroline Islander (1980)"', add
label define ancestr2d_lbl 8302 `"Lamotrekese (1980)"', add
label define ancestr2d_lbl 8303 `"Ulithian (1980)"', add
label define ancestr2d_lbl 8304 `"Woleaian (1980)"', add
label define ancestr2d_lbl 8310 `"Kiribatese"', add
label define ancestr2d_lbl 8320 `"Nauruan"', add
label define ancestr2d_lbl 8330 `"Tarawa Islander (1990-2000)"', add
label define ancestr2d_lbl 8340 `"Tinian Islander (1990-2000)"', add
label define ancestr2d_lbl 8400 `"Melanesian Islander"', add
label define ancestr2d_lbl 8410 `"Fijian"', add
label define ancestr2d_lbl 8430 `"New Guinean"', add
label define ancestr2d_lbl 8440 `"Papuan"', add
label define ancestr2d_lbl 8450 `"Solomon Islander"', add
label define ancestr2d_lbl 8460 `"New Caledonian Islander"', add
label define ancestr2d_lbl 8470 `"Vanuatuan"', add
label define ancestr2d_lbl 8500 `"Pacific Islander (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 8501 `"Campbell Islander (1980)"', add
label define ancestr2d_lbl 8502 `"Christmas Islander (1980)"', add
label define ancestr2d_lbl 8503 `"Kermadec Islander (1980)"', add
label define ancestr2d_lbl 8504 `"Midway Islander (1980)"', add
label define ancestr2d_lbl 8505 `"Phoenix Islander (1980)"', add
label define ancestr2d_lbl 8506 `"Wake Islander (1980)"', add
label define ancestr2d_lbl 8600 `"Oceania"', add
label define ancestr2d_lbl 8620 `"Chamolinian (1990-2000)"', add
label define ancestr2d_lbl 8630 `"Reserved Codes"', add
label define ancestr2d_lbl 8700 `"Other Pacific"', add
label define ancestr2d_lbl 9000 `"Afro-American"', add
label define ancestr2d_lbl 9001 `"Afro-American (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 9002 `"Black (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 9003 `"Negro (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 9004 `"Nonwhite (1990-2000)"', add
label define ancestr2d_lbl 9005 `"Colored (1990-2000)"', add
label define ancestr2d_lbl 9006 `"Creole (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 9007 `"Mulatto (1990-2000)"', add
label define ancestr2d_lbl 9008 `"Afro"', add
label define ancestr2d_lbl 9020 `"African-American (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 9130 `"Central American Indian (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 9140 `"South American Indian (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 9200 `"American Indian (all tribes)"', add
label define ancestr2d_lbl 9201 `"American Indian-English-French"', add
label define ancestr2d_lbl 9202 `"American Indian-English-German"', add
label define ancestr2d_lbl 9203 `"American Indian-English-Irish"', add
label define ancestr2d_lbl 9204 `"American Indian-German-Irish"', add
label define ancestr2d_lbl 9205 `"Cherokee"', add
label define ancestr2d_lbl 9206 `"Native American"', add
label define ancestr2d_lbl 9207 `"Indian"', add
label define ancestr2d_lbl 9210 `"Aleut"', add
label define ancestr2d_lbl 9220 `"Eskimo"', add
label define ancestr2d_lbl 9230 `"Inuit"', add
label define ancestr2d_lbl 9240 `"White/Caucasian"', add
label define ancestr2d_lbl 9241 `"White/Caucasian (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 9242 `"Anglo (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 9243 `"Appalachian (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 9244 `"Aryan (1990-2000)"', add
label define ancestr2d_lbl 9300 `"Greenlander"', add
label define ancestr2d_lbl 9310 `"Canadian"', add
label define ancestr2d_lbl 9330 `"Newfoundland"', add
label define ancestr2d_lbl 9340 `"Nova Scotian"', add
label define ancestr2d_lbl 9350 `"French Canadian"', add
label define ancestr2d_lbl 9360 `"Acadian"', add
label define ancestr2d_lbl 9361 `"Acadian (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 9362 `"Cajun (1990-2000, ACS, PRCS)"', add
label define ancestr2d_lbl 9390 `"American"', add
label define ancestr2d_lbl 9391 `"American/Unites States"', add
label define ancestr2d_lbl 9400 `"United States"', add
label define ancestr2d_lbl 9410 `"Alabama"', add
label define ancestr2d_lbl 9420 `"Alaska"', add
label define ancestr2d_lbl 9430 `"Arizona"', add
label define ancestr2d_lbl 9440 `"Arkansas"', add
label define ancestr2d_lbl 9450 `"California"', add
label define ancestr2d_lbl 9460 `"Colorado"', add
label define ancestr2d_lbl 9470 `"Connecticut"', add
label define ancestr2d_lbl 9480 `"District of Columbia"', add
label define ancestr2d_lbl 9490 `"Delaware"', add
label define ancestr2d_lbl 9500 `"Florida"', add
label define ancestr2d_lbl 9510 `"Georgia"', add
label define ancestr2d_lbl 9520 `"Idaho"', add
label define ancestr2d_lbl 9530 `"Illinois"', add
label define ancestr2d_lbl 9540 `"Indiana"', add
label define ancestr2d_lbl 9550 `"Iowa"', add
label define ancestr2d_lbl 9560 `"Kansas"', add
label define ancestr2d_lbl 9570 `"Kentucky"', add
label define ancestr2d_lbl 9580 `"Louisiana"', add
label define ancestr2d_lbl 9590 `"Maine"', add
label define ancestr2d_lbl 9600 `"Maryland"', add
label define ancestr2d_lbl 9610 `"Massachusetts"', add
label define ancestr2d_lbl 9620 `"Michigan"', add
label define ancestr2d_lbl 9630 `"Minnesota"', add
label define ancestr2d_lbl 9640 `"Mississippi"', add
label define ancestr2d_lbl 9650 `"Missouri"', add
label define ancestr2d_lbl 9660 `"Montana"', add
label define ancestr2d_lbl 9670 `"Nebraska"', add
label define ancestr2d_lbl 9680 `"Nevada"', add
label define ancestr2d_lbl 9690 `"New Hampshire"', add
label define ancestr2d_lbl 9700 `"New Jersey"', add
label define ancestr2d_lbl 9710 `"New Mexico"', add
label define ancestr2d_lbl 9720 `"New York"', add
label define ancestr2d_lbl 9730 `"North Carolina"', add
label define ancestr2d_lbl 9740 `"North Dakota"', add
label define ancestr2d_lbl 9750 `"Ohio"', add
label define ancestr2d_lbl 9760 `"Oklahoma"', add
label define ancestr2d_lbl 9770 `"Oregon"', add
label define ancestr2d_lbl 9780 `"Pennsylvania"', add
label define ancestr2d_lbl 9790 `"Rhode Island"', add
label define ancestr2d_lbl 9800 `"South Carolina"', add
label define ancestr2d_lbl 9810 `"South Dakota"', add
label define ancestr2d_lbl 9820 `"Tennessee"', add
label define ancestr2d_lbl 9830 `"Texas"', add
label define ancestr2d_lbl 9840 `"Utah"', add
label define ancestr2d_lbl 9850 `"Vermont"', add
label define ancestr2d_lbl 9860 `"Virginia"', add
label define ancestr2d_lbl 9870 `"Washington"', add
label define ancestr2d_lbl 9880 `"West Virginia"', add
label define ancestr2d_lbl 9890 `"Wisconsin"', add
label define ancestr2d_lbl 9900 `"Wyoming"', add
label define ancestr2d_lbl 9930 `"Southerner"', add
label define ancestr2d_lbl 9940 `"North American"', add
label define ancestr2d_lbl 9950 `"Mixture"', add
label define ancestr2d_lbl 9960 `"Uncodable"', add
label define ancestr2d_lbl 9961 `"Not Classified"', add
label define ancestr2d_lbl 9962 `"Suppressed"', add
label define ancestr2d_lbl 9970 `"Deferred Cases"', add
label define ancestr2d_lbl 9980 `"Other"', add
label define ancestr2d_lbl 9990 `"Not Reported"', add
label values ancestr2d ancestr2d_lbl

label define citizen_lbl 0 `"N/A"'
label define citizen_lbl 1 `"Born abroad of American parents"', add
label define citizen_lbl 2 `"Naturalized citizen"', add
label define citizen_lbl 3 `"Not a citizen"', add
label define citizen_lbl 4 `"Not a citizen, but has received first papers"', add
label define citizen_lbl 5 `"Foreign born, citizenship status not reported"', add
label define citizen_lbl 8 `"Illegible"', add
label define citizen_lbl 9 `"Missing/blank"', add
label values citizen citizen_lbl

label define yrnatur_lbl 1806 `"1806"'
label define yrnatur_lbl 1807 `"1807"', add
label define yrnatur_lbl 1808 `"1808"', add
label define yrnatur_lbl 1809 `"1809"', add
label define yrnatur_lbl 1810 `"1810"', add
label define yrnatur_lbl 1811 `"1811"', add
label define yrnatur_lbl 1812 `"1812"', add
label define yrnatur_lbl 1813 `"1813"', add
label define yrnatur_lbl 1814 `"1814"', add
label define yrnatur_lbl 1815 `"1815"', add
label define yrnatur_lbl 1816 `"1816"', add
label define yrnatur_lbl 1817 `"1817"', add
label define yrnatur_lbl 1818 `"1818"', add
label define yrnatur_lbl 1819 `"1819"', add
label define yrnatur_lbl 1820 `"1820"', add
label define yrnatur_lbl 1821 `"1821"', add
label define yrnatur_lbl 1822 `"1822"', add
label define yrnatur_lbl 1823 `"1823"', add
label define yrnatur_lbl 1824 `"1824"', add
label define yrnatur_lbl 1825 `"1825"', add
label define yrnatur_lbl 1826 `"1826"', add
label define yrnatur_lbl 1827 `"1827"', add
label define yrnatur_lbl 1828 `"1828"', add
label define yrnatur_lbl 1829 `"1829"', add
label define yrnatur_lbl 1830 `"1830"', add
label define yrnatur_lbl 1831 `"1831"', add
label define yrnatur_lbl 1832 `"1832"', add
label define yrnatur_lbl 1833 `"1833"', add
label define yrnatur_lbl 1834 `"1834"', add
label define yrnatur_lbl 1835 `"1835"', add
label define yrnatur_lbl 1836 `"1836"', add
label define yrnatur_lbl 1837 `"1837"', add
label define yrnatur_lbl 1838 `"1838"', add
label define yrnatur_lbl 1839 `"1839"', add
label define yrnatur_lbl 1840 `"1840"', add
label define yrnatur_lbl 1841 `"1841"', add
label define yrnatur_lbl 1842 `"1842"', add
label define yrnatur_lbl 1843 `"1843"', add
label define yrnatur_lbl 1844 `"1844"', add
label define yrnatur_lbl 1845 `"1845"', add
label define yrnatur_lbl 1846 `"1846"', add
label define yrnatur_lbl 1847 `"1847"', add
label define yrnatur_lbl 1848 `"1848"', add
label define yrnatur_lbl 1849 `"1849"', add
label define yrnatur_lbl 1850 `"1850"', add
label define yrnatur_lbl 1851 `"1851"', add
label define yrnatur_lbl 1852 `"1852"', add
label define yrnatur_lbl 1853 `"1853"', add
label define yrnatur_lbl 1854 `"1854"', add
label define yrnatur_lbl 1855 `"1855"', add
label define yrnatur_lbl 1856 `"1856"', add
label define yrnatur_lbl 1857 `"1857"', add
label define yrnatur_lbl 1858 `"1858"', add
label define yrnatur_lbl 1859 `"1859"', add
label define yrnatur_lbl 1860 `"1860"', add
label define yrnatur_lbl 1861 `"1861"', add
label define yrnatur_lbl 1862 `"1862"', add
label define yrnatur_lbl 1863 `"1863"', add
label define yrnatur_lbl 1864 `"1864"', add
label define yrnatur_lbl 1865 `"1865"', add
label define yrnatur_lbl 1866 `"1866"', add
label define yrnatur_lbl 1867 `"1867"', add
label define yrnatur_lbl 1868 `"1868"', add
label define yrnatur_lbl 1869 `"1869"', add
label define yrnatur_lbl 1870 `"1870"', add
label define yrnatur_lbl 1871 `"1871"', add
label define yrnatur_lbl 1872 `"1872"', add
label define yrnatur_lbl 1873 `"1873"', add
label define yrnatur_lbl 1874 `"1874"', add
label define yrnatur_lbl 1875 `"1875"', add
label define yrnatur_lbl 1876 `"1876"', add
label define yrnatur_lbl 1877 `"1877"', add
label define yrnatur_lbl 1878 `"1878"', add
label define yrnatur_lbl 1879 `"1879"', add
label define yrnatur_lbl 1880 `"1880"', add
label define yrnatur_lbl 1881 `"1881"', add
label define yrnatur_lbl 1882 `"1882"', add
label define yrnatur_lbl 1883 `"1883"', add
label define yrnatur_lbl 1884 `"1884"', add
label define yrnatur_lbl 1885 `"1885"', add
label define yrnatur_lbl 1886 `"1886"', add
label define yrnatur_lbl 1887 `"1887"', add
label define yrnatur_lbl 1888 `"1888"', add
label define yrnatur_lbl 1889 `"1889"', add
label define yrnatur_lbl 1890 `"1890"', add
label define yrnatur_lbl 1891 `"1891"', add
label define yrnatur_lbl 1892 `"1892"', add
label define yrnatur_lbl 1893 `"1893"', add
label define yrnatur_lbl 1894 `"1894"', add
label define yrnatur_lbl 1895 `"1895"', add
label define yrnatur_lbl 1896 `"1896"', add
label define yrnatur_lbl 1897 `"1897"', add
label define yrnatur_lbl 1898 `"1898"', add
label define yrnatur_lbl 1899 `"1899"', add
label define yrnatur_lbl 1900 `"1900"', add
label define yrnatur_lbl 1901 `"1901"', add
label define yrnatur_lbl 1902 `"1902"', add
label define yrnatur_lbl 1903 `"1903"', add
label define yrnatur_lbl 1904 `"1904"', add
label define yrnatur_lbl 1905 `"1905"', add
label define yrnatur_lbl 1906 `"1906"', add
label define yrnatur_lbl 1907 `"1907"', add
label define yrnatur_lbl 1908 `"1908"', add
label define yrnatur_lbl 1909 `"1909"', add
label define yrnatur_lbl 1910 `"1910"', add
label define yrnatur_lbl 1911 `"1911"', add
label define yrnatur_lbl 1912 `"1912"', add
label define yrnatur_lbl 1913 `"1913"', add
label define yrnatur_lbl 1914 `"1914"', add
label define yrnatur_lbl 1915 `"1915"', add
label define yrnatur_lbl 1916 `"1916"', add
label define yrnatur_lbl 1917 `"1917"', add
label define yrnatur_lbl 1918 `"1918"', add
label define yrnatur_lbl 1919 `"1919"', add
label define yrnatur_lbl 1920 `"1920"', add
label define yrnatur_lbl 1921 `"1921"', add
label define yrnatur_lbl 1922 `"1922"', add
label define yrnatur_lbl 1923 `"1923"', add
label define yrnatur_lbl 1924 `"1924"', add
label define yrnatur_lbl 1925 `"1925 (1925 or earlier, ACS/PRCS pre 2012)"', add
label define yrnatur_lbl 1926 `"1925 (1925 or earlier, ACS/PRCS pre 2012)"', add
label define yrnatur_lbl 1927 `"1927"', add
label define yrnatur_lbl 1928 `"1928 (1928 or earlier, 2012-2016 ACS/PRCS)"', add
label define yrnatur_lbl 1929 `"1929 (1929-1933, 2012-2016 ACS/PRCS)"', add
label define yrnatur_lbl 1930 `"1930"', add
label define yrnatur_lbl 1931 `"1931 (1931-1935, ACS/PRCS pre 2012)"', add
label define yrnatur_lbl 1932 `"1932"', add
label define yrnatur_lbl 1933 `"1933"', add
label define yrnatur_lbl 1934 `"1934 (1934-1939, 2012-2016 ACS/PRCS)"', add
label define yrnatur_lbl 1935 `"1935"', add
label define yrnatur_lbl 1936 `"1936 (1936-1940, ACS/PRCS pre 2012)"', add
label define yrnatur_lbl 1937 `"1937"', add
label define yrnatur_lbl 1938 `"1938"', add
label define yrnatur_lbl 1939 `"1939 (1939 or earlier, 2017-2018 ACS/PRCS)"', add
label define yrnatur_lbl 1940 `"1940 (1940-1942, 2012-2016 ACS/PRCS; 1940-1944, 2017-2018 ACS/PRCS)"', add
label define yrnatur_lbl 1941 `"1941 (1941-1942, ACS/PRCS pre 2012)"', add
label define yrnatur_lbl 1942 `"1942"', add
label define yrnatur_lbl 1943 `"1943 (1943-44, 2012-2016 ACS/PRCS)"', add
label define yrnatur_lbl 1944 `"1944 (1944 or earlier, 2019-onward ACS/PRCS)"', add
label define yrnatur_lbl 1945 `"1945 (1945-1947, 2017-onward ACS/PRCS)"', add
label define yrnatur_lbl 1946 `"1946 (1946-1947, 2012-2016 ACS/PRCS)"', add
label define yrnatur_lbl 1947 `"1947 (1947 or earlier, 2022-onward ACS/PRCS)"', add
label define yrnatur_lbl 1948 `"1948 (1948-1949, 2017-onward ACS/PRCS)"', add
label define yrnatur_lbl 1949 `"1949"', add
label define yrnatur_lbl 1950 `"1950 (1950-1951, 2020-onward ACS/PRCS)"', add
label define yrnatur_lbl 1951 `"1951"', add
label define yrnatur_lbl 1952 `"1952 (1952-1953, 2024-onward ACS/PRCS)"', add
label define yrnatur_lbl 1953 `"1953"', add
label define yrnatur_lbl 1954 `"1954"', add
label define yrnatur_lbl 1955 `"1955"', add
label define yrnatur_lbl 1956 `"1956"', add
label define yrnatur_lbl 1957 `"1957"', add
label define yrnatur_lbl 1958 `"1958"', add
label define yrnatur_lbl 1959 `"1959"', add
label define yrnatur_lbl 1960 `"1960"', add
label define yrnatur_lbl 1961 `"1961"', add
label define yrnatur_lbl 1962 `"1962"', add
label define yrnatur_lbl 1963 `"1963"', add
label define yrnatur_lbl 1964 `"1964"', add
label define yrnatur_lbl 1965 `"1965"', add
label define yrnatur_lbl 1966 `"1966"', add
label define yrnatur_lbl 1967 `"1967"', add
label define yrnatur_lbl 1968 `"1968"', add
label define yrnatur_lbl 1969 `"1969"', add
label define yrnatur_lbl 1970 `"1970"', add
label define yrnatur_lbl 1971 `"1971"', add
label define yrnatur_lbl 1972 `"1972"', add
label define yrnatur_lbl 1973 `"1973"', add
label define yrnatur_lbl 1974 `"1974"', add
label define yrnatur_lbl 1975 `"1975"', add
label define yrnatur_lbl 1976 `"1976"', add
label define yrnatur_lbl 1977 `"1977"', add
label define yrnatur_lbl 1978 `"1978"', add
label define yrnatur_lbl 1979 `"1979"', add
label define yrnatur_lbl 1980 `"1980"', add
label define yrnatur_lbl 1981 `"1981"', add
label define yrnatur_lbl 1982 `"1982"', add
label define yrnatur_lbl 1983 `"1983"', add
label define yrnatur_lbl 1984 `"1984"', add
label define yrnatur_lbl 1985 `"1985"', add
label define yrnatur_lbl 1986 `"1986"', add
label define yrnatur_lbl 1987 `"1987"', add
label define yrnatur_lbl 1988 `"1988"', add
label define yrnatur_lbl 1989 `"1989"', add
label define yrnatur_lbl 1990 `"1990"', add
label define yrnatur_lbl 1991 `"1991"', add
label define yrnatur_lbl 1992 `"1992"', add
label define yrnatur_lbl 1993 `"1993"', add
label define yrnatur_lbl 1994 `"1994"', add
label define yrnatur_lbl 1995 `"1995"', add
label define yrnatur_lbl 1996 `"1996"', add
label define yrnatur_lbl 1997 `"1997"', add
label define yrnatur_lbl 1998 `"1998"', add
label define yrnatur_lbl 1999 `"1999"', add
label define yrnatur_lbl 2000 `"2000"', add
label define yrnatur_lbl 2001 `"2001"', add
label define yrnatur_lbl 2002 `"2002"', add
label define yrnatur_lbl 2003 `"2003"', add
label define yrnatur_lbl 2004 `"2004"', add
label define yrnatur_lbl 2005 `"2005"', add
label define yrnatur_lbl 2006 `"2006"', add
label define yrnatur_lbl 2007 `"2007"', add
label define yrnatur_lbl 2008 `"2008"', add
label define yrnatur_lbl 2009 `"2009"', add
label define yrnatur_lbl 2010 `"2010"', add
label define yrnatur_lbl 2011 `"2011"', add
label define yrnatur_lbl 2012 `"2012"', add
label define yrnatur_lbl 2013 `"2013"', add
label define yrnatur_lbl 2014 `"2014"', add
label define yrnatur_lbl 2015 `"2015"', add
label define yrnatur_lbl 2016 `"2016"', add
label define yrnatur_lbl 2017 `"2017"', add
label define yrnatur_lbl 2018 `"2018"', add
label define yrnatur_lbl 2019 `"2019"', add
label define yrnatur_lbl 2020 `"2020"', add
label define yrnatur_lbl 2021 `"2021"', add
label define yrnatur_lbl 2022 `"2022"', add
label define yrnatur_lbl 2023 `"2023"', add
label define yrnatur_lbl 2024 `"2024"', add
label define yrnatur_lbl 9997 `"Unknown"', add
label define yrnatur_lbl 9998 `"Illegible"', add
label define yrnatur_lbl 9999 `"N/A"', add
label values yrnatur yrnatur_lbl

label define yrimmig_lbl 0000 `"N/A"'
label define yrimmig_lbl 1790 `"1790"', add
label define yrimmig_lbl 1791 `"1791"', add
label define yrimmig_lbl 1792 `"1792"', add
label define yrimmig_lbl 1793 `"1793"', add
label define yrimmig_lbl 1794 `"1794"', add
label define yrimmig_lbl 1795 `"1795"', add
label define yrimmig_lbl 1796 `"1796"', add
label define yrimmig_lbl 1797 `"1797"', add
label define yrimmig_lbl 1798 `"1798"', add
label define yrimmig_lbl 1799 `"1799"', add
label define yrimmig_lbl 1800 `"1800"', add
label define yrimmig_lbl 1801 `"1801"', add
label define yrimmig_lbl 1802 `"1802"', add
label define yrimmig_lbl 1803 `"1803"', add
label define yrimmig_lbl 1804 `"1804"', add
label define yrimmig_lbl 1805 `"1805"', add
label define yrimmig_lbl 1806 `"1806"', add
label define yrimmig_lbl 1807 `"1807"', add
label define yrimmig_lbl 1808 `"1808"', add
label define yrimmig_lbl 1809 `"1809"', add
label define yrimmig_lbl 1810 `"1810"', add
label define yrimmig_lbl 1811 `"1811"', add
label define yrimmig_lbl 1812 `"1812"', add
label define yrimmig_lbl 1813 `"1813"', add
label define yrimmig_lbl 1814 `"1814"', add
label define yrimmig_lbl 1815 `"1815"', add
label define yrimmig_lbl 1816 `"1816"', add
label define yrimmig_lbl 1817 `"1817"', add
label define yrimmig_lbl 1818 `"1818"', add
label define yrimmig_lbl 1819 `"1819"', add
label define yrimmig_lbl 1820 `"1820"', add
label define yrimmig_lbl 1821 `"1821"', add
label define yrimmig_lbl 1822 `"1822"', add
label define yrimmig_lbl 1823 `"1823"', add
label define yrimmig_lbl 1824 `"1824"', add
label define yrimmig_lbl 1825 `"1825"', add
label define yrimmig_lbl 1826 `"1826"', add
label define yrimmig_lbl 1827 `"1827"', add
label define yrimmig_lbl 1828 `"1828"', add
label define yrimmig_lbl 1829 `"1829"', add
label define yrimmig_lbl 1830 `"1830"', add
label define yrimmig_lbl 1831 `"1831"', add
label define yrimmig_lbl 1832 `"1832"', add
label define yrimmig_lbl 1833 `"1833"', add
label define yrimmig_lbl 1834 `"1834"', add
label define yrimmig_lbl 1835 `"1835"', add
label define yrimmig_lbl 1836 `"1836"', add
label define yrimmig_lbl 1837 `"1837"', add
label define yrimmig_lbl 1838 `"1838"', add
label define yrimmig_lbl 1839 `"1839"', add
label define yrimmig_lbl 1840 `"1840"', add
label define yrimmig_lbl 1841 `"1841"', add
label define yrimmig_lbl 1842 `"1842"', add
label define yrimmig_lbl 1843 `"1843"', add
label define yrimmig_lbl 1844 `"1844"', add
label define yrimmig_lbl 1845 `"1845"', add
label define yrimmig_lbl 1846 `"1846"', add
label define yrimmig_lbl 1847 `"1847"', add
label define yrimmig_lbl 1848 `"1848"', add
label define yrimmig_lbl 1849 `"1849"', add
label define yrimmig_lbl 1850 `"1850"', add
label define yrimmig_lbl 1851 `"1851"', add
label define yrimmig_lbl 1852 `"1852"', add
label define yrimmig_lbl 1853 `"1853"', add
label define yrimmig_lbl 1854 `"1854"', add
label define yrimmig_lbl 1855 `"1855"', add
label define yrimmig_lbl 1856 `"1856"', add
label define yrimmig_lbl 1857 `"1857"', add
label define yrimmig_lbl 1858 `"1858"', add
label define yrimmig_lbl 1859 `"1859"', add
label define yrimmig_lbl 1860 `"1860"', add
label define yrimmig_lbl 1861 `"1861"', add
label define yrimmig_lbl 1862 `"1862"', add
label define yrimmig_lbl 1863 `"1863"', add
label define yrimmig_lbl 1864 `"1864"', add
label define yrimmig_lbl 1865 `"1865"', add
label define yrimmig_lbl 1866 `"1866"', add
label define yrimmig_lbl 1867 `"1867"', add
label define yrimmig_lbl 1868 `"1868"', add
label define yrimmig_lbl 1869 `"1869"', add
label define yrimmig_lbl 1870 `"1870"', add
label define yrimmig_lbl 1871 `"1871"', add
label define yrimmig_lbl 1872 `"1872"', add
label define yrimmig_lbl 1873 `"1873"', add
label define yrimmig_lbl 1874 `"1874"', add
label define yrimmig_lbl 1875 `"1875"', add
label define yrimmig_lbl 1876 `"1876"', add
label define yrimmig_lbl 1877 `"1877"', add
label define yrimmig_lbl 1878 `"1878"', add
label define yrimmig_lbl 1879 `"1879"', add
label define yrimmig_lbl 1880 `"1880"', add
label define yrimmig_lbl 1881 `"1881"', add
label define yrimmig_lbl 1882 `"1882"', add
label define yrimmig_lbl 1883 `"1883"', add
label define yrimmig_lbl 1884 `"1884"', add
label define yrimmig_lbl 1885 `"1885"', add
label define yrimmig_lbl 1886 `"1886"', add
label define yrimmig_lbl 1887 `"1887"', add
label define yrimmig_lbl 1888 `"1888"', add
label define yrimmig_lbl 1889 `"1889"', add
label define yrimmig_lbl 1890 `"1890"', add
label define yrimmig_lbl 1891 `"1891"', add
label define yrimmig_lbl 1892 `"1892"', add
label define yrimmig_lbl 1893 `"1893"', add
label define yrimmig_lbl 1894 `"1894"', add
label define yrimmig_lbl 1895 `"1895"', add
label define yrimmig_lbl 1896 `"1896"', add
label define yrimmig_lbl 1897 `"1897"', add
label define yrimmig_lbl 1898 `"1898"', add
label define yrimmig_lbl 1899 `"1899"', add
label define yrimmig_lbl 1900 `"1900"', add
label define yrimmig_lbl 1901 `"1901"', add
label define yrimmig_lbl 1902 `"1902"', add
label define yrimmig_lbl 1903 `"1903"', add
label define yrimmig_lbl 1904 `"1904"', add
label define yrimmig_lbl 1905 `"1905"', add
label define yrimmig_lbl 1906 `"1906"', add
label define yrimmig_lbl 1907 `"1907"', add
label define yrimmig_lbl 1908 `"1908"', add
label define yrimmig_lbl 1909 `"1909"', add
label define yrimmig_lbl 1910 `"1910 (2000 PUMS: 1910 or earlier)"', add
label define yrimmig_lbl 1911 `"1911 (2000 PUMS: 1911-1914)"', add
label define yrimmig_lbl 1912 `"1912"', add
label define yrimmig_lbl 1913 `"1913"', add
label define yrimmig_lbl 1914 `"1914 (1970 PUMS: 1914 or earlier)"', add
label define yrimmig_lbl 1915 `"1915 (1970 PUMS: 1915-1924; 2000 PUMS: 1915-1919)"', add
label define yrimmig_lbl 1916 `"1916"', add
label define yrimmig_lbl 1917 `"1917"', add
label define yrimmig_lbl 1918 `"1918"', add
label define yrimmig_lbl 1919 `"1919 (2005 - 2011 ACS & 2012 - 2016 ACS 1-yr & 2016 5-yr files: 1919 or earlier)"', add
label define yrimmig_lbl 1920 `"1920"', add
label define yrimmig_lbl 1921 `"1921 (2012 - 2016 ACS 1-yr & 2016 5-yr files: 1921 or earlier)"', add
label define yrimmig_lbl 1922 `"1922 (2012 - 2016 ACS 1-yr & 2016 5-yr files: 1922-1923)"', add
label define yrimmig_lbl 1923 `"1923"', add
label define yrimmig_lbl 1924 `"1924 (2012 - 2016 ACS 1-yr & 2016 5-yr files: 1924-1925)"', add
label define yrimmig_lbl 1925 `"1925 (1970 PUMS: 1925-1934; 2017 ACS: 1925 or earlier)"', add
label define yrimmig_lbl 1926 `"1926 (2012 - 2016 ACS 1-yr & 2016 5-yr files: 1926-1927; 2017 ACS: 1926-1929)"', add
label define yrimmig_lbl 1927 `"1927"', add
label define yrimmig_lbl 1928 `"1928 (2012 - 2016 ACS 1-yr & 2016 5-yr files: 1928-1929)"', add
label define yrimmig_lbl 1929 `"1929 (2018 - 2019 ACS: 1929 or earlier)"', add
label define yrimmig_lbl 1930 `"1930 (2000 PUMS, 2017 ACS, and 2018 - 2019 ACS: 1930-1934; 2012 - 2016 ACS 1-yr & 2016 5-yr files: 1930-1931)"', add
label define yrimmig_lbl 1931 `"1931 (2005 - 2011 ACS: 1931-1932)"', add
label define yrimmig_lbl 1932 `"1932 (2012 - 2016 ACS 1-yr & 2016 5-yr files: 1932-1934)"', add
label define yrimmig_lbl 1933 `"1933 (2005 - 2011 ACS: 1933-1934)"', add
label define yrimmig_lbl 1934 `"1934 (2020 - 2022: 1934 or earlier)"', add
label define yrimmig_lbl 1935 `"1935 (1970 PUMS: 1935-1944; 2012 - 2016 ACS 1-yr & 2016 5-yr files: 1935-1936; 2017 - 2022 ACS: 1935-1938)"', add
label define yrimmig_lbl 1936 `"1936"', add
label define yrimmig_lbl 1937 `"1937 (2012 - 2016 ACS 1-yr & 2016 5-yr files: 1937-1938)"', add
label define yrimmig_lbl 1938 `"1938 (2023 ACS - Onward: 1938 or earlier)"', add
label define yrimmig_lbl 1939 `"1939 (2018 - 2019 ACS: 1939-1940; 2020 ACS - Onward: 1939-1942)"', add
label define yrimmig_lbl 1940 `"1940"', add
label define yrimmig_lbl 1941 `"1941 (2017 - 2019 ACS: 1941-1942)"', add
label define yrimmig_lbl 1942 `"1942"', add
label define yrimmig_lbl 1943 `"1943 (2012 - 2016 ACS 1-yr & 2016 5-yr files & 2017 ACS - Onward: 1943-1944)"', add
label define yrimmig_lbl 1944 `"1944"', add
label define yrimmig_lbl 1945 `"1945 (1970 PUMS: 1945-1949)"', add
label define yrimmig_lbl 1946 `"1946"', add
label define yrimmig_lbl 1947 `"1947"', add
label define yrimmig_lbl 1948 `"1948"', add
label define yrimmig_lbl 1949 `"1949 (1980 - 1990 PUMS: 1949 or earlier)"', add
label define yrimmig_lbl 1950 `"1950 (1970 PUMS: 1950-1954; 1980 - 1990 PUMS: 1950-1959)"', add
label define yrimmig_lbl 1951 `"1951"', add
label define yrimmig_lbl 1952 `"1952"', add
label define yrimmig_lbl 1953 `"1953"', add
label define yrimmig_lbl 1954 `"1954"', add
label define yrimmig_lbl 1955 `"1955 (1970 PUMS: 1955-1959)"', add
label define yrimmig_lbl 1956 `"1956"', add
label define yrimmig_lbl 1957 `"1957"', add
label define yrimmig_lbl 1958 `"1958"', add
label define yrimmig_lbl 1959 `"1959"', add
label define yrimmig_lbl 1960 `"1960 (1970 - 1990 PUMS: 1960 - 1964)"', add
label define yrimmig_lbl 1961 `"1961"', add
label define yrimmig_lbl 1962 `"1962"', add
label define yrimmig_lbl 1963 `"1963"', add
label define yrimmig_lbl 1964 `"1964"', add
label define yrimmig_lbl 1965 `"1965 (1970 PUMS: 1965-1970; 1980 - 1990 PUMS: 1965-1969)"', add
label define yrimmig_lbl 1966 `"1966"', add
label define yrimmig_lbl 1967 `"1967"', add
label define yrimmig_lbl 1968 `"1968"', add
label define yrimmig_lbl 1969 `"1969"', add
label define yrimmig_lbl 1970 `"1970 (1980 - 1990 PUMS: 1970-1974)"', add
label define yrimmig_lbl 1971 `"1971"', add
label define yrimmig_lbl 1972 `"1972"', add
label define yrimmig_lbl 1973 `"1973"', add
label define yrimmig_lbl 1974 `"1974"', add
label define yrimmig_lbl 1975 `"1975 (1980 PUMS: 1975-1980; 1990 PUMS: 1975-1979)"', add
label define yrimmig_lbl 1976 `"1976"', add
label define yrimmig_lbl 1977 `"1977"', add
label define yrimmig_lbl 1978 `"1978"', add
label define yrimmig_lbl 1979 `"1979"', add
label define yrimmig_lbl 1980 `"1980 (1990 PUMS: 1980-1981)"', add
label define yrimmig_lbl 1981 `"1981"', add
label define yrimmig_lbl 1982 `"1982 (1990 PUMS: 1982-1984)"', add
label define yrimmig_lbl 1983 `"1983"', add
label define yrimmig_lbl 1984 `"1984"', add
label define yrimmig_lbl 1985 `"1985 (1990 PUMS: 1985-1986)"', add
label define yrimmig_lbl 1986 `"1986"', add
label define yrimmig_lbl 1987 `"1987 (1990 PUMS: 1987-1990)"', add
label define yrimmig_lbl 1988 `"1988"', add
label define yrimmig_lbl 1989 `"1989"', add
label define yrimmig_lbl 1990 `"1990"', add
label define yrimmig_lbl 1991 `"1991"', add
label define yrimmig_lbl 1992 `"1992"', add
label define yrimmig_lbl 1993 `"1993"', add
label define yrimmig_lbl 1994 `"1994"', add
label define yrimmig_lbl 1995 `"1995"', add
label define yrimmig_lbl 1996 `"1996"', add
label define yrimmig_lbl 1997 `"1997"', add
label define yrimmig_lbl 1998 `"1998"', add
label define yrimmig_lbl 1999 `"1999"', add
label define yrimmig_lbl 2000 `"2000"', add
label define yrimmig_lbl 2001 `"2001"', add
label define yrimmig_lbl 2002 `"2002"', add
label define yrimmig_lbl 2003 `"2003"', add
label define yrimmig_lbl 2004 `"2004"', add
label define yrimmig_lbl 2005 `"2005"', add
label define yrimmig_lbl 2006 `"2006"', add
label define yrimmig_lbl 2007 `"2007"', add
label define yrimmig_lbl 2008 `"2008"', add
label define yrimmig_lbl 2009 `"2009"', add
label define yrimmig_lbl 2010 `"2010"', add
label define yrimmig_lbl 2011 `"2011"', add
label define yrimmig_lbl 2012 `"2012"', add
label define yrimmig_lbl 2013 `"2013"', add
label define yrimmig_lbl 2014 `"2014"', add
label define yrimmig_lbl 2015 `"2015"', add
label define yrimmig_lbl 2016 `"2016"', add
label define yrimmig_lbl 2017 `"2017"', add
label define yrimmig_lbl 2018 `"2018"', add
label define yrimmig_lbl 2019 `"2019"', add
label define yrimmig_lbl 2020 `"2020"', add
label define yrimmig_lbl 2021 `"2021"', add
label define yrimmig_lbl 2022 `"2022"', add
label define yrimmig_lbl 2023 `"2023"', add
label define yrimmig_lbl 2024 `"2024"', add
label define yrimmig_lbl 0996 `"Not reported"', add
label values yrimmig yrimmig_lbl

label define yrsusa1_lbl 00 `"N/A or less than one year"'
label values yrsusa1 yrsusa1_lbl

label define yrsusa2_lbl 0 `"N/A"'
label define yrsusa2_lbl 1 `"0-5 years"', add
label define yrsusa2_lbl 2 `"6-10 years"', add
label define yrsusa2_lbl 3 `"11-15 years"', add
label define yrsusa2_lbl 4 `"16-20 years"', add
label define yrsusa2_lbl 5 `"21+ years"', add
label define yrsusa2_lbl 9 `"Missing"', add
label values yrsusa2 yrsusa2_lbl

label define language_lbl 00 `"N/A or blank"'
label define language_lbl 01 `"English"', add
label define language_lbl 02 `"German"', add
label define language_lbl 03 `"Yiddish, Jewish"', add
label define language_lbl 04 `"Dutch"', add
label define language_lbl 05 `"Swedish"', add
label define language_lbl 06 `"Danish"', add
label define language_lbl 07 `"Norwegian"', add
label define language_lbl 08 `"Icelandic"', add
label define language_lbl 09 `"Scandinavian"', add
label define language_lbl 10 `"Italian"', add
label define language_lbl 11 `"French"', add
label define language_lbl 12 `"Spanish"', add
label define language_lbl 13 `"Portuguese"', add
label define language_lbl 14 `"Rumanian"', add
label define language_lbl 15 `"Celtic"', add
label define language_lbl 16 `"Greek"', add
label define language_lbl 17 `"Albanian"', add
label define language_lbl 18 `"Russian"', add
label define language_lbl 19 `"Ukrainian, Ruthenian, Little Russian"', add
label define language_lbl 20 `"Czech"', add
label define language_lbl 21 `"Polish"', add
label define language_lbl 22 `"Slovak"', add
label define language_lbl 23 `"Serbo-Croatian, Yugoslavian, Slavonian"', add
label define language_lbl 24 `"Slovene"', add
label define language_lbl 25 `"Lithuanian"', add
label define language_lbl 26 `"Other Balto-Slavic"', add
label define language_lbl 27 `"Slavic unknown"', add
label define language_lbl 28 `"Armenian"', add
label define language_lbl 29 `"Persian, Iranian, Farsi"', add
label define language_lbl 30 `"Other Persian dialects"', add
label define language_lbl 31 `"Hindi and related"', add
label define language_lbl 32 `"Romany, Gypsy"', add
label define language_lbl 33 `"Finnish"', add
label define language_lbl 34 `"Magyar, Hungarian"', add
label define language_lbl 35 `"Uralic"', add
label define language_lbl 36 `"Turkish"', add
label define language_lbl 37 `"Other Altaic"', add
label define language_lbl 38 `"Caucasian, Georgian, Avar"', add
label define language_lbl 39 `"Basque"', add
label define language_lbl 40 `"Dravidian"', add
label define language_lbl 41 `"Kurukh"', add
label define language_lbl 42 `"Burushaski"', add
label define language_lbl 43 `"Chinese"', add
label define language_lbl 44 `"Tibetan"', add
label define language_lbl 45 `"Burmese, Lisu, Lolo"', add
label define language_lbl 46 `"Kachin"', add
label define language_lbl 47 `"Thai, Siamese, Lao"', add
label define language_lbl 48 `"Japanese"', add
label define language_lbl 49 `"Korean"', add
label define language_lbl 50 `"Vietnamese"', add
label define language_lbl 51 `"Other East/Southeast Asian"', add
label define language_lbl 52 `"Indonesian"', add
label define language_lbl 53 `"Other Malayan"', add
label define language_lbl 54 `"Filipino, Tagalog"', add
label define language_lbl 55 `"Micronesian, Polynesian"', add
label define language_lbl 56 `"Hawaiian"', add
label define language_lbl 57 `"Arabic"', add
label define language_lbl 58 `"Near East Arabic dialect"', add
label define language_lbl 59 `"Hebrew, Israeli"', add
label define language_lbl 60 `"Amharic, Ethiopian, etc."', add
label define language_lbl 61 `"Hamitic"', add
label define language_lbl 62 `"Other Afro-Asiatic languages"', add
label define language_lbl 63 `"Sub-Saharan Africa"', add
label define language_lbl 64 `"African, n.s."', add
label define language_lbl 70 `"American Indian (all)"', add
label define language_lbl 71 `"Aleut, Eskimo"', add
label define language_lbl 72 `"Algonquian"', add
label define language_lbl 73 `"Salish, Flathead"', add
label define language_lbl 74 `"Athapascan"', add
label define language_lbl 75 `"Navajo"', add
label define language_lbl 76 `"Penutian-Sahaptin"', add
label define language_lbl 77 `"Other Penutian"', add
label define language_lbl 78 `"Zuni"', add
label define language_lbl 79 `"Yuman"', add
label define language_lbl 80 `"Other Hokan languages"', add
label define language_lbl 81 `"Siouan languages"', add
label define language_lbl 82 `"Muskogean"', add
label define language_lbl 83 `"Keres"', add
label define language_lbl 84 `"Iroquoian"', add
label define language_lbl 85 `"Caddoan"', add
label define language_lbl 86 `"Shoshonean/Hopi"', add
label define language_lbl 87 `"Pima, Papago"', add
label define language_lbl 88 `"Yaqui and other Sonoran, nec"', add
label define language_lbl 89 `"Aztecan, Nahuatl, Uto-Aztecan"', add
label define language_lbl 90 `"Tanoan languages"', add
label define language_lbl 91 `"Other Indian languages"', add
label define language_lbl 92 `"Mayan languages"', add
label define language_lbl 93 `"American Indian, n.s."', add
label define language_lbl 94 `"Native"', add
label define language_lbl 95 `"No language"', add
label define language_lbl 96 `"Other or not reported"', add
label define language_lbl 99 `"Not reported, blank"', add
label values language language_lbl

label define languaged_lbl 0000 `"N/A or blank"'
label define languaged_lbl 0100 `"English"', add
label define languaged_lbl 0110 `"Jamaican Creole"', add
label define languaged_lbl 0120 `"Krio, Pidgin Krio"', add
label define languaged_lbl 0130 `"Hawaiian Pidgin"', add
label define languaged_lbl 0140 `"Pidgin"', add
label define languaged_lbl 0150 `"Gullah, Geechee"', add
label define languaged_lbl 0160 `"Saramacca"', add
label define languaged_lbl 0170 `"Other English-based Creole languages"', add
label define languaged_lbl 0200 `"German"', add
label define languaged_lbl 0210 `"Austrian"', add
label define languaged_lbl 0220 `"Swiss"', add
label define languaged_lbl 0230 `"Luxembourgian"', add
label define languaged_lbl 0240 `"Pennsylvania Dutch"', add
label define languaged_lbl 0300 `"Yiddish, Jewish"', add
label define languaged_lbl 0310 `"Jewish"', add
label define languaged_lbl 0320 `"Yiddish"', add
label define languaged_lbl 0400 `"Dutch"', add
label define languaged_lbl 0410 `"Dutch, Flemish, Belgian"', add
label define languaged_lbl 0420 `"Afrikaans"', add
label define languaged_lbl 0430 `"Frisian"', add
label define languaged_lbl 0440 `"Dutch, Afrikaans, Frisian"', add
label define languaged_lbl 0450 `"Belgian, Flemish"', add
label define languaged_lbl 0460 `"Belgian"', add
label define languaged_lbl 0470 `"Flemish"', add
label define languaged_lbl 0500 `"Swedish"', add
label define languaged_lbl 0600 `"Danish"', add
label define languaged_lbl 0700 `"Norwegian"', add
label define languaged_lbl 0800 `"Icelandic"', add
label define languaged_lbl 0810 `"Faroese"', add
label define languaged_lbl 0900 `"Scandinavian"', add
label define languaged_lbl 1000 `"Italian"', add
label define languaged_lbl 1010 `"Rhaeto-Romanic, Ladin"', add
label define languaged_lbl 1020 `"Friulian"', add
label define languaged_lbl 1030 `"Romansh"', add
label define languaged_lbl 1100 `"French"', add
label define languaged_lbl 1110 `"French, Walloon"', add
label define languaged_lbl 1120 `"Provencal"', add
label define languaged_lbl 1130 `"Patois"', add
label define languaged_lbl 1140 `"French or Haitian Creole"', add
label define languaged_lbl 1150 `"Cajun"', add
label define languaged_lbl 1200 `"Spanish"', add
label define languaged_lbl 1210 `"Catalonian, Valencian"', add
label define languaged_lbl 1220 `"Ladino, Sefaradit, Spanol"', add
label define languaged_lbl 1230 `"Pachuco"', add
label define languaged_lbl 1250 `"Mexican"', add
label define languaged_lbl 1300 `"Portuguese"', add
label define languaged_lbl 1310 `"Papia Mentae"', add
label define languaged_lbl 1320 `"Cape Verdean Creole"', add
label define languaged_lbl 1400 `"Rumanian"', add
label define languaged_lbl 1500 `"Celtic"', add
label define languaged_lbl 1510 `"Welsh, Breton, Cornish"', add
label define languaged_lbl 1520 `"Welsh"', add
label define languaged_lbl 1530 `"Breton"', add
label define languaged_lbl 1540 `"Irish Gaelic, Gaelic"', add
label define languaged_lbl 1550 `"Gaelic"', add
label define languaged_lbl 1560 `"Irish"', add
label define languaged_lbl 1570 `"Scottish Gaelic"', add
label define languaged_lbl 1580 `"Scotch"', add
label define languaged_lbl 1590 `"Manx, Manx Gaelic"', add
label define languaged_lbl 1600 `"Greek"', add
label define languaged_lbl 1700 `"Albanian"', add
label define languaged_lbl 1800 `"Russian"', add
label define languaged_lbl 1810 `"Russian, Great Russian"', add
label define languaged_lbl 1811 `"Great Russian"', add
label define languaged_lbl 1820 `"Bielo-, White Russian"', add
label define languaged_lbl 1900 `"Ukrainian, Ruthenian, Little Russian"', add
label define languaged_lbl 1910 `"Ruthenian"', add
label define languaged_lbl 1920 `"Little Russian"', add
label define languaged_lbl 1930 `"Ukrainian"', add
label define languaged_lbl 2000 `"Czech"', add
label define languaged_lbl 2010 `"Bohemian"', add
label define languaged_lbl 2020 `"Moravian"', add
label define languaged_lbl 2100 `"Polish"', add
label define languaged_lbl 2110 `"Kashubian, Slovincian"', add
label define languaged_lbl 2200 `"Slovak"', add
label define languaged_lbl 2300 `"Serbo-Croatian, Yugoslavian, Slavonian"', add
label define languaged_lbl 2310 `"Croatian"', add
label define languaged_lbl 2320 `"Serbian"', add
label define languaged_lbl 2321 `"Bosnian"', add
label define languaged_lbl 2330 `"Dalmatian, Montenegrin"', add
label define languaged_lbl 2331 `"Dalmatian"', add
label define languaged_lbl 2332 `"Montenegrin"', add
label define languaged_lbl 2400 `"Slovene"', add
label define languaged_lbl 2500 `"Lithuanian"', add
label define languaged_lbl 2510 `"Lettish, Latvian"', add
label define languaged_lbl 2600 `"Other Balto-Slavic"', add
label define languaged_lbl 2610 `"Bulgarian"', add
label define languaged_lbl 2620 `"Lusatian, Sorbian, Wendish"', add
label define languaged_lbl 2621 `"Wendish"', add
label define languaged_lbl 2630 `"Macedonian"', add
label define languaged_lbl 2700 `"Slavic unknown"', add
label define languaged_lbl 2800 `"Armenian"', add
label define languaged_lbl 2900 `"Persian, Iranian, Farsi"', add
label define languaged_lbl 2910 `"Persian"', add
label define languaged_lbl 2920 `"Dari"', add
label define languaged_lbl 3000 `"Other Persian dialects"', add
label define languaged_lbl 3010 `"Pashto, Afghan"', add
label define languaged_lbl 3020 `"Kurdish"', add
label define languaged_lbl 3030 `"Balochi"', add
label define languaged_lbl 3040 `"Tadzhik"', add
label define languaged_lbl 3050 `"Ossete"', add
label define languaged_lbl 3100 `"Hindi and related"', add
label define languaged_lbl 3101 `"Hindi, Hindustani, Indic, Jaipuri, Pali, Urdu"', add
label define languaged_lbl 3102 `"Hindi"', add
label define languaged_lbl 3103 `"Urdu"', add
label define languaged_lbl 3104 `"Other Indo-Iranian languages"', add
label define languaged_lbl 3110 `"Other Indo-Aryan"', add
label define languaged_lbl 3111 `"Sanskrit"', add
label define languaged_lbl 3112 `"Bengali"', add
label define languaged_lbl 3113 `"Panjabi"', add
label define languaged_lbl 3114 `"Marathi"', add
label define languaged_lbl 3115 `"Gujarathi"', add
label define languaged_lbl 3116 `"Bihari"', add
label define languaged_lbl 3117 `"Rajasthani"', add
label define languaged_lbl 3118 `"Oriya"', add
label define languaged_lbl 3119 `"Assamese"', add
label define languaged_lbl 3120 `"Kashmiri"', add
label define languaged_lbl 3121 `"Sindhi"', add
label define languaged_lbl 3122 `"Maldivian"', add
label define languaged_lbl 3123 `"Sinhalese"', add
label define languaged_lbl 3130 `"Kannada"', add
label define languaged_lbl 3140 `"India nec"', add
label define languaged_lbl 3150 `"Pakistan nec"', add
label define languaged_lbl 3190 `"Other Indo-European languages"', add
label define languaged_lbl 3200 `"Romany, Gypsy"', add
label define languaged_lbl 3210 `"Gypsy"', add
label define languaged_lbl 3300 `"Finnish"', add
label define languaged_lbl 3400 `"Magyar, Hungarian"', add
label define languaged_lbl 3401 `"Magyar"', add
label define languaged_lbl 3402 `"Hungarian"', add
label define languaged_lbl 3500 `"Uralic"', add
label define languaged_lbl 3510 `"Estonian, Ingrian, Livonian, Vepsian,  Votic"', add
label define languaged_lbl 3511 `"Estonian"', add
label define languaged_lbl 3520 `"Lapp, Inari, Kola, Lule, Pite, Ruija, Skolt, Ume"', add
label define languaged_lbl 3521 `"Lappish"', add
label define languaged_lbl 3530 `"Other Uralic"', add
label define languaged_lbl 3600 `"Turkish"', add
label define languaged_lbl 3700 `"Other Altaic"', add
label define languaged_lbl 3701 `"Chuvash"', add
label define languaged_lbl 3702 `"Karakalpak"', add
label define languaged_lbl 3703 `"Kazakh"', add
label define languaged_lbl 3704 `"Kirghiz"', add
label define languaged_lbl 3705 `"Karachay, Tatar, Balkar, Bashkir, Kumyk"', add
label define languaged_lbl 3706 `"Uzbek, Uighur"', add
label define languaged_lbl 3707 `"Azerbaijani"', add
label define languaged_lbl 3708 `"Turkmen"', add
label define languaged_lbl 3709 `"Yakut"', add
label define languaged_lbl 3710 `"Mongolian"', add
label define languaged_lbl 3711 `"Tungus"', add
label define languaged_lbl 3800 `"Caucasian, Georgian, Avar"', add
label define languaged_lbl 3810 `"Georgian"', add
label define languaged_lbl 3900 `"Basque"', add
label define languaged_lbl 4000 `"Dravidian"', add
label define languaged_lbl 4001 `"Brahui"', add
label define languaged_lbl 4002 `"Gondi"', add
label define languaged_lbl 4003 `"Telugu"', add
label define languaged_lbl 4004 `"Malayalam"', add
label define languaged_lbl 4005 `"Tamil"', add
label define languaged_lbl 4010 `"Bhili"', add
label define languaged_lbl 4011 `"Nepali"', add
label define languaged_lbl 4100 `"Kurukh"', add
label define languaged_lbl 4110 `"Munda"', add
label define languaged_lbl 4200 `"Burushaski"', add
label define languaged_lbl 4300 `"Chinese"', add
label define languaged_lbl 4301 `"Chinese, Cantonese, Min, Yueh"', add
label define languaged_lbl 4302 `"Cantonese"', add
label define languaged_lbl 4303 `"Mandarin"', add
label define languaged_lbl 4310 `"Other Chinese"', add
label define languaged_lbl 4311 `"Hakka, Fukien, Kechia"', add
label define languaged_lbl 4312 `"Kan, Nan Chang"', add
label define languaged_lbl 4313 `"Hsiang, Chansa, Hunan, Iyan"', add
label define languaged_lbl 4314 `"Fuchow, Min Pei"', add
label define languaged_lbl 4315 `"Wu"', add
label define languaged_lbl 4400 `"Tibetan"', add
label define languaged_lbl 4410 `"Miao-Yao, Mien"', add
label define languaged_lbl 4420 `"Miao, Hmong"', add
label define languaged_lbl 4430 `"Iu Mien"', add
label define languaged_lbl 4500 `"Burmese, Lisu, Lolo"', add
label define languaged_lbl 4510 `"Karen"', add
label define languaged_lbl 4520 `"Chin languages"', add
label define languaged_lbl 4600 `"Kachin"', add
label define languaged_lbl 4700 `"Thai, Siamese, Lao"', add
label define languaged_lbl 4710 `"Thai"', add
label define languaged_lbl 4720 `"Laotian"', add
label define languaged_lbl 4800 `"Japanese"', add
label define languaged_lbl 4900 `"Korean"', add
label define languaged_lbl 5000 `"Vietnamese"', add
label define languaged_lbl 5100 `"Other East/Southeast Asian"', add
label define languaged_lbl 5110 `"Ainu"', add
label define languaged_lbl 5120 `"Mon-Khmer, Cambodian"', add
label define languaged_lbl 5130 `"Siberian, n.e.c."', add
label define languaged_lbl 5140 `"Yukagir"', add
label define languaged_lbl 5150 `"Muong"', add
label define languaged_lbl 5200 `"Indonesian"', add
label define languaged_lbl 5210 `"Buginese"', add
label define languaged_lbl 5220 `"Moluccan"', add
label define languaged_lbl 5230 `"Achinese"', add
label define languaged_lbl 5240 `"Balinese"', add
label define languaged_lbl 5250 `"Cham"', add
label define languaged_lbl 5260 `"Madurese"', add
label define languaged_lbl 5270 `"Malay"', add
label define languaged_lbl 5280 `"Minangkabau"', add
label define languaged_lbl 5290 `"Other Asian languages"', add
label define languaged_lbl 5300 `"Other Malayan"', add
label define languaged_lbl 5310 `"Formosan, Taiwanese"', add
label define languaged_lbl 5320 `"Javanese"', add
label define languaged_lbl 5330 `"Malagasy"', add
label define languaged_lbl 5340 `"Sundanese"', add
label define languaged_lbl 5400 `"Filipino, Tagalog"', add
label define languaged_lbl 5410 `"Bisayan"', add
label define languaged_lbl 5420 `"Sebuano"', add
label define languaged_lbl 5430 `"Pangasinan"', add
label define languaged_lbl 5440 `"Llocano, Hocano"', add
label define languaged_lbl 5450 `"Bikol"', add
label define languaged_lbl 5460 `"Pampangan"', add
label define languaged_lbl 5470 `"Gorontalo"', add
label define languaged_lbl 5480 `"Palau"', add
label define languaged_lbl 5500 `"Micronesian, Polynesian"', add
label define languaged_lbl 5501 `"Micronesian"', add
label define languaged_lbl 5502 `"Carolinian"', add
label define languaged_lbl 5503 `"Chamorro, Guamanian"', add
label define languaged_lbl 5504 `"Gilbertese"', add
label define languaged_lbl 5505 `"Kusaiean"', add
label define languaged_lbl 5506 `"Marshallese"', add
label define languaged_lbl 5507 `"Mokilese"', add
label define languaged_lbl 5508 `"Mortlockese"', add
label define languaged_lbl 5509 `"Nauruan"', add
label define languaged_lbl 5510 `"Ponapean"', add
label define languaged_lbl 5511 `"Trukese"', add
label define languaged_lbl 5512 `"Ulithean, Fais"', add
label define languaged_lbl 5513 `"Woleai-Ulithi"', add
label define languaged_lbl 5514 `"Yapese"', add
label define languaged_lbl 5520 `"Melanesian"', add
label define languaged_lbl 5521 `"Polynesian"', add
label define languaged_lbl 5522 `"Samoan"', add
label define languaged_lbl 5523 `"Tongan"', add
label define languaged_lbl 5524 `"Niuean"', add
label define languaged_lbl 5525 `"Tokelauan"', add
label define languaged_lbl 5526 `"Fijian"', add
label define languaged_lbl 5527 `"Marquesan"', add
label define languaged_lbl 5528 `"Rarotongan"', add
label define languaged_lbl 5529 `"Maori"', add
label define languaged_lbl 5530 `"Nukuoro, Kapingarangan"', add
label define languaged_lbl 5590 `"Other Pacific Island languages"', add
label define languaged_lbl 5600 `"Hawaiian"', add
label define languaged_lbl 5700 `"Arabic"', add
label define languaged_lbl 5710 `"Algerian, Moroccan, Tunisian"', add
label define languaged_lbl 5720 `"Egyptian"', add
label define languaged_lbl 5730 `"Iraqi"', add
label define languaged_lbl 5740 `"Libyan"', add
label define languaged_lbl 5750 `"Maltese"', add
label define languaged_lbl 5760 `"Levantine Arabic"', add
label define languaged_lbl 5800 `"Near East Arabic dialect"', add
label define languaged_lbl 5810 `"Syriac, Aramaic, Chaldean"', add
label define languaged_lbl 5820 `"Syrian"', add
label define languaged_lbl 5900 `"Hebrew, Israeli"', add
label define languaged_lbl 6000 `"Amharic, Ethiopian, etc."', add
label define languaged_lbl 6100 `"Hamitic"', add
label define languaged_lbl 6110 `"Berber"', add
label define languaged_lbl 6120 `"Chadic, Hamitic, Hausa"', add
label define languaged_lbl 6130 `"Cushite, Beja, Somali"', add
label define languaged_lbl 6200 `"Other Afro-Asiatic languages"', add
label define languaged_lbl 6300 `"Nilotic"', add
label define languaged_lbl 6301 `"Nilo-Hamitic"', add
label define languaged_lbl 6302 `"Nubian"', add
label define languaged_lbl 6303 `"Saharan"', add
label define languaged_lbl 6304 `"Nilo-Saharan, Fur, Songhai"', add
label define languaged_lbl 6305 `"Khoisan"', add
label define languaged_lbl 6306 `"Sudanic"', add
label define languaged_lbl 6307 `"Bantu (many subheads)"', add
label define languaged_lbl 6308 `"Swahili"', add
label define languaged_lbl 6309 `"Mande"', add
label define languaged_lbl 6310 `"Fulani"', add
label define languaged_lbl 6311 `"Gur"', add
label define languaged_lbl 6312 `"Kru"', add
label define languaged_lbl 6313 `"Efik, Ibibio, Tiv"', add
label define languaged_lbl 6314 `"Mbum, Gbaya, Sango, Zande"', add
label define languaged_lbl 6315 `"Kinyarwanda"', add
label define languaged_lbl 6320 `"Eastern Sudanic and Khoisan"', add
label define languaged_lbl 6321 `"Niger-Congo regions (many subheads)"', add
label define languaged_lbl 6322 `"Congo, Kongo, Luba, Ruanda, Rundi, Santali, Swahili"', add
label define languaged_lbl 6390 `"Other specified African languages"', add
label define languaged_lbl 6400 `"African, n.s."', add
label define languaged_lbl 7000 `"American Indian (all)"', add
label define languaged_lbl 7100 `"Aleut, Eskimo"', add
label define languaged_lbl 7110 `"Aleut"', add
label define languaged_lbl 7120 `"Pacific Gulf Yupik"', add
label define languaged_lbl 7130 `"Eskimo"', add
label define languaged_lbl 7140 `"Inupik, Innuit"', add
label define languaged_lbl 7150 `"St. Lawrence Isl. Yupik"', add
label define languaged_lbl 7160 `"Yupik"', add
label define languaged_lbl 7200 `"Algonquian"', add
label define languaged_lbl 7201 `"Arapaho"', add
label define languaged_lbl 7202 `"Atsina, Gros Ventre"', add
label define languaged_lbl 7203 `"Blackfoot"', add
label define languaged_lbl 7204 `"Cheyenne"', add
label define languaged_lbl 7205 `"Cree"', add
label define languaged_lbl 7206 `"Delaware, Lenni-Lenape"', add
label define languaged_lbl 7207 `"Fox, Sac"', add
label define languaged_lbl 7208 `"Kickapoo"', add
label define languaged_lbl 7209 `"Menomini"', add
label define languaged_lbl 7210 `"Metis, French Cree"', add
label define languaged_lbl 7211 `"Miami"', add
label define languaged_lbl 7212 `"Micmac"', add
label define languaged_lbl 7213 `"Ojibwa, Chippewa"', add
label define languaged_lbl 7214 `"Ottawa"', add
label define languaged_lbl 7215 `"Passamaquoddy, Malecite"', add
label define languaged_lbl 7216 `"Penobscot"', add
label define languaged_lbl 7217 `"Abnaki"', add
label define languaged_lbl 7218 `"Potawatomi"', add
label define languaged_lbl 7219 `"Shawnee"', add
label define languaged_lbl 7300 `"Salish, Flathead"', add
label define languaged_lbl 7301 `"Lower Chehalis"', add
label define languaged_lbl 7302 `"Upper Chehalis, Chelalis, Satsop"', add
label define languaged_lbl 7303 `"Clallam"', add
label define languaged_lbl 7304 `"Coeur dAlene, Skitsamish"', add
label define languaged_lbl 7305 `"Columbia, Chelan, Wenatchee"', add
label define languaged_lbl 7306 `"Cowlitz"', add
label define languaged_lbl 7307 `"Nootsack"', add
label define languaged_lbl 7308 `"Okanogan"', add
label define languaged_lbl 7309 `"Puget Sound Salish"', add
label define languaged_lbl 7310 `"Quinault, Queets"', add
label define languaged_lbl 7311 `"Tillamook"', add
label define languaged_lbl 7312 `"Twana"', add
label define languaged_lbl 7313 `"Kalispel"', add
label define languaged_lbl 7314 `"Spokane"', add
label define languaged_lbl 7400 `"Athapascan"', add
label define languaged_lbl 7401 `"Ahtena"', add
label define languaged_lbl 7402 `"Han"', add
label define languaged_lbl 7403 `"Ingalit"', add
label define languaged_lbl 7404 `"Koyukon"', add
label define languaged_lbl 7405 `"Kuchin"', add
label define languaged_lbl 7406 `"Upper Kuskokwim"', add
label define languaged_lbl 7407 `"Tanaina"', add
label define languaged_lbl 7408 `"Tanana, Minto"', add
label define languaged_lbl 7409 `"Tanacross"', add
label define languaged_lbl 7410 `"Upper Tanana, Nabesena, Tetlin"', add
label define languaged_lbl 7411 `"Tutchone"', add
label define languaged_lbl 7412 `"Chasta Costa, Chetco, Coquille, Smith River Athapascan"', add
label define languaged_lbl 7413 `"Hupa"', add
label define languaged_lbl 7420 `"Apache"', add
label define languaged_lbl 7421 `"Jicarilla, Lipan"', add
label define languaged_lbl 7422 `"Chiricahua, Mescalero"', add
label define languaged_lbl 7423 `"San Carlos, Cibecue, White Mountain"', add
label define languaged_lbl 7424 `"Kiowa-Apache"', add
label define languaged_lbl 7430 `"Kiowa"', add
label define languaged_lbl 7440 `"Eyak"', add
label define languaged_lbl 7450 `"Other Athapascan-Eyak, Cahto, Mattole, Wailaki"', add
label define languaged_lbl 7490 `"Other Algonquin languages"', add
label define languaged_lbl 7500 `"Navajo"', add
label define languaged_lbl 7600 `"Penutian-Sahaptin"', add
label define languaged_lbl 7610 `"Klamath, Modoc"', add
label define languaged_lbl 7620 `"Nez Perce"', add
label define languaged_lbl 7630 `"Sahaptian, Celilo, Klikitat, Palouse, Tenino, Umatilla, Warm"', add
label define languaged_lbl 7700 `"Mountain Maidu, Maidu"', add
label define languaged_lbl 7701 `"Northwest Maidu, Concow"', add
label define languaged_lbl 7702 `"Southern Maidu, Nisenan"', add
label define languaged_lbl 7703 `"Coast Miwok, Bodega, Marin"', add
label define languaged_lbl 7704 `"Plains Miwok"', add
label define languaged_lbl 7705 `"Sierra Miwok, Miwok"', add
label define languaged_lbl 7706 `"Nomlaki, Tehama"', add
label define languaged_lbl 7707 `"Patwin, Colouse, Suisun"', add
label define languaged_lbl 7708 `"Wintun"', add
label define languaged_lbl 7709 `"Foothill North Yokuts"', add
label define languaged_lbl 7710 `"Tachi"', add
label define languaged_lbl 7711 `"Santiam, Calapooya, Wapatu"', add
label define languaged_lbl 7712 `"Siuslaw, Coos, Lower Umpqua"', add
label define languaged_lbl 7713 `"Tsimshian"', add
label define languaged_lbl 7714 `"Upper Chinook, Clackamas, Multnomah, Wasco, Wishram"', add
label define languaged_lbl 7715 `"Chinook Jargon"', add
label define languaged_lbl 7800 `"Zuni"', add
label define languaged_lbl 7900 `"Yuman"', add
label define languaged_lbl 7910 `"Upriver Yuman"', add
label define languaged_lbl 7920 `"Cocomaricopa"', add
label define languaged_lbl 7930 `"Mohave"', add
label define languaged_lbl 7940 `"Diegueno"', add
label define languaged_lbl 7950 `"Delta River Yuman"', add
label define languaged_lbl 7960 `"Upland Yuman"', add
label define languaged_lbl 7970 `"Havasupai"', add
label define languaged_lbl 7980 `"Walapai"', add
label define languaged_lbl 7990 `"Yavapai"', add
label define languaged_lbl 8000 `"Achumawi"', add
label define languaged_lbl 8010 `"Atsugewi"', add
label define languaged_lbl 8020 `"Karok"', add
label define languaged_lbl 8030 `"Pomo"', add
label define languaged_lbl 8040 `"Shastan"', add
label define languaged_lbl 8050 `"Washo"', add
label define languaged_lbl 8060 `"Chumash"', add
label define languaged_lbl 8100 `"Siouan languages"', add
label define languaged_lbl 8101 `"Crow, Absaroke"', add
label define languaged_lbl 8102 `"Hidatsa"', add
label define languaged_lbl 8103 `"Mandan"', add
label define languaged_lbl 8104 `"Dakota, Lakota, Nakota, Sioux"', add
label define languaged_lbl 8105 `"Chiwere"', add
label define languaged_lbl 8106 `"Winnebago"', add
label define languaged_lbl 8107 `"Kansa, Kaw"', add
label define languaged_lbl 8108 `"Omaha"', add
label define languaged_lbl 8109 `"Osage"', add
label define languaged_lbl 8110 `"Ponca"', add
label define languaged_lbl 8111 `"Quapaw, Arkansas"', add
label define languaged_lbl 8120 `"Iowa"', add
label define languaged_lbl 8200 `"Muskogean"', add
label define languaged_lbl 8210 `"Alabama"', add
label define languaged_lbl 8220 `"Choctaw, Chickasaw"', add
label define languaged_lbl 8230 `"Mikasuki"', add
label define languaged_lbl 8240 `"Hichita, Apalachicola"', add
label define languaged_lbl 8250 `"Koasati"', add
label define languaged_lbl 8260 `"Muskogee, Creek, Seminole"', add
label define languaged_lbl 8300 `"Keres"', add
label define languaged_lbl 8400 `"Iroquoian"', add
label define languaged_lbl 8410 `"Mohawk"', add
label define languaged_lbl 8420 `"Oneida"', add
label define languaged_lbl 8430 `"Onondaga"', add
label define languaged_lbl 8440 `"Cayuga"', add
label define languaged_lbl 8450 `"Seneca"', add
label define languaged_lbl 8460 `"Tuscarora"', add
label define languaged_lbl 8470 `"Wyandot, Huron"', add
label define languaged_lbl 8480 `"Cherokee"', add
label define languaged_lbl 8500 `"Caddoan"', add
label define languaged_lbl 8510 `"Arikara"', add
label define languaged_lbl 8520 `"Pawnee"', add
label define languaged_lbl 8530 `"Wichita"', add
label define languaged_lbl 8600 `"Shoshonean/Hopi"', add
label define languaged_lbl 8601 `"Comanche"', add
label define languaged_lbl 8602 `"Mono, Owens Valley Paiute"', add
label define languaged_lbl 8603 `"Paiute"', add
label define languaged_lbl 8604 `"Northern Paiute, Bannock, Num, Snake"', add
label define languaged_lbl 8605 `"Southern Paiute"', add
label define languaged_lbl 8606 `"Chemehuevi"', add
label define languaged_lbl 8607 `"Kawaiisu"', add
label define languaged_lbl 8608 `"Ute"', add
label define languaged_lbl 8609 `"Shoshoni"', add
label define languaged_lbl 8610 `"Panamint"', add
label define languaged_lbl 8620 `"Hopi"', add
label define languaged_lbl 8630 `"Cahuilla"', add
label define languaged_lbl 8631 `"Cupeno"', add
label define languaged_lbl 8632 `"Luiseno"', add
label define languaged_lbl 8633 `"Serrano"', add
label define languaged_lbl 8640 `"Tubatulabal"', add
label define languaged_lbl 8700 `"Pima, Papago"', add
label define languaged_lbl 8800 `"Yaqui"', add
label define languaged_lbl 8810 `"Sonoran n.e.c., Cahita, Guasave, Huichole, Nayit, Tarahumar"', add
label define languaged_lbl 8820 `"Tarahumara"', add
label define languaged_lbl 8900 `"Aztecan, Nahuatl, Uto-Aztecan"', add
label define languaged_lbl 8910 `"Aztecan, Mexicano, Nahua"', add
label define languaged_lbl 9000 `"Tanoan languages"', add
label define languaged_lbl 9010 `"Picuris, Northern Tiwa, Taos"', add
label define languaged_lbl 9020 `"Tiwa, Isleta"', add
label define languaged_lbl 9030 `"Sandia"', add
label define languaged_lbl 9040 `"Tewa, Hano, Hopi-Tewa, San Ildefonso, San Juan, Santa Clara"', add
label define languaged_lbl 9050 `"Towa"', add
label define languaged_lbl 9100 `"Wiyot"', add
label define languaged_lbl 9101 `"Yurok"', add
label define languaged_lbl 9110 `"Kwakiutl"', add
label define languaged_lbl 9111 `"Nootka"', add
label define languaged_lbl 9112 `"Makah"', add
label define languaged_lbl 9120 `"Kutenai"', add
label define languaged_lbl 9130 `"Haida"', add
label define languaged_lbl 9131 `"Tlingit, Chilkat, Sitka, Tongass, Yakutat"', add
label define languaged_lbl 9140 `"Tonkawa"', add
label define languaged_lbl 9150 `"Yuchi"', add
label define languaged_lbl 9160 `"Chetemacha"', add
label define languaged_lbl 9170 `"Yuki"', add
label define languaged_lbl 9171 `"Wappo"', add
label define languaged_lbl 9200 `"Mayan languages"', add
label define languaged_lbl 9210 `"Misumalpan"', add
label define languaged_lbl 9211 `"Cakchiquel"', add
label define languaged_lbl 9212 `"Mam"', add
label define languaged_lbl 9213 `"Maya"', add
label define languaged_lbl 9214 `"Quekchi"', add
label define languaged_lbl 9215 `"Quiche"', add
label define languaged_lbl 9220 `"Tarascan"', add
label define languaged_lbl 9230 `"Mapuche"', add
label define languaged_lbl 9231 `"Araucanian"', add
label define languaged_lbl 9240 `"Oto-Manguen"', add
label define languaged_lbl 9241 `"Mixtec"', add
label define languaged_lbl 9242 `"Zapotec"', add
label define languaged_lbl 9250 `"Quechua"', add
label define languaged_lbl 9260 `"Aymara"', add
label define languaged_lbl 9270 `"Arawakian"', add
label define languaged_lbl 9271 `"Island Caribs"', add
label define languaged_lbl 9280 `"Chibchan"', add
label define languaged_lbl 9281 `"Cuna"', add
label define languaged_lbl 9282 `"Guaymi"', add
label define languaged_lbl 9290 `"Tupi-Guarani"', add
label define languaged_lbl 9291 `"Tupi"', add
label define languaged_lbl 9292 `"Guarani"', add
label define languaged_lbl 9300 `"American Indian, n.s."', add
label define languaged_lbl 9400 `"Native"', add
label define languaged_lbl 9410 `"Other specified American Indian languages"', add
label define languaged_lbl 9420 `"South/Central American Indian"', add
label define languaged_lbl 9500 `"No language"', add
label define languaged_lbl 9600 `"Other or not reported"', add
label define languaged_lbl 9601 `"Other n.e.c."', add
label define languaged_lbl 9602 `"Other n.s."', add
label define languaged_lbl 9700 `"Unknown"', add
label define languaged_lbl 9800 `"Illegible"', add
label define languaged_lbl 9900 `"Not reported, blank"', add
label values languaged languaged_lbl

label define speakeng_lbl 0 `"N/A (Blank)"'
label define speakeng_lbl 1 `"Does not speak English"', add
label define speakeng_lbl 2 `"Yes, speaks English..."', add
label define speakeng_lbl 3 `"Yes, speaks only English"', add
label define speakeng_lbl 4 `"Yes, speaks very well"', add
label define speakeng_lbl 5 `"Yes, speaks well"', add
label define speakeng_lbl 6 `"Yes, but not well"', add
label define speakeng_lbl 7 `"Unknown"', add
label define speakeng_lbl 8 `"Illegible"', add
label define speakeng_lbl 9 `"Blank"', add
label values speakeng speakeng_lbl

label define rachsing_lbl 1 `"White"'
label define rachsing_lbl 2 `"Black/African American"', add
label define rachsing_lbl 3 `"American Indian/Alaska Native"', add
label define rachsing_lbl 4 `"Asian/Pacific Islander"', add
label define rachsing_lbl 5 `"Hispanic/Latino"', add
label values rachsing rachsing_lbl

label define predhisp_lbl 0 `"Not Hispanic or Latino"'
label define predhisp_lbl 1 `"Hispanic or Latino"', add
label values predhisp predhisp_lbl

label define racamind_lbl 1 `"No"'
label define racamind_lbl 2 `"Yes"', add
label values racamind racamind_lbl

label define racasian_lbl 1 `"No"'
label define racasian_lbl 2 `"Yes"', add
label values racasian racasian_lbl

label define racblk_lbl 1 `"No"'
label define racblk_lbl 2 `"Yes"', add
label values racblk racblk_lbl

label define racpacis_lbl 1 `"No"'
label define racpacis_lbl 2 `"Yes"', add
label values racpacis racpacis_lbl

label define racwht_lbl 1 `"No"'
label define racwht_lbl 2 `"Yes"', add
label values racwht racwht_lbl

label define racother_lbl 1 `"No"'
label define racother_lbl 2 `"Yes"', add
label values racother racother_lbl

label define hcovany_lbl 1 `"No health insurance coverage"'
label define hcovany_lbl 2 `"With health insurance coverage"', add
label values hcovany hcovany_lbl

label define hcovpriv_lbl 1 `"Without private health insurance coverage"'
label define hcovpriv_lbl 2 `"With private health insurance coverage"', add
label values hcovpriv hcovpriv_lbl

label define hinsemp_lbl 1 `"No insurance through employer/union"'
label define hinsemp_lbl 2 `"Has insurance through employer/union"', add
label values hinsemp hinsemp_lbl

label define hinspur_lbl 1 `"No insurance purchased directly"'
label define hinspur_lbl 2 `"Has insurance purchased directly"', add
label values hinspur hinspur_lbl

label define hinstri_lbl 1 `"No insurance through TRICARE"'
label define hinstri_lbl 2 `"Has insurance through TRICARE"', add
label values hinstri hinstri_lbl

label define hcovpub_lbl 1 `"Without public health insurance coverage"'
label define hcovpub_lbl 2 `"With public health insurance coverage"', add
label values hcovpub hcovpub_lbl

label define hinscaid_lbl 1 `"No insurance through Medicaid"'
label define hinscaid_lbl 2 `"Has insurance through Medicaid"', add
label values hinscaid hinscaid_lbl

label define hinscare_lbl 1 `"No"'
label define hinscare_lbl 2 `"Yes"', add
label values hinscare hinscare_lbl

label define hinsva_lbl 1 `"No insurance through VA"'
label define hinsva_lbl 2 `"Has insurance through VA"', add
label values hinsva hinsva_lbl

label define hinsihs_lbl 1 `"No insurance through Indian Health Service"'
label define hinsihs_lbl 2 `"Has insurance through Indian Health Service"', add
label values hinsihs hinsihs_lbl

label define school_lbl 0 `"N/A"'
label define school_lbl 1 `"No, not in school"', add
label define school_lbl 2 `"Yes, in school"', add
label define school_lbl 8 `"Unknown"', add
label define school_lbl 9 `"Missing"', add
label values school school_lbl

label define educ_lbl 00 `"N/A or no schooling"'
label define educ_lbl 01 `"Nursery school to grade 4"', add
label define educ_lbl 02 `"Grade 5, 6, 7, or 8"', add
label define educ_lbl 03 `"Grade 9"', add
label define educ_lbl 04 `"Grade 10"', add
label define educ_lbl 05 `"Grade 11"', add
label define educ_lbl 06 `"Grade 12"', add
label define educ_lbl 07 `"1 year of college"', add
label define educ_lbl 08 `"2 years of college"', add
label define educ_lbl 09 `"3 years of college"', add
label define educ_lbl 10 `"4 years of college"', add
label define educ_lbl 11 `"5+ years of college"', add
label define educ_lbl 99 `"Missing"', add
label values educ educ_lbl

label define educd_lbl 000 `"N/A or no schooling"'
label define educd_lbl 001 `"N/A"', add
label define educd_lbl 002 `"No schooling completed"', add
label define educd_lbl 010 `"Nursery school to grade 4"', add
label define educd_lbl 011 `"Nursery school, preschool"', add
label define educd_lbl 012 `"Kindergarten"', add
label define educd_lbl 013 `"Grade 1, 2, 3, or 4"', add
label define educd_lbl 014 `"Grade 1"', add
label define educd_lbl 015 `"Grade 2"', add
label define educd_lbl 016 `"Grade 3"', add
label define educd_lbl 017 `"Grade 4"', add
label define educd_lbl 020 `"Grade 5, 6, 7, or 8"', add
label define educd_lbl 021 `"Grade 5 or 6"', add
label define educd_lbl 022 `"Grade 5"', add
label define educd_lbl 023 `"Grade 6"', add
label define educd_lbl 024 `"Grade 7 or 8"', add
label define educd_lbl 025 `"Grade 7"', add
label define educd_lbl 026 `"Grade 8"', add
label define educd_lbl 030 `"Grade 9"', add
label define educd_lbl 040 `"Grade 10"', add
label define educd_lbl 050 `"Grade 11"', add
label define educd_lbl 060 `"Grade 12"', add
label define educd_lbl 061 `"12th grade, no diploma"', add
label define educd_lbl 062 `"High school graduate or GED"', add
label define educd_lbl 063 `"Regular high school diploma"', add
label define educd_lbl 064 `"GED or alternative credential"', add
label define educd_lbl 065 `"Some college, but less than 1 year"', add
label define educd_lbl 070 `"1 year of college"', add
label define educd_lbl 071 `"1 or more years of college credit, no degree"', add
label define educd_lbl 080 `"2 years of college"', add
label define educd_lbl 081 `"Associate's degree, type not specified"', add
label define educd_lbl 082 `"Associate's degree, occupational program"', add
label define educd_lbl 083 `"Associate's degree, academic program"', add
label define educd_lbl 090 `"3 years of college"', add
label define educd_lbl 100 `"4 years of college"', add
label define educd_lbl 101 `"Bachelor's degree"', add
label define educd_lbl 110 `"5+ years of college"', add
label define educd_lbl 111 `"6 years of college (6+ in 1960-1970)"', add
label define educd_lbl 112 `"7 years of college"', add
label define educd_lbl 113 `"8+ years of college"', add
label define educd_lbl 114 `"Master's degree"', add
label define educd_lbl 115 `"Professional degree beyond a bachelor's degree"', add
label define educd_lbl 116 `"Doctoral degree"', add
label define educd_lbl 999 `"Missing"', add
label values educd educd_lbl

label define gradeatt_lbl 0 `"N/A"'
label define gradeatt_lbl 1 `"Nursery school/preschool"', add
label define gradeatt_lbl 2 `"Kindergarten"', add
label define gradeatt_lbl 3 `"Grade 1 to grade 4"', add
label define gradeatt_lbl 4 `"Grade 5 to grade 8"', add
label define gradeatt_lbl 5 `"Grade 9 to grade 12"', add
label define gradeatt_lbl 6 `"College undergraduate"', add
label define gradeatt_lbl 7 `"Graduate or professional school"', add
label values gradeatt gradeatt_lbl

label define gradeattd_lbl 00 `"N/A"'
label define gradeattd_lbl 10 `"Nursery school/preschool"', add
label define gradeattd_lbl 20 `"Kindergarten"', add
label define gradeattd_lbl 30 `"Grade 1 to grade 4"', add
label define gradeattd_lbl 31 `"Grade 1"', add
label define gradeattd_lbl 32 `"Grade 2"', add
label define gradeattd_lbl 33 `"Grade 3"', add
label define gradeattd_lbl 34 `"Grade 4"', add
label define gradeattd_lbl 40 `"Grade 5 to grade 8"', add
label define gradeattd_lbl 41 `"Grade 5"', add
label define gradeattd_lbl 42 `"Grade 6"', add
label define gradeattd_lbl 43 `"Grade 7"', add
label define gradeattd_lbl 44 `"Grade 8"', add
label define gradeattd_lbl 50 `"Grade 9 to grade 12"', add
label define gradeattd_lbl 51 `"Grade 9"', add
label define gradeattd_lbl 52 `"Grade 10"', add
label define gradeattd_lbl 53 `"Grade 11"', add
label define gradeattd_lbl 54 `"Grade 12"', add
label define gradeattd_lbl 60 `"College undergraduate"', add
label define gradeattd_lbl 61 `"First year of college"', add
label define gradeattd_lbl 62 `"Second year of college"', add
label define gradeattd_lbl 63 `"Third year of college"', add
label define gradeattd_lbl 64 `"Fourth year of college"', add
label define gradeattd_lbl 70 `"Graduate or professional school"', add
label define gradeattd_lbl 71 `"Fifth year of college"', add
label define gradeattd_lbl 72 `"Sixth year of college"', add
label define gradeattd_lbl 73 `"Seventh year of college"', add
label define gradeattd_lbl 74 `"Eighth year of college"', add
label values gradeattd gradeattd_lbl

label define schltype_lbl 0 `"N/A"'
label define schltype_lbl 1 `"Not enrolled"', add
label define schltype_lbl 2 `"Public school"', add
label define schltype_lbl 3 `"Private school (1960,1990-2000,ACS,PRCS)"', add
label define schltype_lbl 4 `"Church-related (1980)"', add
label define schltype_lbl 5 `"Parochial (1970)"', add
label define schltype_lbl 6 `"Other private, 1980"', add
label define schltype_lbl 7 `"Other private, 1970"', add
label values schltype schltype_lbl

label define degfield_lbl 00 `"N/A"'
label define degfield_lbl 11 `"Agriculture"', add
label define degfield_lbl 13 `"Environment and Natural Resources"', add
label define degfield_lbl 14 `"Architecture"', add
label define degfield_lbl 15 `"Area, Ethnic, and Civilization Studies"', add
label define degfield_lbl 19 `"Communications"', add
label define degfield_lbl 20 `"Communication Technologies"', add
label define degfield_lbl 21 `"Computer and Information Sciences"', add
label define degfield_lbl 22 `"Cosmetology Services and Culinary Arts"', add
label define degfield_lbl 23 `"Education Administration and Teaching"', add
label define degfield_lbl 24 `"Engineering"', add
label define degfield_lbl 25 `"Engineering Technologies"', add
label define degfield_lbl 26 `"Linguistics and Foreign Languages"', add
label define degfield_lbl 29 `"Family and Consumer Sciences"', add
label define degfield_lbl 32 `"Law"', add
label define degfield_lbl 33 `"English Language, Literature, and Composition"', add
label define degfield_lbl 34 `"Liberal Arts and Humanities"', add
label define degfield_lbl 35 `"Library Science"', add
label define degfield_lbl 36 `"Biology and Life Sciences"', add
label define degfield_lbl 37 `"Mathematics and Statistics"', add
label define degfield_lbl 38 `"Military Technologies"', add
label define degfield_lbl 40 `"Interdisciplinary and Multi-Disciplinary Studies (General)"', add
label define degfield_lbl 41 `"Physical Fitness, Parks, Recreation, and Leisure"', add
label define degfield_lbl 48 `"Philosophy and Religious Studies"', add
label define degfield_lbl 49 `"Theology and Religious Vocations"', add
label define degfield_lbl 50 `"Physical Sciences"', add
label define degfield_lbl 51 `"Nuclear, Industrial Radiology, and Biological Technologies"', add
label define degfield_lbl 52 `"Psychology"', add
label define degfield_lbl 53 `"Criminal Justice and Fire Protection"', add
label define degfield_lbl 54 `"Public Affairs, Policy, and Social Work"', add
label define degfield_lbl 55 `"Social Sciences"', add
label define degfield_lbl 56 `"Construction Services"', add
label define degfield_lbl 57 `"Electrical and Mechanic Repairs and Technologies"', add
label define degfield_lbl 58 `"Precision Production and Industrial Arts"', add
label define degfield_lbl 59 `"Transportation Sciences and Technologies"', add
label define degfield_lbl 60 `"Fine Arts"', add
label define degfield_lbl 61 `"Medical and Health Sciences and Services"', add
label define degfield_lbl 62 `"Business"', add
label define degfield_lbl 64 `"History"', add
label values degfield degfield_lbl

label define degfieldd_lbl 0000 `"N/A"'
label define degfieldd_lbl 1100 `"General Agriculture"', add
label define degfieldd_lbl 1101 `"Agriculture Production and Management"', add
label define degfieldd_lbl 1102 `"Agricultural Economics"', add
label define degfieldd_lbl 1103 `"Animal Sciences"', add
label define degfieldd_lbl 1104 `"Food Science"', add
label define degfieldd_lbl 1105 `"Plant Science and Agronomy"', add
label define degfieldd_lbl 1106 `"Soil Science"', add
label define degfieldd_lbl 1107 `"Veterinary Medicine"', add
label define degfieldd_lbl 1199 `"Miscellaneous Agriculture"', add
label define degfieldd_lbl 1300 `"Environment and Natural Resources"', add
label define degfieldd_lbl 1301 `"Environmental Science"', add
label define degfieldd_lbl 1302 `"Forestry"', add
label define degfieldd_lbl 1303 `"Natural Resources Management"', add
label define degfieldd_lbl 1401 `"Architecture"', add
label define degfieldd_lbl 1501 `"Area, Ethnic, and Civilization Studies"', add
label define degfieldd_lbl 1900 `"Communications"', add
label define degfieldd_lbl 1901 `"Communications"', add
label define degfieldd_lbl 1902 `"Journalism"', add
label define degfieldd_lbl 1903 `"Mass Media"', add
label define degfieldd_lbl 1904 `"Advertising and Public Relations"', add
label define degfieldd_lbl 2001 `"Communication Technologies"', add
label define degfieldd_lbl 2100 `"Computer and Information Systems"', add
label define degfieldd_lbl 2101 `"Computer Programming and Data Processing"', add
label define degfieldd_lbl 2102 `"Computer Science"', add
label define degfieldd_lbl 2105 `"Information Sciences"', add
label define degfieldd_lbl 2106 `"Computer Information Management and Security"', add
label define degfieldd_lbl 2107 `"Computer Networking and Telecommunications"', add
label define degfieldd_lbl 2201 `"Cosmetology Services and Culinary Arts"', add
label define degfieldd_lbl 2300 `"General Education"', add
label define degfieldd_lbl 2301 `"Educational Administration and Supervision"', add
label define degfieldd_lbl 2303 `"School Student Counseling"', add
label define degfieldd_lbl 2304 `"Elementary Education"', add
label define degfieldd_lbl 2305 `"Mathematics Teacher Education"', add
label define degfieldd_lbl 2306 `"Physical and Health Education Teaching"', add
label define degfieldd_lbl 2307 `"Early Childhood Education"', add
label define degfieldd_lbl 2308 `"Science  and Computer Teacher Education"', add
label define degfieldd_lbl 2309 `"Secondary Teacher Education"', add
label define degfieldd_lbl 2310 `"Special Needs Education"', add
label define degfieldd_lbl 2311 `"Social Science or History Teacher Education"', add
label define degfieldd_lbl 2312 `"Teacher Education:  Multiple Levels"', add
label define degfieldd_lbl 2313 `"Language and Drama Education"', add
label define degfieldd_lbl 2314 `"Art and Music Education"', add
label define degfieldd_lbl 2399 `"Miscellaneous Education"', add
label define degfieldd_lbl 2400 `"General Engineering"', add
label define degfieldd_lbl 2401 `"Aerospace Engineering"', add
label define degfieldd_lbl 2402 `"Biological Engineering"', add
label define degfieldd_lbl 2403 `"Architectural Engineering"', add
label define degfieldd_lbl 2404 `"Biomedical Engineering"', add
label define degfieldd_lbl 2405 `"Chemical Engineering"', add
label define degfieldd_lbl 2406 `"Civil Engineering"', add
label define degfieldd_lbl 2407 `"Computer Engineering"', add
label define degfieldd_lbl 2408 `"Electrical Engineering"', add
label define degfieldd_lbl 2409 `"Engineering Mechanics, Physics, and Science"', add
label define degfieldd_lbl 2410 `"Environmental Engineering"', add
label define degfieldd_lbl 2411 `"Geological and Geophysical Engineering"', add
label define degfieldd_lbl 2412 `"Industrial and Manufacturing Engineering"', add
label define degfieldd_lbl 2413 `"Materials Engineering and Materials Science"', add
label define degfieldd_lbl 2414 `"Mechanical Engineering"', add
label define degfieldd_lbl 2415 `"Metallurgical Engineering"', add
label define degfieldd_lbl 2416 `"Mining and Mineral Engineering"', add
label define degfieldd_lbl 2417 `"Naval Architecture and Marine Engineering"', add
label define degfieldd_lbl 2418 `"Nuclear Engineering"', add
label define degfieldd_lbl 2419 `"Petroleum Engineering"', add
label define degfieldd_lbl 2499 `"Miscellaneous Engineering"', add
label define degfieldd_lbl 2500 `"Engineering Technologies"', add
label define degfieldd_lbl 2501 `"Engineering and Industrial Management"', add
label define degfieldd_lbl 2502 `"Electrical Engineering Technology"', add
label define degfieldd_lbl 2503 `"Industrial Production Technologies"', add
label define degfieldd_lbl 2504 `"Mechanical Engineering Related Technologies"', add
label define degfieldd_lbl 2599 `"Miscellaneous Engineering Technologies"', add
label define degfieldd_lbl 2600 `"Linguistics and Foreign Languages"', add
label define degfieldd_lbl 2601 `"Linguistics and Comparative Language and Literature"', add
label define degfieldd_lbl 2602 `"French, German, Latin and Other Common Foreign Language Studies"', add
label define degfieldd_lbl 2603 `"Other Foreign Languages"', add
label define degfieldd_lbl 2901 `"Family and Consumer Sciences"', add
label define degfieldd_lbl 3200 `"Law"', add
label define degfieldd_lbl 3201 `"Court Reporting"', add
label define degfieldd_lbl 3202 `"Pre-Law and Legal Studies"', add
label define degfieldd_lbl 3300 `"English Language, Literature, and Composition"', add
label define degfieldd_lbl 3301 `"English Language and Literature"', add
label define degfieldd_lbl 3302 `"Composition and Speech"', add
label define degfieldd_lbl 3400 `"Liberal Arts and Humanities"', add
label define degfieldd_lbl 3401 `"Liberal Arts"', add
label define degfieldd_lbl 3402 `"Humanities"', add
label define degfieldd_lbl 3501 `"Library Science"', add
label define degfieldd_lbl 3600 `"Biology"', add
label define degfieldd_lbl 3601 `"Biochemical Sciences"', add
label define degfieldd_lbl 3602 `"Botany"', add
label define degfieldd_lbl 3603 `"Molecular Biology"', add
label define degfieldd_lbl 3604 `"Ecology"', add
label define degfieldd_lbl 3605 `"Genetics"', add
label define degfieldd_lbl 3606 `"Microbiology"', add
label define degfieldd_lbl 3607 `"Pharmacology"', add
label define degfieldd_lbl 3608 `"Physiology"', add
label define degfieldd_lbl 3609 `"Zoology"', add
label define degfieldd_lbl 3611 `"Neuroscience"', add
label define degfieldd_lbl 3699 `"Miscellaneous Biology"', add
label define degfieldd_lbl 3700 `"Mathematics"', add
label define degfieldd_lbl 3701 `"Applied Mathematics"', add
label define degfieldd_lbl 3702 `"Statistics and Decision Science"', add
label define degfieldd_lbl 3801 `"Military Technologies"', add
label define degfieldd_lbl 4000 `"Interdisciplinary and Multi-Disciplinary Studies (General)"', add
label define degfieldd_lbl 4001 `"Intercultural and International Studies"', add
label define degfieldd_lbl 4002 `"Nutrition Sciences"', add
label define degfieldd_lbl 4003 `"Neuroscience"', add
label define degfieldd_lbl 4005 `"Mathematics and Computer Science"', add
label define degfieldd_lbl 4006 `"Cognitive Science and Biopsychology"', add
label define degfieldd_lbl 4007 `"Interdisciplinary Social Sciences"', add
label define degfieldd_lbl 4008 `"Multi-disciplinary or General Science"', add
label define degfieldd_lbl 4009 `"Data Science and Data Analytics"', add
label define degfieldd_lbl 4101 `"Physical Fitness, Parks, Recreation, and Leisure"', add
label define degfieldd_lbl 4801 `"Philosophy and Religious Studies"', add
label define degfieldd_lbl 4901 `"Theology and Religious Vocations"', add
label define degfieldd_lbl 5000 `"Physical Sciences"', add
label define degfieldd_lbl 5001 `"Astronomy and Astrophysics"', add
label define degfieldd_lbl 5002 `"Atmospheric Sciences and Meteorology"', add
label define degfieldd_lbl 5003 `"Chemistry"', add
label define degfieldd_lbl 5004 `"Geology and Earth Science"', add
label define degfieldd_lbl 5005 `"Geosciences"', add
label define degfieldd_lbl 5006 `"Oceanography"', add
label define degfieldd_lbl 5007 `"Physics"', add
label define degfieldd_lbl 5008 `"Materials Science"', add
label define degfieldd_lbl 5098 `"Multi-disciplinary or General Science"', add
label define degfieldd_lbl 5102 `"Nuclear, Industrial Radiology, and Biological Technologies"', add
label define degfieldd_lbl 5200 `"Psychology"', add
label define degfieldd_lbl 5201 `"Educational Psychology"', add
label define degfieldd_lbl 5202 `"Clinical Psychology"', add
label define degfieldd_lbl 5203 `"Counseling Psychology"', add
label define degfieldd_lbl 5205 `"Industrial and Organizational Psychology"', add
label define degfieldd_lbl 5206 `"Social Psychology"', add
label define degfieldd_lbl 5299 `"Miscellaneous Psychology"', add
label define degfieldd_lbl 5301 `"Criminal Justice and Fire Protection"', add
label define degfieldd_lbl 5400 `"Public Affairs, Policy, and Social Work"', add
label define degfieldd_lbl 5401 `"Public Administration"', add
label define degfieldd_lbl 5402 `"Public Policy"', add
label define degfieldd_lbl 5403 `"Human Services and Community Organization"', add
label define degfieldd_lbl 5404 `"Social Work"', add
label define degfieldd_lbl 5500 `"General Social Sciences"', add
label define degfieldd_lbl 5501 `"Economics"', add
label define degfieldd_lbl 5502 `"Anthropology and Archeology"', add
label define degfieldd_lbl 5503 `"Criminology"', add
label define degfieldd_lbl 5504 `"Geography"', add
label define degfieldd_lbl 5505 `"International Relations"', add
label define degfieldd_lbl 5506 `"Political Science and Government"', add
label define degfieldd_lbl 5507 `"Sociology"', add
label define degfieldd_lbl 5599 `"Miscellaneous Social Sciences"', add
label define degfieldd_lbl 5601 `"Construction Services"', add
label define degfieldd_lbl 5701 `"Electrical and Mechanic Repairs and Technologies"', add
label define degfieldd_lbl 5801 `"Precision Production and Industrial Arts"', add
label define degfieldd_lbl 5901 `"Transportation Sciences and Technologies"', add
label define degfieldd_lbl 6000 `"Fine Arts"', add
label define degfieldd_lbl 6001 `"Drama and Theater Arts"', add
label define degfieldd_lbl 6002 `"Music"', add
label define degfieldd_lbl 6003 `"Visual and Performing Arts"', add
label define degfieldd_lbl 6004 `"Commercial Art and Graphic Design"', add
label define degfieldd_lbl 6005 `"Film, Video and Photographic Arts"', add
label define degfieldd_lbl 6006 `"Art History and Criticism"', add
label define degfieldd_lbl 6007 `"Studio Arts"', add
label define degfieldd_lbl 6099 `"Miscellaneous Fine Arts"', add
label define degfieldd_lbl 6100 `"General Medical and Health Services"', add
label define degfieldd_lbl 6102 `"Communication Disorders Sciences and Services"', add
label define degfieldd_lbl 6103 `"Health and Medical Administrative Services"', add
label define degfieldd_lbl 6104 `"Medical Assisting Services"', add
label define degfieldd_lbl 6105 `"Medical Technologies Technicians"', add
label define degfieldd_lbl 6106 `"Health and Medical Preparatory Programs"', add
label define degfieldd_lbl 6107 `"Nursing"', add
label define degfieldd_lbl 6108 `"Pharmacy, Pharmaceutical Sciences, and Administration"', add
label define degfieldd_lbl 6109 `"Treatment Therapy Professions"', add
label define degfieldd_lbl 6110 `"Community and Public Health"', add
label define degfieldd_lbl 6199 `"Miscellaneous Health Medical Professions"', add
label define degfieldd_lbl 6200 `"General Business"', add
label define degfieldd_lbl 6201 `"Accounting"', add
label define degfieldd_lbl 6202 `"Actuarial Science"', add
label define degfieldd_lbl 6203 `"Business Management and Administration"', add
label define degfieldd_lbl 6204 `"Operations, Logistics and E-Commerce"', add
label define degfieldd_lbl 6205 `"Business Economics"', add
label define degfieldd_lbl 6206 `"Marketing and Marketing Research"', add
label define degfieldd_lbl 6207 `"Finance"', add
label define degfieldd_lbl 6209 `"Human Resources and Personnel Management"', add
label define degfieldd_lbl 6210 `"International Business"', add
label define degfieldd_lbl 6211 `"Hospitality Management"', add
label define degfieldd_lbl 6212 `"Management Information Systems and Statistics"', add
label define degfieldd_lbl 6299 `"Miscellaneous Business and Medical Administration"', add
label define degfieldd_lbl 6402 `"History"', add
label define degfieldd_lbl 6403 `"United States History"', add
label values degfieldd degfieldd_lbl

label define empstat_lbl 0 `"N/A"'
label define empstat_lbl 1 `"Employed"', add
label define empstat_lbl 2 `"Unemployed"', add
label define empstat_lbl 3 `"Not in labor force"', add
label define empstat_lbl 9 `"Unknown/Illegible"', add
label values empstat empstat_lbl

label define empstatd_lbl 00 `"N/A"'
label define empstatd_lbl 10 `"At work"', add
label define empstatd_lbl 11 `"At work, public emerg"', add
label define empstatd_lbl 12 `"Has job, not working"', add
label define empstatd_lbl 13 `"Armed forces"', add
label define empstatd_lbl 14 `"Armed forces--at work"', add
label define empstatd_lbl 15 `"Armed forces--not at work but with job"', add
label define empstatd_lbl 20 `"Unemployed"', add
label define empstatd_lbl 21 `"Unemp, exper worker"', add
label define empstatd_lbl 22 `"Unemp, new worker"', add
label define empstatd_lbl 30 `"Not in Labor Force"', add
label define empstatd_lbl 31 `"NILF, housework"', add
label define empstatd_lbl 32 `"NILF, unable to work"', add
label define empstatd_lbl 33 `"NILF, school"', add
label define empstatd_lbl 34 `"NILF, other"', add
label define empstatd_lbl 99 `"Unknown/Illegible"', add
label values empstatd empstatd_lbl

label define labforce_lbl 0 `"N/A"'
label define labforce_lbl 1 `"No, not in the labor force"', add
label define labforce_lbl 2 `"Yes, in the labor force"', add
label define labforce_lbl 9 `"Unclassifiable (employment status unknown)"', add
label values labforce labforce_lbl

label define classwkr_lbl 0 `"N/A"'
label define classwkr_lbl 1 `"Self-employed"', add
label define classwkr_lbl 2 `"Works for wages"', add
label define classwkr_lbl 9 `"Unknown"', add
label values classwkr classwkr_lbl

label define classwkrd_lbl 00 `"N/A"'
label define classwkrd_lbl 10 `"Self-employed"', add
label define classwkrd_lbl 11 `"Employer"', add
label define classwkrd_lbl 12 `"Working on own account"', add
label define classwkrd_lbl 13 `"Self-employed, not incorporated"', add
label define classwkrd_lbl 14 `"Self-employed, incorporated"', add
label define classwkrd_lbl 20 `"Works for wages"', add
label define classwkrd_lbl 21 `"Works on salary (1920)"', add
label define classwkrd_lbl 22 `"Wage/salary, private"', add
label define classwkrd_lbl 23 `"Wage/salary at non-profit"', add
label define classwkrd_lbl 24 `"Wage/salary, government"', add
label define classwkrd_lbl 25 `"Federal govt employee"', add
label define classwkrd_lbl 26 `"Armed forces"', add
label define classwkrd_lbl 27 `"State govt employee"', add
label define classwkrd_lbl 28 `"Local govt employee"', add
label define classwkrd_lbl 29 `"Unpaid family worker"', add
label define classwkrd_lbl 98 `"Illegible"', add
label define classwkrd_lbl 99 `"Unknown"', add
label values classwkrd classwkrd_lbl

label define occ_lbl 0000 `"0000"'
label define occ_lbl 0001 `"0001"', add
label define occ_lbl 0002 `"0002"', add
label define occ_lbl 0003 `"0003"', add
label define occ_lbl 0004 `"0004"', add
label define occ_lbl 0005 `"0005"', add
label define occ_lbl 0006 `"0006"', add
label define occ_lbl 0007 `"0007"', add
label define occ_lbl 0008 `"0008"', add
label define occ_lbl 0009 `"0009"', add
label define occ_lbl 0010 `"0010"', add
label define occ_lbl 0011 `"0011"', add
label define occ_lbl 0012 `"0012"', add
label define occ_lbl 0013 `"0013"', add
label define occ_lbl 0014 `"0014"', add
label define occ_lbl 0015 `"0015"', add
label define occ_lbl 0016 `"0016"', add
label define occ_lbl 0017 `"0017"', add
label define occ_lbl 0018 `"0018"', add
label define occ_lbl 0019 `"0019"', add
label define occ_lbl 0020 `"0020"', add
label define occ_lbl 0021 `"0021"', add
label define occ_lbl 0022 `"0022"', add
label define occ_lbl 0023 `"0023"', add
label define occ_lbl 0024 `"0024"', add
label define occ_lbl 0025 `"0025"', add
label define occ_lbl 0026 `"0026"', add
label define occ_lbl 0027 `"0027"', add
label define occ_lbl 0028 `"0028"', add
label define occ_lbl 0029 `"0029"', add
label define occ_lbl 0030 `"0030"', add
label define occ_lbl 0031 `"0031"', add
label define occ_lbl 0032 `"0032"', add
label define occ_lbl 0033 `"0033"', add
label define occ_lbl 0034 `"0034"', add
label define occ_lbl 0035 `"0035"', add
label define occ_lbl 0036 `"0036"', add
label define occ_lbl 0037 `"0037"', add
label define occ_lbl 0038 `"0038"', add
label define occ_lbl 0039 `"0039"', add
label define occ_lbl 0040 `"0040"', add
label define occ_lbl 0041 `"0041"', add
label define occ_lbl 0042 `"0042"', add
label define occ_lbl 0043 `"0043"', add
label define occ_lbl 0044 `"0044"', add
label define occ_lbl 0045 `"0045"', add
label define occ_lbl 0046 `"0046"', add
label define occ_lbl 0047 `"0047"', add
label define occ_lbl 0048 `"0048"', add
label define occ_lbl 0049 `"0049"', add
label define occ_lbl 0050 `"0050"', add
label define occ_lbl 0051 `"0051"', add
label define occ_lbl 0052 `"0052"', add
label define occ_lbl 0053 `"0053"', add
label define occ_lbl 0054 `"0054"', add
label define occ_lbl 0055 `"0055"', add
label define occ_lbl 0056 `"0056"', add
label define occ_lbl 0057 `"0057"', add
label define occ_lbl 0058 `"0058"', add
label define occ_lbl 0059 `"0059"', add
label define occ_lbl 0060 `"0060"', add
label define occ_lbl 0061 `"0061"', add
label define occ_lbl 0062 `"0062"', add
label define occ_lbl 0063 `"0063"', add
label define occ_lbl 0064 `"0064"', add
label define occ_lbl 0065 `"0065"', add
label define occ_lbl 0066 `"0066"', add
label define occ_lbl 0067 `"0067"', add
label define occ_lbl 0068 `"0068"', add
label define occ_lbl 0069 `"0069"', add
label define occ_lbl 0070 `"0070"', add
label define occ_lbl 0071 `"0071"', add
label define occ_lbl 0072 `"0072"', add
label define occ_lbl 0073 `"0073"', add
label define occ_lbl 0074 `"0074"', add
label define occ_lbl 0075 `"0075"', add
label define occ_lbl 0076 `"0076"', add
label define occ_lbl 0077 `"0077"', add
label define occ_lbl 0078 `"0078"', add
label define occ_lbl 0079 `"0079"', add
label define occ_lbl 0080 `"0080"', add
label define occ_lbl 0081 `"0081"', add
label define occ_lbl 0082 `"0082"', add
label define occ_lbl 0083 `"0083"', add
label define occ_lbl 0084 `"0084"', add
label define occ_lbl 0085 `"0085"', add
label define occ_lbl 0086 `"0086"', add
label define occ_lbl 0087 `"0087"', add
label define occ_lbl 0088 `"0088"', add
label define occ_lbl 0089 `"0089"', add
label define occ_lbl 0090 `"0090"', add
label define occ_lbl 0091 `"0091"', add
label define occ_lbl 0092 `"0092"', add
label define occ_lbl 0093 `"0093"', add
label define occ_lbl 0094 `"0094"', add
label define occ_lbl 0095 `"0095"', add
label define occ_lbl 0096 `"0096"', add
label define occ_lbl 0097 `"0097"', add
label define occ_lbl 0098 `"0098"', add
label define occ_lbl 0099 `"0099"', add
label define occ_lbl 0100 `"0100"', add
label define occ_lbl 0101 `"0101"', add
label define occ_lbl 0102 `"0102"', add
label define occ_lbl 0103 `"0103"', add
label define occ_lbl 0104 `"0104"', add
label define occ_lbl 0105 `"0105"', add
label define occ_lbl 0106 `"0106"', add
label define occ_lbl 0107 `"0107"', add
label define occ_lbl 0108 `"0108"', add
label define occ_lbl 0109 `"0109"', add
label define occ_lbl 0110 `"0110"', add
label define occ_lbl 0111 `"0111"', add
label define occ_lbl 0112 `"0112"', add
label define occ_lbl 0113 `"0113"', add
label define occ_lbl 0114 `"0114"', add
label define occ_lbl 0115 `"0115"', add
label define occ_lbl 0116 `"0116"', add
label define occ_lbl 0117 `"0117"', add
label define occ_lbl 0118 `"0118"', add
label define occ_lbl 0119 `"0119"', add
label define occ_lbl 0120 `"0120"', add
label define occ_lbl 0121 `"0121"', add
label define occ_lbl 0122 `"0122"', add
label define occ_lbl 0123 `"0123"', add
label define occ_lbl 0124 `"0124"', add
label define occ_lbl 0125 `"0125"', add
label define occ_lbl 0126 `"0126"', add
label define occ_lbl 0127 `"0127"', add
label define occ_lbl 0128 `"0128"', add
label define occ_lbl 0129 `"0129"', add
label define occ_lbl 0130 `"0130"', add
label define occ_lbl 0131 `"0131"', add
label define occ_lbl 0132 `"0132"', add
label define occ_lbl 0133 `"0133"', add
label define occ_lbl 0134 `"0134"', add
label define occ_lbl 0135 `"0135"', add
label define occ_lbl 0136 `"0136"', add
label define occ_lbl 0137 `"0137"', add
label define occ_lbl 0138 `"0138"', add
label define occ_lbl 0139 `"0139"', add
label define occ_lbl 0140 `"0140"', add
label define occ_lbl 0141 `"0141"', add
label define occ_lbl 0142 `"0142"', add
label define occ_lbl 0143 `"0143"', add
label define occ_lbl 0144 `"0144"', add
label define occ_lbl 0145 `"0145"', add
label define occ_lbl 0146 `"0146"', add
label define occ_lbl 0147 `"0147"', add
label define occ_lbl 0148 `"0148"', add
label define occ_lbl 0149 `"0149"', add
label define occ_lbl 0150 `"0150"', add
label define occ_lbl 0151 `"0151"', add
label define occ_lbl 0152 `"0152"', add
label define occ_lbl 0153 `"0153"', add
label define occ_lbl 0154 `"0154"', add
label define occ_lbl 0155 `"0155"', add
label define occ_lbl 0156 `"0156"', add
label define occ_lbl 0157 `"0157"', add
label define occ_lbl 0158 `"0158"', add
label define occ_lbl 0159 `"0159"', add
label define occ_lbl 0160 `"0160"', add
label define occ_lbl 0161 `"0161"', add
label define occ_lbl 0162 `"0162"', add
label define occ_lbl 0163 `"0163"', add
label define occ_lbl 0164 `"0164"', add
label define occ_lbl 0165 `"0165"', add
label define occ_lbl 0166 `"0166"', add
label define occ_lbl 0167 `"0167"', add
label define occ_lbl 0168 `"0168"', add
label define occ_lbl 0169 `"0169"', add
label define occ_lbl 0170 `"0170"', add
label define occ_lbl 0171 `"0171"', add
label define occ_lbl 0172 `"0172"', add
label define occ_lbl 0173 `"0173"', add
label define occ_lbl 0174 `"0174"', add
label define occ_lbl 0175 `"0175"', add
label define occ_lbl 0176 `"0176"', add
label define occ_lbl 0177 `"0177"', add
label define occ_lbl 0178 `"0178"', add
label define occ_lbl 0179 `"0179"', add
label define occ_lbl 0180 `"0180"', add
label define occ_lbl 0181 `"0181"', add
label define occ_lbl 0182 `"0182"', add
label define occ_lbl 0183 `"0183"', add
label define occ_lbl 0184 `"0184"', add
label define occ_lbl 0185 `"0185"', add
label define occ_lbl 0186 `"0186"', add
label define occ_lbl 0187 `"0187"', add
label define occ_lbl 0188 `"0188"', add
label define occ_lbl 0189 `"0189"', add
label define occ_lbl 0190 `"0190"', add
label define occ_lbl 0191 `"0191"', add
label define occ_lbl 0192 `"0192"', add
label define occ_lbl 0193 `"0193"', add
label define occ_lbl 0194 `"0194"', add
label define occ_lbl 0195 `"0195"', add
label define occ_lbl 0196 `"0196"', add
label define occ_lbl 0197 `"0197"', add
label define occ_lbl 0198 `"0198"', add
label define occ_lbl 0199 `"0199"', add
label define occ_lbl 0200 `"0200"', add
label define occ_lbl 0201 `"0201"', add
label define occ_lbl 0202 `"0202"', add
label define occ_lbl 0203 `"0203"', add
label define occ_lbl 0204 `"0204"', add
label define occ_lbl 0205 `"0205"', add
label define occ_lbl 0206 `"0206"', add
label define occ_lbl 0207 `"0207"', add
label define occ_lbl 0208 `"0208"', add
label define occ_lbl 0209 `"0209"', add
label define occ_lbl 0210 `"0210"', add
label define occ_lbl 0211 `"0211"', add
label define occ_lbl 0212 `"0212"', add
label define occ_lbl 0213 `"0213"', add
label define occ_lbl 0214 `"0214"', add
label define occ_lbl 0215 `"0215"', add
label define occ_lbl 0216 `"0216"', add
label define occ_lbl 0217 `"0217"', add
label define occ_lbl 0218 `"0218"', add
label define occ_lbl 0219 `"0219"', add
label define occ_lbl 0220 `"0220"', add
label define occ_lbl 0221 `"0221"', add
label define occ_lbl 0222 `"0222"', add
label define occ_lbl 0223 `"0223"', add
label define occ_lbl 0224 `"0224"', add
label define occ_lbl 0225 `"0225"', add
label define occ_lbl 0226 `"0226"', add
label define occ_lbl 0227 `"0227"', add
label define occ_lbl 0228 `"0228"', add
label define occ_lbl 0229 `"0229"', add
label define occ_lbl 0230 `"0230"', add
label define occ_lbl 0231 `"0231"', add
label define occ_lbl 0232 `"0232"', add
label define occ_lbl 0233 `"0233"', add
label define occ_lbl 0234 `"0234"', add
label define occ_lbl 0235 `"0235"', add
label define occ_lbl 0236 `"0236"', add
label define occ_lbl 0237 `"0237"', add
label define occ_lbl 0238 `"0238"', add
label define occ_lbl 0239 `"0239"', add
label define occ_lbl 0240 `"0240"', add
label define occ_lbl 0241 `"0241"', add
label define occ_lbl 0242 `"0242"', add
label define occ_lbl 0243 `"0243"', add
label define occ_lbl 0244 `"0244"', add
label define occ_lbl 0245 `"0245"', add
label define occ_lbl 0246 `"0246"', add
label define occ_lbl 0247 `"0247"', add
label define occ_lbl 0248 `"0248"', add
label define occ_lbl 0249 `"0249"', add
label define occ_lbl 0250 `"0250"', add
label define occ_lbl 0251 `"0251"', add
label define occ_lbl 0252 `"0252"', add
label define occ_lbl 0253 `"0253"', add
label define occ_lbl 0254 `"0254"', add
label define occ_lbl 0255 `"0255"', add
label define occ_lbl 0256 `"0256"', add
label define occ_lbl 0257 `"0257"', add
label define occ_lbl 0258 `"0258"', add
label define occ_lbl 0259 `"0259"', add
label define occ_lbl 0260 `"0260"', add
label define occ_lbl 0261 `"0261"', add
label define occ_lbl 0262 `"0262"', add
label define occ_lbl 0263 `"0263"', add
label define occ_lbl 0264 `"0264"', add
label define occ_lbl 0265 `"0265"', add
label define occ_lbl 0266 `"0266"', add
label define occ_lbl 0267 `"0267"', add
label define occ_lbl 0268 `"0268"', add
label define occ_lbl 0269 `"0269"', add
label define occ_lbl 0270 `"0270"', add
label define occ_lbl 0271 `"0271"', add
label define occ_lbl 0272 `"0272"', add
label define occ_lbl 0273 `"0273"', add
label define occ_lbl 0274 `"0274"', add
label define occ_lbl 0275 `"0275"', add
label define occ_lbl 0276 `"0276"', add
label define occ_lbl 0277 `"0277"', add
label define occ_lbl 0278 `"0278"', add
label define occ_lbl 0279 `"0279"', add
label define occ_lbl 0280 `"0280"', add
label define occ_lbl 0281 `"0281"', add
label define occ_lbl 0282 `"0282"', add
label define occ_lbl 0283 `"0283"', add
label define occ_lbl 0284 `"0284"', add
label define occ_lbl 0285 `"0285"', add
label define occ_lbl 0286 `"0286"', add
label define occ_lbl 0287 `"0287"', add
label define occ_lbl 0288 `"0288"', add
label define occ_lbl 0289 `"0289"', add
label define occ_lbl 0290 `"0290"', add
label define occ_lbl 0291 `"0291"', add
label define occ_lbl 0292 `"0292"', add
label define occ_lbl 0293 `"0293"', add
label define occ_lbl 0294 `"0294"', add
label define occ_lbl 0295 `"0295"', add
label define occ_lbl 0296 `"0296"', add
label define occ_lbl 0297 `"0297"', add
label define occ_lbl 0298 `"0298"', add
label define occ_lbl 0299 `"0299"', add
label define occ_lbl 0300 `"0300"', add
label define occ_lbl 0301 `"0301"', add
label define occ_lbl 0302 `"0302"', add
label define occ_lbl 0303 `"0303"', add
label define occ_lbl 0304 `"0304"', add
label define occ_lbl 0305 `"0305"', add
label define occ_lbl 0306 `"0306"', add
label define occ_lbl 0307 `"0307"', add
label define occ_lbl 0308 `"0308"', add
label define occ_lbl 0309 `"0309"', add
label define occ_lbl 0310 `"0310"', add
label define occ_lbl 0311 `"0311"', add
label define occ_lbl 0312 `"0312"', add
label define occ_lbl 0313 `"0313"', add
label define occ_lbl 0314 `"0314"', add
label define occ_lbl 0315 `"0315"', add
label define occ_lbl 0316 `"0316"', add
label define occ_lbl 0317 `"0317"', add
label define occ_lbl 0318 `"0318"', add
label define occ_lbl 0319 `"0319"', add
label define occ_lbl 0320 `"0320"', add
label define occ_lbl 0321 `"0321"', add
label define occ_lbl 0322 `"0322"', add
label define occ_lbl 0323 `"0323"', add
label define occ_lbl 0324 `"0324"', add
label define occ_lbl 0325 `"0325"', add
label define occ_lbl 0326 `"0326"', add
label define occ_lbl 0327 `"0327"', add
label define occ_lbl 0328 `"0328"', add
label define occ_lbl 0329 `"0329"', add
label define occ_lbl 0330 `"0330"', add
label define occ_lbl 0331 `"0331"', add
label define occ_lbl 0332 `"0332"', add
label define occ_lbl 0333 `"0333"', add
label define occ_lbl 0334 `"0334"', add
label define occ_lbl 0335 `"0335"', add
label define occ_lbl 0336 `"0336"', add
label define occ_lbl 0337 `"0337"', add
label define occ_lbl 0338 `"0338"', add
label define occ_lbl 0339 `"0339"', add
label define occ_lbl 0340 `"0340"', add
label define occ_lbl 0341 `"0341"', add
label define occ_lbl 0342 `"0342"', add
label define occ_lbl 0343 `"0343"', add
label define occ_lbl 0344 `"0344"', add
label define occ_lbl 0345 `"0345"', add
label define occ_lbl 0346 `"0346"', add
label define occ_lbl 0347 `"0347"', add
label define occ_lbl 0348 `"0348"', add
label define occ_lbl 0349 `"0349"', add
label define occ_lbl 0350 `"0350"', add
label define occ_lbl 0351 `"0351"', add
label define occ_lbl 0352 `"0352"', add
label define occ_lbl 0353 `"0353"', add
label define occ_lbl 0354 `"0354"', add
label define occ_lbl 0355 `"0355"', add
label define occ_lbl 0356 `"0356"', add
label define occ_lbl 0357 `"0357"', add
label define occ_lbl 0358 `"0358"', add
label define occ_lbl 0359 `"0359"', add
label define occ_lbl 0360 `"0360"', add
label define occ_lbl 0361 `"0361"', add
label define occ_lbl 0362 `"0362"', add
label define occ_lbl 0363 `"0363"', add
label define occ_lbl 0364 `"0364"', add
label define occ_lbl 0365 `"0365"', add
label define occ_lbl 0366 `"0366"', add
label define occ_lbl 0367 `"0367"', add
label define occ_lbl 0368 `"0368"', add
label define occ_lbl 0369 `"0369"', add
label define occ_lbl 0370 `"0370"', add
label define occ_lbl 0371 `"0371"', add
label define occ_lbl 0372 `"0372"', add
label define occ_lbl 0373 `"0373"', add
label define occ_lbl 0374 `"0374"', add
label define occ_lbl 0375 `"0375"', add
label define occ_lbl 0376 `"0376"', add
label define occ_lbl 0377 `"0377"', add
label define occ_lbl 0378 `"0378"', add
label define occ_lbl 0379 `"0379"', add
label define occ_lbl 0380 `"0380"', add
label define occ_lbl 0381 `"0381"', add
label define occ_lbl 0382 `"0382"', add
label define occ_lbl 0383 `"0383"', add
label define occ_lbl 0384 `"0384"', add
label define occ_lbl 0385 `"0385"', add
label define occ_lbl 0386 `"0386"', add
label define occ_lbl 0387 `"0387"', add
label define occ_lbl 0388 `"0388"', add
label define occ_lbl 0389 `"0389"', add
label define occ_lbl 0390 `"0390"', add
label define occ_lbl 0391 `"0391"', add
label define occ_lbl 0392 `"0392"', add
label define occ_lbl 0393 `"0393"', add
label define occ_lbl 0394 `"0394"', add
label define occ_lbl 0395 `"0395"', add
label define occ_lbl 0396 `"0396"', add
label define occ_lbl 0397 `"0397"', add
label define occ_lbl 0398 `"0398"', add
label define occ_lbl 0399 `"0399"', add
label define occ_lbl 0400 `"0400"', add
label define occ_lbl 0401 `"0401"', add
label define occ_lbl 0402 `"0402"', add
label define occ_lbl 0403 `"0403"', add
label define occ_lbl 0404 `"0404"', add
label define occ_lbl 0405 `"0405"', add
label define occ_lbl 0406 `"0406"', add
label define occ_lbl 0407 `"0407"', add
label define occ_lbl 0408 `"0408"', add
label define occ_lbl 0409 `"0409"', add
label define occ_lbl 0410 `"0410"', add
label define occ_lbl 0411 `"0411"', add
label define occ_lbl 0412 `"0412"', add
label define occ_lbl 0413 `"0413"', add
label define occ_lbl 0414 `"0414"', add
label define occ_lbl 0415 `"0415"', add
label define occ_lbl 0416 `"0416"', add
label define occ_lbl 0417 `"0417"', add
label define occ_lbl 0418 `"0418"', add
label define occ_lbl 0419 `"0419"', add
label define occ_lbl 0420 `"0420"', add
label define occ_lbl 0421 `"0421"', add
label define occ_lbl 0422 `"0422"', add
label define occ_lbl 0423 `"0423"', add
label define occ_lbl 0424 `"0424"', add
label define occ_lbl 0425 `"0425"', add
label define occ_lbl 0426 `"0426"', add
label define occ_lbl 0427 `"0427"', add
label define occ_lbl 0428 `"0428"', add
label define occ_lbl 0429 `"0429"', add
label define occ_lbl 0430 `"0430"', add
label define occ_lbl 0431 `"0431"', add
label define occ_lbl 0432 `"0432"', add
label define occ_lbl 0433 `"0433"', add
label define occ_lbl 0434 `"0434"', add
label define occ_lbl 0435 `"0435"', add
label define occ_lbl 0436 `"0436"', add
label define occ_lbl 0437 `"0437"', add
label define occ_lbl 0438 `"0438"', add
label define occ_lbl 0439 `"0439"', add
label define occ_lbl 0440 `"0440"', add
label define occ_lbl 0441 `"0441"', add
label define occ_lbl 0442 `"0442"', add
label define occ_lbl 0443 `"0443"', add
label define occ_lbl 0444 `"0444"', add
label define occ_lbl 0445 `"0445"', add
label define occ_lbl 0446 `"0446"', add
label define occ_lbl 0447 `"0447"', add
label define occ_lbl 0448 `"0448"', add
label define occ_lbl 0449 `"0449"', add
label define occ_lbl 0450 `"0450"', add
label define occ_lbl 0451 `"0451"', add
label define occ_lbl 0452 `"0452"', add
label define occ_lbl 0453 `"0453"', add
label define occ_lbl 0454 `"0454"', add
label define occ_lbl 0455 `"0455"', add
label define occ_lbl 0456 `"0456"', add
label define occ_lbl 0457 `"0457"', add
label define occ_lbl 0458 `"0458"', add
label define occ_lbl 0459 `"0459"', add
label define occ_lbl 0460 `"0460"', add
label define occ_lbl 0461 `"0461"', add
label define occ_lbl 0462 `"0462"', add
label define occ_lbl 0463 `"0463"', add
label define occ_lbl 0464 `"0464"', add
label define occ_lbl 0465 `"0465"', add
label define occ_lbl 0466 `"0466"', add
label define occ_lbl 0467 `"0467"', add
label define occ_lbl 0468 `"0468"', add
label define occ_lbl 0469 `"0469"', add
label define occ_lbl 0470 `"0470"', add
label define occ_lbl 0471 `"0471"', add
label define occ_lbl 0472 `"0472"', add
label define occ_lbl 0473 `"0473"', add
label define occ_lbl 0474 `"0474"', add
label define occ_lbl 0475 `"0475"', add
label define occ_lbl 0476 `"0476"', add
label define occ_lbl 0477 `"0477"', add
label define occ_lbl 0478 `"0478"', add
label define occ_lbl 0479 `"0479"', add
label define occ_lbl 0480 `"0480"', add
label define occ_lbl 0481 `"0481"', add
label define occ_lbl 0482 `"0482"', add
label define occ_lbl 0483 `"0483"', add
label define occ_lbl 0484 `"0484"', add
label define occ_lbl 0485 `"0485"', add
label define occ_lbl 0486 `"0486"', add
label define occ_lbl 0487 `"0487"', add
label define occ_lbl 0488 `"0488"', add
label define occ_lbl 0489 `"0489"', add
label define occ_lbl 0490 `"0490"', add
label define occ_lbl 0491 `"0491"', add
label define occ_lbl 0492 `"0492"', add
label define occ_lbl 0493 `"0493"', add
label define occ_lbl 0494 `"0494"', add
label define occ_lbl 0495 `"0495"', add
label define occ_lbl 0496 `"0496"', add
label define occ_lbl 0497 `"0497"', add
label define occ_lbl 0498 `"0498"', add
label define occ_lbl 0499 `"0499"', add
label define occ_lbl 0500 `"0500"', add
label define occ_lbl 0501 `"0501"', add
label define occ_lbl 0502 `"0502"', add
label define occ_lbl 0503 `"0503"', add
label define occ_lbl 0504 `"0504"', add
label define occ_lbl 0505 `"0505"', add
label define occ_lbl 0506 `"0506"', add
label define occ_lbl 0507 `"0507"', add
label define occ_lbl 0508 `"0508"', add
label define occ_lbl 0509 `"0509"', add
label define occ_lbl 0510 `"0510"', add
label define occ_lbl 0511 `"0511"', add
label define occ_lbl 0512 `"0512"', add
label define occ_lbl 0513 `"0513"', add
label define occ_lbl 0514 `"0514"', add
label define occ_lbl 0515 `"0515"', add
label define occ_lbl 0516 `"0516"', add
label define occ_lbl 0517 `"0517"', add
label define occ_lbl 0518 `"0518"', add
label define occ_lbl 0519 `"0519"', add
label define occ_lbl 0520 `"0520"', add
label define occ_lbl 0521 `"0521"', add
label define occ_lbl 0522 `"0522"', add
label define occ_lbl 0523 `"0523"', add
label define occ_lbl 0524 `"0524"', add
label define occ_lbl 0525 `"0525"', add
label define occ_lbl 0526 `"0526"', add
label define occ_lbl 0527 `"0527"', add
label define occ_lbl 0528 `"0528"', add
label define occ_lbl 0529 `"0529"', add
label define occ_lbl 0530 `"0530"', add
label define occ_lbl 0531 `"0531"', add
label define occ_lbl 0532 `"0532"', add
label define occ_lbl 0533 `"0533"', add
label define occ_lbl 0534 `"0534"', add
label define occ_lbl 0535 `"0535"', add
label define occ_lbl 0536 `"0536"', add
label define occ_lbl 0537 `"0537"', add
label define occ_lbl 0538 `"0538"', add
label define occ_lbl 0539 `"0539"', add
label define occ_lbl 0540 `"0540"', add
label define occ_lbl 0541 `"0541"', add
label define occ_lbl 0542 `"0542"', add
label define occ_lbl 0543 `"0543"', add
label define occ_lbl 0544 `"0544"', add
label define occ_lbl 0545 `"0545"', add
label define occ_lbl 0546 `"0546"', add
label define occ_lbl 0547 `"0547"', add
label define occ_lbl 0548 `"0548"', add
label define occ_lbl 0549 `"0549"', add
label define occ_lbl 0550 `"0550"', add
label define occ_lbl 0551 `"0551"', add
label define occ_lbl 0552 `"0552"', add
label define occ_lbl 0553 `"0553"', add
label define occ_lbl 0554 `"0554"', add
label define occ_lbl 0555 `"0555"', add
label define occ_lbl 0556 `"0556"', add
label define occ_lbl 0557 `"0557"', add
label define occ_lbl 0558 `"0558"', add
label define occ_lbl 0559 `"0559"', add
label define occ_lbl 0560 `"0560"', add
label define occ_lbl 0561 `"0561"', add
label define occ_lbl 0562 `"0562"', add
label define occ_lbl 0563 `"0563"', add
label define occ_lbl 0564 `"0564"', add
label define occ_lbl 0565 `"0565"', add
label define occ_lbl 0566 `"0566"', add
label define occ_lbl 0567 `"0567"', add
label define occ_lbl 0568 `"0568"', add
label define occ_lbl 0569 `"0569"', add
label define occ_lbl 0570 `"0570"', add
label define occ_lbl 0571 `"0571"', add
label define occ_lbl 0572 `"0572"', add
label define occ_lbl 0573 `"0573"', add
label define occ_lbl 0574 `"0574"', add
label define occ_lbl 0575 `"0575"', add
label define occ_lbl 0576 `"0576"', add
label define occ_lbl 0577 `"0577"', add
label define occ_lbl 0578 `"0578"', add
label define occ_lbl 0579 `"0579"', add
label define occ_lbl 0580 `"0580"', add
label define occ_lbl 0581 `"0581"', add
label define occ_lbl 0582 `"0582"', add
label define occ_lbl 0583 `"0583"', add
label define occ_lbl 0584 `"0584"', add
label define occ_lbl 0585 `"0585"', add
label define occ_lbl 0586 `"0586"', add
label define occ_lbl 0587 `"0587"', add
label define occ_lbl 0588 `"0588"', add
label define occ_lbl 0589 `"0589"', add
label define occ_lbl 0590 `"0590"', add
label define occ_lbl 0591 `"0591"', add
label define occ_lbl 0592 `"0592"', add
label define occ_lbl 0593 `"0593"', add
label define occ_lbl 0594 `"0594"', add
label define occ_lbl 0595 `"0595"', add
label define occ_lbl 0596 `"0596"', add
label define occ_lbl 0597 `"0597"', add
label define occ_lbl 0598 `"0598"', add
label define occ_lbl 0599 `"0599"', add
label define occ_lbl 0600 `"0600"', add
label define occ_lbl 0601 `"0601"', add
label define occ_lbl 0602 `"0602"', add
label define occ_lbl 0603 `"0603"', add
label define occ_lbl 0604 `"0604"', add
label define occ_lbl 0605 `"0605"', add
label define occ_lbl 0606 `"0606"', add
label define occ_lbl 0607 `"0607"', add
label define occ_lbl 0608 `"0608"', add
label define occ_lbl 0609 `"0609"', add
label define occ_lbl 0610 `"0610"', add
label define occ_lbl 0611 `"0611"', add
label define occ_lbl 0612 `"0612"', add
label define occ_lbl 0613 `"0613"', add
label define occ_lbl 0614 `"0614"', add
label define occ_lbl 0615 `"0615"', add
label define occ_lbl 0616 `"0616"', add
label define occ_lbl 0617 `"0617"', add
label define occ_lbl 0618 `"0618"', add
label define occ_lbl 0619 `"0619"', add
label define occ_lbl 0620 `"0620"', add
label define occ_lbl 0621 `"0621"', add
label define occ_lbl 0622 `"0622"', add
label define occ_lbl 0623 `"0623"', add
label define occ_lbl 0624 `"0624"', add
label define occ_lbl 0625 `"0625"', add
label define occ_lbl 0626 `"0626"', add
label define occ_lbl 0627 `"0627"', add
label define occ_lbl 0628 `"0628"', add
label define occ_lbl 0629 `"0629"', add
label define occ_lbl 0630 `"0630"', add
label define occ_lbl 0631 `"0631"', add
label define occ_lbl 0632 `"0632"', add
label define occ_lbl 0633 `"0633"', add
label define occ_lbl 0634 `"0634"', add
label define occ_lbl 0635 `"0635"', add
label define occ_lbl 0636 `"0636"', add
label define occ_lbl 0637 `"0637"', add
label define occ_lbl 0638 `"0638"', add
label define occ_lbl 0639 `"0639"', add
label define occ_lbl 0640 `"0640"', add
label define occ_lbl 0641 `"0641"', add
label define occ_lbl 0642 `"0642"', add
label define occ_lbl 0643 `"0643"', add
label define occ_lbl 0644 `"0644"', add
label define occ_lbl 0645 `"0645"', add
label define occ_lbl 0646 `"0646"', add
label define occ_lbl 0647 `"0647"', add
label define occ_lbl 0648 `"0648"', add
label define occ_lbl 0649 `"0649"', add
label define occ_lbl 0650 `"0650"', add
label define occ_lbl 0651 `"0651"', add
label define occ_lbl 0652 `"0652"', add
label define occ_lbl 0653 `"0653"', add
label define occ_lbl 0654 `"0654"', add
label define occ_lbl 0655 `"0655"', add
label define occ_lbl 0656 `"0656"', add
label define occ_lbl 0657 `"0657"', add
label define occ_lbl 0658 `"0658"', add
label define occ_lbl 0659 `"0659"', add
label define occ_lbl 0660 `"0660"', add
label define occ_lbl 0661 `"0661"', add
label define occ_lbl 0662 `"0662"', add
label define occ_lbl 0663 `"0663"', add
label define occ_lbl 0664 `"0664"', add
label define occ_lbl 0665 `"0665"', add
label define occ_lbl 0666 `"0666"', add
label define occ_lbl 0667 `"0667"', add
label define occ_lbl 0668 `"0668"', add
label define occ_lbl 0669 `"0669"', add
label define occ_lbl 0670 `"0670"', add
label define occ_lbl 0671 `"0671"', add
label define occ_lbl 0672 `"0672"', add
label define occ_lbl 0673 `"0673"', add
label define occ_lbl 0674 `"0674"', add
label define occ_lbl 0675 `"0675"', add
label define occ_lbl 0676 `"0676"', add
label define occ_lbl 0677 `"0677"', add
label define occ_lbl 0678 `"0678"', add
label define occ_lbl 0679 `"0679"', add
label define occ_lbl 0680 `"0680"', add
label define occ_lbl 0681 `"0681"', add
label define occ_lbl 0682 `"0682"', add
label define occ_lbl 0683 `"0683"', add
label define occ_lbl 0684 `"0684"', add
label define occ_lbl 0685 `"0685"', add
label define occ_lbl 0686 `"0686"', add
label define occ_lbl 0687 `"0687"', add
label define occ_lbl 0688 `"0688"', add
label define occ_lbl 0689 `"0689"', add
label define occ_lbl 0690 `"0690"', add
label define occ_lbl 0691 `"0691"', add
label define occ_lbl 0692 `"0692"', add
label define occ_lbl 0693 `"0693"', add
label define occ_lbl 0694 `"0694"', add
label define occ_lbl 0695 `"0695"', add
label define occ_lbl 0696 `"0696"', add
label define occ_lbl 0697 `"0697"', add
label define occ_lbl 0698 `"0698"', add
label define occ_lbl 0699 `"0699"', add
label define occ_lbl 0700 `"0700"', add
label define occ_lbl 0701 `"0701"', add
label define occ_lbl 0702 `"0702"', add
label define occ_lbl 0703 `"0703"', add
label define occ_lbl 0704 `"0704"', add
label define occ_lbl 0705 `"0705"', add
label define occ_lbl 0706 `"0706"', add
label define occ_lbl 0707 `"0707"', add
label define occ_lbl 0708 `"0708"', add
label define occ_lbl 0709 `"0709"', add
label define occ_lbl 0710 `"0710"', add
label define occ_lbl 0711 `"0711"', add
label define occ_lbl 0712 `"0712"', add
label define occ_lbl 0713 `"0713"', add
label define occ_lbl 0714 `"0714"', add
label define occ_lbl 0715 `"0715"', add
label define occ_lbl 0716 `"0716"', add
label define occ_lbl 0717 `"0717"', add
label define occ_lbl 0718 `"0718"', add
label define occ_lbl 0719 `"0719"', add
label define occ_lbl 0720 `"0720"', add
label define occ_lbl 0721 `"0721"', add
label define occ_lbl 0722 `"0722"', add
label define occ_lbl 0723 `"0723"', add
label define occ_lbl 0724 `"0724"', add
label define occ_lbl 0725 `"0725"', add
label define occ_lbl 0726 `"0726"', add
label define occ_lbl 0727 `"0727"', add
label define occ_lbl 0728 `"0728"', add
label define occ_lbl 0729 `"0729"', add
label define occ_lbl 0730 `"0730"', add
label define occ_lbl 0731 `"0731"', add
label define occ_lbl 0732 `"0732"', add
label define occ_lbl 0733 `"0733"', add
label define occ_lbl 0734 `"0734"', add
label define occ_lbl 0735 `"0735"', add
label define occ_lbl 0736 `"0736"', add
label define occ_lbl 0737 `"0737"', add
label define occ_lbl 0738 `"0738"', add
label define occ_lbl 0739 `"0739"', add
label define occ_lbl 0740 `"0740"', add
label define occ_lbl 0741 `"0741"', add
label define occ_lbl 0742 `"0742"', add
label define occ_lbl 0743 `"0743"', add
label define occ_lbl 0744 `"0744"', add
label define occ_lbl 0745 `"0745"', add
label define occ_lbl 0746 `"0746"', add
label define occ_lbl 0747 `"0747"', add
label define occ_lbl 0748 `"0748"', add
label define occ_lbl 0749 `"0749"', add
label define occ_lbl 0750 `"0750"', add
label define occ_lbl 0751 `"0751"', add
label define occ_lbl 0752 `"0752"', add
label define occ_lbl 0753 `"0753"', add
label define occ_lbl 0754 `"0754"', add
label define occ_lbl 0755 `"0755"', add
label define occ_lbl 0756 `"0756"', add
label define occ_lbl 0757 `"0757"', add
label define occ_lbl 0758 `"0758"', add
label define occ_lbl 0759 `"0759"', add
label define occ_lbl 0760 `"0760"', add
label define occ_lbl 0761 `"0761"', add
label define occ_lbl 0762 `"0762"', add
label define occ_lbl 0763 `"0763"', add
label define occ_lbl 0764 `"0764"', add
label define occ_lbl 0765 `"0765"', add
label define occ_lbl 0766 `"0766"', add
label define occ_lbl 0767 `"0767"', add
label define occ_lbl 0768 `"0768"', add
label define occ_lbl 0769 `"0769"', add
label define occ_lbl 0770 `"0770"', add
label define occ_lbl 0771 `"0771"', add
label define occ_lbl 0772 `"0772"', add
label define occ_lbl 0773 `"0773"', add
label define occ_lbl 0774 `"0774"', add
label define occ_lbl 0775 `"0775"', add
label define occ_lbl 0776 `"0776"', add
label define occ_lbl 0777 `"0777"', add
label define occ_lbl 0778 `"0778"', add
label define occ_lbl 0779 `"0779"', add
label define occ_lbl 0780 `"0780"', add
label define occ_lbl 0781 `"0781"', add
label define occ_lbl 0782 `"0782"', add
label define occ_lbl 0783 `"0783"', add
label define occ_lbl 0784 `"0784"', add
label define occ_lbl 0785 `"0785"', add
label define occ_lbl 0786 `"0786"', add
label define occ_lbl 0787 `"0787"', add
label define occ_lbl 0788 `"0788"', add
label define occ_lbl 0789 `"0789"', add
label define occ_lbl 0790 `"0790"', add
label define occ_lbl 0791 `"0791"', add
label define occ_lbl 0792 `"0792"', add
label define occ_lbl 0793 `"0793"', add
label define occ_lbl 0794 `"0794"', add
label define occ_lbl 0795 `"0795"', add
label define occ_lbl 0796 `"0796"', add
label define occ_lbl 0797 `"0797"', add
label define occ_lbl 0798 `"0798"', add
label define occ_lbl 0799 `"0799"', add
label define occ_lbl 0800 `"0800"', add
label define occ_lbl 0801 `"0801"', add
label define occ_lbl 0802 `"0802"', add
label define occ_lbl 0803 `"0803"', add
label define occ_lbl 0804 `"0804"', add
label define occ_lbl 0805 `"0805"', add
label define occ_lbl 0806 `"0806"', add
label define occ_lbl 0807 `"0807"', add
label define occ_lbl 0808 `"0808"', add
label define occ_lbl 0809 `"0809"', add
label define occ_lbl 0810 `"0810"', add
label define occ_lbl 0811 `"0811"', add
label define occ_lbl 0812 `"0812"', add
label define occ_lbl 0813 `"0813"', add
label define occ_lbl 0814 `"0814"', add
label define occ_lbl 0815 `"0815"', add
label define occ_lbl 0816 `"0816"', add
label define occ_lbl 0817 `"0817"', add
label define occ_lbl 0818 `"0818"', add
label define occ_lbl 0819 `"0819"', add
label define occ_lbl 0820 `"0820"', add
label define occ_lbl 0821 `"0821"', add
label define occ_lbl 0822 `"0822"', add
label define occ_lbl 0823 `"0823"', add
label define occ_lbl 0824 `"0824"', add
label define occ_lbl 0825 `"0825"', add
label define occ_lbl 0826 `"0826"', add
label define occ_lbl 0827 `"0827"', add
label define occ_lbl 0828 `"0828"', add
label define occ_lbl 0829 `"0829"', add
label define occ_lbl 0830 `"0830"', add
label define occ_lbl 0831 `"0831"', add
label define occ_lbl 0832 `"0832"', add
label define occ_lbl 0833 `"0833"', add
label define occ_lbl 0834 `"0834"', add
label define occ_lbl 0835 `"0835"', add
label define occ_lbl 0836 `"0836"', add
label define occ_lbl 0837 `"0837"', add
label define occ_lbl 0838 `"0838"', add
label define occ_lbl 0839 `"0839"', add
label define occ_lbl 0840 `"0840"', add
label define occ_lbl 0841 `"0841"', add
label define occ_lbl 0842 `"0842"', add
label define occ_lbl 0843 `"0843"', add
label define occ_lbl 0844 `"0844"', add
label define occ_lbl 0845 `"0845"', add
label define occ_lbl 0846 `"0846"', add
label define occ_lbl 0847 `"0847"', add
label define occ_lbl 0848 `"0848"', add
label define occ_lbl 0849 `"0849"', add
label define occ_lbl 0850 `"0850"', add
label define occ_lbl 0851 `"0851"', add
label define occ_lbl 0852 `"0852"', add
label define occ_lbl 0853 `"0853"', add
label define occ_lbl 0854 `"0854"', add
label define occ_lbl 0855 `"0855"', add
label define occ_lbl 0856 `"0856"', add
label define occ_lbl 0857 `"0857"', add
label define occ_lbl 0858 `"0858"', add
label define occ_lbl 0859 `"0859"', add
label define occ_lbl 0860 `"0860"', add
label define occ_lbl 0861 `"0861"', add
label define occ_lbl 0862 `"0862"', add
label define occ_lbl 0863 `"0863"', add
label define occ_lbl 0864 `"0864"', add
label define occ_lbl 0865 `"0865"', add
label define occ_lbl 0866 `"0866"', add
label define occ_lbl 0867 `"0867"', add
label define occ_lbl 0868 `"0868"', add
label define occ_lbl 0869 `"0869"', add
label define occ_lbl 0870 `"0870"', add
label define occ_lbl 0871 `"0871"', add
label define occ_lbl 0872 `"0872"', add
label define occ_lbl 0873 `"0873"', add
label define occ_lbl 0874 `"0874"', add
label define occ_lbl 0875 `"0875"', add
label define occ_lbl 0876 `"0876"', add
label define occ_lbl 0877 `"0877"', add
label define occ_lbl 0878 `"0878"', add
label define occ_lbl 0879 `"0879"', add
label define occ_lbl 0880 `"0880"', add
label define occ_lbl 0881 `"0881"', add
label define occ_lbl 0882 `"0882"', add
label define occ_lbl 0883 `"0883"', add
label define occ_lbl 0884 `"0884"', add
label define occ_lbl 0885 `"0885"', add
label define occ_lbl 0886 `"0886"', add
label define occ_lbl 0887 `"0887"', add
label define occ_lbl 0888 `"0888"', add
label define occ_lbl 0889 `"0889"', add
label define occ_lbl 0890 `"0890"', add
label define occ_lbl 0891 `"0891"', add
label define occ_lbl 0892 `"0892"', add
label define occ_lbl 0893 `"0893"', add
label define occ_lbl 0894 `"0894"', add
label define occ_lbl 0895 `"0895"', add
label define occ_lbl 0896 `"0896"', add
label define occ_lbl 0897 `"0897"', add
label define occ_lbl 0898 `"0898"', add
label define occ_lbl 0899 `"0899"', add
label define occ_lbl 0900 `"0900"', add
label define occ_lbl 0901 `"0901"', add
label define occ_lbl 0902 `"0902"', add
label define occ_lbl 0903 `"0903"', add
label define occ_lbl 0904 `"0904"', add
label define occ_lbl 0905 `"0905"', add
label define occ_lbl 0906 `"0906"', add
label define occ_lbl 0907 `"0907"', add
label define occ_lbl 0908 `"0908"', add
label define occ_lbl 0909 `"0909"', add
label define occ_lbl 0910 `"0910"', add
label define occ_lbl 0911 `"0911"', add
label define occ_lbl 0912 `"0912"', add
label define occ_lbl 0913 `"0913"', add
label define occ_lbl 0914 `"0914"', add
label define occ_lbl 0915 `"0915"', add
label define occ_lbl 0916 `"0916"', add
label define occ_lbl 0917 `"0917"', add
label define occ_lbl 0918 `"0918"', add
label define occ_lbl 0919 `"0919"', add
label define occ_lbl 0920 `"0920"', add
label define occ_lbl 0921 `"0921"', add
label define occ_lbl 0922 `"0922"', add
label define occ_lbl 0923 `"0923"', add
label define occ_lbl 0924 `"0924"', add
label define occ_lbl 0925 `"0925"', add
label define occ_lbl 0926 `"0926"', add
label define occ_lbl 0927 `"0927"', add
label define occ_lbl 0928 `"0928"', add
label define occ_lbl 0929 `"0929"', add
label define occ_lbl 0930 `"0930"', add
label define occ_lbl 0931 `"0931"', add
label define occ_lbl 0932 `"0932"', add
label define occ_lbl 0933 `"0933"', add
label define occ_lbl 0934 `"0934"', add
label define occ_lbl 0935 `"0935"', add
label define occ_lbl 0936 `"0936"', add
label define occ_lbl 0937 `"0937"', add
label define occ_lbl 0938 `"0938"', add
label define occ_lbl 0939 `"0939"', add
label define occ_lbl 0940 `"0940"', add
label define occ_lbl 0941 `"0941"', add
label define occ_lbl 0942 `"0942"', add
label define occ_lbl 0943 `"0943"', add
label define occ_lbl 0944 `"0944"', add
label define occ_lbl 0945 `"0945"', add
label define occ_lbl 0946 `"0946"', add
label define occ_lbl 0947 `"0947"', add
label define occ_lbl 0948 `"0948"', add
label define occ_lbl 0949 `"0949"', add
label define occ_lbl 0950 `"0950"', add
label define occ_lbl 0951 `"0951"', add
label define occ_lbl 0952 `"0952"', add
label define occ_lbl 0953 `"0953"', add
label define occ_lbl 0954 `"0954"', add
label define occ_lbl 0955 `"0955"', add
label define occ_lbl 0956 `"0956"', add
label define occ_lbl 0957 `"0957"', add
label define occ_lbl 0958 `"0958"', add
label define occ_lbl 0959 `"0959"', add
label define occ_lbl 0960 `"0960"', add
label define occ_lbl 0961 `"0961"', add
label define occ_lbl 0962 `"0962"', add
label define occ_lbl 0963 `"0963"', add
label define occ_lbl 0964 `"0964"', add
label define occ_lbl 0965 `"0965"', add
label define occ_lbl 0966 `"0966"', add
label define occ_lbl 0967 `"0967"', add
label define occ_lbl 0968 `"0968"', add
label define occ_lbl 0969 `"0969"', add
label define occ_lbl 0970 `"0970"', add
label define occ_lbl 0971 `"0971"', add
label define occ_lbl 0972 `"0972"', add
label define occ_lbl 0973 `"0973"', add
label define occ_lbl 0974 `"0974"', add
label define occ_lbl 0975 `"0975"', add
label define occ_lbl 0976 `"0976"', add
label define occ_lbl 0977 `"0977"', add
label define occ_lbl 0978 `"0978"', add
label define occ_lbl 0979 `"0979"', add
label define occ_lbl 0980 `"0980"', add
label define occ_lbl 0981 `"0981"', add
label define occ_lbl 0982 `"0982"', add
label define occ_lbl 0983 `"0983"', add
label define occ_lbl 0984 `"0984"', add
label define occ_lbl 0985 `"0985"', add
label define occ_lbl 0986 `"0986"', add
label define occ_lbl 0987 `"0987"', add
label define occ_lbl 0988 `"0988"', add
label define occ_lbl 0989 `"0989"', add
label define occ_lbl 0990 `"0990"', add
label define occ_lbl 0991 `"0991"', add
label define occ_lbl 0992 `"0992"', add
label define occ_lbl 0993 `"0993"', add
label define occ_lbl 0994 `"0994"', add
label define occ_lbl 0995 `"0995"', add
label define occ_lbl 0996 `"0996"', add
label define occ_lbl 0997 `"0997"', add
label define occ_lbl 0998 `"0998"', add
label define occ_lbl 0999 `"0999"', add
label values occ occ_lbl

label define occ2010_lbl 0010 `"Chief executives and legislators"'
label define occ2010_lbl 0020 `"General and Operations Managers"', add
label define occ2010_lbl 0040 `"Advertising and Promotions Managers"', add
label define occ2010_lbl 0050 `"Marketing and Sales Managers"', add
label define occ2010_lbl 0060 `"Public Relations and Fundraising Managers"', add
label define occ2010_lbl 0100 `"Administrative Services Managers"', add
label define occ2010_lbl 0110 `"Computer and Information Systems Managers"', add
label define occ2010_lbl 0120 `"Financial Managers"', add
label define occ2010_lbl 0135 `"Compensation and benefits managers"', add
label define occ2010_lbl 0136 `"Human Resources Managers"', add
label define occ2010_lbl 0137 `"Training and development managers"', add
label define occ2010_lbl 0140 `"Industrial Production Managers"', add
label define occ2010_lbl 0150 `"Purchasing Managers"', add
label define occ2010_lbl 0160 `"Transportation, Storage, and Distribution Managers"', add
label define occ2010_lbl 0205 `"Farmers, Ranchers, and Other Agricultural Managers"', add
label define occ2010_lbl 0220 `"Construction Managers"', add
label define occ2010_lbl 0230 `"Education Administrators"', add
label define occ2010_lbl 0300 `"Architectural and Engineering Managers"', add
label define occ2010_lbl 0310 `"Food Service Managers"', add
label define occ2010_lbl 0330 `"Gaming Managers"', add
label define occ2010_lbl 0340 `"Lodging Managers"', add
label define occ2010_lbl 0350 `"Medical and Health Services Managers"', add
label define occ2010_lbl 0360 `"Natural Sciences Managers"', add
label define occ2010_lbl 0410 `"Property, Real Estate, and Community Association Managers"', add
label define occ2010_lbl 0420 `"Social and Community Service Managers"', add
label define occ2010_lbl 0425 `"Emergency management directors"', add
label define occ2010_lbl 0430 `"Miscellaneous managers, including funeral service managers and postmasters and mail superintendents"', add
label define occ2010_lbl 0500 `"Agents and Business Managers of Artists, Performers, and Athletes"', add
label define occ2010_lbl 0510 `"Buyers and Purchasing Agents, Farm Products"', add
label define occ2010_lbl 0520 `"Wholesale and Retail Buyers, Except Farm Products"', add
label define occ2010_lbl 0530 `"Purchasing Agents, Except Wholesale, Retail, and Farm Products"', add
label define occ2010_lbl 0540 `"Claims Adjusters, Appraisers, Examiners, and Investigators"', add
label define occ2010_lbl 0565 `"Compliance Officers"', add
label define occ2010_lbl 0600 `"Cost Estimators"', add
label define occ2010_lbl 0630 `"Human Resources Workers"', add
label define occ2010_lbl 0640 `"Compensation, benefits, and job analysis specialists"', add
label define occ2010_lbl 0650 `"Training and development specialists"', add
label define occ2010_lbl 0700 `"Logisticians"', add
label define occ2010_lbl 0710 `"Management Analysts"', add
label define occ2010_lbl 0725 `"Meeting, Convention, and Event Planners"', add
label define occ2010_lbl 0726 `"Fundraisers"', add
label define occ2010_lbl 0735 `"Market Research Analysts and Marketing Specialists"', add
label define occ2010_lbl 0740 `"Business Operations Specialists, All Other"', add
label define occ2010_lbl 0800 `"Accountants and Auditors"', add
label define occ2010_lbl 0810 `"Appraisers and Assessors of Real Estate"', add
label define occ2010_lbl 0820 `"Budget Analysts"', add
label define occ2010_lbl 0830 `"Credit Analysts"', add
label define occ2010_lbl 0840 `"Financial Analysts"', add
label define occ2010_lbl 0850 `"Personal Financial Advisors"', add
label define occ2010_lbl 0860 `"Insurance Underwriters"', add
label define occ2010_lbl 0900 `"Financial Examiners"', add
label define occ2010_lbl 0910 `"Credit Counselors and Loan Officers"', add
label define occ2010_lbl 0930 `"Tax Examiners and Collectors, and Revenue Agents"', add
label define occ2010_lbl 0940 `"Tax Preparers"', add
label define occ2010_lbl 0950 `"Financial Specialists, All Other"', add
label define occ2010_lbl 1005 `"Computer and information research scientists"', add
label define occ2010_lbl 1006 `"Computer Systems Analysts"', add
label define occ2010_lbl 1007 `"Information security analysts"', add
label define occ2010_lbl 1010 `"Computer Programmers"', add
label define occ2010_lbl 1020 `"Software Developers, Applications and Systems Software"', add
label define occ2010_lbl 1030 `"Web Developers"', add
label define occ2010_lbl 1050 `"Computer Support Specialists"', add
label define occ2010_lbl 1060 `"Database Administrators"', add
label define occ2010_lbl 1105 `"Network and Computer Systems Administrators"', add
label define occ2010_lbl 1106 `"Computer network architects"', add
label define occ2010_lbl 1107 `"Computer occupations, all other"', add
label define occ2010_lbl 1200 `"Actuaries"', add
label define occ2010_lbl 1220 `"Operations Research Analysts"', add
label define occ2010_lbl 1240 `"Miscellaneous mathematical science occupations, including mathematicians and statisticians"', add
label define occ2010_lbl 1300 `"Architects, Except Naval"', add
label define occ2010_lbl 1310 `"Surveyors, Cartographers, and Photogrammetrists"', add
label define occ2010_lbl 1320 `"Aerospace Engineers"', add
label define occ2010_lbl 1340 `"Biomedical and agricultural engineers"', add
label define occ2010_lbl 1350 `"Chemical Engineers"', add
label define occ2010_lbl 1360 `"Civil Engineers"', add
label define occ2010_lbl 1400 `"Computer Hardware Engineers"', add
label define occ2010_lbl 1410 `"Electrical and Electronics Engineers"', add
label define occ2010_lbl 1420 `"Environmental Engineers"', add
label define occ2010_lbl 1430 `"Industrial Engineers, including Health and Safety"', add
label define occ2010_lbl 1440 `"Marine Engineers and Naval Architects"', add
label define occ2010_lbl 1450 `"Materials Engineers"', add
label define occ2010_lbl 1460 `"Mechanical Engineers"', add
label define occ2010_lbl 1520 `"Petroleum, mining and geological engineers, including mining safety engineers"', add
label define occ2010_lbl 1530 `"Miscellaneous engineers, including nuclear engineers"', add
label define occ2010_lbl 1540 `"Drafters"', add
label define occ2010_lbl 1550 `"Engineering Technicians, Except Drafters"', add
label define occ2010_lbl 1560 `"Surveying and Mapping Technicians"', add
label define occ2010_lbl 1600 `"Agricultural and Food Scientists"', add
label define occ2010_lbl 1610 `"Biological Scientists"', add
label define occ2010_lbl 1640 `"Conservation Scientists and Foresters"', add
label define occ2010_lbl 1650 `"Medical scientists, and life scientists, all other"', add
label define occ2010_lbl 1700 `"Astronomers and Physicists"', add
label define occ2010_lbl 1710 `"Atmospheric and Space Scientists"', add
label define occ2010_lbl 1720 `"Chemists and Materials Scientists"', add
label define occ2010_lbl 1740 `"Environmental Scientists and Geoscientists"', add
label define occ2010_lbl 1760 `"Physical Scientists, All Other"', add
label define occ2010_lbl 1800 `"Economists"', add
label define occ2010_lbl 1820 `"Psychologists"', add
label define occ2010_lbl 1840 `"Urban and Regional Planners"', add
label define occ2010_lbl 1860 `"Miscellaneous social scientists, including survey researchers and sociologists"', add
label define occ2010_lbl 1900 `"Agricultural and Food Science Technicians"', add
label define occ2010_lbl 1910 `"Biological Technicians"', add
label define occ2010_lbl 1920 `"Chemical Technicians"', add
label define occ2010_lbl 1930 `"Geological and petroleum technicians, and nuclear technicians"', add
label define occ2010_lbl 1965 `"Miscellaneous life, physical, and social science technicians, including social science research assistants"', add
label define occ2010_lbl 2000 `"Counselors"', add
label define occ2010_lbl 2010 `"Social Workers"', add
label define occ2010_lbl 2015 `"Probation officers and correctional treatment specialists"', add
label define occ2010_lbl 2016 `"Social and human service assistants"', add
label define occ2010_lbl 2025 `"Miscellaneous community and social service specialists, including health educators and community health workers"', add
label define occ2010_lbl 2040 `"Clergy"', add
label define occ2010_lbl 2050 `"Directors, Religious Activities and Education"', add
label define occ2010_lbl 2060 `"Religious Workers, All Other"', add
label define occ2010_lbl 2100 `"Lawyers, and judges, magistrates, and other judicial workers"', add
label define occ2010_lbl 2105 `"Judicial law clerks"', add
label define occ2010_lbl 2145 `"Paralegals and Legal Assistants"', add
label define occ2010_lbl 2160 `"Miscellaneous Legal Support Workers"', add
label define occ2010_lbl 2200 `"Postsecondary Teachers"', add
label define occ2010_lbl 2300 `"Preschool and Kindergarten Teachers"', add
label define occ2010_lbl 2310 `"Elementary and Middle School Teachers"', add
label define occ2010_lbl 2320 `"Secondary School Teachers"', add
label define occ2010_lbl 2330 `"Special Education Teachers"', add
label define occ2010_lbl 2340 `"Other Teachers and Instructors"', add
label define occ2010_lbl 2400 `"Archivists, Curators, and Museum Technicians"', add
label define occ2010_lbl 2430 `"Librarians"', add
label define occ2010_lbl 2440 `"Library Technicians"', add
label define occ2010_lbl 2540 `"Teacher Assistants"', add
label define occ2010_lbl 2550 `"Other Education, Training, and Library Workers"', add
label define occ2010_lbl 2600 `"Artists and Related Workers"', add
label define occ2010_lbl 2630 `"Designers"', add
label define occ2010_lbl 2700 `"Actors"', add
label define occ2010_lbl 2710 `"Producers and Directors"', add
label define occ2010_lbl 2720 `"Athletes, Coaches, Umpires, and Related Workers"', add
label define occ2010_lbl 2740 `"Dancers and Choreographers"', add
label define occ2010_lbl 2750 `"Musicians, Singers, and Related Workers"', add
label define occ2010_lbl 2760 `"Entertainers and Performers, Sports and Related Workers, All Other"', add
label define occ2010_lbl 2800 `"Announcers"', add
label define occ2010_lbl 2810 `"News Analysts, Reporters and Correspondents"', add
label define occ2010_lbl 2825 `"Public Relations Specialists"', add
label define occ2010_lbl 2830 `"Editors"', add
label define occ2010_lbl 2840 `"Technical Writers"', add
label define occ2010_lbl 2850 `"Writers and Authors"', add
label define occ2010_lbl 2860 `"Miscellaneous Media and Communication Workers"', add
label define occ2010_lbl 2900 `"Broadcast and sound engineering technicians and radio operators, and media and communication equipment workers, all other"', add
label define occ2010_lbl 2910 `"Photographers"', add
label define occ2010_lbl 2920 `"Television, Video, and Motion Picture Camera Operators and Editors"', add
label define occ2010_lbl 3000 `"Chiropractors"', add
label define occ2010_lbl 3010 `"Dentists"', add
label define occ2010_lbl 3030 `"Dietitians and Nutritionists"', add
label define occ2010_lbl 3040 `"Optometrists"', add
label define occ2010_lbl 3050 `"Pharmacists"', add
label define occ2010_lbl 3060 `"Physicians and Surgeons"', add
label define occ2010_lbl 3110 `"Physician Assistants"', add
label define occ2010_lbl 3120 `"Podiatrists"', add
label define occ2010_lbl 3140 `"Audiologists"', add
label define occ2010_lbl 3150 `"Occupational Therapists"', add
label define occ2010_lbl 3160 `"Physical Therapists"', add
label define occ2010_lbl 3200 `"Radiation Therapists"', add
label define occ2010_lbl 3210 `"Recreational Therapists"', add
label define occ2010_lbl 3220 `"Respiratory Therapists"', add
label define occ2010_lbl 3230 `"Speech-Language Pathologists"', add
label define occ2010_lbl 3245 `"Other therapists, including exercise physiologists"', add
label define occ2010_lbl 3250 `"Veterinarians"', add
label define occ2010_lbl 3255 `"Registered Nurses"', add
label define occ2010_lbl 3256 `"Nurse anesthetists"', add
label define occ2010_lbl 3258 `"Nurse practitioners and nurse midwives"', add
label define occ2010_lbl 3260 `"Health Diagnosing and Treating Practitioners, All Other"', add
label define occ2010_lbl 3300 `"Clinical Laboratory Technologists and Technicians"', add
label define occ2010_lbl 3310 `"Dental Hygienists"', add
label define occ2010_lbl 3320 `"Diagnostic Related Technologists and Technicians"', add
label define occ2010_lbl 3400 `"Emergency Medical Technicians and Paramedics"', add
label define occ2010_lbl 3420 `"Health Practitioner Support Technologists and  Technicians"', add
label define occ2010_lbl 3500 `"Licensed Practical and Licensed Vocational Nurses"', add
label define occ2010_lbl 3510 `"Medical Records and Health Information Technicians"', add
label define occ2010_lbl 3520 `"Opticians, Dispensing"', add
label define occ2010_lbl 3535 `"Miscellaneous Health Technologists and Technicians"', add
label define occ2010_lbl 3540 `"Other Healthcare Practitioners and Technical Occupations"', add
label define occ2010_lbl 3600 `"Nursing, Psychiatric, and Home Health Aides"', add
label define occ2010_lbl 3610 `"Occupational Therapy Assistants and Aides"', add
label define occ2010_lbl 3620 `"Physical Therapist Assistants and Aides"', add
label define occ2010_lbl 3630 `"Massage Therapists"', add
label define occ2010_lbl 3640 `"Dental Assistants"', add
label define occ2010_lbl 3645 `"Medical Assistants"', add
label define occ2010_lbl 3646 `"Medical transcriptionists"', add
label define occ2010_lbl 3647 `"Pharmacy aides"', add
label define occ2010_lbl 3648 `"Veterinary assistants and laboratory animal caretakers"', add
label define occ2010_lbl 3649 `"Phlebotomists"', add
label define occ2010_lbl 3655 `"Healthcare support workers, all other, including medical equipment preparers"', add
label define occ2010_lbl 3700 `"First-Line Supervisors of Correctional Officers"', add
label define occ2010_lbl 3710 `"First-Line Supervisors of Police and Detectives"', add
label define occ2010_lbl 3720 `"First-Line Supervisors of Fire Fighting and Prevention Workers"', add
label define occ2010_lbl 3730 `"First-Line Supervisors of Protective Service Workers, All Other"', add
label define occ2010_lbl 3740 `"Firefighters"', add
label define occ2010_lbl 3750 `"Fire Inspectors"', add
label define occ2010_lbl 3800 `"Bailiffs, Correctional Officers, and Jailers"', add
label define occ2010_lbl 3820 `"Detectives and Criminal Investigators"', add
label define occ2010_lbl 3840 `"Miscellaneous law enforcement workers"', add
label define occ2010_lbl 3850 `"Police officers"', add
label define occ2010_lbl 3900 `"Animal Control Workers"', add
label define occ2010_lbl 3910 `"Private Detectives and Investigators"', add
label define occ2010_lbl 3930 `"Security Guards and Gaming Surveillance Officers"', add
label define occ2010_lbl 3940 `"Crossing Guards"', add
label define occ2010_lbl 3945 `"Transportation security screeners"', add
label define occ2010_lbl 3955 `"Lifeguards and Other Recreational, and All Other Protective Service Workers"', add
label define occ2010_lbl 4000 `"Chefs and Head Cooks"', add
label define occ2010_lbl 4010 `"First-Line Supervisors of Food Preparation and Serving Workers"', add
label define occ2010_lbl 4020 `"Cooks"', add
label define occ2010_lbl 4030 `"Food Preparation Workers"', add
label define occ2010_lbl 4040 `"Bartenders"', add
label define occ2010_lbl 4050 `"Combined Food Preparation and Serving Workers, Including Fast Food"', add
label define occ2010_lbl 4060 `"Counter Attendants, Cafeteria, Food Concession, and Coffee Shop"', add
label define occ2010_lbl 4110 `"Waiters and Waitresses"', add
label define occ2010_lbl 4120 `"Food Servers, Nonrestaurant"', add
label define occ2010_lbl 4130 `"Miscellaneous food preparation and serving related workers, including dining room and cafeteria attendants and bartender helpers"', add
label define occ2010_lbl 4140 `"Dishwashers"', add
label define occ2010_lbl 4150 `"Hosts and Hostesses, Restaurant, Lounge, and Coffee Shop"', add
label define occ2010_lbl 4200 `"First-Line Supervisors of Housekeeping and Janitorial Workers"', add
label define occ2010_lbl 4210 `"First-Line Supervisors of Landscaping, Lawn Service, and Groundskeeping Workers"', add
label define occ2010_lbl 4220 `"Janitors and Building Cleaners"', add
label define occ2010_lbl 4230 `"Maids and housekeeping cleaners"', add
label define occ2010_lbl 4240 `"Pest Control Workers"', add
label define occ2010_lbl 4250 `"Grounds Maintenance Workers"', add
label define occ2010_lbl 4300 `"First-Line Supervisors of Gaming Workers"', add
label define occ2010_lbl 4320 `"First-Line Supervisors of Personal Service Workers"', add
label define occ2010_lbl 4340 `"Animal Trainers"', add
label define occ2010_lbl 4350 `"Nonfarm Animal Caretakers"', add
label define occ2010_lbl 4400 `"Gaming Services Workers"', add
label define occ2010_lbl 4410 `"Motion Picture Projectionists"', add
label define occ2010_lbl 4420 `"Ushers, Lobby Attendants, and Ticket Takers"', add
label define occ2010_lbl 4430 `"Miscellaneous Entertainment Attendants and Related Workers"', add
label define occ2010_lbl 4460 `"Embalmers and Funeral Attendants"', add
label define occ2010_lbl 4465 `"Morticians, undertakers, and funeral directors"', add
label define occ2010_lbl 4500 `"Barbers"', add
label define occ2010_lbl 4510 `"Hairdressers, Hairstylists, and Cosmetologists"', add
label define occ2010_lbl 4520 `"Miscellaneous Personal Appearance Workers"', add
label define occ2010_lbl 4530 `"Baggage Porters, Bellhops, and Concierges"', add
label define occ2010_lbl 4540 `"Tour and Travel Guides"', add
label define occ2010_lbl 4600 `"Childcare Workers"', add
label define occ2010_lbl 4610 `"Personal Care Aides"', add
label define occ2010_lbl 4620 `"Recreation and Fitness Workers"', add
label define occ2010_lbl 4640 `"Residential Advisors"', add
label define occ2010_lbl 4650 `"Personal Care and Service Workers, All Other"', add
label define occ2010_lbl 4700 `"First-Line Supervisors of Retail Sales Workers"', add
label define occ2010_lbl 4710 `"First-Line Supervisors of Non-Retail Sales Workers"', add
label define occ2010_lbl 4720 `"Cashiers"', add
label define occ2010_lbl 4740 `"Counter and Rental Clerks"', add
label define occ2010_lbl 4750 `"Parts Salespersons"', add
label define occ2010_lbl 4760 `"Retail Salespersons"', add
label define occ2010_lbl 4800 `"Advertising Sales Agents"', add
label define occ2010_lbl 4810 `"Insurance Sales Agents"', add
label define occ2010_lbl 4820 `"Securities, Commodities, and Financial Services Sales Agents"', add
label define occ2010_lbl 4830 `"Travel Agents"', add
label define occ2010_lbl 4840 `"Sales Representatives, Services, All Other"', add
label define occ2010_lbl 4850 `"Sales Representatives, Wholesale and Manufacturing"', add
label define occ2010_lbl 4900 `"Models, Demonstrators, and Product Promoters"', add
label define occ2010_lbl 4920 `"Real Estate Brokers and Sales Agents"', add
label define occ2010_lbl 4930 `"Sales Engineers"', add
label define occ2010_lbl 4940 `"Telemarketers"', add
label define occ2010_lbl 4950 `"Door-to-Door Sales Workers, News and Street Vendors, and Related Workers"', add
label define occ2010_lbl 4965 `"Sales and Related Workers, All Other"', add
label define occ2010_lbl 5000 `"First-Line Supervisors of Office and Administrative Support Workers"', add
label define occ2010_lbl 5010 `"Switchboard Operators, Including Answering Service"', add
label define occ2010_lbl 5020 `"Telephone Operators"', add
label define occ2010_lbl 5030 `"Communications Equipment Operators, All Other"', add
label define occ2010_lbl 5100 `"Bill and Account Collectors"', add
label define occ2010_lbl 5110 `"Billing and Posting Clerks"', add
label define occ2010_lbl 5120 `"Bookkeeping, Accounting, and Auditing Clerks"', add
label define occ2010_lbl 5130 `"Gaming Cage Workers"', add
label define occ2010_lbl 5140 `"Payroll and Timekeeping Clerks"', add
label define occ2010_lbl 5150 `"Procurement Clerks"', add
label define occ2010_lbl 5160 `"Tellers"', add
label define occ2010_lbl 5165 `"Financial clerks, all other"', add
label define occ2010_lbl 5200 `"Brokerage Clerks"', add
label define occ2010_lbl 5220 `"Court, Municipal, and License Clerks"', add
label define occ2010_lbl 5230 `"Credit Authorizers, Checkers, and Clerks"', add
label define occ2010_lbl 5240 `"Customer Service Representatives"', add
label define occ2010_lbl 5250 `"Eligibility Interviewers, Government Programs"', add
label define occ2010_lbl 5260 `"File Clerks"', add
label define occ2010_lbl 5300 `"Hotel, Motel, and Resort Desk Clerks"', add
label define occ2010_lbl 5310 `"Interviewers, Except Eligibility and Loan"', add
label define occ2010_lbl 5320 `"Library Assistants, Clerical"', add
label define occ2010_lbl 5330 `"Loan Interviewers and Clerks"', add
label define occ2010_lbl 5340 `"New Accounts Clerks"', add
label define occ2010_lbl 5350 `"Correspondence clerks and order clerks"', add
label define occ2010_lbl 5360 `"Human resources assistants, except payroll and timekeeping"', add
label define occ2010_lbl 5400 `"Receptionists and Information Clerks"', add
label define occ2010_lbl 5410 `"Reservation and Transportation Ticket Agents and Travel Clerks"', add
label define occ2010_lbl 5420 `"Information and Record Clerks, All Other"', add
label define occ2010_lbl 5500 `"Cargo and Freight Agents"', add
label define occ2010_lbl 5510 `"Couriers and Messengers"', add
label define occ2010_lbl 5520 `"Dispatchers"', add
label define occ2010_lbl 5530 `"Meter Readers, Utilities"', add
label define occ2010_lbl 5540 `"Postal Service Clerks"', add
label define occ2010_lbl 5550 `"Postal Service Mail Carriers"', add
label define occ2010_lbl 5560 `"Postal Service Mail Sorters, Processors, and Processing Machine Operators"', add
label define occ2010_lbl 5600 `"Production, Planning, and Expediting Clerks"', add
label define occ2010_lbl 5610 `"Shipping, Receiving, and Traffic Clerks"', add
label define occ2010_lbl 5620 `"Stock Clerks and Order Fillers"', add
label define occ2010_lbl 5630 `"Weighers, Measurers, Checkers, and Samplers, Recordkeeping"', add
label define occ2010_lbl 5700 `"Secretaries and Administrative Assistants"', add
label define occ2010_lbl 5800 `"Computer Operators"', add
label define occ2010_lbl 5810 `"Data Entry Keyers"', add
label define occ2010_lbl 5820 `"Word Processors and Typists"', add
label define occ2010_lbl 5840 `"Insurance Claims and Policy Processing Clerks"', add
label define occ2010_lbl 5850 `"Mail Clerks and Mail Machine Operators, Except Postal Service"', add
label define occ2010_lbl 5860 `"Office Clerks, General"', add
label define occ2010_lbl 5900 `"Office Machine Operators, Except Computer"', add
label define occ2010_lbl 5910 `"Proofreaders and Copy Markers"', add
label define occ2010_lbl 5920 `"Statistical Assistants"', add
label define occ2010_lbl 5940 `"Miscellaneous office and administrative support workers, including desktop publishers"', add
label define occ2010_lbl 6005 `"First-line supervisors of farming, fishing, and forestry workers"', add
label define occ2010_lbl 6010 `"Agricultural Inspectors"', add
label define occ2010_lbl 6040 `"Graders and Sorters, Agricultural Products"', add
label define occ2010_lbl 6050 `"Miscellaneous agricultural workers, including animal breeders"', add
label define occ2010_lbl 6100 `"Fishing and hunting workers"', add
label define occ2010_lbl 6120 `"Forest and Conservation Workers"', add
label define occ2010_lbl 6130 `"Logging Workers"', add
label define occ2010_lbl 6200 `"First-Line Supervisors of Construction Trades and Extraction Workers"', add
label define occ2010_lbl 6210 `"Boilermakers"', add
label define occ2010_lbl 6220 `"Brickmasons, blockmasons, stonemasons, and reinforcing iron and rebar workers"', add
label define occ2010_lbl 6230 `"Carpenters"', add
label define occ2010_lbl 6240 `"Carpet, Floor, and Tile Installers and Finishers"', add
label define occ2010_lbl 6250 `"Cement Masons, Concrete Finishers, and Terrazzo Workers"', add
label define occ2010_lbl 6260 `"Construction Laborers"', add
label define occ2010_lbl 6300 `"Paving, Surfacing, and Tamping Equipment Operators"', add
label define occ2010_lbl 6320 `"Construction equipment operators except paving, surfacing, and tamping equipment operators"', add
label define occ2010_lbl 6330 `"Drywall Installers, Ceiling Tile Installers, and Tapers"', add
label define occ2010_lbl 6355 `"Electricians"', add
label define occ2010_lbl 6360 `"Glaziers"', add
label define occ2010_lbl 6400 `"Insulation Workers"', add
label define occ2010_lbl 6420 `"Painters and paperhangers"', add
label define occ2010_lbl 6440 `"Pipelayers, Plumbers, Pipefitters, and Steamfitters"', add
label define occ2010_lbl 6460 `"Plasterers and Stucco Masons"', add
label define occ2010_lbl 6515 `"Roofers"', add
label define occ2010_lbl 6520 `"Sheet Metal Workers"', add
label define occ2010_lbl 6530 `"Structural Iron and Steel Workers"', add
label define occ2010_lbl 6600 `"Helpers, Construction Trades"', add
label define occ2010_lbl 6660 `"Construction and Building Inspectors"', add
label define occ2010_lbl 6700 `"Elevator Installers and Repairers"', add
label define occ2010_lbl 6710 `"Fence Erectors"', add
label define occ2010_lbl 6720 `"Hazardous Materials Removal Workers"', add
label define occ2010_lbl 6730 `"Highway Maintenance Workers"', add
label define occ2010_lbl 6740 `"Rail-Track Laying and Maintenance Equipment Operators"', add
label define occ2010_lbl 6765 `"Miscellaneous construction workers, including solar photovoltaic installers, septic tank servicers and sewer pipe cleaners"', add
label define occ2010_lbl 6800 `"Derrick, rotary drill, and service unit operators, and roustabouts, oil, gas, and mining"', add
label define occ2010_lbl 6820 `"Earth Drillers, Except Oil and Gas"', add
label define occ2010_lbl 6830 `"Explosives Workers, Ordnance Handling Experts, and Blasters"', add
label define occ2010_lbl 6840 `"Mining Machine Operators"', add
label define occ2010_lbl 6940 `"Miscellaneous extraction workers, including roof bolters and helpers"', add
label define occ2010_lbl 7000 `"First-Line Supervisors of Mechanics, Installers, and Repairers"', add
label define occ2010_lbl 7010 `"Computer, Automated Teller, and Office Machine Repairers"', add
label define occ2010_lbl 7020 `"Radio and Telecommunications Equipment Installers and Repairers"', add
label define occ2010_lbl 7030 `"Avionics Technicians"', add
label define occ2010_lbl 7040 `"Electric Motor, Power Tool, and Related Repairers"', add
label define occ2010_lbl 7100 `"Electrical and electronics repairers, transportation equipment, and industrial and utility"', add
label define occ2010_lbl 7110 `"Electronic Equipment Installers and Repairers, Motor Vehicles"', add
label define occ2010_lbl 7120 `"Electronic Home Entertainment Equipment Installers and Repairers"', add
label define occ2010_lbl 7130 `"Security and Fire Alarm Systems Installers"', add
label define occ2010_lbl 7140 `"Aircraft Mechanics and Service Technicians"', add
label define occ2010_lbl 7150 `"Automotive Body and Related Repairers"', add
label define occ2010_lbl 7160 `"Automotive Glass Installers and Repairers"', add
label define occ2010_lbl 7200 `"Automotive Service Technicians and Mechanics"', add
label define occ2010_lbl 7210 `"Bus and Truck Mechanics and Diesel Engine Specialists"', add
label define occ2010_lbl 7220 `"Heavy Vehicle and Mobile Equipment Service Technicians and Mechanics"', add
label define occ2010_lbl 7240 `"Small Engine Mechanics"', add
label define occ2010_lbl 7260 `"Miscellaneous Vehicle and Mobile Equipment Mechanics, Installers, and Repairers"', add
label define occ2010_lbl 7300 `"Control and Valve Installers and Repairers"', add
label define occ2010_lbl 7315 `"Heating, Air Conditioning, and Refrigeration Mechanics and Installers"', add
label define occ2010_lbl 7320 `"Home Appliance Repairers"', add
label define occ2010_lbl 7330 `"Industrial and Refractory Machinery Mechanics"', add
label define occ2010_lbl 7340 `"Maintenance and Repair Workers, General"', add
label define occ2010_lbl 7350 `"Maintenance Workers, Machinery"', add
label define occ2010_lbl 7360 `"Millwrights"', add
label define occ2010_lbl 7410 `"Electrical Power-Line Installers and Repairers"', add
label define occ2010_lbl 7420 `"Telecommunications Line Installers and Repairers"', add
label define occ2010_lbl 7430 `"Precision Instrument and Equipment Repairers"', add
label define occ2010_lbl 7510 `"Coin, Vending, and Amusement Machine Servicers and Repairers"', add
label define occ2010_lbl 7540 `"Locksmiths and Safe Repairers"', add
label define occ2010_lbl 7560 `"Riggers"', add
label define occ2010_lbl 7610 `"Helpers--Installation, Maintenance, and Repair Workers"', add
label define occ2010_lbl 7630 `"Miscellaneous installation, maintenance, and repair workers, including wind turbine service technicians"', add
label define occ2010_lbl 7700 `"First-Line Supervisors of Production and Operating Workers"', add
label define occ2010_lbl 7710 `"Aircraft Structure, Surfaces, Rigging, and Systems Assemblers"', add
label define occ2010_lbl 7720 `"Electrical, Electronics, and Electromechanical Assemblers"', add
label define occ2010_lbl 7730 `"Engine and Other Machine Assemblers"', add
label define occ2010_lbl 7740 `"Structural Metal Fabricators and Fitters"', add
label define occ2010_lbl 7750 `"Miscellaneous Assemblers and Fabricators"', add
label define occ2010_lbl 7800 `"Bakers"', add
label define occ2010_lbl 7810 `"Butchers and Other Meat, Poultry, and Fish Processing Workers"', add
label define occ2010_lbl 7830 `"Food and Tobacco Roasting, Baking, and Drying Machine Operators and Tenders"', add
label define occ2010_lbl 7840 `"Food Batchmakers"', add
label define occ2010_lbl 7850 `"Food Cooking Machine Operators and Tenders"', add
label define occ2010_lbl 7855 `"Food processing workers, all other"', add
label define occ2010_lbl 7900 `"Computer Control Programmers and Operators"', add
label define occ2010_lbl 7920 `"Extruding and Drawing Machine Setters, Operators, and Tenders, Metal and Plastic"', add
label define occ2010_lbl 7930 `"Forging Machine Setters, Operators, and Tenders, Metal and Plastic"', add
label define occ2010_lbl 7940 `"Rolling Machine Setters, Operators, and Tenders, Metal and Plastic"', add
label define occ2010_lbl 7950 `"Machine tool cutting setters, operators, and tenders, metal and plastic"', add
label define occ2010_lbl 8030 `"Machinists"', add
label define occ2010_lbl 8040 `"Metal Furnace Operators, Tenders, Pourers, and Casters"', add
label define occ2010_lbl 8100 `"Model makers, patternmakers, and molding machine setters, metal and plastic"', add
label define occ2010_lbl 8130 `"Tool and Die Makers"', add
label define occ2010_lbl 8140 `"Welding, Soldering, and Brazing Workers"', add
label define occ2010_lbl 8220 `"Miscellaneous metal workers and plastic workers, including multiple machine tool setters"', add
label define occ2010_lbl 8250 `"Prepress Technicians and Workers"', add
label define occ2010_lbl 8255 `"Printing Press Operators"', add
label define occ2010_lbl 8256 `"Print Binding and Finishing Workers"', add
label define occ2010_lbl 8300 `"Laundry and Dry-Cleaning Workers"', add
label define occ2010_lbl 8310 `"Pressers, Textile, Garment, and Related Materials"', add
label define occ2010_lbl 8320 `"Sewing Machine Operators"', add
label define occ2010_lbl 8330 `"Shoe and leather workers"', add
label define occ2010_lbl 8350 `"Tailors, Dressmakers, and Sewers"', add
label define occ2010_lbl 8400 `"Textile bleaching and dyeing, and cutting machine setters, operators, and tenders"', add
label define occ2010_lbl 8410 `"Textile Knitting and Weaving Machine Setters, Operators, and Tenders"', add
label define occ2010_lbl 8420 `"Textile Winding, Twisting, and Drawing Out Machine Setters, Operators, and Tenders"', add
label define occ2010_lbl 8450 `"Upholsterers"', add
label define occ2010_lbl 8460 `"Miscellaneous textile, apparel, and furnishings workers except upholsterers"', add
label define occ2010_lbl 8500 `"Cabinetmakers and Bench Carpenters"', add
label define occ2010_lbl 8510 `"Furniture Finishers"', add
label define occ2010_lbl 8530 `"Sawing Machine Setters, Operators, and Tenders, Wood"', add
label define occ2010_lbl 8540 `"Woodworking Machine Setters, Operators, and Tenders, Except Sawing"', add
label define occ2010_lbl 8550 `"Miscellaneous woodworkers, including model makers and patternmakers"', add
label define occ2010_lbl 8600 `"Power Plant Operators, Distributors, and Dispatchers"', add
label define occ2010_lbl 8610 `"Stationary Engineers and Boiler Operators"', add
label define occ2010_lbl 8620 `"Water and Wastewater Treatment Plant and System Operators"', add
label define occ2010_lbl 8630 `"Miscellaneous Plant and System Operators"', add
label define occ2010_lbl 8640 `"Chemical Processing Machine Setters, Operators, and Tenders"', add
label define occ2010_lbl 8650 `"Crushing, Grinding, Polishing, Mixing, and Blending Workers"', add
label define occ2010_lbl 8710 `"Cutting Workers"', add
label define occ2010_lbl 8720 `"Extruding, Forming, Pressing, and Compacting Machine Setters, Operators, and Tenders"', add
label define occ2010_lbl 8730 `"Furnace, Kiln, Oven, Drier, and Kettle Operators and Tenders"', add
label define occ2010_lbl 8740 `"Inspectors, Testers, Sorters, Samplers, and Weighers"', add
label define occ2010_lbl 8750 `"Jewelers and Precious Stone and Metal Workers"', add
label define occ2010_lbl 8760 `"Medical, Dental, and Ophthalmic Laboratory Technicians"', add
label define occ2010_lbl 8800 `"Packaging and Filling Machine Operators and Tenders"', add
label define occ2010_lbl 8810 `"Painting Workers"', add
label define occ2010_lbl 8830 `"Photographic Process Workers and Processing Machine Operators"', add
label define occ2010_lbl 8850 `"Adhesive Bonding Machine Operators and Tenders"', add
label define occ2010_lbl 8910 `"Etchers and Engravers"', add
label define occ2010_lbl 8920 `"Molders, Shapers, and Casters, Except Metal and Plastic"', add
label define occ2010_lbl 8930 `"Paper Goods Machine Setters, Operators, and Tenders"', add
label define occ2010_lbl 8940 `"Tire Builders"', add
label define occ2010_lbl 8950 `"Helpers--Production Workers"', add
label define occ2010_lbl 8965 `"Miscellaneous production workers, including semiconductor processors"', add
label define occ2010_lbl 9000 `"Supervisors of Transportation and Material Moving Workers"', add
label define occ2010_lbl 9030 `"Aircraft Pilots and Flight Engineers"', add
label define occ2010_lbl 9040 `"Air Traffic Controllers and Airfield Operations Specialists"', add
label define occ2010_lbl 9050 `"Flight Attendants"', add
label define occ2010_lbl 9110 `"Ambulance Drivers and Attendants, Except Emergency Medical Technicians"', add
label define occ2010_lbl 9120 `"Bus Drivers"', add
label define occ2010_lbl 9130 `"Driver/Sales Workers and Truck Drivers"', add
label define occ2010_lbl 9140 `"Taxi Drivers and Chauffeurs"', add
label define occ2010_lbl 9150 `"Motor Vehicle Operators, All Other"', add
label define occ2010_lbl 9200 `"Locomotive Engineers and Operators"', add
label define occ2010_lbl 9240 `"Railroad Conductors and Yardmasters"', add
label define occ2010_lbl 9260 `"Subway, streetcar, and other rail transportation workers"', add
label define occ2010_lbl 9300 `"Sailors and marine oilers, and ship engineers"', add
label define occ2010_lbl 9310 `"Ship and Boat Captains and Operators"', add
label define occ2010_lbl 9350 `"Parking Lot Attendants"', add
label define occ2010_lbl 9360 `"Automotive and Watercraft Service Attendants"', add
label define occ2010_lbl 9410 `"Transportation Inspectors"', add
label define occ2010_lbl 9415 `"Transportation attendants, except flight attendants"', add
label define occ2010_lbl 9420 `"Miscellaneous transportation workers, including bridge and lock tenders and traffic technicians"', add
label define occ2010_lbl 9510 `"Crane and Tower Operators"', add
label define occ2010_lbl 9520 `"Dredge, Excavating, and Loading Machine Operators"', add
label define occ2010_lbl 9560 `"Conveyor operators and tenders, and hoist and winch operators"', add
label define occ2010_lbl 9600 `"Industrial Truck and Tractor Operators"', add
label define occ2010_lbl 9610 `"Cleaners of Vehicles and Equipment"', add
label define occ2010_lbl 9620 `"Laborers and Freight, Stock, and Material Movers, Hand"', add
label define occ2010_lbl 9630 `"Machine Feeders and Offbearers"', add
label define occ2010_lbl 9640 `"Packers and Packagers, Hand"', add
label define occ2010_lbl 9650 `"Pumping Station Operators"', add
label define occ2010_lbl 9720 `"Refuse and Recyclable Material Collectors"', add
label define occ2010_lbl 9750 `"Miscellaneous material moving workers, including mine shuttle car operators, and tank car, truck, and ship loaders"', add
label define occ2010_lbl 9800 `"Military Officer Special and Tactical Operations Leaders"', add
label define occ2010_lbl 9810 `"First-Line Enlisted Military Supervisors"', add
label define occ2010_lbl 9820 `"Military Enlisted Tactical Operations and Air/Weapons Specialists and Crew Members"', add
label define occ2010_lbl 9830 `"Military, Rank Not Specified"', add
label define occ2010_lbl 9920 `"Unemployed, with No Work Experience in the Last 5 Years or Earlier or Never Worked"', add
label define occ2010_lbl 9999 `"NIU"', add
label values occ2010 occ2010_lbl

label define ind_lbl 0000 `"0000"'
label define ind_lbl 0001 `"0001"', add
label define ind_lbl 0002 `"0002"', add
label define ind_lbl 0003 `"0003"', add
label define ind_lbl 0004 `"0004"', add
label define ind_lbl 0005 `"0005"', add
label define ind_lbl 0006 `"0006"', add
label define ind_lbl 0007 `"0007"', add
label define ind_lbl 0008 `"0008"', add
label define ind_lbl 0009 `"0009"', add
label define ind_lbl 0010 `"0010"', add
label define ind_lbl 0011 `"0011"', add
label define ind_lbl 0012 `"0012"', add
label define ind_lbl 0013 `"0013"', add
label define ind_lbl 0014 `"0014"', add
label define ind_lbl 0015 `"0015"', add
label define ind_lbl 0016 `"0016"', add
label define ind_lbl 0017 `"0017"', add
label define ind_lbl 0018 `"0018"', add
label define ind_lbl 0019 `"0019"', add
label define ind_lbl 0020 `"0020"', add
label define ind_lbl 0021 `"0021"', add
label define ind_lbl 0022 `"0022"', add
label define ind_lbl 0023 `"0023"', add
label define ind_lbl 0024 `"0024"', add
label define ind_lbl 0025 `"0025"', add
label define ind_lbl 0026 `"0026"', add
label define ind_lbl 0027 `"0027"', add
label define ind_lbl 0028 `"0028"', add
label define ind_lbl 0029 `"0029"', add
label define ind_lbl 0030 `"0030"', add
label define ind_lbl 0031 `"0031"', add
label define ind_lbl 0032 `"0032"', add
label define ind_lbl 0033 `"0033"', add
label define ind_lbl 0034 `"0034"', add
label define ind_lbl 0035 `"0035"', add
label define ind_lbl 0036 `"0036"', add
label define ind_lbl 0037 `"0037"', add
label define ind_lbl 0038 `"0038"', add
label define ind_lbl 0039 `"0039"', add
label define ind_lbl 0040 `"0040"', add
label define ind_lbl 0041 `"0041"', add
label define ind_lbl 0042 `"0042"', add
label define ind_lbl 0043 `"0043"', add
label define ind_lbl 0044 `"0044"', add
label define ind_lbl 0045 `"0045"', add
label define ind_lbl 0046 `"0046"', add
label define ind_lbl 0047 `"0047"', add
label define ind_lbl 0048 `"0048"', add
label define ind_lbl 0049 `"0049"', add
label define ind_lbl 0050 `"0050"', add
label define ind_lbl 0051 `"0051"', add
label define ind_lbl 0052 `"0052"', add
label define ind_lbl 0053 `"0053"', add
label define ind_lbl 0054 `"0054"', add
label define ind_lbl 0055 `"0055"', add
label define ind_lbl 0056 `"0056"', add
label define ind_lbl 0057 `"0057"', add
label define ind_lbl 0058 `"0058"', add
label define ind_lbl 0059 `"0059"', add
label define ind_lbl 0060 `"0060"', add
label define ind_lbl 0061 `"0061"', add
label define ind_lbl 0062 `"0062"', add
label define ind_lbl 0063 `"0063"', add
label define ind_lbl 0064 `"0064"', add
label define ind_lbl 0065 `"0065"', add
label define ind_lbl 0066 `"0066"', add
label define ind_lbl 0067 `"0067"', add
label define ind_lbl 0068 `"0068"', add
label define ind_lbl 0069 `"0069"', add
label define ind_lbl 0070 `"0070"', add
label define ind_lbl 0071 `"0071"', add
label define ind_lbl 0072 `"0072"', add
label define ind_lbl 0073 `"0073"', add
label define ind_lbl 0074 `"0074"', add
label define ind_lbl 0075 `"0075"', add
label define ind_lbl 0076 `"0076"', add
label define ind_lbl 0077 `"0077"', add
label define ind_lbl 0078 `"0078"', add
label define ind_lbl 0079 `"0079"', add
label define ind_lbl 0080 `"0080"', add
label define ind_lbl 0081 `"0081"', add
label define ind_lbl 0082 `"0082"', add
label define ind_lbl 0083 `"0083"', add
label define ind_lbl 0084 `"0084"', add
label define ind_lbl 0085 `"0085"', add
label define ind_lbl 0086 `"0086"', add
label define ind_lbl 0087 `"0087"', add
label define ind_lbl 0088 `"0088"', add
label define ind_lbl 0089 `"0089"', add
label define ind_lbl 0090 `"0090"', add
label define ind_lbl 0091 `"0091"', add
label define ind_lbl 0092 `"0092"', add
label define ind_lbl 0093 `"0093"', add
label define ind_lbl 0094 `"0094"', add
label define ind_lbl 0095 `"0095"', add
label define ind_lbl 0096 `"0096"', add
label define ind_lbl 0097 `"0097"', add
label define ind_lbl 0098 `"0098"', add
label define ind_lbl 0099 `"0099"', add
label define ind_lbl 0100 `"0100"', add
label define ind_lbl 0101 `"0101"', add
label define ind_lbl 0102 `"0102"', add
label define ind_lbl 0103 `"0103"', add
label define ind_lbl 0104 `"0104"', add
label define ind_lbl 0105 `"0105"', add
label define ind_lbl 0106 `"0106"', add
label define ind_lbl 0107 `"0107"', add
label define ind_lbl 0108 `"0108"', add
label define ind_lbl 0109 `"0109"', add
label define ind_lbl 0110 `"0110"', add
label define ind_lbl 0111 `"0111"', add
label define ind_lbl 0112 `"0112"', add
label define ind_lbl 0113 `"0113"', add
label define ind_lbl 0114 `"0114"', add
label define ind_lbl 0115 `"0115"', add
label define ind_lbl 0116 `"0116"', add
label define ind_lbl 0117 `"0117"', add
label define ind_lbl 0118 `"0118"', add
label define ind_lbl 0119 `"0119"', add
label define ind_lbl 0120 `"0120"', add
label define ind_lbl 0121 `"0121"', add
label define ind_lbl 0122 `"0122"', add
label define ind_lbl 0123 `"0123"', add
label define ind_lbl 0124 `"0124"', add
label define ind_lbl 0125 `"0125"', add
label define ind_lbl 0126 `"0126"', add
label define ind_lbl 0127 `"0127"', add
label define ind_lbl 0128 `"0128"', add
label define ind_lbl 0129 `"0129"', add
label define ind_lbl 0130 `"0130"', add
label define ind_lbl 0131 `"0131"', add
label define ind_lbl 0137 `"0137"', add
label define ind_lbl 0138 `"0138"', add
label define ind_lbl 0139 `"0139"', add
label define ind_lbl 0146 `"0146"', add
label define ind_lbl 0147 `"0147"', add
label define ind_lbl 0148 `"0148"', add
label define ind_lbl 0149 `"0149"', add
label define ind_lbl 0157 `"0157"', add
label define ind_lbl 0158 `"0158"', add
label define ind_lbl 0159 `"0159"', add
label define ind_lbl 0166 `"0166"', add
label define ind_lbl 0167 `"0167"', add
label define ind_lbl 0168 `"0168"', add
label define ind_lbl 0169 `"0169"', add
label define ind_lbl 0176 `"0176"', add
label define ind_lbl 0177 `"0177"', add
label define ind_lbl 0178 `"0178"', add
label define ind_lbl 0179 `"0179"', add
label define ind_lbl 0186 `"0186"', add
label define ind_lbl 0187 `"0187"', add
label define ind_lbl 0188 `"0188"', add
label define ind_lbl 0197 `"0197"', add
label define ind_lbl 0198 `"0198"', add
label define ind_lbl 0199 `"0199"', add
label define ind_lbl 0206 `"0206"', add
label define ind_lbl 0207 `"0207"', add
label define ind_lbl 0208 `"0208"', add
label define ind_lbl 0209 `"0209"', add
label define ind_lbl 0219 `"0219"', add
label define ind_lbl 0227 `"0227"', add
label define ind_lbl 0228 `"0228"', add
label define ind_lbl 0229 `"0229"', add
label define ind_lbl 0236 `"0236"', add
label define ind_lbl 0237 `"0237"', add
label define ind_lbl 0238 `"0238"', add
label define ind_lbl 0239 `"0239"', add
label define ind_lbl 0246 `"0246"', add
label define ind_lbl 0247 `"0247"', add
label define ind_lbl 0248 `"0248"', add
label define ind_lbl 0249 `"0249"', add
label define ind_lbl 0257 `"0257"', add
label define ind_lbl 0258 `"0258"', add
label define ind_lbl 0259 `"0259"', add
label define ind_lbl 0267 `"0267"', add
label define ind_lbl 0268 `"0268"', add
label define ind_lbl 0269 `"0269"', add
label define ind_lbl 0278 `"0278"', add
label define ind_lbl 0279 `"0279"', add
label define ind_lbl 0287 `"0287"', add
label define ind_lbl 0288 `"0288"', add
label define ind_lbl 0289 `"0289"', add
label define ind_lbl 0293 `"0293"', add
label define ind_lbl 0297 `"0297"', add
label define ind_lbl 0298 `"0298"', add
label define ind_lbl 0299 `"0299"', add
label define ind_lbl 0307 `"0307"', add
label define ind_lbl 0308 `"0308"', add
label define ind_lbl 0309 `"0309"', add
label define ind_lbl 0317 `"0317"', add
label define ind_lbl 0318 `"0318"', add
label define ind_lbl 0319 `"0319"', add
label define ind_lbl 0327 `"0327"', add
label define ind_lbl 0328 `"0328"', add
label define ind_lbl 0329 `"0329"', add
label define ind_lbl 0337 `"0337"', add
label define ind_lbl 0338 `"0338"', add
label define ind_lbl 0339 `"0339"', add
label define ind_lbl 0346 `"0346"', add
label define ind_lbl 0347 `"0347"', add
label define ind_lbl 0348 `"0348"', add
label define ind_lbl 0349 `"0349"', add
label define ind_lbl 0357 `"0357"', add
label define ind_lbl 0358 `"0358"', add
label define ind_lbl 0359 `"0359"', add
label define ind_lbl 0367 `"0367"', add
label define ind_lbl 0368 `"0368"', add
label define ind_lbl 0369 `"0369"', add
label define ind_lbl 0377 `"0377"', add
label define ind_lbl 0378 `"0378"', add
label define ind_lbl 0379 `"0379"', add
label define ind_lbl 0387 `"0387"', add
label define ind_lbl 0388 `"0388"', add
label define ind_lbl 0389 `"0389"', add
label define ind_lbl 0397 `"0397"', add
label define ind_lbl 0398 `"0398"', add
label define ind_lbl 0399 `"0399"', add
label define ind_lbl 0407 `"0407"', add
label define ind_lbl 0408 `"0408"', add
label define ind_lbl 0409 `"0409"', add
label define ind_lbl 0417 `"0417"', add
label define ind_lbl 0418 `"0418"', add
label define ind_lbl 0419 `"0419"', add
label define ind_lbl 0427 `"0427"', add
label define ind_lbl 0428 `"0428"', add
label define ind_lbl 0429 `"0429"', add
label define ind_lbl 0447 `"0447"', add
label define ind_lbl 0448 `"0448"', add
label define ind_lbl 0449 `"0449"', add
label define ind_lbl 0467 `"0467"', add
label define ind_lbl 0468 `"0468"', add
label define ind_lbl 0469 `"0469"', add
label define ind_lbl 0477 `"0477"', add
label define ind_lbl 0478 `"0478"', add
label define ind_lbl 0479 `"0479"', add
label define ind_lbl 0499 `"0499"', add
label define ind_lbl 0507 `"0507"', add
label define ind_lbl 0508 `"0508"', add
label define ind_lbl 0509 `"0509"', add
label define ind_lbl 0527 `"0527"', add
label define ind_lbl 0528 `"0528"', add
label define ind_lbl 0529 `"0529"', add
label define ind_lbl 0536 `"0536"', add
label define ind_lbl 0537 `"0537"', add
label define ind_lbl 0538 `"0538"', add
label define ind_lbl 0539 `"0539"', add
label define ind_lbl 0557 `"0557"', add
label define ind_lbl 0558 `"0558"', add
label define ind_lbl 0559 `"0559"', add
label define ind_lbl 0566 `"0566"', add
label define ind_lbl 0567 `"0567"', add
label define ind_lbl 0568 `"0568"', add
label define ind_lbl 0569 `"0569"', add
label define ind_lbl 0587 `"0587"', add
label define ind_lbl 0588 `"0588"', add
label define ind_lbl 0599 `"0599"', add
label define ind_lbl 0607 `"0607"', add
label define ind_lbl 0608 `"0608"', add
label define ind_lbl 0609 `"0609"', add
label define ind_lbl 0617 `"0617"', add
label define ind_lbl 0618 `"0618"', add
label define ind_lbl 0619 `"0619"', add
label define ind_lbl 0626 `"0626"', add
label define ind_lbl 0627 `"0627"', add
label define ind_lbl 0628 `"0628"', add
label define ind_lbl 0629 `"0629"', add
label define ind_lbl 0636 `"0636"', add
label define ind_lbl 0637 `"0637"', add
label define ind_lbl 0638 `"0638"', add
label define ind_lbl 0639 `"0639"', add
label define ind_lbl 0646 `"0646"', add
label define ind_lbl 0647 `"0647"', add
label define ind_lbl 0648 `"0648"', add
label define ind_lbl 0649 `"0649"', add
label define ind_lbl 0657 `"0657"', add
label define ind_lbl 0658 `"0658"', add
label define ind_lbl 0667 `"0667"', add
label define ind_lbl 0668 `"0668"', add
label define ind_lbl 0669 `"0669"', add
label define ind_lbl 0676 `"0676"', add
label define ind_lbl 0677 `"0677"', add
label define ind_lbl 0678 `"0678"', add
label define ind_lbl 0679 `"0679"', add
label define ind_lbl 0687 `"0687"', add
label define ind_lbl 0688 `"0688"', add
label define ind_lbl 0689 `"0689"', add
label define ind_lbl 0696 `"0696"', add
label define ind_lbl 0697 `"0697"', add
label define ind_lbl 0698 `"0698"', add
label define ind_lbl 0699 `"0699"', add
label define ind_lbl 0706 `"0706"', add
label define ind_lbl 0707 `"0707"', add
label define ind_lbl 0708 `"0708"', add
label define ind_lbl 0709 `"0709"', add
label define ind_lbl 0717 `"0717"', add
label define ind_lbl 0718 `"0718"', add
label define ind_lbl 0719 `"0719"', add
label define ind_lbl 0727 `"0727"', add
label define ind_lbl 0728 `"0728"', add
label define ind_lbl 0729 `"0729"', add
label define ind_lbl 0736 `"0736"', add
label define ind_lbl 0737 `"0737"', add
label define ind_lbl 0738 `"0738"', add
label define ind_lbl 0739 `"0739"', add
label define ind_lbl 0747 `"0747"', add
label define ind_lbl 0748 `"0748"', add
label define ind_lbl 0749 `"0749"', add
label define ind_lbl 0756 `"0756"', add
label define ind_lbl 0757 `"0757"', add
label define ind_lbl 0758 `"0758"', add
label define ind_lbl 0759 `"0759"', add
label define ind_lbl 0766 `"0766"', add
label define ind_lbl 0767 `"0767"', add
label define ind_lbl 0769 `"0769"', add
label define ind_lbl 0776 `"0776"', add
label define ind_lbl 0777 `"0777"', add
label define ind_lbl 0778 `"0778"', add
label define ind_lbl 0779 `"0779"', add
label define ind_lbl 0786 `"0786"', add
label define ind_lbl 0787 `"0787"', add
label define ind_lbl 0788 `"0788"', add
label define ind_lbl 0789 `"0789"', add
label define ind_lbl 0797 `"0797"', add
label define ind_lbl 0798 `"0798"', add
label define ind_lbl 0799 `"0799"', add
label define ind_lbl 0807 `"0807"', add
label define ind_lbl 0808 `"0808"', add
label define ind_lbl 0809 `"0809"', add
label define ind_lbl 0817 `"0817"', add
label define ind_lbl 0826 `"0826"', add
label define ind_lbl 0828 `"0828"', add
label define ind_lbl 0829 `"0829"', add
label define ind_lbl 0837 `"0837"', add
label define ind_lbl 0838 `"0838"', add
label define ind_lbl 0839 `"0839"', add
label define ind_lbl 0847 `"0847"', add
label define ind_lbl 0848 `"0848"', add
label define ind_lbl 0849 `"0849"', add
label define ind_lbl 0856 `"0856"', add
label define ind_lbl 0857 `"0857"', add
label define ind_lbl 0858 `"0858"', add
label define ind_lbl 0859 `"0859"', add
label define ind_lbl 0867 `"0867"', add
label define ind_lbl 0868 `"0868"', add
label define ind_lbl 0869 `"0869"', add
label define ind_lbl 0876 `"0876"', add
label define ind_lbl 0877 `"0877"', add
label define ind_lbl 0878 `"0878"', add
label define ind_lbl 0879 `"0879"', add
label define ind_lbl 0887 `"0887"', add
label define ind_lbl 0888 `"0888"', add
label define ind_lbl 0889 `"0889"', add
label define ind_lbl 0897 `"0897"', add
label define ind_lbl 0899 `"0899"', add
label define ind_lbl 0907 `"0907"', add
label define ind_lbl 0917 `"0917"', add
label define ind_lbl 0927 `"0927"', add
label define ind_lbl 0937 `"0937"', add
label define ind_lbl 0947 `"0947"', add
label define ind_lbl 0995 `"0995"', add
label define ind_lbl 0996 `"0996"', add
label define ind_lbl 0997 `"0997"', add
label define ind_lbl 0998 `"0998"', add
label define ind_lbl 0999 `"0999"', add
label values ind ind_lbl

label define wkswork2_lbl 0 `"N/A"'
label define wkswork2_lbl 1 `"1-13 weeks"', add
label define wkswork2_lbl 2 `"14-26 weeks"', add
label define wkswork2_lbl 3 `"27-39 weeks"', add
label define wkswork2_lbl 4 `"40-47 weeks"', add
label define wkswork2_lbl 5 `"48-49 weeks"', add
label define wkswork2_lbl 6 `"50-52 weeks"', add
label values wkswork2 wkswork2_lbl

label define uhrswork_lbl 00 `"N/A"'
label define uhrswork_lbl 01 `"1"', add
label define uhrswork_lbl 02 `"2"', add
label define uhrswork_lbl 03 `"3"', add
label define uhrswork_lbl 04 `"4"', add
label define uhrswork_lbl 05 `"5"', add
label define uhrswork_lbl 06 `"6"', add
label define uhrswork_lbl 07 `"7"', add
label define uhrswork_lbl 08 `"8"', add
label define uhrswork_lbl 09 `"9"', add
label define uhrswork_lbl 10 `"10"', add
label define uhrswork_lbl 11 `"11"', add
label define uhrswork_lbl 12 `"12"', add
label define uhrswork_lbl 13 `"13"', add
label define uhrswork_lbl 14 `"14"', add
label define uhrswork_lbl 15 `"15"', add
label define uhrswork_lbl 16 `"16"', add
label define uhrswork_lbl 17 `"17"', add
label define uhrswork_lbl 18 `"18"', add
label define uhrswork_lbl 19 `"19"', add
label define uhrswork_lbl 20 `"20"', add
label define uhrswork_lbl 21 `"21"', add
label define uhrswork_lbl 22 `"22"', add
label define uhrswork_lbl 23 `"23"', add
label define uhrswork_lbl 24 `"24"', add
label define uhrswork_lbl 25 `"25"', add
label define uhrswork_lbl 26 `"26"', add
label define uhrswork_lbl 27 `"27"', add
label define uhrswork_lbl 28 `"28"', add
label define uhrswork_lbl 29 `"29"', add
label define uhrswork_lbl 30 `"30"', add
label define uhrswork_lbl 31 `"31"', add
label define uhrswork_lbl 32 `"32"', add
label define uhrswork_lbl 33 `"33"', add
label define uhrswork_lbl 34 `"34"', add
label define uhrswork_lbl 35 `"35"', add
label define uhrswork_lbl 36 `"36"', add
label define uhrswork_lbl 37 `"37"', add
label define uhrswork_lbl 38 `"38"', add
label define uhrswork_lbl 39 `"39"', add
label define uhrswork_lbl 40 `"40"', add
label define uhrswork_lbl 41 `"41"', add
label define uhrswork_lbl 42 `"42"', add
label define uhrswork_lbl 43 `"43"', add
label define uhrswork_lbl 44 `"44"', add
label define uhrswork_lbl 45 `"45"', add
label define uhrswork_lbl 46 `"46"', add
label define uhrswork_lbl 47 `"47"', add
label define uhrswork_lbl 48 `"48"', add
label define uhrswork_lbl 49 `"49"', add
label define uhrswork_lbl 50 `"50"', add
label define uhrswork_lbl 51 `"51"', add
label define uhrswork_lbl 52 `"52"', add
label define uhrswork_lbl 53 `"53"', add
label define uhrswork_lbl 54 `"54"', add
label define uhrswork_lbl 55 `"55"', add
label define uhrswork_lbl 56 `"56"', add
label define uhrswork_lbl 57 `"57"', add
label define uhrswork_lbl 58 `"58"', add
label define uhrswork_lbl 59 `"59"', add
label define uhrswork_lbl 60 `"60"', add
label define uhrswork_lbl 61 `"61"', add
label define uhrswork_lbl 62 `"62"', add
label define uhrswork_lbl 63 `"63"', add
label define uhrswork_lbl 64 `"64"', add
label define uhrswork_lbl 65 `"65"', add
label define uhrswork_lbl 66 `"66"', add
label define uhrswork_lbl 67 `"67"', add
label define uhrswork_lbl 68 `"68"', add
label define uhrswork_lbl 69 `"69"', add
label define uhrswork_lbl 70 `"70"', add
label define uhrswork_lbl 71 `"71"', add
label define uhrswork_lbl 72 `"72"', add
label define uhrswork_lbl 73 `"73"', add
label define uhrswork_lbl 74 `"74"', add
label define uhrswork_lbl 75 `"75"', add
label define uhrswork_lbl 76 `"76"', add
label define uhrswork_lbl 77 `"77"', add
label define uhrswork_lbl 78 `"78"', add
label define uhrswork_lbl 79 `"79"', add
label define uhrswork_lbl 80 `"80"', add
label define uhrswork_lbl 81 `"81"', add
label define uhrswork_lbl 82 `"82"', add
label define uhrswork_lbl 83 `"83"', add
label define uhrswork_lbl 84 `"84"', add
label define uhrswork_lbl 85 `"85"', add
label define uhrswork_lbl 86 `"86"', add
label define uhrswork_lbl 87 `"87"', add
label define uhrswork_lbl 88 `"88"', add
label define uhrswork_lbl 89 `"89"', add
label define uhrswork_lbl 90 `"90"', add
label define uhrswork_lbl 91 `"91"', add
label define uhrswork_lbl 92 `"92"', add
label define uhrswork_lbl 93 `"93"', add
label define uhrswork_lbl 94 `"94"', add
label define uhrswork_lbl 95 `"95"', add
label define uhrswork_lbl 96 `"96"', add
label define uhrswork_lbl 97 `"97"', add
label define uhrswork_lbl 98 `"98"', add
label define uhrswork_lbl 99 `"99 (Topcode)"', add
label values uhrswork uhrswork_lbl

label define wrklstwk_lbl 0 `"N/A"'
label define wrklstwk_lbl 1 `"Did not work"', add
label define wrklstwk_lbl 2 `"Worked"', add
label define wrklstwk_lbl 3 `"Not Reported"', add
label values wrklstwk wrklstwk_lbl

label define absent_lbl 0 `"N/A"'
label define absent_lbl 1 `"No"', add
label define absent_lbl 2 `"Yes, laid off"', add
label define absent_lbl 3 `"Yes, other reason (vacation, illness, labor dispute, etc.)"', add
label define absent_lbl 4 `"Not reported"', add
label values absent absent_lbl

label define looking_lbl 0 `"N/A"'
label define looking_lbl 1 `"No, did not look for work"', add
label define looking_lbl 2 `"Yes, looked for work"', add
label define looking_lbl 3 `"Not reported"', add
label values looking looking_lbl

label define availble_lbl 0 `"N/A"'
label define availble_lbl 1 `"No, already has job"', add
label define availble_lbl 2 `"No, temporarily ill"', add
label define availble_lbl 3 `"No, other reason(s)"', add
label define availble_lbl 4 `"Yes, available for work"', add
label define availble_lbl 5 `"Not reported"', add
label values availble availble_lbl

label define wrkrecal_lbl 0 `"N/A"'
label define wrkrecal_lbl 1 `"No"', add
label define wrkrecal_lbl 2 `"Yes"', add
label define wrkrecal_lbl 3 `"Not reported"', add
label values wrkrecal wrkrecal_lbl

label define workedyr_lbl 0 `"N/A"'
label define workedyr_lbl 1 `"No"', add
label define workedyr_lbl 2 `"No, but worked 1-5 years ago (ACS only)"', add
label define workedyr_lbl 3 `"Yes"', add
label values workedyr workedyr_lbl

label define incwage_lbl 000000 `"000000"'
label define incwage_lbl 000100 `"000100"', add
label define incwage_lbl 000200 `"000200"', add
label define incwage_lbl 000300 `"000300"', add
label define incwage_lbl 000400 `"000400"', add
label define incwage_lbl 000500 `"000500"', add
label define incwage_lbl 000600 `"000600"', add
label define incwage_lbl 000700 `"000700"', add
label define incwage_lbl 000800 `"000800"', add
label define incwage_lbl 000900 `"000900"', add
label define incwage_lbl 001000 `"001000"', add
label define incwage_lbl 001100 `"001100"', add
label define incwage_lbl 001200 `"001200"', add
label define incwage_lbl 001300 `"001300"', add
label define incwage_lbl 001400 `"001400"', add
label define incwage_lbl 001500 `"001500"', add
label define incwage_lbl 001600 `"001600"', add
label define incwage_lbl 001700 `"001700"', add
label define incwage_lbl 001800 `"001800"', add
label define incwage_lbl 001900 `"001900"', add
label define incwage_lbl 002000 `"002000"', add
label define incwage_lbl 002100 `"002100"', add
label define incwage_lbl 002200 `"002200"', add
label define incwage_lbl 002300 `"002300"', add
label define incwage_lbl 002400 `"002400"', add
label define incwage_lbl 002500 `"002500"', add
label define incwage_lbl 002600 `"002600"', add
label define incwage_lbl 002700 `"002700"', add
label define incwage_lbl 002800 `"002800"', add
label define incwage_lbl 002900 `"002900"', add
label define incwage_lbl 003000 `"003000"', add
label define incwage_lbl 003100 `"003100"', add
label define incwage_lbl 003200 `"003200"', add
label define incwage_lbl 003300 `"003300"', add
label define incwage_lbl 003400 `"003400"', add
label define incwage_lbl 003500 `"003500"', add
label define incwage_lbl 003600 `"003600"', add
label define incwage_lbl 003700 `"003700"', add
label define incwage_lbl 003800 `"003800"', add
label define incwage_lbl 003900 `"003900"', add
label define incwage_lbl 004000 `"004000"', add
label define incwage_lbl 004100 `"004100"', add
label define incwage_lbl 004200 `"004200"', add
label define incwage_lbl 004300 `"004300"', add
label define incwage_lbl 004400 `"004400"', add
label define incwage_lbl 004500 `"004500"', add
label define incwage_lbl 004600 `"004600"', add
label define incwage_lbl 004700 `"004700"', add
label define incwage_lbl 004800 `"004800"', add
label define incwage_lbl 004900 `"004900"', add
label define incwage_lbl 005000 `"005000"', add
label define incwage_lbl 005100 `"005100"', add
label define incwage_lbl 005200 `"005200"', add
label define incwage_lbl 005300 `"005300"', add
label define incwage_lbl 005400 `"005400"', add
label define incwage_lbl 005500 `"005500"', add
label define incwage_lbl 005600 `"005600"', add
label define incwage_lbl 005700 `"005700"', add
label define incwage_lbl 005800 `"005800"', add
label define incwage_lbl 005900 `"005900"', add
label define incwage_lbl 006000 `"006000"', add
label define incwage_lbl 006100 `"006100"', add
label define incwage_lbl 006200 `"006200"', add
label define incwage_lbl 006300 `"006300"', add
label define incwage_lbl 006400 `"006400"', add
label define incwage_lbl 006500 `"006500"', add
label define incwage_lbl 006600 `"006600"', add
label define incwage_lbl 006700 `"006700"', add
label define incwage_lbl 006800 `"006800"', add
label define incwage_lbl 006900 `"006900"', add
label define incwage_lbl 007000 `"007000"', add
label define incwage_lbl 007100 `"007100"', add
label define incwage_lbl 007200 `"007200"', add
label define incwage_lbl 007300 `"007300"', add
label define incwage_lbl 007400 `"007400"', add
label define incwage_lbl 007500 `"007500"', add
label define incwage_lbl 007600 `"007600"', add
label define incwage_lbl 007700 `"007700"', add
label define incwage_lbl 007800 `"007800"', add
label define incwage_lbl 007900 `"007900"', add
label define incwage_lbl 008000 `"008000"', add
label define incwage_lbl 008100 `"008100"', add
label define incwage_lbl 008200 `"008200"', add
label define incwage_lbl 008300 `"008300"', add
label define incwage_lbl 008400 `"008400"', add
label define incwage_lbl 008500 `"008500"', add
label define incwage_lbl 008600 `"008600"', add
label define incwage_lbl 008700 `"008700"', add
label define incwage_lbl 008800 `"008800"', add
label define incwage_lbl 008900 `"008900"', add
label define incwage_lbl 009000 `"009000"', add
label define incwage_lbl 009100 `"009100"', add
label define incwage_lbl 009200 `"009200"', add
label define incwage_lbl 009300 `"009300"', add
label define incwage_lbl 009400 `"009400"', add
label define incwage_lbl 009500 `"009500"', add
label define incwage_lbl 009600 `"009600"', add
label define incwage_lbl 009700 `"009700"', add
label define incwage_lbl 009800 `"009800"', add
label define incwage_lbl 009900 `"009900"', add
label define incwage_lbl 010000 `"010000"', add
label define incwage_lbl 999998 `"Missing"', add
label define incwage_lbl 999999 `"N/A"', add
label values incwage incwage_lbl

label define incbus00_lbl 999999 `"NIU"'
label define incbus00_lbl 999998 `"$1 or break even (2000, 2005-2007 ACS)"', add
label values incbus00 incbus00_lbl

label define incwelfr_lbl 99999 `"NIU"'
label define incwelfr_lbl 99998 `"99998"', add
label define incwelfr_lbl 00000 `"00000"', add
label values incwelfr incwelfr_lbl

label define incinvst_lbl 999999 `"N/A"'
label define incinvst_lbl 999998 `"999998"', add
label values incinvst incinvst_lbl

label define incretir_lbl 999999 `"NIU"'
label values incretir incretir_lbl

label define incsupp_lbl 99998 `"99998"'
label define incsupp_lbl 99999 `"NIU"', add
label values incsupp incsupp_lbl

label define incother_lbl -9900 `"-9900"'
label define incother_lbl -0050 `"-0050"', add
label define incother_lbl -0001 `"Net Loss (1950)"', add
label define incother_lbl 00000 `"00000"', add
label define incother_lbl 00100 `"00100"', add
label define incother_lbl 00200 `"00200"', add
label define incother_lbl 00300 `"00300"', add
label define incother_lbl 00400 `"00400"', add
label define incother_lbl 00500 `"00500"', add
label define incother_lbl 00600 `"00600"', add
label define incother_lbl 00700 `"00700"', add
label define incother_lbl 00800 `"00800"', add
label define incother_lbl 00900 `"00900"', add
label define incother_lbl 01000 `"01000"', add
label define incother_lbl 01100 `"01100"', add
label define incother_lbl 01200 `"01200"', add
label define incother_lbl 01300 `"01300"', add
label define incother_lbl 01400 `"01400"', add
label define incother_lbl 01500 `"01500"', add
label define incother_lbl 01600 `"01600"', add
label define incother_lbl 01700 `"01700"', add
label define incother_lbl 01800 `"01800"', add
label define incother_lbl 01900 `"01900"', add
label define incother_lbl 02000 `"02000"', add
label define incother_lbl 02100 `"02100"', add
label define incother_lbl 02200 `"02200"', add
label define incother_lbl 02300 `"02300"', add
label define incother_lbl 02400 `"02400"', add
label define incother_lbl 02500 `"02500"', add
label define incother_lbl 02600 `"02600"', add
label define incother_lbl 02700 `"02700"', add
label define incother_lbl 02800 `"02800"', add
label define incother_lbl 02900 `"02900"', add
label define incother_lbl 03000 `"03000"', add
label define incother_lbl 03100 `"03100"', add
label define incother_lbl 03200 `"03200"', add
label define incother_lbl 03300 `"03300"', add
label define incother_lbl 03400 `"03400"', add
label define incother_lbl 03500 `"03500"', add
label define incother_lbl 03600 `"03600"', add
label define incother_lbl 03700 `"03700"', add
label define incother_lbl 03800 `"03800"', add
label define incother_lbl 03900 `"03900"', add
label define incother_lbl 04000 `"04000"', add
label define incother_lbl 04100 `"04100"', add
label define incother_lbl 04200 `"04200"', add
label define incother_lbl 04300 `"04300"', add
label define incother_lbl 04400 `"04400"', add
label define incother_lbl 04500 `"04500"', add
label define incother_lbl 04600 `"04600"', add
label define incother_lbl 04700 `"04700"', add
label define incother_lbl 04800 `"04800"', add
label define incother_lbl 04900 `"04900"', add
label define incother_lbl 05000 `"05000"', add
label define incother_lbl 05100 `"05100"', add
label define incother_lbl 05200 `"05200"', add
label define incother_lbl 05300 `"05300"', add
label define incother_lbl 05400 `"05400"', add
label define incother_lbl 05500 `"05500"', add
label define incother_lbl 05600 `"05600"', add
label define incother_lbl 05700 `"05700"', add
label define incother_lbl 05800 `"05800"', add
label define incother_lbl 05900 `"05900"', add
label define incother_lbl 06000 `"06000"', add
label define incother_lbl 06100 `"06100"', add
label define incother_lbl 06200 `"06200"', add
label define incother_lbl 06300 `"06300"', add
label define incother_lbl 06400 `"06400"', add
label define incother_lbl 06500 `"06500"', add
label define incother_lbl 06600 `"06600"', add
label define incother_lbl 06700 `"06700"', add
label define incother_lbl 06800 `"06800"', add
label define incother_lbl 06900 `"06900"', add
label define incother_lbl 07000 `"07000"', add
label define incother_lbl 07100 `"07100"', add
label define incother_lbl 07200 `"07200"', add
label define incother_lbl 07300 `"07300"', add
label define incother_lbl 07400 `"07400"', add
label define incother_lbl 07500 `"07500"', add
label define incother_lbl 07600 `"07600"', add
label define incother_lbl 07700 `"07700"', add
label define incother_lbl 07800 `"07800"', add
label define incother_lbl 07900 `"07900"', add
label define incother_lbl 08000 `"08000"', add
label define incother_lbl 08100 `"08100"', add
label define incother_lbl 08200 `"08200"', add
label define incother_lbl 08300 `"08300"', add
label define incother_lbl 08400 `"08400"', add
label define incother_lbl 08500 `"08500"', add
label define incother_lbl 08600 `"08600"', add
label define incother_lbl 08700 `"08700"', add
label define incother_lbl 08800 `"08800"', add
label define incother_lbl 08900 `"08900"', add
label define incother_lbl 09000 `"09000"', add
label define incother_lbl 09100 `"09100"', add
label define incother_lbl 09200 `"09200"', add
label define incother_lbl 09300 `"09300"', add
label define incother_lbl 09400 `"09400"', add
label define incother_lbl 09500 `"09500"', add
label define incother_lbl 09600 `"09600"', add
label define incother_lbl 09700 `"09700"', add
label define incother_lbl 09800 `"09800"', add
label define incother_lbl 09900 `"09900"', add
label define incother_lbl 10000 `"10000"', add
label define incother_lbl 25000 `"25000"', add
label define incother_lbl 50000 `"50000"', add
label define incother_lbl 99998 `"Unknown"', add
label define incother_lbl 99999 `"NIU"', add
label values incother incother_lbl

label define incearn_lbl 0000000 `"0000000"'
label define incearn_lbl 0000001 `"$1 or breakeven"', add
label values incearn incearn_lbl

label define occscore_lbl 00 `"00"'
label define occscore_lbl 03 `"03"', add
label define occscore_lbl 04 `"04"', add
label define occscore_lbl 05 `"05"', add
label define occscore_lbl 06 `"06"', add
label define occscore_lbl 07 `"07"', add
label define occscore_lbl 08 `"08"', add
label define occscore_lbl 09 `"09"', add
label define occscore_lbl 10 `"10"', add
label define occscore_lbl 11 `"11"', add
label define occscore_lbl 12 `"12"', add
label define occscore_lbl 13 `"13"', add
label define occscore_lbl 14 `"14"', add
label define occscore_lbl 15 `"15"', add
label define occscore_lbl 16 `"16"', add
label define occscore_lbl 17 `"17"', add
label define occscore_lbl 18 `"18"', add
label define occscore_lbl 19 `"19"', add
label define occscore_lbl 20 `"20"', add
label define occscore_lbl 21 `"21"', add
label define occscore_lbl 22 `"22"', add
label define occscore_lbl 23 `"23"', add
label define occscore_lbl 24 `"24"', add
label define occscore_lbl 25 `"25"', add
label define occscore_lbl 26 `"26"', add
label define occscore_lbl 27 `"27"', add
label define occscore_lbl 28 `"28"', add
label define occscore_lbl 29 `"29"', add
label define occscore_lbl 30 `"30"', add
label define occscore_lbl 31 `"31"', add
label define occscore_lbl 32 `"32"', add
label define occscore_lbl 33 `"33"', add
label define occscore_lbl 34 `"34"', add
label define occscore_lbl 35 `"35"', add
label define occscore_lbl 36 `"36"', add
label define occscore_lbl 37 `"37"', add
label define occscore_lbl 38 `"38"', add
label define occscore_lbl 39 `"39"', add
label define occscore_lbl 40 `"40"', add
label define occscore_lbl 41 `"41"', add
label define occscore_lbl 42 `"42"', add
label define occscore_lbl 43 `"43"', add
label define occscore_lbl 44 `"44"', add
label define occscore_lbl 45 `"45"', add
label define occscore_lbl 46 `"46"', add
label define occscore_lbl 47 `"47"', add
label define occscore_lbl 48 `"48"', add
label define occscore_lbl 49 `"49"', add
label define occscore_lbl 50 `"50"', add
label define occscore_lbl 52 `"52"', add
label define occscore_lbl 54 `"54"', add
label define occscore_lbl 58 `"58"', add
label define occscore_lbl 60 `"60"', add
label define occscore_lbl 61 `"61"', add
label define occscore_lbl 62 `"62"', add
label define occscore_lbl 63 `"63"', add
label define occscore_lbl 79 `"79"', add
label define occscore_lbl 80 `"80"', add
label values occscore occscore_lbl

label define sei_lbl 78 `"78"'
label define sei_lbl 60 `"60"', add
label define sei_lbl 79 `"79"', add
label define sei_lbl 90 `"90"', add
label define sei_lbl 67 `"67"', add
label define sei_lbl 52 `"52"', add
label define sei_lbl 76 `"76"', add
label define sei_lbl 75 `"75"', add
label define sei_lbl 84 `"84"', add
label define sei_lbl 45 `"45"', add
label define sei_lbl 96 `"96"', add
label define sei_lbl 73 `"73"', add
label define sei_lbl 39 `"39"', add
label define sei_lbl 82 `"82"', add
label define sei_lbl 87 `"87"', add
label define sei_lbl 86 `"86"', add
label define sei_lbl 85 `"85"', add
label define sei_lbl 31 `"31"', add
label define sei_lbl 83 `"83"', add
label define sei_lbl 48 `"48"', add
label define sei_lbl 59 `"59"', add
label define sei_lbl 93 `"93"', add
label define sei_lbl 46 `"46"', add
label define sei_lbl 51 `"51"', add
label define sei_lbl 80 `"80"', add
label define sei_lbl 50 `"50"', add
label define sei_lbl 92 `"92"', add
label define sei_lbl 69 `"69"', add
label define sei_lbl 56 `"56"', add
label define sei_lbl 64 `"64"', add
label define sei_lbl 81 `"81"', add
label define sei_lbl 72 `"72"', add
label define sei_lbl 53 `"53"', add
label define sei_lbl 62 `"62"', add
label define sei_lbl 58 `"58"', add
label define sei_lbl 65 `"65"', add
label define sei_lbl 14 `"14"', add
label define sei_lbl 36 `"36"', add
label define sei_lbl 33 `"33"', add
label define sei_lbl 74 `"74"', add
label define sei_lbl 63 `"63"', add
label define sei_lbl 32 `"32"', add
label define sei_lbl 54 `"54"', add
label define sei_lbl 66 `"66"', add
label define sei_lbl 77 `"77"', add
label define sei_lbl 68 `"68"', add
label define sei_lbl 44 `"44"', add
label define sei_lbl 38 `"38"', add
label define sei_lbl 25 `"25"', add
label define sei_lbl 40 `"40"', add
label define sei_lbl 28 `"28"', add
label define sei_lbl 22 `"22"', add
label define sei_lbl 61 `"61"', add
label define sei_lbl 47 `"47"', add
label define sei_lbl 35 `"35"', add
label define sei_lbl 08 `"8"', add
label define sei_lbl 27 `"27"', add
label define sei_lbl 16 `"16"', add
label define sei_lbl 23 `"23"', add
label define sei_lbl 19 `"19"', add
label define sei_lbl 21 `"21"', add
label define sei_lbl 55 `"55"', add
label define sei_lbl 24 `"24"', add
label define sei_lbl 49 `"49"', add
label define sei_lbl 26 `"26"', add
label define sei_lbl 41 `"41"', add
label define sei_lbl 10 `"10"', add
label define sei_lbl 12 `"12"', add
label define sei_lbl 43 `"43"', add
label define sei_lbl 34 `"34"', add
label define sei_lbl 15 `"15"', add
label define sei_lbl 18 `"18"', add
label define sei_lbl 37 `"37"', add
label define sei_lbl 29 `"29"', add
label define sei_lbl 11 `"11"', add
label define sei_lbl 42 `"42"', add
label define sei_lbl 30 `"30"', add
label define sei_lbl 03 `"3"', add
label define sei_lbl 05 `"5"', add
label define sei_lbl 17 `"17"', add
label define sei_lbl 06 `"6"', add
label define sei_lbl 07 `"7"', add
label define sei_lbl 13 `"13"', add
label define sei_lbl 09 `"9"', add
label define sei_lbl 04 `"4"', add
label define sei_lbl 20 `"20"', add
label define sei_lbl 00 `"0"', add
label values sei sei_lbl

label define hwsei_lbl 0713 `"0713"'
label define hwsei_lbl 0956 `"0956"', add
label define hwsei_lbl 1051 `"1051"', add
label define hwsei_lbl 1267 `"1267"', add
label define hwsei_lbl 1303 `"1303"', add
label define hwsei_lbl 1338 `"1338"', add
label define hwsei_lbl 1388 `"1388"', add
label define hwsei_lbl 1402 `"1402"', add
label define hwsei_lbl 1492 `"1492"', add
label define hwsei_lbl 1554 `"1554"', add
label define hwsei_lbl 1559 `"1559"', add
label define hwsei_lbl 1575 `"1575"', add
label define hwsei_lbl 1578 `"1578"', add
label define hwsei_lbl 1613 `"1613"', add
label define hwsei_lbl 1629 `"1629"', add
label define hwsei_lbl 1685 `"1685"', add
label define hwsei_lbl 1725 `"1725"', add
label define hwsei_lbl 1738 `"1738"', add
label define hwsei_lbl 1779 `"1779"', add
label define hwsei_lbl 1782 `"1782"', add
label define hwsei_lbl 1802 `"1802"', add
label define hwsei_lbl 1829 `"1829"', add
label define hwsei_lbl 1832 `"1832"', add
label define hwsei_lbl 1874 `"1874"', add
label define hwsei_lbl 1884 `"1884"', add
label define hwsei_lbl 1900 `"1900"', add
label define hwsei_lbl 1917 `"1917"', add
label define hwsei_lbl 1930 `"1930"', add
label define hwsei_lbl 1941 `"1941"', add
label define hwsei_lbl 1956 `"1956"', add
label define hwsei_lbl 1958 `"1958"', add
label define hwsei_lbl 1970 `"1970"', add
label define hwsei_lbl 1972 `"1972"', add
label define hwsei_lbl 2000 `"2000"', add
label define hwsei_lbl 2003 `"2003"', add
label define hwsei_lbl 2020 `"2020"', add
label define hwsei_lbl 2030 `"2030"', add
label define hwsei_lbl 2057 `"2057"', add
label define hwsei_lbl 2094 `"2094"', add
label define hwsei_lbl 2103 `"2103"', add
label define hwsei_lbl 2106 `"2106"', add
label define hwsei_lbl 2130 `"2130"', add
label define hwsei_lbl 2140 `"2140"', add
label define hwsei_lbl 2141 `"2141"', add
label define hwsei_lbl 2146 `"2146"', add
label define hwsei_lbl 2152 `"2152"', add
label define hwsei_lbl 2176 `"2176"', add
label define hwsei_lbl 2188 `"2188"', add
label define hwsei_lbl 2190 `"2190"', add
label define hwsei_lbl 2199 `"2199"', add
label define hwsei_lbl 2210 `"2210"', add
label define hwsei_lbl 2224 `"2224"', add
label define hwsei_lbl 2244 `"2244"', add
label define hwsei_lbl 2254 `"2254"', add
label define hwsei_lbl 2261 `"2261"', add
label define hwsei_lbl 2265 `"2265"', add
label define hwsei_lbl 2290 `"2290"', add
label define hwsei_lbl 2298 `"2298"', add
label define hwsei_lbl 2302 `"2302"', add
label define hwsei_lbl 2305 `"2305"', add
label define hwsei_lbl 2341 `"2341"', add
label define hwsei_lbl 2348 `"2348"', add
label define hwsei_lbl 2352 `"2352"', add
label define hwsei_lbl 2354 `"2354"', add
label define hwsei_lbl 2363 `"2363"', add
label define hwsei_lbl 2365 `"2365"', add
label define hwsei_lbl 2370 `"2370"', add
label define hwsei_lbl 2398 `"2398"', add
label define hwsei_lbl 2408 `"2408"', add
label define hwsei_lbl 2411 `"2411"', add
label define hwsei_lbl 2419 `"2419"', add
label define hwsei_lbl 2426 `"2426"', add
label define hwsei_lbl 2429 `"2429"', add
label define hwsei_lbl 2439 `"2439"', add
label define hwsei_lbl 2448 `"2448"', add
label define hwsei_lbl 2460 `"2460"', add
label define hwsei_lbl 2479 `"2479"', add
label define hwsei_lbl 2486 `"2486"', add
label define hwsei_lbl 2487 `"2487"', add
label define hwsei_lbl 2488 `"2488"', add
label define hwsei_lbl 2495 `"2495"', add
label define hwsei_lbl 2515 `"2515"', add
label define hwsei_lbl 2518 `"2518"', add
label define hwsei_lbl 2519 `"2519"', add
label define hwsei_lbl 2525 `"2525"', add
label define hwsei_lbl 2545 `"2545"', add
label define hwsei_lbl 2546 `"2546"', add
label define hwsei_lbl 2553 `"2553"', add
label define hwsei_lbl 2556 `"2556"', add
label define hwsei_lbl 2560 `"2560"', add
label define hwsei_lbl 2580 `"2580"', add
label define hwsei_lbl 2583 `"2583"', add
label define hwsei_lbl 2602 `"2602"', add
label define hwsei_lbl 2609 `"2609"', add
label define hwsei_lbl 2610 `"2610"', add
label define hwsei_lbl 2616 `"2616"', add
label define hwsei_lbl 2619 `"2619"', add
label define hwsei_lbl 2624 `"2624"', add
label define hwsei_lbl 2628 `"2628"', add
label define hwsei_lbl 2629 `"2629"', add
label define hwsei_lbl 2630 `"2630"', add
label define hwsei_lbl 2631 `"2631"', add
label define hwsei_lbl 2639 `"2639"', add
label define hwsei_lbl 2662 `"2662"', add
label define hwsei_lbl 2668 `"2668"', add
label define hwsei_lbl 2682 `"2682"', add
label define hwsei_lbl 2694 `"2694"', add
label define hwsei_lbl 2707 `"2707"', add
label define hwsei_lbl 2708 `"2708"', add
label define hwsei_lbl 2709 `"2709"', add
label define hwsei_lbl 2712 `"2712"', add
label define hwsei_lbl 2716 `"2716"', add
label define hwsei_lbl 2722 `"2722"', add
label define hwsei_lbl 2728 `"2728"', add
label define hwsei_lbl 2729 `"2729"', add
label define hwsei_lbl 2731 `"2731"', add
label define hwsei_lbl 2737 `"2737"', add
label define hwsei_lbl 2758 `"2758"', add
label define hwsei_lbl 2760 `"2760"', add
label define hwsei_lbl 2767 `"2767"', add
label define hwsei_lbl 2784 `"2784"', add
label define hwsei_lbl 2800 `"2800"', add
label define hwsei_lbl 2812 `"2812"', add
label define hwsei_lbl 2823 `"2823"', add
label define hwsei_lbl 2830 `"2830"', add
label define hwsei_lbl 2843 `"2843"', add
label define hwsei_lbl 2849 `"2849"', add
label define hwsei_lbl 2852 `"2852"', add
label define hwsei_lbl 2865 `"2865"', add
label define hwsei_lbl 2877 `"2877"', add
label define hwsei_lbl 2882 `"2882"', add
label define hwsei_lbl 2887 `"2887"', add
label define hwsei_lbl 2888 `"2888"', add
label define hwsei_lbl 2909 `"2909"', add
label define hwsei_lbl 2913 `"2913"', add
label define hwsei_lbl 2919 `"2919"', add
label define hwsei_lbl 2924 `"2924"', add
label define hwsei_lbl 2928 `"2928"', add
label define hwsei_lbl 2930 `"2930"', add
label define hwsei_lbl 2931 `"2931"', add
label define hwsei_lbl 2968 `"2968"', add
label define hwsei_lbl 2971 `"2971"', add
label define hwsei_lbl 2975 `"2975"', add
label define hwsei_lbl 2981 `"2981"', add
label define hwsei_lbl 3027 `"3027"', add
label define hwsei_lbl 3030 `"3030"', add
label define hwsei_lbl 3035 `"3035"', add
label define hwsei_lbl 3057 `"3057"', add
label define hwsei_lbl 3058 `"3058"', add
label define hwsei_lbl 3061 `"3061"', add
label define hwsei_lbl 3068 `"3068"', add
label define hwsei_lbl 3085 `"3085"', add
label define hwsei_lbl 3106 `"3106"', add
label define hwsei_lbl 3118 `"3118"', add
label define hwsei_lbl 3123 `"3123"', add
label define hwsei_lbl 3127 `"3127"', add
label define hwsei_lbl 3130 `"3130"', add
label define hwsei_lbl 3133 `"3133"', add
label define hwsei_lbl 3136 `"3136"', add
label define hwsei_lbl 3147 `"3147"', add
label define hwsei_lbl 3149 `"3149"', add
label define hwsei_lbl 3162 `"3162"', add
label define hwsei_lbl 3174 `"3174"', add
label define hwsei_lbl 3175 `"3175"', add
label define hwsei_lbl 3176 `"3176"', add
label define hwsei_lbl 3184 `"3184"', add
label define hwsei_lbl 3185 `"3185"', add
label define hwsei_lbl 3186 `"3186"', add
label define hwsei_lbl 3211 `"3211"', add
label define hwsei_lbl 3212 `"3212"', add
label define hwsei_lbl 3247 `"3247"', add
label define hwsei_lbl 3250 `"3250"', add
label define hwsei_lbl 3277 `"3277"', add
label define hwsei_lbl 3282 `"3282"', add
label define hwsei_lbl 3301 `"3301"', add
label define hwsei_lbl 3302 `"3302"', add
label define hwsei_lbl 3307 `"3307"', add
label define hwsei_lbl 3313 `"3313"', add
label define hwsei_lbl 3318 `"3318"', add
label define hwsei_lbl 3339 `"3339"', add
label define hwsei_lbl 3348 `"3348"', add
label define hwsei_lbl 3368 `"3368"', add
label define hwsei_lbl 3380 `"3380"', add
label define hwsei_lbl 3382 `"3382"', add
label define hwsei_lbl 3398 `"3398"', add
label define hwsei_lbl 3399 `"3399"', add
label define hwsei_lbl 3439 `"3439"', add
label define hwsei_lbl 3444 `"3444"', add
label define hwsei_lbl 3457 `"3457"', add
label define hwsei_lbl 3460 `"3460"', add
label define hwsei_lbl 3491 `"3491"', add
label define hwsei_lbl 3496 `"3496"', add
label define hwsei_lbl 3506 `"3506"', add
label define hwsei_lbl 3565 `"3565"', add
label define hwsei_lbl 3578 `"3578"', add
label define hwsei_lbl 3603 `"3603"', add
label define hwsei_lbl 3609 `"3609"', add
label define hwsei_lbl 3619 `"3619"', add
label define hwsei_lbl 3631 `"3631"', add
label define hwsei_lbl 3670 `"3670"', add
label define hwsei_lbl 3672 `"3672"', add
label define hwsei_lbl 3674 `"3674"', add
label define hwsei_lbl 3679 `"3679"', add
label define hwsei_lbl 3693 `"3693"', add
label define hwsei_lbl 3713 `"3713"', add
label define hwsei_lbl 3731 `"3731"', add
label define hwsei_lbl 3732 `"3732"', add
label define hwsei_lbl 3775 `"3775"', add
label define hwsei_lbl 3792 `"3792"', add
label define hwsei_lbl 3797 `"3797"', add
label define hwsei_lbl 3807 `"3807"', add
label define hwsei_lbl 3814 `"3814"', add
label define hwsei_lbl 3827 `"3827"', add
label define hwsei_lbl 3838 `"3838"', add
label define hwsei_lbl 3840 `"3840"', add
label define hwsei_lbl 3851 `"3851"', add
label define hwsei_lbl 3869 `"3869"', add
label define hwsei_lbl 3870 `"3870"', add
label define hwsei_lbl 3896 `"3896"', add
label define hwsei_lbl 3900 `"3900"', add
label define hwsei_lbl 3965 `"3965"', add
label define hwsei_lbl 3980 `"3980"', add
label define hwsei_lbl 4029 `"4029"', add
label define hwsei_lbl 4031 `"4031"', add
label define hwsei_lbl 4040 `"4040"', add
label define hwsei_lbl 4061 `"4061"', add
label define hwsei_lbl 4083 `"4083"', add
label define hwsei_lbl 4091 `"4091"', add
label define hwsei_lbl 4097 `"4097"', add
label define hwsei_lbl 4122 `"4122"', add
label define hwsei_lbl 4157 `"4157"', add
label define hwsei_lbl 4168 `"4168"', add
label define hwsei_lbl 4182 `"4182"', add
label define hwsei_lbl 4189 `"4189"', add
label define hwsei_lbl 4208 `"4208"', add
label define hwsei_lbl 4250 `"4250"', add
label define hwsei_lbl 4260 `"4260"', add
label define hwsei_lbl 4261 `"4261"', add
label define hwsei_lbl 4269 `"4269"', add
label define hwsei_lbl 4304 `"4304"', add
label define hwsei_lbl 4312 `"4312"', add
label define hwsei_lbl 4326 `"4326"', add
label define hwsei_lbl 4335 `"4335"', add
label define hwsei_lbl 4351 `"4351"', add
label define hwsei_lbl 4357 `"4357"', add
label define hwsei_lbl 4406 `"4406"', add
label define hwsei_lbl 4413 `"4413"', add
label define hwsei_lbl 4439 `"4439"', add
label define hwsei_lbl 4440 `"4440"', add
label define hwsei_lbl 4445 `"4445"', add
label define hwsei_lbl 4479 `"4479"', add
label define hwsei_lbl 4520 `"4520"', add
label define hwsei_lbl 4545 `"4545"', add
label define hwsei_lbl 4583 `"4583"', add
label define hwsei_lbl 4607 `"4607"', add
label define hwsei_lbl 4626 `"4626"', add
label define hwsei_lbl 4633 `"4633"', add
label define hwsei_lbl 4645 `"4645"', add
label define hwsei_lbl 4648 `"4648"', add
label define hwsei_lbl 4667 `"4667"', add
label define hwsei_lbl 4671 `"4671"', add
label define hwsei_lbl 4684 `"4684"', add
label define hwsei_lbl 4704 `"4704"', add
label define hwsei_lbl 4723 `"4723"', add
label define hwsei_lbl 4730 `"4730"', add
label define hwsei_lbl 4743 `"4743"', add
label define hwsei_lbl 4745 `"4745"', add
label define hwsei_lbl 4763 `"4763"', add
label define hwsei_lbl 4780 `"4780"', add
label define hwsei_lbl 4786 `"4786"', add
label define hwsei_lbl 4788 `"4788"', add
label define hwsei_lbl 4790 `"4790"', add
label define hwsei_lbl 4834 `"4834"', add
label define hwsei_lbl 4846 `"4846"', add
label define hwsei_lbl 4865 `"4865"', add
label define hwsei_lbl 4868 `"4868"', add
label define hwsei_lbl 4878 `"4878"', add
label define hwsei_lbl 4909 `"4909"', add
label define hwsei_lbl 4930 `"4930"', add
label define hwsei_lbl 4942 `"4942"', add
label define hwsei_lbl 4952 `"4952"', add
label define hwsei_lbl 5001 `"5001"', add
label define hwsei_lbl 5017 `"5017"', add
label define hwsei_lbl 5046 `"5046"', add
label define hwsei_lbl 5086 `"5086"', add
label define hwsei_lbl 5122 `"5122"', add
label define hwsei_lbl 5360 `"5360"', add
label define hwsei_lbl 5379 `"5379"', add
label define hwsei_lbl 5425 `"5425"', add
label define hwsei_lbl 5451 `"5451"', add
label define hwsei_lbl 5456 `"5456"', add
label define hwsei_lbl 5479 `"5479"', add
label define hwsei_lbl 5492 `"5492"', add
label define hwsei_lbl 5529 `"5529"', add
label define hwsei_lbl 5592 `"5592"', add
label define hwsei_lbl 5644 `"5644"', add
label define hwsei_lbl 5649 `"5649"', add
label define hwsei_lbl 5686 `"5686"', add
label define hwsei_lbl 5726 `"5726"', add
label define hwsei_lbl 5727 `"5727"', add
label define hwsei_lbl 5750 `"5750"', add
label define hwsei_lbl 5825 `"5825"', add
label define hwsei_lbl 5826 `"5826"', add
label define hwsei_lbl 5854 `"5854"', add
label define hwsei_lbl 5912 `"5912"', add
label define hwsei_lbl 5983 `"5983"', add
label define hwsei_lbl 6008 `"6008"', add
label define hwsei_lbl 6056 `"6056"', add
label define hwsei_lbl 6107 `"6107"', add
label define hwsei_lbl 6120 `"6120"', add
label define hwsei_lbl 6180 `"6180"', add
label define hwsei_lbl 6199 `"6199"', add
label define hwsei_lbl 6225 `"6225"', add
label define hwsei_lbl 6242 `"6242"', add
label define hwsei_lbl 6245 `"6245"', add
label define hwsei_lbl 6252 `"6252"', add
label define hwsei_lbl 6271 `"6271"', add
label define hwsei_lbl 6381 `"6381"', add
label define hwsei_lbl 6409 `"6409"', add
label define hwsei_lbl 6427 `"6427"', add
label define hwsei_lbl 6456 `"6456"', add
label define hwsei_lbl 6497 `"6497"', add
label define hwsei_lbl 6506 `"6506"', add
label define hwsei_lbl 6575 `"6575"', add
label define hwsei_lbl 6622 `"6622"', add
label define hwsei_lbl 6653 `"6653"', add
label define hwsei_lbl 6655 `"6655"', add
label define hwsei_lbl 6692 `"6692"', add
label define hwsei_lbl 6712 `"6712"', add
label define hwsei_lbl 6752 `"6752"', add
label define hwsei_lbl 6834 `"6834"', add
label define hwsei_lbl 6874 `"6874"', add
label define hwsei_lbl 6877 `"6877"', add
label define hwsei_lbl 6939 `"6939"', add
label define hwsei_lbl 6948 `"6948"', add
label define hwsei_lbl 6992 `"6992"', add
label define hwsei_lbl 7046 `"7046"', add
label define hwsei_lbl 7066 `"7066"', add
label define hwsei_lbl 7086 `"7086"', add
label define hwsei_lbl 7148 `"7148"', add
label define hwsei_lbl 7180 `"7180"', add
label define hwsei_lbl 7323 `"7323"', add
label define hwsei_lbl 7440 `"7440"', add
label define hwsei_lbl 7494 `"7494"', add
label define hwsei_lbl 7550 `"7550"', add
label define hwsei_lbl 7558 `"7558"', add
label define hwsei_lbl 7679 `"7679"', add
label define hwsei_lbl 7708 `"7708"', add
label define hwsei_lbl 7744 `"7744"', add
label define hwsei_lbl 8026 `"8026"', add
label define hwsei_lbl 8053 `"8053"', add
label define hwsei_lbl 0000 `"N/A"', add
label values hwsei hwsei_lbl

label define migrate1_lbl 0 `"N/A"'
label define migrate1_lbl 1 `"Same house"', add
label define migrate1_lbl 2 `"Moved within state"', add
label define migrate1_lbl 3 `"Moved between states"', add
label define migrate1_lbl 4 `"Abroad one year ago"', add
label define migrate1_lbl 9 `"Unknown"', add
label values migrate1 migrate1_lbl

label define migrate1d_lbl 00 `"N/A"'
label define migrate1d_lbl 10 `"Same house"', add
label define migrate1d_lbl 20 `"Same state (migration status within state unknown)"', add
label define migrate1d_lbl 21 `"Different house, moved within county"', add
label define migrate1d_lbl 22 `"Different house, moved within state, between counties"', add
label define migrate1d_lbl 23 `"Different house, moved within state, within PUMA"', add
label define migrate1d_lbl 24 `"Different house, moved within state, between PUMAs"', add
label define migrate1d_lbl 25 `"Different house, unknown within state"', add
label define migrate1d_lbl 30 `"Different state (general)"', add
label define migrate1d_lbl 31 `"Moved between contigious states"', add
label define migrate1d_lbl 32 `"Moved between non-contiguous states"', add
label define migrate1d_lbl 40 `"Abroad one year ago"', add
label define migrate1d_lbl 90 `"Unknown"', add
label values migrate1d migrate1d_lbl

label define migplac1_lbl 000 `"N/A"'
label define migplac1_lbl 001 `"Alabama"', add
label define migplac1_lbl 002 `"Alaska"', add
label define migplac1_lbl 004 `"Arizona"', add
label define migplac1_lbl 005 `"Arkansas"', add
label define migplac1_lbl 006 `"California"', add
label define migplac1_lbl 008 `"Colorado"', add
label define migplac1_lbl 009 `"Connecticut"', add
label define migplac1_lbl 010 `"Delaware"', add
label define migplac1_lbl 011 `"District of Columbia"', add
label define migplac1_lbl 012 `"Florida"', add
label define migplac1_lbl 013 `"Georgia"', add
label define migplac1_lbl 015 `"Hawaii"', add
label define migplac1_lbl 016 `"Idaho"', add
label define migplac1_lbl 017 `"Illinois"', add
label define migplac1_lbl 018 `"Indiana"', add
label define migplac1_lbl 019 `"Iowa"', add
label define migplac1_lbl 020 `"Kansas"', add
label define migplac1_lbl 021 `"Kentucky"', add
label define migplac1_lbl 022 `"Louisiana"', add
label define migplac1_lbl 023 `"Maine"', add
label define migplac1_lbl 024 `"Maryland"', add
label define migplac1_lbl 025 `"Massachusetts"', add
label define migplac1_lbl 026 `"Michigan"', add
label define migplac1_lbl 027 `"Minnesota"', add
label define migplac1_lbl 028 `"Mississippi"', add
label define migplac1_lbl 029 `"Missouri"', add
label define migplac1_lbl 030 `"Montana"', add
label define migplac1_lbl 031 `"Nebraska"', add
label define migplac1_lbl 032 `"Nevada"', add
label define migplac1_lbl 033 `"New Hampshire"', add
label define migplac1_lbl 034 `"New Jersey"', add
label define migplac1_lbl 035 `"New Mexico"', add
label define migplac1_lbl 036 `"New York"', add
label define migplac1_lbl 037 `"North Carolina"', add
label define migplac1_lbl 038 `"North Dakota"', add
label define migplac1_lbl 039 `"Ohio"', add
label define migplac1_lbl 040 `"Oklahoma"', add
label define migplac1_lbl 041 `"Oregon"', add
label define migplac1_lbl 042 `"Pennsylvania"', add
label define migplac1_lbl 044 `"Rhode Island"', add
label define migplac1_lbl 045 `"South Carolina"', add
label define migplac1_lbl 046 `"South Dakota"', add
label define migplac1_lbl 047 `"Tennessee"', add
label define migplac1_lbl 048 `"Texas"', add
label define migplac1_lbl 049 `"Utah"', add
label define migplac1_lbl 050 `"Vermont"', add
label define migplac1_lbl 051 `"Virginia"', add
label define migplac1_lbl 053 `"Washington"', add
label define migplac1_lbl 054 `"West Virginia"', add
label define migplac1_lbl 055 `"Wisconsin"', add
label define migplac1_lbl 056 `"Wyoming"', add
label define migplac1_lbl 099 `"United States, ns"', add
label define migplac1_lbl 100 `"Samoa, 1950"', add
label define migplac1_lbl 105 `"Guam"', add
label define migplac1_lbl 110 `"Puerto Rico"', add
label define migplac1_lbl 115 `"Virgin Islands"', add
label define migplac1_lbl 120 `"Other US Possessions"', add
label define migplac1_lbl 150 `"Canada"', add
label define migplac1_lbl 151 `"English Canada"', add
label define migplac1_lbl 152 `"French Canada"', add
label define migplac1_lbl 160 `"Atlantic Islands"', add
label define migplac1_lbl 200 `"Mexico"', add
label define migplac1_lbl 211 `"Belize/British Honduras"', add
label define migplac1_lbl 212 `"Costa Rica"', add
label define migplac1_lbl 213 `"El Salvador"', add
label define migplac1_lbl 214 `"Guatemala"', add
label define migplac1_lbl 215 `"Honduras"', add
label define migplac1_lbl 216 `"Nicaragua"', add
label define migplac1_lbl 217 `"Panama"', add
label define migplac1_lbl 218 `"Canal Zone"', add
label define migplac1_lbl 219 `"Central America, nec"', add
label define migplac1_lbl 250 `"Cuba"', add
label define migplac1_lbl 261 `"Dominican Republic"', add
label define migplac1_lbl 262 `"Haiti"', add
label define migplac1_lbl 263 `"Jamaica"', add
label define migplac1_lbl 264 `"British West Indies"', add
label define migplac1_lbl 267 `"Other West Indies"', add
label define migplac1_lbl 290 `"Other Caribbean and North America"', add
label define migplac1_lbl 305 `"Argentina"', add
label define migplac1_lbl 310 `"Bolivia"', add
label define migplac1_lbl 315 `"Brazil"', add
label define migplac1_lbl 320 `"Chile"', add
label define migplac1_lbl 325 `"Colombia"', add
label define migplac1_lbl 330 `"Ecuador"', add
label define migplac1_lbl 345 `"Paraguay"', add
label define migplac1_lbl 350 `"Peru"', add
label define migplac1_lbl 360 `"Uruguay"', add
label define migplac1_lbl 365 `"Venezuela"', add
label define migplac1_lbl 390 `"South America, nec"', add
label define migplac1_lbl 400 `"Denmark"', add
label define migplac1_lbl 401 `"Finland"', add
label define migplac1_lbl 402 `"Iceland"', add
label define migplac1_lbl 404 `"Norway"', add
label define migplac1_lbl 405 `"Sweden"', add
label define migplac1_lbl 410 `"England"', add
label define migplac1_lbl 411 `"Scotland"', add
label define migplac1_lbl 412 `"Wales"', add
label define migplac1_lbl 413 `"United Kingdom (excluding England: 2005ACS)"', add
label define migplac1_lbl 414 `"Ireland"', add
label define migplac1_lbl 415 `"Northern Ireland"', add
label define migplac1_lbl 419 `"Other Northern Europe"', add
label define migplac1_lbl 420 `"Belgium"', add
label define migplac1_lbl 421 `"France"', add
label define migplac1_lbl 422 `"Luxembourg"', add
label define migplac1_lbl 425 `"Netherlands"', add
label define migplac1_lbl 426 `"Switzerland"', add
label define migplac1_lbl 429 `"Other Western Europe"', add
label define migplac1_lbl 430 `"Albania"', add
label define migplac1_lbl 433 `"Greece"', add
label define migplac1_lbl 434 `"Dodecanese Islands"', add
label define migplac1_lbl 435 `"Italy"', add
label define migplac1_lbl 436 `"Portugal"', add
label define migplac1_lbl 437 `"Azores"', add
label define migplac1_lbl 438 `"Spain"', add
label define migplac1_lbl 450 `"Austria"', add
label define migplac1_lbl 451 `"Bulgaria"', add
label define migplac1_lbl 452 `"Czechoslovakia"', add
label define migplac1_lbl 453 `"Germany"', add
label define migplac1_lbl 454 `"Hungary"', add
label define migplac1_lbl 455 `"Poland"', add
label define migplac1_lbl 456 `"Romania"', add
label define migplac1_lbl 457 `"Yugoslavia"', add
label define migplac1_lbl 458 `"Bosnia and Herzegovinia"', add
label define migplac1_lbl 459 `"Other Eastern Europe"', add
label define migplac1_lbl 460 `"Estonia"', add
label define migplac1_lbl 461 `"Latvia"', add
label define migplac1_lbl 462 `"Lithuania"', add
label define migplac1_lbl 463 `"Other Northern or Eastern Europe"', add
label define migplac1_lbl 465 `"USSR"', add
label define migplac1_lbl 498 `"Ukraine"', add
label define migplac1_lbl 499 `"Europe, ns"', add
label define migplac1_lbl 500 `"China"', add
label define migplac1_lbl 501 `"Japan"', add
label define migplac1_lbl 502 `"Korea"', add
label define migplac1_lbl 503 `"Taiwan"', add
label define migplac1_lbl 515 `"Philippines"', add
label define migplac1_lbl 517 `"Thailand"', add
label define migplac1_lbl 518 `"Vietnam"', add
label define migplac1_lbl 519 `"Other South East Asia"', add
label define migplac1_lbl 520 `"Nepal"', add
label define migplac1_lbl 521 `"India"', add
label define migplac1_lbl 522 `"Iran"', add
label define migplac1_lbl 523 `"Iraq"', add
label define migplac1_lbl 525 `"Pakistan"', add
label define migplac1_lbl 534 `"Israel/Palestine"', add
label define migplac1_lbl 535 `"Jordan"', add
label define migplac1_lbl 537 `"Lebanon"', add
label define migplac1_lbl 539 `"United Arab Emirates"', add
label define migplac1_lbl 540 `"Saudi Arabia"', add
label define migplac1_lbl 541 `"Syria"', add
label define migplac1_lbl 542 `"Turkey"', add
label define migplac1_lbl 543 `"Afghanistan"', add
label define migplac1_lbl 551 `"Other Western Asia"', add
label define migplac1_lbl 599 `"Asia, nec"', add
label define migplac1_lbl 600 `"Africa"', add
label define migplac1_lbl 610 `"Northern Africa"', add
label define migplac1_lbl 611 `"Egypt"', add
label define migplac1_lbl 619 `"Nigeria"', add
label define migplac1_lbl 620 `"Western Africa"', add
label define migplac1_lbl 621 `"Eastern Africa"', add
label define migplac1_lbl 622 `"Ethiopia"', add
label define migplac1_lbl 623 `"Kenya"', add
label define migplac1_lbl 694 `"South Africa (Union of)"', add
label define migplac1_lbl 699 `"Africa, nec"', add
label define migplac1_lbl 701 `"Australia"', add
label define migplac1_lbl 702 `"New Zealand"', add
label define migplac1_lbl 710 `"Pacific Islands (Australia and New Zealand Subregions, not specified, Oceania and at Sea: ACS)"', add
label define migplac1_lbl 900 `"Abroad (unknown) or at sea"', add
label define migplac1_lbl 988 `"Suppressed for data year 2022 for select cases"', add
label define migplac1_lbl 997 `"Unknown value"', add
label define migplac1_lbl 999 `"Missing"', add
label values migplac1 migplac1_lbl

label define migmet131_lbl 00000 `"Not in universe or not in identifiable area"'
label define migmet131_lbl 10420 `"Akron, OH"', add
label define migmet131_lbl 10580 `"Albany-Schenectady-Troy, NY"', add
label define migmet131_lbl 10740 `"Albuquerque, NM"', add
label define migmet131_lbl 10780 `"Alexandria, LA"', add
label define migmet131_lbl 10900 `"Allentown-Bethlehem-Easton, PA-NJ"', add
label define migmet131_lbl 11020 `"Altoona, PA"', add
label define migmet131_lbl 11100 `"Amarillo, TX"', add
label define migmet131_lbl 11260 `"Anchorage, AK"', add
label define migmet131_lbl 11460 `"Ann Arbor, MI"', add
label define migmet131_lbl 11500 `"Anniston-Oxford-Jacksonville, AL"', add
label define migmet131_lbl 11700 `"Asheville, NC"', add
label define migmet131_lbl 12020 `"Athens-Clarke County, GA"', add
label define migmet131_lbl 12060 `"Atlanta-Sandy Springs-Roswell, GA"', add
label define migmet131_lbl 12100 `"Atlantic City-Hammonton, NJ"', add
label define migmet131_lbl 12220 `"Auburn-Opelika, AL"', add
label define migmet131_lbl 12260 `"Augusta-Richmond County, GA-SC"', add
label define migmet131_lbl 12420 `"Austin-Round Rock, TX"', add
label define migmet131_lbl 12540 `"Bakersfield, CA"', add
label define migmet131_lbl 12580 `"Baltimore-Columbia-Towson, MD"', add
label define migmet131_lbl 12620 `"Bangor, ME"', add
label define migmet131_lbl 12700 `"Barnstable Town, MA"', add
label define migmet131_lbl 12940 `"Baton Rouge, LA"', add
label define migmet131_lbl 12980 `"Battle Creek, MI"', add
label define migmet131_lbl 13140 `"Beaumont-Port Arthur, TX"', add
label define migmet131_lbl 13220 `"Beckley, WV"', add
label define migmet131_lbl 13380 `"Bellingham, WA"', add
label define migmet131_lbl 13460 `"Bend-Redmond, OR"', add
label define migmet131_lbl 13740 `"Billings, MT"', add
label define migmet131_lbl 13780 `"Binghamton, NY"', add
label define migmet131_lbl 13820 `"Birmingham-Hoover, AL"', add
label define migmet131_lbl 13900 `"Bismarck, ND"', add
label define migmet131_lbl 13980 `"Blacksburg-Christiansburg-Radford, VA"', add
label define migmet131_lbl 14010 `"Bloomington, IL"', add
label define migmet131_lbl 14020 `"Bloomington, IN"', add
label define migmet131_lbl 14260 `"Boise City, ID"', add
label define migmet131_lbl 14460 `"Boston-Cambridge-Newton, MA-NH"', add
label define migmet131_lbl 14740 `"Bremerton-Silverdale, WA"', add
label define migmet131_lbl 14860 `"Bridgeport-Stamford-Norwalk, CT"', add
label define migmet131_lbl 15180 `"Brownsville-Harlingen, TX"', add
label define migmet131_lbl 15380 `"Buffalo-Cheektowaga-Niagara Falls, NY"', add
label define migmet131_lbl 15500 `"Burlington, NC"', add
label define migmet131_lbl 15540 `"Burlington-South Burlington, VT"', add
label define migmet131_lbl 15940 `"Canton-Massillon, OH"', add
label define migmet131_lbl 15980 `"Cape Coral-Fort Myers, FL"', add
label define migmet131_lbl 16580 `"Champaign-Urbana, IL"', add
label define migmet131_lbl 16620 `"Charleston, WV"', add
label define migmet131_lbl 16700 `"Charleston-North Charleston, SC"', add
label define migmet131_lbl 16740 `"Charlotte-Concord-Gastonia, NC-SC"', add
label define migmet131_lbl 16820 `"Charlottesville, VA"', add
label define migmet131_lbl 16860 `"Chattanooga, TN-GA"', add
label define migmet131_lbl 16940 `"Cheyenne, WY"', add
label define migmet131_lbl 16980 `"Chicago-Naperville-Elgin, IL-IN-WI"', add
label define migmet131_lbl 17020 `"Chico, CA"', add
label define migmet131_lbl 17140 `"Cincinnati, OH-KY-IN"', add
label define migmet131_lbl 17300 `"Clarksville, TN-KY"', add
label define migmet131_lbl 17420 `"Cleveland, TN"', add
label define migmet131_lbl 17460 `"Cleveland-Elyria, OH"', add
label define migmet131_lbl 17660 `"Coeur d'Alene, ID"', add
label define migmet131_lbl 17780 `"College Station-Bryan, TX"', add
label define migmet131_lbl 17820 `"Colorado Springs, CO"', add
label define migmet131_lbl 17860 `"Columbia, MO"', add
label define migmet131_lbl 17900 `"Columbia, SC"', add
label define migmet131_lbl 18140 `"Columbus, OH"', add
label define migmet131_lbl 18580 `"Corpus Christi, TX"', add
label define migmet131_lbl 18880 `"Crestview-Fort Walton Beach-Destin, FL"', add
label define migmet131_lbl 19100 `"Dallas-Fort Worth-Arlington, TX"', add
label define migmet131_lbl 19300 `"Daphne-Fairhope-Foley, AL"', add
label define migmet131_lbl 19340 `"Davenport-Moline-Rock Island, IA-IL"', add
label define migmet131_lbl 19380 `"Dayton, OH"', add
label define migmet131_lbl 19460 `"Decatur, AL"', add
label define migmet131_lbl 19500 `"Decatur, IL"', add
label define migmet131_lbl 19660 `"Deltona-Daytona Beach-Ormond Beach, FL"', add
label define migmet131_lbl 19740 `"Denver-Aurora-Lakewood, CO"', add
label define migmet131_lbl 19780 `"Des Moines-West Des Moines, IA"', add
label define migmet131_lbl 19820 `"Detroit-Warren-Dearborn, MI"', add
label define migmet131_lbl 20020 `"Dothan, AL"', add
label define migmet131_lbl 20100 `"Dover, DE"', add
label define migmet131_lbl 20500 `"Durham-Chapel Hill, NC"', add
label define migmet131_lbl 20700 `"East Stroudsburg, PA"', add
label define migmet131_lbl 20740 `"Eau Claire, WI"', add
label define migmet131_lbl 20940 `"El Centro, CA"', add
label define migmet131_lbl 21060 `"Elizabethtown-Fort Knox, KY"', add
label define migmet131_lbl 21140 `"Elkhart-Goshen, IN"', add
label define migmet131_lbl 21340 `"El Paso, TX"', add
label define migmet131_lbl 21500 `"Erie, PA"', add
label define migmet131_lbl 21660 `"Eugene, OR"', add
label define migmet131_lbl 21780 `"Evansville, IN-KY"', add
label define migmet131_lbl 22140 `"Farmington, NM"', add
label define migmet131_lbl 22180 `"Fayetteville, NC"', add
label define migmet131_lbl 22220 `"Fayetteville-Springdale-Rogers, AR-MO"', add
label define migmet131_lbl 22380 `"Flagstaff, AZ"', add
label define migmet131_lbl 22420 `"Flint, MI"', add
label define migmet131_lbl 22500 `"Florence, SC"', add
label define migmet131_lbl 22520 `"Florence-Muscle Shoals, AL"', add
label define migmet131_lbl 22660 `"Fort Collins, CO"', add
label define migmet131_lbl 23060 `"Fort Wayne, IN"', add
label define migmet131_lbl 23420 `"Fresno, CA"', add
label define migmet131_lbl 23460 `"Gadsden, AL"', add
label define migmet131_lbl 23540 `"Gainesville, FL"', add
label define migmet131_lbl 23580 `"Gainesville, GA"', add
label define migmet131_lbl 24020 `"Glens Falls, NY"', add
label define migmet131_lbl 24140 `"Goldsboro, NC"', add
label define migmet131_lbl 24300 `"Grand Junction, CO"', add
label define migmet131_lbl 24340 `"Grand Rapids-Wyoming, MI"', add
label define migmet131_lbl 24540 `"Greeley, CO"', add
label define migmet131_lbl 24660 `"Greensboro-High Point, NC"', add
label define migmet131_lbl 24780 `"Greenville, NC"', add
label define migmet131_lbl 24860 `"Greenville-Anderson-Mauldin, SC"', add
label define migmet131_lbl 25060 `"Gulfport-Biloxi-Pascagoula, MS"', add
label define migmet131_lbl 25220 `"Hammond, LA"', add
label define migmet131_lbl 25260 `"Hanford-Corcoran, CA"', add
label define migmet131_lbl 25420 `"Harrisburg-Carlisle, PA"', add
label define migmet131_lbl 25500 `"Harrisonburg, VA"', add
label define migmet131_lbl 25540 `"Hartford-West Hartford-East Hartford, CT"', add
label define migmet131_lbl 25620 `"Hattiesburg, MS"', add
label define migmet131_lbl 25860 `"Hickory-Lenoir-Morganton, NC"', add
label define migmet131_lbl 25940 `"Hilton Head Island-Bluffton-Beaufort, SC"', add
label define migmet131_lbl 26140 `"Homosassa Springs, FL"', add
label define migmet131_lbl 26380 `"Houma-Thibodaux, LA"', add
label define migmet131_lbl 26420 `"Houston-The Woodlands-Sugar Land, TX"', add
label define migmet131_lbl 26620 `"Huntsville, AL"', add
label define migmet131_lbl 26900 `"Indianapolis-Carmel-Anderson, IN"', add
label define migmet131_lbl 26980 `"Iowa City, IA"', add
label define migmet131_lbl 27060 `"Ithaca, NY"', add
label define migmet131_lbl 27100 `"Jackson, MI"', add
label define migmet131_lbl 27140 `"Jackson, MS"', add
label define migmet131_lbl 27180 `"Jackson, TN"', add
label define migmet131_lbl 27260 `"Jacksonville, FL"', add
label define migmet131_lbl 27340 `"Jacksonville, NC"', add
label define migmet131_lbl 27500 `"Janesville-Beloit, WI"', add
label define migmet131_lbl 27620 `"Jefferson City, MO"', add
label define migmet131_lbl 27740 `"Johnson City, TN"', add
label define migmet131_lbl 27780 `"Johnstown, PA"', add
label define migmet131_lbl 27860 `"Jonesboro, AR"', add
label define migmet131_lbl 27900 `"Joplin, MO"', add
label define migmet131_lbl 28020 `"Kalamazoo-Portage, MI"', add
label define migmet131_lbl 28100 `"Kankakee, IL"', add
label define migmet131_lbl 28140 `"Kansas City, MO-KS"', add
label define migmet131_lbl 28420 `"Kennewick-Richland, WA"', add
label define migmet131_lbl 28660 `"Killeen-Temple, TX"', add
label define migmet131_lbl 28700 `"Kingsport-Bristol-Bristol, TN-VA"', add
label define migmet131_lbl 28940 `"Knoxville, TN"', add
label define migmet131_lbl 29100 `"La Crosse-Onalaska, WI-MN"', add
label define migmet131_lbl 29180 `"Lafayette, LA"', add
label define migmet131_lbl 29200 `"Lafayette-West Lafayette, IN"', add
label define migmet131_lbl 29340 `"Lake Charles, LA"', add
label define migmet131_lbl 29420 `"Lake Havasu City-Kingman, AZ"', add
label define migmet131_lbl 29460 `"Lakeland-Winter Haven, FL"', add
label define migmet131_lbl 29540 `"Lancaster, PA"', add
label define migmet131_lbl 29620 `"Lansing-East Lansing, MI"', add
label define migmet131_lbl 29700 `"Laredo, TX"', add
label define migmet131_lbl 29740 `"Las Cruces, NM"', add
label define migmet131_lbl 29820 `"Las Vegas-Henderson-Paradise, NV"', add
label define migmet131_lbl 29940 `"Lawrence, KS"', add
label define migmet131_lbl 30020 `"Lawton, OK"', add
label define migmet131_lbl 30140 `"Lebanon, PA"', add
label define migmet131_lbl 30340 `"Lewiston-Auburn, ME"', add
label define migmet131_lbl 30620 `"Lima, OH"', add
label define migmet131_lbl 30700 `"Lincoln, NE"', add
label define migmet131_lbl 30780 `"Little Rock-North Little Rock-Conway, AR"', add
label define migmet131_lbl 31080 `"Los Angeles-Long Beach-Anaheim, CA"', add
label define migmet131_lbl 31140 `"Louisville/Jefferson County, KY-IN"', add
label define migmet131_lbl 31180 `"Lubbock, TX"', add
label define migmet131_lbl 31340 `"Lynchburg, VA"', add
label define migmet131_lbl 31460 `"Madera, CA"', add
label define migmet131_lbl 31700 `"Manchester-Nashua, NH"', add
label define migmet131_lbl 31860 `"Mankato-North Mankato, MN"', add
label define migmet131_lbl 31900 `"Mansfield, OH"', add
label define migmet131_lbl 32420 `"Mayagüez, PR"', add
label define migmet131_lbl 32580 `"McAllen-Edinburg-Mission, TX"', add
label define migmet131_lbl 32780 `"Medford, OR"', add
label define migmet131_lbl 32820 `"Memphis, TN-MS-AR"', add
label define migmet131_lbl 32900 `"Merced, CA"', add
label define migmet131_lbl 33100 `"Miami-Fort Lauderdale-West Palm Beach, FL"', add
label define migmet131_lbl 33140 `"Michigan City-La Porte, IN"', add
label define migmet131_lbl 33260 `"Midland, TX"', add
label define migmet131_lbl 33340 `"Milwaukee-Waukesha-West Allis, WI"', add
label define migmet131_lbl 33460 `"Minneapolis-St. Paul-Bloomington, MN-WI"', add
label define migmet131_lbl 33660 `"Mobile, AL"', add
label define migmet131_lbl 33700 `"Modesto, CA"', add
label define migmet131_lbl 33740 `"Monroe, LA"', add
label define migmet131_lbl 33780 `"Monroe, MI"', add
label define migmet131_lbl 33860 `"Montgomery, AL"', add
label define migmet131_lbl 34060 `"Morgantown, WV"', add
label define migmet131_lbl 34580 `"Mount Vernon-Anacortes, WA"', add
label define migmet131_lbl 34620 `"Muncie, IN"', add
label define migmet131_lbl 34740 `"Muskegon, MI"', add
label define migmet131_lbl 34820 `"Myrtle Beach-Conway-North Myrtle Beach, SC-NC"', add
label define migmet131_lbl 34900 `"Napa, CA"', add
label define migmet131_lbl 34940 `"Naples-Immokalee-Marco Island, FL"', add
label define migmet131_lbl 34980 `"Nashville-Davidson--Murfreesboro--Franklin, TN"', add
label define migmet131_lbl 35300 `"New Haven-Milford, CT"', add
label define migmet131_lbl 35380 `"New Orleans-Metairie, LA"', add
label define migmet131_lbl 35620 `"New York-Newark-Jersey City, NY-NJ-PA"', add
label define migmet131_lbl 35660 `"Niles-Benton Harbor, MI"', add
label define migmet131_lbl 35840 `"North Port-Sarasota-Bradenton, FL"', add
label define migmet131_lbl 35980 `"Norwich-New London, CT"', add
label define migmet131_lbl 36100 `"Ocala, FL"', add
label define migmet131_lbl 36140 `"Ocean City, NJ"', add
label define migmet131_lbl 36220 `"Odessa, TX"', add
label define migmet131_lbl 36260 `"Ogden-Clearfield, UT"', add
label define migmet131_lbl 36420 `"Oklahoma City, OK"', add
label define migmet131_lbl 36500 `"Olympia-Tumwater, WA"', add
label define migmet131_lbl 36540 `"Omaha-Council Bluffs, NE-IA"', add
label define migmet131_lbl 36740 `"Orlando-Kissimmee-Sanford, FL"', add
label define migmet131_lbl 36780 `"Oshkosh-Neenah, WI"', add
label define migmet131_lbl 36980 `"Owensboro, KY"', add
label define migmet131_lbl 37100 `"Oxnard-Thousand Oaks-Ventura, CA"', add
label define migmet131_lbl 37340 `"Palm Bay-Melbourne-Titusville, FL"', add
label define migmet131_lbl 37460 `"Panama City, FL"', add
label define migmet131_lbl 37620 `"Parkersburg-Vienna, WV"', add
label define migmet131_lbl 37860 `"Pensacola-Ferry Pass-Brent, FL"', add
label define migmet131_lbl 37900 `"Peoria, IL"', add
label define migmet131_lbl 37980 `"Philadelphia-Camden-Wilmington, PA-NJ-DE-MD"', add
label define migmet131_lbl 38060 `"Phoenix-Mesa-Scottsdale, AZ"', add
label define migmet131_lbl 38300 `"Pittsburgh, PA"', add
label define migmet131_lbl 38340 `"Pittsfield, MA"', add
label define migmet131_lbl 38660 `"Ponce, PR"', add
label define migmet131_lbl 38860 `"Portland-South Portland, ME"', add
label define migmet131_lbl 38900 `"Portland-Vancouver-Hillsboro, OR-WA"', add
label define migmet131_lbl 38940 `"Port St. Lucie, FL"', add
label define migmet131_lbl 39140 `"Prescott, AZ"', add
label define migmet131_lbl 39300 `"Providence-Warwick, RI-MA"', add
label define migmet131_lbl 39340 `"Provo-Orem, UT"', add
label define migmet131_lbl 39380 `"Pueblo, CO"', add
label define migmet131_lbl 39460 `"Punta Gorda, FL"', add
label define migmet131_lbl 39540 `"Racine, WI"', add
label define migmet131_lbl 39580 `"Raleigh, NC"', add
label define migmet131_lbl 39740 `"Reading, PA"', add
label define migmet131_lbl 39820 `"Redding, CA"', add
label define migmet131_lbl 39900 `"Reno, NV"', add
label define migmet131_lbl 40060 `"Richmond, VA"', add
label define migmet131_lbl 40140 `"Riverside-San Bernardino-Ontario, CA"', add
label define migmet131_lbl 40220 `"Roanoke, VA"', add
label define migmet131_lbl 40380 `"Rochester, NY"', add
label define migmet131_lbl 40420 `"Rockford, IL"', add
label define migmet131_lbl 40580 `"Rocky Mount, NC"', add
label define migmet131_lbl 40900 `"Sacramento--Roseville--Arden-Arcade, CA"', add
label define migmet131_lbl 40980 `"Saginaw, MI"', add
label define migmet131_lbl 41060 `"St. Cloud, MN"', add
label define migmet131_lbl 41100 `"St. George, UT"', add
label define migmet131_lbl 41140 `"St. Joseph, MO-KS"', add
label define migmet131_lbl 41180 `"St. Louis, MO-IL"', add
label define migmet131_lbl 41420 `"Salem, OR"', add
label define migmet131_lbl 41500 `"Salinas, CA"', add
label define migmet131_lbl 41540 `"Salisbury, MD-DE"', add
label define migmet131_lbl 41620 `"Salt Lake City, UT"', add
label define migmet131_lbl 41660 `"San Angelo, TX"', add
label define migmet131_lbl 41700 `"San Antonio-New Braunfels, TX"', add
label define migmet131_lbl 41740 `"San Diego-Carlsbad, CA"', add
label define migmet131_lbl 41860 `"San Francisco-Oakland-Hayward, CA"', add
label define migmet131_lbl 41900 `"San Germán, PR"', add
label define migmet131_lbl 41940 `"San Jose-Sunnyvale-Santa Clara, CA"', add
label define migmet131_lbl 41980 `"San Juan-Carolina-Caguas, PR"', add
label define migmet131_lbl 42020 `"San Luis Obispo-Paso Robles-Arroyo Grande, CA"', add
label define migmet131_lbl 42100 `"Santa Cruz-Watsonville, CA"', add
label define migmet131_lbl 42140 `"Santa Fe, NM"', add
label define migmet131_lbl 42200 `"Santa Maria-Santa Barbara, CA"', add
label define migmet131_lbl 42220 `"Santa Rosa, CA"', add
label define migmet131_lbl 42540 `"Scranton--Wilkes-Barre--Hazleton, PA"', add
label define migmet131_lbl 42660 `"Seattle-Tacoma-Bellevue, WA"', add
label define migmet131_lbl 42680 `"Sebastian-Vero Beach, FL"', add
label define migmet131_lbl 43100 `"Sheboygan, WI"', add
label define migmet131_lbl 43340 `"Shreveport-Bossier City, LA"', add
label define migmet131_lbl 43900 `"Spartanburg, SC"', add
label define migmet131_lbl 44060 `"Spokane-Spokane Valley, WA"', add
label define migmet131_lbl 44100 `"Springfield, IL"', add
label define migmet131_lbl 44140 `"Springfield, MA"', add
label define migmet131_lbl 44180 `"Springfield, MO"', add
label define migmet131_lbl 44220 `"Springfield, OH"', add
label define migmet131_lbl 44300 `"State College, PA"', add
label define migmet131_lbl 44700 `"Stockton-Lodi, CA"', add
label define migmet131_lbl 44940 `"Sumter, SC"', add
label define migmet131_lbl 45060 `"Syracuse, NY"', add
label define migmet131_lbl 45220 `"Tallahassee, FL"', add
label define migmet131_lbl 45300 `"Tampa-St. Petersburg-Clearwater, FL"', add
label define migmet131_lbl 45460 `"Terre Haute, IN"', add
label define migmet131_lbl 45540 `"The Villages, FL"', add
label define migmet131_lbl 45780 `"Toledo, OH"', add
label define migmet131_lbl 45820 `"Topeka, KS"', add
label define migmet131_lbl 45940 `"Trenton, NJ"', add
label define migmet131_lbl 46060 `"Tucson, AZ"', add
label define migmet131_lbl 46140 `"Tulsa, OK"', add
label define migmet131_lbl 46220 `"Tuscaloosa, AL"', add
label define migmet131_lbl 46340 `"Tyler, TX"', add
label define migmet131_lbl 46520 `"Urban Honolulu, HI"', add
label define migmet131_lbl 46540 `"Utica-Rome, NY"', add
label define migmet131_lbl 46660 `"Valdosta, GA"', add
label define migmet131_lbl 46700 `"Vallejo-Fairfield, CA"', add
label define migmet131_lbl 47220 `"Vineland-Bridgeton, NJ"', add
label define migmet131_lbl 47260 `"Virginia Beach-Norfolk-Newport News, VA-NC"', add
label define migmet131_lbl 47300 `"Visalia-Porterville, CA"', add
label define migmet131_lbl 47380 `"Waco, TX"', add
label define migmet131_lbl 47580 `"Warner Robins, GA"', add
label define migmet131_lbl 47900 `"Washington-Arlington-Alexandria, DC-VA-MD-WV"', add
label define migmet131_lbl 48140 `"Wausau, WI"', add
label define migmet131_lbl 48300 `"Wenatchee, WA"', add
label define migmet131_lbl 48620 `"Wichita, KS"', add
label define migmet131_lbl 48660 `"Wichita Falls, TX"', add
label define migmet131_lbl 48700 `"Williamsport, PA"', add
label define migmet131_lbl 48900 `"Wilmington, NC"', add
label define migmet131_lbl 49180 `"Winston-Salem, NC"', add
label define migmet131_lbl 49340 `"Worcester, MA-CT"', add
label define migmet131_lbl 49420 `"Yakima, WA"', add
label define migmet131_lbl 49620 `"York-Hanover, PA"', add
label define migmet131_lbl 49660 `"Youngstown-Warren-Boardman, OH-PA"', add
label define migmet131_lbl 49700 `"Yuba City, CA"', add
label define migmet131_lbl 49740 `"Yuma, AZ"', add
label values migmet131 migmet131_lbl

label define movedin_lbl 0 `"N/A"'
label define movedin_lbl 1 `"This yr or last (ACS: up to 12 months)"', add
label define movedin_lbl 2 `"2(1960-70);2-5(1980-2000);13-23 mo(ACS)"', add
label define movedin_lbl 3 `"3(1960-70);2-4(ACS)"', add
label define movedin_lbl 4 `"4-6 (1960);4-5(1970);5-9(ACS)"', add
label define movedin_lbl 5 `"7-10 (1960); 6-10 (1970-2000);10-19(ACS)"', add
label define movedin_lbl 6 `"11-20(1960-2000);20-29(ACS)"', add
label define movedin_lbl 7 `"21+(1960-70);21-30(1980-2000);30+(ACS)"', add
label define movedin_lbl 9 `"Always lived here (1960-70)"', add
label define movedin_lbl 8 `"31+ (1980-2000)"', add
label values movedin movedin_lbl

label define disabwrk_lbl 0 `"N/A"'
label define disabwrk_lbl 1 `"No disability that affects work"', add
label define disabwrk_lbl 2 `"Disability limits but does not prevent work"', add
label define disabwrk_lbl 3 `"Disability prevents work"', add
label define disabwrk_lbl 4 `"Difficulty working"', add
label values disabwrk disabwrk_lbl

label define vetdisab_lbl 0 `"N/A"'
label define vetdisab_lbl 1 `"No disability rating"', add
label define vetdisab_lbl 2 `"0 percent disability rating"', add
label define vetdisab_lbl 3 `"10 or 20 percent disability rating"', add
label define vetdisab_lbl 4 `"30 or 40 percent"', add
label define vetdisab_lbl 5 `"50 or 60 percent"', add
label define vetdisab_lbl 6 `"70 percent or higher"', add
label define vetdisab_lbl 9 `"Has disability rating, level not reported"', add
label values vetdisab vetdisab_lbl

label define diffrem_lbl 0 `"N/A"'
label define diffrem_lbl 1 `"No cognitive difficulty"', add
label define diffrem_lbl 2 `"Has cognitive difficulty"', add
label values diffrem diffrem_lbl

label define diffphys_lbl 0 `"N/A"'
label define diffphys_lbl 1 `"No ambulatory difficulty"', add
label define diffphys_lbl 2 `"Has ambulatory difficulty"', add
label values diffphys diffphys_lbl

label define diffmob_lbl 0 `"N/A"'
label define diffmob_lbl 1 `"No independent living difficulty"', add
label define diffmob_lbl 2 `"Has independent living difficulty"', add
label values diffmob diffmob_lbl

label define diffcare_lbl 0 `"N/A"'
label define diffcare_lbl 1 `"No"', add
label define diffcare_lbl 2 `"Yes"', add
label values diffcare diffcare_lbl

label define diffsens_lbl 0 `"N/A"'
label define diffsens_lbl 1 `"No vision or hearing difficulty"', add
label define diffsens_lbl 2 `"Has vision or hearing difficulty"', add
label values diffsens diffsens_lbl

label define vetstat_lbl 0 `"N/A"'
label define vetstat_lbl 1 `"Not a veteran"', add
label define vetstat_lbl 2 `"Veteran"', add
label define vetstat_lbl 9 `"Unknown"', add
label values vetstat vetstat_lbl

label define vetstatd_lbl 00 `"N/A"'
label define vetstatd_lbl 10 `"Not a veteran"', add
label define vetstatd_lbl 11 `"No military service"', add
label define vetstatd_lbl 12 `"Currently on active duty"', add
label define vetstatd_lbl 13 `"Training for Reserves or National Guard only"', add
label define vetstatd_lbl 20 `"Veteran"', add
label define vetstatd_lbl 21 `"Veteran, on active duty prior to past year"', add
label define vetstatd_lbl 22 `"Veteran, on active duty in past year"', add
label define vetstatd_lbl 23 `"Veteran, on active duty in Reserves or National Guard only"', add
label define vetstatd_lbl 99 `"Unknown"', add
label values vetstatd vetstatd_lbl

label define pwstate2_lbl 00 `"N/A"'
label define pwstate2_lbl 01 `"Alabama"', add
label define pwstate2_lbl 02 `"Alaska"', add
label define pwstate2_lbl 04 `"Arizona"', add
label define pwstate2_lbl 05 `"Arkansas"', add
label define pwstate2_lbl 06 `"California"', add
label define pwstate2_lbl 08 `"Colorado"', add
label define pwstate2_lbl 09 `"Connecticut"', add
label define pwstate2_lbl 10 `"Delaware"', add
label define pwstate2_lbl 11 `"District of Columbia"', add
label define pwstate2_lbl 12 `"Florida"', add
label define pwstate2_lbl 13 `"Georgia"', add
label define pwstate2_lbl 15 `"Hawaii"', add
label define pwstate2_lbl 16 `"Idaho"', add
label define pwstate2_lbl 17 `"Illinois"', add
label define pwstate2_lbl 18 `"Indiana"', add
label define pwstate2_lbl 19 `"Iowa"', add
label define pwstate2_lbl 20 `"Kansas"', add
label define pwstate2_lbl 21 `"Kentucky"', add
label define pwstate2_lbl 22 `"Louisiana"', add
label define pwstate2_lbl 23 `"Maine"', add
label define pwstate2_lbl 24 `"Maryland"', add
label define pwstate2_lbl 25 `"Massachusetts"', add
label define pwstate2_lbl 26 `"Michigan"', add
label define pwstate2_lbl 27 `"Minnesota"', add
label define pwstate2_lbl 28 `"Mississippi"', add
label define pwstate2_lbl 29 `"Missouri"', add
label define pwstate2_lbl 30 `"Montana"', add
label define pwstate2_lbl 31 `"Nebraska"', add
label define pwstate2_lbl 32 `"Nevada"', add
label define pwstate2_lbl 33 `"New Hampshire"', add
label define pwstate2_lbl 34 `"New Jersey"', add
label define pwstate2_lbl 35 `"New Mexico"', add
label define pwstate2_lbl 36 `"New York"', add
label define pwstate2_lbl 37 `"North Carolina"', add
label define pwstate2_lbl 38 `"North Dakota"', add
label define pwstate2_lbl 39 `"Ohio"', add
label define pwstate2_lbl 40 `"Oklahoma"', add
label define pwstate2_lbl 41 `"Oregon"', add
label define pwstate2_lbl 42 `"Pennsylvania"', add
label define pwstate2_lbl 44 `"Rhode Island"', add
label define pwstate2_lbl 45 `"South Carolina"', add
label define pwstate2_lbl 46 `"South Dakota"', add
label define pwstate2_lbl 47 `"Tennessee"', add
label define pwstate2_lbl 48 `"Texas"', add
label define pwstate2_lbl 49 `"Utah"', add
label define pwstate2_lbl 50 `"Vermont"', add
label define pwstate2_lbl 51 `"Virginia"', add
label define pwstate2_lbl 53 `"Washington"', add
label define pwstate2_lbl 54 `"West Virginia"', add
label define pwstate2_lbl 55 `"Wisconsin"', add
label define pwstate2_lbl 56 `"Wyoming"', add
label define pwstate2_lbl 61 `"Maine-New Hamp-Vermont"', add
label define pwstate2_lbl 62 `"Massachusetts-Rhode Island"', add
label define pwstate2_lbl 63 `"Minn-Iowa-Missouri-Kansas-S Dakota-N Dakota"', add
label define pwstate2_lbl 64 `"Mayrland-Delaware"', add
label define pwstate2_lbl 65 `"Montana-Idaho-Wyoming"', add
label define pwstate2_lbl 66 `"Utah-Nevada"', add
label define pwstate2_lbl 67 `"Arizona-New Mexico"', add
label define pwstate2_lbl 68 `"Alaska-Hawaii"', add
label define pwstate2_lbl 72 `"Puerto Rico"', add
label define pwstate2_lbl 73 `"U.S. outlying area"', add
label define pwstate2_lbl 74 `"United States (1980 Puerto Rico samples)"', add
label define pwstate2_lbl 80 `"Abroad"', add
label define pwstate2_lbl 81 `"Europe"', add
label define pwstate2_lbl 82 `"Eastern Asia"', add
label define pwstate2_lbl 83 `"South Central, South East, and Western Asia"', add
label define pwstate2_lbl 84 `"Mexico"', add
label define pwstate2_lbl 85 `"Other Americas"', add
label define pwstate2_lbl 86 `"Other, nec"', add
label define pwstate2_lbl 87 `"Iraq"', add
label define pwstate2_lbl 88 `"Canada"', add
label define pwstate2_lbl 90 `"Confidential"', add
label define pwstate2_lbl 99 `"Not reported"', add
label values pwstate2 pwstate2_lbl

label define tranwork_lbl 00 `"N/A"'
label define tranwork_lbl 10 `"Auto, truck, or van"', add
label define tranwork_lbl 11 `"Auto"', add
label define tranwork_lbl 12 `"Driver"', add
label define tranwork_lbl 13 `"Passenger"', add
label define tranwork_lbl 14 `"Truck"', add
label define tranwork_lbl 15 `"Van"', add
label define tranwork_lbl 20 `"Motorcycle"', add
label define tranwork_lbl 31 `"Bus"', add
label define tranwork_lbl 32 `"Bus or trolley bus"', add
label define tranwork_lbl 33 `"Bus or streetcar"', add
label define tranwork_lbl 34 `"Light rail, streetcar, or trolley (Carro público in PR)"', add
label define tranwork_lbl 35 `"Streetcar or trolley car (publico in Puerto Rico, 2000)"', add
label define tranwork_lbl 36 `"Subway or elevated"', add
label define tranwork_lbl 37 `"Long-distance train or commuter train"', add
label define tranwork_lbl 38 `"Taxicab or ride-hailing services"', add
label define tranwork_lbl 39 `"Ferryboat"', add
label define tranwork_lbl 50 `"Bicycle"', add
label define tranwork_lbl 60 `"Walked only"', add
label define tranwork_lbl 70 `"Other"', add
label define tranwork_lbl 80 `"Worked at home"', add
label values tranwork tranwork_lbl

label define carpool_lbl 0 `"N/A"'
label define carpool_lbl 1 `"Drives alone"', add
label define carpool_lbl 2 `"Carpools"', add
label define carpool_lbl 3 `"Shares driving"', add
label define carpool_lbl 4 `"Drives others only"', add
label define carpool_lbl 5 `"Passenger only"', add
label values carpool carpool_lbl

label define riders_lbl 0 `"N/A"'
label define riders_lbl 1 `"Drives alone"', add
label define riders_lbl 2 `"2 people"', add
label define riders_lbl 3 `"3"', add
label define riders_lbl 4 `"4"', add
label define riders_lbl 5 `"5"', add
label define riders_lbl 6 `"6"', add
label define riders_lbl 7 `"7+ (1980,2000)"', add
label define riders_lbl 8 `"7-9 (1990,ACS,PRCS)"', add
label define riders_lbl 9 `"10 or more (1990,ACS,PRCS)"', add
label values riders riders_lbl

label define departs_lbl 0000 `"0000"'
label define departs_lbl 0015 `"0015"', add
label define departs_lbl 0045 `"0045"', add
label define departs_lbl 0115 `"0115"', add
label define departs_lbl 0145 `"0145"', add
label define departs_lbl 0215 `"0215"', add
label define departs_lbl 0245 `"0245"', add
label define departs_lbl 0305 `"0305"', add
label define departs_lbl 0315 `"0315"', add
label define departs_lbl 0325 `"0325"', add
label define departs_lbl 0335 `"0335"', add
label define departs_lbl 0345 `"0345"', add
label define departs_lbl 0355 `"0355"', add
label define departs_lbl 0405 `"0405"', add
label define departs_lbl 0415 `"0415"', add
label define departs_lbl 0425 `"0425"', add
label define departs_lbl 0435 `"0435"', add
label define departs_lbl 0445 `"0445"', add
label define departs_lbl 0455 `"0455"', add
label define departs_lbl 0502 `"0502"', add
label define departs_lbl 0507 `"0507"', add
label define departs_lbl 0512 `"0512"', add
label define departs_lbl 0517 `"0517"', add
label define departs_lbl 0522 `"0522"', add
label define departs_lbl 0527 `"0527"', add
label define departs_lbl 0532 `"0532"', add
label define departs_lbl 0537 `"0537"', add
label define departs_lbl 0542 `"0542"', add
label define departs_lbl 0547 `"0547"', add
label define departs_lbl 0552 `"0552"', add
label define departs_lbl 0557 `"0557"', add
label define departs_lbl 0602 `"0602"', add
label define departs_lbl 0607 `"0607"', add
label define departs_lbl 0612 `"0612"', add
label define departs_lbl 0617 `"0617"', add
label define departs_lbl 0622 `"0622"', add
label define departs_lbl 0627 `"0627"', add
label define departs_lbl 0632 `"0632"', add
label define departs_lbl 0637 `"0637"', add
label define departs_lbl 0642 `"0642"', add
label define departs_lbl 0647 `"0647"', add
label define departs_lbl 0652 `"0652"', add
label define departs_lbl 0657 `"0657"', add
label define departs_lbl 0702 `"0702"', add
label define departs_lbl 0707 `"0707"', add
label define departs_lbl 0712 `"0712"', add
label define departs_lbl 0717 `"0717"', add
label define departs_lbl 0722 `"0722"', add
label define departs_lbl 0727 `"0727"', add
label define departs_lbl 0732 `"0732"', add
label define departs_lbl 0737 `"0737"', add
label define departs_lbl 0742 `"0742"', add
label define departs_lbl 0747 `"0747"', add
label define departs_lbl 0752 `"0752"', add
label define departs_lbl 0757 `"0757"', add
label define departs_lbl 0802 `"0802"', add
label define departs_lbl 0807 `"0807"', add
label define departs_lbl 0812 `"0812"', add
label define departs_lbl 0817 `"0817"', add
label define departs_lbl 0822 `"0822"', add
label define departs_lbl 0827 `"0827"', add
label define departs_lbl 0832 `"0832"', add
label define departs_lbl 0837 `"0837"', add
label define departs_lbl 0842 `"0842"', add
label define departs_lbl 0847 `"0847"', add
label define departs_lbl 0852 `"0852"', add
label define departs_lbl 0857 `"0857"', add
label define departs_lbl 0902 `"0902"', add
label define departs_lbl 0907 `"0907"', add
label define departs_lbl 0912 `"0912"', add
label define departs_lbl 0917 `"0917"', add
label define departs_lbl 0922 `"0922"', add
label define departs_lbl 0927 `"0927"', add
label define departs_lbl 0932 `"0932"', add
label define departs_lbl 0937 `"0937"', add
label define departs_lbl 0942 `"0942"', add
label define departs_lbl 0947 `"0947"', add
label define departs_lbl 0952 `"0952"', add
label define departs_lbl 0957 `"0957"', add
label define departs_lbl 1002 `"1002"', add
label define departs_lbl 1005 `"1005"', add
label define departs_lbl 1007 `"1007"', add
label define departs_lbl 1012 `"1012"', add
label define departs_lbl 1015 `"1015"', add
label define departs_lbl 1017 `"1017"', add
label define departs_lbl 1022 `"1022"', add
label define departs_lbl 1025 `"1025"', add
label define departs_lbl 1027 `"1027"', add
label define departs_lbl 1032 `"1032"', add
label define departs_lbl 1035 `"1035"', add
label define departs_lbl 1037 `"1037"', add
label define departs_lbl 1042 `"1042"', add
label define departs_lbl 1045 `"1045"', add
label define departs_lbl 1047 `"1047"', add
label define departs_lbl 1052 `"1052"', add
label define departs_lbl 1055 `"1055"', add
label define departs_lbl 1057 `"1057"', add
label define departs_lbl 1105 `"1105"', add
label define departs_lbl 1115 `"1115"', add
label define departs_lbl 1125 `"1125"', add
label define departs_lbl 1135 `"1135"', add
label define departs_lbl 1145 `"1145"', add
label define departs_lbl 1155 `"1155"', add
label define departs_lbl 1205 `"1205"', add
label define departs_lbl 1215 `"1215"', add
label define departs_lbl 1225 `"1225"', add
label define departs_lbl 1235 `"1235"', add
label define departs_lbl 1245 `"1245"', add
label define departs_lbl 1255 `"1255"', add
label define departs_lbl 1305 `"1305"', add
label define departs_lbl 1315 `"1315"', add
label define departs_lbl 1325 `"1325"', add
label define departs_lbl 1335 `"1335"', add
label define departs_lbl 1345 `"1345"', add
label define departs_lbl 1355 `"1355"', add
label define departs_lbl 1405 `"1405"', add
label define departs_lbl 1415 `"1415"', add
label define departs_lbl 1425 `"1425"', add
label define departs_lbl 1435 `"1435"', add
label define departs_lbl 1445 `"1445"', add
label define departs_lbl 1455 `"1455"', add
label define departs_lbl 1505 `"1505"', add
label define departs_lbl 1515 `"1515"', add
label define departs_lbl 1525 `"1525"', add
label define departs_lbl 1535 `"1535"', add
label define departs_lbl 1545 `"1545"', add
label define departs_lbl 1555 `"1555"', add
label define departs_lbl 1605 `"1605"', add
label define departs_lbl 1615 `"1615"', add
label define departs_lbl 1625 `"1625"', add
label define departs_lbl 1635 `"1635"', add
label define departs_lbl 1645 `"1645"', add
label define departs_lbl 1655 `"1655"', add
label define departs_lbl 1705 `"1705"', add
label define departs_lbl 1715 `"1715"', add
label define departs_lbl 1725 `"1725"', add
label define departs_lbl 1735 `"1735"', add
label define departs_lbl 1745 `"1745"', add
label define departs_lbl 1755 `"1755"', add
label define departs_lbl 1805 `"1805"', add
label define departs_lbl 1815 `"1815"', add
label define departs_lbl 1825 `"1825"', add
label define departs_lbl 1835 `"1835"', add
label define departs_lbl 1845 `"1845"', add
label define departs_lbl 1855 `"1855"', add
label define departs_lbl 1905 `"1905"', add
label define departs_lbl 1915 `"1915"', add
label define departs_lbl 1920 `"1920"', add
label define departs_lbl 1925 `"1925"', add
label define departs_lbl 1935 `"1935"', add
label define departs_lbl 1945 `"1945"', add
label define departs_lbl 1955 `"1955"', add
label define departs_lbl 2005 `"2005"', add
label define departs_lbl 2015 `"2015"', add
label define departs_lbl 2020 `"2020"', add
label define departs_lbl 2025 `"2025"', add
label define departs_lbl 2035 `"2035"', add
label define departs_lbl 2045 `"2045"', add
label define departs_lbl 2050 `"2050"', add
label define departs_lbl 2055 `"2055"', add
label define departs_lbl 2105 `"2105"', add
label define departs_lbl 2115 `"2115"', add
label define departs_lbl 2125 `"2125"', add
label define departs_lbl 2135 `"2135"', add
label define departs_lbl 2145 `"2145"', add
label define departs_lbl 2155 `"2155"', add
label define departs_lbl 2205 `"2205"', add
label define departs_lbl 2215 `"2215"', add
label define departs_lbl 2225 `"2225"', add
label define departs_lbl 2235 `"2235"', add
label define departs_lbl 2245 `"2245"', add
label define departs_lbl 2255 `"2255"', add
label define departs_lbl 2305 `"2305"', add
label define departs_lbl 2315 `"2315"', add
label define departs_lbl 2325 `"2325"', add
label define departs_lbl 2335 `"2335"', add
label define departs_lbl 2345 `"2345"', add
label define departs_lbl 2350 `"2350"', add
label define departs_lbl 2355 `"2355"', add
label values departs departs_lbl

label define arrives_lbl 0000 `"0000"'
label define arrives_lbl 0004 `"0004"', add
label define arrives_lbl 0009 `"0009"', add
label define arrives_lbl 0014 `"0014"', add
label define arrives_lbl 0019 `"0019"', add
label define arrives_lbl 0024 `"0024"', add
label define arrives_lbl 0029 `"0029"', add
label define arrives_lbl 0039 `"0039"', add
label define arrives_lbl 0044 `"0044"', add
label define arrives_lbl 0049 `"0049"', add
label define arrives_lbl 0059 `"0059"', add
label define arrives_lbl 0104 `"0104"', add
label define arrives_lbl 0109 `"0109"', add
label define arrives_lbl 0114 `"0114"', add
label define arrives_lbl 0119 `"0119"', add
label define arrives_lbl 0124 `"0124"', add
label define arrives_lbl 0129 `"0129"', add
label define arrives_lbl 0134 `"0134"', add
label define arrives_lbl 0139 `"0139"', add
label define arrives_lbl 0144 `"0144"', add
label define arrives_lbl 0149 `"0149"', add
label define arrives_lbl 0159 `"0159"', add
label define arrives_lbl 0204 `"0204"', add
label define arrives_lbl 0209 `"0209"', add
label define arrives_lbl 0214 `"0214"', add
label define arrives_lbl 0219 `"0219"', add
label define arrives_lbl 0224 `"0224"', add
label define arrives_lbl 0229 `"0229"', add
label define arrives_lbl 0234 `"0234"', add
label define arrives_lbl 0239 `"0239"', add
label define arrives_lbl 0244 `"0244"', add
label define arrives_lbl 0249 `"0249"', add
label define arrives_lbl 0254 `"0254"', add
label define arrives_lbl 0259 `"0259"', add
label define arrives_lbl 0304 `"0304"', add
label define arrives_lbl 0309 `"0309"', add
label define arrives_lbl 0314 `"0314"', add
label define arrives_lbl 0319 `"0319"', add
label define arrives_lbl 0324 `"0324"', add
label define arrives_lbl 0329 `"0329"', add
label define arrives_lbl 0334 `"0334"', add
label define arrives_lbl 0339 `"0339"', add
label define arrives_lbl 0344 `"0344"', add
label define arrives_lbl 0349 `"0349"', add
label define arrives_lbl 0354 `"0354"', add
label define arrives_lbl 0359 `"0359"', add
label define arrives_lbl 0404 `"0404"', add
label define arrives_lbl 0409 `"0409"', add
label define arrives_lbl 0414 `"0414"', add
label define arrives_lbl 0419 `"0419"', add
label define arrives_lbl 0424 `"0424"', add
label define arrives_lbl 0429 `"0429"', add
label define arrives_lbl 0434 `"0434"', add
label define arrives_lbl 0439 `"0439"', add
label define arrives_lbl 0444 `"0444"', add
label define arrives_lbl 0449 `"0449"', add
label define arrives_lbl 0454 `"0454"', add
label define arrives_lbl 0459 `"0459"', add
label define arrives_lbl 0504 `"0504"', add
label define arrives_lbl 0509 `"0509"', add
label define arrives_lbl 0514 `"0514"', add
label define arrives_lbl 0519 `"0519"', add
label define arrives_lbl 0524 `"0524"', add
label define arrives_lbl 0529 `"0529"', add
label define arrives_lbl 0534 `"0534"', add
label define arrives_lbl 0539 `"0539"', add
label define arrives_lbl 0544 `"0544"', add
label define arrives_lbl 0549 `"0549"', add
label define arrives_lbl 0554 `"0554"', add
label define arrives_lbl 0559 `"0559"', add
label define arrives_lbl 0604 `"0604"', add
label define arrives_lbl 0609 `"0609"', add
label define arrives_lbl 0614 `"0614"', add
label define arrives_lbl 0619 `"0619"', add
label define arrives_lbl 0624 `"0624"', add
label define arrives_lbl 0629 `"0629"', add
label define arrives_lbl 0634 `"0634"', add
label define arrives_lbl 0639 `"0639"', add
label define arrives_lbl 0644 `"0644"', add
label define arrives_lbl 0649 `"0649"', add
label define arrives_lbl 0654 `"0654"', add
label define arrives_lbl 0659 `"0659"', add
label define arrives_lbl 0704 `"0704"', add
label define arrives_lbl 0709 `"0709"', add
label define arrives_lbl 0714 `"0714"', add
label define arrives_lbl 0719 `"0719"', add
label define arrives_lbl 0724 `"0724"', add
label define arrives_lbl 0729 `"0729"', add
label define arrives_lbl 0734 `"0734"', add
label define arrives_lbl 0739 `"0739"', add
label define arrives_lbl 0744 `"0744"', add
label define arrives_lbl 0749 `"0749"', add
label define arrives_lbl 0754 `"0754"', add
label define arrives_lbl 0759 `"0759"', add
label define arrives_lbl 0804 `"0804"', add
label define arrives_lbl 0809 `"0809"', add
label define arrives_lbl 0814 `"0814"', add
label define arrives_lbl 0819 `"0819"', add
label define arrives_lbl 0824 `"0824"', add
label define arrives_lbl 0829 `"0829"', add
label define arrives_lbl 0834 `"0834"', add
label define arrives_lbl 0839 `"0839"', add
label define arrives_lbl 0844 `"0844"', add
label define arrives_lbl 0849 `"0849"', add
label define arrives_lbl 0854 `"0854"', add
label define arrives_lbl 0859 `"0859"', add
label define arrives_lbl 0904 `"0904"', add
label define arrives_lbl 0909 `"0909"', add
label define arrives_lbl 0914 `"0914"', add
label define arrives_lbl 0919 `"0919"', add
label define arrives_lbl 0924 `"0924"', add
label define arrives_lbl 0929 `"0929"', add
label define arrives_lbl 0934 `"0934"', add
label define arrives_lbl 0939 `"0939"', add
label define arrives_lbl 0944 `"0944"', add
label define arrives_lbl 0949 `"0949"', add
label define arrives_lbl 0954 `"0954"', add
label define arrives_lbl 0959 `"0959"', add
label define arrives_lbl 1004 `"1004"', add
label define arrives_lbl 1009 `"1009"', add
label define arrives_lbl 1014 `"1014"', add
label define arrives_lbl 1019 `"1019"', add
label define arrives_lbl 1024 `"1024"', add
label define arrives_lbl 1029 `"1029"', add
label define arrives_lbl 1034 `"1034"', add
label define arrives_lbl 1039 `"1039"', add
label define arrives_lbl 1044 `"1044"', add
label define arrives_lbl 1049 `"1049"', add
label define arrives_lbl 1054 `"1054"', add
label define arrives_lbl 1059 `"1059"', add
label define arrives_lbl 1104 `"1104"', add
label define arrives_lbl 1109 `"1109"', add
label define arrives_lbl 1114 `"1114"', add
label define arrives_lbl 1119 `"1119"', add
label define arrives_lbl 1124 `"1124"', add
label define arrives_lbl 1129 `"1129"', add
label define arrives_lbl 1134 `"1134"', add
label define arrives_lbl 1139 `"1139"', add
label define arrives_lbl 1144 `"1144"', add
label define arrives_lbl 1149 `"1149"', add
label define arrives_lbl 1154 `"1154"', add
label define arrives_lbl 1159 `"1159"', add
label define arrives_lbl 1204 `"1204"', add
label define arrives_lbl 1209 `"1209"', add
label define arrives_lbl 1214 `"1214"', add
label define arrives_lbl 1219 `"1219"', add
label define arrives_lbl 1224 `"1224"', add
label define arrives_lbl 1229 `"1229"', add
label define arrives_lbl 1234 `"1234"', add
label define arrives_lbl 1239 `"1239"', add
label define arrives_lbl 1244 `"1244"', add
label define arrives_lbl 1249 `"1249"', add
label define arrives_lbl 1254 `"1254"', add
label define arrives_lbl 1259 `"1259"', add
label define arrives_lbl 1304 `"1304"', add
label define arrives_lbl 1309 `"1309"', add
label define arrives_lbl 1314 `"1314"', add
label define arrives_lbl 1319 `"1319"', add
label define arrives_lbl 1324 `"1324"', add
label define arrives_lbl 1329 `"1329"', add
label define arrives_lbl 1334 `"1334"', add
label define arrives_lbl 1339 `"1339"', add
label define arrives_lbl 1344 `"1344"', add
label define arrives_lbl 1349 `"1349"', add
label define arrives_lbl 1354 `"1354"', add
label define arrives_lbl 1359 `"1359"', add
label define arrives_lbl 1404 `"1404"', add
label define arrives_lbl 1409 `"1409"', add
label define arrives_lbl 1414 `"1414"', add
label define arrives_lbl 1419 `"1419"', add
label define arrives_lbl 1424 `"1424"', add
label define arrives_lbl 1429 `"1429"', add
label define arrives_lbl 1434 `"1434"', add
label define arrives_lbl 1439 `"1439"', add
label define arrives_lbl 1444 `"1444"', add
label define arrives_lbl 1449 `"1449"', add
label define arrives_lbl 1454 `"1454"', add
label define arrives_lbl 1459 `"1459"', add
label define arrives_lbl 1504 `"1504"', add
label define arrives_lbl 1509 `"1509"', add
label define arrives_lbl 1514 `"1514"', add
label define arrives_lbl 1519 `"1519"', add
label define arrives_lbl 1524 `"1524"', add
label define arrives_lbl 1529 `"1529"', add
label define arrives_lbl 1534 `"1534"', add
label define arrives_lbl 1539 `"1539"', add
label define arrives_lbl 1544 `"1544"', add
label define arrives_lbl 1549 `"1549"', add
label define arrives_lbl 1554 `"1554"', add
label define arrives_lbl 1559 `"1559"', add
label define arrives_lbl 1604 `"1604"', add
label define arrives_lbl 1609 `"1609"', add
label define arrives_lbl 1614 `"1614"', add
label define arrives_lbl 1619 `"1619"', add
label define arrives_lbl 1624 `"1624"', add
label define arrives_lbl 1629 `"1629"', add
label define arrives_lbl 1634 `"1634"', add
label define arrives_lbl 1639 `"1639"', add
label define arrives_lbl 1644 `"1644"', add
label define arrives_lbl 1649 `"1649"', add
label define arrives_lbl 1654 `"1654"', add
label define arrives_lbl 1659 `"1659"', add
label define arrives_lbl 1704 `"1704"', add
label define arrives_lbl 1709 `"1709"', add
label define arrives_lbl 1714 `"1714"', add
label define arrives_lbl 1719 `"1719"', add
label define arrives_lbl 1724 `"1724"', add
label define arrives_lbl 1729 `"1729"', add
label define arrives_lbl 1734 `"1734"', add
label define arrives_lbl 1739 `"1739"', add
label define arrives_lbl 1744 `"1744"', add
label define arrives_lbl 1749 `"1749"', add
label define arrives_lbl 1754 `"1754"', add
label define arrives_lbl 1759 `"1759"', add
label define arrives_lbl 1804 `"1804"', add
label define arrives_lbl 1809 `"1809"', add
label define arrives_lbl 1814 `"1814"', add
label define arrives_lbl 1819 `"1819"', add
label define arrives_lbl 1824 `"1824"', add
label define arrives_lbl 1829 `"1829"', add
label define arrives_lbl 1834 `"1834"', add
label define arrives_lbl 1839 `"1839"', add
label define arrives_lbl 1844 `"1844"', add
label define arrives_lbl 1849 `"1849"', add
label define arrives_lbl 1854 `"1854"', add
label define arrives_lbl 1859 `"1859"', add
label define arrives_lbl 1904 `"1904"', add
label define arrives_lbl 1909 `"1909"', add
label define arrives_lbl 1914 `"1914"', add
label define arrives_lbl 1919 `"1919"', add
label define arrives_lbl 1924 `"1924"', add
label define arrives_lbl 1929 `"1929"', add
label define arrives_lbl 1934 `"1934"', add
label define arrives_lbl 1939 `"1939"', add
label define arrives_lbl 1944 `"1944"', add
label define arrives_lbl 1949 `"1949"', add
label define arrives_lbl 1954 `"1954"', add
label define arrives_lbl 1959 `"1959"', add
label define arrives_lbl 2004 `"2004"', add
label define arrives_lbl 2009 `"2009"', add
label define arrives_lbl 2014 `"2014"', add
label define arrives_lbl 2019 `"2019"', add
label define arrives_lbl 2024 `"2024"', add
label define arrives_lbl 2029 `"2029"', add
label define arrives_lbl 2034 `"2034"', add
label define arrives_lbl 2039 `"2039"', add
label define arrives_lbl 2044 `"2044"', add
label define arrives_lbl 2049 `"2049"', add
label define arrives_lbl 2054 `"2054"', add
label define arrives_lbl 2059 `"2059"', add
label define arrives_lbl 2104 `"2104"', add
label define arrives_lbl 2109 `"2109"', add
label define arrives_lbl 2114 `"2114"', add
label define arrives_lbl 2119 `"2119"', add
label define arrives_lbl 2124 `"2124"', add
label define arrives_lbl 2129 `"2129"', add
label define arrives_lbl 2134 `"2134"', add
label define arrives_lbl 2139 `"2139"', add
label define arrives_lbl 2144 `"2144"', add
label define arrives_lbl 2149 `"2149"', add
label define arrives_lbl 2154 `"2154"', add
label define arrives_lbl 2159 `"2159"', add
label define arrives_lbl 2204 `"2204"', add
label define arrives_lbl 2209 `"2209"', add
label define arrives_lbl 2214 `"2214"', add
label define arrives_lbl 2219 `"2219"', add
label define arrives_lbl 2224 `"2224"', add
label define arrives_lbl 2229 `"2229"', add
label define arrives_lbl 2234 `"2234"', add
label define arrives_lbl 2239 `"2239"', add
label define arrives_lbl 2244 `"2244"', add
label define arrives_lbl 2249 `"2249"', add
label define arrives_lbl 2254 `"2254"', add
label define arrives_lbl 2259 `"2259"', add
label define arrives_lbl 2304 `"2304"', add
label define arrives_lbl 2309 `"2309"', add
label define arrives_lbl 2314 `"2314"', add
label define arrives_lbl 2319 `"2319"', add
label define arrives_lbl 2324 `"2324"', add
label define arrives_lbl 2329 `"2329"', add
label define arrives_lbl 2334 `"2334"', add
label define arrives_lbl 2339 `"2339"', add
label define arrives_lbl 2344 `"2344"', add
label define arrives_lbl 2349 `"2349"', add
label define arrives_lbl 2354 `"2354"', add
label define arrives_lbl 2359 `"2359"', add
label define arrives_lbl 8888 `"Suppressed for data year 2023 for select PUMAs"', add
label values arrives arrives_lbl

label define qage_lbl 0 `"Entered as written"'
label define qage_lbl 1 `"Failed edit"', add
label define qage_lbl 2 `"Illegible"', add
label define qage_lbl 3 `"Missing"', add
label define qage_lbl 4 `"Allocated"', add
label define qage_lbl 5 `"Illegible"', add
label define qage_lbl 6 `"Missing"', add
label define qage_lbl 7 `"Original entry illegible"', add
label define qage_lbl 8 `"Original entry missing or failed edit"', add
label values qage qage_lbl

label define qmarst_lbl 0 `"Entered as written"'
label define qmarst_lbl 1 `"Failed edit"', add
label define qmarst_lbl 2 `"Illegible"', add
label define qmarst_lbl 3 `"Missing"', add
label define qmarst_lbl 4 `"Allocated"', add
label define qmarst_lbl 5 `"Illegible"', add
label define qmarst_lbl 6 `"Missing"', add
label define qmarst_lbl 7 `"Original entry illegible"', add
label define qmarst_lbl 8 `"Original entry missing or failed edit"', add
label values qmarst qmarst_lbl

label define qrelate_lbl 0 `"Not edited"'
label define qrelate_lbl 1 `"Logical edit"', add
label define qrelate_lbl 2 `"Logical edit"', add
label define qrelate_lbl 3 `"Logical edit"', add
label define qrelate_lbl 4 `"Allocated"', add
label define qrelate_lbl 5 `"Allocated"', add
label define qrelate_lbl 6 `"Allocated"', add
label define qrelate_lbl 7 `"Cold deck allocation"', add
label define qrelate_lbl 8 `"Cold deck allocation"', add
label define qrelate_lbl 9 `"Same sex spouse changed to unmarried partner"', add
label values qrelate qrelate_lbl

label define qsex_lbl 0 `"Entered as written"'
label define qsex_lbl 1 `"Failed edit"', add
label define qsex_lbl 2 `"Illegible"', add
label define qsex_lbl 3 `"Missing"', add
label define qsex_lbl 4 `"Allocated"', add
label define qsex_lbl 5 `"Illegible"', add
label define qsex_lbl 6 `"Missing"', add
label define qsex_lbl 7 `"Original entry illegible"', add
label define qsex_lbl 8 `"Original entry missing or failed edit"', add
label values qsex qsex_lbl

label define qbpl_lbl 0 `"Entered as written"'
label define qbpl_lbl 1 `"Specific U.S. state or foreign country of birth pre-edited or not reported (1980 Puerto Rico)"', add
label define qbpl_lbl 2 `"Failed edit/illegible"', add
label define qbpl_lbl 3 `"Consistency edit"', add
label define qbpl_lbl 4 `"Allocated"', add
label define qbpl_lbl 5 `"Both general and specific response allocated (1980 Puerto Rico)"', add
label define qbpl_lbl 6 `"Failed edit/missing"', add
label define qbpl_lbl 7 `"Illegible"', add
label define qbpl_lbl 8 `"Illegible/missing or failed edit"', add
label values qbpl qbpl_lbl

label define qcitizen_lbl 0 `"Original entry or Inapplicable (not in universe)"'
label define qcitizen_lbl 1 `"Failed edit"', add
label define qcitizen_lbl 2 `"Illegible"', add
label define qcitizen_lbl 3 `"Missing"', add
label define qcitizen_lbl 4 `"Allocated"', add
label define qcitizen_lbl 5 `"Illegible"', add
label define qcitizen_lbl 6 `"Missing"', add
label define qcitizen_lbl 7 `"Original entry illegible"', add
label define qcitizen_lbl 8 `"Original entry missing or failed edit"', add
label values qcitizen qcitizen_lbl

label define qhispan_lbl 0 `"Not allocated"'
label define qhispan_lbl 1 `"Allocated from information for this person or from relative, this household"', add
label define qhispan_lbl 2 `"Allocated from nonrelative, this household"', add
label define qhispan_lbl 4 `"Allocated"', add
label values qhispan qhispan_lbl

label define qlanguag_lbl 0 `"Not allocated or N/A"'
label define qlanguag_lbl 3 `"Consistency edit"', add
label define qlanguag_lbl 4 `"Allocated, pre-edit"', add
label values qlanguag qlanguag_lbl

label define qrace_lbl 0 `"Entered as written"'
label define qrace_lbl 1 `"Failed edit"', add
label define qrace_lbl 2 `"Illegible"', add
label define qrace_lbl 3 `"Missing"', add
label define qrace_lbl 4 `"Allocated"', add
label define qrace_lbl 5 `"Allocated, hot deck"', add
label define qrace_lbl 6 `"Missing"', add
label define qrace_lbl 7 `"Original entry illegible"', add
label define qrace_lbl 8 `"Original entry missing or failed edit"', add
label values qrace qrace_lbl

label define qspeaken_lbl 0 `"Not allocated"'
label define qspeaken_lbl 3 `"Consistency edit"', add
label define qspeaken_lbl 4 `"Allocated, hot deck"', add
label values qspeaken qspeaken_lbl

label define qyrimm_lbl 0 `"Fields OK as written"'
label define qyrimm_lbl 1 `"Altered by coders"', add
label define qyrimm_lbl 2 `"Logical hand edit by Census Office or by census sample research staff"', add
label define qyrimm_lbl 3 `"Consistency edit"', add
label define qyrimm_lbl 4 `"Allocated, hot deck"', add
label values qyrimm qyrimm_lbl

label define qyrnatur_lbl 0 `"Not Allocated"'
label define qyrnatur_lbl 4 `"Allocated"', add
label values qyrnatur qyrnatur_lbl

label define qeduc_lbl 0 `"Original entry or Inapplicable (not in universe)"'
label define qeduc_lbl 1 `"Failed edit"', add
label define qeduc_lbl 2 `"Failed edit/illegible"', add
label define qeduc_lbl 3 `"Failed edit/missing"', add
label define qeduc_lbl 4 `"Consistency edit"', add
label define qeduc_lbl 5 `"Consistency edit/allocated, hot deck"', add
label define qeduc_lbl 6 `"Failed edit/missing"', add
label define qeduc_lbl 7 `"Illegible"', add
label define qeduc_lbl 8 `"Illegible/missing or failed edit"', add
label values qeduc qeduc_lbl

label define qschool_lbl 0 `"Original entry or Inapplicable (not in universe)"'
label define qschool_lbl 1 `"Failed edit"', add
label define qschool_lbl 2 `"Illegible"', add
label define qschool_lbl 3 `"Missing"', add
label define qschool_lbl 4 `"Allocated"', add
label define qschool_lbl 5 `"Illegible"', add
label define qschool_lbl 6 `"Missing"', add
label define qschool_lbl 7 `"Original entry illegible"', add
label define qschool_lbl 8 `"Original entry missing or failed edit"', add
label values qschool qschool_lbl

label define qempstat_lbl 0 `"Original entry or Inapplicable (not in universe)"'
label define qempstat_lbl 1 `"Failed edit"', add
label define qempstat_lbl 2 `"Illegible"', add
label define qempstat_lbl 3 `"Missing"', add
label define qempstat_lbl 4 `"Allocated"', add
label define qempstat_lbl 5 `"Illegible"', add
label define qempstat_lbl 6 `"Missing"', add
label define qempstat_lbl 7 `"Original entry illegible"', add
label define qempstat_lbl 8 `"Original entry missing or failed edit"', add
label values qempstat qempstat_lbl

label define qocc_lbl 0 `"Entered as written"'
label define qocc_lbl 1 `"Failed edit"', add
label define qocc_lbl 2 `"Illegible"', add
label define qocc_lbl 3 `"Missing"', add
label define qocc_lbl 4 `"Allocated"', add
label define qocc_lbl 5 `"Illegible"', add
label define qocc_lbl 6 `"Missing"', add
label define qocc_lbl 7 `"Original entry illegible"', add
label define qocc_lbl 8 `"Original entry missing or failed edit"', add
label values qocc qocc_lbl

label define quhrswor_lbl 0 `"Not allocated"'
label define quhrswor_lbl 3 `"Allocated, direct"', add
label define quhrswor_lbl 4 `"Allocated"', add
label define quhrswor_lbl 5 `"Allocated, indirect"', add
label define quhrswor_lbl 9 `"Allocated, direct/indirect"', add
label values quhrswor quhrswor_lbl

label define qwkswork2_lbl 0 `"Original entry or Inapplicable (not in universe)"'
label define qwkswork2_lbl 1 `"Failed edit"', add
label define qwkswork2_lbl 2 `"Illegible"', add
label define qwkswork2_lbl 3 `"Missing"', add
label define qwkswork2_lbl 4 `"Allocated, pre-edit"', add
label define qwkswork2_lbl 5 `"Allocated, hot deck"', add
label define qwkswork2_lbl 6 `"Missing"', add
label define qwkswork2_lbl 7 `"Original entry illegible"', add
label define qwkswork2_lbl 8 `"Original entry missing or failed edit"', add
label values qwkswork2 qwkswork2_lbl

label define qworkedy_lbl 0 `"Not allocated"'
label define qworkedy_lbl 3 `"Allocated, consistency edit"', add
label define qworkedy_lbl 4 `"Allocated"', add
label values qworkedy qworkedy_lbl

label define qmigrat1_lbl 0 `"Not allocated"'
label define qmigrat1_lbl 1 `"Failed edit"', add
label define qmigrat1_lbl 2 `"Illegible"', add
label define qmigrat1_lbl 3 `"Missing"', add
label define qmigrat1_lbl 4 `"Allocated"', add
label define qmigrat1_lbl 5 `"Illegible"', add
label define qmigrat1_lbl 6 `"Missing"', add
label define qmigrat1_lbl 7 `"Original entry illegible"', add
label define qmigrat1_lbl 8 `"Original entry missing or failed edit"', add
label values qmigrat1 qmigrat1_lbl

label define spmpov_lbl 0 `"Not in poverty"'
label define spmpov_lbl 1 `"In poverty"', add
label define spmpov_lbl 9 `"N/A"', add
label values spmpov spmpov_lbl

label define offpov_lbl 0 `"Not in poverty"'
label define offpov_lbl 1 `"In poverty"', add
label define offpov_lbl 9 `"N/A"', add
label values offpov offpov_lbl


