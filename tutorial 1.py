import streamlit as st
import pandas as pd
import requests
import io

# GitHub 링크에서 엑셀 파일 읽어오기
@st.cache_data
def load_data():
    github_url = 'https://github.com/smartky23/Dummy/blob/main/data_1117_20250917.xlsx?raw=true'
    try:
        response = requests.get(github_url)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        excel_file = io.BytesIO(response.content)
        df = pd.read_excel(excel_file, engine='openpyxl')
        return df
    except requests.exceptions.RequestException as e:
        st.error(f"GitHub에서 파일을 다운로드하는 중 오류가 발생했습니다: {e}")
        return None
    except Exception as e:
        st.error(f"엑셀 파일을 읽는 중 오류가 발생했습니다: {e}")
        return None

df = load_data()

if df is not None:
    st.title('주식 정보 검색 앱')

    query = st.text_input("종목명 또는 종목코드를 입력하세요:")

    if query:
        # 종목코드로 검색
        result = df[df['종목코드'].astype(str) == query]
        if not result.empty:
            st.write(f"종목코드 {query}의 종목명은: {result['종목명'].iloc[0]} 입니다.")
        else:
            # 종목명으로 검색
            result = df[df['종목명'].str.contains(query, na=False)]
            if not result.empty:
                st.write(f"종목명 '{query}'에 해당하는 종목코드는: {result['종목코드'].iloc[0]} 입니다.")
            else:
                st.write("해당하는 정보를 찾을 수 없습니다.")
