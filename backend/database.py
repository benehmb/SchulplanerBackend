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
                "CREATE TABLE `" + self.database + "`.`exams` ( `id` INT(8) NOT NULL, `group_id` INT("
                                                   "8) NOT NULL , `date` INT(10) NOT NULL , `subject` TEXT "
                                                   "CHARACTER SET latin1 COLLATE latin1_german1_ci NOT NULL , "
                                                   "`exam` TEXT CHARACTER SET latin1 COLLATE latin1_german1_ci NOT "
                                                   "NULL) ENGINE = InnoDB;")
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
                "CREATE TABLE `" + self.database + "`.`deleted_exams` ( `id` INT(8) NOT NULL AUTO_INCREMENT, "
                                                   "`group_id` INT( "
                                                   "8) NOT NULL , `date` INT(10) NOT NULL , `subject` TEXT "
                                                   "CHARACTER SET latin1 COLLATE latin1_german1_ci NOT NULL , "
                                                   "`exam` TEXT CHARACTER SET latin1 COLLATE latin1_german1_ci NOT "
                                                   "NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;")
        return

    # --------------------------------------------------Initiate end--------------------------------------------------#
    # -----------------------------------------------------Groups-----------------------------------------------------#
    # Creates a random password

    def create_group(self, name):
        mydb = self.connect()
        mycursor = mydb.cursor()

        sql = "INSERT INTO groups (name, pass) VALUES (%s, %s)"
        password = create_pass()
        val = (name, password)
        mycursor.execute(sql, val)
        mydb.commit()
        group_id = mycursor.lastrowid
        return True, 201, {"group_id": group_id, "password": password}

    def get_group_name(self, group_id):
        mydb = self.connect()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT name FROM groups WHERE id=%s" % group_id)
        myresult = mycursor.fetchall()
        if myresult:
            return True, 200, myresult[0][0]
        else:
            return False, 404

    # todo check ig group is already deleted
    def change_group_pass(self, group_id, old_password):
        mydb = self.connect()
        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM groups WHERE id=%s" % group_id)
        myresult = mycursor.fetchall()
        if myresult:
            mycursor.execute("SELECT * FROM groups WHERE id='%s' AND pass='%s'" % (group_id, old_password,))
            myresult = mycursor.fetchall()
            if myresult:
                sql = "UPDATE groups SET pass = %s WHERE id = %s;"
                password = create_pass()
                val = (password, group_id)

                mycursor.execute(sql, val)
                mydb.commit()
                return True, 200, password
            else:
                return False, 401
        else:
            return False, 404

    # todo check ig group is already deleted
    def change_group_name(self, group_id, name, password):
        mydb = self.connect()
        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM groups WHERE id=%s" % group_id)
        myresult = mycursor.fetchall()
        if myresult:
            mycursor.execute("SELECT * FROM groups WHERE id='%s' AND pass='%s'" % (group_id, password,))
            myresult = mycursor.fetchall()
            if myresult:
                sql = "UPDATE groups SET name = %s WHERE id = %s;"
                val = (name, group_id)
                mycursor.execute(sql, val)
                mydb.commit()
                return True, 200
            else:
                return False, 401
        else:
            return False, 404

    # todo check ig group is already deleted
    def delete_group(self, group_id, password):
        mydb = self.connect()
        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM groups WHERE id=%s" % group_id)
        myresult = mycursor.fetchall()
        mydb.commit()
        if myresult:
            mycursor.execute("SELECT * FROM groups WHERE id='%s' AND pass='%s'" % (group_id, password,))
            myresult = mycursor.fetchall()
            if myresult:
                mycursor.execute("INSERT INTO deleted_groups (id, name, pass, created_at) SELECT id, name, pass, created_at FROM groups WHERE id = '%s'" % group_id)
                # todo do this for DELETE FROM homework and DELETE FROM exams
                mydb.commit()
                sql = "DELETE FROM groups WHERE id = '%s'" % group_id
                mycursor.execute(sql)
                mydb.commit()
                sql = "DELETE FROM homework WHERE group_id = '%s';" % group_id
                mycursor.execute(sql)
                mydb.commit()
                sql = "DELETE FROM exams WHERE group_id = '%s';" % group_id
                mycursor.execute(sql)
                mydb.commit()
                return True, 204
            else:
                return False, 401
        else:
            return False, 404

    # Methods:
    # print(get_group_name(1))
    # print(delete_group(1, "01234567891012131415"))
    # print(change_group_pass(1, "01234567891012131415"))
    # print(create_group("groupOne"))
    # print(change_group_name(1, "Heyy", "01234567891012131415"))
    # ---------------------------------------------------Groups end---------------------------------------------------#

    # ----------------------------------------------------Homework----------------------------------------------------#
    # todo make test if group exists and there are homework to return
    def get_homework(self, group_id):
        mydb = self.connect()
        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM groups WHERE id=%s" % group_id)
        myresult = mycursor.fetchall()
        mydb.commit()
        if myresult:
            sql = "SELECT * FROM homework WHERE group_id = '%s'" % group_id
            mycursor.execute(sql)
            result = mycursor.fetchall()
            mydb.commit()
            return True, 200, result
        else:
            return False, 404

    def add_homework(self, group_id, date, subject, homework, password):
        mydb = self.connect()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM groups WHERE id=%s" % group_id)
        myresult = mycursor.fetchall()
        mydb.commit()
        if myresult:
            mycursor.execute("SELECT * FROM groups WHERE id='%s' AND pass='%s'" % (group_id, password,))
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

    # todo make test if homework is deleted
    def delete_homework(self, homework_id, group_id, password):
        mydb = self.connect()
        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM groups WHERE id=%s" % group_id)
        myresult = mycursor.fetchall()
        mydb.commit()
        if myresult:
            mycursor.execute("SELECT * FROM groups WHERE id='%s' AND pass='%s'" % (group_id, password,))
            myresult = mycursor.fetchall()
            if myresult:
                mycursor.execute("SELECT * FROM homework WHERE id = %s" % homework_id)
                myresult = mycursor.fetchall()
                if myresult:
                    sql = "DELETE FROM homework WHERE id = '%s'" % homework_id
                    mycursor.execute(sql)
                    mydb.commit()
                    return True, 204
                else:
                    return False, 404
            else:
                return False, 401
        else:
            return False, 404

    # todo make test if homework is deleted
    def edit_homework(self, homework_id, group_id, date, subject, homework, password):
        mydb = self.connect()
        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM groups WHERE id=%s" % group_id)
        myresult = mycursor.fetchall()
        mydb.commit()
        if myresult:
            mycursor.execute("SELECT * FROM groups WHERE id='%s' AND pass='%s'" % (group_id, password,))
            myresult = mycursor.fetchall()
            if myresult:
                mycursor.execute("SELECT * FROM homework WHERE id=%s" % homework_id)
                myresult = mycursor.fetchall()
                mydb.commit()
                if myresult:
                    sql = "UPDATE homework SET group_id = %s, date = %s, subject = %s, homework = %s WHERE id = %s;"
                    val = (group_id, date, subject, homework, homework_id)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    return True, 200
                else:
                    return False, 404
            else:
                return False, 401
        else:
            return False, 404

    # Methods:
    # print(add_homework(1, 1010, "Math", "Something", "01234567891012131415"))
    # print(edit_homework(1, 1, 1020, "English", "something else", "01234567891012131415"))
    # print(delete_homework(1, 1, "01234567891012131415"))
    # print(get_homework(1))

    # --------------------------------------------------Homework end--------------------------------------------------#

    # ----------------------------------------------------Homework----------------------------------------------------#

    # todo make test if there are exams to return
    def get_exams(self, group_id):
        mydb = self.connect()
        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM groups WHERE id=%s" % group_id)
        myresult = mycursor.fetchall()
        mydb.commit()
        if myresult:
            sql = "SELECT * FROM exams WHERE group_id = '%s'" % group_id
            mycursor.execute(sql)
            result = mycursor.fetchall()
            mydb.commit()
            return True, 200, result
        else:
            return False, 404

    def add_exam(self, group_id, date, subject, exam, password):
        mydb = self.connect()
        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM groups WHERE id=%s" % group_id)
        myresult = mycursor.fetchall()
        mydb.commit()
        if myresult:
            mycursor.execute("SELECT * FROM groups WHERE id='%s' AND pass='%s'" % (group_id, password,))
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

    # todo make test if exam is deleted
    def delete_exam(self, exam_id, group_id, password):
        mydb = self.connect()
        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM groups WHERE id=%s" % group_id)
        myresult = mycursor.fetchall()
        mydb.commit()
        if myresult:
            mycursor.execute("SELECT * FROM groups WHERE id='%s' AND pass='%s'" % (group_id, password,))
            myresult = mycursor.fetchall()
            if myresult:
                mycursor.execute("SELECT * FROM exams WHERE id = %s" % exam_id)
                myresult = mycursor.fetchall()
                if myresult:
                    sql = "DELETE FROM exams WHERE id = '%s'" % exam_id
                    mycursor.execute(sql)
                    mydb.commit()
                    return True, 204
                else:
                    return False, 404
            else:
                return False, 401
        else:
            return False, 404

    # todo make test if exam is deleted
    def edit_exam(self, exam_id, group_id, date, subject, exam, password):
        mydb = self.connect()
        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM groups WHERE id=%s" % group_id)
        myresult = mycursor.fetchall()
        mydb.commit()
        if myresult:
            mycursor.execute("SELECT * FROM exams WHERE id=%s" % exam_id)
            myresult = mycursor.fetchall()
            mydb.commit()
            if myresult:
                mycursor.execute("SELECT * FROM groups WHERE id='%s' AND pass='%s'" % (group_id, password,))
                myresult = mycursor.fetchall()
                if myresult:
                    sql = "UPDATE exams SET group_id = %s, date = %s, subject = %s, exam = %s WHERE id = %s;"
                    val = (group_id, date, subject, exam, exam_id)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    return True, 200
                else:
                    return False, 401
            else:
                return False, 404
        else:
            return False, 404

    # Methods:
    # print(add_exam(1, 1010, "Math", "Something", "01234567891012131415"))
    # print(edit_exam(1, 1, 1020, "English", "something else", "01234567891012131415"))
    # print(delete_exam(1, 1, "01234567891012131415"))
    # print(get_exams(1))

    # --------------------------------------------------Homework end--------------------------------------------------#
    # init()


