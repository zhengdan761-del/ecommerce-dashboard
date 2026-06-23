
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import StringIO
import re

# =========================================================
# 原始報表資料
# =========================================================
RAW_DATA = """核心成效總覽

項目	數值
期間	2026/06/17－2026/06/23
幣別	NTD 新台幣
曝光量 IMP	46,284,917
點擊量	1,306,742
點擊率 CTR	2.82%
廣告花費	NT$14,105,639
平均點擊成本 CPC	NT$10.79
成交訂單數	50,216
成交轉換率 CVR	3.84%
商品交易總額 GMV	NT$114,876,459
廣告投資報酬率 ROAS	8.14x
單筆成交成本 CPA	NT$280.90
淨利	NT$29,342,150
扣除退款後營收	NT$113,492,704

報表圖表用資料

圖表資料	2026/06/17	2026/06/18	2026/06/19	2026/06/20	2026/06/21	2026/06/22	2026/06/23	合計
曝光量 IMP	5,785,615	6,572,458	6,155,894	5,507,905	7,914,721	6,665,028	7,683,296	46,284,917
點擊量	159,422	193,398	176,410	154,195	229,987	179,024	214,306	1,306,742
成交訂單數	6,076	7,583	6,729	5,674	9,390	6,478	8,286	50,216
商品交易總額 GMV	NT$13,325,669	NT$17,805,851	NT$15,623,198	NT$12,636,411	NT$23,549,674	NT$14,704,187	NT$17,231,469	NT$114,876,459
廣告花費	NT$1,819,627	NT$2,017,106	NT$1,932,473	NT$1,622,149	NT$2,383,853	NT$1,918,367	NT$2,412,064	NT$14,105,639
淨利	NT$3,168,952	NT$4,929,481	NT$4,049,217	NT$2,904,873	NT$6,807,379	NT$3,491,716	NT$3,990,532	NT$29,342,150
扣除退款後營收	NT$13,163,770	NT$17,599,672	NT$15,435,007	NT$12,481,430	NT$23,281,226	NT$14,522,915	NT$17,008,684	NT$113,492,704

每日點擊趨勢

日期	曝光量 IMP	點擊量	點擊率 CTR	廣告花費	平均點擊成本 CPC
2026/06/17	5,785,615	159,422	2.76%	NT$1,819,627	NT$11.41
2026/06/18	6,572,458	193,398	2.94%	NT$2,017,106	NT$10.43
2026/06/19	6,155,894	176,410	2.87%	NT$1,932,473	NT$10.95
2026/06/20	5,507,905	154,195	2.80%	NT$1,622,149	NT$10.52
2026/06/21	7,914,721	229,987	2.91%	NT$2,383,853	NT$10.37
2026/06/22	6,665,028	179,024	2.69%	NT$1,918,367	NT$10.72
2026/06/23	7,683,296	214,306	2.79%	NT$2,412,064	NT$11.26
合計	46,284,917	1,306,742	2.82%	NT$14,105,639	NT$10.79

每日訂單趨勢

日期	點擊量	成交訂單數	成交轉換率 CVR	廣告花費	單筆成交成本 CPA
2026/06/17	159,422	6,076	3.81%	NT$1,819,627	NT$299.48
2026/06/18	193,398	7,583	3.92%	NT$2,017,106	NT$266.00
2026/06/19	176,410	6,729	3.81%	NT$1,932,473	NT$287.19
2026/06/20	154,195	5,674	3.68%	NT$1,622,149	NT$285.89
2026/06/21	229,987	9,390	4.08%	NT$2,383,853	NT$253.87
2026/06/22	179,024	6,478	3.62%	NT$1,918,367	NT$296.14
2026/06/23	214,306	8,286	3.87%	NT$2,412,064	NT$291.10
合計	1,306,742	50,216	3.84%	NT$14,105,639	NT$280.90

每日銷售額趨勢

日期	成交訂單數	商品交易總額 GMV	廣告花費	ROAS	淨利	扣除退款後營收	淨利率
2026/06/17	6,076	NT$13,325,669	NT$1,819,627	7.32x	NT$3,168,952	NT$13,163,770	24.07%
2026/06/18	7,583	NT$17,805,851	NT$2,017,106	8.83x	NT$4,929,481	NT$17,599,672	28.01%
2026/06/19	6,729	NT$15,623,198	NT$1,932,473	8.08x	NT$4,049,217	NT$15,435,007	26.23%
2026/06/20	5,674	NT$12,636,411	NT$1,622,149	7.79x	NT$2,904,873	NT$12,481,430	23.27%
2026/06/21	9,390	NT$23,549,674	NT$2,383,853	9.88x	NT$6,807,379	NT$23,281,226	29.24%
2026/06/22	6,478	NT$14,704,187	NT$1,918,367	7.66x	NT$3,491,716	NT$14,522,915	24.04%
2026/06/23	8,286	NT$17,231,469	NT$2,412,064	7.14x	NT$3,990,532	NT$17,008,684	23.46%
合計	50,216	NT$114,876,459	NT$14,105,639	8.14x	NT$29,342,150	NT$113,492,704	25.85%

平台銷售額排名

排名	銷售平台／通路	成交訂單數	商品交易總額 GMV	銷售占比
1	自有品牌站／Shopify Plus	21,995	NT$50,086,136	43.60%
2	TikTok Shop	12,403	NT$28,374,485	24.70%
3	Amazon Marketplace	7,281	NT$16,657,087	14.50%
4	eBay	3,666	NT$8,500,858	7.40%
5	Shopee Cross-border	2,862	NT$6,433,082	5.60%
6	Walmart Marketplace	2,009	NT$4,824,811	4.20%
合計		50,216	NT$114,876,459	100.00%

每日完整投放數據

日期	IMP	Clicks	CTR	Ad Spend	CPC	Orders	CVR	GMV	ROAS	CPA	Net Profit	Net Revenue	淨利率
2026/06/17	5,785,615	159,422	2.76%	NT$1,819,627	NT$11.41	6,076	3.81%	NT$13,325,669	7.32x	NT$299.48	NT$3,168,952	NT$13,163,770	24.07%
2026/06/18	6,572,458	193,398	2.94%	NT$2,017,106	NT$10.43	7,583	3.92%	NT$17,805,851	8.83x	NT$266.00	NT$4,929,481	NT$17,599,672	28.01%
2026/06/19	6,155,894	176,410	2.87%	NT$1,932,473	NT$10.95	6,729	3.81%	NT$15,623,198	8.08x	NT$287.19	NT$4,049,217	NT$15,435,007	26.23%
2026/06/20	5,507,905	154,195	2.80%	NT$1,622,149	NT$10.52	5,674	3.68%	NT$12,636,411	7.79x	NT$285.89	NT$2,904,873	NT$12,481,430	23.27%
2026/06/21	7,914,721	229,987	2.91%	NT$2,383,853	NT$10.37	9,390	4.08%	NT$23,549,674	9.88x	NT$253.87	NT$6,807,379	NT$23,281,226	29.24%
2026/06/22	6,665,028	179,024	2.69%	NT$1,918,367	NT$10.72	6,478	3.62%	NT$14,704,187	7.66x	NT$296.14	NT$3,491,716	NT$14,522,915	24.04%
2026/06/23	7,683,296	214,306	2.79%	NT$2,412,064	NT$11.26	8,286	3.87%	NT$17,231,469	7.14x	NT$291.10	NT$3,990,532	NT$17,008,684	23.46%
合計	46,284,917	1,306,742	2.82%	NT$14,105,639	NT$10.79	50,216	3.84%	NT$114,876,459	8.14x	NT$280.90	NT$29,342,150	NT$113,492,704	25.85%

廣告平台成效

廣告平台	IMP	Clicks	CTR	Ad Spend	CPC	Orders	CVR	GMV	ROAS	CPA	Net Revenue	Net Profit	淨利率
TikTok Ads	18,051,118	548,831	3.04%	NT$5,360,143	NT$9.77	16,571	3.02%	NT$39,057,996	7.29x	NT$323.47	NT$38,587,519	NT$5,281,587	13.69%
Meta Ads	12,496,927	365,888	2.93%	NT$3,949,579	NT$10.79	15,567	4.25%	NT$36,760,467	9.31x	NT$253.71	NT$36,317,665	NT$9,976,331	27.47%
Google Ads	8,331,285	222,146	2.67%	NT$2,821,128	NT$12.70	10,043	4.52%	NT$20,677,763	7.33x	NT$280.90	NT$20,428,687	NT$6,455,273	31.60%
Pinterest Ads	4,628,492	117,607	2.54%	NT$1,128,451	NT$9.60	5,022	4.27%	NT$11,487,646	10.18x	NT$224.70	NT$11,349,271	NT$5,281,587	46.54%
Snapchat Ads	2,777,095	52,270	1.88%	NT$846,338	NT$16.19	3,013	5.76%	NT$6,892,587	8.14x	NT$280.90	NT$6,809,562	NT$2,347,372	34.47%
合計	46,284,917	1,306,742	2.82%	NT$14,105,639	NT$10.79	50,216	3.84%	NT$114,876,459	8.14x	NT$280.90	NT$113,492,704	NT$29,342,150	25.85%

國家市場成效

國家市場	IMP	Clicks	CTR	Ad Spend	CPC	Orders	CVR	GMV	ROAS	CPA	Net Revenue	Net Profit	淨利率
United States 美國	19,439,665	535,764	2.76%	NT$6,065,425	NT$11.32	19,082	3.56%	NT$46,524,966	7.67x	NT$317.86	NT$45,964,545	NT$8,215,802	17.87%
United Kingdom 英國	7,868,436	235,214	2.99%	NT$2,256,902	NT$9.60	8,537	3.63%	NT$20,103,380	8.91x	NT$264.37	NT$19,861,223	NT$5,868,430	29.55%
Canada 加拿大	6,479,888	182,944	2.82%	NT$2,045,318	NT$11.18	7,532	4.12%	NT$16,657,087	8.14x	NT$271.55	NT$16,456,442	NT$4,988,165	30.31%
Australia 澳洲	5,091,341	143,742	2.82%	NT$1,481,092	NT$10.30	5,524	3.84%	NT$12,062,028	8.14x	NT$268.12	NT$11,916,734	NT$3,521,058	29.55%
Japan 日本	3,702,793	104,539	2.82%	NT$1,057,923	NT$10.12	4,017	3.84%	NT$9,190,117	8.69x	NT$263.36	NT$9,079,416	NT$2,934,215	32.32%
Singapore 新加坡	2,314,246	65,337	2.82%	NT$775,810	NT$11.87	3,515	5.38%	NT$6,318,205	8.14x	NT$220.71	NT$6,242,099	NT$2,347,372	37.61%
Malaysia 馬來西亞	1,388,548	39,202	2.82%	NT$423,169	NT$10.79	2,009	5.12%	NT$4,020,676	9.50x	NT$210.64	NT$3,972,245	NT$1,467,108	36.93%
合計	46,284,917	1,306,742	2.82%	NT$14,105,639	NT$10.79	50,216	3.84%	NT$114,876,459	8.14x	NT$280.90	NT$113,492,704	NT$29,342,150	25.85%

商品銷售成效

商品名稱	商品類型	參考單價帶	AOV	單件成本	IMP	Clicks	CTR	Ad Spend	CPC	Orders	CVR	GMV	ROAS	CPA	商品成本	Net Profit	Net Revenue	淨利率
智能香氛小夜燈	居家氛圍／生活小家電	NT$970－NT$1,870	NT$2,673.44	NT$936.67	823,079	30,884	3.75%	NT$570,700	NT$18.48	1,014	3.28%	NT$2,710,872	4.75x	NT$562.82	NT$949,783	NT$664,859	NT$2,692,226	24.70%
桌面空氣循環扇	辦公室／居家小家電	NT$1,040－NT$2,020	NT$3,033.83	NT$1,157.12	342,959	14,128	4.12%	NT$249,121	NT$17.63	386	2.73%	NT$1,171,058	4.70x	NT$645.39	NT$446,648	NT$307,238	NT$1,160,260	26.48%
智能空氣淨化器	居家健康／空氣清潔設備	NT$3,740－NT$7,240	NT$10,767.15	NT$4,553.60	915,185	28,683	3.13%	NT$1,021,323	NT$35.61	1,143	3.98%	NT$12,306,851	12.05x	NT$893.55	NT$5,204,760	NT$3,046,270	NT$12,203,826	24.96%
智能廚房秤	廚房用品／智能小工具	NT$520－NT$1,000	NT$1,917.01	NT$690.99	81,737	2,508	3.07%	NT$31,046	NT$12.38	120	4.78%	NT$230,041	7.41x	NT$258.72	NT$82,919	NT$42,559	NT$227,350	18.72%
便攜式保溫杯	生活用品／外出隨行	NT$590－NT$1,150	NT$1,985.18	NT$736.71	279,583	10,544	3.77%	NT$112,381	NT$10.66	426	4.04%	NT$845,688	7.53x	NT$263.81	NT$313,838	NT$207,279	NT$831,785	24.92%
多功能收納包	旅行／居家收納用品	NT$670－NT$1,290	NT$2,160.82	NT$733.34	1,359,665	27,232	2.00%	NT$306,087	NT$11.24	1,596	5.86%	NT$3,448,676	11.27x	NT$191.78	NT$1,170,405	NT$982,976	NT$3,391,841	28.98%
旅行壓縮袋組	旅行用品／行李收納	NT$820－NT$1,580	NT$2,343.27	NT$929.93	2,802,116	62,691	2.24%	NT$684,954	NT$10.93	1,798	2.87%	NT$4,213,203	6.15x	NT$380.95	NT$1,672,018	NT$1,049,329	NT$4,158,741	25.23%
磁吸式無線充電座	3C配件／桌面充電	NT$970－NT$1,870	NT$2,268.05	NT$997.50	537,739	20,220	3.76%	NT$459,098	NT$22.71	612	3.03%	NT$1,388,044	3.02x	NT$750.16	NT$610,473	NT$196,201	NT$1,365,894	14.36%
藍牙降噪耳機	3C配件／影音設備	NT$1,870－NT$3,610	NT$5,808.55	NT$2,299.42	480,497	11,731	2.44%	NT$323,761	NT$27.60	480	4.09%	NT$2,788,106	8.61x	NT$674.50	NT$1,103,722	NT$868,085	NT$2,753,141	31.53%
手機防水收納袋	戶外用品／手機配件	NT$290－NT$570	NT$1,211.01	NT$344.48	1,768,490	41,139	2.33%	NT$144,123	NT$3.50	2,165	5.26%	NT$2,621,835	18.19x	NT$66.57	NT$745,794	NT$693,562	NT$2,597,634	26.70%
摺疊式手機支架	3C配件／桌面用品	NT$340－NT$650	NT$1,118.62	NT$373.47	1,019,393	22,463	2.20%	NT$266,515	NT$11.86	1,002	4.46%	NT$1,120,854	4.21x	NT$265.98	NT$374,214	NT$316,211	NT$1,112,079	28.43%
LED補光化妝鏡	美妝工具／居家小物	NT$890－NT$1,730	NT$2,575.93	NT$944.44	538,405	18,708	3.47%	NT$207,429	NT$11.09	512	2.74%	NT$1,318,876	6.36x	NT$405.13	NT$483,553	NT$353,441	NT$1,303,032	27.12%
電動筋膜按摩器	健康放鬆／按摩設備	NT$2,240－NT$4,340	NT$6,267.65	NT$2,421.59	307,801	10,581	3.44%	NT$442,026	NT$41.78	604	5.71%	NT$3,785,660	8.56x	NT$731.83	NT$1,462,639	NT$1,033,257	NT$3,731,822	27.69%
頸掛式小風扇	夏季用品／個人小家電	NT$740－NT$1,440	NT$2,411.05	NT$672.46	3,428,158	91,694	2.67%	NT$1,036,467	NT$11.30	2,339	2.55%	NT$5,639,447	5.44x	NT$443.12	NT$1,572,882	NT$1,173,377	NT$5,552,347	21.13%
USB加熱暖手寶	冬季用品／生活小家電	NT$520－NT$1,000	NT$1,185.05	NT$390.39	408,043	12,226	3.00%	NT$102,744	NT$8.40	705	5.77%	NT$835,459	8.13x	NT$145.74	NT$275,224	NT$256,204	NT$823,335	31.12%
智能感應垃圾桶	居家用品／智能生活	NT$1,420－NT$2,740	NT$4,559.43	NT$2,056.98	958,747	26,711	2.79%	NT$431,226	NT$16.14	1,398	5.23%	NT$6,374,089	14.78x	NT$308.46	NT$2,875,661	NT$1,113,381	NT$6,272,853	17.75%
防滑浴室地墊	居家用品／浴室收納	NT$440－NT$860	NT$1,129.65	NT$416.10	458,129	13,417	2.93%	NT$159,213	NT$11.87	467	3.48%	NT$527,548	3.31x	NT$340.93	NT$194,319	NT$82,870	NT$523,751	15.82%
廚房瀝水置物架	廚房用品／收納整理	NT$890－NT$1,730	NT$2,219.06	NT$731.47	505,227	16,958	3.36%	NT$170,922	NT$10.08	688	4.06%	NT$1,526,713	8.93x	NT$248.43	NT$503,250	NT$570,379	NT$1,506,518	37.86%
矽膠保鮮袋組	廚房用品／環保收納	NT$370－NT$710	NT$1,046.32	NT$388.89	1,134,720	44,981	3.96%	NT$199,366	NT$4.43	2,355	5.24%	NT$2,464,075	12.36x	NT$84.66	NT$915,829	NT$673,944	NT$2,443,162	27.58%
不鏽鋼保鮮盒	廚房用品／食物收納	NT$670－NT$1,290	NT$2,300.29	NT$769.27	3,148,622	91,673	2.91%	NT$323,897	NT$3.53	4,167	4.55%	NT$9,585,322	29.59x	NT$77.73	NT$3,205,556	NT$2,926,087	NT$9,445,444	30.98%
可折疊購物袋	生活用品／外出收納	NT$290－NT$570	NT$1,125.24	NT$369.99	542,810	12,865	2.37%	NT$113,747	NT$8.84	758	5.89%	NT$852,933	7.50x	NT$150.06	NT$280,454	NT$274,182	NT$839,679	32.65%
旅行盥洗收納包	旅行用品／盥洗收納	NT$590－NT$1,150	NT$2,313.76	NT$942.48	1,113,608	25,068	2.25%	NT$251,254	NT$10.02	928	3.70%	NT$2,147,165	8.55x	NT$270.75	NT$874,619	NT$380,917	NT$2,114,985	18.01%
護照證件收納包	旅行用品／證件收納	NT$520－NT$1,000	NT$1,824.23	NT$640.17	903,758	26,021	2.88%	NT$108,792	NT$4.18	1,303	5.01%	NT$2,376,967	21.85x	NT$83.49	NT$834,144	NT$691,360	NT$2,363,330	29.25%
行李箱電子秤	旅行用品／行李配件	NT$440－NT$860	NT$1,717.09	NT$642.16	1,833,426	36,917	2.01%	NT$478,547	NT$12.96	952	2.58%	NT$1,634,668	3.42x	NT$502.68	NT$611,332	NT$342,637	NT$1,622,706	21.12%
車用手機支架	汽車用品／車內配件	NT$590－NT$1,150	NT$2,179.02	NT$676.94	407,903	14,741	3.61%	NT$69,453	NT$4.71	472	3.20%	NT$1,028,498	14.81x	NT$147.15	NT$319,514	NT$317,408	NT$1,016,700	31.22%
車用香氛擴香器	汽車用品／車內香氛	NT$740－NT$1,440	NT$1,715.13	NT$643.63	133,305	3,250	2.44%	NT$11,256	NT$3.46	193	5.94%	NT$331,020	29.41x	NT$58.32	NT$124,220	NT$83,861	NT$326,619	25.68%
車用吸塵器	汽車用品／清潔設備	NT$1,190－NT$2,310	NT$3,281.46	NT$1,349.06	430,531	14,769	3.43%	NT$197,758	NT$13.39	647	4.38%	NT$2,123,104	10.74x	NT$305.65	NT$872,840	NT$488,249	NT$2,088,759	23.38%
寵物飲水機	寵物用品／智能設備	NT$1,490－NT$2,890	NT$5,833.14	NT$2,234.83	169,739	6,418	3.78%	NT$70,288	NT$10.95	205	3.19%	NT$1,195,793	17.01x	NT$342.87	NT$458,141	NT$356,285	NT$1,187,876	29.99%
寵物除毛刷	寵物用品／清潔護理	NT$520－NT$1,000	NT$1,949.07	NT$585.46	973,638	36,888	3.79%	NT$487,002	NT$13.20	1,006	2.73%	NT$1,960,760	4.03x	NT$484.10	NT$588,972	NT$371,821	NT$1,929,632	19.27%
寵物外出水壺	寵物用品／外出用品	NT$490－NT$940	NT$1,913.68	NT$716.23	745,191	20,715	2.78%	NT$130,796	NT$6.31	913	4.41%	NT$1,747,187	13.36x	NT$143.26	NT$653,919	NT$352,138	NT$1,721,851	20.45%
瑜珈彈力帶組	運動用品／健身配件	NT$440－NT$860	NT$1,318.31	NT$476.62	1,309,258	52,105	3.98%	NT$626,938	NT$12.03	1,385	2.66%	NT$1,825,854	2.91x	NT$452.66	NT$660,116	NT$334,558	NT$1,815,306	18.43%
防滑瑜珈墊	運動用品／居家健身	NT$1,270－NT$2,450	NT$3,548.63	NT$1,587.86	1,372,295	25,879	1.89%	NT$341,366	NT$13.19	709	2.74%	NT$2,515,982	7.37x	NT$481.48	NT$1,125,796	NT$495,476	NT$2,477,745	20.00%
運動水壺	運動用品／外出補水	NT$520－NT$1,000	NT$1,290.52	NT$414.97	220,980	7,963	3.60%	NT$33,278	NT$4.18	431	5.41%	NT$556,212	16.71x	NT$77.21	NT$178,850	NT$123,812	NT$549,008	22.55%
快乾運動毛巾	運動用品／戶外用品	NT$370－NT$710	NT$828.59	NT$325.39	294,930	11,704	3.97%	NT$60,618	NT$5.18	308	2.63%	NT$255,205	4.21x	NT$196.81	NT$100,219	NT$62,240	NT$252,749	24.63%
露營LED掛燈	戶外用品／露營照明	NT$740－NT$1,440	NT$2,687.71	NT$1,068.12	260,717	7,699	2.95%	NT$40,403	NT$5.25	333	4.33%	NT$895,009	22.15x	NT$121.33	NT$355,685	NT$210,117	NT$884,854	23.75%
戶外折疊椅	戶外用品／露營家具	NT$1,790－NT$3,470	NT$5,003.06	NT$1,860.17	573,761	15,539	2.71%	NT$570,589	NT$36.72	758	4.88%	NT$3,792,320	6.65x	NT$752.76	NT$1,410,010	NT$958,148	NT$3,749,726	25.55%
便攜餐具組	戶外用品／旅行餐具	NT$370－NT$710	NT$1,645.09	NT$666.45	1,304,263	33,742	2.59%	NT$250,946	NT$7.44	1,234	3.66%	NT$2,030,036	8.09x	NT$203.36	NT$822,403	NT$434,706	NT$2,008,397	21.64%
防水收納乾濕袋	旅行用品／戶外收納	NT$440－NT$860	NT$1,607.24	NT$560.16	1,989,281	52,006	2.61%	NT$458,067	NT$8.81	1,579	3.04%	NT$2,537,830	5.54x	NT$290.10	NT$884,489	NT$693,664	NT$2,495,638	27.80%
兒童防漏水杯	親子用品／兒童餐具	NT$520－NT$1,000	NT$1,328.65	NT$522.30	1,529,077	50,158	3.28%	NT$439,474	NT$8.76	1,911	3.81%	NT$2,539,041	5.78x	NT$229.97	NT$998,108	NT$472,629	NT$2,516,839	18.78%
兒童矽膠圍兜	親子用品／用餐用品	NT$370－NT$710	NT$1,068.01	NT$279.03	1,352,671	46,810	3.46%	NT$493,764	NT$10.55	2,334	4.99%	NT$2,492,726	5.05x	NT$211.55	NT$651,245	NT$866,225	NT$2,469,066	35.08%
嬰兒推車收納袋	親子用品／外出收納	NT$670－NT$1,290	NT$2,587.71	NT$772.85	1,170,431	27,642	2.36%	NT$218,362	NT$7.90	989	3.58%	NT$2,559,246	11.72x	NT$220.79	NT$764,351	NT$755,707	NT$2,527,209	29.90%
居家防撞條組	親子用品／安全防護	NT$370－NT$710	NT$1,004.96	NT$309.80	572,662	21,057	3.68%	NT$226,961	NT$10.78	791	3.76%	NT$794,920	3.50x	NT$286.93	NT$245,050	NT$164,494	NT$782,399	21.02%
收納抽屜分隔板	居家收納／衣櫃整理	NT$520－NT$1,000	NT$1,883.80	NT$507.22	272,415	9,911	3.64%	NT$38,898	NT$3.92	576	5.81%	NT$1,085,071	27.90x	NT$67.53	NT$292,158	NT$434,338	NT$1,072,584	40.49%
真空壓縮收納袋	居家收納／換季整理	NT$590－NT$1,150	NT$1,786.85	NT$700.11	654,648	17,233	2.63%	NT$85,550	NT$4.96	530	3.08%	NT$947,030	11.07x	NT$161.42	NT$371,060	NT$232,562	NT$933,852	24.90%
衣物除毛球機	居家用品／衣物護理	NT$670－NT$1,290	NT$2,351.70	NT$907.27	1,447,045	36,617	2.53%	NT$196,809	NT$5.37	1,217	3.32%	NT$2,862,022	14.54x	NT$161.72	NT$1,104,144	NT$920,663	NT$2,822,753	32.62%
迷你熨燙機	居家用品／衣物整理	NT$1,190－NT$2,310	NT$3,358.78	NT$1,405.55	647,594	14,771	2.28%	NT$224,284	NT$15.18	405	2.74%	NT$1,360,304	6.07x	NT$553.79	NT$569,246	NT$336,852	NT$1,350,385	24.94%
防藍光眼鏡	健康用品／護眼配件	NT$590－NT$1,150	NT$1,960.38	NT$724.50	548,069	13,131	2.40%	NT$76,683	NT$5.84	641	4.88%	NT$1,256,604	16.39x	NT$119.63	NT$464,405	NT$273,981	NT$1,235,391	22.18%
睡眠遮光眼罩	生活用品／睡眠配件	NT$440－NT$860	NT$1,718.25	NT$685.97	879,593	25,366	2.88%	NT$355,569	NT$14.02	901	3.55%	NT$1,548,145	4.35x	NT$394.64	NT$618,061	NT$378,470	NT$1,539,370	24.59%
人體工學滑鼠墊	辦公用品／桌面配件	NT$520－NT$1,000	NT$1,609.87	NT$440.01	565,492	20,873	3.69%	NT$87,036	NT$4.17	1,193	5.72%	NT$1,920,570	22.07x	NT$72.96	NT$524,927	NT$769,784	NT$1,906,975	40.37%
桌面理線收納盒	辦公用品／桌面收納	NT$370－NT$710	NT$1,258.74	NT$415.09	767,531	19,712	2.57%	NT$118,752	NT$6.02	637	3.23%	NT$801,820	6.75x	NT$186.42	NT$264,415	NT$207,357	NT$793,280	26.14%
合計				NT$840.10	46,284,917	1,306,742	2.82%	NT$14,105,639	NT$10.79	50,216	3.84%	NT$114,876,459	8.14x	NT$280.90	NT$42,186,380	NT$29,342,150	NT$113,492,704	25.85%

廣告素材成效

廣告素材	素材類型	IMP	Clicks	CTR	Ad Spend	CPC	Orders	CVR	GMV	ROAS	CPA	Net Revenue	Net Profit	淨利率
短影音A｜高單價家電開箱	15秒短影音	11,339,805	261,349	2.30%	NT$3,385,353	NT$12.95	9,541	3.65%	NT$24,124,056	7.13x	NT$354.82	NT$23,833,468	NT$4,107,901	17.24%
短影音B｜旅行收納前後對比	20秒短影音	9,488,408	307,084	3.24%	NT$2,115,846	NT$6.89	12,554	4.09%	NT$28,144,733	13.30x	NT$168.54	NT$27,805,712	NT$8,215,802	29.55%
短影音C｜辦公桌面改造	18秒短影音	7,174,162	196,011	2.73%	NT$1,974,789	NT$10.07	8,035	4.10%	NT$18,380,233	9.31x	NT$245.77	NT$18,158,833	NT$4,694,744	25.85%
短影音D｜寵物日常實測	25秒短影音	6,248,464	169,877	2.72%	NT$2,821,128	NT$16.61	6,528	3.84%	NT$16,082,704	5.70x	NT$432.16	NT$15,888,978	NT$3,814,479	24.01%
輪播圖E｜低單價爆品合集	圖文輪播	7,637,011	287,483	3.76%	NT$1,974,790	NT$6.87	10,043	3.49%	NT$20,677,763	10.47x	NT$196.63	NT$20,428,687	NT$6,455,273	31.60%
再行銷F｜購物車限時優惠	再行銷素材	4,397,067	84,938	1.93%	NT$1,833,733	NT$21.59	3,515	4.14%	NT$7,466,970	4.07x	NT$521.69	NT$7,377,026	NT$2,053,951	27.84%
合計		46,284,917	1,306,742	2.82%	NT$14,105,639	NT$10.79	50,216	3.84%	NT$114,876,459	8.14x	NT$280.90	NT$113,492,704	NT$29,342,150	25.85%

裝置來源成效

裝置來源	IMP	Clicks	CTR	Ad Spend	CPC	Orders	CVR	GMV	ROAS	CPA	Net Revenue	Net Profit	淨利率
Mobile App / 行動裝置	32,399,442	940,854	2.90%	NT$9,732,891	NT$10.34	35,151	3.74%	NT$80,413,521	8.26x	NT$276.89	NT$79,444,893	NT$18,192,133	22.90%
Desktop Web / 桌機網頁	8,331,285	222,146	2.67%	NT$2,680,071	NT$12.06	9,039	4.07%	NT$20,677,763	7.72x	NT$296.50	NT$20,428,687	NT$5,868,430	28.73%
Tablet / 平板	3,471,369	91,472	2.64%	NT$1,128,451	NT$12.34	3,766	4.12%	NT$8,615,734	7.64x	NT$299.64	NT$8,511,953	NT$3,227,636	37.92%
In-App Webview / 內嵌瀏覽器	2,082,821	52,270	2.51%	NT$564,226	NT$10.79	2,260	4.32%	NT$5,169,441	9.16x	NT$249.66	NT$5,107,171	NT$2,053,951	40.22%
合計	46,284,917	1,306,742	2.82%	NT$14,105,639	NT$10.79	50,216	3.84%	NT$114,876,459	8.14x	NT$280.90	NT$113,492,704	NT$29,342,150	25.85%

受眾年齡成效

年齡層	IMP	Clicks	CTR	Ad Spend	CPC	Orders	CVR	GMV	ROAS	CPA	Net Revenue	Net Profit	淨利率
18-24	8,794,134	235,214	2.67%	NT$2,539,015	NT$10.79	8,537	3.63%	NT$19,528,998	7.69x	NT$297.41	NT$19,293,760	NT$4,694,744	24.33%
25-34	17,819,693	522,697	2.93%	NT$5,501,199	NT$10.52	20,086	3.84%	NT$45,950,584	8.35x	NT$273.88	NT$45,397,081	NT$11,443,438	25.21%
35-44	12,496,928	352,820	2.82%	NT$3,949,579	NT$11.19	14,311	4.06%	NT$32,165,408	8.14x	NT$275.98	NT$31,777,957	NT$7,922,381	24.93%
45-54	4,859,916	137,208	2.82%	NT$1,481,092	NT$10.79	5,022	3.66%	NT$12,062,028	8.14x	NT$294.92	NT$11,916,734	NT$3,521,058	29.55%
55+	2,314,246	58,803	2.54%	NT$634,754	NT$10.79	2,260	3.84%	NT$5,169,441	8.14x	NT$280.86	NT$5,107,172	NT$1,760,529	34.47%
合計	46,284,917	1,306,742	2.82%	NT$14,105,639	NT$10.79	50,216	3.84%	NT$114,876,459	8.14x	NT$280.90	NT$113,492,704	NT$29,342,150	25.85%

受眾性別成效

性別	IMP	Clicks	CTR	Ad Spend	CPC	Orders	CVR	GMV	ROAS	CPA	Net Revenue	Net Profit	淨利率
女性	28,696,649	823,247	2.87%	NT$8,463,384	NT$10.28	30,632	3.72%	NT$70,074,640	8.28x	NT$276.29	NT$69,230,550	NT$17,605,290	25.43%
男性	14,811,173	405,090	2.74%	NT$4,795,917	NT$11.84	16,571	4.09%	NT$37,909,231	7.90x	NT$289.42	NT$37,452,592	NT$9,682,909	25.85%
未揭露／其他	2,777,095	78,405	2.82%	NT$846,338	NT$10.79	3,013	3.84%	NT$6,892,588	8.14x	NT$280.90	NT$6,809,562	NT$2,053,951	30.16%
合計	46,284,917	1,306,742	2.82%	NT$14,105,639	NT$10.79	50,216	3.84%	NT$114,876,459	8.14x	NT$280.90	NT$113,492,704	NT$29,342,150	25.85%

顧客轉換路徑

轉換階段	數量	與上一階段轉換率
曝光量 IMP	46,284,917	-
點擊量	1,306,742	2.82%
成交訂單數	50,216	3.84%
商品交易總額 GMV	NT$114,876,459	-
扣除退款後營收	NT$113,492,704	98.80%
淨利	NT$29,342,150	25.85%

訂單與退款資料

日期	成交訂單數	GMV	退款金額	扣除退款後營收	淨利
2026/06/17	6,076	NT$13,325,669	NT$161,899	NT$13,163,770	NT$3,168,952
2026/06/18	7,583	NT$17,805,851	NT$206,179	NT$17,599,672	NT$4,929,481
2026/06/19	6,729	NT$15,623,198	NT$188,191	NT$15,435,007	NT$4,049,217
2026/06/20	5,674	NT$12,636,411	NT$154,981	NT$12,481,430	NT$2,904,873
2026/06/21	9,390	NT$23,549,674	NT$268,448	NT$23,281,226	NT$6,807,379
2026/06/22	6,478	NT$14,704,187	NT$181,272	NT$14,522,915	NT$3,491,716
2026/06/23	8,286	NT$17,231,469	NT$222,785	NT$17,008,684	NT$3,990,532
合計	50,216	NT$114,876,459	NT$1,383,755	NT$113,492,704	NT$29,342,150

營收與利潤

日期	GMV	退款金額	扣除退款後營收	商品成本	國際物流／履約成本	倉儲與包裝成本	平台／金流手續費	跨境關稅／稅務成本	退貨損耗	客服與營運成本	廣告花費	淨利	淨利率
2026/06/17	NT$13,325,669	NT$161,899	NT$13,163,770	NT$5,267,055	NT$953,385	NT$294,028	NT$450,316	NT$283,006	NT$189,814	NT$737,587	NT$1,819,627	NT$3,168,952	24.07%
2026/06/18	NT$17,805,851	NT$206,179	NT$17,599,672	NT$6,387,427	NT$1,304,781	NT$432,471	NT$580,521	NT$350,775	NT$308,421	NT$1,288,689	NT$2,017,106	NT$4,929,481	28.01%
2026/06/19	NT$15,623,198	NT$188,191	NT$15,435,007	NT$5,766,115	NT$1,241,737	NT$330,070	NT$485,040	NT$353,418	NT$279,136	NT$997,801	NT$1,932,473	NT$4,049,217	26.23%
2026/06/20	NT$12,636,411	NT$154,981	NT$12,481,430	NT$4,690,542	NT$1,014,963	NT$271,964	NT$425,475	NT$266,478	NT$209,289	NT$1,075,697	NT$1,622,149	NT$2,904,873	23.27%
2026/06/21	NT$23,549,674	NT$268,448	NT$23,281,226	NT$8,390,018	NT$1,825,081	NT$476,217	NT$681,285	NT$448,918	NT$363,477	NT$1,904,998	NT$2,383,853	NT$6,807,379	29.24%
2026/06/22	NT$14,704,187	NT$181,272	NT$14,522,915	NT$5,507,348	NT$1,162,676	NT$351,458	NT$480,081	NT$265,888	NT$252,707	NT$1,092,674	NT$1,918,367	NT$3,491,716	24.04%
2026/06/23	NT$17,231,469	NT$222,785	NT$17,008,684	NT$6,177,875	NT$1,170,919	NT$330,567	NT$611,801	NT$373,219	NT$276,382	NT$1,665,325	NT$2,412,064	NT$3,990,532	23.46%
7天合計	NT$114,876,459	NT$1,383,755	NT$113,492,704	NT$42,186,380	NT$8,673,542	NT$2,486,775	NT$3,714,519	NT$2,341,702	NT$1,879,226	NT$8,762,771	NT$14,105,639	NT$29,342,150	25.85%"""

