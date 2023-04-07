

def filtering_string(value):
  
    
    stringValue = value.replace(',','').replace('배송비 ','').replace('배송비','').replace('무료','0').replace('KRW','').replace('배송','').replace('원','').replace('유지','').replace('상품','').replace('펼치기','').replace('상품접기','').replace('상승','').replace('하락','').replace('접기','').replace('NEW','').replace('오늘출발','')
   
    return stringValue