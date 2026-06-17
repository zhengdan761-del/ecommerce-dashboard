
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
期間	2026/06/05－2026/06/11
幣別	NTD 新台幣
曝光量 IMP	21,832,719
點擊量	548,963
點擊率 CTR	2.51%
廣告花費	NT$6,418,574
平均點擊成本 CPC	NT$11.69
成交訂單數	18,206
成交轉換率 CVR	3.32%
商品交易總額 GMV	NT$38,641,287
廣告投資報酬率 ROAS	6.02x
單筆成交成本 CPA	NT$352.55
淨利	NT$9,575,321
扣除退款後營收	NT$38,177,591

報表圖表用資料

圖表資料	2026/06/05	2026/06/06	2026/06/07	2026/06/08	2026/06/09	2026/06/10	2026/06/11	合計
曝光量 IMP	3,142,887	2,709,314	3,498,756	3,012,450	3,849,173	2,526,384	3,093,755	21,832,719
點擊量	78,132	64,178	89,425	73,319	100,846	59,472	83,591	548,963
成交訂單數	2,541	2,106	3,109	2,328	3,567	1,834	2,721	18,206
商品交易總額 GMV	NT$5,409,816	NT$4,312,785	NT$6,721,394	NT$4,858,607	NT$7,438,126	NT$3,952,481	NT$5,948,078	NT$38,641,287
廣告花費	NT$897,453	NT$822,719	NT$1,081,662	NT$865,388	NT$967,251	NT$812,940	NT$971,161	NT$6,418,574
淨利	NT$1,185,420	NT$694,385	NT$1,926,118	NT$1,008,219	NT$2,438,750	NT$598,114	NT$1,724,315	NT$9,575,321
扣除退款後營收	NT$5,344,991	NT$4,261,570	NT$6,634,180	NT$4,801,338	NT$7,345,445	NT$3,906,569	NT$5,883,498	NT$38,177,591

每日點擊趨勢

日期	曝光量 IMP	點擊量	點擊率 CTR	廣告花費	平均點擊成本 CPC
2026/06/05	3,142,887	78,132	2.49%	NT$897,453	NT$11.49
2026/06/06	2,709,314	64,178	2.37%	NT$822,719	NT$12.82
2026/06/07	3,498,756	89,425	2.56%	NT$1,081,662	NT$12.10
2026/06/08	3,012,450	73,319	2.43%	NT$865,388	NT$11.80
2026/06/09	3,849,173	100,846	2.62%	NT$967,251	NT$9.59
2026/06/10	2,526,384	59,472	2.35%	NT$812,940	NT$13.67
2026/06/11	3,093,755	83,591	2.70%	NT$971,161	NT$11.62
合計	21,832,719	548,963	2.51%	NT$6,418,574	NT$11.69

每日訂單趨勢

日期	點擊量	成交訂單數	成交轉換率 CVR	廣告花費	單筆成交成本 CPA
2026/06/05	78,132	2,541	3.25%	NT$897,453	NT$353.19
2026/06/06	64,178	2,106	3.28%	NT$822,719	NT$390.65
2026/06/07	89,425	3,109	3.48%	NT$1,081,662	NT$347.91
2026/06/08	73,319	2,328	3.18%	NT$865,388	NT$371.73
2026/06/09	100,846	3,567	3.54%	NT$967,251	NT$271.17
2026/06/10	59,472	1,834	3.08%	NT$812,940	NT$443.26
2026/06/11	83,591	2,721	3.26%	NT$971,161	NT$356.91
合計	548,963	18,206	3.32%	NT$6,418,574	NT$352.55

每日銷售額趨勢

日期	成交訂單數	商品交易總額 GMV	廣告花費	廣告投資報酬率 ROAS	淨利	扣除退款後營收	淨利率
2026/06/05	2,541	NT$5,409,816	NT$897,453	6.03x	NT$1,185,420	NT$5,344,991	22.18%
2026/06/06	2,106	NT$4,312,785	NT$822,719	5.24x	NT$694,385	NT$4,261,570	16.29%
2026/06/07	3,109	NT$6,721,394	NT$1,081,662	6.21x	NT$1,926,118	NT$6,634,180	29.03%
2026/06/08	2,328	NT$4,858,607	NT$865,388	5.61x	NT$1,008,219	NT$4,801,338	21.00%
2026/06/09	3,567	NT$7,438,126	NT$967,251	7.69x	NT$2,438,750	NT$7,345,445	33.20%
2026/06/10	1,834	NT$3,952,481	NT$812,940	4.86x	NT$598,114	NT$3,906,569	15.31%
2026/06/11	2,721	NT$5,948,078	NT$971,161	6.12x	NT$1,724,315	NT$5,883,498	29.31%
合計	18,206	NT$38,641,287	NT$6,418,574	6.02x	NT$9,575,321	NT$38,177,591	25.08%