# =========================================================
# 頁面設定
# =========================================================
st.set_page_config(
    page_title="跨境電商廣告投放報表",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3 {
    letter-spacing: .5px;
}
[data-testid="stMetricValue"] {
    font-size: 28px;
}
.metric-title{
    font-size:22px;
    font-weight:900;
    color:#0f172a;
    line-height:1.15;
    margin-bottom:8px;
}

.metric-value{
    font-size:28px;
    font-weight:900;
    color:#111827;
}

.gauge-title{
    text-align:center;
    font-size:36px;
    font-weight:900;
    color:#0f172a;
    margin-top:12px;
    margin-bottom:12px;
}
.section-title{
    font-size:28px;
    font-weight:900;
    color:#0f172a;
    margin-top:28px;
    margin-bottom:12px;
}
.summary-box{
    border:1px solid #e5e7eb;
    border-radius:12px;
    padding:18px 20px;
    background:#ffffff;
    line-height:1.8;
    font-size:17px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 解析工具
# =========================================================
SECTION_TITLES = [
    "核心成效總覽",
    "報表圖表用資料",
    "每日點擊趨勢",
    "每日訂單趨勢",
    "每日銷售額趨勢",
    "平台銷售額排名",
    "每日完整投放數據",
    "廣告平台成效",
    "國家市場成效",
    "商品銷售成效",
    "廣告素材成效",
    "裝置來源成效",
    "受眾年齡成效",
    "受眾性別成效",
    "顧客轉換路徑",
    "訂單與退款資料",
    "營收與利潤",
]

def section_text(title):
    start = RAW_DATA.index(title) + len(title)
    next_positions = []
    for t in SECTION_TITLES:
        if t == title:
            continue
        pos = RAW_DATA.find(t, start)
        if pos != -1:
            next_positions.append(pos)
    end = min(next_positions) if next_positions else len(RAW_DATA)
    return RAW_DATA[start:end].strip()

def read_table(title):
    txt = section_text(title)
    lines = [line.strip() for line in txt.splitlines() if line.strip()]
    if not lines:
        return pd.DataFrame()
    return normalize_columns(pd.read_csv(StringIO("\n".join(lines)), sep="\t", dtype=str).fillna(""))


def normalize_columns(df):
    alias = {
        "IMP": "曝光量 IMP",
        "Clicks": "點擊量",
        "點擊": "點擊量",
        "CTR": "點擊率 CTR",
        "Ad Spend": "廣告花費",
        "CPC": "平均點擊成本 CPC",
        "Orders": "成交訂單數",
        "訂單": "成交訂單數",
        "訂單數": "成交訂單數",
        "CVR": "成交轉換率 CVR",
        "GMV": "商品交易總額 GMV",
        "ROAS": "廣告投資報酬率 ROAS",
        "CPA": "單筆成交成本 CPA",
        "Net Profit": "淨利",
        "Net Revenue": "扣除退款後營收",
        "AOV": "平均客單價 AOV",
    }
    return df.rename(columns={k: v for k, v in alias.items() if k in df.columns})

def to_int(v):
    if isinstance(v, (int, float)):
        return int(v)
    s = str(v).replace("NT$", "").replace(",", "").replace("%", "").replace("x", "").strip()
    if s in ["", "-", "nan", "None"]:
        return ""
    try:
        return int(round(float(s)))
    except Exception:
        m = re.search(r"-?\d+(?:\.\d+)?", s)
        if m:
            return int(round(float(m.group(0))))
        return ""

def to_float(v):
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).replace("NT$", "").replace(",", "").replace("%", "").replace("x", "").strip()
    if s in ["", "-", "nan", "None"]:
        return ""
    try:
        return float(s)
    except Exception:
        m = re.search(r"-?\d+(?:\.\d+)?", s)
        if m:
            return float(m.group(0))
        return ""

def clean_numeric_df(df):
    out = df.copy()
    int_cols = ["曝光量 IMP", "點擊量", "成交訂單數", "商品交易總額 GMV", "廣告花費", "淨利", "扣除退款後營收", "退款金額", "其他成本合計", "商品成本", "單件成本", "國際物流／履約成本", "倉儲與包裝成本", "平台／金流手續費", "跨境關稅／稅務成本", "退貨損耗", "客服與營運成本", "數量"]
    float_cols = ["點擊率 CTR", "平均點擊成本 CPC", "成交轉換率 CVR", "廣告投資報酬率 ROAS", "單筆成交成本 CPA", "銷售占比", "淨利率", "平均客單價 AOV"]
    for col in out.columns:
        if col in int_cols:
            out[col] = out[col].apply(to_int)
        elif col in float_cols:
            out[col] = out[col].apply(to_float)
        elif col == "排名":
            out[col] = out[col].apply(lambda x: to_int(x) if str(x).strip() not in ["合計", ""] else x)
    return out

def money(v):
    return f"NT${v:,.0f}"

def money2(v):
    return f"NT${v:,.2f}"

def number(v):
    return f"{v:,.0f}"

def percent(v):
    return f"{v:.2f}%"

def roas(v):
    return f"{v:.2f}x"

def rgba(hex_color, alpha=0.18):
    hex_color = hex_color.replace("#", "")
    r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:], 16)
    return f"rgba({r},{g},{b},{alpha})"

