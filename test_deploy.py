import yaml
from checkers import getout
from ssh_lesson4 import ssh_checkout, upload_files, ssh_getout, ssh_checkout_negative


with open('config4.yaml') as f:
   data = yaml.safe_load(f)

class TestPositive:

    def save_log(self, starttime, name, func):
        with open(name, 'a') as f:
            f.write(f'---------------------{func}------------------------\n\n')
            f.write(getout("journalctl --since '{}'".format(starttime)) + '\n')


    def test_step1(self, start_time):
        res = []
        upload_files(data.get("ip"), data.get("user"), data.get("passwd"), data.get("local_path"),
                     data.get("remote_path"))
        res.append(ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"),
                                f'echo {data.get("passwd")} | sudo -S dpkg -i {data.get("remote_path")}',
                                "Настраивается пакет"))
        res.append(ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"),
                                f'echo {data.get("passwd")} | sudo -S dpkg -s {data.get("filename")}',
                                "Status: install ok installed"))
        self.save_log(start_time, "log_deploy_test.txt", "test_step1")
        assert all(res), "test1 FAIL"

    def test_step2(self, make_folders, clear_folders, make_files, start_time):
        res1 = ssh_checkout(data["ip"], data["user"], data["passwd"],
                            "cd {}; 7z a -t{} {}/arx2".format(data["folder_in"], data['type'], data["folder_out"]),
                            "Everything is Ok")
        res2 = ssh_checkout(data["ip"], data["user"], data["passwd"],
                            "ls {}".format(data["folder_out"]),
                            f"arx2.{data['type']}")
        self.save_log(start_time, "log_deploy_test.txt", "test_step2")
        assert res1 and res2, "test2 FAIL"

    def test_step3(self, clear_folders, make_files, start_time):
        res = []
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                "cd {}; 7z a -t{} {}/arx2".format(data["folder_in"], data['type'], data["folder_out"]),
                                "Everything is Ok"))
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                "cd {}; 7z e arx2.{} -o{} -y".format(data["folder_out"], data['type'], data["folder_ext"]),
                                "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], "ls {}".format(data["folder_ext"]), item))
        self.save_log(start_time, "log_deploy_test.txt", "test_step3")
        assert all(res), "test3 FAIL"

    def test_step4(self, start_time):
        self.save_log(start_time, "log_deploy_test.txt", "test_step4")
        assert ssh_checkout(data["ip"], data["user"], data["passwd"],
                            "cd {}; 7z t arx2.{}".format(data["folder_out"], data['type']),
                            "Everything is Ok"), "test4 FAIL"

    def test_step5(self, start_time):
        self.save_log(start_time, "log_deploy_test.txt", "test_step5")
        assert ssh_checkout(data["ip"], data["user"], data["passwd"],
                            "cd {}; 7z u arx2.{}".format(data["folder_in"], data['type']),
                            "Everything is Ok"), "test5 FAIL"

    def test_step6(self, clear_folders, make_files, start_time):
        res = []
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                "cd {}; 7z a -t{} {}/arx2".format(data["folder_in"], data['type'], data["folder_out"]),
                                "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                    "cd {}; 7z l arx2.{}".format(data["folder_out"], data['type'], data["folder_ext"]), item))
        self.save_log(start_time, "log_deploy_test.txt", "test_step6")
        assert all(res), "test6 FAIL"

    def test_step7(self, clear_folders, make_files, make_subfolder, start_time):
        res = []
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                "cd {}; 7z a -t{} {}/arx".format(data["folder_in"], data['type'], data["folder_out"]),
                                "Everything is Ok"))
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                "cd {}; 7z x arx.{} -o{} -y".format(data["folder_out"], data['type'], data["folder_ext2"]),
                                "Everything is Ok"))
        self.save_log(start_time, "log_deploy_test.txt", "test_step7")
        assert all(res), "test7 FAIL"

    def test_step8(self, start_time):
        self.save_log(start_time, "log_deploy_test.txt", "test_step8")
        assert ssh_checkout(data["ip"], data["user"], data["passwd"],
                            "cd {}; 7z d arx.{}".format(data["folder_out"], data['type']),
                            "Everything is Ok"), "test8 FAIL"

    def test_step9(self, clear_folders, make_files, start_time):
        res = []
        for item in make_files:
            res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                    "cd {}; 7z h {}".format(data["folder_in"], item),
                                    "Everything is Ok"))
            hash = ssh_getout(data["ip"], data["user"], data["passwd"],
                              "cd {}; crc32 {}".format(data["folder_in"], item)).upper()
            res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                    "cd {}; 7z h {}".format(data["folder_in"], item),
                                    hash))
        self.save_log(start_time, "log_deploy_test.txt", "test_step9")
        assert all(res), "test9 FAIL"

    def test_step10(self, start_time):
        res = []
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                "echo '{}' | sudo -S dpkg -r {}".format(data["passwd"], data["filename"]),
                                "Удаляется"))
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                "echo '{}' | sudo -S dpkg -s {}".format(data["passwd"], data["filename"]),
                                "Status: deinstall ok"))
        self.save_log(start_time, "log_deploy_test.txt", "test_step10")
        assert all(res), "test10 FAIL"

class TestNegative:

    def save_log(self, starttime, name, func):
        with open(name, 'a') as f:
            f.write(f'---------------------{func}------------------------\n\n')
            f.write(getout("journalctl --since '{}'".format(starttime)) + '\n')

    def test_negstep1(self, make_folders, make_bad_arx, start_time):
        self.save_log(start_time, "log_deploy_negtest.txt", "test_negstep1")
        assert ssh_checkout_negative(data["ip"], data["user"], data["passwd"],
                                     "cd {}; 7z e {}.{} -o{} -y".format(data["folder_out"], make_bad_arx, data["type"], data["folder_ext"]),
                                     "ERROR:"), "test1 FAIL"

    def test_negstep2(self, make_bad_arx, start_time):
        self.save_log(start_time, "log_deploy_negtest.txt", "test_negstep2")
        assert ssh_checkout_negative(data["ip"], data["user"], data["passwd"],
                                     "cd {}; 7z t {}.{}".format(data["folder_out"], make_bad_arx, data["type"]),
                                     "ERROR:"), "test2 FAIL"

    def test_negstep3(self, start_time):
        res = []
        res.append(ssh_checkout_negative(data["ip"], data["user"], data["passwd"],
                                "echo '{}' | sudo -S dpkg -r {}".format(data["passwd"], data["filename"]),
                                "Удаляется"))
        res.append(ssh_checkout_negative(data["ip"], data["user"], data["passwd"],
                                "echo '{}' | sudo -S dpkg -s {}".format(data["passwd"], data["filename"]),
                                "Status: deinstall ok"))
        self.save_log(start_time, "log_deploy_negtest.txt", "test_negstep3")
        assert all(res), "test3 FAIL"