平台銷售額排名

排名	銷售平台／通路	成交訂單數	商品交易總額 GMV	銷售占比
1	自有品牌站／Shopify Plus	7,647	NT$16,615,753	43.00%
2	TikTok Shop	4,369	NT$9,080,702	23.50%
3	Amazon Marketplace	2,913	NT$5,989,400	15.50%
4	eBay	1,457	NT$3,052,662	7.90%
5	Shopee Cross-border	1,092	NT$2,241,195	5.80%
6	Walmart Marketplace	728	NT$1,661,575	4.30%
合計		18,206	NT$38,641,287	100.00%

每日完整投放數據

日期	曝光量 IMP	點擊量	點擊率 CTR	廣告花費	平均點擊成本 CPC	成交訂單數	成交轉換率 CVR	商品交易總額 GMV	廣告投資報酬率 ROAS	單筆成交成本 CPA	淨利	扣除退款後營收	淨利率
2026/06/05	3,142,887	78,132	2.49%	NT$897,453	NT$11.49	2,541	3.25%	NT$5,409,816	6.03x	NT$353.19	NT$1,185,420	NT$5,344,991	22.18%
2026/06/06	2,709,314	64,178	2.37%	NT$822,719	NT$12.82	2,106	3.28%	NT$4,312,785	5.24x	NT$390.65	NT$694,385	NT$4,261,570	16.29%
2026/06/07	3,498,756	89,425	2.56%	NT$1,081,662	NT$12.10	3,109	3.48%	NT$6,721,394	6.21x	NT$347.91	NT$1,926,118	NT$6,634,180	29.03%
2026/06/08	3,012,450	73,319	2.43%	NT$865,388	NT$11.80	2,328	3.18%	NT$4,858,607	5.61x	NT$371.73	NT$1,008,219	NT$4,801,338	21.00%
2026/06/09	3,849,173	100,846	2.62%	NT$967,251	NT$9.59	3,567	3.54%	NT$7,438,126	7.69x	NT$271.17	NT$2,438,750	NT$7,345,445	33.20%
2026/06/10	2,526,384	59,472	2.35%	NT$812,940	NT$13.67	1,834	3.08%	NT$3,952,481	4.86x	NT$443.26	NT$598,114	NT$3,906,569	15.31%
2026/06/11	3,093,755	83,591	2.70%	NT$971,161	NT$11.62	2,721	3.26%	NT$5,948,078	6.12x	NT$356.91	NT$1,724,315	NT$5,883,498	29.31%
合計	21,832,719	548,963	2.51%	NT$6,418,574	NT$11.69	18,206	3.32%	NT$38,641,287	6.02x	NT$352.55	NT$9,575,321	NT$38,177,591	25.08%

廣告平台成效

廣告平台	曝光量 IMP	點擊量	點擊率 CTR	廣告花費	平均點擊成本 CPC	成交訂單數	成交轉換率 CVR	商品交易總額 GMV	廣告投資報酬率 ROAS	單筆成交成本 CPA	扣除退款後營收	淨利	淨利率
TikTok Ads	8,514,760	230,564	2.71%	NT$2,567,430	NT$11.14	6,918	3.00%	NT$13,910,863	5.42x	NT$371.12	NT$13,743,933	NT$1,723,558	12.54%
Meta Ads	5,894,834	153,710	2.61%	NT$1,797,201	NT$11.69	5,462	3.55%	NT$11,592,386	6.45x	NT$329.04	NT$11,453,277	NT$4,021,635	35.11%
Google Ads	3,929,889	87,834	2.24%	NT$1,283,715	NT$14.62	3,277	3.73%	NT$6,955,432	5.42x	NT$391.73	NT$6,871,967	NT$1,915,064	27.87%
Pinterest Ads	1,746,618	49,407	2.83%	NT$385,114	NT$7.79	1,548	3.13%	NT$3,477,716	9.03x	NT$248.78	NT$3,435,983	NT$1,532,051	44.59%
Snapchat Ads	1,746,618	27,448	1.57%	NT$385,114	NT$14.03	1,001	3.65%	NT$2,704,890	7.02x	NT$384.73	NT$2,672,431	NT$383,013	14.33%
合計	21,832,719	548,963	2.51%	NT$6,418,574	NT$11.69	18,206	3.32%	NT$38,641,287	6.02x	NT$352.55	NT$38,177,591	NT$9,575,321	25.08%

國家市場成效