def wan_label(v):
    return f"{v / 10000:,.1f} 萬"

# =========================================================
# 資料建立
# =========================================================
core_raw = read_table("核心成效總覽")
core_map = dict(zip(core_raw["項目"], core_raw["數值"]))
REPORT_TITLE = "跨境電商廣告投放報表"
PERIOD = core_map.get("期間", "")
CURRENCY = core_map.get("幣別", "")

core = {
    "曝光量 IMP": to_int(core_map["曝光量 IMP"]),
    "點擊量": to_int(core_map["點擊量"]),
    "點擊率 CTR": to_float(core_map["點擊率 CTR"]),
    "廣告花費": to_int(core_map["廣告花費"]),
    "平均點擊成本 CPC": to_float(core_map["平均點擊成本 CPC"]),
    "成交訂單數": to_int(core_map["成交訂單數"]),
    "成交轉換率 CVR": to_float(core_map["成交轉換率 CVR"]),
    "商品交易總額 GMV": to_int(core_map["商品交易總額 GMV"]),
    "廣告投資報酬率 ROAS": to_float(core_map["廣告投資報酬率 ROAS"]),
    "單筆成交成本 CPA": to_float(core_map["單筆成交成本 CPA"]),
    "淨利": to_int(core_map["淨利"]),
    "扣除退款後營收": to_int(core_map["扣除退款後營收"]),
}

