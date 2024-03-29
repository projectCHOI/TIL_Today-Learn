import os
import pandas as pd
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt

# streamlit 페이지 생성
st.set_page_config(
    page_title='Bugok Class Dashboard',		# 브라우저 탭 제목
    page_icon = ":bar_chart:",				# 브라우저 파비콘
    layout = "wide"							# 레이아웃
    )

# 폴더내에 
def read_xlsx_files():
    path = "./data"
    file_list = os.listdir(path)
    lst_xlsx = [file for file in file_list if file.endswith(".xlsx")]
    file_names = [lst.split('_')[2].split('.')[0] for lst in lst_xlsx]
    lst_xlsx = sorted(lst_xlsx)
    file_names = sorted(file_names)
    return file_names, lst_xlsx

# 데이터 파일의 시트 불러오기
def get_excelfile(p_file, p_sheet_name):
    df = pd.read_excel(
		io = f'./data/{p_file}',
		engine="openpyxl",
		sheet_name=f"{p_sheet_name}",)
    return df

file_names, lst_xlsx = read_xlsx_files()
lst_xlsx.sort()
default_ix = lst_xlsx[-1]

# 데이터 프레임 카운트 하기
def count_df(lst_xlsx, p_sheet_name):
    lst_date = []
    lst_count = []
    for i in lst_xlsx:
        df = get_excelfile(i, p_sheet_name)
        str_date = i.split('_')[-1].split('.')[0].split('-')[0]
        str_now = f'{str_date[:4]}.{str_date[4:6]}.{str_date[6:]}'
        lst_date.append(str_now)
        lst_count.append(len(df))
    return {'날짜':lst_date, '건(개)':lst_count}

# --- 사이드바 생성하기 ---
st.sidebar.header("Please Filter Here:")	# 사이드바 헤더(제목)
# 파일 선택하기 
file_xlsx = st.sidebar.selectbox(
	"Select data file:",
	lst_xlsx,
	index=lst_xlsx.index(default_ix)  # 마지막 값 선택
)

# 날짜 데이터 가져오기
str_date = file_xlsx.split('_')[-1].split('.')[0].split('-')[0]
str_now = f'{str_date[:4]}.{str_date[4:6]}.{str_date[6:]}'

# 데이터 프레임 만들기 
df = get_excelfile(file_xlsx,'전체명부')    # 전체명부
df_type = get_excelfile(file_xlsx,'전보유형_지역별인원').ffill()	# 전보유형 지역별 인원
df_error_type = get_excelfile(file_xlsx,'유형에러').ffill()	# 유형별 에러
df_error_score = get_excelfile(file_xlsx,'점수에러').ffill()	# 유형별 에러
df_type_sex = get_excelfile(file_xlsx,'전보유형_성별').ffill()	# 전보유형 성별 
df_same_name_first = get_excelfile(file_xlsx,'동명이인_지역_1희망')	# 동명이인 같은지역 1희망 지역
df_same_name_region = get_excelfile(file_xlsx,'동명이인_지역_소속')	# 동명이인 같은 학교
df_region_card = get_excelfile(file_xlsx,'지역 Top10')	# 내신제출 지역 top10
df_spc_treat = get_excelfile(file_xlsx,'우대사항 Top10').ffill()	# 우대 사항 Top10

# --- 메인 페이지 ---
# --- 메인 페이지 ---
st.write(f"### {str_now} 현재")
st.title(":bar_chart: 인사작업 현황판")

gr_type = df_type.groupby(['지역','코드_유형']).agg({0:'sum'}).reset_index()
gr_type.columns = ['지역', '전보유형', '인원']

# 화면 타이틀

# 상단 현황판
gr_sum_type = df_type.groupby('코드_유형').sum().reset_index()
sum_gap = gr_sum_type.loc[0][0]
sum_gen = gr_sum_type.loc[1][0]
sum_spc = gr_sum_type.loc[2][0]
sum_total = sum_gap + sum_gen + sum_spc

col_14, col_24, col_34, col_44 = st.columns(4)
with col_14:
    st.subheader(f"일반전보 : {sum_gen}명")
with col_24:
    st.subheader(f"특만기: {sum_spc}명")
with col_34:
    st.subheader(f"갑만기: {sum_gap}명")
with col_44:
    st.subheader(f"전체인원: {sum_total}명")


# 화면분활 01 - 유형별 전보인원
st.title("★ 오류인원 통계")
result = count_df(lst_xlsx,'점수에러')
fig = px.line(result, x='날짜', y='건(개)',title="점수에러 변화 추이")
st.plotly_chart(fig)

# 화면 분할 02
st.title("★ 유형별 전보인원")

# 칼럼 나누기 2개
a_col_12, a_col_22 = st.columns(2)

with a_col_12:
    # st.subheader("전보유형 전체 시각화")
    result = df_type.groupby(['코드_유형']).sum().reset_index()
    result.columns = ['전보유형', '인원']
    fig = px.bar(result, 
        x='전보유형', 
        y='인원',
        title="전보유형별 인원",
        color='전보유형',
        text_auto=True   #그래프에 수치 나타내기
        )
    fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})  # 값 정렬
    st.plotly_chart(fig, use_container_width=True)

with a_col_22:
    # Pie 그래프로 나타내기
    fig = px.pie(result, values='인원', names='전보유형')
    st.plotly_chart(fig, use_container_width=True)


# 칼럼 2개로 나누기 
b_col_12, b_col_22 = st.columns(2)
with b_col_12:
    # st.subheader("특만기-일반-갑만기 통합 지역별 통계")
    # gr_type.columns = ['지역', '전보유형', '인원']
    fig1 = px.bar(gr_type, 
        x='지역', 
        y='인원',
        title="전보유형별 제출 현황",
        color='전보유형',
        text_auto=True   #그래프에 수치 나타내기
        )
    fig1.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})  # 값 정렬
    st.plotly_chart(fig1, use_container_width=True)

with b_col_22:
    # st.subheader("일반 지역별 통계")
    df_gen = gr_type.query('전보유형.str.contains("일반")')  # 전보유형중 '일반' 추출
    fig_gen = px.bar(df_gen, x='지역', y='인원', color='지역', title='일반내신 제출 현황')
    fig_gen.update_layout(barmode='stack',xaxis={'categoryorder':'total descending'})  # 값 정렬
    st.plotly_chart(fig_gen, use_container_width=True)


# ----- 칼럼 나누기 3개 
c_col_12, c_col_22 = st.columns(2)

with c_col_12:
    # st.subheader("특만기 지역별 통계")
    df_spc = gr_type.query('전보유형.str.contains("특만기")')  # 전보유형중 '일반' 추출
    fig_spc = px.bar(df_spc, x='지역', y='인원', color='지역', title='특만기 내신 제출 현황')
    fig_spc.update_layout(barmode='stack',xaxis={'categoryorder':'total descending'})  # 값 정렬
    st.plotly_chart(fig_spc, use_container_width=True)


with c_col_22:
    # st.subheader("갑만기 지역별 통계")
    df_gap = gr_type.query('전보유형.str.contains("갑만기")')  # 전보유형중 '일반' 추출
    fig_gap = px.bar(df_gap, x='지역', y='인원', color='지역', title='갑만기 제출 현황')
    fig_gap.update_layout(barmode='stack',xaxis={'categoryorder':'total descending'})  # 값 정렬
    st.plotly_chart(fig_gap, use_container_width=True)

# 화면 분할 03
st.subheader("★ 각종 통계")

st.write(result)