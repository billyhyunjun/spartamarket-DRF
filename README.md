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
<summary>View Template (click here) </summary>
<div markdown="1">       

## ** index **
- 메인화면으로 화면 상단 네브바에는 유저의 정보 밑 바로가기키가 있으며, 중단에는 최근에 작성된 게시글과 판매글이 업로드 됩니다. 그리고 하단에는 메인가기 및 도감확인, 웹페이시 사용법이 표기 되어 있습니다.

![image](https://github.com/billyhyunjun/sparta_market/assets/157565164/58633751-83ce-46f6-9091-e8161ac4d079)



</div>
</details>


## 📌 Key Features

### 1. Post CRUD
   - Users can create new posts and view all posts.
   - Posts can be edited or deleted on the post detail view page.

### 2. Comment CRD
   - All comments on the post are displayed at the bottom of the post detail view page.
   - Users can create, view, and delete comments on the post detail page.

### 3. Sign Up, Log In
   - Membership registration is mandatory for first-time users, enabling them to log in and access the site's features.
   - Only logged-in users can create posts, while both logged-in and anonymous users can view posts and comments.
     
### 5. Search Functionality
   - Users can search for posts by movie name, article title, author, and content using the post search box.
   - Clicking on search results directs users to the detailed page of the respective post.

### 6. Like Feature
   - Users can like posts on the post details view page.
   - The 'Like' button toggles to 'Dislike' upon clicking and can be undone, allowing users to like a post only once.
     
### 8. Administrator Permissions
   - Administrators with the ID "admin_team8" have the authority to edit or delete posts and comments, irrespective of the post's author.

### 9. User Interaction
   - Users can follow and unfollow other users, fostering a sense of community within the platform.
   - The 'Following' list enables users to keep track of updates from their followed users.

<br> 

## ✒️ API

![image](https://github.com/billyhyunjun/spartamarket-DRF/assets/157565164/be0f7036-1ada-40bc-aa11-8529175cdcd6)




