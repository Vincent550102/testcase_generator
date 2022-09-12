import os
import time
import sys
import subprocess


class Testcase_Generator():
    def __init__(self, _excutable_file):
        self.in_dir = 'in'
        self.out_dir = 'out'
        if not os.path.exists(_excutable_file):
            raise(Exception("找不到此執行檔"))
        self.excutable_file = _excutable_file

    def runner(self, _testcase_in):
        testcase_in = os.path.join(  # gen xlsx
            os.getcwd(),
            self.in_dir,
            _testcase_in)

        out = subprocess.Popen(
            f"{self.excutable_file} < {testcase_in}",
            stdout=subprocess.PIPE,
            shell=True).communicate()
        if out[1] is not None:
            raise(out[1])

        testcase_in_name = _testcase_in.split(".")[0]
        testcase_out = os.path.join(  # gen xlsx
            os.getcwd(),
            self.out_dir,
            f"{testcase_in_name}.out")

        fo = open(testcase_out, "w")
        fo.write(out[0].decode('utf-8'))
        fo.close()

    def read_testcases_in(self):
        testcases_in = os.listdir(self.in_dir)
        for testcase_in in testcases_in:
            if testcase_in.split(
                    '.')[-1] != 'in' and testcase_in != '.gitkeep':
                raise(Exception(f"{self.in_dir} 中包含副檔名不為 .in 的檔案"))

        return testcases_in

    def run(self):
        testcases_in = self.read_testcases_in()
        for testcase_in in testcases_in:
            time_start = time.time()
            self.runner(testcase_in)
            time_end = time.time()
            print(f"✔️{testcase_in} 運行成功，已成功生成測試資料輸出。 運行時間：{time_end-time_start} s")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'使用方式: python {__file__} <excutable file>')
        sys.exit()
    try:
        testcase_generator = Testcase_Generator(sys.argv[1])
        testcase_generator.run()
    except Exception as e:
        print(f"❌發生問題：{e}")