國家市場	曝光量 IMP	點擊量	點擊率 CTR	廣告花費	平均點擊成本 CPC	成交訂單數	成交轉換率 CVR	商品交易總額 GMV	廣告投資報酬率 ROAS	單筆成交成本 CPA	扣除退款後營收	淨利	淨利率
United States 美國	8,951,415	230,565	2.58%	NT$2,695,801	NT$11.69	7,100	3.08%	NT$14,683,689	5.45x	NT$379.69	NT$14,507,485	NT$1,915,064	13.20%
United Kingdom 英國	3,493,235	98,813	2.83%	NT$962,786	NT$9.74	3,277	3.32%	NT$6,955,432	7.22x	NT$293.80	NT$6,871,966	NT$2,968,350	43.20%
Canada 加拿大	3,056,581	71,365	2.33%	NT$898,600	NT$12.59	2,549	3.57%	NT$5,409,780	6.02x	NT$352.53	NT$5,344,863	NT$1,436,298	26.87%
Australia 澳洲	2,401,599	54,896	2.29%	NT$770,229	NT$14.03	1,821	3.32%	NT$3,864,129	5.02x	NT$422.97	NT$3,817,759	NT$766,026	20.06%
Japan 日本	2,183,272	43,917	2.01%	NT$641,857	NT$14.62	1,457	3.32%	NT$3,477,716	5.42x	NT$440.53	NT$3,435,983	NT$670,272	19.51%
Singapore 新加坡	982,472	32,938	3.35%	NT$320,929	NT$9.74	1,365	4.14%	NT$2,511,683	7.83x	NT$235.11	NT$2,481,543	NT$1,340,545	54.02%
Malaysia 馬來西亞	764,145	16,469	2.16%	NT$128,372	NT$7.79	637	3.87%	NT$1,738,858	13.55x	NT$201.53	NT$1,717,992	NT$478,766	27.87%
合計	21,832,719	548,963	2.51%	NT$6,418,574	NT$11.69	18,206	3.32%	NT$38,641,287	6.02x	NT$352.55	NT$38,177,591	NT$9,575,321	25.08%

商品銷售成效

