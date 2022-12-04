import pytest

def test_cd_conn():
    import mysql.connector as mysql
    conn = mysql.connect(host = 'spryrr1myu6oalwl.chr7pe7iynqr.eu-west-1.rds.amazonaws.com', port = '3306', user = 'oyqw7racyiwryzq3', 
                    password = 'v9rfrsbqk1om7rwe', database = 'i9ihdbgoe8d4no07')             # server1
    assert conn.is_connected() == True

if __name__ == '__main__':
    test_cd_conn()