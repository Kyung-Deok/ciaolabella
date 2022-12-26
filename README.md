# Ciao laBella - extension
## 라벨 여부 이미지 인식에 따른 에코포인트 적립 서비스 - 확장 데이터 파이프라인 구축
>1차 프로젝트 기간 : 2022.08.18 ~ 2022.09.30<br>
2차 프로젝트 기간 : 2022.10.12 ~ 2022.12.21<br>
[서비스 페이지](https://ciaoleblla.ga/)

기존 ciaolabella 서비스를 확장하여, 
1) 유저 로그를 수집·집계·적재·시각화하는 파이프라인을 구축 
2) 주기적인 서비스 업데이트를 위한 스케쥴링 
3) 모델 재학습을 위한 유저 업로드 사진 및 모델 결과 수집
4) 실시간 검색어 제공, 유저 맞춤형 마이페이지 등 서비스 고도화
* 고유정[yu-je0ng](https://github.com/yu-je0ng)
* 김세진[nijes](https://github.com/nijes)
* 류재선[prudent-PS](https://github.com/prudent-PS)
* 이경덕[Kyung-Deok](https://github.com/Kyung-Deok)
* 주한나[hanna-joo](https://github.com/hanna-joo)

<br>

## 수집 데이터
| no  |         내용         |        출처        |    형식/방식     |
|:---:|:------------------:|:----------------:|:------------:|
|  1  |     생활폐기물 이미지      |      직접 생성       |   IMG/FILE   |
|  2  |     생활폐기물 이미지      |  [AIHUB][AIHUB]  |  JSON/FILE   |
|  3  |    우리동네 제로웨이스트샵    |    [네이버][네이버]    |   CSV/CRAWLING   |
|  4  |   지도_전국 제로웨이스트샵    |    [구글맵][구글맵]    |   CSV/CRAWLING   |
|  5  | 카카오 제로웨이스트숍/리필/재활용 |   [카카오맵][카카오맵]   |   CSV/CRAWLING   |
|  6  |  스마트서울맵 제로웨이스트 상점  | [스마트서울맵][스마트서울맵] |   JSON/API   |
|  7  |  카카오API 제로웨이스트 상점  | [카카오API][카카오API] |   JSON/API   |
|  8  |       네이버 쇼핑       |  [네이버쇼핑][네이버쇼핑]  | CSV/CRAWLING |
|  9  |   슈퍼빈:네프론 위치 정보    |    [슈퍼빈][슈퍼빈]    |   JSON/API   |

[AIHUB]: https://www.aihub.or.kr/
[네이버]: https://www.naver.com/
[구글맵]: https://www.google.co.kr/maps
[카카오맵]: https://map.kakao.com/
[스마트서울맵]: https://map.seoul.go.kr/smgis2/
[카카오API]: https://developers.kakao.com/
[네이버쇼핑]: https://shopping.naver.com/home
[슈퍼빈]: https://www.superbin.co.kr/

<br>

## 아키텍처 및 기술 스택

![차라라_아키텍처정의서](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbnHN5A%2FbtrUceYxRKX%2FrdwbcF5K70ug4KLEQPmktk%2Fimg.png)
![차라라_노드분리도](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FLzwYo%2FbtrUfr3FIzB%2FncVH8O47CWbZTETzEdAHU0%2Fimg.png)

* AWS EC2 [free tier]
* Ubuntu [20.04]
* Kafka [2.12-3.2.0]
* Zookeeper [3.8.0]
* Hadoop [3.3.3]
* Spark [3.1.3]
* Django [3.2.16]
* MySQL [8.0.31]
* Elasticsearch [7.17.5]
* Redis [7.0.5]
* MongoDB [4.4.5]
* Flask [2.2.2]
* Docker
* Nginx
* Airflow [2.5.0]

<br>

## 데이터 종류별 구축 파이프라인

### 사용자 로그 데이터
![log_pipeline](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbX4png%2FbtrUxdYLAle%2F8zh19fuY0isLKuS6jLpJak%2Fimg.png)
* 수집 목적에 따라 Hot data(실시간으로 확인하기 위한 당일 데이터)/Warm data(최근 일주일 치 데이터)/Cool data(향후 사용 가능성 있는 과거 데이터)로 구분
* 장고에서 수집한 원본 로그 데이터를 1차적으로 데이터허브인 Kafka에 저장
  * spark-streaming을 통하여 실시간 데이터에 대해 1분 또는 5분 단위로 집계하여 redis에 저장 => streamlit을 통한 시각화
  * spark-streaming을 통하여 당일 발생 로그에 대해 집계본을 만들어 kafka에 저장
* 로그 집계 데이터를 2차적으로 Kafka에 저장
  * Warm data로 활용하기 위하여 최근 1주일치 데이터에 대해 MongoDB에 저장 => Grafana를 통한 시각화
  * Cool data로 활용하기 위하여 전체 데이터를 Hadoop에 parquet 형식으로 저장
<br><br>
### 사용자 이미지 데이터
![image_pipeline](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fst5dt%2FbtrUxpLw4L5%2Fa1INFUKaCa7QmRt8XmBkJk%2Fimg.png)
* django 서비스에서 유저가 업로드한 이미지 원본을 grifs를 이용하여 mongodb에 저장
* flask app에서 원본 이미지에 대한 yolov5모델 결과가 포함된 이미지를 grifs를 이용하여 mongodb에 저장 
<br><br>
### nolabal 제품 정보 데이터
![nolabel_pipeline](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fddv8U1%2FbtrUuQpJIBP%2FIKPlXmd5VoZxjy5ESBq9B1%2Fimg.png)
* 파이썬 스크립트를 통하여 웹에서 nolabel 제품데이터 크롤링 후 원본 hadoop에 적재
* spark를 통한 원본 데이터 가공 후 kafka 적재 후 es 저장
* 매주 일요일 02:00 데이터 업데이트 되도록 airflow를 통한 스케쥴링
<br><br>
### lesswaste 위치 데이터
![lesswaste_pipeline](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbyN5bs%2FbtrUyhUcJJ0%2FkzZDrYU6EVSQQoa5LKWDB1%2Fimg.png)
* api, 크롤링 등을 통해 수집한 원본 데이터 hadoop 적재
* spark를 통한 원본 데이터 가공 후 mongodb에 geojson 형태로 저장

<br>

[//]: # ()
[//]: # (## 데이터 파이프라인 세부 기술)

[//]: # ()
[//]: # (### Kafka)

[//]: # ()
[//]: # (### Hadoop)

[//]: # ()
[//]: # (### Spark)

[//]: # ()
[//]: # (### ElasticSearch)

[//]: # ()
[//]: # (### Airflow)

[//]: # ()
[//]: # (### Redis)

[//]: # ()
[//]: # (### MongoDB)

[//]: # ()
[//]: # (### MySQL)

[//]: # ()
[//]: # (### Docker)

[//]: # ()
[//]: # (### Streamlit)

[//]: # ()
[//]: # (### Grafana)

[//]: # ()
[//]: # (<br>)

## 서비스 화면
### 인덱스 페이지
![index](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FYUkFY%2FbtrUfbmCVv8%2F6gL7fLdgTH73ygvGvVWUnK%2Fimg.png)

### About 페이지
![About](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcmQZ58%2FbtrUzl25CIf%2FF2x66CpWPKg7bw0F45mbRk%2Fimg.png)

### Ecopoint1 페이지
![Ecopoint1](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FWBCCL%2FbtrUxeQXxet%2F4MrkEniqZA7jbrJk3TP3e1%2Fimg.png)

### Ecopoint2 페이지
![Ecopoint2](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FpLeNy%2FbtrUt25gkFq%2FTbj4o4yUfr9LKWQBs61WBK%2Fimg.png)

### No Label 페이지
![NoLabel](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcDON8h%2FbtrUzlINwqq%2FfZCTjOPQ7xKboUMdmyqHFk%2Fimg.png)

### Less Waste 페이지
![LessWaste](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fbxt71o%2FbtrUExBL38m%2FXGieoLXyooN407mZHJV2JK%2Fimg.png)

### 마이페이지
![Mypage](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbHRshn%2FbtrUBaAglcl%2Fiax4Tr9qUTTb49J1Komhzk%2Fimg.png)

### 회원가입 페이지
![SignUp](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FXu8Ja%2FbtrUa25u90u%2FP5AHkpz1pAtB9ScT5im210%2Fimg.png)

### 로그인 페이지
![SignIn](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FYKE0k%2FbtrUuhHFrhk%2FzTyaKCh9ZYXay9hAsx9LhK%2Fimg.png)