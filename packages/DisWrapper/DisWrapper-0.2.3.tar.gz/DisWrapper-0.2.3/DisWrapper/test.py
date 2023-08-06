from wrapper import DisWrapper

test = DisWrapper()

test.auth("scraggjoshua@gmail.com", "ek63KbW41Ked")

user = test.getUserInfo("275475207651590146")
print(user.user_id, user.username)