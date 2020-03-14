import mysql.connector
import random
import string


def create_pass():
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(0, 20))


class Database:
    host = "localhost"
    user = "root"
    passwd = ""
    database = "schulplaner"

    # ----------------------------------------------------Initiate----------------------------------------------------#
    def __init__(self):
        self.init()

    def connect(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            database=self.database
        )

    def init(self):
        mydb = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd
        )
        mycursor = mydb.cursor()

        # Check if Database-Structure exists
        mycursor.execute("SHOW DATABASES LIKE '" + self.database + "'")

        found = {'database': False, 'groups': False, 'homework': False, 'exams': False, 'deleted_groups': False,
                 'deleted_homework': False, 'deleted_exams': False}
        result = mycursor.fetchone()
        if result:
            found['database'] = True
        if not found['database']:
            mycursor.execute("CREATE DATABASE " + self.database)
        mydb = self.connect()
        mycursor = mydb.cursor()

        databases = {"groups", "homework", "exams", "deleted_groups", "deleted_homework", "deleted_exams"}
        for x in databases:
            mycursor.execute("SHOW TABLES LIKE '%s'" % x)
            results = mycursor.fetchall()
            results_list = [item[0] for item in results]
            if x in results_list:
                found[x] = True
        if not found['groups']:
            mycursor.execute(
                "CREATE TABLE `" + self.database + "`.groups ( `id` INT(8) NOT NULL AUTO_INCREMENT, `name` TEXT "
                                                   "CHARACTER SET latin1 COLLATE latin1_german1_ci NOT NULL , "
                                                   "`pass` TEXT "
                                                   "CHARACTER SET latin1 COLLATE latin1_german1_ci NOT NULL , "
                                                   "`created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP , "
                                                   "PRIMARY KEY (`id`)) ENGINE = InnoDB;")
        if not found['homework']:
            mycursor.execute(
                "CREATE TABLE `" + self.database + "`.`homework` ( `id` INT(8) NOT NULL AUTO_INCREMENT, `group_id` "
                                                   "INT(8) NOT NULL , `date` INT(10) NOT NULL , `subject` TEXT "
                                                   "CHARACTER SET latin1 COLLATE latin1_german1_ci NOT NULL , "
                                                   "`homework` TEXT CHARACTER SET latin1 COLLATE latin1_german1_ci "
                                                   "NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;")
        if not found['exams']:
            mycursor.execute(
                "CREATE TABLE `" + self.database + "`.`exams` ( `id` INT(8) NOT NULL AUTO_INCREMENT, `group_id` INT("
                                                   "8) NOT NULL , `date` INT(10) NOT NULL , `subject` TEXT "
                                                   "CHARACTER SET latin1 COLLATE latin1_german1_ci NOT NULL , "
                                                   "`exam` TEXT CHARACTER SET latin1 COLLATE latin1_german1_ci NOT "
                                                   "NULL, PRIMARY KEY (`id`)) ENGINE = InnoDB;")
        if not found['deleted_groups']:
            mycursor.execute(
                "CREATE TABLE `" + self.database + "`.deleted_groups ( `id` INT(8) NOT NULL, `name` "
                                                   "TEXT "
                                                   "CHARACTER SET latin1 COLLATE latin1_german1_ci NOT NULL , "
                                                   "`pass` TEXT "
                                                   "CHARACTER SET latin1 COLLATE latin1_german1_ci NOT NULL , "
                                                   "`created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
                                                   ") ENGINE = InnoDB;")
        if not found['deleted_homework']:
            mycursor.execute(
                "CREATE TABLE `" + self.database + "`.`deleted_homework` ( `id` INT(8) NOT NULL, "
                                                   "`group_id` "
                                                   "INT(8) NOT NULL , `date` INT(10) NOT NULL , `subject` TEXT "
                                                   "CHARACTER SET latin1 COLLATE latin1_german1_ci NOT NULL , "
                                                   "`homework` TEXT CHARACTER SET latin1 COLLATE latin1_german1_ci "
                                                   "NOT NULL) ENGINE = InnoDB;")
        if not found['deleted_exams']:
            mycursor.execute(
                "CREATE TABLE `" + self.database + "`.`deleted_exams` ( `id` INT(8) NOT NULL, "
                                                   "`group_id` INT( "
                                                   "8) NOT NULL , `date` INT(10) NOT NULL , `subject` TEXT "
                                                   "CHARACTER SET latin1 COLLATE latin1_german1_ci NOT NULL , "
                                                   "`exam` TEXT CHARACTER SET latin1 COLLATE latin1_german1_ci NOT "
                                                   "NULL) ENGINE = InnoDB;")
        return

    # --------------------------------------------------Initiate end--------------------------------------------------#
    # -----------------------------------------------------Groups-----------------------------------------------------#
    # Creates a random password

    def create_group(self, name):
        mydb = self.connect()
        mycursor = mydb.cursor(dictionary=True)

        sql = "INSERT INTO groups (name, pass) VALUES (%s, %s)"
        password = create_pass()
        val = (name, password)
        mycursor.execute(sql, val)
        mydb.commit()
        group_id = mycursor.lastrowid
        return True, 201, {"group_id": group_id, "password": password}

    def get_group_name(self, group_id):
        mydb = self.connect()
        mycursor = mydb.cursor(dictionary=True)
        sql = "SELECT name FROM groups WHERE id=%s"
        val = group_id,
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        if myresult:
            return True, 200, myresult[0]
        else:
            return False, 404

    def change_group_pass(self, group_id, old_password):
        mydb = self.connect()
        mycursor = mydb.cursor(dictionary=True)

        sql = "SELECT * FROM deleted_groups WHERE id=%s"
        val = group_id,
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        if myresult.__len__() == 0:
            sql = "SELECT * FROM groups WHERE id=%s"
            val = group_id,
            mycursor.execute(sql, val)
            myresult = mycursor.fetchall()
            if myresult:
                sql = "SELECT * FROM groups WHERE id=%s AND pass=%s"
                val = (group_id, old_password)
                mycursor.execute(sql, val)
                myresult = mycursor.fetchall()
                if myresult:
                    sql = "UPDATE groups SET pass=%s WHERE id=%s"
                    password = create_pass()
                    val = (password, group_id)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    return True, 200, {"password": password}
                else:
                    return False, 401
            else:
                return False, 404
        else:
            return False, 410

    def change_group_name(self, group_id, name, password):
        mydb = self.connect()
        mycursor = mydb.cursor(dictionary=True)

        sql = "SELECT * FROM deleted_groups WHERE id=%s"
        val = group_id,
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        if myresult.__len__() == 0:
            sql = "SELECT * FROM groups WHERE id=%s"
            val = group_id,
            mycursor.execute(sql, val)
            myresult = mycursor.fetchall()
            if myresult:
                sql = "SELECT * FROM groups WHERE id=%s AND pass=%s"
                val = (group_id, password)
                mycursor.execute(sql, val)
                myresult = mycursor.fetchall()
                if myresult:
                    sql = "UPDATE groups SET name = %s WHERE id=%s"
                    val = (name, group_id)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    return True, 200
                else:
                    return False, 401
            else:
                return False, 404
        else:
            return False, 410

    def delete_group(self, group_id, password):
        mydb = self.connect()
        mycursor = mydb.cursor(dictionary=True)

        sql = "SELECT * FROM deleted_groups WHERE id=%s"
        val = group_id,
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        if myresult.__len__() == 0:
            sql = "SELECT * FROM groups WHERE id=%s"
            val = group_id,
            mycursor.execute(sql, val)
            myresult = mycursor.fetchall()
            if myresult:
                sql = "SELECT * FROM groups WHERE id=%s AND pass=%s"
                val = (group_id, password)
                mycursor.execute(sql, val)
                myresult = mycursor.fetchall()
                if myresult:
                    sql = "INSERT INTO deleted_groups (id, name, pass, created_at) SELECT " \
                          "id, name, pass, created_at FROM groups WHERE id=%s"
                    val = group_id,
                    mycursor.execute(sql, val)
                    mydb.commit()
                    sql = "DELETE FROM groups WHERE id=%s"
                    val = group_id,
                    mycursor.execute(sql, val)
                    mydb.commit()
                    sql = "INSERT INTO deleted_homework (id, group_id, date, subject, homework) SELECT " \
                          "id, group_id, date, subject, homework FROM homework WHERE group_id=%s"
                    val = group_id,
                    mycursor.execute(sql, val)
                    mydb.commit()
                    sql = "DELETE FROM homework WHERE group_id=%s"
                    val = group_id,
                    mycursor.execute(sql, val)
                    mydb.commit()
                    sql = "INSERT INTO deleted_exams (id, group_id, date, subject, exam) SELECT id, group_id, date, " \
                          "subject, exam FROM exams WHERE group_id=%s"
                    val = group_id,
                    mycursor.execute(sql, val)
                    mydb.commit()
                    sql = "DELETE FROM exams WHERE group_id=%s"
                    val = group_id,
                    mycursor.execute(sql, val)
                    mydb.commit()
                    return True, 204
                else:
                    return False, 401
            else:
                return False, 404
        else:
            return False, 410

    # Methods:
    # print(get_group_name(1))
    # print(delete_group(1, "01234567891012131415"))
    # print(change_group_pass(1, "01234567891012131415"))
    # print(create_group("groupOne"))
    # print(change_group_name(1, "Heyy", "01234567891012131415"))
    # ---------------------------------------------------Groups end---------------------------------------------------#

    # ----------------------------------------------------Homework----------------------------------------------------#
    def get_homework(self, group_id):
        mydb = self.connect()
        mycursor = mydb.cursor(dictionary=True)

        sql = "SELECT * FROM groups WHERE id=%s"
        val = group_id,
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        if myresult:
            sql = "SELECT * FROM homework WHERE group_id=%s"
            val = group_id,
            mycursor.execute(sql, val)
            result = mycursor.fetchall()
            if result.__len__() > 0:
                return True, 200, result[0]
            else:
                return False, 204
        else:
            return False, 404

    def add_homework(self, group_id, date, subject, homework, password):
        mydb = self.connect()
        mycursor = mydb.cursor(dictionary=True)
        sql = "SELECT * FROM groups WHERE id=%s"
        val = group_id,
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        if myresult:
            sql = "SELECT * FROM groups WHERE id=%s AND pass=%s"
            val = (group_id, password)
            mycursor.execute(sql, val)
            myresult = mycursor.fetchall()
            if myresult:
                sql = "INSERT INTO homework (group_id, date, subject, homework) VALUES (%s, %s, %s, %s)"
                val = (group_id, date, subject, homework)
                mycursor.execute(sql, val)
                mydb.commit()
                return True, 201
            else:
                return False, 401
        else:
            return False, 404

    def delete_homework(self, homework_id, group_id, password):
        mydb = self.connect()
        mycursor = mydb.cursor(dictionary=True)

        sql = "SELECT * FROM groups WHERE id=%s"
        val = group_id,
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        if myresult:
            sql = "SELECT * FROM groups WHERE id=%s AND pass=%s"
            val = (group_id, password)
            mycursor.execute(sql, val)
            myresult = mycursor.fetchall()
            if myresult:
                sql = "SELECT * FROM deleted_homework WHERE id=%s AND group_id=%s"
                val = (homework_id, group_id)
                mycursor.execute(sql, val)
                myresult = mycursor.fetchall()
                if myresult.__len__() == 0:
                    sql = "SELECT * FROM homework WHERE id=%s"
                    val = homework_id,
                    mycursor.execute(sql, val)
                    myresult = mycursor.fetchall()
                    if myresult:
                        sql = "INSERT INTO deleted_homework (id, group_id, date, subject, homework) SELECT " \
                              "id, group_id, date, subject, homework FROM homework WHERE id=%s"
                        val = homework_id,
                        mycursor.execute(sql, val)
                        mydb.commit()
                        sql = "DELETE FROM homework WHERE id=%s"
                        val = homework_id,
                        mycursor.execute(sql, val)
                        mydb.commit()
                        return True, 204
                    else:
                        return False, 404
                else:
                    return False, 410
            else:
                return False, 401
        else:
            return False, 404

    def edit_homework(self, homework_id, group_id, date, subject, homework, password):
        mydb = self.connect()
        mycursor = mydb.cursor(dictionary=True)

        sql = "SELECT * FROM groups WHERE id=%s"
        val = group_id,
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        if myresult:
            sql = "SELECT * FROM deleted_homework WHERE id=%s AND group_id=%s"
            val = (homework_id, group_id)
            mycursor.execute(sql, val)
            myresult = mycursor.fetchall()
            if myresult.__len__() == 0:
                sql = "SELECT * FROM groups WHERE id=%s AND pass=%s"
                val = (group_id, password)
                mycursor.execute(sql, val)
                myresult = mycursor.fetchall()
                if myresult:
                    sql = "SELECT * FROM homework WHERE id=%s"
                    val = homework_id,
                    mycursor.execute(sql, val)
                    myresult = mycursor.fetchall()
                    if myresult:
                        sql = "UPDATE homework SET group_id = %s, date = %s, subject = %s, homework = %s WHERE id=%s"
                        val = (group_id, date, subject, homework, homework_id)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        return True, 200
                    else:
                        return False, 404
                else:
                    return False, 401
            else:
                return False, 410
        else:
            return False, 404

    # Methods:
    # print(add_homework(1, 1010, "Math", "Something", "01234567891012131415"))
    # print(edit_homework(1, 1, 1020, "English", "something else", "01234567891012131415"))
    # print(delete_homework(1, 1, "01234567891012131415"))
    # print(get_homework(1))

    # --------------------------------------------------Homework end--------------------------------------------------#

    # ----------------------------------------------------Exams----------------------------------------------------#

    def get_exams(self, group_id):
        mydb = self.connect()
        mycursor = mydb.cursor(dictionary=True)

        sql = "SELECT * FROM groups WHERE id=%s"
        val = group_id,
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        if myresult:
            sql = "SELECT * FROM exams WHERE group_id=%s"
            val = group_id,
            mycursor.execute(sql, val)
            result = mycursor.fetchall()
            if result.__len__() > 0:
                return True, 200, result[0]
            else:
                return False, 204
        else:
            return False, 404

    def add_exam(self, group_id, date, subject, exam, password):
        mydb = self.connect()
        mycursor = mydb.cursor(dictionary=True)

        sql = "SELECT * FROM groups WHERE id=%s"
        val = group_id,
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        if myresult:
            sql = "SELECT * FROM groups WHERE id=%s AND pass=%s"
            val = (group_id, password)
            mycursor.execute(sql, val)
            myresult = mycursor.fetchall()
            if myresult:
                sql = "INSERT INTO exams (group_id, date, subject, exam) VALUES (%s, %s, %s, %s)"
                val = (group_id, date, subject, exam)
                mycursor.execute(sql, val)
                mydb.commit()
                return True, 201
            else:
                return False, 401
        else:
            return False, 404

    def delete_exam(self, exam_id, group_id, password):
        mydb = self.connect()
        mycursor = mydb.cursor(dictionary=True)

        sql = "SELECT * FROM groups WHERE id=%s"
        val = group_id,
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        if myresult:
            sql = "SELECT * FROM groups WHERE id=%s AND pass=%s"
            val = (group_id, password)
            mycursor.execute(sql, val)
            myresult = mycursor.fetchall()
            if myresult:
                sql = "SELECT * FROM deleted_exams WHERE id=%s AND group_id=%s"
                val = (exam_id, group_id)
                mycursor.execute(sql, val)
                myresult = mycursor.fetchall()
                if myresult.__len__() == 0:
                    sql = "SELECT * FROM exams WHERE id=%s"
                    val = exam_id,
                    mycursor.execute(sql, val)
                    myresult = mycursor.fetchall()
                    if myresult:
                        sql = "INSERT INTO deleted_exams (id, group_id, date, subject, exam) SELECT " \
                              "id, group_id, date, subject, exam FROM exams WHERE id=%s"
                        val = exam_id,
                        mycursor.execute(sql, val)
                        mydb.commit()
                        sql = "DELETE FROM exams WHERE id=%s"
                        val = exam_id,
                        mycursor.execute(sql, val)
                        mydb.commit()
                        return True, 204
                    else:
                        return False, 404
                else:
                    return False, 410
            else:
                return False, 401
        else:
            return False, 404

    def edit_exam(self, exam_id, group_id, date, subject, exam, password):
        mydb = self.connect()
        mycursor = mydb.cursor(dictionary=True)

        sql = "SELECT * FROM groups WHERE id=%s"
        val = group_id,
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        if myresult:
            sql = "SELECT * FROM deleted_exams WHERE id=%s AND group_id=%s"
            val = (exam_id, group_id)
            mycursor.execute(sql, val)
            myresult = mycursor.fetchall()
            if myresult.__len__() == 0:
                sql = "SELECT * FROM groups WHERE id=%s AND pass=%s"
                val = (group_id, password)
                mycursor.execute(sql, val)
                myresult = mycursor.fetchall()
                if myresult:
                    sql = "SELECT * FROM exams WHERE id=%s"
                    val = exam_id,
                    mycursor.execute(sql, val)
                    myresult = mycursor.fetchall()
                    if myresult:
                        sql = "UPDATE exams SET group_id = %s, date = %s, subject = %s, exam = %s WHERE id=%s"
                        val = (group_id, date, subject, exam, exam_id)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        return True, 200
                    else:
                        return False, 404
                else:
                    return False, 401
            else:
                return False, 410
        else:
            return False, 404

    # Methods:
    # print(add_exam(1, 1010, "Math", "Something", "01234567891012131415"))
    # print(edit_exam(1, 1, 1020, "English", "something else", "01234567891012131415"))
    # print(delete_exam(1, 1, "01234567891012131415"))
    # print(get_exams(1))

    # --------------------------------------------------Exams end--------------------------------------------------#
    # init()