商品名稱	商品類型	參考單價帶	平均客單價 AOV	曝光量 IMP	點擊量	點擊率 CTR	廣告花費	平均點擊成本 CPC	成交訂單數	成交轉換率 CVR	商品交易總額 GMV	廣告投資報酬率 ROAS	單筆成交成本 CPA	淨利	扣除退款後營收	淨利率
智能香氛小夜燈	居家氛圍／生活小家電	NT$970－NT$1,870	NT$2,341.84	358,334	12,890	3.60%	NT$138,379	NT$10.74	548	4.25%	NT$1,283,327	9.27x	NT$252.52	NT$253,017	NT$1,276,153	19.83%
桌面空氣循環扇	辦公室／居家小家電	NT$1,040－NT$2,020	NT$2,915.57	194,024	7,858	4.05%	NT$72,982	NT$9.29	235	2.99%	NT$685,158	9.39x	NT$310.56	NT$182,506	NT$679,822	26.85%
智能空氣淨化器	居家健康／空氣清潔設備	NT$3,740－NT$7,240	NT$7,515.98	1,113,074	19,178	1.72%	NT$580,549	NT$30.27	249	1.30%	NT$1,871,478	3.22x	NT$2,331.52	NT$202,553	NT$1,852,423	10.93%
智能廚房秤	廚房用品／智能小工具	NT$520－NT$1,000	NT$1,344.06	410,969	12,394	3.02%	NT$288,861	NT$23.31	677	5.46%	NT$909,927	3.15x	NT$426.68	NT$269,280	NT$892,350	30.18%
便攜式保溫杯	生活用品／外出隨行	NT$590－NT$1,150	NT$1,343.03	182,358	5,822	3.19%	NT$25,019	NT$4.30	213	3.66%	NT$286,065	11.43x	NT$117.46	NT$81,759	NT$284,282	28.76%
多功能收納包	旅行／居家收納用品	NT$670－NT$1,290	NT$2,206.97	382,160	7,321	1.92%	NT$95,736	NT$13.08	227	3.10%	NT$500,982	5.23x	NT$421.74	NT$176,533	NT$492,213	35.87%
旅行壓縮袋組	旅行用品／行李收納	NT$820－NT$1,580	NT$2,330.54	467,449	14,168	3.03%	NT$97,771	NT$6.90	796	5.62%	NT$1,855,110	18.97x	NT$122.83	NT$656,059	NT$1,843,522	35.59%
磁吸式無線充電座	3C配件／桌面充電	NT$970－NT$1,870	NT$2,966.78	183,532	6,113	3.33%	NT$70,836	NT$11.59	248	4.06%	NT$735,762	10.39x	NT$285.63	NT$179,054	NT$729,079	24.56%
藍牙降噪耳機	3C配件／影音設備	NT$1,870－NT$3,610	NT$4,892.96	485,135	11,596	2.39%	NT$303,399	NT$26.16	203	1.75%	NT$993,271	3.27x	NT$1,494.58	NT$69,829	NT$978,778	7.13%
手機防水收納袋	戶外用品／手機配件	NT$290－NT$570	NT$1,137.75	266,264	8,721	3.28%	NT$95,722	NT$10.98	326	3.74%	NT$370,908	3.87x	NT$293.63	NT$50,672	NT$365,864	13.85%
摺疊式手機支架	3C配件／桌面用品	NT$340－NT$650	NT$1,215.49	168,007	5,777	3.44%	NT$107,650	NT$18.63	155	2.68%	NT$188,401	1.75x	NT$694.52	NT$52,620	NT$186,517	28.21%
LED補光化妝鏡	美妝工具／居家小物	NT$890－NT$1,730	NT$2,444.94	344,948	12,231	3.55%	NT$68,458	NT$5.60	527	4.31%	NT$1,288,485	18.82x	NT$129.90	NT$64,668	NT$1,275,600	5.07%
電動筋膜按摩器	健康放鬆／按摩設備	NT$2,240－NT$4,340	NT$6,128.15	250,292	6,919	2.76%	NT$96,895	NT$14.00	387	5.59%	NT$2,371,594	24.48x	NT$250.37	NT$90,202	NT$2,347,878	3.84%
頸掛式小風扇	夏季用品／個人小家電	NT$740－NT$1,440	NT$2,129.39	1,593,263	29,550	1.85%	NT$228,182	NT$7.72	1,076	3.64%	NT$2,291,224	10.04x	NT$212.07	NT$437,526	NT$2,248,542	19.46%
USB加熱暖手寶	冬季用品／生活小家電	NT$520－NT$1,000	NT$1,455.85	254,870	8,253	3.24%	NT$76,811	NT$9.31	423	5.13%	NT$615,825	8.02x	NT$181.59	NT$77,674	NT$606,462	12.81%
智能感應垃圾桶	居家用品／智能生活	NT$1,420－NT$2,740	NT$4,355.52	279,012	9,278	3.33%	NT$105,288	NT$11.35	120	1.29%	NT$522,662	4.96x	NT$877.40	NT$27,976	NT$520,614	5.37%
防滑浴室地墊	居家用品／浴室收納	NT$440－NT$860	NT$1,200.06	315,866	9,707	3.07%	NT$31,515	NT$3.25	362	3.73%	NT$434,423	13.78x	NT$87.06	NT$198,413	NT$427,241	46.44%
廚房瀝水置物架	廚房用品／收納整理	NT$890－NT$1,730	NT$3,105.13	171,547	3,357	1.96%	NT$53,410	NT$15.91	155	4.62%	NT$481,295	9.01x	NT$344.58	NT$145,063	NT$472,532	30.70%
矽膠保鮮袋組	廚房用品／環保收納	NT$370－NT$710	NT$1,138.60	290,051	7,370	2.54%	NT$31,906	NT$4.33	303	4.11%	NT$344,995	10.81x	NT$105.30	NT$108,078	NT$340,822	31.71%
不鏽鋼保鮮盒	廚房用品／食物收納	NT$670－NT$1,290	NT$2,031.02	853,519	20,568	2.41%	NT$151,840	NT$7.38	300	1.46%	NT$609,305	4.01x	NT$506.13	NT$103,082	NT$605,162	17.03%
可折疊購物袋	生活用品／外出收納	NT$290－NT$570	NT$1,118.83	183,517	7,111	3.87%	NT$27,844	NT$3.92	409	5.75%	NT$457,600	16.43x	NT$68.08	NT$180,787	NT$454,610	39.77%
旅行盥洗收納包	旅行用品／盥洗收納	NT$590－NT$1,150	NT$1,610.77	426,577	14,797	3.47%	NT$161,970	NT$10.95	276	1.87%	NT$444,573	2.74x	NT$586.85	NT$141,788	NT$436,878	32.45%
護照證件收納包	旅行用品／證件收納	NT$520－NT$1,000	NT$1,284.65	835,475	14,672	1.76%	NT$57,097	NT$3.89	651	4.44%	NT$836,307	14.65x	NT$87.71	NT$391,637	NT$832,111	47.07%
行李箱電子秤	旅行用品／行李配件	NT$440－NT$860	NT$1,404.22	845,690	17,867	2.11%	NT$124,197	NT$6.95	286	1.60%	NT$401,606	3.23x	NT$434.26	NT$183,217	NT$396,602	46.20%
車用手機支架	汽車用品／車內配件	NT$590－NT$1,150	NT$1,369.51	195,246	5,954	3.05%	NT$36,837	NT$6.19	253	4.25%	NT$346,487	9.41x	NT$145.60	NT$67,438	NT$344,096	19.60%
車用香氛擴香器	汽車用品／車內香氛	NT$740－NT$1,440	NT$2,134.10	261,883	7,130	2.72%	NT$88,751	NT$12.45	204	2.86%	NT$435,356	4.91x	NT$435.05	NT$51,046	NT$431,661	11.83%
車用吸塵器	汽車用品／清潔設備	NT$1,190－NT$2,310	NT$3,954.10	367,727	11,554	3.14%	NT$137,376	NT$11.89	390	3.38%	NT$1,542,098	11.23x	NT$352.25	NT$553,646	NT$1,512,111	36.61%
寵物飲水機	寵物用品／智能設備	NT$1,490－NT$2,890	NT$4,169.85	433,790	9,656	2.23%	NT$383,522	NT$39.72	281	2.91%	NT$1,171,727	3.06x	NT$1,364.85	NT$127,549	NT$1,162,250	10.97%
寵物除毛刷	寵物用品／清潔護理	NT$520－NT$1,000	NT$1,500.57	882,702	16,378	1.86%	NT$60,377	NT$3.69	369	2.25%	NT$553,712	9.17x	NT$163.62	NT$82,988	NT$545,581	15.21%
寵物外出水壺	寵物用品／外出用品	NT$490－NT$940	NT$1,050.71	461,446	14,975	3.25%	NT$41,580	NT$2.78	350	2.34%	NT$367,747	8.84x	NT$118.80	NT$67,011	NT$361,846	18.52%
瑜珈彈力帶組	運動用品／健身配件	NT$440－NT$860	NT$1,436.44	319,134	13,586	4.26%	NT$155,782	NT$11.47	805	5.93%	NT$1,156,338	7.42x	NT$193.52	NT$445,594	NT$1,146,768	38.86%
防滑瑜珈墊	運動用品／居家健身	NT$1,270－NT$2,450	NT$3,469.04	219,565	7,873	3.59%	NT$95,247	NT$12.10	397	5.04%	NT$1,377,207	14.46x	NT$239.92	NT$598,576	NT$1,368,973	43.72%
運動水壺	運動用品／外出補水	NT$520－NT$1,000	NT$1,347.16	208,819	6,298	3.02%	NT$58,343	NT$9.26	270	4.29%	NT$363,732	6.23x	NT$216.09	NT$20,427	NT$357,868	5.71%
快乾運動毛巾	運動用品／戶外用品	NT$370－NT$710	NT$1,365.53	99,327	3,748	3.77%	NT$20,833	NT$5.56	165	4.40%	NT$225,312	10.82x	NT$126.26	NT$36,415	NT$222,843	16.34%
露營LED掛燈	戶外用品／露營照明	NT$740－NT$1,440	NT$2,231.29	449,587	12,411	2.76%	NT$75,528	NT$6.09	497	4.00%	NT$1,108,951	14.68x	NT$151.97	NT$317,787	NT$1,099,780	28.90%
戶外折疊椅	戶外用品／露營家具	NT$1,790－NT$3,470	NT$4,563.34	2,027,845	28,698	1.42%	NT$277,622	NT$9.67	681	2.37%	NT$3,107,635	11.19x	NT$407.67	NT$958,936	NT$3,085,776	31.08%
便攜餐具組	戶外用品／旅行餐具	NT$370－NT$710	NT$914.98	372,909	6,824	1.83%	NT$20,710	NT$3.03	194	2.84%	NT$177,507	8.57x	NT$106.75	NT$63,354	NT$174,036	36.40%
防水收納乾濕袋	旅行用品／戶外收納	NT$440－NT$860	NT$1,296.19	212,831	4,838	2.27%	NT$17,188	NT$3.55	163	3.37%	NT$211,279	12.29x	NT$105.45	NT$70,178	NT$208,304	33.69%
兒童防漏水杯	親子用品／兒童餐具	NT$520－NT$1,000	NT$1,614.75	150,468	6,215	4.13%	NT$36,420	NT$5.86	189	3.04%	NT$305,188	8.38x	NT$192.70	NT$29,595	NT$301,500	9.82%
兒童矽膠圍兜	親子用品／用餐用品	NT$370－NT$710	NT$1,198.89	391,737	14,976	3.82%	NT$31,534	NT$2.11	275	1.84%	NT$329,695	10.46x	NT$114.67	NT$87,335	NT$327,897	26.63%
嬰兒推車收納袋	親子用品／外出收納	NT$670－NT$1,290	NT$1,886.16	821,364	21,848	2.66%	NT$64,189	NT$2.94	381	1.74%	NT$718,626	11.20x	NT$168.48	NT$191,887	NT$705,406	27.20%
居家防撞條組	親子用品／安全防護	NT$370－NT$710	NT$1,078.33	133,423	4,378	3.28%	NT$20,568	NT$4.70	218	4.98%	NT$235,076	11.43x	NT$94.35	NT$37,899	NT$232,961	16.27%
收納抽屜分隔板	居家收納／衣櫃整理	NT$520－NT$1,000	NT$1,715.61	297,956	8,020	2.69%	NT$112,353	NT$14.01	151	1.88%	NT$259,057	2.31x	NT$744.06	NT$27,522	NT$254,803	10.80%
真空壓縮收納袋	居家收納／換季整理	NT$590－NT$1,150	NT$1,624.30	458,156	9,218	2.01%	NT$95,836	NT$10.40	606	6.57%	NT$984,325	10.27x	NT$158.15	NT$350,657	NT$966,330	36.29%
衣物除毛球機	居家用品／衣物護理	NT$670－NT$1,290	NT$1,743.37	367,708	9,804	2.67%	NT$184,219	NT$18.79	467	4.76%	NT$814,153	4.42x	NT$394.47	NT$369,324	NT$808,503	45.68%
迷你熨燙機	居家用品／衣物整理	NT$1,190－NT$2,310	NT$3,913.69	531,335	19,670	3.70%	NT$606,243	NT$30.82	264	1.34%	NT$1,033,213	1.70x	NT$2,296.38	NT$132,851	NT$1,013,108	13.11%
防藍光眼鏡	健康用品／護眼配件	NT$590－NT$1,150	NT$1,953.58	291,736	8,135	2.79%	NT$261,761	NT$32.18	354	4.35%	NT$691,568	2.64x	NT$739.44	NT$51,709	NT$679,051	7.61%
睡眠遮光眼罩	生活用品／睡眠配件	NT$440－NT$860	NT$1,312.65	347,653	9,256	2.66%	NT$49,105	NT$5.31	378	4.08%	NT$496,181	10.10x	NT$129.91	NT$96,283	NT$489,839	19.66%
人體工學滑鼠墊	辦公用品／桌面配件	NT$520－NT$1,000	NT$1,671.53	288,022	7,873	2.73%	NT$46,100	NT$5.86	464	5.89%	NT$775,588	16.82x	NT$99.35	NT$316,734	NT$763,686	41.47%
桌面理線收納盒	辦公用品／桌面收納	NT$370－NT$710	NT$723.88	256,602	5,770	2.25%	NT$36,746	NT$6.37	247	4.28%	NT$178,799	4.87x	NT$148.77	NT$12,958	NT$177,351	7.31%
合計				21,832,719	548,963	2.51%	NT$6,418,574	NT$11.69	18,206	3.32%	NT$38,641,287	6.02x	NT$352.55	NT$9,575,321	NT$38,177,591	25.08%

