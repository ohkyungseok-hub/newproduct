import pandas as pd
import streamlit as st

# Streamlit 앱 설정
st.title("📂 엑셀 파일 변환기 - 상품 일괄 등록 양식")

# 파일 업로드 버튼
uploaded_file = st.file_uploader("상품제안서 엑셀 파일을 업로드하세요", type=["xlsx"])
template_file = "상품일괄등록양식.xlsx"  # 템플릿 파일

if uploaded_file is not None:
    # 상품제안서 데이터 읽기
    df_input = pd.read_excel(uploaded_file)
# 파일 읽은 직후에 컬럼명 정리
    df_input.columns = df_input.columns.str.strip().str.replace("\n", "") 

    # 템플릿 파일 읽어서 컬럼 순서(헤더)를 가져옴
try:
        df_template = pd.read_excel(template_file)
        template_columns = df_template.columns.tolist()
except FileNotFoundError:
        st.error("❌ 템플릿 파일을 찾을 수 없습니다. '상품일괄등록양식.xlsx' 파일이 존재하는지 확인하세요.")
        st.stop()

    # 빈 데이터프레임 생성
df_output = pd.DataFrame(columns=template_columns)

    # 데이터 매핑
df_output["스토어번호"] = ""  # 빈 값
df_output["상품명(item_name)"] = df_input["상품명"]
df_output["원래가격(original_price)"] = df_input["소비자가"]
df_output["옵션값(option_value)"] = df_input["구성(옵션)"]

 
# 옵션값 및 옵션가격, 옵션 구성수량, 옵션 수량 처리 함수
def process_option(opt):
    if pd.isna(opt) or str(opt).strip() == "":
        # 옵션값이 없으면 모두 빈 문자열 처리
        return "", "", "", ""
    # 옵션명이 있는 경우, 입력된 옵션명을 쉼표로 분리한 후 그대로 사용
    options = [x.strip() for x in str(opt).split(",") if x.strip() != ""]
    option_value = ",".join(options)
    # 옵션가격, 옵션 구성수량, 옵션 수량은 옵션값의 수만큼 0원을 쉼표로 구분하여 생성
    option_price = ",".join(["0"] * len(options))
    option_bundle_qty = ",".join(["0"] * len(options))
    option_qty = ",".join(["0"] * len(options))
    return option_value, option_price, option_bundle_qty, option_qty

# "구성(옵션)" 컬럼을 처리하여 옵션값과 옵션가격, 옵션 구성수량, 옵션 수량 생성
option_results = df_input["구성(옵션)"].apply(process_option)
df_output["옵션값(option_value)"] = option_results.apply(lambda x: x[0])
df_output["옵션 가격(option_price)"] = option_results.apply(lambda x: x[1])
df_output["옵션 구성수량(option_bundle_qty)"] = option_results.apply(lambda x: x[2])
df_output["옵션 수량(option_qty)"] = option_results.apply(lambda x: x[3])

# 옵션값이 있는 경우 옵션명(option_group_title)은 무조건 "선택"으로 표기
df_output["옵션명(option_group_title)"] = df_output["옵션값(option_value)"].apply(lambda x: "선택" if x != "" else "")


df_output["마감할인/마켓 구분(delivery_type)"] = "S"
df_output["상품구분(goods_type)"] = "D"
df_output["성인용 상품여부(is_adult)"] = "N"
df_output["태그(tags)"] = "최저가보장"
df_input.columns = df_input.columns.str.strip()  # 앞뒤 공백 제거
df_input.columns = df_input.columns.str.replace("\n", "")  # 줄바꿈 문자 제거

    # "면/과세" 열의 값에 따라 과세여부 결정
df_output["과세여부(is_tax)"] = df_input["면/과세"].apply(lambda x: "Y" if x == "과세" else ("N" if x == "면세" else x))

df_output["매입가격(offer_price)"] = df_input["공급가"]
df_output["판매가격(price)"] = (df_input["공급가"].fillna(0) * 1.15).round().astype(int)
df_output["구성수량(bundle_qty)"] = 1
df_output["판매수량(qty)"] = df_input["재고수량"]
df_output["주문당 최소 주문수량(min_sell)"] = 1
df_output["주문당 최대 주문수량(max_sell)"] = 10
df_output["소개내용(description)"] = df_input["유통기한"]

    # 변환된 데이터 미리보기
st.write("### 변환된 데이터 미리보기")
st.dataframe(df_output)

    # 변환된 엑셀 파일 다운로드
output_file = "일괄상품등록_결과.xlsx"
df_output.to_excel(output_file, index=False)

    # 안전한 파일 다운로드 처리
with open(output_file, "rb") as f:
        st.download_button(
            label="📥 변환된 파일 다운로드",
            data=f,
            file_name=output_file,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )