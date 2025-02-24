import pandas as pd
import streamlit as st

# Streamlit 앱 설정
st.title("📂 엑셀 파일 변환기 - 오경석매직")

# 파일 업로드 버튼
uploaded_file = st.file_uploader("상품제안서 엑셀 파일을 업로드하세요", type=["xlsx"])
template_file = "상품일괄등록양식.xlsx"                       # 일괄상품등록양식 파일(템플릿)
if uploaded_file is not None:
    # 상품제안서 데이터 읽기
    df_input = pd.read_excel(uploaded_file)
    
    ]
    # 템플릿 파일 읽어서 컬럼 순서(헤더)를 가져옴
df_template = pd.read_excel(template_file)
template_columns = df_template.columns.tolist()
    # 빈 데이터프레임 생성
    df_output = pd.DataFrame(columns=template_columns)
    
    # 데이터 매핑
    df_output["스토어번호"] = ""  # 빈 값
    df_output["상품명(item_name)"] = df_input["상품명"]
    df_output["원래가격(original_price)"] = df_input["소비자가"]
    df_output["옵션값(option_value)"] = df_input["구성(옵션)"]
    df_output["마감할인/마켓 구분(delivery_type)"] = "s"
    df_output["상품구분(goods_type)"] = "D"
    df_output["성인용 상품여부(is_adult)"] = "N"
    
    # "면/과세" 열의 값에 따라 과세여부 결정
    df_output["과세여부(is_tax)"] = df_input["면/과세"].apply(lambda x: "Y" if x == "과세" else ("N" if x == "면세" else x))
    
    df_output["매입가격(offer_price)"] = df_input["공급가"]
    df_output["판매가격(price)"] = (df_input["공급가"].fillna(0) * 1.15).round().astype(int)
    df_output["구성수량(bundle_qty)"] = 1
    df_output["판매수량(qty)"] = df_input["재고수량"]
    df_output["주문당 최소 주문수량(min_sell)"] = 1
    df_output["주문당 최대 주문수량(max_sell)"] = 10
    df_output["소개내용(description)"] = df_input["배송마감시간"]
    
    # 변환된 데이터 미리보기
    st.write("### 변환된 데이터 미리보기")
    st.dataframe(df_output)
    
    # 변환된 엑셀 파일 다운로드
    output_file = "일괄상품등록_결과.xlsx"
    df_output.to_excel(output_file, index=False)
    st.download_button(label="📥 변환된 파일 다운로드", data=open(output_file, "rb"), file_name=output_file, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
