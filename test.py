import pytest

def test_cd_conn():
    import mysql.connector as mysql
    conn = mysql.connect(host = 'spryrr1myu6oalwl.chr7pe7iynqr.eu-west-1.rds.amazonaws.com', port = '3306', user = 'jpj80vf0rrg10g3m', 
                    password = 'p46enny4y03h8tcb', database = 'qpgekjgzhdj91u8j')               # server2
    assert conn.is_connected() == True

if __name__ == '__main__':
    test_cd_conn()