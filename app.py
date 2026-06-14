
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
3	Amazon Marketplace	2,913	NT$5,989,399	15.50%
4	eBay	1,456	NT$3,052,662	7.90%
5	Shopee Cross-border	1,092	NT$2,241,195	5.80%
6	Walmart Marketplace	729	NT$1,661,576	4.30%
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
TikTok Ads	8,514,760	230,564	2.71%	NT$2,567,430	NT$11.14	7,100	3.08%	NT$13,910,863	5.42x	NT$361.61	NT$13,743,933	NT$1,723,558	12.54%
Meta Ads	6,113,161	153,710	2.51%	NT$1,797,201	NT$11.69	5,644	3.67%	NT$11,592,386	6.45x	NT$318.43	NT$11,453,277	NT$4,021,635	35.11%
Google Ads	3,929,890	87,834	2.24%	NT$1,283,715	NT$14.62	3,095	3.52%	NT$6,955,432	5.42x	NT$414.77	NT$6,871,967	NT$1,819,311	26.47%
Pinterest Ads	1,746,618	49,407	2.83%	NT$385,114	NT$7.79	1,456	2.95%	NT$3,477,716	9.03x	NT$264.50	NT$3,435,983	NT$1,532,051	44.59%
Snapchat Ads	1,528,290	27,448	1.80%	NT$385,114	NT$14.03	911	3.32%	NT$2,704,890	7.02x	NT$422.74	NT$2,672,431	NT$478,766	17.92%
合計	21,832,719	548,963	2.51%	NT$6,418,574	NT$11.69	18,206	3.32%	NT$38,641,287	6.02x	NT$352.55	NT$38,177,591	NT$9,575,321	25.08%

國家市場成效

國家市場	曝光量 IMP	點擊量	點擊率 CTR	廣告花費	平均點擊成本 CPC	成交訂單數	成交轉換率 CVR	商品交易總額 GMV	廣告投資報酬率 ROAS	單筆成交成本 CPA	扣除退款後營收	淨利	淨利率
United States 美國	8,951,415	230,565	2.58%	NT$2,695,801	NT$11.69	7,100	3.08%	NT$14,683,689	5.45x	NT$379.69	NT$14,507,485	NT$1,915,064	13.20%
United Kingdom 英國	3,493,235	98,814	2.83%	NT$962,786	NT$9.74	3,277	3.32%	NT$6,955,432	7.22x	NT$293.80	NT$6,871,966	NT$2,968,350	43.20%
Canada 加拿大	3,056,581	71,365	2.33%	NT$898,600	NT$12.59	2,549	3.57%	NT$5,409,780	6.02x	NT$352.53	NT$5,344,863	NT$1,436,298	26.87%
Australia 澳洲	2,401,599	54,896	2.29%	NT$770,229	NT$14.03	1,821	3.32%	NT$3,864,129	5.02x	NT$422.97	NT$3,817,759	NT$766,026	20.06%
Japan 日本	2,183,272	43,917	2.01%	NT$641,857	NT$14.62	1,456	3.32%	NT$3,477,716	5.42x	NT$440.84	NT$3,435,983	NT$670,272	19.51%
Singapore 新加坡	982,472	32,938	3.35%	NT$320,929	NT$9.74	1,365	4.14%	NT$2,511,684	7.83x	NT$235.11	NT$2,481,543	NT$1,340,545	54.02%
Malaysia 馬來西亞	764,145	16,469	2.15%	NT$128,372	NT$7.79	638	3.87%	NT$1,738,857	13.55x	NT$201.21	NT$1,717,992	NT$478,766	27.87%
合計	21,832,719	548,963	2.51%	NT$6,418,574	NT$11.69	18,206	3.32%	NT$38,641,287	6.02x	NT$352.55	NT$38,177,591	NT$9,575,321	25.08%

商品銷售成效

