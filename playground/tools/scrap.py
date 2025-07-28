import requests
from typing import List, Dict, Any
from langchain.tools import tool
from concurrent.futures import ThreadPoolExecutor, as_completed

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "ko-KR,ko;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
})

# =============================================================================
# 🛠️ 1. 기본 상품 검색 도구
# =============================================================================
@tool
def search_basic_products(keyword: str, gender: str = "A", minPrice: int = 0, maxPrice: int = 999999, color: str = "",shoeSize: str = 0)-> list:
    """
    사용자가 단순히 "청바지 찾아줘", "나이키 신발 목록 보여줘" 와 같이 특정 조건의 상품 '목록'을 요청할 때 사용하세요.    
    혜택이나 리뷰 등 상세 정보 없이, 빠르고 간단한 검색 결과를 원할 때 가장 효율적입니다.
    예시) "나이키 신발 목록 보여줘" (keyword: 나이키 신발, 브랜드 + 상품명을 함께 키워드에 사용합니다) 

    Args:
        keyword (str): 검색할 상품 키워드 (예: "청바지", "반팔티"). 필수값입니다.
        gender (str): 검색할 성별. "M"(남성,남자), "F"(여성,여자) 중 하나를 지정할 수 있으며, 지정하지 않으면 "A"(전체)가 됩니다.
        minPrice (int): 검색할 최소 가격. 사용자 입력이 10만원이면 숫자 100000으로, 5만5천원이면 55000으로 변환하여 전달해야 합니다. 0 또는 미지정 시 무시됩니다.
        maxPrice (int): 검색할 최대 가격. 사용자 입력이 10만원이면 숫자 100000으로, 5만5천원이면 55000으로 변환하여 전달해야 합니다. 미지정 시 무시됩니다.
        color (str): 색상 필터. 사용자의 요청('빨간색', '레드')을 아래 목록의 영문 대문자 값('RED')으로 정확히 매핑해야 합니다. 미지정 시 무시됩니다.
                사용 가능한 값 : "WHITE", "SILVER", "LIGHTGREY", "GRAY", "DARKGREY", "BLACK", "RED",
                "DEEPRED", "BURGUNDY", "BRICK", "PALEPINK", "LIGHTPINK", "PINK", "DARKPINK", "PEACH", "LIGHTORANGE",
                "ORANGE", "DARKORANGE", "IVORY", "OATMEAL", "LIGHTYELLOW", "YELLOW", "MUSTARD", "GOLD", "LIME",
                "LIGHTGREEN", "GREEN", "OLIVEGREEN", "KHAKI", "DARKGREEN", "MINT", "SKYBLUE", "BLUE", "DARKBLUE",
                "NAVY", "DARKNAVY", "LAVENDER", "PURPLE", "LIGHTBROWN", "BROWN", "DARKBROWN", "CAMEL", "SAND",
                "BEIGE", "DARKBEIGE", "KHAKIBEIGE", "DENIM", "LIGHTBLUEDENIM", "MEDIUMBLUEDENIM", "DARKBLUEDENIM",
                "BLACKDENIM", "ETC"
        shoeSizeOption(int): 검색할 신발 사이즈. 미지정 시 무시됩니다. (220mm 이하: 220, 290mm 이상: 290)
                사용 가능한 값 : "220","225","230","235","240","245","250","255","260","265","270","275","280","285","290"
    Returns:
        Dict[str, Any]: 검색 결과를 담은 딕셔너리. 반환되는 상품 정보는 LLM이 사용자에게 답변하기 용이하도록 'goodsName', 'brandName', 'price, 'saleRate' 등 핵심 필드만으로 정제되어 있습니다.
        {
            "goodsNo": 4149670,
            "goodsName": "상품명",
            "goodsLinkUrl": "구매링크",
            "thumbnail": "이미지 URL",
            "displayGenderText": "남성",
            "isSoldOut": false, // true : 품절, false : 판매중
            "normalPrice": 49000, //정가
            "price": 29400, //할인가
            "saleRate": 40, //할인률
            "brand": "toffee", //브랜드 코드
            "brandName": "토피", //브랜드 명
            "brandLinkUrl": "https://www.musinsa.com/brand/toffee",
            "reviewCount": 1507,//리뷰수
            "reviewScore": 96,  //실제 평점은 96/20 = 4.8점)
            "isPlusDelivery": false
        }           
    """
    return search_basic_products_impl(keyword, gender, minPrice,maxPrice,color,shoeSize)


