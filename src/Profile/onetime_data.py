import pandas as pd
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from Profile.models import WatchList
from Movies.models import Movies
import warnings

warnings.filterwarnings("ignore")
ratings = pd.read_csv("E:/Internship/data/ratings_cleaned_v1.csv", sep="\t")
users_data = pd.read_csv("E:/Internship/data/user_data.csv", sep="\t")


# Lists that are going to be used
user = []
watches = []
# important metadata

user_limit = 10_000

# Functions
print("Dowloading Content $user$....")
ignore = 2000
for i in range(ignore, users_data.shape[0]):
    if i >= 10_000:
        break
    use_pass = users_data.at[i, "password"]
    user.append(User(username=use_pass, password=make_password(use_pass)))
    print("stored in list upto {}/{}...".format(i, user_limit), end="\r")
    bulk = 1000
    if len(user) >= bulk:
        User.objects.bulk_create(user)
        user = []
        print(
            "\nstored $user$ bulk {}/{}...".format(user_limit / i, user_limit / bulk),
            end="\r",
        )
if user:
    User.objects.bulk_create(user)

print("Finished $user$ Table upto: {}".format(i))
del user

# for i, j in enumerate(ratings.index, 1):
#     print("Dowloading Content $watchlist$....")
#     uid = ratings.at[j, "userId"]
#     mid = ratings.at[j, "movieId"]
#     rating = ratings.at[j, "rating"]
#     timestamp = ratings.at[j, "date_time"]
#     watches.append(
#         WatchList(
#             uid=User.objects.get(id=uid),
#             m_id=Movies(id=mid),
#             rating=rating,
#             timestamp=timestamp,
#         )
#     )
#     if len(watches) == 1000:
#         WatchList.objects.bulk_create(watches)
#         watches = []
#         print("Done {0:,}".format(i), end="\r")
#     print("Data {:,}".format(i), end="\r")
# if watches:
#     WatchList.objects.bulk_create(watches)
#
#     print("Total Data Imported {}".format(len(ratings)))