core_table = pd.DataFrame([
    ["期間", PERIOD],
    ["幣別", CURRENCY],
    ["曝光量 IMP", number(core["曝光量 IMP"])],
    ["點擊量", number(core["點擊量"])],
    ["點擊率 CTR", percent(core["點擊率 CTR"])],
    ["廣告花費", money(core["廣告花費"])],
    ["平均點擊成本 CPC", money2(core["平均點擊成本 CPC"])],
    ["成交訂單數", number(core["成交訂單數"])],
    ["成交轉換率 CVR", percent(core["成交轉換率 CVR"])],
    ["商品交易總額 GMV", money(core["商品交易總額 GMV"])],
    ["廣告投資報酬率 ROAS", roas(core["廣告投資報酬率 ROAS"])],
    ["單筆成交成本 CPA", money2(core["單筆成交成本 CPA"])],
    ["淨利", money(core["淨利"])],
    ["扣除退款後營收", money(core["扣除退款後營收"])],
], columns=["項目", "數值"])

chart_table = read_table("報表圖表用資料")

daily_full_display = clean_numeric_df(read_table("每日完整投放數據"))
daily_full = daily_full_display[daily_full_display["日期"] != "合計"].copy()

daily = daily_full[[
    "日期", "曝光量 IMP", "點擊量", "成交訂單數",
    "商品交易總額 GMV", "廣告花費", "淨利", "扣除退款後營收"
]].copy()