廣告素材成效

廣告素材	素材類型	曝光量 IMP	點擊量	點擊率 CTR	廣告花費	平均點擊成本 CPC	成交訂單數	成交轉換率 CVR	商品交易總額 GMV	廣告投資報酬率 ROAS	單筆成交成本 CPA	扣除退款後營收	淨利	淨利率
短影音A｜高單價家電開箱	15秒短影音	5,458,180	109,793	2.01%	NT$1,476,272	NT$13.45	3,277	2.98%	NT$8,114,670	5.50x	NT$450.49	NT$8,017,294	NT$1,053,285	13.14%
短影音B｜旅行收納前後對比	20秒短影音	4,366,544	126,261	2.89%	NT$962,786	NT$7.63	4,370	3.46%	NT$8,501,083	8.83x	NT$220.32	NT$8,399,070	NT$3,159,856	37.62%
短影音C｜辦公桌面改造	18秒短影音	3,056,581	76,855	2.51%	NT$898,601	NT$11.69	2,731	3.55%	NT$5,409,780	6.02x	NT$329.04	NT$5,344,863	NT$1,723,558	32.25%
短影音D｜寵物日常實測	25秒短影音	2,838,253	65,876	2.32%	NT$1,283,715	NT$19.49	2,367	3.59%	NT$5,796,193	4.52x	NT$542.34	NT$5,726,639	NT$1,149,038	20.06%
輪播圖E｜低單價爆品合集	圖文輪播	3,493,235	126,261	3.61%	NT$898,600	NT$7.12	4,187	3.32%	NT$6,182,606	6.88x	NT$214.62	NT$6,108,414	NT$2,106,571	34.49%
再行銷F｜購物車限時優惠	再行銷素材	2,619,926	43,917	1.68%	NT$898,600	NT$20.46	1,274	2.90%	NT$4,636,955	5.16x	NT$705.34	NT$4,581,311	NT$383,013	8.36%
合計		21,832,719	548,963	2.51%	NT$6,418,574	NT$11.69	18,206	3.32%	NT$38,641,287	6.02x	NT$352.55	NT$38,177,591	NT$9,575,321	25.08%