# todo check if Password-test works
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


database = Database()
defaultTestGroupName = "Test01"
success = 0
failed = 0

print(BColors.OKBLUE + "Testing groups" + BColors.ENDC)
testGroup = database.create_group(defaultTestGroupName)
print("Created testGroup: %s" % (testGroup,))

print("Get name:")
tempObj = database.get_group_name(testGroup[2]['group_id'])
if tempObj[2] == defaultTestGroupName:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Get wrong name:")
tempObj = database.get_group_name(testGroup[2]['group_id'] + 1)
if tempObj[1] == 404:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1

print("Change pass: ")
tempObj = database.change_group_pass(testGroup[2]['group_id'], testGroup[2]['password'])
newPass = tempObj[2]
if tempObj[1] == 200:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Change wrong pass: ")
tempObj = database.change_group_pass(testGroup[2]['group_id'], testGroup[2]['password'])
if tempObj[1] == 401:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Change wrong group pass: ")
tempObj = database.change_group_pass(testGroup[2]['group_id'] + 1, testGroup[2]['password'])
if tempObj[1] == 404:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1

print("Delete wrong group: ")
tempObj = database.delete_group(testGroup[2]['group_id'] + 1, testGroup[2]['password'])
if tempObj[1] == 404:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Delete wrong pass: ")
tempObj = database.delete_group(testGroup[2]['group_id'], testGroup[2]['password'])
if tempObj[1] == 401:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Delete group: ")
tempObj = database.delete_group(testGroup[2]['group_id'], newPass)
if tempObj[1] == 204:
    print(BColors.OKGREEN + "Success " + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed:" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Delete group again: ")