click_display = clean_numeric_df(read_table("每日點擊趨勢"))
click_trend = click_display[click_display["日期"] != "合計"].copy()

order_display = clean_numeric_df(read_table("每日訂單趨勢"))
order_trend = order_display[order_display["日期"] != "合計"].copy()

sales_display = clean_numeric_df(read_table("每日銷售額趨勢"))
sales_trend = sales_display[sales_display["日期"] != "合計"].copy()

platform_rank_display = clean_numeric_df(read_table("平台銷售額排名"))
platform_rank = platform_rank_display[platform_rank_display["排名"] != "合計"].copy()
platform_rank["報表顯示"] = platform_rank["商品交易總額 GMV"].apply(wan_label)
platform_rank_display["報表顯示"] = platform_rank_display["商品交易總額 GMV"].apply(lambda x: wan_label(x) if isinstance(x, (int, float)) else "")

ad_platform_display = clean_numeric_df(read_table("廣告平台成效"))
ad_platform = ad_platform_display[ad_platform_display["廣告平台"] != "合計"].copy()

country_display = clean_numeric_df(read_table("國家市場成效"))
country = country_display[country_display["國家市場"] != "合計"].copy()

product_display = clean_numeric_df(read_table("商品銷售成效"))
product = product_display[product_display["商品名稱"] != "合計"].copy()