裝置來源成效

裝置來源	曝光量 IMP	點擊量	點擊率 CTR	廣告花費	平均點擊成本 CPC	成交訂單數	成交轉換率 CVR	商品交易總額 GMV	廣告投資報酬率 ROAS	單筆成交成本 CPA	扣除退款後營收	淨利	淨利率
Mobile App / 行動裝置	15,937,885	406,232	2.55%	NT$4,493,002	NT$11.06	13,108	3.23%	NT$27,821,727	6.19x	NT$342.77	NT$27,487,866	NT$5,840,946	21.25%
Desktop Web / 桌機網頁	3,711,562	93,324	2.51%	NT$1,155,343	NT$12.38	3,277	3.51%	NT$6,955,432	6.02x	NT$352.56	NT$6,871,966	NT$1,915,064	27.87%
Tablet / 平板	1,309,963	32,938	2.51%	NT$513,486	NT$15.59	1,093	3.32%	NT$2,318,477	4.52x	NT$469.80	NT$2,290,655	NT$1,149,039	50.16%
In-App Webview / 內嵌瀏覽器	873,309	16,469	1.89%	NT$256,743	NT$15.59	728	4.42%	NT$1,545,651	6.02x	NT$352.67	NT$1,527,104	NT$670,272	43.89%
合計	21,832,719	548,963	2.51%	NT$6,418,574	NT$11.69	18,206	3.32%	NT$38,641,287	6.02x	NT$352.55	NT$38,177,591	NT$9,575,321	25.08%

