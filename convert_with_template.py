import pandas as pd

# --- 파일 경로 설정 ---
input_file = "상품제안서.xlsx"  # 상품제안서 파일
template_file = "상품일괄등록양식.xlsx"                       # 일괄상품등록양식 파일(템플릿)
output_file = "일괄상품등록 결과.xlsx"                             # 변환 결과 파일

# --- 데이터 읽기 ---
# 상품제안서 파일 읽기
df_input = pd.read_excel(input_file)

# 템플릿 파일 읽어서 컬럼 순서(헤더)를 가져옴
df_template = pd.read_excel(template_file)
template_columns = df_template.columns.tolist()

# --- 출력 데이터프레임 생성 ---
# 템플릿 파일의 컬럼 순서를 그대로 사용하여 빈 데이터프레임 생성
df_output = pd.DataFrame(columns=template_columns)

# --- 데이터 매핑 (템플릿의 컬럼명이 아래와 같다고 가정) ---
# 만약 템플릿의 컬럼명이 실제와 다르다면, 아래 키값을 템플릿에 맞게 수정하세요.
# 예시에서는 "상품명 (item_name)"이라는 컬럼명이 템플릿에 있다고 가정합니다.

df_output["스토어번호"] = ""  # 빈 값

# 상품제안서의 "상품명" 열을 템플릿의 "상품명 (item_name)" 열에 복사
df_output["상품명(item_name)"] = df_input["상품명"]
df_output["원래가격(original_price)"] = df_input["소비자가"]
df_output["옵션값(option_value)"] = df_input["구성(옵션)"]
df_output["마감할인/마켓 구분(delivery_type)"] = "s"
df_output["상품구분(goods_type)"] = "D"
df_output["성인용 상품여부(is_adult)"] = "N"

# "면/과세" 열의 값에 따라 과세여부(is_tax) 결정: "과세" -> "Y", "면세" -> "N"
df_output["과세여부(is_tax)"] = df_input["면/과세"].apply(lambda x: "Y" if x == "과세" else ("N" if x == "면세" else x))

df_output["매입가격(offer_price)"] = df_input["공급가"]

# 공급가 결측값 처리 후 115% 계산하여 정수형으로 변환
df_output["판매가격(price)"] = (df_input["공급가"].fillna(0) * 1.15).round().astype(int)

df_output["구성수량(bundle_qty)"] = 1
df_output["판매수량(qty)"] = df_input["재고수량"]
df_output["주문당 최소 주문수량(min_sell)"] = 1
df_output["주문당 최대 주문수량(max_sell)"] = 10

df_output["소개내용(description)"] = df_input["배송마감시간"]

# 템플릿에 존재하지만 변환에 사용하지 않은 나머지 컬럼은 그대로 두거나 추가 처리가 가능함.
# (필요시 추가 매핑 작업을 진행하세요.)

# --- 결과 저장 ---
df_output.to_excel(output_file, index=False)
print(f"변환 완료! 생성된 파일: {output_file}")