creative_display = clean_numeric_df(read_table("廣告素材成效"))
creative = creative_display[creative_display["廣告素材"] != "合計"].copy()

device_display = clean_numeric_df(read_table("裝置來源成效"))
device = device_display[device_display["裝置來源"] != "合計"].copy()

age_display = clean_numeric_df(read_table("受眾年齡成效"))
age = age_display[age_display["年齡層"] != "合計"].copy()

gender_display = clean_numeric_df(read_table("受眾性別成效"))
gender = gender_display[gender_display["性別"] != "合計"].copy()

funnel_raw = read_table("顧客轉換路徑")
funnel = funnel_raw.copy()
funnel["顯示數值"] = funnel["數量"]
funnel["數量"] = funnel["數量"].apply(to_int)

refund = clean_numeric_df(read_table("訂單與退款資料"))
profit = clean_numeric_df(read_table("營收與利潤"))
cost_cols_for_total = ["商品成本", "國際物流／履約成本", "倉儲與包裝成本", "平台／金流手續費", "跨境關稅／稅務成本", "退貨損耗", "客服與營運成本"]
if "其他成本合計" not in profit.columns:
    present_cost_cols = [c for c in cost_cols_for_total if c in profit.columns]
    if present_cost_cols:
        profit["其他成本合計"] = profit[present_cost_cols].apply(
            lambda row: sum([x for x in row if isinstance(x, (int, float))]),
            axis=1
        )
    else:
        profit["其他成本合計"] = 0