受眾年齡成效

年齡層	曝光量 IMP	點擊量	點擊率 CTR	廣告花費	平均點擊成本 CPC	成交訂單數	成交轉換率 CVR	商品交易總額 GMV	廣告投資報酬率 ROAS	單筆成交成本 CPA	扣除退款後營收	淨利	淨利率
18-24	3,929,890	98,813	2.51%	NT$1,155,343	NT$11.69	2,913	2.95%	NT$6,182,606	5.35x	NT$396.62	NT$6,108,415	NT$1,340,545	21.95%
25-34	8,514,760	219,585	2.58%	NT$2,567,430	NT$11.69	7,646	3.48%	NT$15,842,928	6.17x	NT$335.79	NT$15,652,812	NT$4,021,635	25.69%
35-44	5,894,834	142,731	2.42%	NT$1,668,829	NT$11.69	4,916	3.44%	NT$10,433,147	6.25x	NT$339.47	NT$10,307,950	NT$2,202,324	21.37%
45-54	2,401,599	60,386	2.51%	NT$706,043	NT$11.69	1,821	3.02%	NT$4,250,542	6.02x	NT$387.72	NT$4,199,535	NT$1,149,038	27.36%
55+	1,091,636	27,448	2.51%	NT$320,929	NT$11.69	910	3.32%	NT$1,932,064	6.02x	NT$352.67	NT$1,908,879	NT$861,779	45.15%
合計	21,832,719	548,963	2.51%	NT$6,418,574	NT$11.69	18,206	3.32%	NT$38,641,287	6.02x	NT$352.55	NT$38,177,591	NT$9,575,321	25.08%

受眾性別成效

性別	曝光量 IMP	點擊量	點擊率 CTR	廣告花費	平均點擊成本 CPC	成交訂單數	成交轉換率 CVR	商品交易總額 GMV	廣告投資報酬率 ROAS	單筆成交成本 CPA	扣除退款後營收	淨利	淨利率
女性	13,536,286	345,847	2.55%	NT$3,851,144	NT$11.14	11,288	3.26%	NT$23,571,185	6.12x	NT$341.17	NT$23,288,330	NT$5,553,686	23.85%
男性	6,986,470	175,668	2.51%	NT$2,182,315	NT$12.42	6,008	3.42%	NT$13,138,038	6.02x	NT$363.23	NT$12,980,381	NT$3,255,609	25.08%
未揭露／其他	1,309,963	27,448	2.10%	NT$385,115	NT$14.03	910	3.32%	NT$1,932,064	5.02x	NT$423.20	NT$1,908,880	NT$766,026	40.13%
合計	21,832,719	548,963	2.51%	NT$6,418,574	NT$11.69	18,206	3.32%	NT$38,641,287	6.02x	NT$352.55	NT$38,177,591	NT$9,575,321	25.08%

