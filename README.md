# 🗣️Project: spartamarket-DRF
### Django_DRF로 작성한 spartamarket

<br>

## 👨‍🏫 Project Introduction
SpartaMarket는 Django_DRF를 이용하여 백앤드에서 자료를 받아 데이터 베이스에 저장하는 방식을 이용한 프로젝트입니다.

<br>

## ⏲️ Development time
- 2024.04.29(월) ~ 2023.05.02(목)
- 아이디어 노트 작성
- 와이어프레임
- 기능구현
- 발표
<br>

## 🧑‍🤝‍🧑 Development Function: 
- ** 사용자 계정 ** : 회원가입, 로그인, 로그아웃 기능을 제공합니다. 
- ** 상점 관리 ** : 상점 등록, 수정, 삭제, 구매, 좋아요, 해시태그, 카테고리 기능을 제공합니다. 또한 검색을 통해서 원하는 게시글을 검색 할 수 있습니다.
- ** 유저 프로필 및 기타 기능 ** : 유저 프로필 보기, 팔로우의 기능을 지원합니다.

<br>

## 💻 Development Environment
- **Programming Language** : Python 3.12
- **Web Framework** : Django
- **Template Engine** : Jinja2
- **Database** : SQLite3 (for development and testing)
- **IDE** : Visual Studio Code
- **Version Control** : Git, GitHub
<br>

## ⚙️ Technology Stack
- **Backend** : Django
- **Database ORMR** : SQLite3
- **Idea Brainstorming Tools and Environments** : figmam, drow.io
<br>

## 📝 Project Architecture

- **WireFrame**

https://www.figma.com/file/KLAi2WghRyyMJGMVMDvNb8/SpartaMarket_DRF?type=whiteboard&node-id=0-1&t=0cbuzv9KO2j3BG2U-0

- **ERD**

https://app.diagrams.net/#G1VK_R85V6tnn5qrfNOdDxszWH0Wu17HJT#%7B%22pageId%22%3A%22R2lEEEUBdFMjLlhIrx00%22%7D

## 🖥️Poatman View

<details>
<summary>View Json (click here) </summary>
<div markdown="1">       

## ** 회원가입 **
- 회원가입을 위해서 username, 비밀번호, 이메일, 이름, 생일을 입력 받을 수 있으며 ID, 비밀번호, 이메일을 필수로 입력을 받으며, ID와 이메일은 중복으로 작성이 불가능합니다.

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/e913ed79-bb0b-48ba-8d81-7d6d2effb52d)


## ** 로그인 **
- 회원 가입으로 작성이 된 아이디와 비밀번호로 로그인을 시도하면 refresh_token과 access_token이 발급이 됩니다.

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/ffe02b2f-85a6-41f9-a181-89bdccd2749d)


## ** 토큰 재발급 **
- 로그인으로 발급 받은 refresh_token은 하루동안 사용이 가능하며 access_token은 1분으로 설정이 되어있습니다. access_token이 만료가 되면  refresh_token토큰을 이용하여 access_token을 재발급 받을 수 있습니다.

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/7059ada1-8898-449a-ab8e-40cd377fbe15)


## ** 프로필 조회 **
- 주소끝에 유저의 ID를 적어 해당 유저의 프로필을 확인 할 수 있습니다.

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/2cc0df55-ffc6-41f3-a606-c17804d07c76)



## ** 로그아웃 **
- 로그아웃의 데이터로 refresh_token을 입력하면 해당 refresh_token는 블랙리스트에 입력이 되어 재발급을 받지 못하는 상태로 저장 되어 로그아웃이 됩니다.

- 로그아웃 완료

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/c7f5e66a-4778-4713-a10e-e49007722e6e)

- 재시도시

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/2872e145-ad29-40de-bd95-77e8dfddfa5f)

- 토큰 재발급시 블랙처리된 토큰

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/57c2f2f6-5306-480f-ac76-2a764c240011)


## ** 본인 정보 수정 **
- 주소에 해당하는 유저의 아이디로 접속을 하여 내용을 수정할 수 있으며 변경되지 않은 내용은 전의 내용을 반영하며, 자신이 설정한 이메일 또는 사용이력이 없는 이메일로 변경시에는 적용이 가능하나 타유저가 사용중인 이메일을 사용시 에러가 발생하며, 현재 접속중인 아이디로 타유저의 프로필을 변경할 수는 없습니다.

- 수정 완료

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/2af0b5b8-56c8-431a-9a83-d66b08e175b7)

- 다른 계정 수정시도 시

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/e6ef14d1-4440-4b31-86be-3319fcb0b45c)

- 중복 이메일 작성시

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/f92c6608-6c4f-41c7-92bb-3d4bd89532af)


## ** 패스워드 변경 **
- 페스워드 변경 또한 로그인되어 있는 유저의 비밀번호를 변경을 하게 되며, 로그인되어 있는 아이디와 current_password가 일치하여야 하며, current_password와 new_password가 서로 다르고 new_password와 confirm_password의 일치를 확인 되면 비밀번호를 수정하며, 이후로는 수정된 비밀번호로 로그인을 시도해야지만, 토큰이 발급이 됩니다.