商品名稱	商品類型	參考單價帶	平均客單價 AOV	曝光量 IMP	點擊量	點擊率 CTR	廣告花費	平均點擊成本 CPC	成交訂單數	成交轉換率 CVR	商品交易總額 GMV	廣告投資報酬率 ROAS	單筆成交成本 CPA	淨利	扣除退款後營收	淨利率
智能香氛小夜燈	居家氛圍／生活小家電	NT$970－NT$1,870	NT$2,355.27	1,136,486	15,270	1.34%	NT$131,027	NT$8.58	294	1.93%	NT$692,448	5.28x	NT$445.67	NT$158,746	NT$686,862	23.11%
桌面空氣循環扇	辦公室／居家小家電	NT$1,040－NT$2,020	NT$2,293.00	601,580	14,981	2.49%	NT$88,934	NT$5.94	211	1.41%	NT$483,824	5.44x	NT$421.49	NT$152,968	NT$478,537	31.97%
智能空氣淨化器	居家健康／空氣清潔設備	NT$3,740－NT$7,240	NT$7,705.38	683,370	12,233	1.79%	NT$617,951	NT$50.52	450	3.68%	NT$3,467,421	5.61x	NT$1,373.22	NT$292,254	NT$3,431,151	8.52%
智能廚房秤	廚房用品／智能小工具	NT$520－NT$1,000	NT$1,508.21	835,404	22,112	2.65%	NT$64,504	NT$2.92	174	0.79%	NT$262,428	4.07x	NT$370.71	NT$43,770	NT$260,312	16.81%
便攜式保溫杯	生活用品／外出隨行	NT$590－NT$1,150	NT$1,491.90	933,579	17,587	1.88%	NT$121,064	NT$6.88	396	2.25%	NT$590,791	4.88x	NT$305.72	NT$100,559	NT$581,646	17.29%
多功能收納包	旅行／居家收納用品	NT$670－NT$1,290	NT$1,947.11	542,803	16,762	3.09%	NT$165,333	NT$9.86	314	1.87%	NT$611,391	3.70x	NT$526.54	NT$124,459	NT$607,682	20.48%
旅行壓縮袋組	旅行用品／行李收納	NT$820－NT$1,580	NT$1,910.19	670,725	24,703	3.68%	NT$76,247	NT$3.09	335	1.36%	NT$639,913	8.39x	NT$227.60	NT$394,165	NT$633,494	62.19%
磁吸式無線充電座	3C配件／桌面充電	NT$970－NT$1,870	NT$3,036.50	513,670	14,531	2.83%	NT$121,351	NT$8.35	381	2.62%	NT$1,156,907	9.53x	NT$318.51	NT$201,803	NT$1,147,843	17.58%
藍牙降噪耳機	3C配件／影音設備	NT$1,870－NT$3,610	NT$5,642.79	986,952	18,595	1.88%	NT$164,176	NT$8.83	189	1.02%	NT$1,066,488	6.50x	NT$868.66	NT$121,247	NT$1,046,846	11.58%
手機防水收納袋	戶外用品／手機配件	NT$290－NT$570	NT$951.73	1,050,219	23,716	2.26%	NT$81,363	NT$3.43	346	1.46%	NT$329,299	4.05x	NT$235.15	NT$95,572	NT$327,039	29.22%
摺疊式手機支架	3C配件／桌面用品	NT$340－NT$650	NT$1,091.01	653,782	19,043	2.91%	NT$57,515	NT$3.02	192	1.01%	NT$209,474	3.64x	NT$299.56	NT$73,382	NT$207,176	35.42%
LED補光化妝鏡	美妝工具／居家小物	NT$890－NT$1,730	NT$2,311.14	1,023,542	18,575	1.82%	NT$58,378	NT$3.14	182	0.98%	NT$420,627	7.20x	NT$320.76	NT$99,541	NT$415,931	23.93%
電動筋膜按摩器	健康放鬆／按摩設備	NT$2,240－NT$4,340	NT$6,355.42	1,099,761	25,848	2.35%	NT$237,886	NT$9.20	317	1.23%	NT$2,014,668	8.47x	NT$750.43	NT$162,090	NT$1,985,546	8.16%
頸掛式小風扇	夏季用品／個人小家電	NT$740－NT$1,440	NT$2,424.14	614,989	17,705	2.88%	NT$371,534	NT$20.99	542	3.06%	NT$1,313,884	3.54x	NT$685.49	NT$320,706	NT$1,299,083	24.69%
USB加熱暖手寶	冬季用品／生活小家電	NT$520－NT$1,000	NT$1,767.02	1,178,412	29,141	2.47%	NT$93,587	NT$3.21	254	0.87%	NT$448,824	4.80x	NT$368.45	NT$176,734	NT$443,979	39.81%
智能感應垃圾桶	居家用品／智能生活	NT$1,420－NT$2,740	NT$4,068.85	875,228	22,381	2.56%	NT$86,379	NT$3.86	234	1.05%	NT$952,111	11.02x	NT$369.14	NT$146,077	NT$939,877	15.54%
防滑浴室地墊	居家用品／浴室收納	NT$440－NT$860	NT$1,381.05	343,161	10,039	2.93%	NT$36,715	NT$3.66	395	3.93%	NT$545,515	14.86x	NT$92.95	NT$184,706	NT$540,937	34.15%
廚房瀝水置物架	廚房用品／收納整理	NT$890－NT$1,730	NT$2,961.18	1,040,356	17,902	1.72%	NT$213,733	NT$11.94	600	3.35%	NT$1,776,710	8.31x	NT$356.22	NT$731,947	NT$1,761,679	41.55%
矽膠保鮮袋組	廚房用品／環保收納	NT$370－NT$710	NT$1,328.23	798,265	16,470	2.06%	NT$38,143	NT$2.32	392	2.38%	NT$520,665	13.65x	NT$97.30	NT$120,624	NT$517,393	23.32%
不鏽鋼保鮮盒	廚房用品／食物收納	NT$670－NT$1,290	NT$2,105.68	554,528	19,243	3.47%	NT$238,011	NT$12.37	409	2.13%	NT$861,224	3.62x	NT$581.93	NT$289,712	NT$854,783	33.89%
可折疊購物袋	生活用品／外出收納	NT$290－NT$570	NT$955.57	504,834	13,899	2.75%	NT$98,583	NT$7.09	642	4.62%	NT$613,478	6.22x	NT$153.56	NT$182,420	NT$607,042	30.05%
旅行盥洗收納包	旅行用品／盥洗收納	NT$590－NT$1,150	NT$1,557.31	228,458	8,522	3.73%	NT$26,336	NT$3.09	219	2.57%	NT$341,051	12.95x	NT$120.26	NT$114,432	NT$338,521	33.80%
護照證件收納包	旅行用品／證件收納	NT$520－NT$1,000	NT$1,485.63	318,695	9,480	2.97%	NT$37,493	NT$3.95	490	5.17%	NT$727,957	19.42x	NT$76.52	NT$202,848	NT$718,195	28.25%
行李箱電子秤	旅行用品／行李配件	NT$440－NT$860	NT$1,274.56	286,822	8,544	2.98%	NT$115,074	NT$13.47	286	3.35%	NT$364,325	3.17x	NT$402.36	NT$129,403	NT$360,418	35.90%
車用手機支架	汽車用品／車內配件	NT$590－NT$1,150	NT$1,649.21	288,456	9,209	3.19%	NT$132,453	NT$14.38	522	5.67%	NT$861,889	6.51x	NT$253.74	NT$201,331	NT$854,518	23.56%
車用香氛擴香器	汽車用品／車內香氛	NT$740－NT$1,440	NT$2,230.37	798,444	15,256	1.91%	NT$99,613	NT$6.53	285	1.87%	NT$635,655	6.38x	NT$349.52	NT$133,340	NT$629,079	21.20%
車用吸塵器	汽車用品／清潔設備	NT$1,190－NT$2,310	NT$3,389.01	211,726	4,442	2.10%	NT$159,346	NT$35.87	485	10.92%	NT$1,643,669	10.32x	NT$328.55	NT$388,557	NT$1,620,526	23.98%
寵物飲水機	寵物用品／智能設備	NT$1,490－NT$2,890	NT$3,859.53	623,204	13,271	2.13%	NT$389,734	NT$29.37	269	2.03%	NT$1,038,214	2.66x	NT$1,448.83	NT$160,358	NT$1,030,366	15.56%
寵物除毛刷	寵物用品／清潔護理	NT$520－NT$1,000	NT$1,423.45	1,190,621	33,181	2.79%	NT$243,111	NT$7.33	761	2.29%	NT$1,083,648	4.46x	NT$319.46	NT$365,845	NT$1,073,653	34.07%
寵物外出水壺	寵物用品／外出用品	NT$490－NT$940	NT$1,306.02	453,413	9,470	2.09%	NT$40,253	NT$4.25	537	5.67%	NT$701,334	17.42x	NT$74.96	NT$204,405	NT$695,546	29.39%
瑜珈彈力帶組	運動用品／健身配件	NT$440－NT$860	NT$1,320.21	1,162,059	27,277	2.35%	NT$90,063	NT$3.30	774	2.84%	NT$1,021,844	11.34x	NT$116.36	NT$252,959	NT$1,009,871	25.05%
防滑瑜珈墊	運動用品／居家健身	NT$1,270－NT$2,450	NT$2,979.32	573,076	12,670	2.21%	NT$285,217	NT$22.51	675	5.33%	NT$2,011,044	7.05x	NT$422.54	NT$731,757	NT$1,987,779	36.81%
運動水壺	運動用品／外出補水	NT$520－NT$1,000	NT$1,536.97	796,764	16,325	2.05%	NT$202,897	NT$12.43	449	2.75%	NT$690,100	3.40x	NT$451.89	NT$170,024	NT$680,706	24.98%
快乾運動毛巾	運動用品／戶外用品	NT$370－NT$710	NT$1,048.67	396,290	10,085	2.54%	NT$200,711	NT$19.90	225	2.23%	NT$235,950	1.18x	NT$892.05	NT$48,054	NT$232,899	20.63%
露營LED掛燈	戶外用品／露營照明	NT$740－NT$1,440	NT$2,640.88	446,595	16,723	3.74%	NT$241,024	NT$14.41	721	4.31%	NT$1,903,673	7.90x	NT$334.29	NT$598,345	NT$1,879,458	31.84%
戶外折疊椅	戶外用品／露營家具	NT$1,790－NT$3,470	NT$5,842.53	898,681	30,346	3.38%	NT$348,008	NT$11.47	884	2.91%	NT$5,164,394	14.84x	NT$393.67	NT$1,663,004	NT$5,107,815	32.56%
便攜餐具組	戶外用品／旅行餐具	NT$370－NT$710	NT$1,086.51	452,417	8,733	1.93%	NT$119,105	NT$13.64	389	4.45%	NT$422,652	3.55x	NT$306.18	NT$88,236	NT$416,881	21.17%
防水收納乾濕袋	旅行用品／戶外收納	NT$440－NT$860	NT$1,316.52	364,880	13,307	3.65%	NT$128,420	NT$9.65	261	1.96%	NT$343,411	2.67x	NT$492.03	NT$96,541	NT$339,026	28.48%
兒童防漏水杯	親子用品／兒童餐具	NT$520－NT$1,000	NT$1,357.72	437,143	12,057	2.76%	NT$161,606	NT$13.40	394	3.27%	NT$534,943	3.31x	NT$410.17	NT$138,787	NT$527,926	26.29%
兒童矽膠圍兜	親子用品／用餐用品	NT$370－NT$710	NT$1,169.19	281,693	8,023	2.85%	NT$97,257	NT$12.12	434	5.41%	NT$507,828	5.22x	NT$224.09	NT$83,294	NT$500,368	16.65%
嬰兒推車收納袋	親子用品／外出收納	NT$670－NT$1,290	NT$1,926.28	887,680	17,710	2.00%	NT$227,089	NT$12.82	328	1.85%	NT$631,821	2.78x	NT$692.34	NT$174,275	NT$625,571	27.86%
居家防撞條組	親子用品／安全防護	NT$370－NT$710	NT$1,220.40	335,077	9,664	2.88%	NT$43,697	NT$4.52	574	5.94%	NT$700,509	16.03x	NT$76.13	NT$156,039	NT$691,488	22.57%
收納抽屜分隔板	居家收納／衣櫃整理	NT$520－NT$1,000	NT$1,648.96	729,798	21,216	2.91%	NT$149,952	NT$7.07	309	1.46%	NT$509,529	3.40x	NT$485.28	NT$111,056	NT$503,457	22.06%
真空壓縮收納袋	居家收納／換季整理	NT$590－NT$1,150	NT$1,632.53	1,119,432	24,071	2.15%	NT$254,669	NT$10.58	530	2.20%	NT$865,239	3.40x	NT$480.51	NT$293,642	NT$854,839	34.35%
衣物除毛球機	居家用品／衣物護理	NT$670－NT$1,290	NT$2,188.33	693,113	24,726	3.57%	NT$290,601	NT$11.75	758	3.07%	NT$1,658,151	5.71x	NT$383.38	NT$648,539	NT$1,642,511	39.48%
迷你熨燙機	居家用品／衣物整理	NT$1,190－NT$2,310	NT$3,061.92	1,198,386	30,697	2.56%	NT$463,002	NT$15.08	300	0.98%	NT$918,577	1.98x	NT$1,543.34	NT$210,568	NT$907,527	23.20%
防藍光眼鏡	健康用品／護眼配件	NT$590－NT$1,150	NT$1,984.03	825,432	19,550	2.37%	NT$124,195	NT$6.35	407	2.08%	NT$807,501	6.50x	NT$305.15	NT$149,439	NT$795,481	18.79%
睡眠遮光眼罩	生活用品／睡眠配件	NT$440－NT$860	NT$1,271.72	577,324	18,232	3.16%	NT$200,863	NT$11.02	438	2.40%	NT$557,015	2.77x	NT$458.59	NT$122,456	NT$550,585	22.24%
人體工學滑鼠墊	辦公用品／桌面配件	NT$520－NT$1,000	NT$1,526.85	1,254,401	34,741	2.77%	NT$220,049	NT$6.33	410	1.18%	NT$625,978	2.84x	NT$536.70	NT$198,545	NT$616,508	32.20%
桌面理線收納盒	辦公用品／桌面收納	NT$370－NT$710	NT$771.54	833,900	18,273	2.19%	NT$177,289	NT$9.70	227	1.24%	NT$175,140	0.99x	NT$780.99	NT$39,163	NT$172,485	22.70%
合計				21,832,719	548,963	2.51%	NT$6,418,574	NT$11.69	18,206	3.32%	NT$38,641,287	6.02x	NT$352.55	NT$9,575,321	NT$38,177,591	25.08%