顧客轉換路徑

轉換階段	數量	與上一階段轉換率
曝光量 IMP	21,832,719	-
點擊量	548,963	2.51%
成交訂單數	18,206	3.32%
商品交易總額 GMV	NT$38,641,287	-
扣除退款後營收	NT$38,177,591	98.80%
淨利	NT$9,575,321	25.08%

訂單與退款資料

日期	成交訂單數	商品交易總額 GMV	退款金額	扣除退款後營收	淨利
2026/06/05	2,541	NT$5,409,816	NT$64,825	NT$5,344,991	NT$1,185,420
2026/06/06	2,106	NT$4,312,785	NT$51,215	NT$4,261,570	NT$694,385
2026/06/07	3,109	NT$6,721,394	NT$87,214	NT$6,634,180	NT$1,926,118
2026/06/08	2,328	NT$4,858,607	NT$57,269	NT$4,801,338	NT$1,008,219
2026/06/09	3,567	NT$7,438,126	NT$92,681	NT$7,345,445	NT$2,438,750
2026/06/10	1,834	NT$3,952,481	NT$45,912	NT$3,906,569	NT$598,114
2026/06/11	2,721	NT$5,948,078	NT$64,580	NT$5,883,498	NT$1,724,315
合計	18,206	NT$38,641,287	NT$463,696	NT$38,177,591	NT$9,575,321

營收與利潤

日期	商品交易總額 GMV	退款金額	扣除退款後營收	商品成本	國際物流／履約成本	倉儲與包裝成本	平台／金流手續費	跨境關稅／稅務成本	退貨損耗	客服與營運成本	廣告花費	淨利	淨利率
2026/06/05	NT$5,409,816	NT$64,825	NT$5,344,991	NT$1,598,438	NT$456,697	NT$146,795	NT$195,727	NT$179,416	NT$114,174	NT$570,871	NT$897,453	NT$1,185,420	22.18%
2026/06/06	NT$4,312,785	NT$51,215	NT$4,261,570	NT$1,180,120	NT$356,781	NT$137,223	NT$178,390	NT$137,223	NT$68,612	NT$686,117	NT$822,719	NT$694,385	16.29%
2026/06/07	NT$6,721,394	NT$87,214	NT$6,634,180	NT$1,885,728	NT$543,960	NT$145,056	NT$199,452	NT$126,924	NT$145,056	NT$580,224	NT$1,081,662	NT$1,926,118	29.03%
2026/06/08	NT$4,858,607	NT$57,269	NT$4,801,338	NT$1,346,756	NT$322,051	NT$131,748	NT$175,664	NT$161,025	NT$73,193	NT$717,294	NT$865,388	NT$1,008,219	21.00%
2026/06/09	NT$7,438,126	NT$92,681	NT$7,345,445	NT$1,575,778	NT$393,944	NT$157,578	NT$256,064	NT$177,275	NT$78,789	NT$1,300,016	NT$967,251	NT$2,438,750	33.20%
2026/06/10	NT$3,952,481	NT$45,912	NT$3,906,569	NT$1,372,533	NT$399,283	NT$137,253	NT$149,731	NT$149,731	NT$112,298	NT$174,686	NT$812,940	NT$598,114	15.31%
2026/06/11	NT$5,948,078	NT$64,580	NT$5,883,498	NT$1,338,969	NT$382,563	NT$127,521	NT$175,341	NT$127,521	NT$79,700	NT$956,407	NT$971,161	NT$1,724,315	29.31%
7天合計	NT$38,641,287	NT$463,696	NT$38,177,591	NT$10,298,322	NT$2,855,279	NT$983,174	NT$1,330,369	NT$1,059,115	NT$671,822	NT$4,985,615	NT$6,418,574	NT$9,575,321	25.08%"""

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
    return pd.read_csv(StringIO("\n".join(lines)), sep="\t", dtype=str).fillna("")

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
    int_cols = ["曝光量 IMP", "點擊量", "成交訂單數", "商品交易總額 GMV", "廣告花費", "淨利", "扣除退款後營收", "退款金額", "其他成本合計", "商品成本", "國際物流／履約成本", "倉儲與包裝成本", "平台／金流手續費", "跨境關稅／稅務成本", "退貨損耗", "客服與營運成本", "數量"]
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
        "其他成本合計", "商品成本", "國際物流／履約成本", "倉儲與包裝成本", "平台／金流手續費", "跨境關稅／稅務成本", "退貨損耗", "客服與營運成本", "平均客單價 AOV"
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