total_profit_rate = to_float(profit.iloc[-1]["淨利率"])

total_profit_rate = to_float(profit.iloc[-1]["淨利率"])

# =========================================================
# 顯示格式
# =========================================================
def display_df(df):
    out = df.copy()
    money_cols = [
        "商品交易總額 GMV", "廣告花費", "淨利", "扣除退款後營收", "退款金額",
        "其他成本合計", "商品成本", "單件成本", "國際物流／履約成本", "倉儲與包裝成本", "平台／金流手續費", "跨境關稅／稅務成本", "退貨損耗", "客服與營運成本", "平均客單價 AOV"
    ]
    number_cols = ["曝光量 IMP", "點擊量", "成交訂單數", "排名", "數量"]
    percent_cols = ["點擊率 CTR", "成交轉換率 CVR", "銷售占比", "淨利率"]
    money2_cols = ["平均點擊成本 CPC", "單筆成交成本 CPA"]
    roas_cols = ["廣告投資報酬率 ROAS"]

    for col in out.columns:
        if col in money_cols:
            out[col] = out[col].apply(lambda x: f"NT${x:,.2f}" if col == "平均客單價 AOV" and isinstance(x, (int, float)) else (f"NT${x:,.0f}" if isinstance(x, (int, float)) else x))
        elif col in number_cols:
            out[col] = out[col].apply(lambda x: f"{x:,.0f}" if isinstance(x, (int, float)) else x)
        elif col in percent_cols:
            out[col] = out[col].apply(lambda x: f"{x:.2f}%" if isinstance(x, (int, float)) else x)
        elif col in money2_cols:
            out[col] = out[col].apply(lambda x: f"NT${x:,.2f}" if isinstance(x, (int, float)) else x)
        elif col in roas_cols:
            out[col] = out[col].apply(lambda x: f"{x:.2f}x" if isinstance(x, (int, float)) else x)
    return out

# =========================================================
# 圖表工具
# =========================================================
def metric_card(title, value, trend_data, note="", line_color="#7E57C2"):
    with st.container(border=True):
        left, right = st.columns([3, 1])
        with left:
            st.markdown(
                f"""
                <div class="metric-title">
                    {title}
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
    f"""
    <div class="metric-value">
        {value}
    </div>
    """,
    unsafe_allow_html=True
)
        with right:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                y=trend_data,
                mode="lines",
                line=dict(color=line_color, width=2.5),
                fill="tozeroy",
                fillcolor=rgba(line_color, 0.18)
            ))
            fig.update_layout(
                height=80,
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def gauge_chart(title, value, max_value, color, suffix=""):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={
            "suffix": suffix,
            "font": {
                "size": 34,
                "color": "#0f172a",
                "family": "Arial Black"
            }
        },
        gauge={
            "axis": {"range": [0, max_value], "visible": False},
            "bar": {"color": color, "thickness": 0.35},
            "bgcolor": "#e5e7eb",
            "borderwidth": 0,
            "steps": [
                {"range": [0, max_value * .35], "color": "#fee2e2"},
                {"range": [max_value * .35, max_value * .7], "color": "#fef3c7"},
                {"range": [max_value * .7, max_value], "color": "#dcfce7"},
            ],
        },
        title={"text": ""},
    ))

    fig.update_layout(
        height=230,
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
    )

    with st.container(border=True):
        st.markdown(
            f"""
            <div class="gauge-title">
                {title}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

def horizontal_bar(title, df, label_col, value_col, color="#2563eb", height=330, text_col=None):
    st.subheader(title)
    dfx = df.copy()
    dfx[value_col] = pd.to_numeric(dfx[value_col], errors="coerce").fillna(0)
    max_value = dfx[value_col].max()
    if max_value == 0:
        max_value = 1
    text_values = dfx[text_col] if text_col and text_col in dfx.columns else dfx[value_col].apply(lambda x: f"{x:,.0f}")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=dfx[value_col],
        y=dfx[label_col],
        orientation="h",
        text=text_values,
        textposition="outside",
        cliponaxis=False,
        marker=dict(color=color),
        textfont=dict(size=13),
    ))
    fig.update_layout(
        height=height,
        margin=dict(l=190, r=190, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[0, max_value * 1.30]),
        yaxis=dict(autorange="reversed", title="", tickfont=dict(size=14)),
        showlegend=False,
        font=dict(family="Microsoft JhengHei"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def line_chart(title, x, y, name, color="#2563eb", height=330):
    st.subheader(title)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode="lines+markers",
        name=name,
        line=dict(color=color, width=3),
        marker=dict(size=7),
    ))
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Microsoft JhengHei"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# =========================================================
# 頁面
# =========================================================
st.sidebar.header("篩選條件")
st.sidebar.write(f"期間：{PERIOD}")
st.sidebar.write(f"幣別：{CURRENCY}")
st.sidebar.divider()
st.sidebar.caption("資料類型：跨境電商廣告投放")
st.sidebar.caption("資料週期：7 天")

st.title(REPORT_TITLE)
st.caption(f"期間：{PERIOD}｜幣別：{CURRENCY}")

r1 = st.columns(4)
with r1[0]:
    metric_card("曝光量 IMP", number(core["曝光量 IMP"]), daily["曝光量 IMP"], "", "#6D3FD1")
with r1[1]:
    metric_card("點擊量", number(core["點擊量"]), daily["點擊量"], "", "#1FA7A1")
with r1[2]:
    metric_card("點擊率 CTR", percent(core["點擊率 CTR"]), click_trend["點擊率 CTR"], "", "#F0A500")
with r1[3]:
    metric_card("廣告花費", money(core["廣告花費"]), daily["廣告花費"], "", "#EF5350")

r2 = st.columns(4)
with r2[0]:
    metric_card("平均點擊成本 CPC", money2(core["平均點擊成本 CPC"]), click_trend["平均點擊成本 CPC"], "", "#B14AE0")
with r2[1]:
    metric_card("成交訂單數", number(core["成交訂單數"]), daily["成交訂單數"], "", "#42A5F5")
with r2[2]:
    metric_card("成交轉換率 CVR", percent(core["成交轉換率 CVR"]), order_trend["成交轉換率 CVR"], "", "#66BB6A")
with r2[3]:
    metric_card("商品交易總額 GMV", money(core["商品交易總額 GMV"]), daily["商品交易總額 GMV"], "", "#F05A5A")

r3 = st.columns(4)
with r3[0]:
    metric_card("廣告投資報酬率 ROAS", roas(core["廣告投資報酬率 ROAS"]), sales_trend["廣告投資報酬率 ROAS"], "", "#22C55E")
with r3[1]:
    metric_card("單筆成交成本 CPA", money2(core["單筆成交成本 CPA"]), order_trend["單筆成交成本 CPA"], "", "#64748B")
with r3[2]:
    metric_card("淨利", money(core["淨利"]), daily["淨利"], "", "#0EA5E9")
with r3[3]:
    metric_card("扣除退款後營收", money(core["扣除退款後營收"]), daily["扣除退款後營收"], "", "#A855F7")

st.subheader("核心成效總覽")
g1, g2, g3 = st.columns([1, 1, 2])

with g1:
    gauge_chart(
        "ROAS 廣告投報",
        core["廣告投資報酬率 ROAS"],
        10,
        "#22c55e",
        "x"
    )

with g2:
    gauge_chart(
        "淨利率",
        total_profit_rate,
        100,
        "#3b82f6",
        "%"
    )
