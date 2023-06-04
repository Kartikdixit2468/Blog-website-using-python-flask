# import smtplib

# rec_email = "kartikdixt8595@gmail.com"
# my_email = "kartikdixt2468@gmail.com"
# password = "DontTellYou5"
# message = "Hi there"

# with smtplib.SMTP(host="smtp.gmail.com", port=465) as connection:
#     connection.starttls()
#     connection.login(user=my_email, password=password)
#     connection.sendmail(
#         from_addr=my_email,
#         to_addrs=rec_email,
#         msg=message.encode("utf-8")
#         )

str_1 = "kartik is a good boy"
str2 = str_1[0:16].replace(" ", "-")
print(str2)