廣告素材成效

廣告素材	素材類型	曝光量 IMP	點擊量	點擊率 CTR	廣告花費	平均點擊成本 CPC	成交訂單數	成交轉換率 CVR	商品交易總額 GMV	廣告投資報酬率 ROAS	單筆成交成本 CPA	扣除退款後營收	淨利	淨利率
短影音A｜高單價家電開箱	15秒短影音	5,458,180	109,793	2.01%	NT$1,476,272	NT$13.45	3,277	2.98%	NT$8,114,670	5.50x	NT$450.50	NT$8,017,294	NT$957,532	11.94%
短影音B｜旅行收納前後對比	20秒短影音	4,366,544	126,262	2.89%	NT$962,786	NT$7.62	4,369	3.46%	NT$8,501,083	8.83x	NT$220.37	NT$8,399,070	NT$3,159,856	37.62%
短影音C｜辦公桌面改造	18秒短影音	3,056,581	76,855	2.51%	NT$898,600	NT$11.69	2,549	3.32%	NT$5,409,780	6.02x	NT$352.53	NT$5,344,863	NT$1,819,311	34.04%
短影音D｜寵物日常實測	25秒短影音	2,838,253	65,876	2.32%	NT$1,283,715	NT$19.49	2,367	3.59%	NT$5,796,193	4.51x	NT$542.34	NT$5,726,639	NT$1,148, -	
輪播圖E｜低單價爆品合集	圖文輪播	3,493,235	126,262	3.61%	NT$898,600	NT$7.12	4,187	3.32%	NT$6,182,606	6.88x	NT$214.60	NT$6,108,415	NT$2,106,571	34.49%
再行銷F｜購物車限時優惠	再行銷素材	2,619,926	43,915	1.68%	NT$898,601	NT$20.46	1,457	3.32%	NT$4,637, -	5.16x	NT$616.75	NT$4,581,310	NT$383, -	
合計	21,832,719	548,963	2.51%	NT$6,418,574	NT$11.69	18,206	3.32%	NT$38,641,287	6.02x	NT$352.55	NT$38,177,591	NT$9,575,321	25.08%	