def search_basic_products_impl(keyword: str, gender: str = "A", minPrice: int = 0, maxPrice: int = 0, color: str = "",shoeSize: str = 0) -> list:    
    try:
        params = {
            'keyword': keyword,
            'gf': gender,            
            'page': 1,
            'size': 60,
            'caller': 'SEARCH'
        }        
        # 가격 조건이 유효할 경우에만 파라미터에 추가
        if minPrice > 0:
            params['minPrice'] = minPrice
        if maxPrice > 0:
            params['maxPrice'] = maxPrice
        
        # 색상 조건이 있을 경우에만 파라미터에 추가
        if color.strip():
            params['color'] = color
        if shoeSize:
            params['shoeSizeOption'] = shoeSize

        url = f"https://api.musinsa.com/api2/dp/v1/plp/goods"
        
        print(f"params: {params}")

        response = session.get(url, verify=False, timeout=10,params=params)
        response.raise_for_status()
        
        product_list = response.json()
        return {
            "success" : True,
            "product_list" : product_list
        }    
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error scrapping Musinsa search: {e}"
        }
# =============================================================================
# 2. 상품 혜택 조회 도구
# =============================================================================
@tool
def fetch_product_benefits(goods_no: str, brand: str) -> Dict[str, Any]:
    """
    * 중요사항 : goods_no(상품번호)값은 search_basic_products 함수 호출 후 반환받은 값을 활용해야 합니다.
    개별 상품의 결제 혜택 프로모션 정보를 가져옵니다.
    
    Args:
        goods_no (str): 상품번호(Required)
        brand   (str): 브랜드명(Optional)
    
    Returns:
        Dict[str, Any]: 혜택 정보
        {
            "success": True/False,
            "goods_no": "4149670",
            "benefits": [
                {
                    "applyPayKindName": "무신사페이",
                    "applyCardName": "무신사현대카드", 
                    "discountAmount": 10000,  # 할인 금액 (원)
                    "minAmount": 11000       # 최소 구매 금액 (원)
                }
            ]
        }
    """    
    return fetch_product_benefits_impl(goods_no,brand)

def fetch_product_benefits_impl(goods_no: str, brand: str) -> Dict[str, Any]:
    try:        
        response = session.get(f"https://goods-detail.musinsa.com/api2/goods/{goods_no}/card-promotion?&brand={brand}", timeout=10,verify=False)
        response.raise_for_status()
        
        data = response.json()
        
        promotion_list = []
        
        promotions = data.get('data').get('promotions', [])        
        for promotion in promotions:
            promotion_fields = get_promotion_fields(promotion)
            if promotion_fields:
                promotion_list.append(promotion_fields)

        
        return {
            "success": True,
            "goods_no": goods_no,
            "product_promotion_list": promotion_list
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }

# =============================================================================
# 📝 3. 상품 리뷰 조회 도구
# =============================================================================
@tool
def fetch_product_reviews(goods_no: str,review_count: int = 3) -> Dict[str, Any]:
    """
    * 중요사항 : goods_no(상품번호)값은 search_basic_products 함수 호출 후 반환받은 값을 활용해야 합니다.
    특정 상품의 사용자 리뷰를 조회합니다.

    언제 사용하나요?
    - 사용자가 "이 상품 리뷰 보여줘", "후기 알려줘" 라고 물을 때
    - 특정 상품 번호(goods_no)를 알고 있을 때
    
    Args:
        goods_no (str): 상품번호
        review_count (int): 가져올 리뷰 개수 (기본값: 3)
            최소 1개, 최대 20개까지 가능
    
    Returns:
        Dict[str, Any]: 리뷰 정보
        {
            "success": True/False,
            "goods_no": "4149670", 
            "review_list": [
                {
                    "review": "정말 편하고 좋아요!",
                }
            ]
        }
    """
    return fetch_product_reviews_impl(goods_no, review_count)