# Testing:
# Console colors and formatting
class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def test():
    database = Database()
    default_test_group_name = "Test01"
    success = 0
    failed = 0

    print(BColors.OKBLUE + "Testing groups" + BColors.ENDC)
    test_group = database.create_group(default_test_group_name)
    print("Created test_group: %s" % (test_group,))

    print("Get name:")
    temp_obj = database.get_group_name(test_group[2]['group_id'])
    if temp_obj[2]['name'] == default_test_group_name:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Get wrong name:")
    temp_obj = database.get_group_name(test_group[2]['group_id'] + 1)
    if temp_obj[1] == 404:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1

    print("Change pass: ")
    temp_obj = database.change_group_pass(test_group[2]['group_id'], test_group[2]['password'])
    newPass = temp_obj[2]
    if temp_obj[1] == 200:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Change wrong pass: ")
    temp_obj = database.change_group_pass(test_group[2]['group_id'], test_group[2]['password'])
    if temp_obj[1] == 401:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Change wrong group pass: ")
    temp_obj = database.change_group_pass(test_group[2]['group_id'] + 1, test_group[2]['password'])
    if temp_obj[1] == 404:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1

    print("Change group_name: ")
    temp_obj = database.change_group_name(test_group[2]['group_id'], "Hallo", newPass)
    if temp_obj[1] == 200:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Change wrong pass name: ")
    temp_obj = database.change_group_name(test_group[2]['group_id'], "Hallo", test_group[2]['password'])
    if temp_obj[1] == 401:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Change wrong group name: ")
    temp_obj = database.change_group_name(test_group[2]['group_id'] + 1, "Hallo", newPass)
    if temp_obj[1] == 404:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1

    print("Delete wrong group: ")
    temp_obj = database.delete_group(test_group[2]['group_id'] + 1, test_group[2]['password'])
    if temp_obj[1] == 404:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Delete wrong pass: ")
    temp_obj = database.delete_group(test_group[2]['group_id'], test_group[2]['password'])
    if temp_obj[1] == 401:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Delete group: ")
    temp_obj = database.delete_group(test_group[2]['group_id'], newPass)
    if temp_obj[1] == 204:
        print(BColors.OKGREEN + "Success " + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed:" + BColors.ENDC, temp_obj)
        failed += 1
    print("Delete group again: ")
    temp_obj = database.delete_group(test_group[2]['group_id'], newPass)
    if temp_obj[1] == 410:
        print(BColors.OKGREEN + "Success " + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed:" + BColors.ENDC, temp_obj)
        failed += 1
    print("Change pass after deleted: ")
    temp_obj = database.change_group_pass(test_group[2]['group_id'], test_group[2]['password'])
    if temp_obj[1] == 410:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Change name after deleted: ")
    temp_obj = database.change_group_name(test_group[2]['group_id'], "Hey", test_group[2]['password'])
    if temp_obj[1] == 410:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1

    print(BColors.OKBLUE + "Groups test done" + BColors.ENDC)

    print(BColors.OKBLUE + "Testing exams" + BColors.ENDC)
    test_group = database.create_group(default_test_group_name)
    groupID = test_group[2]['group_id']
    groupPass = test_group[2]['password']
    print("Created test_group: %s" % (test_group,))
    print("Get exam without adding one first:")
    temp_obj = database.get_exams(groupID)
    if temp_obj[1] == 204:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Create testExam with wrong pass:")
    temp_obj = database.add_exam(groupID, 1583770158, "Math", "Test", groupPass + "1")
    if temp_obj[1] == 401:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Create testExam with wrong GroupID:")
    temp_obj = database.add_exam(groupID + 1, 1583770158, "Math", "Test", groupPass)
    if temp_obj[1] == 404:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Create testExam:")
    temp_obj = database.add_exam(groupID, 1583770158, "Math", "Test", groupPass)
    if temp_obj[1] == 201:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1

    print("Getting all testExam for wrong group:")
    temp_obj = database.get_exams(groupID + 1)
    if temp_obj[1] == 404:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Getting all testExam for group:")
    temp_obj = database.get_exams(groupID)
    if temp_obj[1] == 200 and temp_obj[2][0]['group_id'] == groupID and temp_obj[2][0]['date'] == 1583770158 and \
            temp_obj[2][0]['subject'] == "Math" and temp_obj[2][0]['exam'] == "Test":
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1

    testExam = temp_obj[2][0]
    print("Edit testExam for wrong group:")
    temp_obj = database.edit_exam(testExam['id'], groupID + 1, 1583770159, "English", "Test02", groupPass)
    if temp_obj[1] == 404:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Edit wrong testExam:")
    temp_obj = database.edit_exam(testExam['id'] + 1, groupID, 1583770159, "English", "Test02", groupPass)
    if temp_obj[1] == 404:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Edit testExam for wrong pass:")
    temp_obj = database.edit_exam(testExam['id'], groupID, 1583770159, "English", "Test02", groupPass + "1")
    if temp_obj[1] == 401:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Edit testExam:")
    temp_obj = database.edit_exam(testExam['id'], groupID, 1583770159, "English", "Test02", groupPass)
    if temp_obj[1] == 200:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1

    print("Delete testExam for wrong group:")
    temp_obj = database.delete_exam(testExam['id'], groupID + 1, groupPass)
    if temp_obj[1] == 404:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Delete wrong testExam:")
    temp_obj = database.delete_exam(testExam['id'] + 1, groupID, groupPass)
    if temp_obj[1] == 404:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Delete testExam for wrong pass:")
    temp_obj = database.delete_exam(testExam['id'], groupID, groupPass + "1")
    if temp_obj[1] == 401:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Delete testExam:")
    temp_obj = database.delete_exam(testExam['id'], groupID, groupPass)
    if temp_obj[1] == 204:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Delete testExam again:")
    temp_obj = database.delete_exam(testExam['id'], groupID, groupPass)
    if temp_obj[1] == 410:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Edit testExam after deleted:")
    temp_obj = database.edit_exam(testExam['id'], groupID, 1583770159, "English", "Test02", groupPass)
    if temp_obj[1] == 410:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Delete test_group: %s" % (database.delete_group(groupID, groupPass),))

    print(BColors.OKBLUE + "Exam test done" + BColors.ENDC)

    print(BColors.OKBLUE + "Testing homework" + BColors.ENDC)
    test_group = database.create_group(default_test_group_name)
    groupID = test_group[2]['group_id']
    groupPass = test_group[2]['password']
    print("Created test_group: %s" % (test_group,))
    print("Get homework without adding one first:")
    temp_obj = database.get_homework(groupID)
    if temp_obj[1] == 204:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Create testHomework with wrong pass:")
    temp_obj = database.add_homework(groupID, 1583770158, "Math", "Test", groupPass + "1")
    if temp_obj[1] == 401:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Create testHomework with wrong GroupID:")
    temp_obj = database.add_homework(groupID + 1, 1583770158, "Math", "Test", groupPass)
    if temp_obj[1] == 404:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Create testHomework:")
    temp_obj = database.add_homework(groupID, 1583770158, "Math", "Test", groupPass)
    if temp_obj[1] == 201:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1

    print("Getting all testHomework for wrong group:")
    temp_obj = database.get_homework(groupID + 1)
    if temp_obj[1] == 404:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
    print("Getting all testHomework for group:")
    temp_obj = database.get_homework(groupID)
    if temp_obj[1] == 200 and temp_obj[2][0]['group_id'] == groupID and temp_obj[2][0]['date'] == 1583770158 and \
            temp_obj[2][0]['subject'] == "Math" and temp_obj[2][0]['homework'] == "Test":
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1

    testHomework = temp_obj[2][0]
    print("Edit testHomework for wrong group:")
    temp_obj = database.edit_homework(testHomework['id'], groupID + 1, 1583770159, "English", "Test02", groupPass)
    if temp_obj[1] == 404:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Edit wrong testHomework:")
    temp_obj = database.edit_homework(testHomework['id'] + 1, groupID, 1583770159, "English", "Test02", groupPass)
    if temp_obj[1] == 404:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Edit testHomework for wrong pass:")
    temp_obj = database.edit_homework(testHomework['id'], groupID, 1583770159, "English", "Test02", groupPass + "1")
    if temp_obj[1] == 401:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Edit testHomework:")
    temp_obj = database.edit_homework(testHomework['id'], groupID, 1583770159, "English", "Test02", groupPass)
    if temp_obj[1] == 200:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1

    print("Delete testHomework for wrong group:")
    temp_obj = database.delete_homework(testHomework['id'], groupID + 1, groupPass)
    if temp_obj[1] == 404:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Delete wrong testHomework:")
    temp_obj = database.delete_homework(testHomework['id'] + 1, groupID, groupPass)
    if temp_obj[1] == 404:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Delete testHomework for wrong pass:")
    temp_obj = database.delete_homework(testHomework['id'], groupID, groupPass + "1")
    if temp_obj[1] == 401:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Delete testHomework:")
    temp_obj = database.delete_homework(testHomework['id'], groupID, groupPass)
    if temp_obj[1] == 204:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Delete testHomework again:")
    temp_obj = database.delete_homework(testHomework['id'], groupID, groupPass)
    if temp_obj[1] == 410:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Edit testHomework after deleted:")
    temp_obj = database.edit_homework(testHomework['id'], groupID, 1583770159, "English", "Test02", groupPass)
    if temp_obj[1] == 410:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Delete test_group: %s" % (database.delete_group(groupID, groupPass),))

    print(BColors.OKBLUE + "Homework test done" + BColors.ENDC)
    print(
        BColors.OKBLUE + BColors.BOLD + "All Tests done! " + BColors.ENDC +
        BColors.WARNING + "Success:", "{0},".format(str(success)), "Failed:", "{0},".format(str(failed)),
        "Successrate:", "{0}%".format((success / (success + failed) * 100)))


# test()