裝置來源成效

裝置來源	曝光量 IMP	點擊量	點擊率 CTR	廣告花費	平均點擊成本 CPC	成交訂單數	成交轉換率 CVR	商品交易總額 GMV	廣告投資報酬率 ROAS	單筆成交成本 CPA	扣除退款後營收	淨利	淨利率
Mobile App / 行動裝置	15,938,885	406,233	2.55%	NT$4,493,002	NT$11.06	13,108	3.23%	NT$27,821,727	6.19x	NT$342.77	NT$27,487,866	NT$5,553,686	20.20%
Desktop Web / 桌機網頁	3,711,562	93,324	2.51%	NT$1,155,343	NT$12.38	3,277	3.51%	NT$6,955,432	6.02x	NT$352.56	NT$6,871,966	NT$1,723,558	25.08%
Tablet / 平板	1,309,963	32,938	2.51%	NT$513,486	NT$15.59	1,092	3.32%	NT$2,318,477	4.52x	NT$470.23	NT$2,290,655	NT$1,340,545	58.52%
In-App Webview / 內嵌瀏覽器	873,309	16,468	1.89%	NT$256,743	NT$15.59	729	4.43%	NT$1,545,651	6.02x	NT$352.19	NT$1,527,104	NT$957,532	62.70%
合計	21,832,719	548,963	2.51%	NT$6,418,574	NT$11.69	18,206	3.32%	NT$38,641,287	6.02x	NT$352.55	NT$38,177,591	NT$9,575,321	25.08%

