from sql.configDB import MyDB
import hashlib

def ex_sql():
    db = MyDB()
    db.connectDB(database='i61', host='10.60.7.62')
    sql_all = '''SELECT userid,account FROM `userinfo` ORDER BY userid ASC;'''
    cursor_all = db.executeSQL(sql_all)
    rt = db.get_all(cursor_all)
    not_update = []
    for r in rt:
        new_list = ['123'+r[1][3:], '111'+r[1][3:], '112'+r[1][3:], '113'+r[1][3:], '114'+r[1][3:], '115'+r[1][3:], '116'+r[1][3:], '117'+r[1][3:]]
        # new = '123'+r[1][3:]
        for new in new_list:
            # sql_dup = '''SELECT * FROM `userinfo` WHERE account='{}';'''.format(new)
            sql_dup = '''SELECT * FROM `userinfo` WHERE account='{}' AND userid={};'''.format(new, r[0])
            cursor_dup = db.executeSQL(sql_dup)
            dup = db.get_one(cursor_dup)
            if dup is not None:
                print(r[0])
                break

            else:

                # sql_dup2 = '''SELECT * FROM `userinfo` WHERE account='{}' AND userid={};'''.format(new, r[0])
                sql_dup2 = '''SELECT * FROM `userinfo` WHERE account='{}';'''.format(new)
                cursor_dup2 = db.executeSQL(sql_dup2)
                dup2 = db.get_one(cursor_dup2)
                if dup2 is None:
                    sql_update = '''update `userinfo` set account='{}' where userid={};'''.format(new, r[0])
                    cursor_update = db.executeSQL(sql_update)
                    update = db.get_all(cursor_update)
                    print(update)
                    break

                else:
                    if (r not in not_update) and (r[1][:3] not in ['123', '111', '112', '113', '114', '115', '116', '117']):
                        print(r)
                        not_update.append(r)
                    continue


    for n in not_update:
        print(n)

    db.closeDB()

def encrypt_student_password(account, password):
    # 学生密码加密，直接写入数据库
    if account and password:
        account_byte = str(account).encode(encoding='utf-8')
        password_byte = str(password).encode(encoding='utf-8')

        md = hashlib.md5()
        md.update(password_byte)
        password_md5 = md.hexdigest()

        md = hashlib.md5()
        md.update(account_byte)
        account_md5 = md.hexdigest()

        # print('password_md5: '+ password_md5)
        # print('account_md5: '+account_md5)

        password_md5_byte = str(password_md5).encode(encoding='utf-8')

        md = hashlib.md5()
        md.update(password_md5_byte)
        password_double_md5 = md.hexdigest()
        # print('password_double_md5: '+password_double_md5)

        combination_str = ''
        for i in range(len(account_md5)):

            ascii_sum = ord(account_md5[i]) + ord(password_double_md5[i])       # ascii码数值之和
            combination_str = combination_str + str(ascii_sum)

        combination_byte = combination_str.encode(encoding='utf-8')
        md = hashlib.md5()
        md.update(combination_byte)
        combination_md5 = md.hexdigest()
        return combination_md5

def update_usersecurityinfo():
    not_userid = []
    error = []
    db = MyDB()
    db.connectDB(database='i61', host='10.60.7.62')
    sql_userid = '''select userid from `usersecurityinfo` ORDER BY userid ASC;'''
    cursor_userid = db.executeSQL(sql_userid)
    userid_tup = db.get_all(cursor_userid)
    print(userid_tup)

    for u in userid_tup:
        userid = u[0]
        print(userid)
        sql_account = '''SELECT account FROM `userinfo` WHERE userid={};'''.format(userid)
        cursor_account = db.executeSQL(sql_account)
        account = db.get_one(cursor_account)
        print(account)
        if account is None:
            not_userid.append(userid)
        else:
            password = encrypt_student_password(account=account[0], password='000000')
            sql_update = '''UPDATE `usersecurityinfo` SET account='{}', password='{}' WHERE userid={};'''.format(account[0], password, userid)
            cursor_update = db.executeSQL(sql_update)
            update = db.get_all(cursor_update)
            print(update)
            if update != ():
                error.append((userid,update))

    account = 0
    for nu in not_userid:
        print(nu)
        account += 1
    print('account of not_userid: {}'.format(account))

    print('################################################')
    for e in error:
        print(e)

    db.closeDB()



def main():
    # ex_sql()

    # p = '098d6bb820b56e8413cac932fd71b306'
    en_p = encrypt_student_password('18800000001', '123456')
    print(en_p)
    # if en_p == p:
    #     print('yes')
    # update_usersecurityinfo()

    
if __name__ == '__main__':
    main()

