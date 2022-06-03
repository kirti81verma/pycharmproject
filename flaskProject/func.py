from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, desc, func,select

print(select(func.concat('a', 'b')))
print(func.concat('="' + 'BankDetail.acc_number' + '"'))