def fetch_product_reviews_impl(goods_no: str,review_count: int = 3) -> Dict[str, Any]:
    try:
        response = session.get(f"https://goods.musinsa.com/api2/review/v1/picture-reviews?goodsNo={goods_no}&size={review_count}&page=1", timeout=10,verify=False)
        response.raise_for_status()
        
        data = response.json();
        review_list = data.get("data").get("list")
        
        improve_review_list = []

        for review in review_list:
            review_fields = get_review_fields(review)
            if review_fields:
                improve_review_list.append(review_fields)

        
        return {
            "success": True,
            "goods_no": goods_no,
            "review_list": improve_review_list
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }

def get_promotion_fields(promotion):
    return {
        "applyPayKindName": promotion.get("applyPayKindName",""),
        "applyCardName": promotion.get("applyCardName",""),
        "discountAmount": promotion.get("discountAmount",""),
        "minAmount": promotion.get("minAmount","")
    }
def get_review_fields(review):
    return {
        "review": review["content"]
    }

# =============================================================================
# 🚀 4. 완전한 상품 정보 수집 도구 (통합형)
# ============================================================================

@tool
def search_detailed_products(keyword: str, gender: str = "A", minPrice: int = 0, maxPrice: int = 0, color: str = "", shoeSize: int = 0, limit: int = 1) -> Dict[str, Any]:
    """
    사용자가 "10만원 이하 청바지 추천해줘", "가장 할인율 높은 반팔티 알려줘", "리뷰 좋은 신발 3개만 요약해줘" 와 같이 여러 정보를 종합하여 
    '추천'이나 '비교', '요약'을 요청할 때 사용하세요. 검색 결과에 혜택과 리뷰 정보가 반드시 포함되어야 할 때 적합합니다.

    Args:
        keyword (str): 검색할 상품 키워드 (예: "청바지", "반팔티"). 필수값입니다.
        gender (str): 검색할 성별. "M"(남성), "F"(여성) 중 하나를 지정할 수 있으며, 지정하지 않으면 "A"(전체)가 됩니다.
        minPrice (int): 검색할 최소 가격. 사용자 입력이 10만원이면 숫자 100000으로, 5만5천원이면 55000으로 변환하여 전달해야 합니다. 0 또는 미지정 시 무시됩니다.
        maxPrice (int): 검색할 최대 가격. 사용자 입력이 10만원이면 숫자 100000으로, 5만5천원이면 55000으로 변환하여 전달해야 합니다. 0 또는 미지정 시 무시됩니다.
        color (str): 색상 필터. 사용자의 요청('빨간색', '레드')을 아래 목록의 영문 대문자 값('RED')으로 정확히 매핑해야 합니다. 미지정 시 무시됩니다.
                사용 가능한 값 : "WHITE", "SILVER", "LIGHTGREY", "GRAY", "DARKGREY", "BLACK", "RED",
                "DEEPRED", "BURGUNDY", "BRICK", "PALEPINK", "LIGHTPINK", "PINK", "DARKPINK", "PEACH", "LIGHTORANGE",
                "ORANGE", "DARKORANGE", "IVORY", "OATMEAL", "LIGHTYELLOW", "YELLOW", "MUSTARD", "GOLD", "LIME",
                "LIGHTGREEN", "GREEN", "OLIVEGREEN", "KHAKI", "DARKGREEN", "MINT", "SKYBLUE", "BLUE", "DARKBLUE",
                "NAVY", "DARKNAVY", "LAVENDER", "PURPLE", "LIGHTBROWN", "BROWN", "DARKBROWN", "CAMEL", "SAND",
                "BEIGE", "DARKBEIGE", "KHAKIBEIGE", "DENIM", "LIGHTBLUEDENIM", "MEDIUMBLUEDENIM", "DARKBLUEDENIM",
                "BLACKDENIM", "ETC"
        shoeSizeOption(int): 검색할 신발 사이즈. 미지정 시 무시됩니다. (220mm 이하: 220, 290mm 이상: 290)
                사용 가능한 값 : "220","225","230","235","240","245","250","255","260","265","270","275","280","285","290"
    
    Returns:
        Dict[str, Any]: 검색 결과를 담은 딕셔너리. 반환되는 상품 정보는 LLM이 사용자에게 답변하기 용이하도록 'goodsName', 'brandName', 'price, 'saleRate' 등 핵심 필드만으로 정제되어 있습니다.
    """
    print(f"검색 시작 - 키워드: {keyword}, 조건: gender={gender}, price={minPrice}-{maxPrice}")
    
    # 1. 기본 상품 검색
    search_result = search_basic_products_impl(keyword, gender, minPrice, maxPrice, color, shoeSize)
    print(f"검색 완료 by search_result : {search_result}")
    if not search_result.get('success') != True:
        return search_result

    products = search_result.get('product_list').get('data').get('list', [])[:limit]  # 제한된 수의 상품만 처리
    
    if not products:
        return {
            "success": True,
            "message": "검색 결과가 없습니다.",
            "products": []
        }
    
    # 2. 각 상품에 대한 추가 정보 수집
    print(f"{len(products)}개 상품에 대한 추가 정보 수집 시작")
    enhanced_products = enrich_products_with_details_impl(products)    
    
    return {
        "success": True,
        "keyword": keyword,
        "total_found": len(enhanced_products),
        "products": enhanced_products
    }      

