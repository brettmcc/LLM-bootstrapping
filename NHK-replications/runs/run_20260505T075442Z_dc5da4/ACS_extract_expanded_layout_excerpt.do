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
  using `"usa_00045.dat"'

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