受眾年齡成效

年齡層	曝光量 IMP	點擊量	點擊率 CTR	廣告花費	平均點擊成本 CPC	成交訂單數	成交轉換率 CVR	商品交易總額 GMV	廣告投資報酬率 ROAS	單筆成交成本 CPA	扣除退款後營收	淨利	淨利率
18-24	3,929,889	98,814	2.51%	NT$1,155,343	NT$11.69	2,913	2.95%	NT$6,182,606	5.35x	NT$396.62	NT$6,108,414	NT$1,340,545	21.95%
25-34	8,514,760	219,585	2.58%	NT$2,567,430	NT$11.69	7,646	3.48%	NT$15,842,928	6.17x	NT$335.79	NT$15,652,812	NT$3,638,622	23.25%
35-44	5,894,834	142,731	2.42%	NT$1,668,829	NT$11.69	4,551	3.19%	NT$9,660,322	5.79x	NT$366.70	NT$9,544,398	NT$1,915,064	20.07%
45-54	2,401,599	60,386	2.51%	NT$706,043	NT$11.69	2,185	3.62%	NT$4,636,954	6.57x	NT$323.13	NT$4,581,311	NT$957,532	20.90%
55+	1,091,637	27,447	2.51%	NT$320,929	NT$11.69	911	3.32%	NT$2,318,477	7.22x	NT$352.28	NT$2,290,656	NT$1,723,558	75.24%
合計	21,832,719	548,963	2.51%	NT$6,418,574	NT$11.69	18,206	3.32%	NT$38,641,287	6.02x	NT$352.55	NT$38,177,591	NT$9,575,321	25.08%