# =============================================================================
# 🔧 5. 병렬 데이터 수집 도구
# =============================================================================

@tool
def enrich_products_with_details(products: List[Dict[str, Any]], max_workers: int = 5) -> List[Dict[str, Any]]:
    """
    상품 리스트에 대해 병렬로 혜택과 리뷰 정보를 수집합니다.

    언제 사용하나요?
    - 이미 상품 리스트가 있고, 추가 정보만 필요할 때
    - 다른 도구에서 받은 상품 데이터를 보강하고 싶을 때
    
    Args:
        products (List[Dict[str, Any]]): 기본 상품 정보 리스트
        max_workers (int): 최대 동시 작업 수
    
    Returns:
        List[Dict[str, Any]]: 혜택과 리뷰가 추가된 상품 리스트
    """    
    return enrich_products_with_details_impl(products)

def enrich_products_with_details_impl(products: List[Dict[str, Any]], max_workers: int = 5) -> List[Dict[str, Any]]:
    enhanced_products = []
    
    def fetch_additional_data(product):
        """개별 상품에 대한 추가 데이터 수집"""
        goods_no = str(product.get('goodsNo', ''))
        brand = str(product.get('brand', ''))
        if not goods_no:
            return product
        if not brand:
            return product            
        
        # 혜택과 리뷰 정보를 병렬로 수집
        benefits_data = fetch_product_benefits_impl(goods_no,brand)
        # print(f"혜택 리스트 : {benefits_data}\n")
        reviews_data = fetch_product_reviews_impl(goods_no)
        # print(f"리뷰 리스트 : {reviews_data}\n")
        # 기본 상품 정보에 추가 정보 병합
        enhanced_product = product.copy()
        enhanced_product['benefits'] = benefits_data.get('product_promotion_list', [])
        enhanced_product['reviews'] = reviews_data.get('review_list', [])
        enhanced_product['benefits_success'] = benefits_data.get('success', False)
        enhanced_product['reviews_success'] = reviews_data.get('success', False)
        
        return enhanced_product
    
    # ThreadPoolExecutor를 사용한 병렬 처리
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_product = {executor.submit(fetch_additional_data, product): product for product in products}
        
        for future in as_completed(future_to_product):
            try:
                enhanced_product = future.result(timeout=30)
                enhanced_products.append(enhanced_product)
            except Exception as e:
                original_product = future_to_product[future]
                print(f"상품 {original_product.get('goodsNo')} 데이터 수집 실패: {e}")
                # 실패한 경우에도 기본 정보는 포함
                enhanced_products.append(original_product)
    
    return enhanced_products  


if __name__ == "__main__":
    result = search_detailed_products.invoke("청바지")
    print(result)