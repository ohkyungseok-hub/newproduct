import pandas as pd
import pandas as pd

input_file = "상품제안서.xlsx"
df = pd.read_excel(input_file)
print(df.columns)

# 입력 파일 (업로드하신 상품제안서 파일)
input_file = "상품제안서.xlsx"
df = pd.read_excel(input_file)

# 출력 데이터프레임 생성 (일괄상품등록파일 양식)
df_output = pd.DataFrame()

df_output["스토어번호"] = ""                           # 빈 값
df_output["상품명(item_name)"] = df["상품명"]                      # 상품제안서의 상품명 칸 복사
df_output["delivery_type"] = "s"                       # 모든 행 s
df_output["goods_type"] = "D"                          # 모든 행 D
df_output["is_adult"] = "N"                            # 모든 행 N

# 과세여부: 면/과세 칸의 값이 "과세"이면 Y, "면세"이면 N (그 외 값은 그대로)
df_output["is_tax"] = df["면/과세"].apply(lambda x: "Y" if x == "과세" else ("N" if x == "면세" else x))

df_output["offer_price"] = df["공급가"]                # 공급가 그대로 사용
df_output["price"] = (df["공급가"] * 1.15).round().astype("Int64")
  # 판매가격 = 매입가격 * 1.15 (정수형)


df_output["bundle_qty"] = 1                           # 1로 통일
df_output["qty"] = 1000                               # 1000으로 통일
df_output["min_sell"] = 1                             # 1로 통일
df_output["max_sell"] = 10                            # 10으로 통일
df_output["description"] = df["배송마감시간"]           # 배송마감시간 칸 복사

# 출력 파일 저장
output_file = "상품일괄등록양식 결과.xlsx"
df_output.to_excel(output_file, index=False)

print(f"변환 완료! 생성된 파일: {output_file}")