with g3:
    with st.container(border=True):
        st.markdown("**核心成效總覽表**")
        st.dataframe(core_table, use_container_width=True, hide_index=True, height=330)

horizontal_bar(
    "平台銷售額排名",
    platform_rank,
    "銷售平台／通路",
    "商品交易總額 GMV",
    "#2563eb",
    350,
    text_col="報表顯示",
)

st.subheader("報表圖表用資料")
c1, c2 = st.columns(2)

with c1:
    line_chart("每日曝光趨勢", daily["日期"], daily["曝光量 IMP"], "曝光量 IMP", "#2563eb")
    line_chart("每日點擊趨勢", daily["日期"], daily["點擊量"], "點擊量", "#f97316")

with c2:
    line_chart("每日訂單趨勢", daily["日期"], daily["成交訂單數"], "成交訂單數", "#22c55e")
    line_chart("每日銷售額趨勢", daily["日期"], daily["商品交易總額 GMV"], "商品交易總額 GMV", "#a855f7")

st.dataframe(chart_table, use_container_width=True, hide_index=True)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "每日數據", "平台／市場", "商品／素材", "裝置／受眾", "轉換與退款", "營收與利潤"
])

with tab1:
    st.subheader("每日點擊趨勢")
    st.dataframe(display_df(click_display), use_container_width=True, hide_index=True)

    st.subheader("每日訂單趨勢")
    st.dataframe(display_df(order_display), use_container_width=True, hide_index=True)

    st.subheader("每日銷售額趨勢")
    st.dataframe(display_df(sales_display), use_container_width=True, hide_index=True)

    st.subheader("每日完整投放數據")
    st.dataframe(display_df(daily_full_display), use_container_width=True, hide_index=True)

with tab2:
    st.subheader("平台銷售額排名")
    st.dataframe(display_df(platform_rank_display), use_container_width=True, hide_index=True)

    st.subheader("廣告平台成效")
    st.dataframe(display_df(ad_platform_display), use_container_width=True, hide_index=True)

    st.subheader("國家市場成效")
    st.dataframe(display_df(country_display), use_container_width=True, hide_index=True)

    cc1, cc2 = st.columns(2)
    with cc1:
        horizontal_bar("廣告平台 GMV", ad_platform.assign(**{"商品交易總額 GMV": pd.to_numeric(ad_platform["商品交易總額 GMV"], errors="coerce").fillna(0)}).sort_values("商品交易總額 GMV", ascending=False), "廣告平台", "商品交易總額 GMV", "#2563eb", 360)
    with cc2:
        horizontal_bar("國家市場 GMV", country.assign(**{"商品交易總額 GMV": pd.to_numeric(country["商品交易總額 GMV"], errors="coerce").fillna(0)}).sort_values("商品交易總額 GMV", ascending=False), "國家市場", "商品交易總額 GMV", "#0ea5e9", 360)

with tab3:
    st.subheader("商品銷售成效")
    st.dataframe(display_df(product_display), use_container_width=True, hide_index=True)

    st.subheader("廣告素材成效")
    st.dataframe(display_df(creative_display), use_container_width=True, hide_index=True)

    horizontal_bar("商品 GMV", product.assign(**{"商品交易總額 GMV": pd.to_numeric(product["商品交易總額 GMV"], errors="coerce").fillna(0)}).sort_values("商品交易總額 GMV", ascending=False), "商品名稱", "商品交易總額 GMV", "#22c55e", 1150)
    horizontal_bar("廣告素材 GMV", creative.assign(**{"商品交易總額 GMV": pd.to_numeric(creative["商品交易總額 GMV"], errors="coerce").fillna(0)}).sort_values("商品交易總額 GMV", ascending=False), "廣告素材", "商品交易總額 GMV", "#f97316", 420)

with tab4:
    st.subheader("裝置來源成效")
    st.dataframe(display_df(device_display), use_container_width=True, hide_index=True)

    st.subheader("受眾年齡成效")
    st.dataframe(display_df(age_display), use_container_width=True, hide_index=True)

    st.subheader("受眾性別成效")
    st.dataframe(display_df(gender_display), use_container_width=True, hide_index=True)

    d1, d2, d3 = st.columns(3)
    with d1:
        horizontal_bar("裝置來源 GMV", device.assign(**{"商品交易總額 GMV": pd.to_numeric(device["商品交易總額 GMV"], errors="coerce").fillna(0)}).sort_values("商品交易總額 GMV", ascending=False), "裝置來源", "商品交易總額 GMV", "#2563eb", 340)
    with d2:
        horizontal_bar("受眾年齡 GMV", age.assign(**{"商品交易總額 GMV": pd.to_numeric(age["商品交易總額 GMV"], errors="coerce").fillna(0)}).sort_values("商品交易總額 GMV", ascending=False), "年齡層", "商品交易總額 GMV", "#a855f7", 340)
    with d3:
        horizontal_bar("受眾性別 GMV", gender.assign(**{"商品交易總額 GMV": pd.to_numeric(gender["商品交易總額 GMV"], errors="coerce").fillna(0)}).sort_values("商品交易總額 GMV", ascending=False), "性別", "商品交易總額 GMV", "#ec4899", 340)

with tab5:
    st.subheader("顧客轉換路徑")

    fig_funnel = go.Figure()
    fig_funnel.add_trace(go.Bar(
        x=funnel["數量"],
        y=funnel["轉換階段"],
        orientation="h",
        text=funnel["顯示數值"],
        textposition="outside",
        cliponaxis=False,
        marker=dict(color=["#2563eb", "#7c3aed", "#10b981", "#f59e0b", "#0ea5e9", "#22c55e"]),
    ))
    fig_funnel.update_layout(
        height=430,
        margin=dict(l=170, r=190, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[0, funnel["數量"].max() * 1.25]),
        yaxis=dict(autorange="reversed", title=""),
        showlegend=False,
        font=dict(family="Microsoft JhengHei"),
    )
    st.plotly_chart(fig_funnel, use_container_width=True, config={"displayModeBar": False})

    st.dataframe(funnel[["轉換階段", "顯示數值", "與上一階段轉換率"]], use_container_width=True, hide_index=True)

    st.subheader("訂單與退款資料")
    st.dataframe(display_df(refund), use_container_width=True, hide_index=True)

with tab6:
    st.subheader("營收與利潤")
    st.dataframe(display_df(profit), use_container_width=True, hide_index=True)

    total_profit = profit.iloc[-1]
    profit_chart = pd.DataFrame({
        "項目": ["扣除退款後營收", "廣告花費", "其他成本合計", "淨利"],
        "金額": [
            to_int(total_profit["扣除退款後營收"]),
            to_int(total_profit["廣告花費"]),
            to_int(total_profit["其他成本合計"]),
            to_int(total_profit["淨利"]),
        ],
    })
    profit_chart["顯示"] = profit_chart["金額"].apply(wan_label)
    horizontal_bar("營收與利潤結構", profit_chart, "項目", "金額", "#22c55e", 390, text_col="顯示")

st.markdown("<div class='section-title'>關鍵摘要</div>", unsafe_allow_html=True)
st.markdown(f"""
<div class="summary-box">
本期 <b>{REPORT_TITLE}</b> 期間為 <b>{PERIOD}</b>。<br>
曝光量 IMP <b>{number(core['曝光量 IMP'])}</b>、點擊量 <b>{number(core['點擊量'])}</b>、點擊率 CTR <b>{percent(core['點擊率 CTR'])}</b>。<br>
廣告花費 <b>{money(core['廣告花費'])}</b>，成交訂單數 <b>{number(core['成交訂單數'])}</b>，商品交易總額 GMV <b>{money(core['商品交易總額 GMV'])}</b>。<br>
廣告投資報酬率 ROAS <b>{roas(core['廣告投資報酬率 ROAS'])}</b>，單筆成交成本 CPA <b>{money2(core['單筆成交成本 CPA'])}</b>。<br>
淨利 <b>{money(core['淨利'])}</b>，扣除退款後營收 <b>{money(core['扣除退款後營收'])}</b>。
</div>
""", unsafe_allow_html=True)