tempObj = database.delete_group(testGroup[2]['group_id'], newPass)
if tempObj[1] == 410:
    print(BColors.OKGREEN + "Success " + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed:" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Change pass after deleted: ")
tempObj = database.change_group_pass(testGroup[2]['group_id'], testGroup[2]['password'])
if tempObj[1] == 410:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1

print(BColors.OKBLUE + "Groups test done" + BColors.ENDC)

print(BColors.OKBLUE + "Testing exams" + BColors.ENDC)
testGroup = database.create_group(defaultTestGroupName)
groupID = testGroup[2]['group_id']
groupPass = testGroup[2]['password']
print("Created testGroup: %s" % (testGroup,))

print("Create testExam with wrong pass:")
tempObj = database.add_exam(groupID, 1583770158, "Math", "Test", groupPass + "1")
if tempObj[1] == 401:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Create testExam with wrong GroupID:")
tempObj = database.add_exam(groupID + 1, 1583770158, "Math", "Test", groupPass)
if tempObj[1] == 404:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Create testExam:")
tempObj = database.add_exam(groupID, 1583770158, "Math", "Test", groupPass)
if tempObj[1] == 201:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1

print("Getting all testExam for wrong group:")
tempObj = database.get_exams(groupID + 1)
if tempObj[1] == 404:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Getting all testExam for group:")
tempObj = database.get_exams(groupID)
if tempObj[1] == 200 and tempObj[2][0][1] == groupID and tempObj[2][0][2] == 1583770158 and tempObj[2][0][3] == "Math" \
        and tempObj[2][0][4] == "Test":
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1

testExam = tempObj[2][0]
print("Edit testExam for wrong group:")
tempObj = database.edit_exam(testExam[0], groupID + 1, 1583770159, "English", "Test02", groupPass)
if tempObj[1] == 404:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Edit wrong testExam:")
tempObj = database.edit_exam(testExam[0] + 1, groupID, 1583770159, "English", "Test02", groupPass)
if tempObj[1] == 404:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Edit testExam for wrong pass:")
tempObj = database.edit_exam(testExam[0], groupID, 1583770159, "English", "Test02", groupPass + "1")
if tempObj[1] == 401:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Edit testExam:")
tempObj = database.edit_exam(testExam[0], groupID, 1583770159, "English", "Test02", groupPass)
if tempObj[1] == 200:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1

