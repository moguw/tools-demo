import os
import shutil
import subprocess

ALLURE_RESULTS_DIR = "allure-results"
ALLURE_REPORT_DIR = "allure-report"
HISTORY_DIR = os.path.join(ALLURE_RESULTS_DIR, "history")

def copy_history(src, dst):
    if os.path.exists(src):
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

def run_tests():
    if not os.path.exists(ALLURE_RESULTS_DIR):
        os.makedirs(ALLURE_RESULTS_DIR)

    # Copy history from previous report to results directory
    previous_history_dir = os.path.join(ALLURE_REPORT_DIR, "history")
    copy_history(previous_history_dir, HISTORY_DIR)

    # Run Playwright tests with pytest and allure
    subprocess.run(["pytest", "--alluredir", ALLURE_RESULTS_DIR], check=True)

    # Generate allure report
    subprocess.run(["allure", "generate", ALLURE_RESULTS_DIR, "-o", ALLURE_REPORT_DIR, "--clean"], check=True)

    # Copy new history to results directory
    copy_history(os.path.join(ALLURE_REPORT_DIR, "history"), HISTORY_DIR)

    # Open the allure report
    subprocess.run(["allure", "open", ALLURE_REPORT_DIR])

if __name__ == "__main__":
    run_tests()
