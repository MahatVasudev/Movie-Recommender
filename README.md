# Movie-Recommender

## An Internship Project

Before Proceeding you need to download dataset from here
[Updated Kaggle Data Set Link](https://www.kaggle.com/datasets/mahatvasudev/movie-dataset-for-personal-project).
I have cleaned and updated the dataset that I got from somewhere (I have to find the source)

---

# Movie Recommendation Website

![Screenshot 2024-06-22 122200(1)](https://github.com/user-attachments/assets/9b488bea-4ee8-475a-bc4d-f43ad8425f10)

![Pasted image 20240703094103](https://github.com/user-attachments/assets/e4c166de-89e2-4243-9c17-415f1fd93822)


# Tech Used
- Django Python
- HTML/CSS
- JobLib
- SpaCy
- NLTK
- Selenium

# All Movies Section

![Screenshot 2024-06-22 125743(1)](https://github.com/user-attachments/assets/38dd7251-52f9-4eb0-8fb4-bfb648dc45dc)

Showed all Movies with Pagination

# Movie Details

![Screenshot 2024-07-03 195535](https://github.com/user-attachments/assets/9d3b3b4e-c386-4203-9d77-4868833c0473)

![Pasted image 20240703194907](https://github.com/user-attachments/assets/174fb259-69e9-4efd-8243-cfa5043401b9)

![Screenshot 2024-07-03 194813](https://github.com/user-attachments/assets/42b38ab1-737d-47fc-a0f5-6462f24f8724)

## Adding Watch List

![Pasted image 20240703195447](https://github.com/user-attachments/assets/ff314444-43b9-413f-bca4-3d407948f9cf)

## Removing Watch List

![Pasted image 20240703195634](https://github.com/user-attachments/assets/bf2cbb5a-fc35-4ea3-a49d-04ad7ff76b6a)

# Watchlist section

![Pasted image 20240703190537](https://github.com/user-attachments/assets/b3f7a60d-07ad-444a-bef4-87ef6946cadb)

![Pasted image 20240703094103](https://github.com/user-attachments/assets/d354e201-d7ee-45e0-9866-41e4886cb02a)

# Search Page

![Screenshot 2024-07-03 201943](https://github.com/user-attachments/assets/2db01a86-b97c-42fd-b7cb-9db31e163c6c)

![Screenshot 2024-07-03 202045](https://github.com/user-attachments/assets/23520117-e151-480e-9d88-15bd308af5f6)

# Statistics Page

## Global

  ![Screenshot 2024-07-03 190909](https://github.com/user-attachments/assets/2f28251d-e65c-4658-b832-0b810eb89222)

  ![Screenshot 2024-07-03 190941](https://github.com/user-attachments/assets/b4f26256-75cd-42e4-a3cc-d2d30b7c7f27)

## Personal

![Screenshot 2024-07-03 191942](https://github.com/user-attachments/assets/36f9771b-c0d5-493c-82de-c6c28f2be0c9)

![Screenshot 2024-07-03 192221](https://github.com/user-attachments/assets/d69c2692-b155-4d3e-8b3a-f21ae0b8534d)

# Login / Registeration

![Pasted image 20240703202723](https://github.com/user-attachments/assets/fbdbfca7-5bf6-4b4e-97ff-b7489cb96a78)

![Pasted image 20240703202723](https://github.com/user-attachments/assets/e608394d-a694-4c55-8ef5-90d547fb6244)

# User Profile

![Screenshot 2024-07-03 203152](https://github.com/user-attachments/assets/36333673-8fde-43e6-bedd-3b3e914b1fc2)

![Pasted image 20240703203635](https://github.com/user-attachments/assets/41b78ff9-8410-44ba-857b-d3b2c4b1e1d8)

![Pasted image 20240703203741](https://github.com/user-attachments/assets/36874e78-f3bf-45a9-ac8d-0f092bd30d6e)

---

# Theory

## Collaborative filtering

Collaborative Filtering is a technique used in recommendation systems.

It is a method of making predictions about the interest of a user based on taste of many different users.

It has a basic assumption is that if a Person A has the same opinion or taste as other Person B then most likely they will have similar opinion on different topic.

### Types

- **Memory Based**: Uses user rating data to compute between users or items.
- **Model-Based**: Using machine learning model to predict user rating of unrated items.
- **Hybrid**: Using both Memory Based and Model Based, They overcome issues of both the types but are more complicated to compute.

![Pasted image 20240506235012 1](https://github.com/user-attachments/assets/54e70bc3-0c5e-415f-8cad-a62afe6732ec)

## Content based filtering

Content Based Filtering is a type of recommender systems, where we use item features to recommend other items similar to their interests.

In this features need to be hand engineered to make use of Content based filtering effectively.

![Pasted image 20240506231854](https://github.com/user-attachments/assets/06a71fce-0a0c-4177-bdc6-6c6224d7305c)

We use the utility matrix to define whether the specific person/ user should be recommended certain category.

We can use methods such as **dot products**, **cosine distances**


---

# Blog

I started this project at the beginning of my third year as part of my internship. Since I was learning along the way, some parts of the code might not be perfect. 😅

Most of the development was done independently. I built the web interface in 7-10 days, but spent 1.5 months researching recommendation systems to ensure a solid foundation. At the time, I wasn’t very experienced in web development, so some parts of the code might not follow best practices.

To run this project, the dataset needs to be imported into a MySQL database.

---

Thank you!
