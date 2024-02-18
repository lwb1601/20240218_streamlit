import streamlit as st
import requests
import pandas as pd

def get_btc_price():
    """비트코인 가격을 가져오는 함수"""
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice/BTC.json')
    data = response.json()
    btc_price = data['bpi']['USD']['rate_float']
    return int(btc_price)

def calculate_final_debt_increase_and_daily_investment(current_assets_btc, existing_debt_btc, target_ltv, target_period):
    """목표 LTV를 달성하기 위한 최종 부채 증가량 및 일일 투자금액 계산 함수"""
    k = (target_ltv * current_assets_btc - existing_debt_btc) / (1 - target_ltv)
    final_debt_increase_btc = k
    daily_investment_btc = final_debt_increase_btc / target_period
    return final_debt_increase_btc, daily_investment_btc

def simulate_asset_changes(current_assets_btc, existing_debt_btc, daily_investment_btc, target_period, btc_price):
    """자산 변화 시뮬레이션 함수"""
    data = []
    for day in range(target_period + 1):
        if day > 0:
            current_assets_btc += daily_investment_btc
            existing_debt_btc += daily_investment_btc
        ltv = existing_debt_btc / current_assets_btc if current_assets_btc else 0
        data.append([day, current_assets_btc, existing_debt_btc, ltv])
    df = pd.DataFrame(data, columns=['Day', 'Total Assets (BTC)', 'Debt (BTC)', 'LTV'])
    return df

def app():
    btc_price = get_btc_price()
  


    st.header(':red[레버리지] 일일 투자금액(BTC) 계산기 :sunglasses:', divider='rainbow')
    st.subheader(f"현재 비트코인 가격 = :blue[{btc_price}] USDT")
    st.caption('특정 LTV까지 레버리지를 분할로 사용하고 싶을 때 일일 투자금액을 계산해주는 프로그램입니다. 이 프로그램에서 제공하는 데이터는 실제 데이터와 차이가 있을 수 있으니 대략적인 투자 금액을 파악하기 위한 용도로 사용하세요. ')
    current_assets_btc = st.number_input('현재 총 자산 (BTC)', value=0.5)
    existing_debt_btc = st.number_input('현재 총 부채 (BTC)', value=0.2)
    target_ltv = st.number_input('목표 LTV', value=0.6, min_value=0.01, max_value=1.0, step=0.01)
    target_period = st.number_input('분할 매수 기간 (일)', value=30, min_value=1)

    existing_debt_usd = existing_debt_btc * btc_price
    ltv50price = int(existing_debt_usd *2 / current_assets_btc)
    #ltv50price_percent = (btc_price - ltv50price) / btc_price  


    if st.button('레버리지 일일 투자금액 계산 및 자산 변화 시뮬레이션'):
        
        st.divider()
        
        final_debt_increase_btc, daily_investment_btc = calculate_final_debt_increase_and_daily_investment(
            current_assets_btc, existing_debt_btc, target_ltv, target_period)
        df = simulate_asset_changes(current_assets_btc, existing_debt_btc, daily_investment_btc, target_period, btc_price)
        st.subheader(f'일일 투자금액 : :blue[{round(daily_investment_btc, 5)} BTC] (:blue[{int(daily_investment_btc * btc_price)} USDT])')
        #st.subheader(f'최종 부채 증가량 : :blue[{round(final_debt_increase_btc, 5)} BTC]')
        st.subheader(f"현재 자산에서 LTV 50%가 되는 BTC가격 : :red[{ltv50price} USDT]")
        st.divider()


        st.subheader('투자 기간별 자산 변화 시뮬레이션')
        #st.dataframe(df.style.format(formatter="{:.4f}"))  # 수정된 부분
        st.table(df)

if __name__ == '__main__':
    app()
