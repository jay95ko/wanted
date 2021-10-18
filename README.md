# [위코드 x 원티드] 백엔드 프리온보딩 선발 과제
- 사용자 인증, 인가 구현
- 게시물 CRUD 구현하기
___

## 구현한 방법과 이유에 대한 간략한 내용
#### 사용자
- 사용자의 인증과 인가를 위해 jwt토큰을 사용하였습니다.
- jwt토큰의 보안성을 위해 만료시간을 추가하였으며, 테스트의 편의성을 위해 시간은 5분으로 설정하였습니다.
- jwt토큰에 담고있는 정보는 만료시간과 user의 pk가 전부입니다.

#### 게시물
- 로그인을 하지 않은 유저도 게시물은 확인 할 수 있게 하였습니다.
- 혹시나 존재하는 익명의 사용자에 의한 악성 파일 업로드, 불필요 글 게시등 을 막기 위해 사용자는 로그인을 해야 글을 작성 할 수 있습니다.
- 게시물을 작성한 사용자를 확인하는 방법은 로그인이 되었을 때 발급되는 jwt토큰을 활용하여 확인 하였으며, 게시물을 작성한 본인만이 게시물을 수정 또는 삭제할 수 있습니다.
___

## 자세한 실행 방법(endpoint 호출방법)
| METHOD | URL           | Req body              | 비고         |
|:------:|:-------------:|-----------------------|------------|
| POST   | /users/signup | email, name, password | 회원가입       |
| POST   | /users/login  | email, password       | 로그인        |
| GET    | /posts        |                       | 게시물 리스트 확인 |
| POST   | /posts        | post                  | 게시물 생성     |
| GET    | /posts/<id>   |                       | 게시물 확인     |
| PATCH  | /posts/<id>   | post                  | 게시물 수정     |
| DELETE | /posts/<id>   |                       | 게시물 삭제     |
___
## api 명세(request/response 서술 필요)
### 1. 회원가입
- METHOD : POST 
- URL : /users/signup
- Request

| 항목       | 데이터 형  | 예시                         | 비고                     |
|----------|--------|----------------------------|------------------------|
| email    | string | “email” : “tour@gmail.com” | “@“와 “.”이 들어간 이메일 형식   |
| password | string | “password” : “1q2w3e4r!”   | 특수문자, 숫자, 영어 포험 8-20글자 |
| name     | string | “name” : “tour”            |                        |
- Request example
```bash
curl --location --request POST 'http://127.0.0.1:8000/users/signup' \
--data-raw '{
    "email" : "abcde@gmail.com",
    "password" : "abcd123!@",
    "name" : "김철수",
}
'
```
- Response example
```bash
{
  "Message": "SUCCESS_CREATE"
}
```

### 2. 로그인
- METHOD : POST 
- URL : /users/login
- Request

| 항목       | 데이터 형  | 예시                         | 비고                     |
|----------|--------|----------------------------|------------------------|
| email    | string | “email” : “tour@gmail.com” | “@“와 “.”이 들어간 이메일 형식   |
| password | string | “password” : “1q2w3e4r!”   | 특수문자, 숫자, 영어 포험 8-20글자 |
- Request example
```bash
curl --location --request POST 'http://127.0.0.1:8000/users/login' \
--data-raw '{
    "email" : "tour@gmail.com",
    "password" : "1q2w3e4r!"
}'

```
- Response example
```bash
{
    "Message": "LOGIN_SUCCESS",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MywiZXhwIjoxNjM0NTk5MzU1fQ.T74ldyuj-Y8MLA-dc2j5Ilvwlww8W6lwUXQ-lMSOpao"
}
```

### 3. 게시물 리스트 확인
- METHOD : GET
- URL : /posts
- PARAMS

| 항목     | 데이터 형 | 예시        | 비고  |
|--------|-------|-----------|-----|
| offset | int   | ?offset=0 |     |
| limit  | int   | ?limit=5  |     |
- Request example
```bash
curl --location --request GET 'http://127.0.0.1:8000/posts?offset=0&limit=5'
```
- Response example
```bash
{
    "Result": {
        "count": 5,
        "data": [
            {
                "post": "post8",
                "author": "ko",
                "created_at": "2021-10-19 08:21:21"
            },
            {
                "post": "post7",
                "author": "ko",
                "created_at": "2021-10-19 08:21:15"
            },
            {
                "post": "post6",
                "author": "ko",
                "created_at": "2021-10-18 20:28:13"
            },
            {
                "post": "post5",
                "author": "ko",
                "created_at": "2021-10-18 20:28:08"
            },
            {
                "post": "post4",
                "author": "ko",
                "created_at": "2021-10-18 20:28:05"
            }
        ]
    }
}
```

### 4. 게시물 생성
- METHOD : POST 
- URL : /posts
- Request

| 항목   | 데이터 형  | 예시                      | 비고  |
|------|--------|-------------------------|-----|
| post | string | “post” : “this is post” |     |
- Request example
```bash
curl --location --request POST 'http://127.0.0.1:8000/posts' \
--data-raw '{
    "post" : "this is post",
}'
```
- Response example
```bash
{
    "Message": "SUCCESS_CREATE"
}
```

### 5. 게시물 확인
- METHOD : GET
- URL : /posts/<id>
- Path PARAMS

| 항목  | 데이터 형 | 예시  | 비고  |
|-----|-------|-----|-----|
| id  | int   | /1  |     |
- Request example
```bash
curl --location --request GET 'http://127.0.0.1:8000/posts/1'
```
- Response example
```bash
{
    "Result": {
        "post": "post6",
        "author": "ko",
        "created_at": "2021-10-18 20:28:13"
    }
}
```

### 6. 게시물 수정
- METHOD : PATCH
- URL : /posts/<id>
- Path PARAMS

| 항목  | 데이터 형 | 예시  | 비고  |
|-----|-------|-----|-----|
| id  | int   | /1  |     |
- Request

| 항목   | 데이터 형  | 예시                           | 비고  |
|------|--------|------------------------------|-----|
| post | string | “post” : “this is edit post” |     |
- Request example
```bash
curl --location --request POST 'http://127.0.0.1:8000/posts/1' \
--data-raw '{
    "post" : "this is post",
}'
```
- Response example
```bash
{
    "Message": "SUCESS_UPDATE"
}
```

### 7. 게시물 삭제
- METHOD : DELETE
- URL : /posts/<id>
- Path PARAMS

| 항목  | 데이터 형 | 예시  | 비고  |
|-----|-------|-----|-----|
| id  | int   | /1  |     |
- Request example
```bash
curl --location --request GET 'http://127.0.0.1:8000/posts/1'
```
- Response
| status_code | json |
|-------------|------|
| 204         | x    |