print("Delete testExam for wrong group:")
tempObj = database.delete_exam(testExam[0], groupID + 1, groupPass)
if tempObj[1] == 404:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Delete wrong testExam:")
tempObj = database.delete_exam(testExam[0] + 1, groupID, groupPass)
if tempObj[1] == 404:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Delete testExam for wrong pass:")
tempObj = database.delete_exam(testExam[0], groupID, groupPass + "1")
if tempObj[1] == 401:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Delete testExam:")
tempObj = database.delete_exam(testExam[0], groupID, groupPass)
if tempObj[1] == 204:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Delete testExam again:")
tempObj = database.delete_exam(testExam[0], groupID, groupPass)
if tempObj[1] == 410:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Edit testExam after deleted:")
tempObj = database.edit_exam(testExam[0], groupID, 1583770159, "English", "Test02", groupPass)
if tempObj[1] == 410:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Delete testGroup: %s" % (database.delete_group(groupID, groupPass),))

print(BColors.OKBLUE + "Exam test done" + BColors.ENDC)

print(BColors.OKBLUE + "Testing homework" + BColors.ENDC)
testGroup = database.create_group(defaultTestGroupName)
groupID = testGroup[2]['group_id']
groupPass = testGroup[2]['password']
print("Created testGroup: %s" % (testGroup,))

print("Create testHomework with wrong pass:")
tempObj = database.add_homework(groupID, 1583770158, "Math", "Test", groupPass + "1")
if tempObj[1] == 401:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Create testHomework with wrong GroupID:")
tempObj = database.add_homework(groupID + 1, 1583770158, "Math", "Test", groupPass)
if tempObj[1] == 404:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Create testHomework:")
tempObj = database.add_homework(groupID, 1583770158, "Math", "Test", groupPass)
if tempObj[1] == 201:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1

print("Getting all testHomework for wrong group:")
tempObj = database.get_homework(groupID + 1)
if tempObj[1] == 404:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
print("Getting all testHomework for group:")
tempObj = database.get_homework(groupID)
if tempObj[1] == 200 and tempObj[2][0][1] == groupID and tempObj[2][0][2] == 1583770158 and tempObj[2][0][3] == "Math" \
        and tempObj[2][0][4] == "Test":
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1

testHomework = tempObj[2][0]
print("Edit testHomework for wrong group:")
tempObj = database.edit_homework(testHomework[0], groupID + 1, 1583770159, "English", "Test02", groupPass)
if tempObj[1] == 404:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Edit wrong testHomework:")
tempObj = database.edit_homework(testHomework[0] + 1, groupID, 1583770159, "English", "Test02", groupPass)
if tempObj[1] == 404:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Edit testHomework for wrong pass:")
tempObj = database.edit_homework(testHomework[0], groupID, 1583770159, "English", "Test02", groupPass + "1")
if tempObj[1] == 401:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Edit testHomework:")
tempObj = database.edit_homework(testHomework[0], groupID, 1583770159, "English", "Test02", groupPass)
if tempObj[1] == 200:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1

print("Delete testHomework for wrong group:")
tempObj = database.delete_homework(testHomework[0], groupID + 1, groupPass)
if tempObj[1] == 404:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Delete wrong testHomework:")
tempObj = database.delete_homework(testHomework[0] + 1, groupID, groupPass)
if tempObj[1] == 404:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Delete testHomework for wrong pass:")
tempObj = database.delete_homework(testHomework[0], groupID, groupPass + "1")
if tempObj[1] == 401:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Delete testHomework:")
tempObj = database.delete_homework(testHomework[0], groupID, groupPass)
if tempObj[1] == 204:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Delete testHomework again:")
tempObj = database.delete_homework(testHomework[0], groupID, groupPass)
if tempObj[1] == 410:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Edit testHomework after deleted:")
tempObj = database.edit_homework(testHomework[0], groupID, 1583770159, "English", "Test02", groupPass)
if tempObj[1] == 410:
    print(BColors.OKGREEN + "Success" + BColors.ENDC, tempObj)
    success = success + 1
else:
    print(BColors.FAIL + "Failed" + BColors.ENDC, tempObj)
    failed = failed + 1
print("Delete testGroup: %s" % (database.delete_group(groupID, groupPass),))

print(BColors.OKBLUE + "Homework test done" + BColors.ENDC)
print(
    BColors.OKBLUE + BColors.BOLD + "All Tests done! " + BColors.ENDC +
    BColors.WARNING + "Success:", success,  "Failed:", failed, "Successrate:",
    (success / (success + failed) * 100), "%")

# todo test sql-injections
