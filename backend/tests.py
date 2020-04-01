from backend.database import *


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
    newPass = temp_obj[2]['password']
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

    print("Check if Password is correct for wrong group: ")
    temp_obj = database.check_group_pass(test_group[2]['group_id'] + 1, test_group[2]['password'])
    if temp_obj[1] == 404:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Check if Password is correct with wrong password: ")
    temp_obj = database.check_group_pass(test_group[2]['group_id'], test_group[2]['password'] + "1")
    if temp_obj[1] == 401:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Check if Password is correct: ")
    temp_obj = database.check_group_pass(test_group[2]['group_id'], newPass)
    if temp_obj[1] == 200:
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
    print("Check if Password is correct for deleted group: ")
    temp_obj = database.check_group_pass(test_group[2]['group_id'], test_group[2]['password'])
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
    temp_obj = database.add_exam(groupID,
                                 calendar.timegm((datetime.date.today()).timetuple()),
                                 "Math", "Test", groupPass + "1")
    if temp_obj[1] == 401:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Create testExam with wrong GroupID:")
    temp_obj = database.add_exam(groupID + 1,
                                 calendar.timegm((datetime.date.today()).timetuple()),
                                 "Math", "Test", groupPass)
    if temp_obj[1] == 404:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Create testExam:")
    temp_obj = database.add_exam(groupID,
                                 calendar.timegm((datetime.date.today()).timetuple()),
                                 "Math", "Test", groupPass)
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
    if temp_obj[1] == 200 and temp_obj[2][0]['group_id'] == groupID and temp_obj[2][0]['date'] == calendar.timegm(
            (datetime.date.today()).timetuple()) and \
            temp_obj[2][0]['subject'] == "Math" and temp_obj[2][0]['exam'] == "Test":
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1

    testExam = temp_obj[2][0]
    print("Edit testExam for wrong group:")
    temp_obj = database.edit_exam(testExam['id'], groupID + 1,
                                  calendar.timegm((datetime.date.today()).timetuple()),
                                  "English", "Test02", groupPass)
    if temp_obj[1] == 404:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Edit wrong testExam:")
    temp_obj = database.edit_exam(testExam['id'] + 1, groupID,
                                  calendar.timegm((datetime.date.today()).timetuple()),
                                  "English", "Test02", groupPass)
    if temp_obj[1] == 404:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Edit testExam for wrong pass:")
    temp_obj = database.edit_exam(testExam['id'], groupID,
                                  calendar.timegm((datetime.date.today()).timetuple()),
                                  "English", "Test02", groupPass + "1")
    if temp_obj[1] == 401:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Edit testExam:")
    temp_obj = database.edit_exam(testExam['id'], groupID,
                                  calendar.timegm((datetime.date.today()).timetuple()),
                                  "English", "Test02", groupPass)
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
    temp_obj = database.edit_exam(testExam['id'], groupID,
                                  calendar.timegm((datetime.date.today()).timetuple()),
                                  "English", "Test02", groupPass)
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
    temp_obj = database.add_homework(groupID, calendar.timegm(
        (datetime.date.today()).timetuple()), "Math", "Test", groupPass + "1")
    if temp_obj[1] == 401:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Create testHomework with wrong GroupID:")
    temp_obj = database.add_homework(groupID + 1, calendar.timegm(
        (datetime.date.today()).timetuple()), "Math", "Test", groupPass)
    if temp_obj[1] == 404:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Create testHomework:")
    temp_obj = database.add_homework(groupID, calendar.timegm(
        (datetime.date.today()).timetuple()), "Math", "Test", groupPass)
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
    if temp_obj[1] == 200 and temp_obj[2][0]['group_id'] == groupID and temp_obj[2][0]['date'] == calendar.timegm(
            (datetime.date.today()).timetuple()) and \
            temp_obj[2][0]['subject'] == "Math" and temp_obj[2][0]['homework'] == "Test":
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1

    testHomework = temp_obj[2][0]
    print("Edit testHomework for wrong group:")
    temp_obj = database.edit_homework(testHomework['id'], groupID + 1, calendar.timegm(
        (datetime.date.today()).timetuple()), "English", "Test02", groupPass)
    if temp_obj[1] == 404:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Edit wrong testHomework:")
    temp_obj = database.edit_homework(testHomework['id'] + 1, groupID, calendar.timegm(
        (datetime.date.today()).timetuple()), "English", "Test02", groupPass)
    if temp_obj[1] == 404:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Edit testHomework for wrong pass:")
    temp_obj = database.edit_homework(testHomework['id'], groupID, calendar.timegm(
        (datetime.date.today()).timetuple()), "English", "Test02", groupPass + "1")
    if temp_obj[1] == 401:
        print(BColors.OKGREEN + "Success" + BColors.ENDC, temp_obj)
        success += 1
    else:
        print(BColors.FAIL + "Failed" + BColors.ENDC, temp_obj)
        failed += 1
    print("Edit testHomework:")
    temp_obj = database.edit_homework(testHomework['id'], groupID, calendar.timegm(
        (datetime.date.today()).timetuple()), "English", "Test02", groupPass)
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
    temp_obj = database.edit_homework(testHomework['id'], groupID, calendar.timegm(
        (datetime.date.today()).timetuple()), "English", "Test02", groupPass)
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


test()
