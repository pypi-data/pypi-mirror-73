'''a not so secure otp library for python. created by sanjay marison.use this library to send otp for valid purpose only
different functions in the module
1)send_otp() - takes one argument(the mail of the person you are sending)
2)resend_otp() - takes no argument , use this only if you have used the send_otp function to send the otp to the person the first time
3)get_otp() - takes no argument use this to print the otp that has been generated
4)custom_otp() - takes one argument (the otp which you want to send), use this if you want to send your own otp
5)resend_custom_otp() - takes no argument , use this only if you have used the custom_otp function to send the otp to the person the first time
6)custom_mail() - takes three arguments (your mail id , your password for mail id ,otp(type "OTP" if you want to use the randomly generated
                   otp) use this function if you want to use your own mail to send the otp
7)resend_custom_mail() - takes no argument , use this only if you have used the custom_mail function to send the otp to the person the first time
'''


'''
**note /  when using the predefined mail id for sending otp 
the coder of the library that's me is having access to that mail but promises that he will not use it , if you do not trust him ,
you can use the custom_mail(),resend_custom_mail() command which uses the mail provided by you to send the otp to your client
i am not sure if you can create an mail account for sending otp , if you can please mail me the methods to do it at marisonsanjay@gmail.com'''

'''
***note / when sending otp using custom mail
if you want to use the already generated otp to send the mail , just give the fourth argument of the function as "OTP"
'''
import random #importing random for generating a random otp
import smtplib #importing smtplib for sending the otp to the recipient



OTP = random.randint(100000,999999) #generates random otp

#these values will be changed later
resend_otp_mail = ""
resend_custom_otp_mail = ""
resend_custom_otp_otp = ""
v = ""
b = ""
n = ""
m = ""


'''use send_otp to send otp to the mail id using another predefined mail id , if you want to change the mail 
of the predefined mail is used the custom mail , the function accepts one value which is the mail id you want to send'''


def send_otp(*args): #completed
    EMAIL_ADRESS = "pythonprojectmail1@gmail.com" #do not misuse the mail
    EMAIL_PASSWORD = "vrzdoskkghtvhyjv" #do not misuse the password
    SENDERSMAILID = str(*args)

    #saving the mail id if we want to use it again to resend the otp
    resend_otp_mail = str(*args)

    body_otp = "YOUR OTP IS:",OTP,".","DO NOT SHARE YOUR OTP WITH ANYONE" #this is the body of the mail which also contains the otp


    #sending otp to the person
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)

        subject = "MAIL TO VERIFY ACCOUNT" #do not declare th otp here
        body = body_otp

        msg = f'subject:{subject}\n\n{body}'

        smtp.sendmail(SENDERSMAILID, EMAIL_ADRESS, msg)


'''use this function to resend otp only if you have used the send_otp() function the first time'''
def resend_otp(): #completed
    EMAIL_ADRESS = "pythonprojectmail1@gmail.com" #do not misuse the mail
    EMAIL_PASSWORD = "vrzdoskkghtvhyjv" #do not misuse the password
    SENDERSMAILID = resend_otp_mail
    body_otp = "YOUR OTP IS:", OTP, ".", "DO NOT SHARE YOUR OTP WITH ANYONE"

    # sending otp to the person
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)

        subject = "MAIL TO VERIFY ACCOUNT"  #do not declare th otp here
        body = body_otp

        msg = f'subject:{subject}\n\n{body}'

        smtp.sendmail(SENDERSMAILID, EMAIL_ADRESS, msg)


def custom_otp(*args,**kwargs): #completed
    EMAIL_ADRESS = "pythonprojectmail1@gmail.com" #do not misuse the mail
    EMAIL_PASSWORD = "vrzdoskkghtvhyjv" #do not misuse the password
    SENDERSMAILID = str(**kwargs)
    resend_custom_otp_mail = str(**kwargs)
    resend_custom_otp_otp = int(*args)
    body_otp = "YOUR OTP IS:",str(*args) , ".", "DO NOT SHARE YOUR OTP WITH ANYONE"

    # sending otp to the person
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)

        subject = "MAIL TO VERIFY ACCOUNT"  #do not declare th otp here
        body = body_otp

        msg = f'subject:{subject}\n\n{body}'

        smtp.sendmail(SENDERSMAILID, EMAIL_ADRESS, msg)

def resend_custom_otp(): #completed
    EMAIL_ADRESS = "pythonprojectmail1@gmail.com" #do not misuse the mail
    EMAIL_PASSWORD = "vrzdoskkghtvhyjv" #do not misuse the password
    SENDERSMAILID = resend_custom_otp_mail
    body_otp = "YOUR OTP IS:",str(resend_custom_otp_otp), ".", "DO NOT SHARE YOUR OTP WITH ANYONE"

    # sending otp to the person
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)

        subject = "MAIL TO VERIFY ACCOUNT"  #do not declare th otp here
        body = body_otp

        msg = f'subject:{subject}\n\n{body}'

        smtp.sendmail(SENDERSMAILID, EMAIL_ADRESS, msg)



def get_otp(): #completed
    print(OTP)

def custom_mail(first,second,third,fourth): #completed
    EMAIL_ADRESS = str(first)
    EMAIL_PASSWORD =  str(second)
    SENDERSMAILID = str(third)
    v = str(first)
    b = str(second)
    n = str(third)
    m = str(fourth)
    body_otp = "YOUR OTP IS:", str(fourth), ".", "DO NOT SHARE YOUR OTP WITH ANYONE"

    # sending otp to the person
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)

        subject = "MAIL TO VERIFY ACCOUNT"  # do not declare th otp here
        body = body_otp

        msg = f'subject:{subject}\n\n{body}'

        smtp.sendmail(SENDERSMAILID, EMAIL_ADRESS, msg)


def resend_custom_mail(): #completed
    EMAIL_ADRESS = v
    EMAIL_PASSWORD = b
    SENDERSMAILID = n
    body_otp = "YOUR OTP IS:",m,".","DO NOT SHARE YOUR OTP WITH ANYONE"

    # sending otp to the person
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)

        subject = "MAIL TO VERIFY ACCOUNT"  # do not declare th otp here
        body = body_otp

        msg = f'subject:{subject}\n\n{body}'

        smtp.sendmail(SENDERSMAILID, EMAIL_ADRESS, msg)
    return




'''this library was created by sanjay marison, please feel free contact me for any queries or any other problems,improvements to my code at 
marisonsanjay@gmail.com, thank you for using my code.'''