- 변경 성공

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/c3d37ff4-8164-434f-beac-fc377d5f9884)

- 수정 전 비밀번호 입력력

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/5bab4639-f045-4569-a802-0b46baf45bf4)

- 수정 후 비밀번호 입력

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/0d07f747-1501-4f52-a7ce-31214134a320)


## ** 회원 탈퇴 **
- 로그인이 되어 있는 상태에서 탈퇴를 할려는 계정과 로그인 되어 있는 계정

- 회원 탈퇴 성공

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/4f037194-6569-4d02-a6e1-5f6ee93242db)

- 탈퇴 후 로그인 시도 시

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/5771d94d-e6fd-41bd-a014-ee34f5e64000)

- 다른 계정 탈퇴 시도시

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/a43c6d41-4356-4e40-a7fc-9d5269148720)


## ** 팔로잉 시스템 **
- 로그인이 되어 있는 상태에서 내가 팔로잉을 하고 싶은 계정으로 팔로잉을 하면 내 프로필에 해당 계정이 생성이 됩니다.

- 팔로잉 성공

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/724f4101-d08c-41e0-8e3e-6e7eee363579)

- 내 프로필에 팔로잉 한 계정이 생성

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/0a29f0d3-40d4-4c9c-b6d6-c0e0e567148f)



## ** 상품 등록 **
- 상품을 등록시 제목, 내용, 가격, 해시태그, 카테고리를 입력 받으며, 해시태그는 대소문자를 전부 대문자로 받아들여 저장을 하고, 중복없이 저장을 합니다.

- 상품 등록

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/bce5c5aa-f80e-4b15-8e28-105ea2fb12fd)

- 등록 결과

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/d7067a1f-5e24-437f-b078-9beee20e22d5)


## ** 상품 목록 조회 **
- 상품은 로그인이 필요 없이 조회가 가능하며, 각 상점의 생성 순으로 작성이 되어 있습니다.

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/64a56108-e468-4278-b9ee-5ed0906e2d17)


## ** 상품 상세 조회 **
- 상품 게시글의 id을 입력으로 넣어 해당 게시물의 내용만을 따로 볼 수 있으며 해당 게시물에 작성 되어 있는 댓글도 함께 볼 수 있습니다. 

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/9aca4411-5789-4f11-b26a-74dd87d68f78)


## ** 상품 수정 **
- 상품의 내용을 수정하고, 변경 되지 않는 내용을 그대로 반영을 합니다.

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/9a63dd57-1434-4634-9b88-23378640272d)


## ** 상품 삭제 **
- 해당 로그인아이디와 작성된 게시글의 작성자가 동일하다면 게시글을 삭제 할 수 있습니다.

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/7e674a29-80b0-4d99-9663-d3343289b901)


## ** 필터링(검색기능) **
- key값에 검색할 대상과 value값으로 해당 내용을 입력하면 입력 데이터에 맞는 게시글이 조회가 되어 검색이 됩니다.

- 작성자 검색

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/974948d2-71b6-4fea-bb5f-123f332ea6d3)

- 제목 검색

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/f5b28365-e13c-4374-8904-a721227177b9)

- 내용 검색

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/b9b6bc85-b4c9-4e6c-967e-a1a9540d38f5)

- 게시글 좋아요 많은 순으로 보기

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/641f7660-941d-40f6-9be7-cd5b0e8d62d5)

- 해시태그 검색

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/018159bf-63b9-4401-9148-819ac3fee990)

- 카테고리 검색

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/1f16cb6b-e6b3-4b9f-8029-32c72044d488)




</div>
</details>

## 📌 Key Features

### Sign Up and Log In
- New users can sign up to the site by providing their username, password, and email, all of which are mandatory fields. Duplicate usernames and emails are not allowed.
- Registered users can log in using the username and password they provided during sign up, accessing the site's functionalities.
### Token Refreshment
- Upon login, users receive a refresh_token that remains valid for one day, while the access_token has a one-minute lifespan. When the access_token expires, users can use the refresh_token to obtain a new access_token.
Profile Viewing and Editing
- Users can view and modify their profiles. While editing profiles, changing to an email address without usage history is allowed, but an error occurs if attempting to use an email address already in use by another user.
### Password Modification
- Logged-in users can change their passwords. When changing passwords, they must provide their current password along with the new one and confirm it.
### Account Deactivation
- Logged-in users have the option to deactivate their accounts.
### Following System
- Users can follow other users, and the users they follow will appear on their profile.
### Product Management: Create, Read, Update, Delete (CRUD)
- Users can create new products and view, edit, or delete existing ones.
### Filtering and Search Functionality
- Users can search for posts based on various criteria such as author, title, content, hashtags, and categories.
- Search results are sorted by the number of likes on the posts, and users can view detailed information of the relevant posts.

<br> 

## ✒️ API

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/be0f7036-1ada-40bc-aa11-8529175cdcd6)