受眾性別成效

性別	曝光量 IMP	點擊量	點擊率 CTR	廣告花費	平均點擊成本 CPC	成交訂單數	成交轉換率 CVR	商品交易總額 GMV	廣告投資報酬率 ROAS	單筆成交成本 CPA	扣除退款後營收	淨利	淨利率
女性	13,536,286	345,847	2.55%	NT$3,851,144	NT$11.14	11,288	3.26%	NT$23,571,185	6.12x	NT$341.17	NT$23,288,331	NT$5,553,686	23.85%
男性	6,986,470	175,668	2.51%	NT$2,182,315	NT$12.42	6,008	3.42%	NT$13,138,038	6.02x	NT$363.24	NT$12,980,381	NT$3,064,103	23.61%
未揭露／其他	1,309,963	27,448	2.10%	NT$385,115	NT$14.03	910	3.32%	NT$1,932,064	5.02x	NT$423.20	NT$1,908,879	NT$957,532	50.16%
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
2026/06/05	NT$5,409,816	NT$64,825	NT$5,344,991	NT$1,761,544	NT$424,075	NT$130,485	NT$179,417	NT$114,174	NT$114,174	NT$538,249	NT$897,453	NT$1,185,420	22.18%
2026/06/06	NT$4,312,785	NT$51,215	NT$4,261,570	NT$1,344,788	NT$329,336	NT$137,223	NT$170,157	NT$112,523	NT$74,101	NT$576,338	NT$822,719	NT$694,385	16.29%
2026/06/07	NT$6,721,394	NT$87,214	NT$6,634,180	NT$2,067,048	NT$525,828	NT$155,935	NT$181,320	NT$108,792	NT$181,320	NT$406,157	NT$1,081,662	NT$1,926,118	29.03%
2026/06/08	NT$4,858,607	NT$57,269	NT$4,801,338	NT$1,522,420	NT$322,821	NT$137,927	NT$176,294	NT$132,220	NT$93,668	NT$542,909	NT$865,388	NT$1,008,219	21.00%
2026/06/09	NT$7,438,126	NT$92,681	NT$7,345,445	NT$1,851,539	NT$472,733	NT$149,032	NT$259,109	NT$157,036	NT$86,370	NT$960,625	NT$967,251	NT$2,438,750	33.20%
2026/06/10	NT$3,952,481	NT$45,912	NT$3,906,569	NT$1,472,354	NT$387,907	NT$105,136	NT$122,658	NT$95,020	NT$112,552	NT$202,828	NT$812,940	NT$598,114	15.31%
2026/06/11	NT$5,948,078	NT$64,580	NT$5,883,498	NT$1,593,013	NT$430,114	NT$175,231	NT$184,790	NT$140,883	NT$108,456	NT$556,042	NT$971,161	NT$1,724,315	29.31%
7天合計	NT$38,641,287	NT$463,696	NT$38,177,591	NT$11,613,704	NT$2,891,211	NT$991,098	NT$1,273,746	NT$859,917	NT$770,641	NT$3,783,379	NT$6,418,574	NT$9,575,321	25.08%"""

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
