import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "sansheng.py"


class SanshengCliTest(unittest.TestCase):
    def run_cli(self, *args, data_dir=None, check=True):
        env = os.environ.copy()
        if data_dir is not None:
            env["SANSHENG_DATA_DIR"] = str(data_dir)
        result = subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=ROOT,
            env=env,
            text=True,
            encoding="utf-8",
            capture_output=True,
        )
        if check and result.returncode != 0:
            self.fail(f"command failed: {result.args}\nstdout={result.stdout}\nstderr={result.stderr}")
        return result

    def test_create_dispatch_and_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            self.run_cli("init", data_dir=data_dir)
            created = self.run_cli(
                "create",
                "测试三省六部流程",
                "--request",
                "请验证任务流转",
                data_dir=data_dir,
            )
            task_id = created.stdout.split()[0]
            self.run_cli("plan", task_id, "先拟案再审议", "--step", "拟案", "--acceptance", "可报告", data_dir=data_dir)
            self.run_cli("state", task_id, "Menxia", "提交审议", "--actor", "zhongshu", data_dir=data_dir)
            self.run_cli("review", task_id, "approve", "准奏", "--actor", "menxia", data_dir=data_dir)
            self.run_cli("state", task_id, "Assigned", "准奏派发", "--actor", "menxia", data_dir=data_dir)
            self.run_cli("dispatch", task_id, "bingbu", "实现测试任务", data_dir=data_dir)
            self.run_cli("state", task_id, "Doing", "开始执行", "--actor", "shangshu", data_dir=data_dir)
            self.run_cli(
                "todo",
                task_id,
                "B1",
                "完成测试任务",
                "completed",
                "--owner",
                "bingbu",
                "--detail",
                "产出完成",
                data_dir=data_dir,
            )
            self.run_cli("done", task_id, "最终产出", "完成", "--actor", "shangshu", data_dir=data_dir)
            report = self.run_cli("report", task_id, data_dir=data_dir).stdout
            self.assertIn("最终回奏", report)
            self.assertIn("兵部", report)

            tasks = json.loads((data_dir / "tasks.json").read_text(encoding="utf-8"))
            self.assertEqual(tasks["tasks"][0]["state"], "Done")

    def test_illegal_transition_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            created = self.run_cli("create", "非法流转测试", data_dir=data_dir)
            task_id = created.stdout.split()[0]
            result = self.run_cli("state", task_id, "Done", "跳过审议", data_dir=data_dir, check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("illegal transition", result.stderr)

    def test_doctor(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            self.run_cli("init", data_dir=data_dir)
            result = self.run_cli("doctor", data_dir=data_dir)
            self.assertIn("doctor ok", result.stdout)


if __name__ == "__main__":
    unittest.main()
